# Architecture

## Overview

SkillHub is structured as a three-layer system:

```
┌────────────┐     ┌────────────┐     ┌───────────┐
│  CLI / SDK │ ──▶ │  Client    │ ──▶ │  Skills/  │
│  (user)    │     │  Library   │     │  (local)  │
└────────────┘     └────────────┘     └───────────┘
                         │
                         ▼
                   ┌────────────┐
                   │  FastAPI   │
                   │  Server    │
                   └────────────┘
```

### 1. Client Library (`client/`)

The client is a pure-Python library with no network dependencies.  
It scans a local `skills/` directory, parses `SKILL.md` frontmatter (YAML), and returns Pydantic models.

Key classes:
- **SkillHubClient** — discovery and inspection.
- **SkillInstaller** — copies skill folders and manages the lockfile.
- **LockFile** — reads/writes `skills-lock.json` for reproducible installs.

### 2. Server (`server/`)

A minimal FastAPI application that exposes the client's data over HTTP.  
Currently offers `GET /skills/` to list all registered skills.  
Designed to be extended with authentication, search, and remote registry support.

### 3. Skills Directory (`skills/`)

Each sub-directory is a self-contained skill.  
The only required file is `SKILL.md` with valid YAML frontmatter.  
The `entrypoint` field points to the script that runs the skill.

## Data Flow

1. User runs `skillhub list` → Client scans `skills/` → returns Pydantic `Skill` objects.
2. User runs `python scripts/validate_skill.py` → YAML frontmatter is validated against `schemas/skill.schema.json`.
3. User runs `python scripts/pack_skill.py` → skill folder is zipped with a SHA-256 checksum.
4. Server imports `SkillHubClient` and exposes the same data via REST.

## Design Decisions

- **Frontmatter-in-Markdown**: skills are documented and machine-readable in one file.
- **No database**: the filesystem *is* the registry for the local case.
- **Pydantic v2**: strict validation, JSON-serializable models.
- **JSON Schema**: enables cross-language validation (not just Python).
