import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key():
    """Load student private key (PEM) from project root"""
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def decrypt_encrypted_seed(encrypted_seed_b64: str) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP-SHA256.

    Returns:
        64-character hex seed string
    """
    try:
        private_key = load_private_key()

        # Base64 decode
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)

        # RSA OAEP decrypt (SHA-256 + MGF1(SHA-256), label=None)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        hex_seed = decrypted_bytes.decode().strip()

        # Validate format: must be 64-character lowercase hex
        if len(hex_seed) != 64:
            raise ValueError("Seed length mismatch")

        valid_chars = set("0123456789abcdef")
        if any(c not in valid_chars for c in hex_seed):
            raise ValueError("Seed contains non-hex characters")

        return hex_seed

    except Exception as e:
        print("Crypto Decryption Error:", e)
        raise
