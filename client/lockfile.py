"""Lockfile management for installed skills (skills-lock.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from client.models import Skill


class LockFile:
    """Read/write a simple JSON lockfile that tracks installed skills."""

    def __init__(self, path: str | Path = "skills-lock.json") -> None:
        self.path = Path(path)

    def _read(self) -> dict[str, Any]:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {"skills": {}}

    def _write(self, data: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def add(self, skill: Skill) -> None:
        """Record a skill in the lockfile."""
        data = self._read()
        data["skills"][skill.name] = {
            "version": skill.version,
            "checksum": skill.checksum,
        }
        self._write(data)

    def remove(self, name: str) -> bool:
        """Remove a skill entry. Returns True if it existed."""
        data = self._read()
        removed = data["skills"].pop(name, None) is not None
        if removed:
            self._write(data)
        return removed

    def list_installed(self) -> dict[str, dict[str, str]]:
        """Return the dict of installed skills."""
        return self._read().get("skills", {})
