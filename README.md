# SkillHub

**SkillHub** is the skill registry and client for **Ching Tech OS (CTOS)**.  
It provides tooling to discover, validate, install, and serve CTOS skills — self-contained automation units described by a `SKILL.md` metadata file.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# List locally available skills
python -m client.client list

# Validate installed skills have their entrypoints
python -m client.client validate

# Inspect a single skill
python -m client.client info example-skill

# Validate a skill's metadata against the schema
python scripts/validate_skill.py skills/example-skill/SKILL.md

# Package a skill into a zip artifact
python scripts/pack_skill.py skills/example-skill

# Start the API server (development)
python -m server.main
```

## Authoring a Skill

1. Copy `templates/SKILL.md` into a new directory under `skills/`:
   ```bash
   mkdir skills/my-new-skill
   cp templates/SKILL.md skills/my-new-skill/SKILL.md
   ```
2. Edit the YAML frontmatter with your skill's metadata.
3. Add your scripts (e.g., `run.py`) and list them in the `files` field.
4. Validate: `python scripts/validate_skill.py skills/my-new-skill/SKILL.md`

See [docs/skill-format.md](docs/skill-format.md) for the full specification.

## Skill Format 說明

`SKILL.md` 使用 YAML frontmatter + 文字說明來描述技能。除了基本欄位外，建議提供 `metadata.openclaw` 以宣告需要的 binaries 與環境變數，方便 CTOS/OpenClaw 在載入時檢查依賴。

## CTOS Integration

CTOS 會讀取 `metadata.openclaw.requires` 來確認必要的 `bins` 與 `env` 是否存在。系統端設定範本可參考 `templates/skill-config.yaml.example`，用來集中管理 skill 的環境變數與 MCP server 參數。

## Contributing

歡迎 PR！請在新增或修改技能後更新 `SKILL.md`，並執行 `python scripts/validate_skill.py skills/<skill>/SKILL.md` 驗證格式。若新增欄位或調整格式，請同步更新 `docs/skill-format.md`。

## Schema

The canonical metadata schema lives at [`schemas/skill.schema.json`](schemas/skill.schema.json).  
It defines required fields (`name`, `version`, `description`, `author`, `entrypoint`) and the `ctos` namespace for platform-specific metadata (deprecated in SKILL.md; system-side config recommended).

## Project Layout

```
ching-tech-os-skillhub/
├── client/          # Python client library & CLI
├── server/          # FastAPI HTTP interface
├── schemas/         # JSON Schema for skill metadata
├── templates/       # SKILL.md template for new skills
├── skills/          # Local skill registry (git-tracked examples)
├── scripts/         # Validation & packaging utilities
├── docs/            # Architecture & format documentation
└── .github/         # CI workflows
```

## Migration from ClawHub

SkillHub is the successor to the earlier **ClawHub** skill format.  
See [docs/migration-from-clawhub.md](docs/migration-from-clawhub.md) for a step-by-step migration guide.  
Key changes: unified `SKILL.md` frontmatter, JSON Schema validation, and a `ctos` namespace for platform bindings.

## License

[MIT](LICENSE)
