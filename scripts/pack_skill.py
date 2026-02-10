#!/usr/bin/env python3
"""Package a skill folder into a .zip artifact and print its SHA-256 checksum.

Usage:
    python scripts/pack_skill.py skills/example-skill
"""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path


def pack(skill_dir: Path) -> Path:
    """Create a zip of *skill_dir* and return the archive path."""
    skill_dir = skill_dir.resolve()
    if not skill_dir.is_dir():
        raise FileNotFoundError(f"Not a directory: {skill_dir}")

    archive_name = f"{skill_dir.name}.zip"
    archive_path = skill_dir.parent / archive_name

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(skill_dir.rglob("*")):
            if file.is_file():
                zf.write(file, file.relative_to(skill_dir.parent))

    return archive_path


def checksum(path: Path) -> str:
    """Return the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scripts/pack_skill.py <skill-directory>")
        sys.exit(2)

    skill_dir = Path(sys.argv[1])
    archive = pack(skill_dir)
    sha = checksum(archive)
    print(f"Packed: {archive}")
    print(f"SHA-256: {sha}")


if __name__ == "__main__":
    main()
