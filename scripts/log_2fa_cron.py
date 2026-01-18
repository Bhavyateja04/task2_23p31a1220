#!/usr/bin/env python3
import os, sys
from datetime import datetime, timezone

# Add /app to sys.path
sys.path.append('/app')

from app.totp_utils import generate_code

SEED_FILE = "/data/seed.txt"

def main():
    if not os.path.exists(SEED_FILE):
        print("Seed not found")
        return

    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    code, _ = generate_code(seed)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ts} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
