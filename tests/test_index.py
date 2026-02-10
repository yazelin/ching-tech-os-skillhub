import json
from pathlib import Path
import pytest

def test_index_structure():
    """Validate structure of index.json."""
    root = Path(__file__).resolve().parent.parent
    index_path = root / "index.json"
    
    if not index_path.exists():
        pytest.skip("index.json not found")
        
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        pytest.fail("index.json is not valid JSON")
        
    required_root = ["version", "updated_at", "skills"]
    for field in required_root:
        assert field in data, f"Missing root field: {field}"
        
    assert isinstance(data["skills"], list), "skills must be a list"
    
    required_skill = ["slug", "name", "version", "description", "author"]
    for skill in data["skills"]:
        for field in required_skill:
            assert field in skill, f"Skill {skill.get('slug', '?')} missing {field}"
            
        # Optional check for download_url format if present
        if skill.get("download_url"):
            assert skill["download_url"].startswith("http"), f"Invalid URL for {skill['slug']}"
