#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path
from app.totp_utils import generate_totp

seed_file = Path("/data/seed.txt")

if not seed_file.exists():
    raise SystemExit("Seed not found")

seed = seed_file.read_text().strip()
code, _ = generate_totp(seed)

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
print(f"{timestamp} - 2FA Code: {code}")
