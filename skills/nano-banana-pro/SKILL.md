---
name: nano-banana-pro
version: "0.4.4"
description: "Nano Banana Pro with auto model fallback — generate/edit images via Gemini Image API. Supports text-to-image and image-to-image (up to 14 images) at 1K/2K/4K resolutions. Fallback chain: gemini-2.5-flash-image → gemini-2.0-flash-exp-image-generation."
author: yazelin
entrypoint: scripts/generate_image.py
license: MIT
homepage: https://github.com/yazelin/nanobanana-pro
tags:
  - ai-image
  - gemini
  - image-generation
  - image-editing
  - fallback
compatibility:
  platforms:
    - openclaw
    - ching-tech-os
metadata:
  openclaw:
    emoji: "🍌"
    requires:
      bins: ["uv"]
      env: ["GEMINI_API_KEY"]
    primaryEnv: GEMINI_API_KEY
    install:
      - id: uv-brew
        kind: brew
        formula: uv
        bins: ["uv"]
        label: "Install uv (brew)"
---

# Nano Banana Pro

Use the bundled script to generate or edit images. Automatically falls back through multiple Gemini models if one fails.

## Prerequisites

- `uv` installed and available in `PATH`
- `GEMINI_API_KEY` environment variable

## Usage

⚠️ **IMPORTANT: MUST use `uv run` or the `generate` wrapper. Do NOT use `python3` directly — dependencies won't be available.**

Generate (wrapper script):

```bash
{baseDir}/scripts/generate --prompt "your image description" --filename "output.png" --resolution 1K
```

Generate (uv run):

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

Edit (single image):

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" -i "/path/in.png" --resolution 2K
```

Multi-image composition (up to 14 images):

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "output.png" -i img1.png -i img2.png -i img3.png
```

## Configuration

- `GEMINI_API_KEY` env var
- Or set `skills.\"nano-banana-pro\".apiKey` / `skills.\"nano-banana-pro\".env.GEMINI_API_KEY` in `~/.openclaw/openclaw.json`

## Notes

- Resolutions: `1K` (default), `2K`, `4K`.
- Models tried in order: `gemini-2.5-flash-image` → `gemini-2.0-flash-exp-image-generation` (configurable via `NANOBANANA_FALLBACK_MODELS` env var).
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`.
- The script prints a `MEDIA:` line for OpenClaw to auto-attach on supported chat providers.
- Do not read the image back; report the saved path only.
