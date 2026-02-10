---
name: nano-banana-pro
version: "1.0.0"
description: "Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). Supports text-to-image, image editing, and multi-image composition."
author: yazelin
tags:
  - ai-image
  - gemini
  - image-generation
  - image-editing
entrypoint: scripts/generate_image.py
---

# Nano Banana Pro (Gemini 3 Pro Image)

🍌 使用 Google Gemini 3 Pro Image API 生成或編輯圖片的 Skill。

包含完整可執行的 Python 腳本，支援：
- **文字生成圖片** — 描述即生成
- **單圖編輯** — 上傳一張圖 + 編輯指令
- **多圖合成** — 最多 14 張圖片合成（構圖、風格轉換等）

## 前置需求

- Python >= 3.10
- `uv`（推薦）或 `pip`
- `GEMINI_API_KEY` 環境變數

## 使用方式

### 生成圖片

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一幅水彩畫：雪地森林裡的狐狸" --filename "fox.png" --resolution 1K
```

### 編輯圖片

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "把背景換成星空" --filename "output.png" -i "/path/to/input.png" --resolution 2K
```

### 多圖合成（最多 14 張）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "output.png" -i img1.png -i img2.png -i img3.png
```

## API Key 設定

三種方式（優先順序由高到低）：

1. 命令列參數：`--api-key YOUR_KEY`
2. 環境變數：`export GEMINI_API_KEY="YOUR_KEY"`
3. OpenClaw config：`skills."nano-banana-pro".apiKey`

## 參數說明

| 參數 | 說明 |
|------|------|
| `--prompt, -p` | 圖片描述或編輯指令（必填） |
| `--filename, -f` | 輸出檔名（必填） |
| `--resolution, -r` | 解析度：1K（預設）、2K、4K |
| `--input-image, -i` | 輸入圖片路徑（可多次指定，最多 14 張） |
| `--api-key, -k` | Gemini API Key |

## 注意事項

- 解析度建議用 1K 即可（速度快、品質夠）
- 檔名建議加時間戳：`yyyy-mm-dd-hh-mm-ss-name.png`
- 腳本會輸出 `MEDIA:` 行，OpenClaw 會自動在聊天中附加圖片
- 編輯模式會自動偵測輸入圖片尺寸來調整輸出解析度
- 不要讀回生成的圖片內容，只回報檔案路徑

## 實際程式碼

`scripts/generate_image.py` — 176 行完整可執行的 Python 腳本，使用 `google-genai` SDK 直接呼叫 Gemini API。不是 wrapper、不是範例、是真的能跑的程式。
