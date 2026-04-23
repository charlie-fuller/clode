# Work Laptop Setup — Pending Tasks

## Token Efficiency Overhaul (added 2026-04-23)

Changes made on charlie.fuller laptop to reduce Claude Code token usage. All files are in clode.

### What changed

**1. Statusline** — shows model name + context % progress bar at bottom of Claude Code.

```bash
cp global/statusline-command.sh ~/.claude/statusline-command.sh
chmod +x ~/.claude/statusline-command.sh
```

Already wired in `global/settings.json` via `statusLine` config.

**2. New slash commands:**
- `/caveman` — strips filler from responses (~65% fewer output tokens). Run at session start.
- `/convert <path>` — converts docs to markdown via ailang/pdf2md before reading.

```bash
cp global/commands/caveman.md ~/.claude/commands/
cp global/commands/convert.md ~/.claude/commands/
```

**3. Auto-convert hook** — intercepts Read tool calls on document files (.docx, .pptx, .xlsx, etc.) and auto-converts to markdown. AI-requiring formats (.pdf, .png, audio, video) are blocked with instructions to run ailang manually.

Requires `ailang` installed at `/usr/local/bin/ailang` (install from ailang registry).

```bash
cp global/hooks/auto-convert-docs.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/auto-convert-docs.py
```

Already wired in `global/settings.json` via `PreToolUse` hook on `Read`.

**4. context7 MCP scoped to Glean repos only** — removed from global settings, add only in Glean repos:

```bash
# In ~/Vault/GitHub/glean-agent-factory/ and glean-agent-factory-app/
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
EOF
```

**5. Session habits** (no files, just behaviors):
- `/effort low` before extraction/formatting tasks
- `/compact` or `/clear` when context passes 35%

### Notes
- The hook script finds ailang's docparse path dynamically (handles version upgrades)
- Settings paths hardcoded to `/Users/motorthings/` — update if username differs
- GOOGLE_API_KEY must be available in env for PDF/image/audio conversion via hook

---

## Granola Enricher (added 2026-04-04)

Auto-enriches Granola meeting notes using the Stuart Winter-Tear / Unhyped decision-forcing
framework. Fires automatically via launchd when new files appear in your Granola folder.

### Steps

1. **Pull clode** — `cd ~/wherever/clode && git pull`

2. **Copy the script** to your vault's `_tools/scripts/` folder:
   ```bash
   cp project-templates/obsidian-vault/scripts/granola_enricher.py \
      ~/Documents/Vault/_tools/scripts/granola_enricher.py
   ```

3. **Add API key** to `_tools/scripts/config.py`:
   ```python
   ANTHROPIC_API_KEY = "sk-ant-..."  # get from 1Password: "Anthropic API Key — doc-conv"
   ```

4. **Set up launchd** (fires automatically when Granola syncs a new file):
   ```bash
   # Edit the plist first if your vault path or username differs from motorthings
   cp project-templates/obsidian-vault/launchd/com.motorthings.granola-enricher.plist \
      ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.motorthings.granola-enricher.plist
   ```

5. **Run backfill** to process your existing Granola/Summaries/ files:
   ```bash
   cd ~/Documents/Vault/_tools/scripts
   python3 granola_enricher.py --backfill --workers 4
   ```
   (~300 files, ~15–20 min, costs ~$3–5)

6. **Verify** enriched summaries are appearing in `Granola/Enriched/`

### Notes
- `OBSIDIAN_VAULT_PATH` env var overrides the default `~/Documents/Vault` if your vault is elsewhere
- Raw originals move to `Granola/Archive/` — never deleted
- Logs: `~/Library/Logs/granola-enricher.log`
