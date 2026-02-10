"""API route definitions for SkillHub server."""

from fastapi import APIRouter

from client.client import SkillHubClient
from server.models import SkillListResponse

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/", response_model=SkillListResponse)
def list_skills() -> SkillListResponse:
    """Return all locally registered skills."""
    client = SkillHubClient()
    skills = client.list_skills()
    return SkillListResponse(skills=skills)
