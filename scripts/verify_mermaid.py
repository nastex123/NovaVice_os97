#!/usr/bin/env python3
# Verify fenced mermaid blocks are syntactically balanced (TODO-4.8).
# Checks DIAGRAMA.md and EXPLICACION_TECNICA.md without external parser.
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TARGETS = [BASE / "DIAGRAMA.md", BASE / "EXPLICACION_TECNICA.md", BASE / "TECHNICAL_EXPLANATION.md"]


def check_file(path: Path) -> bool:
    # Return True if all mermaid fences open and close correctly.
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8")
    opens = len(re.findall(r"```mermaid", text))
    closes = 0
    in_block = False
    for line in text.splitlines():
        if line.strip().startswith("```mermaid"):
            in_block = True
        elif line.strip() == "```" and in_block:
            closes += 1
            in_block = False
    if in_block or opens != closes:
        print(f"FAIL {path.name}: opens={opens} closes={closes}")
        return False
    print(f"OK {path.name}: {opens} blocks")
    return True


def main() -> None:
    # Exit nonzero on any unbalanced diagram file.
    ok = all(check_file(p) for p in TARGETS)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
