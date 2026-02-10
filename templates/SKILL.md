---
name: my-skill-name
version: "1.0.0"
description: "A short description of what this skill does."
author: your-github-handle
tags:
  - automation
  - example
entrypoint: run.py
files:
  - run.py
  - SKILL.md
license: MIT
checksum: ""
dependencies: []
ctos:
  version: "0.1.0"
  compatible_with:
    - "0.1.0"
  upgrade_policy: notify
---

# Skill Title

## Overview

Describe what this skill does, why it exists, and when to use it.

## Usage

```bash
python run.py
```

## Configuration

List any environment variables or config files the skill reads.

| Key | Default | Description |
|-----|---------|-------------|
| `EXAMPLE_VAR` | `""` | An example environment variable. |

## Files

- `run.py` — Main entrypoint script.
- `SKILL.md` — This metadata and documentation file.

## Author

Your Name — <your-email@example.com>

## License

MIT
