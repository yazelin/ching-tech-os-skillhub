"""Server-side response models (thin wrappers around client.models)."""

from client.models import Skill  # re-use the canonical model
from pydantic import BaseModel


class SkillListResponse(BaseModel):
    """Response envelope for the GET /skills/ endpoint."""

    skills: list[Skill]
