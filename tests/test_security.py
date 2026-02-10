import hashlib
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_hash_verification():
    idx = __import__("json").loads((REPO_ROOT / "index.json").read_text(encoding="utf-8"))
    # find first entry that maps to a local zip file in the repo
    found = None
    for s in idx.get("skills", []):
        slug = s.get("slug")
        candidate = REPO_ROOT / f"{slug}.zip"
        # also check common filenames
        alt = REPO_ROOT / f"{slug}-1.0.0.zip"
        if candidate.exists():
            found = (s, candidate)
            break
        if alt.exists():
            found = (s, alt)
            break
    if found is None:
        pytest.skip("No local zip artifacts to verify in this repo")
    entry, local_zip = found
    h = hashlib.sha256()
    with open(local_zip, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    # only check if entry has a non-empty sha
    if entry.get("sha256"):
        assert h.hexdigest() == entry["sha256"]


def test_path_traversal(tmp_path):
    # create malicious zip with a path traversal entry
    malicious = tmp_path / "mal.zip"
    with zipfile.ZipFile(malicious, "w") as zf:
        zf.writestr("../../../etc/passwd", "fake")
    # simulate extraction using safe routine that should be provided by the installer
    extract_dir = tmp_path / "extract"
    extract_dir.mkdir()

    # naive extraction (vulnerable): using zipfile.extractall would write outside the dir
    with zipfile.ZipFile(malicious) as zf:
        # ensure our test detects traversal
        bad_names = [n for n in zf.namelist() if Path(n).parts[0] == ".." or ".." in Path(n).parts]
        assert bad_names, "malicious zip did not contain traversal paths"

    # The installer should refuse or sanitize such archives. Here we assert sanitization: no file is created outside extract_dir
    # Attempt safe extraction (the production code should implement similar protection)
    # Use the client's safe_extract utility to ensure no traversal occurs
    from client.client import safe_extract
    extracted = safe_extract(malicious, extract_dir)
    # Ensure none of the extracted files escaped the extract_dir
    for e in extracted:
        resolved = (extract_dir / Path(e)).resolve()
        assert str(resolved).startswith(str(extract_dir.resolve())), "Path traversal detected"
