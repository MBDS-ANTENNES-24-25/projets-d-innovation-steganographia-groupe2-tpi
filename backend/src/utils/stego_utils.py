import json, uuid, zlib, base64
from io import BytesIO
from typing import Optional
from PIL import Image

# chiffrement symétrique
from cryptography.fernet import Fernet
# chiffrement asymétrique
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

EOF_MARKER = '1111111111111110'  # fin de flux LSB (1 octet 0xFE)

# -------------------------
# utilitaires bits <-> str
# -------------------------
def _str_to_bits(s: str) -> str:
    return ''.join(format(ord(c), '08b') for c in s)

def _bits_to_str(bits: str) -> str:
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

# -------------------------
# enveloppe / encryptions
# -------------------------
def _encrypt_payload(payload_bytes: bytes, mode: str,
                     fernet_key: Optional[bytes]=None,
                     rsa_public_pem: Optional[bytes]=None) -> bytes:
    if mode == "none":
        return payload_bytes
    if mode == "aes":
        if not fernet_key:
            raise ValueError("fernet_key required for aes mode")
        f = Fernet(fernet_key)
        return f.encrypt(payload_bytes)
    if mode == "rsa":
        if not rsa_public_pem:
            raise ValueError("rsa_public_pem required for rsa mode")
        pub = serialization.load_pem_public_key(rsa_public_pem)
        encrypted = pub.encrypt(
            payload_bytes,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        return encrypted
    raise ValueError("unsupported encryption mode")

def _decrypt_payload(data_bytes: bytes, mode: str,
                     fernet_key: Optional[bytes]=None,
                     rsa_private_pem: Optional[bytes]=None) -> bytes:
    if mode == "none":
        return data_bytes
    if mode == "aes":
        if not fernet_key:
            raise ValueError("fernet_key required for aes mode")
        f = Fernet(fernet_key)
        return f.decrypt(data_bytes)
    if mode == "rsa":
        if not rsa_private_pem:
            raise ValueError("rsa_private_pem required for rsa mode")
        priv = serialization.load_pem_private_key(rsa_private_pem, password=None)
        decrypted = priv.decrypt(
            data_bytes,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        return decrypted
    raise ValueError("unsupported encryption mode")

# -------------------------
# Embedding / Extraction LSB
# -------------------------
def _embed_string_into_image_bytes(image_bytes: bytes, s: str) -> BytesIO:
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    pixels = img.load()
    bits = _str_to_bits(s) + EOF_MARKER
    bit_index = 0
    max_bits = img.width * img.height * 3
    if len(bits) > max_bits:
        raise ValueError("Payload too large for this image")

    for y in range(img.height):
        for x in range(img.width):
            if bit_index >= len(bits):
                break
            r, g, b = pixels[x, y]
            if bit_index < len(bits):
                r = (r & ~1) | int(bits[bit_index]); bit_index += 1
            if bit_index < len(bits):
                g = (g & ~1) | int(bits[bit_index]); bit_index += 1
            if bit_index < len(bits):
                b = (b & ~1) | int(bits[bit_index]); bit_index += 1
            pixels[x, y] = (r, g, b)

    out = BytesIO()
    img.save(out, format="PNG")  # sauvegarde en PNG pour préserver bits
    out.seek(0)
    return out

def _extract_string_from_image_bytes(image_bytes: bytes) -> str:
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    pixels = img.load()
    bits = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)
    s = _bits_to_str(bits)
    # découpe avant EOF marker byte (\xFE)
    s = s.split(chr(int("11111110", 2)))[0]
    return s

# -------------------------
# Fonctions publiques
# -------------------------
def embed_data_into_image(image_bytes: bytes, author_id: int, message: str,
                          mode: str = "none",
                          fernet_key: Optional[bytes]=None,
                          rsa_public_pem: Optional[bytes]=None,
                          signature_uuid: Optional[str] = None) -> BytesIO:
    if signature_uuid is None:
        signature_uuid = str(uuid.uuid4())
        
    payload = {
        "author_id": author_id,
        "signature_uuid": signature_uuid,
        "message": message
    }
    payload_json = json.dumps(payload).encode()           # bytes
    compressed = zlib.compress(payload_json)              # bytes

    encrypted = _encrypt_payload(compressed, mode, fernet_key, rsa_public_pem)  # bytes
    envelope = {
        "mode": mode,
        "data": base64.b64encode(encrypted).decode("ascii")
    }
    envelope_bytes = json.dumps(envelope).encode()  
    envelope_str = envelope_bytes.decode("latin1")
    out = _embed_string_into_image_bytes(image_bytes, envelope_str)
    return out, signature_uuid

def extract_data_from_image(image_bytes: bytes,
                            fernet_key: Optional[bytes]=None,
                            rsa_private_pem: Optional[bytes]=None) -> dict:
    envelope_str = _extract_string_from_image_bytes(image_bytes)
    envelope_bytes = envelope_str.encode("latin1")
    envelope = json.loads(envelope_bytes.decode())

    mode = envelope.get("mode")
    data_b64 = envelope.get("data")
    if data_b64 is None:
        raise ValueError("No data field in envelope")

    encrypted_bytes = base64.b64decode(data_b64)
    compressed = _decrypt_payload(encrypted_bytes, mode, fernet_key, rsa_private_pem)
    payload_json = zlib.decompress(compressed)
    payload = json.loads(payload_json.decode())
    return payload
