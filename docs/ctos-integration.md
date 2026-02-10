# CTOS Integration with SkillHub Design Document

## 1. Overview
This document outlines the architecture for integrating Ching Tech OS (CTOS) with the new SkillHub repository. It covers the client-side Skill Manager, API interactions, UI design, update mechanisms, security, and migration from ClawHub.

## 2. Skill Manager Module Architecture

The `SkillManager` is the core component within CTOS responsible for managing the lifecycle of skills.

### 2.1 Class Structure

```python
class SkillManager:
    def __init__(self, storage_path: str, remote_url: str, public_key: str):
        self.storage_path = storage_path
        self.remote_url = remote_url
        self.verifier = SignatureVerifier(public_key)
        self.registry = LocalRegistry(os.path.join(storage_path, "registry.json"))

    def search_remote_skills(self, query: str, filters: dict) -> List[SkillMetadata]:
        """Queries SkillHub for available skills."""
        pass

    def get_skill_details(self, skill_id: str) -> SkillDetails:
        """Fetches detailed info including dependencies and versions."""
        pass

    def install_skill(self, skill_id: str, version: str = "latest") -> bool:
        """
        1. Checks dependencies.
        2. Downloads artifact.
        3. Verifies signature/checksum.
        4. Extracts to staging.
        5. Validates manifest.
        6. Moves to active skills directory.
        7. Updates local registry.
        """
        pass

    def uninstall_skill(self, skill_id: str) -> bool:
        """Removes skill files and updates registry."""
        pass

    def update_check(self) -> List[UpdateAvailable]:
        """Checks installed skills against remote for newer versions."""
        pass

    def update_skill(self, skill_id: str, target_version: str) -> bool:
        """Performs transactional update (backup -> install -> verify -> commit/rollback)."""
        pass

    def _download_artifact(self, url: str, destination: str) -> str:
        """Downloads file with progress tracking."""
        pass

    def _verify_integrity(self, file_path: str, signature: str, checksum: str) -> bool:
        """Verifies SHA256 checksum and cryptographic signature."""
        pass
```

### 2.2 Local Storage Layout

```text
/ching-tech-os/skills/
├── registry.json       # Tracks installed skills, versions, and status
├── lockfile.json       # Resolved dependency tree
├── installed/
│   ├── <skill_id_v1>/  # Active skill files
│   └── <skill_id_v2>/
└── cache/              # Downloaded artifacts
```

## 3. REST API Interactions

CTOS acts as a client to the SkillHub Server.

### 3.1 Endpoints

*   **Search**: `GET /api/v1/skills?q={query}&tags={tags}&page={page}`
*   **Details**: `GET /api/v1/skills/{skill_id}`
*   **Version Info**: `GET /api/v1/skills/{skill_id}/versions/{version}`
*   **Download**: `GET /api/v1/skills/{skill_id}/versions/{version}/download`
    *   Returns 302 Redirect to object storage or stream.
*   **Batch Update Check**: `POST /api/v1/updates/check`

### 3.2 Example Payloads

**Batch Update Check Request:**
```json
{
  "installed_skills": [
    { "id": "net.chingtech.accounting", "version": "1.2.0" },
    { "id": "net.chingtech.crm", "version": "2.0.1" }
  ],
  "channel": "stable"
}
```

**Batch Update Check Response:**
```json
{
  "updates": [
    {
      "id": "net.chingtech.accounting",
      "current_version": "1.2.0",
      "latest_version": "1.3.0",
      "severity": "minor",
      "release_notes": "Fixes VAT calculation bug."
    }
  ]
}
```

## 4. Web UI Marketplace

The Marketplace is a module in the CTOS Admin Panel.

### 4.1 Mockup Description

**Layout:**
*   **Header**: "Skill Marketplace", Search Bar (global), "Check for Updates" button.
*   **Sidebar**: Categories (Finance, Operations, HR), Filters (Official, Community, Verified), Sort (Popularity, Newest).
*   **Main Content Area**:
    *   **Grid View**: Cards for each skill showing Icon, Name, Author, Star Rating, "Install" button.
    *   **Tabs**: "Discover", "Installed", "Updates Available (badge)".

**Skill Detail Modal:**
*   Large Icon & Banner.
*   Description (Markdown support).
*   Screenshots carousel.
*   Version History dropdown.
*   Dependencies list.
*   Permissions requested (e.g., "Read Sales Data").
*   Action Buttons: "Install", "Update", "Settings", "Uninstall".

### 4.2 Interaction Patterns

1.  **Search**: Debounced input triggers `SkillManager.search_remote_skills`. Results update asynchronously.
2.  **Install**:
    *   User clicks "Install".
    *   UI shows spinner/progress bar (WebSocket or polling task status).
    *   On success: Toast notification "Skill Installed", button changes to "Open".
    *   On failure: Error modal with logs.
