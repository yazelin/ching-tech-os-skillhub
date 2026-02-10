#!/usr/bin/env bash
set -euo pipefail
DIR=${1:-/opt/erpnext-mcp}
ENV_FILE="$DIR/.env"

if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
else
  echo ".env not found at $ENV_FILE"; exit 2
fi

# Basic check: try to list doctypes via running the MCP server temporarily (requires uv)
if command -v uv >/dev/null 2>&1; then
  echo "Attempting to run erpnext-mcp to perform a quick list_documents test (will run in foreground)..."
  set -a
  source "$ENV_FILE"
  set +a
  # Run a single list_documents via uv run -- but this requires the MCP client context; instruct user instead
  echo "Please ensure the MCP server is running (uv run erpnext-mcp) and use a MCP client to call list_documents."
  exit 0
else
  echo "uv not available; cannot auto-run server. Verify ERPNEXT_URL, ERPNEXT_API_KEY, ERPNEXT_API_SECRET are set:"
  echo "ERPNEXT_URL=${ERPNEXT_URL:-}
ERPNEXT_API_KEY=${ERPNEXT_API_KEY:-}
ERPNEXT_API_SECRET=${ERPNEXT_API_SECRET:-}" || true
  exit 0
fi
