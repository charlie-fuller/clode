Convert a document to markdown using the ailang docparse pipeline.

File to convert: $ARGUMENTS

Routing rules (from CLAUDE.md):
- PDF: try pdf2md MCP first (free, fast). Fall back to ailang if output is garbled, scanned, or has complex tables.
- DOCX, PPTX, XLSX, ODT, ODP, ODS, HTML, CSV, TSV, EPUB: ailang deterministic (no AI key needed)
- PNG, JPG, audio (mp3/wav/flac/aac/ogg/aiff), video (mp4/mov/avi/webm): ailang with AI model

ailang command (when needed):
  ailang run --entry main --caps IO,FS,Env,AI --ai gemini-2.5-flash docparse/main.ail <file>

AI model options: gemini-2.5-flash (needs GOOGLE_API_KEY, recommended) or claude-haiku-4-5 (needs ANTHROPIC_API_KEY)

Output goes to docparse/data/ by default.

If no file path was provided in $ARGUMENTS, ask the user for the file path before proceeding.
