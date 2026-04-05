# Work Laptop Setup — Pending Tasks

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
