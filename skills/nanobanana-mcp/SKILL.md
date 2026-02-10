# NanoBanana MCP

tags: ["ai", "image-generation", "mcp", "gemini"]

簡介
---
NanoBanana 是一個以 Google Gemini 為後端的 AI 圖片生成 MCP Server（Python），提供文字轉圖、圖片編修、圖片修復、圖示/圖樣/故事序列與技術圖表等功能，並具備自動 fallback 機制以在主模型失敗時切換備用模型。

快速開始
---
1. 安裝：

```bash
pip install nanobanana-py
```

2. 設定 API Key（至少設定一個）：

```bash
export NANOBANANA_GEMINI_API_KEY="your-api-key-here"
# 或使用備援變數
export NANOBANANA_GOOGLE_API_KEY="..."
export GEMINI_API_KEY="..."
```

3. 在 .mcp.json 中加入（範例）：

```json
{
  "mcpServers": {
    "nanobanana": {
      "command": "uvx",
      "args": ["nanobanana-py"],
      "env": {
        "NANOBANANA_GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

使用說明（主要功能）
---
- generate_image(prompt, output_count=1, styles=[], variations=[], resolution="1K", preview=False, parallel=2)
  - 文字生成圖片，支援單張或多張輸出、風格與變化類型。
- edit_image(file, prompt, resolution="1K", preview=False)
  - 對既有圖片進行自然語言編修。
- restore_image(file, prompt, resolution="1K", preview=False)
  - 修復並強化受損或老舊照片。
- generate_icon(prompt, sizes=[1024], type="app-icon", style="modern")
  - 生成 App 圖示、favicon 與 UI 元件。
- generate_pattern(prompt, size="256x256", type="seamless")
  - 生成可無縫拼接的圖樣與背景材質。
- generate_story(prompt, steps=4, layout="separate")
  - 生成故事序列或教學步驟的多張圖片。
- generate_diagram(prompt, type="flowchart", style="professional")
  - 生成技術圖表與流程圖。

環境變數與設定
---
- NANOBANANA_GEMINI_API_KEY (建議，必要)
- NANOBANANA_GOOGLE_API_KEY / GEMINI_API_KEY / GOOGLE_API_KEY (備援)
- NANOBANANA_MODEL （預設：gemini-2.5-flash-image）
- NANOBANANA_FALLBACK_MODELS （逗號分隔）
- NANOBANANA_TIMEOUT （秒，預設 60）
- NANOBANANA_OUTPUT_DIR （輸出目錄）
- NANOBANANA_DEBUG (設定為 1 啟用除錯日誌)

注意事項
---
- 建議在生產環境限制並妥善保護 API 金鑰。
- fallback 會在主模型超時或錯誤時依序嘗試備用模型，回應會包含使用的模型資訊。

參考
---
- 原始專案：https://github.com/yazelin/nanobanana-py
- 使用說明與參數請參考套件 README
