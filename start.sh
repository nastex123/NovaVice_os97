#!/usr/bin/env bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export PATH="$HOME/.local/bin:$PATH"

echo "================================================================"
echo "  Iniciando Sistema Completo para Linux / macOS..."
echo "================================================================"
python3 run.py "$@"
