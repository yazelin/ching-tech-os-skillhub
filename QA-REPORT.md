# QA Report

**日期**: 2024-05-22
**狀態**: 草稿 (Draft)

## 摘要
本專案結構大致良好，包含必要的文件與 CI 工作流程。然而，CI/CD 流程中缺乏嚴格的程式碼品質檢查（Linting）與單元測試執行。程式碼中未發現硬編碼的敏感資訊。

## 詳細檢查結果

| 類別 | 檢查項目 | 狀態 | 備註 |
| :--- | :--- | :--- | :--- |
| **文件 (Docs)** | README.md 關鍵字 | ✅ 通過 | 包含安裝 (Install)、使用 (Usage)、授權 (License) 資訊。 |
| | docs/index.html | ✅ 通過 | 檔案存在。 |
| | LICENSE | ✅ 通過 | MIT License 存在。 |
| **CI/CD** | .github/workflows | ✅ 通過 | `ci.yml` 存在，且設定了 `push` 與 `pull_request` 觸發條件。 |
| | 工作流程內容 | ⚠️ 警告 | 僅執行 `compileall` (語法檢查)，**缺少 Linter** (flake8/ruff) 與 **單元測試**。 |
| **程式碼品質** | Linter 設定 | ❌ 失敗 | 環境與 `requirements.txt` 中未發現 `flake8` 或 `ruff`。 |
| | 單元測試 | ❌ 失敗 | `tests/` 目錄存在測試檔案，但 CI 未執行 `pytest`。 |
| **安全性** | 硬編碼 Secrets | ✅ 通過 | 僅在文件中發現範例用的佔位符（如 `your_api_key`），無真實密鑰。 |

## 2. Index + Release 驗證

**驗證日期**: 2025-07-25
**方法**: 實際下載 ZIP、SHA256 驗算、HTTP HEAD 檢查、ZIP 結構驗證

### 2.1 JSON Schema 驗證

| 項目 | 結果 | 備註 |
| :--- | :--- | :--- |
| `schemas/index.schema.json` 存在 | ⚠️ 不存在 | 僅有 `schemas/skill.schema.json`，以 ad-hoc index schema 驗證 |
| `index.json` 通過 schema 驗證 | ✅ 通過 | 無 validation errors |

> **建議**: 應建立正式的 `schemas/index.schema.json` 並納入 CI 驗證流程。

### 2.2 Per-Skill 驗證總表

| Skill | download_url | HTTP Status | SHA256 Match | ZIP Structure | SKILL.md | Path Traversal | Frontmatter |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `pr-reviewer` | [v0.1.0/pr-reviewer-1.0.0.zip](https://github.com/yazelin/ching-tech-os-skillhub/releases/download/v0.1.0/pr-reviewer-1.0.0.zip) | 200 | ✅ Match | ✅ Valid | ✅ Found | ✅ Clean | ✅ Parseable |
| `nano-banana-pro` | [v0.1.1/nano-banana-pro-0.4.4.zip](https://github.com/yazelin/ching-tech-os-skillhub/releases/download/v0.1.1/nano-banana-pro-0.4.4.zip) | 200 | ✅ Match | ✅ Valid | ✅ Found | ✅ Clean | ✅ Parseable |
| `erpnext` | *(empty)* | N/A | N/A | N/A | N/A | N/A | N/A |

### 2.3 SHA256 驗算明細

| Skill | Expected | Actual | 結果 |
| :--- | :--- | :--- | :---: |
| `pr-reviewer` | `335414a3...fc501` | `335414a3...fc501` | ✅ |
| `nano-banana-pro` | `d6e4a838...a542` | `d6e4a838...a542` | ✅ |
| `erpnext` | *(empty)* | — | ⚠️ 無 release |

### 2.4 ZIP 結構驗證

**pr-reviewer** (4 entries):
```
pr-reviewer/.clawhub/origin.json
pr-reviewer/SKILL.md
pr-reviewer/_meta.json
pr-reviewer/scripts/pr-review.sh
```
- SKILL.md frontmatter keys: `name`, `version`, `author`, `entrypoint`, `tags`, `description`, `ctos`

**nano-banana-pro** (5 entries):
```
SKILL.md
README.md
scripts/
scripts/generate
scripts/generate_image.py
```
- SKILL.md frontmatter keys: `name`, `description`, `version`, `entrypoint`, `license`, `homepage`, `author`, `tags`, `compatibility`, `metadata`

> ⚠️ 注意: `nano-banana-pro` ZIP 無頂層目錄包裹（flat layout），而 `pr-reviewer` 有 `pr-reviewer/` 前綴。兩者 layout 不一致，建議統一規範。

### 2.5 發現與建議

| # | 嚴重度 | 說明 |
| :---: | :--- | :--- |
| 1 | ⚠️ 警告 | `schemas/index.schema.json` 不存在，index.json 無正式 schema 定義 |
| 2 | ⚠️ 警告 | `erpnext` skill 的 `download_url` 和 `sha256` 為空字串，尚無可下載的 release |
| 3 | ⚠️ 警告 | ZIP layout 不一致：`pr-reviewer` 使用目錄前綴，`nano-banana-pro` 為 flat layout |
| 4 | ✅ 通過 | 所有可下載 skill 的 SHA256 完全匹配 |
| 5 | ✅ 通過 | 所有 ZIP 無 path traversal（無 `../` 或絕對路徑） |
| 6 | ✅ 通過 | 所有 SKILL.md frontmatter 可正常解析為 YAML |

**🔴 Critical Issues: 0**

---

## 修復建議

1.  **整合 Linter**: 在 `requirements.txt` 加入 `ruff` 或 `flake8`，並在 `.github/workflows/ci.yml` 中新增檢查步驟，以確保程式碼風格一致。
2.  **啟用單元測試**: 專案內有 `tests/` 目錄（包含 `test_client.py` 等），但目前 CI 未執行。建議在 CI 中加入 `pytest` 步驟。
3.  **補充貢獻指南**: 雖然 README 有提及如何製作 Skill，但建議新增 `CONTRIBUTING.md` 說明核心專案的開發與測試規範。
