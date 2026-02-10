"""Pydantic models for SkillHub skill metadata."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class CTOSMeta(BaseModel):
    """CTOS-specific metadata embedded in a skill."""

    version: str = Field(..., description="Target CTOS platform version.")
    compatible_with: list[str] = Field(
        default_factory=list,
        description="CTOS versions this skill is tested against.",
    )
    upgrade_policy: str = Field(
        default="notify",
        description="Upgrade policy: auto | manual | notify.",
    )


class Dependency(BaseModel):
    """A dependency on another skill."""

    name: str
    version: str


class Skill(BaseModel):
    """Full skill metadata matching skill.schema.json."""

    name: str
    version: str
    description: str
    author: str
    tags: list[str] = Field(default_factory=list)
    entrypoint: str
    files: list[str] = Field(default_factory=list)
    license: str = "MIT"
    checksum: str = ""
    dependencies: list[dict] = Field(default_factory=list)
    ctos: Optional[dict] = None
