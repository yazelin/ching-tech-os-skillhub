import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((REPO_ROOT / "schemas" / "skill.schema.json").read_text(encoding="utf-8"))


def extract_frontmatter(skill_md: Path) -> dict:
    import yaml
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("malformed frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter did not parse to a mapping")
    return data


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
