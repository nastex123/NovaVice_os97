#!/usr/bin/env python3
# Background file watcher triggering re-index on documents change (TODO-5.5).
import time
import hashlib
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "backend" / "data" / "documents"


def snapshot() -> str:
    # Hash filenames and mtimes for change detection.
    h = hashlib.sha256()
    if DOCS.exists():
        for p in sorted(DOCS.glob("*.md")):
            h.update(p.name.encode())
            h.update(str(p.stat().st_mtime).encode())
    return h.hexdigest()


def main() -> None:
    # Poll every 30s and print re-index signal on change.
    prev = snapshot()
    print(f"watching {DOCS} hash={prev[:12]}")
    while True:
        time.sleep(30)
        cur = snapshot()
        if cur != prev:
            print(f"change detected {prev[:8]}->{cur[:8]}: re-index signal")
            prev = cur


if __name__ == "__main__":
    main()
