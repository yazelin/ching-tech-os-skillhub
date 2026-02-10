# Skill 格式說明

## SKILL.md

每個 skill 都必須在根目錄提供 `SKILL.md`。它結合 YAML frontmatter（機器可讀）與文字說明（人類可讀），用來描述技能的用途、使用方式與執行需求。

### Frontmatter 欄位

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `name` | string | ✅ | 技能識別字，僅小寫與連字號。 |
| `version` | string | ✅ | 語意化版本（MAJOR.MINOR.PATCH）。 |
| `description` | string | ✅ | 一行簡介。 |
| `author` | string | ✅ | 作者名稱或 GitHub 帳號。 |
| `entrypoint` | string | ✅ | 主要入口（相對路徑）。 |
| `license` | string | ✅ | 授權（建議 SPDX，如 `MIT`）。 |
| `tags` | string[] | ❌ | 搜尋用標籤。 |
| `files` | string[] | ❌ | 打包時的明確檔案清單。 |
| `dependencies` | object[] | ❌ | 其他 skill 依賴（`{name, version}`）。 |
| `checksum` | string | ❌ | 打包檔的 SHA-256。 |
| `compatibility` | object | ❌ | 相容平台描述。 |
| `metadata.openclaw` | object | ❌ | OpenClaw/CTOS 執行需求（見下方）。 |
| `ctos` | object | ❌ | CTOS 平台額外設定（系統端管理為佳）。 |

### metadata.openclaw

用於描述執行環境需求，常見欄位如下：

- `requires.bins`：必須存在的 binaries（如 `uv`、`gh`）。
- `requires.env`：必須設定的環境變數（如 `GEMINI_API_KEY`）。
- `requires.optional_bins`：非必要但可提升功能的 binaries。
- `primaryEnv`：主要金鑰（用於 UI 引導）。
- `install`：建議安裝方式清單（可選）。

如需在 CTOS 系統端集中管理環境變數與 MCP 參數，請參考 `templates/skill-config.yaml.example`。
