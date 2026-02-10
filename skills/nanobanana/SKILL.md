---
name: nanobanana
version: "1.0.0"
description: "Nanobanana skill — 使用說明與輔助腳本，用於呼叫 nanobanana-py MCP 生成與編輯圖片。"
author: yazelin
tags:
  - ai-image
  - nanobanana
  - gemini
  - images
entrypoint: scripts/run.py
files:
  - SKILL.md
  - scripts/run.py
license: MIT
checksum: ""
dependencies:
  - name: nanobanana-py
    version: ">=0.0.0"
ctos:
  version: "0.1.0"
  compatible_with:
    - "0.1.0"
  upgrade_policy: notify
---

# Nanobanana Skill / Nanobanana 技能

此 Skill 提供 Nanobanana（nanobanana-py）的使用說明與輔助指令範例，教導 AI agent 如何呼叫已安裝的 nanobanana-py MCP 進行圖片生成、編修與修復。請注意：此 Skill 不包含 MCP server 的程式碼，僅為說明與輔助腳本。

## 快速開始 (Quick start)

1. 安裝 MCP（選一種方式）:

- 使用 uvx (推薦，會自動管理環境)：

```bash
uvx nanobanana-py
```

- 或使用 pip / pipx：

```bash
pip install nanobanana-py
# or
pipx install nanobanana-py
```

2. 設定 API Key（必要）：

```bash
export NANOBANANA_GEMINI_API_KEY="your-api-key-here"
# 備援變數: NANOBANANA_GOOGLE_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY
```

3. 使用範例（透過本 skill 的輔助腳本）：

```bash
python3 scripts/run.py --generate "一幅水彩畫：雪地森林裡的狐狸" --filename fox.png --resolution 1K
```

## 指南（Guide）

- Env / API key:
  - 優先使用 `NANOBANANA_GEMINI_API_KEY`。
  - 亦可設定 `GEMINI_API_KEY` 或 `NANOBANANA_GOOGLE_API_KEY` 作為備援。

- 常用參數：
  - prompt / description: 圖片描述文字
  - files: 參考圖片路徑（1-14 張）
  - filename: 指定輸出檔名（不含副檔名）
  - output_count: 生成張數（1-8）
  - resolution: `1K` / `2K` / `4K`
  - styles / variations: 風格與變體

## Agent 使用說明（For AI agents）

- 目標：呼叫已安裝之 nanobanana-py（MCP server）或使用 CLI wrapper 產生圖片。Skill 應提供範例命令、環境變數說明與建議流程，而非包含或執行 MCP server 原始碼。

- 範例流程：
  1. 檢查環境變數 `NANOBANANA_GEMINI_API_KEY` 是否存在（或從配置讀取）。
  2. 使用 CLI（uvx / pipx）或系統安裝的 `nanobanana-py` 呼叫生成指令。
  3. 等待輸出檔案，回報輸出路徑給使用者。不要在對話中直接回傳二進位內容，僅提供檔案路徑或上傳到支援的媒體服務。

## 安裝提示 (Hints)

- 若要在 OpenClaw / CTOS 中自動化：在 `~/.openclaw/openclaw.json` 中設定：

```json
"skills": {
  "nanobanana": {
    "env": { "NANOBANANA_GEMINI_API_KEY": "<your-key>" }
  }
}
```

- 若使用 uvx，確保 `uvx` 可用於系統路徑。

## 範例（Examples）

- 生成單張圖：

```bash
python3 scripts/run.py --generate "群山日落" --filename sunset --resolution 2K
```

- 編輯圖片：

```bash
python3 scripts/run.py --edit input.png --prompt "幫人物加上太陽眼鏡" --filename edited
```

## 檔案 (Files)

- scripts/run.py — 輔助腳本，示範如何構造命令呼叫 nanobanana-py。
- SKILL.md — 本文件。

## 授權

MIT
