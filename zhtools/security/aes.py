import base64

from zhtools.exceptions import ModuleRequired

try:
    from Crypto import Random
    from Crypto.Cipher import AES as _AES
except ImportError:
    raise ModuleRequired("pycryptodome")


class AES:
    def __init__(self, key: str, mode=_AES.MODE_CBC):
        self.key = key.encode()
        self.mode = mode

    @staticmethod
    def pkcs7padding(text: str):
        length = len(text)
        bytes_length = len(text.encode())
        padding_size = length if (bytes_length == length) else bytes_length
        padding = 16 - padding_size % 16
        padding_text = chr(padding) * padding
        return text + padding_text

    @staticmethod
    def pkcs7unpadding(text: str):
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0 : length - unpadding]

    def decrypt(self, content: str) -> str:
        content_b = base64.b64decode(content)
        iv = content_b[:16]
        content_b = content_b[16:]
        cipher = _AES.new(self.key, self.mode, iv)  # type: ignore
        decrypt_bytes = cipher.decrypt(content)
        return self.pkcs7unpadding(decrypt_bytes.decode())

    def encrypt(self, content: str) -> str:
        iv = Random.new().read(16)
        cipher = _AES.new(self.key, self.mode, iv)  # type: ignore
        content_padding = self.pkcs7padding(content)
        encrypt_bytes = cipher.encrypt(content_padding.encode())
        return base64.b64encode(iv + encrypt_bytes).decode()
