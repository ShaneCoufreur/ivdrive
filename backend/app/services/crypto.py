"""AES-256-GCM encryption helpers for sensitive fields (VINs, tokens, credentials)."""

import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.config import settings

_NONCE_SIZE = 12


def _get_key() -> bytes:
    raw = settings.encryption_key
    try:
        key = base64.b64decode(raw)
    except Exception:
        key = hashlib.sha256(raw.encode()).digest()
    if len(key) != 32:
        key = hashlib.sha256(key).digest()
    return key


def encrypt_field(plaintext: str) -> str:
    key = _get_key()
    nonce = os.urandom(_NONCE_SIZE)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


def decrypt_field(token: str) -> str:
    key = _get_key()
    raw = base64.b64decode(token)
    nonce = raw[:_NONCE_SIZE]
    ciphertext = raw[_NONCE_SIZE:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


def hash_field(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
