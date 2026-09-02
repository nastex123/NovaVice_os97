const fs = require('fs');
const path = require('path');
const { execFileSync, execSync } = require('child_process');

const BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe";

if (!fs.existsSync(BRAVE_PATH)) {
    console.error("Error: Brave browser executable not found at " + BRAVE_PATH);
    process.exit(1);
}

// List of markdown files to convert, excluding 03_PROTOTIPO_SOLUCION_SOFTWARE.md
const FILES_TO_CONVERT = [
    path.join(__dirname, '..', 'SENA', 'README.md'),
    path.join(__dirname, '..', 'SENA', 'part1', '00_GUIA_ENTREGA_PARTE_1.md'),
    path.join(__dirname, '..', 'SENA', 'part1', '01_DOCUMENTO_DISENO_SOFTWARE.md'),
    path.join(__dirname, '..', 'SENA', 'part1', '02_DIAGRAMAS_UML.md'),
    // Note: part1/03_PROTOTIPO_SOLUCION_SOFTWARE.md is SKIPPED by user request
    path.join(__dirname, '..', 'SENA', 'part1', '04_MODELO_BASE_DATOS.md'),
    path.join(__dirname, '..', 'SENA', 'part2', '00_GUIA_ENTREGA_PARTE_2.md'),
    path.join(__dirname, '..', 'SENA', 'part2', '01_DOCUMENTO_TECNICO_CODIGO_FUENTE.md'),
    path.join(__dirname, '..', 'SENA', 'part2', '02_INSTRUCTIVO_USO_SOLUCION_SOFTWARE.md'),
    path.join(__dirname, '..', 'SENA', 'part2', '03_ENTREGA_SOLUCION_SOFTWARE.md')
];

function buildHtml(markdownContent, title) {
    const base64Md = Buffer.from(markdownContent, 'utf8').toString('base64');
    return `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <!-- KaTeX for math formulas -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <!-- Mermaid for diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <!-- Marked for markdown parsing -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    @page {
      size: letter;
      margin: 18mm 16mm;
      @bottom-right {
        content: counter(page);
      }
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.5;
      color: #1e293b;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }
    h1 {
      font-size: 19pt;
      color: #0f172a;
      border-bottom: 2.5px solid #2563eb;
      padding-bottom: 6px;
      margin-top: 0;
      margin-bottom: 12px;
    }
    h2 {
      font-size: 13.5pt;
      color: #1e3a8a;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      margin-top: 18px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }
    h3 {
      font-size: 11.5pt;
      color: #1d4ed8;
      margin-top: 14px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }
    h4 {
      font-size: 10.5pt;
      color: #334155;
      margin-top: 10px;
      margin-bottom: 4px;
      page-break-after: avoid;
    }
    p, ul, ol {
      margin-top: 0;
      margin-bottom: 8px;
    }
    li {
      margin-bottom: 3px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
      font-size: 9pt;
      page-break-inside: avoid;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 5px 8px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background-color: #f1f5f9;
      color: #0f172a;
      font-weight: 600;
    }
    tr:nth-child(even) td {
      background-color: #f8fafc;
    }
    pre {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 8px 10px;
      font-family: "Consolas", "Courier New", monospace;
      font-size: 8.5pt;
      line-height: 1.35;
      overflow-x: auto;
      page-break-inside: avoid;
    }
    code {
      font-family: "Consolas", "Courier New", monospace;
      font-size: 8.5pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
      color: #0f172a;
    }
    pre code {
      background: none;
      padding: 0;
      color: inherit;
    }
    blockquote {
      border-left: 3.5px solid #2563eb;
      margin: 10px 0;
      padding: 6px 12px;
      background: #eff6ff;
      color: #1e40af;
      border-radius: 0 5px 5px 0;
      page-break-inside: avoid;
    }
    hr {
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 16px 0;
    }
    .mermaid {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 12px;
      margin: 14px 0;
      text-align: center;
      page-break-inside: avoid;
    }
    .mermaid svg {
      max-width: 100% !important;
      height: auto !important;
    }
  </style>
</head>
<body>
<div id="content"></div>
<script>
  function decodeBase64Utf8(b64) {
    const binStr = atob(b64);
    const bytes = new Uint8Array(binStr.length);
    for (let i = 0; i < binStr.length; i++) {
      bytes[i] = binStr.charCodeAt(i);
    }
    return new TextDecoder('utf-8').decode(bytes);
  }

  const rawMarkdown = decodeBase64Utf8("${base64Md}");
  
  // Custom marked options
  marked.setOptions({
    gfm: true,
    breaks: false
  });

  document.getElementById('content').innerHTML = marked.parse(rawMarkdown);

  // Convert mermaid code blocks
  document.querySelectorAll('pre code.language-mermaid').forEach((codeBlock) => {
    const pre = codeBlock.parentElement;
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = codeBlock.textContent;
    pre.replaceWith(div);
  });

  // Render Mermaid diagrams
  mermaid.initialize({
    startOnLoad: false,
    theme: 'neutral',
    securityLevel: 'loose',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  });
  mermaid.run();

  // Render math
  renderMathInElement(document.body, {
    delimiters: [
      {left: '$$', right: '$$', display: true},
      {left: '$', right: '$', display: false},
      {left: '\\\\(', right: '\\\\)', display: false},
      {left: '\\\\[', right: '\\\\]', display: true}
    ],
    throwOnError: false
  });
</script>
</body>
</html>`;
}

