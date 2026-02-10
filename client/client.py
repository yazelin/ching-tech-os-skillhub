"""SkillHub client — discover and inspect locally installed skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import urllib.request
import hashlib
import zipfile
import tempfile
import shutil
import os

from client.models import Skill


def _parse_frontmatter(skill_md: Path) -> Optional[dict]:
    """Extract simple YAML frontmatter from a SKILL.md file without external deps.

    Returns the parsed dict or None if frontmatter is missing.
    """
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm_text = parts[1]
    meta: dict = {}
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
            vals: list[str] = []
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


class SkillHubClient:
    """Lightweight client that reads skills from a local directory."""

    def __init__(self, skills_dir: str | Path = "skills") -> None:
        self.skills_dir = Path(skills_dir)

    def list_skills(self) -> list[Skill]:
        """Scan skills_dir for sub-directories containing SKILL.md and return models."""
        results: list[Skill] = []
        if not self.skills_dir.is_dir():
            return results
        for child in sorted(self.skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                meta = _parse_frontmatter(skill_md)
                if meta:
                    results.append(Skill(**meta))
        return results

    def get_skill(self, name: str) -> Optional[Skill]:
        """Return a single skill by name, or None."""
        for skill in self.list_skills():
            if skill.name == name:
                return skill
        return None

    def validate_install(self) -> dict[str, bool]:
        """Check that each skill's entrypoint file exists."""
        report: dict[str, bool] = {}
        for skill in self.list_skills():
            ep = self.skills_dir / skill.name / skill.entrypoint
            report[skill.name] = ep.exists()
        return report


def main() -> None:
    """CLI entrypoint for skillhub."""
    parser = argparse.ArgumentParser(
        prog="skillhub",
        description="SkillHub client — list and inspect CTOS skills.",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    sub.add_parser("list", help="List all skills in the local skills/ directory.")

    # validate
    sub.add_parser("validate", help="Validate that installed skills have their entrypoints.")

    # info
    info_p = sub.add_parser("info", help="Show metadata for a single skill.")
    info_p.add_argument("name", help="Skill name.")

    # remote index and install
    sub.add_parser("list-remote", help="List remote skills from index.json")
    install_p = sub.add_parser("install", help="Install skill by slug from remote index")
    install_p.add_argument("slug", help="Skill slug to install")

    args = parser.parse_args()
    client = SkillHubClient()

    if args.command == "list":
        skills = client.list_skills()
        if not skills:
            print("No skills found.")
            return
        for s in skills:
            print(f"  {s.name}  v{s.version}  — {s.description}")

    elif args.command == "list-remote":
        index_url = "https://raw.githubusercontent.com/yazelin/ching-tech-os-skillhub/main/index.json"
        try:
            with urllib.request.urlopen(index_url) as r:
                idx = json.loads(r.read().decode())
        except Exception as e:
            print("Failed to fetch index:", e)
            sys.exit(1)
        skills = idx.get("skills", [])
        if not skills:
            print("No remote skills found.")
            return
        for s in skills:
            print(f"  {s['slug']}  {s.get('name','')}  v{s.get('version','')}  — {s.get('description','')}")

    elif args.command == "install":
        index_url = "https://raw.githubusercontent.com/yazelin/ching-tech-os-skillhub/main/index.json"
        try:
            with urllib.request.urlopen(index_url) as r:
                idx = json.loads(r.read().decode())
        except Exception as e:
            print("Failed to fetch index:", e)
            sys.exit(1)
        skill = next((s for s in idx.get("skills", []) if s["slug"] == args.slug), None)
        if not skill:
            print(f"Skill '{args.slug}' not found in index.")
            sys.exit(1)
        url = skill["download_url"]
        expected = skill.get("sha256")
        tmpf = tempfile.NamedTemporaryFile(delete=False)
        try:
            urllib.request.urlretrieve(url, tmpf.name)
        except Exception as e:
            print("Download failed:", e)
            sys.exit(1)
        h = hashlib.sha256()
        with open(tmpf.name, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        if expected and h.hexdigest() != expected:
            print("SHA256 mismatch: expected", expected, "got", h.hexdigest())
            sys.exit(1)
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(tmpf.name) as zf:
            zf.extractall(tmpdir)
        entries = [p for p in os.listdir(tmpdir) if p]
        target_dir = client.skills_dir / args.slug
        if target_dir.exists():
            shutil.rmtree(target_dir)
        if len(entries) == 1 and entries[0] == args.slug:
            shutil.move(os.path.join(tmpdir, entries[0]), str(target_dir))
        else:
            os.makedirs(target_dir, exist_ok=True)
            for item in entries:
                shutil.move(os.path.join(tmpdir, item), str(target_dir))
        print(f"Installed {args.slug} -> {target_dir}")

    elif args.command == "validate":
        report = client.validate_install()
        ok = all(report.values())
        for name, valid in report.items():
            status = "OK" if valid else "MISSING entrypoint"
            print(f"  {name}: {status}")
        sys.exit(0 if ok else 1)

    elif args.command == "info":
        skill = client.get_skill(args.name)
        if skill is None:
            print(f"Skill '{args.name}' not found.")
            sys.exit(1)
        print(json.dumps(skill.model_dump(), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
