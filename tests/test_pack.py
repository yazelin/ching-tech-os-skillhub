from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_pack_skill(tmp_path):
    pkg = __import__("importlib").machinery.SourceFileLoader("pack_skill", str(REPO_ROOT / "scripts" / "pack_skill.py")).load_module()
    archive = pkg.pack(REPO_ROOT / "skills" / "example-skill")
    assert archive.exists()
    # cleanup
    archive.unlink()


def test_validate_skill():
    validator = __import__("importlib").machinery.SourceFileLoader("validate", str(REPO_ROOT / "scripts" / "validate_skill.py")).load_module()
    # validate one SKILL.md
    ok = validator.validate(REPO_ROOT / "skills" / "example-skill" / "SKILL.md")
    assert ok
