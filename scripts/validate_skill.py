#!/usr/bin/env python3
"""Validate a SKILL.md frontmatter against the SkillHub JSON Schema.

Usage:
    python scripts/validate_skill.py skills/example-skill/SKILL.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except Exception:
    jsonschema = None

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "skill.schema.json"


def extract_frontmatter(skill_md: Path) -> dict:
    """Parse YAML frontmatter from a SKILL.md file using PyYAML."""
    import yaml
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{skill_md}: missing YAML frontmatter delimiter.")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{skill_md}: malformed frontmatter.")
    fm_text = parts[1]
    data = yaml.safe_load(fm_text)
    if not isinstance(data, dict):
        raise ValueError(f"{skill_md}: frontmatter did not parse to a mapping")
    return data


def validate(skill_md: Path) -> bool:
    """Return True if the frontmatter is valid; print errors otherwise."""
    meta = extract_frontmatter(skill_md)

    # If jsonschema is not installed (CI or restricted env), perform a basic required-field check.
    if jsonschema is None:
        missing = [k for k in ("name", "version", "author", "entrypoint", "tags") if k not in (meta or {})]
        if missing:
            for m in missing:
                print(f"  ERROR [missing]: required field '{m}' is missing")
            return False
        print(f"  OK: {skill_md} basic validation passed (jsonschema not available).")
        return True

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(meta), key=lambda e: list(e.path))

    if errors:
        for err in errors:
            loc = ".".join(str(p) for p in err.absolute_path) or "(root)"
            print(f"  ERROR [{loc}]: {err.message}")
        return False

    print(f"  OK: {skill_md} is valid.")
    return True


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_skill.py <SKILL.md> [SKILL.md ...]")
        sys.exit(2)

    all_ok = True
    for path_str in sys.argv[1:]:
        p = Path(path_str)
        if not p.exists():
            print(f"  SKIP: {p} does not exist.")
            all_ok = False
            continue
        if not validate(p):
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
