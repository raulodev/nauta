import base64
from unittest.mock import patch

from nauta.secure import decrypt_password, encrypt_password, generate_key, xor_bytes

MOCK_SECRET = "supersecreto"
MOCK_KEY = bytes([0x42] * 32)


@patch("nauta.secure.get_secret", return_value=MOCK_SECRET)
def test_generate_key(mock_get_secret):
    key = generate_key()
    expected = __import__("hashlib").sha256(MOCK_SECRET.encode()).digest()
    assert key == expected
    mock_get_secret.assert_called_once()


def test_xor_bytes_roundtrip():
    data = b"hola mundo"
    key = b"\x01\x02"
    encrypted = xor_bytes(data, key)
    decrypted = xor_bytes(encrypted, key)
    assert decrypted == data


def test_encrypt_decrypt_password():
    password = "contrasena123"
    encrypted = encrypt_password(password, MOCK_KEY)
    assert isinstance(encrypted, str)

    decrypted = decrypt_password(encrypted, MOCK_KEY)
    assert decrypted == password


def test_encrypt_password_output_is_base64():
    password = "123"
    encrypted = encrypt_password(password, MOCK_KEY)
    # Asegurar que el texto cifrado sea decodificable como base64
    decoded = base64.b64decode(encrypted.encode("utf-8"))
    assert isinstance(decoded, bytes)
