---
name: example-skill
version: "0.1.0"
description: "A minimal example skill that prints a greeting message."
author: ctos-team
tags:
  - example
  - demo
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

# Example Skill

## Overview

This is a minimal demonstration skill for SkillHub. It prints a greeting
message to stdout, proving that the skill runtime works correctly.

## Usage

```bash
python run.py
```

You should see:

```
[example-skill] Hello from SkillHub! CTOS skill runtime is working.
```

## Files

- `run.py` — Prints a greeting message.
- `SKILL.md` — Skill metadata and documentation.

## Author

CTOS Team

## License

MIT
