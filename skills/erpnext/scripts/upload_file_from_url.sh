#!/usr/bin/env bash
set -euo pipefail
# Usage: upload_file_from_url.sh /opt/erpnext-mcp <doc_type> <doc_name> <file_url>
DIR=${1:-/opt/erpnext-mcp}
DOCTYPE=${2:-"File"}
DOCNAME=${3:-}
FILE_URL=${4:-}

if [ -z "$DOCNAME" ] || [ -z "$FILE_URL" ]; then
  echo "Usage: $0 /opt/erpnext-mcp <DocType> <DocName> <FileURL>"; exit 2
fi

# This script is a helper that demonstrates calling the MCP server's upload_file_from_url tool via curl to a local MCP HTTP endpoint, if available.
# Adjust HOST/PORT to your MCP server config.
HOST=${ERPNEXT_MCP_HOST:-"http://localhost:8000"}
API_PATH="/mcp/upload_file_from_url" # example path; replace with actual MCP endpoint if exposed

echo "Uploading $FILE_URL to $DOCTYPE $DOCNAME via MCP at $HOST"
# Example curl (commented out; adapt to your MCP client's HTTP API if present)
# curl -X POST "$HOST$API_PATH" -H "Content-Type: application/json" -d '{"doctype":"'$DOCTYPE'","docname":"'$DOCNAME'","file_url":"'$FILE_URL'"}'

echo "Adjust this script to call your MCP client's HTTP API or use an MCP client library."
