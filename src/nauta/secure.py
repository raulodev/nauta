import base64
from hashlib import sha256

from nauta.database import get_secret


def generate_key() -> bytes:
    """Generar una clave derivada de un string (clave simple)"""
    secret = get_secret()
    return sha256(secret.encode()).digest()  # Derivar clave fija


def encrypt_password(password: str, key: bytes) -> str:
    """Encriptar un texto"""
    password_bytes = password.encode("utf-8")
    encrypted_bytes = base64.b64encode(xor_bytes(password_bytes, key))
    return encrypted_bytes.decode("utf-8")


def decrypt_password(encrypted_password: str, key: bytes) -> str:
    """Desencriptar un texto"""
    encrypted_bytes = base64.b64decode(encrypted_password.encode("utf-8"))
    decrypted_bytes = xor_bytes(encrypted_bytes, key)
    return decrypted_bytes.decode("utf-8")


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR entre bytes para encriptar/desencriptar"""
    key_repeated = key * (len(data) // len(key)) + key[: len(data) % len(key)]
    return bytes(a ^ b for a, b in zip(data, key_repeated))
