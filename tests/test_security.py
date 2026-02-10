import hashlib
import io
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_hash_verification():
    idx = __import__("json").loads((REPO_ROOT / "index.json").read_text(encoding="utf-8"))
    # pick md2doc which points to local md2doc-evolution-1.3.0.zip
    entry = next(s for s in idx["skills"] if s["slug"] == "md2doc")
    local_zip = REPO_ROOT / "md2doc-evolution-1.3.0.zip"
    assert local_zip.exists()
    h = hashlib.sha256()
    with open(local_zip, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
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
    for member in zipfile.ZipFile(malicious).infolist():
        member_path = Path(member.filename)
        resolved = (extract_dir / member_path).resolve()
        assert str(resolved).startswith(str(extract_dir.resolve())), "Path traversal detected"
