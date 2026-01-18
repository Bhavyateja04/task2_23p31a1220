from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os

from app.crypto_utils import decrypt_encrypted_seed
from app.totp_utils import generate_code, verify_code

app = FastAPI()

DATA_DIR = Path("/data")
SEED_FILE = DATA_DIR / "seed.txt"

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_seed_api(req: DecryptRequest):
    try:
        seed = decrypt_encrypted_seed(req.encrypted_seed)

        DATA_DIR.mkdir(exist_ok=True)
        SEED_FILE.write_text(seed)

        return {"status": "ok"}
    except Exception as e:
        print("decrypt error:", e)
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = SEED_FILE.read_text().strip()
    code, valid_for = generate_code(seed)
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = SEED_FILE.read_text().strip()
    return {"valid": verify_code(seed, req.code)}
