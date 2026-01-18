import base64
import time
import pyotp


def _hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex seed → bytes → base32 string
    Base32 must be ASCII string for pyotp
    """
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode('utf-8')


def generate_code(hex_seed: str):
    """
    Generate TOTP code using:
    - SHA1
    - 30s period
    - 6 digits

    Returns: (code, valid_for)
    """
    base32_seed = _hex_to_base32(hex_seed)

    totp = pyotp.TOTP(
        base32_seed,
        digits=6,
        interval=30,
        digest="sha1"
    )

    code = totp.now()

    # Remaining seconds in current 30s window
    valid_for = 30 - (int(time.time()) % 30)

    return code, valid_for


def verify_code(hex_seed: str, code: str):
    """
    Verify TOTP code allowing ±1 time window tolerance

    valid_window=1 => current, previous, next window accepted
                     (±30 seconds)
    """
    base32_seed = _hex_to_base32(hex_seed)

    totp = pyotp.TOTP(
        base32_seed,
        digits=6,
        interval=30,
        digest="sha1"
    )

    return totp.verify(code, valid_window=1)
