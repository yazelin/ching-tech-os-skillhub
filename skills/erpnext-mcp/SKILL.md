---
name: erpnext-mcp
version: "0.1.0"
description: "ERPNext MCP server - expose ERPNext REST API as an MCP toolset (CRUD, reports, workflows, files, inventory)."
author: yazelin
tags:
  - erpnext
  - mcp
  - erp
entrypoint: run.py
files:
  - run.py
  - SKILL.md
  - src/erpnext_mcp/server.py
  - src/erpnext_mcp/client.py
  - src/erpnext_mcp/types.py
license: MIT
checksum: ""
dependencies:
  - python>=3.11
  - httpx
  - fastmcp
  - python-dotenv
  - pydantic
ctos:
  version: "0.1.0"
  namespace: erpnext-mcp
  compatible_with:
    - "0.1.0"
  upgrade_policy: notify
  erp_integration:
    enabled: true
    systems:
      - "erpnext"
---

# ERPNext MCP Skill

## 概要

本 Skill 將 yazelin/erpnext-mcp 包裝為 CTOS SkillHub skill，提供對 ERPNext REST API 的 MCP 工具集（CRUD、報表、工作流程、檔案、庫存等）。

## 快速開始

1. 在 Skill 目錄下建立 .env，填入 ERPNext 服務設定：

```bash
cat > .env << 'EOF'
ERPNEXT_URL=https://your-erpnext-instance.com
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
EOF
```

2. 啟動 Skill（需 Python 3.11+ 且安裝 dependencies）：

```bash
python run.py
```

或使用 uv:

```bash
set -a && source .env && set +a && uv run erpnext-mcp
```

## 使用說明

本 Skill 暴露多個 MCP 工具，主要包括：

- list_documents(doctype, ...)
- get_document(doctype, name, ...)
- create_document(doctype, data)
- update_document(doctype, name, data)
- delete_document(doctype, name)
- submit_document / cancel_document
- run_report(report_name, filters)
- get_stock_balance / get_stock_ledger / get_item_price
- get_supplier_details / get_customer_details
- upload_file / upload_file_from_url / list_files / download_file
- run_method(method, http_method, args) — 呼叫 ERPNext server-side method

參數說明與範例請參考 repo README。

## 設定

本 Skill 依賴以下環境變數：

- ERPNEXT_URL
- ERPNEXT_API_KEY
- ERPNEXT_API_SECRET

## 權責

作者: yazelin

## License

MIT
