"""Skill installer — copies a skill folder to a target directory and updates the lockfile."""

from __future__ import annotations

import shutil
from pathlib import Path

from client.lockfile import LockFile
from client.models import Skill


class SkillInstaller:
    """Installs a skill by copying its directory to a target location."""

    def __init__(
        self,
        target_dir: str | Path = "installed_skills",
        lockfile_path: str | Path = "skills-lock.json",
    ) -> None:
        self.target_dir = Path(target_dir)
        self.lockfile = LockFile(lockfile_path)

    def install(self, skill: Skill, source_dir: Path) -> Path:
        """Copy *source_dir* into target_dir/<skill.name> and record in lockfile.

        Returns the destination path.
        """
        dest = self.target_dir / skill.name
        self.target_dir.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source_dir, dest)
        self.lockfile.add(skill)
        return dest

    def uninstall(self, name: str) -> bool:
        """Remove an installed skill by name. Returns True if removed."""
        dest = self.target_dir / name
        if dest.exists():
            shutil.rmtree(dest)
        return self.lockfile.remove(name)
