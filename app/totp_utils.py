import base64
import time
import pyotp

PERIOD = 30

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")

def generate_totp(hex_seed: str):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=PERIOD)
    code = totp.now()
    valid_for = PERIOD - (int(time.time()) % PERIOD)
    return code, valid_for

def verify_totp(hex_seed: str, code: str, window: int = 1) -> bool:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, interval=PERIOD)
    return totp.verify(code, valid_window=window)
