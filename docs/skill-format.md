# Skill Format Specification

## SKILL.md

Every skill **must** contain a `SKILL.md` file at its root.  
This file combines human-readable documentation with machine-readable YAML frontmatter.

### Frontmatter Fields

| Field          | Type       | Required | Description                                    |
|----------------|------------|----------|------------------------------------------------|
| `name`         | string     | ✅       | Unique identifier (lowercase, hyphens only).   |
| `version`      | string     | ✅       | Semantic version (`MAJOR.MINOR.PATCH`).        |
| `description`  | string     | ✅       | Short one-line description.                    |
| `author`       | string     | ✅       | Author name or GitHub handle.                  |
| `tags`         | string[]   | ❌       | Searchable tags for categorization.            |
| `entrypoint`   | string     | ✅       | Relative path to main script (e.g. `run.py`). |
| `files`        | string[]   | ❌       | Explicit file list for packaging.              |
| `license`      | string     | ❌       | SPDX identifier. Defaults to `MIT`.            |
| `checksum`     | string     | ❌       | SHA-256 of the packaged artifact.              |
| `dependencies` | object[]   | ❌       | List of `{name, version}` skill dependencies.  |
| `ctos`         | object     | ❌       | CTOS platform namespace (see below).           |

### CTOS Namespace

The `ctos` object provides platform-specific metadata:

| Field              | Type     | Required | Description                         |
|--------------------|----------|----------|-------------------------------------|
| `ctos.version`     | string   | ✅*      | Target CTOS version.                |
| `ctos.compatible_with` | string[] | ❌   | Tested CTOS versions.               |
| `ctos.upgrade_policy`  | string   | ❌   | `auto`, `manual`, or `notify`.      |

*Required when `ctos` object is present.

### Name Conventions

- Lowercase alphanumeric with hyphens: `my-cool-skill`
- No underscores, no uppercase, no spaces.
- Maximum 64 characters.

### Example

```yaml
---
name: weather-checker
version: "1.2.0"
description: "Fetches current weather for a configured location."
author: yaze
tags: [weather, utility]
entrypoint: main.py
files: [main.py, SKILL.md, config.yaml]
license: MIT
ctos:
  version: "0.1.0"
  compatible_with: ["0.1.0"]
  upgrade_policy: auto
---
```

## Validation

Use the provided script:

```bash
python scripts/validate_skill.py skills/weather-checker/SKILL.md
```

Or programmatically with `jsonschema` against `schemas/skill.schema.json`.
