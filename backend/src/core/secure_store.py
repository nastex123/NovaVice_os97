import base64
import hashlib
import os
import secrets
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

_MAGIC = b"NVVAULT\x00\x01"
_SALT_SIZE = 16
_PBKDF2_ITERATIONS = 210_000
_ENV_KEY_VAR = "ESCALATIONS_DB_KEY"


def get_vault_password() -> Optional[str]:
    """Clave maestra derivada del entorno (nunca hardcodeada)."""
    value = os.getenv(_ENV_KEY_VAR, "").strip()
    return value or None


def _derive_key(password: str, salt: bytes) -> bytes:
    material = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS, dklen=32
    )
    return base64.urlsafe_b64encode(material)


def _fernet(password: str, salt: bytes) -> Fernet:
    return Fernet(_derive_key(password, salt))


def encrypt_bytes(data: bytes, password: str, salt: Optional[bytes] = None) -> bytes:
    """Cifra bytes en blob NovVault v1: magic + salt(16) + token Fernet."""
    salt = salt or secrets.token_bytes(_SALT_SIZE)
    return _MAGIC + salt + _fernet(password, salt).encrypt(data)


def decrypt_bytes(payload: bytes, password: str) -> bytes:
    """Descifra un blob NovVault v1. Lanza InvalidToken con clave incorrecta."""
    if not payload.startswith(_MAGIC):
        raise ValueError("El archivo no es un vault NovVault v1.")
    salt = payload[len(_MAGIC):len(_MAGIC) + _SALT_SIZE]
    token = payload[len(_MAGIC) + _SALT_SIZE:]
    return _fernet(password, salt).decrypt(token)


def encrypt_file(source: Path, target: Path, password: str) -> None:
    """Cifra un archivo en el destino de forma atómica (write de tmp + replace)."""
    raw = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    tmp.write_bytes(encrypt_bytes(raw, password))
    os.replace(tmp, target)


def decrypt_file(source: Path, password: str) -> bytes:
    """Devuelve los bytes en claro de un vault NovVault v1."""
    return decrypt_bytes(source.read_bytes(), password)


def atomic_write_encrypted(path: Path, content: str, password: Optional[str] = None) -> None:
    """Escribe texto cifrado en reposo (o plano si no hay clave)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not password:
        path.write_text(content, encoding="utf-8")
        return
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(encrypt_bytes(content.encode("utf-8"), password))
    os.replace(tmp, path)


def read_text_decrypted(path: Path, password: Optional[str] = None) -> str:
    """Lee texto cifrado (o plano); tolera journals legacy sin cifrar (migración)."""
    if not path.exists():
        return ""
    raw = path.read_bytes()
    if not password:
        return raw.decode("utf-8")
    try:
        return decrypt_bytes(raw, password).decode("utf-8")
    except (InvalidToken, ValueError):
        return raw.decode("utf-8")