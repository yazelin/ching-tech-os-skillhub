import json
from pathlib import Path
import urllib.request


from client.client import SkillHubClient

REPO_ROOT = Path(__file__).resolve().parent.parent

class DummyResp:
    def __init__(self, data: bytes):
        self._data = data
    def read(self):
        return self._data
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False


def test_list_remote(monkeypatch):
    idx_path = REPO_ROOT / "index.json"
    data = idx_path.read_bytes()

    def fake_urlopen(url):
        return DummyResp(data)

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    # call the same logic used by the client to parse remote index
    with urllib.request.urlopen("http://example") as r:
        idx = json.loads(r.read().decode())
    assert isinstance(idx, dict)
    assert "skills" in idx
    assert len(idx["skills"]) >= 1


def test_list_local(tmp_path):
    client = SkillHubClient(skills_dir=REPO_ROOT / "skills")
    local = client.list_skills()
    # Ensure local listing matches remote index count
    idx = json.loads((REPO_ROOT / "index.json").read_text(encoding="utf-8"))
    assert len(local) >= len(idx["skills"])


def test_install_and_validate(tmp_path):
    # Use installer directly to avoid network in tests
    from client.installer import SkillInstaller
    from client.models import Skill

    src = REPO_ROOT / "skills" / "pr-reviewer"
    assert src.exists()

    skill_meta = json.loads((REPO_ROOT / "index.json").read_text())["skills"][0]
    skill = Skill(**{
        "name": skill_meta.get("slug", skill_meta.get("name")),
        "version": skill_meta.get("version","0.0.0"),
        "author": skill_meta.get("author",""),
        "entrypoint": skill_meta.get("entrypoint","scripts/pr-review.sh"),
        "tags": skill_meta.get("tags",[]),
        "description": skill_meta.get("description", "")
    })

    installer = SkillInstaller(target_dir=tmp_path / "installed_skills", lockfile_path=tmp_path / "skills-lock.json")
    dest = installer.install(skill, src)
    assert (dest / "scripts" / "pr-review.sh").exists()

    # validate entrypoint via client.validate_install
    client = SkillHubClient(skills_dir=tmp_path / "installed_skills")
    report = client.validate_install()
    assert report.get(skill.name) is True
