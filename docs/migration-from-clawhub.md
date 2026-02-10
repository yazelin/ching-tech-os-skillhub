# Migration from ClawHub

## Background

**ClawHub** was the original skill format used in early CTOS prototypes.  
**SkillHub** replaces it with a standardized, schema-validated approach.

## Key Differences

| Aspect               | ClawHub                        | SkillHub                              |
|----------------------|--------------------------------|---------------------------------------|
| Metadata file        | `skill.json`                   | `SKILL.md` (YAML frontmatter)        |
| Validation           | Manual / ad-hoc                | JSON Schema (`skill.schema.json`)     |
| Platform binding     | Top-level `platform` field     | Nested `ctos` namespace               |
| Upgrade policy       | Not supported                  | `ctos.upgrade_policy` field            |
| Documentation        | Separate `README.md`           | Integrated in `SKILL.md` body         |
| Packaging            | Manual tar/zip                 | `scripts/pack_skill.py` with checksum |
| Lockfile             | None                           | `skills-lock.json`                    |

## Step-by-Step Migration

### 1. Convert `skill.json` → `SKILL.md`

Take your existing `skill.json`:

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "main": "run.py"
}
```

Create a `SKILL.md` with frontmatter:

```yaml
---
name: my-skill
version: "1.0.0"
description: "Describe your skill here."
author: your-handle
entrypoint: run.py
files: [run.py, SKILL.md]
ctos:
  version: "0.1.0"
---
# My Skill

Your existing README content goes here.
```

### 2. Add CTOS Namespace

If your ClawHub skill had a `platform` field, map it:

- `platform: "ctos-0.1"` → `ctos.version: "0.1.0"`
- Add `ctos.compatible_with` and `ctos.upgrade_policy` as needed.

### 3. Validate

```bash
python scripts/validate_skill.py skills/my-skill/SKILL.md
```

### 4. Remove Old Files

Delete `skill.json` once `SKILL.md` passes validation.

## FAQ

**Q: Can I keep both `skill.json` and `SKILL.md` during transition?**  
A: Yes, but SkillHub only reads `SKILL.md`. The old file is ignored.

**Q: Do I need to change my entrypoint script?**  
A: No. Only the metadata format changed. Your scripts remain the same.