3.  **Update**:
    *   "Updates Available" tab shows list of outdated skills with "Update All" or individual "Update" buttons.
    *   Diff view of permissions (if changed) requires user confirmation before updating.

## 5. Automatic Update Mechanism

### 5.1 Strategy

*   **Polling**: CTOS background cron job runs `SkillManager.update_check()` daily (randomized time to avoid thundering herd). Webhooks are not used to avoid exposing CTOS instances to the public internet.
*   **Lockfile**: `skill-lock.json` pins exact versions. Updates modify this file.
*   **Transactional Updates**:
    1.  **Prepare**: Download new version to temp dir. verify signature.
    2.  **Backup**: Snapshot current version data/config.
    3.  **Swap**: Atomic directory switch (symlink or rename).
    4.  **Migrate**: Run skill-defined migration scripts.
    5.  **Commit**: If health check passes, delete backup.
    6.  **Rollback**: On failure, restore backup and alert admin.

### 5.2 Policies

*   **Silent Updates**: Enabled by default for patch versions (x.x.Z) and security fixes.
*   **User Prompt**: Required for major versions (X.x.x) or if new permissions are requested.
*   **Channels**: Users can subscribe to `stable`, `beta`, or `nightly`.

## 6. Security Considerations

### 6.1 Verification
*   **Checksums**: SHA256 hash of the artifact is verified against the manifest.
*   **Signatures**: All official skills must be signed by Ching Tech's private key. Community skills must be signed by a verified developer key.
*   **Trust on First Use (TOFU)**: Public keys are pinned upon installation.

### 6.2 Permissions Model
*   Skills define a `manifest.json` requesting capabilities:
    ```json
    "permissions": ["db:read:sales", "network:outbound", "filesystem:temp"]
    ```
*   CTOS runtime enforces these via API gateways or capability tokens.

### 6.3 Sandboxing
*   Skills run in isolated subprocesses or lightweight containers (Docker/Podman if available, otherwise strict process isolation).
*   File system access restricted to the skill's own data directory.

## 7. Backwards Compatibility (ClawHub)

### 7.1 Adapter Layer
We introduce a `SkillSource` interface to abstract the backend.

```python
class SkillSource(ABC):
    @abstractmethod
    def search(self, query): pass
    @abstractmethod
    def fetch(self, id): pass

class SkillHubAdapter(SkillSource):
    # New implementation
    pass

class ClawHubAdapter(SkillSource):
    # Legacy implementation wrapping old ClawHub API
    pass
```

### 7.2 Migration Plan
1.  **Phase 1 (Hybrid)**: CTOS ships with both adapters. `SkillManager` aggregates results. Installed ClawHub skills are marked as "Legacy".
2.  **Phase 2 (Mapping)**: A mapping file (`claw_to_skill_map.json`) is maintained to associate old ClawHub IDs with new SkillHub IDs.
3.  **Phase 3 (Migration Tool)**:
    *   User clicks "Migrate to SkillHub".
    *   Tool checks installed ClawHub skills against the map.
    *   Downloads equivalent SkillHub versions.
    *   Migrates config/data.
    *   Uninstalls ClawHub version.
4.  **Phase 4 (Deprecation)**: ClawHub adapter removed in CTOS v4.0.

## 8. Sequence Diagrams

### 8.1 Install Skill

```text
User          Web UI          CTOS Backend (SkillMgr)      SkillHub
 |               |                    |                       |
 |--- Install -->|                    |                       |
 |               |--- POST /install ->|                       |
 |               |                    |--- Get Manifest ----->|
 |               |                    |<-- JSON + Sig --------|
 |               |                    | (Verify Signature)    |
 |               |                    |--- Download Artifact->|
 |               |                    |<-- Zip File ----------|
 |               |                    | (Verify Checksum)     |
 |               |                    | (Extract & Install)   |
 |               |<-- Task ID --------|                       |
 |<-- Spinner ---|                    |                       |
 |               |--- Poll Status --->|                       |
 |               |<-- Progress % -----|                       |
 |               |<-- Success --------|                       |
 |<-- "Ready" ---|                    |                       |
```

### 8.2 Auto-Update (Background)

```text
Cron Job      SkillMgr            Local Registry           SkillHub
 |               |                    |                       |
 |--- Trigger -->|                    |                       |
 |               |--- Load Installed->|                       |
 |               |<-- List [v1.0] ----|                       |
 |               |-------------------- POST /updates/check -->|
 |               |<------------------- Updates [v1.1] --------|
 |               | (Policy Check: Silent OK?)                 |
 |               |--- Download v1.1 ------------------------->|
 |               | (Verify & Install to Staging)              |
 |               |--- Stop v1.0 Service --------------------->|
 |               |--- Run Migrations ------------------------>|
 |               |--- Swap Directories ---------------------->|
 |               |--- Start v1.1 Service -------------------->|
 |               |--- Update Registry ----------------------->|
```
