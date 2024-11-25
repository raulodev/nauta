import base64
from hashlib import sha256


# Generar una clave derivada de un string (clave simple)
def generate_key(secret: str) -> bytes:
    return sha256(secret.encode()).digest()  # Derivar clave fija


# Encriptar un texto
def encrypt_password(password: str, key: bytes) -> str:
    password_bytes = password.encode("utf-8")
    encrypted_bytes = base64.b64encode(xor_bytes(password_bytes, key))
    return encrypted_bytes.decode("utf-8")


# Desencriptar un texto
def decrypt_password(encrypted_password: str, key: bytes) -> str:
    encrypted_bytes = base64.b64decode(encrypted_password.encode("utf-8"))
    decrypted_bytes = xor_bytes(encrypted_bytes, key)
    return decrypted_bytes.decode("utf-8")


# XOR entre bytes para encriptar/desencriptar
def xor_bytes(data: bytes, key: bytes) -> bytes:
    key_repeated = key * (len(data) // len(key)) + key[: len(data) % len(key)]
    return bytes(a ^ b for a, b in zip(data, key_repeated))


# # Ejemplo de uso
# if __name__ == "__main__":
#     # Clave secreta (puedes guardarla en un archivo o variable de entorno)
#     secret = "miClaveSecreta"
#     key = generate_key(secret)

#     # Encriptar una contraseña
#     plain_password = "miContrasena123"
#     encrypted_password = encrypt_password(plain_password, key)
#     print(f"Contraseña encriptada: {encrypted_password}")

#     # Desencriptar la contraseña
#     decrypted_password = decrypt_password(encrypted_password, key)
#     print(f"Contraseña desencriptada: {decrypted_password}")
