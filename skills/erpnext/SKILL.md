---
name: erpnext
version: 1.0.0
ctos:
  erp_integration:
    enabled: true
---

# ERPNext Skill

本 Skill 指引 AI agent 如何使用 ERPNext MCP（erpnext-mcp）提供的功能來和 ERPNext 系統互動。包含安裝、設定、可用工具說明、常見操作範例與錯誤處理建議。

注意：此 Skill 不是 erpnext-mcp 的原始碼複製，僅為使用與整合指南及輔助腳本。

## 前置需求

- 已有 ERPNext 實例與 API key/secret
- Python >= 3.11
- 建議安裝 `uv`（[Astral uv runner](https://docs.astral.sh/uv/)），或使用 `pip` 安裝依賴

## 安裝與啟動（快速指南）

1. 取得 erpnext-mcp 原始碼（或在管理主機上放置已安裝的 erpnext-mcp）：

```bash
# 在本地或管理主機上
git clone https://github.com/yazelin/erpnext-mcp.git /opt/erpnext-mcp
cd /opt/erpnext-mcp
```

2. 設定環境變數（或在 .env）：

```bash
cat > .env << 'EOF'
ERPNEXT_URL=https://your-erpnext-instance.com
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
EOF
```

3. 安裝依賴並啟動（推薦 uv）：

```bash
uv sync
set -a && source .env && set +a && uv run erpnext-mcp
```

或使用 pip 直接在虛擬環境中安裝依賴並以 uv 或 python 啟動。

## 連線設定（Agent 必須知道）

Agent 使用下列資訊與 MCP client 連到 erpnext-mcp：

- URL（mcp server 執行主機）
- ERPNEXT_URL（ERPNext 實例 URL）
- ERPNEXT_API_KEY / ERPNEXT_API_SECRET（ERPNext 帳戶 API 金鑰）

範例 MCP client 設定：

```json
{
  "mcpServers": {
    "erpnext": {
      "command": "uv",
      "args": ["--directory", "/opt/erpnext-mcp", "run", "erpnext-mcp"],
      "env": {
        "ERPNEXT_URL": "https://your-erpnext-instance.com",
        "ERPNEXT_API_KEY": "your_api_key",
        "ERPNEXT_API_SECRET": "your_api_secret"
      }
    }
  }
}
```

Agent 在對話中應明確要求並確認上述參數，並可使用腳本驗證連線。

## 可用工具（summary）

erpnext-mcp 提供的主要工具：
- CRUD: list_documents, get_document, create_document, update_document, delete_document
- Workflow: submit_document, cancel_document
- Reports: run_report
- Schema: list_doctypes, get_doctype_meta
- Inventory & trading: get_stock_balance, get_stock_ledger, get_item_price, make_mapped_doc
- Party: get_party_balance, get_supplier_details, get_customer_details
- Files: upload_file, upload_file_from_url, list_files, download_file, get_file_url
- Helpers: get_count, get_list_with_summary, run_method, search_link

（具體工具名稱與參數以實際 erpnext-mcp 版本為準）

## 常見使用場景與範例 Prompt

1) 查詢文件列表

Prompt 範例：
"使用 erpnext-mcp 的 list_documents 列出 Sales Invoice，限制 50 筆，按修改時間遞減，欄位包含: name, customer, grand_total。"

2) 創建新文件（示例：Sales Invoice）

Prompt 範例：
"使用 create_document 在 DocType 'Sales Invoice' 建立一筆，payload 包含 customer='ACME', items=[{item_code:'ITEM-001', qty:1, rate:100}]; 回傳剛建立的 name。"

3) 執行報表

Prompt 範例：
"使用 run_report 執行 'Sales Register'，帶入日期範圍 2026-01-01 至 2026-01-31，回傳前 100 筆結果與總計。"

4) 上傳檔案

Prompt 範例：
"使用 upload_file 將本地路徑 /tmp/invoice.pdf 上傳到 Sales Invoice 名為 SINV-0001 的文件，並回傳檔案 URL。"

5) 庫存查詢

Prompt 範例：
"使用 get_stock_balance 查詢 Item 'ITEM-001' 在 Warehouse 'Main - WH' 的即時庫存。"

## 錯誤處理指南

- 驗證連線錯誤：檢查 MCP server 是否啟動、.env 設定是否正確、網路是否通。建議使用 scripts/check_connection.sh 取得詳細錯誤回傳。 
- 權限錯誤（401/403）：確認 API key/secret 與 ERPNext 用戶權限設定。
- 資料驗證失敗（422）：檢查 payload 欄位、必填欄位是否遺漏，回傳完整錯誤訊息給 user 並建議修正欄位。
- 超時或 5xx：重試策略（exponential backoff），並記錄請求與回應以便除錯。

## Security 與 Best Practices

- 禁止把完整的 API secret 直接回報到聊天內容；對用戶請求時只回報是否成功與資源識別（例如 document name / id）。
- 使用最小權限原則建立 ERPNext API key。
- 對於會改變系統狀態的請求（create/update/submit/cancel），在執行前務必再次確認使用者意圖並提示可能風險。

## Scripts（輔助腳本）

- scripts/check_install.sh — 檢查 erpnext-mcp 目錄、uv 安裝、Python 版本
- scripts/check_connection.sh — 以環境變數呼叫 health endpoint 或簡單 list_documents 測試連線
- scripts/upload_file_from_url.sh — 透過 upload_file_from_url 上傳並回傳 URL

使用方式（示例）：

```bash
# 檢查安裝
bash scripts/check_install.sh /opt/erpnext-mcp

# 測試連線（從環境或指定 .env）
bash scripts/check_connection.sh /opt/erpnext-mcp
```

## 參考連結

- erpnext-mcp README: https://github.com/yazelin/erpnext-mcp

