import math
import cv2
import numpy as np
import zlib
import hashlib
import random
import base64
import os
from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy.orm import Session


class SteganoDCTService:
    """
    Service de stéganographie utilisant la transformation DCT (Discrete Cosine Transform)
    avec chiffrement AES-GCM et dérivation de clé PBKDF2.
    """
    
    BLOCK = 8
    
    def __init__(self, db: Session):
        self.db = db
    
    # ---------- AES helpers (AES-GCM + PBKDF2) ----------
    def _derive_key(self, password: str, salt: bytes, iterations: int = 100_000, length: int = 32) -> bytes:
        """Dérive une clé cryptographique à partir d'un mot de passe et d'un sel."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            iterations=iterations,
        )
        return kdf.derive(password.encode())

    def aes_encrypt(self, plaintext: bytes, password: str) -> bytes:
        """
        Chiffre des données avec AES-GCM.
        Return bytes: salt(16) || nonce(12) || tag+ciphertext
        """
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext, associated_data=None)  # ct contains tag at the end
        return salt + nonce + ct

    def aes_decrypt(self, payload: bytes, password: str) -> bytes:
        """
        Déchiffre des données avec AES-GCM.
        payload = salt(16) || nonce(12) || ct_with_tag
        """
        if len(payload) < 16 + 12 + 16:
            raise ValueError("Payload AES trop court")
        salt = payload[:16]
        nonce = payload[16:28]
        ct = payload[28:]
        key = self._derive_key(password, salt)
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ct, associated_data=None)

    # ---------- DCT stego (adapted to embed arbitrary bytes) ----------
    def _blocks_from_channel(self, channel: np.ndarray):
        """Divise un canal d'image en blocs 8x8 pour la transformation DCT."""
        h, w = channel.shape
        pad_h = (self.BLOCK - (h % self.BLOCK)) % self.BLOCK
        pad_w = (self.BLOCK - (w % self.BLOCK)) % self.BLOCK
        channel_p = np.pad(channel, ((0, pad_h), (0, pad_w)), mode='constant', constant_values=0)
        H, W = channel_p.shape
        blocks = channel_p.reshape(H // self.BLOCK, self.BLOCK, W // self.BLOCK, self.BLOCK).swapaxes(1,2).reshape(-1, self.BLOCK, self.BLOCK)
        return blocks, channel.shape, (H, W)

    def _channel_from_blocks(self, blocks: np.ndarray, orig_shape: Tuple[int,int], padded_shape: Tuple[int,int]):
        """Reconstruit un canal d'image à partir des blocs 8x8."""
        bh = padded_shape[0] // self.BLOCK
        bw = padded_shape[1] // self.BLOCK
        arr = blocks.reshape(bh, bw, self.BLOCK, self.BLOCK).swapaxes(1,2).reshape(padded_shape)
        return arr[:orig_shape[0], :orig_shape[1]]

    def _select_mid_coeff_positions(self) -> Tuple[int,int]:
        """Sélectionne les positions des coefficients DCT de fréquence moyenne."""
        return (3, 2)

    def _bit_to_delta(self, bit: int, strength: float):
        """Convertit un bit en delta de modification pour les coefficients DCT."""
        return strength if bit == 1 else -strength

    def _int_to_bits(self, x: int, length: int):
        """Convertit un entier en liste de bits."""
        return [(x >> i) & 1 for i in range(length)][::-1]

    def _bits_to_int(self, bits):
        """Convertit une liste de bits en entier."""
        x = 0
        for b in bits:
            x = (x << 1) | int(b)
        return x

    # ---------- Embedding (now accepts bytes payload) ----------
    def embed_message_bytes(
        self,
        in_path: str,
        out_path: str,
        payload_bytes: bytes,
        key: str,
        strength: float = 20.0,
        redundancy: int = 20,
        channel_choice: str = "Y",
        jpeg_quality: int = 100
    ):
        """
        Intègre des données binaires dans une image en utilisant la DCT.
        """
        img_bgr = cv2.imread(in_path)
        if img_bgr is None:
            raise FileNotFoundError("Image non trouvée.")
        img_ycc = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
        ch_map = {"Y":0, "Cr":1, "Cb":2}
        ch_idx = ch_map.get(channel_choice, 0)
        channel = img_ycc[:,:,ch_idx]

        blocks, orig_shape, padded_shape = self._blocks_from_channel(channel)
        dct_blocks = np.empty_like(blocks)
        for i, blk in enumerate(blocks):
            dct_blocks[i] = cv2.dct(blk)

        # Payload packaging: [4 bytes len] + payload + [4 bytes CRC]
        length = len(payload_bytes)
        crc = zlib.crc32(payload_bytes) & 0xffffffff
        header = length.to_bytes(4, "big") + payload_bytes + crc.to_bytes(4, "big")
        bits = []
        for b in header:
            bits.extend(self._int_to_bits(b, 8))
        total_bits = len(bits)

        print(f"Total bits à intégrer: {total_bits}")

        num_blocks = dct_blocks.shape[0]
        rng = random.Random(hashlib.sha256(key.encode()).digest())
        all_indices = list(range(num_blocks))
        rng.shuffle(all_indices)

        ci, cj = self._select_mid_coeff_positions()

        positions = []
        idx_cursor = 0
        for bit_i in range(total_bits):
            chosen = []
            for r in range(redundancy):
                chosen.append(all_indices[(idx_cursor + r) % num_blocks])
            positions.append(chosen)
            idx_cursor = (idx_cursor + redundancy) % num_blocks

        print(f"Positions: {len(positions)} bits, {len(positions[0]) if positions else 0} blocs par bit")

        for bit_i, bit in enumerate(bits):
            d = self._bit_to_delta(bit, strength)
            for bidx in positions[bit_i]:
                # Vérifier si le bloc contient principalement du blanc ou du noir
                block = blocks[bidx]
                mean_val = np.mean(block)
                if 15 < mean_val < 240:  # Éviter les zones trop noires (<15) et trop blanches (>240)
                    val = dct_blocks[bidx, ci, cj]
                    dct_blocks[bidx, ci, cj] = val + d

        idct_blocks = np.empty_like(dct_blocks)
        for i, b in enumerate(dct_blocks):
            idct_blocks[i] = cv2.idct(b)

        new_channel = self._channel_from_blocks(idct_blocks, orig_shape, padded_shape)
        img_ycc[:,:,ch_idx] = new_channel
        img_out = cv2.cvtColor(img_ycc.astype(np.uint8), cv2.COLOR_YCrCb2BGR)
        cv2.imwrite(out_path, img_out, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        print(f"Embed done — bits: {total_bits}, redundancy: {redundancy}, strength: {strength}")

    # ---------- Extraction (returns bytes payload) ----------
    def extract_message_bytes(
        self,
        in_path: str,
        key: str,
        redundancy: int = 20,
        channel_choice: str = "Y",
        max_message_bytes: int = 1000
    ) -> bytes:
        """
        Extrait des données binaires d'une image stéganographiée.
        """
        img_bgr = cv2.imread(in_path)
        if img_bgr is None:
            raise FileNotFoundError("Image non trouvée.")
        img_ycc = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb).astype(np.float32)
        ch_map = {"Y":0, "Cr":1, "Cb":2}
        ch_idx = ch_map.get(channel_choice, 0)
        channel = img_ycc[:,:,ch_idx]

        blocks, orig_shape, padded_shape = self._blocks_from_channel(channel)
        dct_blocks = np.empty_like(blocks)
        for i, blk in enumerate(blocks):
            dct_blocks[i] = cv2.dct(blk)

        num_blocks = dct_blocks.shape[0]
        rng = random.Random(hashlib.sha256(key.encode()).digest())
        all_indices = list(range(num_blocks))
        rng.shuffle(all_indices)

        ci, cj = self._select_mid_coeff_positions()

        max_header_bits = (4 + max_message_bytes + 4) * 8
        positions = []
        idx_cursor = 0
        for bit_i in range(max_header_bits):
            chosen = []
            for r in range(redundancy):
                chosen.append(all_indices[(idx_cursor + r) % num_blocks])
            positions.append(chosen)
            idx_cursor = (idx_cursor + redundancy) % num_blocks

        print(f"Positions d'extraction: {len(positions)} bits, {len(positions[0]) if positions else 0} blocs par bit")

        bits = []
        for bit_i in range(max_header_bits):
            votes = []
            for bidx in positions[bit_i]:
                val = dct_blocks[bidx, ci, cj]
                votes.append(1 if val > 0 else 0)
            bit = 1 if sum(votes) >= (len(votes)/2) else 0
            bits.append(bit)

        print(f"Bits extraits: {len(bits)}")

        if len(bits) < 32:
            raise ValueError("Image trop petite.")
        len_bits = bits[:32]
        length = self._bits_to_int(len_bits)
        print(f"Longueur du message: {length} octets")
        if length <= 0 or length > max_message_bytes:
            raise ValueError(f"Payload length invalide : {length}")

        total_bits_needed = (4 + length + 4) * 8
        payload_bits = bits[:total_bits_needed]
        byts = bytearray()
        for i in range(0, total_bits_needed, 8):
            byte = self._bits_to_int(payload_bits[i:i+8])
            byts.append(byte)
        msg_len = int.from_bytes(byts[0:4], "big")
        msg_bytes = bytes(byts[4:4+msg_len])
        crc_recv = int.from_bytes(byts[4+msg_len:4+msg_len+4], "big")
        crc_calc = zlib.crc32(msg_bytes) & 0xffffffff
        if crc_recv != crc_calc:
            raise ValueError("CRC mismatch. Corruption probable ou mauvais key/params.")
        return msg_bytes

    # ---------- Convenience wrappers combining AES + stego ----------
    def embed_message_aes(
        self,
        in_path: str,
        out_path: str,
        message: str,
        password: str,
        key_positions_secret: str,
        strength: float = 24.0,
        redundancy: int = 30,
        channel_choice: str = "Y",
        jpeg_quality: int = 85
    ):
        """
        Intègre un message chiffré avec AES dans une image.
        """
        # encrypt message bytes with AES-GCM, then base64-encode to keep binary-safe if you want text transport.
        ciphertext = self.aes_encrypt(message.encode('utf-8'), password)
        # We embed raw bytes (no base64 needed). embed_message_bytes accepts bytes.
        self.embed_message_bytes(
            in_path=in_path,
            out_path=out_path,
            payload_bytes=ciphertext,
            key=key_positions_secret,
            strength=strength,
            redundancy=redundancy,
            channel_choice=channel_choice,
            jpeg_quality=jpeg_quality
        )

    def extract_message_aes(
        self,
        in_path: str,
        password: str,
        key_positions_secret: str,
        redundancy: int = 30,
        channel_choice: str = "Y"
    ) -> str:
        """
        Extrait et déchiffre un message d'une image stéganographiée.
        """
        payload_bytes = self.extract_message_bytes(
            in_path=in_path,
            key=key_positions_secret,
            redundancy=redundancy,
            channel_choice=channel_choice
        )
        # decrypt
        try:
            plain = self.aes_decrypt(payload_bytes, password)
        except Exception as e:
            raise ValueError("Déchiffrement AES échoué: " + str(e))
        return plain.decode('utf-8')