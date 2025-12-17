import base64
import re
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

HEX_RE = re.compile(r"^[0-9a-f]{64}$")

def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    ciphertext = base64.b64decode(encrypted_seed_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    seed = plaintext.decode("utf-8")
    if not HEX_RE.match(seed):
        raise ValueError("Invalid seed")
    return seed
