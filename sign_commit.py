from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
import sys

def load_private_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def rsa_pss_sign(private_key, commit_hash: str) -> bytes:
    # MUST sign ASCII string, NOT hex binary
    commit_bytes = commit_hash.encode("utf-8")
    signature = private_key.sign(
        commit_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH  # CRITICAL!
        ),
        hashes.SHA256()
    )
    return signature

def rsa_oaep_encrypt(public_key, data: bytes) -> bytes:
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None   # CRITICAL: label must be None
        )
    )
    return ciphertext


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sign_commit.py <commit_hash>")
        sys.exit(1)

    commit_hash = sys.argv[1]

    private_key = load_private_key("student_private.pem")
    instructor_pub = load_public_key("instructor_public.pem")

    signature = rsa_pss_sign(private_key, commit_hash)
    encrypted = rsa_oaep_encrypt(instructor_pub, signature)

    # Output single-line base64
    print(base64.b64encode(encrypted).decode("utf-8"))