async function convertAll() {
    console.log("=== INICIANDO CONVERSIÓN DE DOCUMENTOS SENA A PDF ===");
    console.log("Excluyendo: part1/03_PROTOTIPO_SOLUCION_SOFTWARE.md (solicitud del usuario)\n");

    const tempDir = path.join(__dirname, '..', 'tmp_pdf_build');
    if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
    }

    for (let i = 0; i < FILES_TO_CONVERT.length; i++) {
        const mdPath = FILES_TO_CONVERT[i];
        if (!fs.existsSync(mdPath)) {
            console.warn(`[!] Archivo no encontrado: ${mdPath}`);
            continue;
        }

        const baseName = path.basename(mdPath, '.md');
        const dirName = path.dirname(mdPath);
        const outPdfPath = path.join(dirName, `${baseName}.pdf`);
        const tempHtmlPath = path.join(tempDir, `${baseName}.html`);

        console.log(`[${i + 1}/${FILES_TO_CONVERT.length}] Procesando: ${path.relative(path.join(__dirname, '..'), mdPath)}`);

        const mdContent = fs.readFileSync(mdPath, 'utf8');
        const title = baseName.replace(/_/g, ' ');
        const html = buildHtml(mdContent, title);

        fs.writeFileSync(tempHtmlPath, html, 'utf8');

        const htmlUri = `file:///${tempHtmlPath.replace(/\\/g, '/')}`;
        const pdfPathArg = `--print-to-pdf=${outPdfPath}`;

        const args = [
            '--headless=new',
            '--disable-gpu',
            '--no-sandbox',
            '--no-pdf-header-footer',
            '--virtual-time-budget=6000',
            pdfPathArg,
            htmlUri
        ];

        try {
            execFileSync(BRAVE_PATH, args, { stdio: 'pipe', timeout: 30000 });
            if (fs.existsSync(outPdfPath)) {
                const stats = fs.statSync(outPdfPath);
                console.log(`    -> Creado exitosamente: ${path.basename(outPdfPath)} (${(stats.size / 1024).toFixed(1)} KB)`);
            } else {
                console.error(`    -> Error: No se generó el PDF para ${baseName}`);
            }
        } catch (err) {
            console.error(`    -> Error al compilar PDF para ${baseName}:`, err.message);
        }
    }

    // Clean up temporary HTML build folder
    try {
        fs.rmSync(tempDir, { recursive: true, force: true });
    } catch (e) {}

    console.log("\n=== CONVERSIÓN FINALIZADA EXITOSAMENTE ===");
}

convertAll();
