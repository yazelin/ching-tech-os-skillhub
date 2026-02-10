#!/usr/bin/env bash
set -euo pipefail
DIR=${1:-/opt/erpnext-mcp}

echo "Checking ERPNEXT MCP installation at: $DIR"
[ -d "$DIR" ] || { echo "Directory not found: $DIR"; exit 2; }

python3 -V || true
if command -v uv >/dev/null 2>&1; then
  echo "uv runner detected: $(uv --version 2>/dev/null || echo 'unknown')"
else
  echo "uv not found; ensure uv or use pip to install requirements"
fi

if [ -f "$DIR/.env" ]; then
  echo ".env found"
else
  echo ".env not found — ensure ERPNEXT_URL and API keys are configured"
fi

echo "Done" 
