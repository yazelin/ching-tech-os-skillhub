"""SkillHub client — discover and inspect locally installed skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import yaml

from client.models import Skill


def _parse_frontmatter(skill_md: Path) -> Optional[dict]:
    """Extract YAML frontmatter from a SKILL.md file.

    Returns the parsed dict or None if frontmatter is missing.
    """
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])


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

    args = parser.parse_args()
    client = SkillHubClient()

    if args.command == "list":
        skills = client.list_skills()
        if not skills:
            print("No skills found.")
            return
        for s in skills:
            print(f"  {s.name}  v{s.version}  — {s.description}")

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
