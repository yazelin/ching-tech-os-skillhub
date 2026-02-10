# MD2DOC-Evolution (md2doc)

**Tags:** ["document", "word", "markdown", "conversion"]

簡介

MD2DOC-Evolution 是一個將 Markdown 轉換為 Word (DOCX) 的工具，主要以 Web 前端應用實作，適合技術書籍作者與內容創作者使用。此 skill 封裝說明提供使用、建置與部署的快速指南，並標示專案的 entrypoint 與主要相依套件。

Repository

- GitHub: https://github.com/yazelin/MD2DOC-Evolution
- 版本: 1.3.0 (package.json)
- Entry point: Web app — src/index.tsx / App.tsx (前端入口)

主要相依項目

- docx (docx generation)
- marked (markdown parser)
- mermaid (diagram rendering)
- qrcode (QR code generation)
- react / react-dom

快速安裝與執行 (開發)

1. Clone the repo

```bash
git clone https://github.com/yazelin/MD2DOC-Evolution.git
cd MD2DOC-Evolution
```

2. Install

```bash
npm install
```

3. Run dev server

```bash
npm run dev
# open http://localhost:5173
```

打包與產出

```bash
npm run build
# serve build output or deploy static site
```

How to use (使用說明)

1. 在編輯器中撰寫或貼上 Markdown。
2. 使用右側預覽檢視排版效果。
3. 點選匯出/Download 按鈕（或 UI 上的 "Export"）將文件匯出為 .docx 檔案。

Remarks

- 此專案主要為前端 Web 應用，若需 CLI 或 server-side 的無頭匯出，需另行客製。
- 若要整合至 CTOS SkillHub，建議直接使用封裝的 ZIP 套件或透過 GitHub release 進行發佈。
