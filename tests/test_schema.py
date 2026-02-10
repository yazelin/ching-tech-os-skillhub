import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((REPO_ROOT / "schemas" / "skill.schema.json").read_text(encoding="utf-8"))


def extract_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("malformed frontmatter")
    fm_text = parts[1]
    meta = {}
    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "":
            vals = []
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("-"):
                vals.append(lines[j].strip().lstrip("-").strip())
                j += 1
            meta[key] = vals
            i = j
            continue
        meta[key] = val.strip('"').strip("'")
        i += 1
    return meta


def test_all_skills_valid():
    # Use jsonschema if available, otherwise basic required-field checks
    try:
        import jsonschema
    except Exception:
        jsonschema = None

    skills_dir = REPO_ROOT / "skills"
    for md in sorted(skills_dir.rglob("SKILL.md")):
        meta = extract_frontmatter(md)
        assert "name" in meta
        assert "version" in meta
        assert "author" in meta
        assert "entrypoint" in meta
        assert "tags" in meta
        if jsonschema is not None:
            validator = jsonschema.Draft202012Validator(SCHEMA)
            errors = list(validator.iter_errors(meta))
            assert errors == []


def test_index_consistency():
    idx = json.loads((REPO_ROOT / "index.json").read_text(encoding="utf-8"))
    slugs = {s["slug"] for s in idx.get("skills", [])}
    local = {p.parent.name for p in (REPO_ROOT / "skills").rglob("SKILL.md")}
    for slug in slugs:
        assert slug in local
