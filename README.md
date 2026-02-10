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

## Schema

The canonical metadata schema lives at [`schemas/skill.schema.json`](schemas/skill.schema.json).  
It defines required fields (`name`, `version`, `description`, `author`, `entrypoint`) and the `ctos` namespace for platform-specific metadata.

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
