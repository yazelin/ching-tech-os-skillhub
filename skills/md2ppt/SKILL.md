名稱: MD2PPT-Evolution
slug: md2ppt
version: 1.0.0
author: yazelin
tags: ["document", "ppt", "markdown", "conversion"]

簡介
====
MD2PPT-Evolution 是一個將 Markdown 筆記轉換為可編輯 PowerPoint (.pptx) 的 Web 工具，支援主題系統、圖表轉換、PWA 離線模式與 AI 協助產生內容。

快速使用說明
===========
1. 線上體驗
   - 前往 Demo: https://huangchiyu.com/MD2PPT-Evolution/

2. 本地執行（開發）
   ```bash
   git clone https://github.com/eric861129/MD2PPT-Evolution.git
   cd MD2PPT-Evolution
   npm install
   npm run dev
   # 瀏覽 http://localhost:3000
   ```

3. 基本操作
   - 在左側編輯 Markdown，右側即時預覽。
   - 使用 YAML 前導欄位設定 title、theme、layout 等；範例請見 README。
   - 完成後使用匯出（Export）功能下載 PPTX 檔案，或使用 QRCode 與 P2P 遙控功能。

進階與客製化
===========
- 佈局與主題可在 CUSTOMIZATION.md 中修改與擴充。
- 支援 remark plugin 與自訂 directive（如圖表、特殊版型）。

隱私與授權
=========
- 所有解析與生成皆在用戶端執行，不會上傳筆記資料到伺服器。
- 授權：MIT

聯絡與貢獻
=========
歡迎在原始專案發起 PR 與 Issue： https://github.com/eric861129/MD2PPT-Evolution
