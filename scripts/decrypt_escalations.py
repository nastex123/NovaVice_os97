#!/usr/bin/env python3
"""
Recupera un respaldo cifrado NovVault v1 (PROP-183).
Descifra `escalations.db.enc` (o el journal JSON cifrado) a un archivo en claro.

Uso:
    python scripts/decrypt_escalations.py escalations.db.enc --out backup.db
    # sin --password usa la env ESCALATIONS_DB_KEY
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from src.core.secure_store import decrypt_file, get_vault_password


def main() -> int:
    parser = argparse.ArgumentParser(description="Descifra un vault NovVault v1 (PROP-183).")
    parser.add_argument("vault", type=Path, help="Ruta al archivo cifrado (p. ej. escalations.db.enc).")
    parser.add_argument("--out", "-o", type=Path, required=True, help="Ruta de salida del archivo en claro (respaldo recuperado).")
    parser.add_argument("--password", type=str, default=None, help="Clave maestra (si se omite usa la env ESCALATIONS_DB_KEY).")
    args = parser.parse_args()

    if not args.vault.exists():
        print(f"ERROR: no existe el vault {args.vault}", file=sys.stderr)
        return 2

    password = args.password or get_vault_password()
    if not password:
        print("ERROR: se requiere --password o la variable de entorno ESCALATIONS_DB_KEY.", file=sys.stderr)
        return 2

    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_bytes(decrypt_file(args.vault, password))
    tmp.replace(out)
    print(f"OK: respaldo descifrado en {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())