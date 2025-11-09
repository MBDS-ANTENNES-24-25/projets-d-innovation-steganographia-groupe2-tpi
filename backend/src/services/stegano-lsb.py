from PIL import Image
import zlib
from collections import Counter
from sqlalchemy.orm import Session

END_MARKER = '0110110011001101'

class SteganoLSBService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def compress_message(message: str) -> bytes:
        return zlib.compress(message.encode())

    @staticmethod
    def decompress_message(data: bytes) -> str:
        return zlib.decompress(data).decode()

    @staticmethod
    def to_bitstring(data: bytes) -> str:
        return ''.join(f'{byte:08b}' for byte in data)

    @staticmethod
    def from_bitstring(bits: str) -> bytes:
        return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    def hide_message(self, input_path: str, output_path: str, message: str, repeat: int = 5):
        img = Image.open(input_path)
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGBA')

        pixels = list(img.getdata())
        total_pixels = len(pixels)

        compressed = self.compress_message(message)
        bitstring_unit = self.to_bitstring(compressed) + END_MARKER

        # Vérifier que chaque copie tient dans une zone
        pixels_per_copy = total_pixels // repeat
        bits_per_copy = len(bitstring_unit)
        if bits_per_copy > pixels_per_copy * 3:
            raise ValueError("❌ Message trop long pour l'image ou pour le nombre de répétitions.")

        new_pixels = pixels[:]
        for i in range(repeat):
            bit_idx = 0
            start = i * pixels_per_copy
            end = start + pixels_per_copy

            for j in range(start, end):
                if bit_idx >= len(bitstring_unit):
                    break

                r, g, b = new_pixels[j][:3]

                if bit_idx < len(bitstring_unit):
                    r = (r & ~1) | int(bitstring_unit[bit_idx])
                    bit_idx += 1
                if bit_idx < len(bitstring_unit):
                    g = (g & ~1) | int(bitstring_unit[bit_idx])
                    bit_idx += 1
                if bit_idx < len(bitstring_unit):
                    b = (b & ~1) | int(bitstring_unit[bit_idx])
                    bit_idx += 1

                new_pixels[j] = (r, g, b, new_pixels[j][3]) if img.mode == 'RGBA' else (r, g, b)

        img.putdata(new_pixels)
        img.save(output_path)
        print(f"✅ Message caché avec redondance répartie sur {repeat} zones.")

    def extract_message(self, image_path: str, repeat: int = 5) -> str:
        img = Image.open(image_path)
        if img.mode not in ['RGB', 'RGBA']:
            raise ValueError("❌ Image non supportée")

        pixels = list(img.getdata())
        total_pixels = len(pixels)
        pixels_per_zone = total_pixels // repeat
        messages = []

        for i in range(repeat):
            bits = ''
            start = i * pixels_per_zone
            end = start + pixels_per_zone

            for j in range(start, min(end, total_pixels)):
                for channel in pixels[j][:3]:
                    bits += str(channel & 1)
                    if bits.endswith(END_MARKER):
                        bits = bits[:-len(END_MARKER)]
                        try:
                            data = self.from_bitstring(bits)
                            msg = self.decompress_message(data)
                            messages.append(msg)
                        except:
                            continue
                        break  # ne lit qu'un message par zone
                if bits.endswith(END_MARKER):
                    break

        if not messages:
            return "❌ Aucun message lisible trouvé."

        return Counter(messages).most_common(1)[0][0]



