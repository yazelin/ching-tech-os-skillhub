---
name: erpnext
version: "0.1.0"
description: "MCP server for ERPNext REST API with CRUD, workflow, reports, schema inspection, inventory, trading, and file operations."
author: yazelin
entrypoint: run.sh
tags:
  - erpnext
  - mcp
  - api
files:
  - run.sh
  - SKILL.md
license: MIT
dependencies: []
ctos: {}
---

# ERPNext MCP Server

MCP (Model Context Protocol) server for ERPNext REST API, built with FastMCP and Python.

## Features

- CRUD — list, get, create, update, delete documents
- Workflow — submit and cancel submittable documents
- Reports — run ERPNext query reports
- Schema — inspect DocType field definitions, list all DocTypes
- Inventory — stock balance, stock ledger, item prices
- Trading — document conversion (e.g. Quotation → Sales Order), party balance
- Supplier/Customer — complete details with address, phone, contacts; supports alias search
- Files — upload, list, download files
- Helpers — link search (autocomplete), document count, generic method calls

## Requirements

- Python >= 3.11
- uv (recommended) or pip
- ERPNext instance with API key/secret

## Setup

```bash
# Clone the repo
git clone https://github.com/yazelin/erpnext-mcp && cd erpnext-mcp

# Create .env file
cat > .env << 'ENV'
ERPNEXT_URL=https://your-erpnext-instance.com
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
ENV

# Install dependencies
uv sync
```

## Run

```bash
set -a && source .env && set +a && uv run erpnext-mcp
```

## MCP Client Configuration

```json
{
  "mcpServers": {
    "erpnext": {
      "command": "uv",
      "args": ["--directory", "/path/to/erpnext-mcp", "run", "erpnext-mcp"],
      "env": {
        "ERPNEXT_URL": "https://your-erpnext-instance.com",
        "ERPNEXT_API_KEY": "your_api_key",
        "ERPNEXT_API_SECRET": "your_api_secret"
      }
    }
  }
}
```

## Repository

https://github.com/yazelin/erpnext-mcp
