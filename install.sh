#!/usr/bin/env bash
# Quick installer script for Linux and macOS
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export PATH="$HOME/.local/bin:$PATH"

echo "================================================================"
echo "  Starting Automated Installer (Linux / macOS)..."
echo "================================================================"
python3 scripts/installer.py "$@"
