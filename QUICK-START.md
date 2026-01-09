# Clode Quick Start Guide

## 🎉 Your Other Machine Setup

On your second laptop, follow these steps:

### 1. Clone the Repository

```bash
cd ~/Documents/GitHub
git clone https://github.com/motorthings/clode.git
cd clode
```

### 2. Run Interactive Installation

```bash
./scripts/install.sh
```

This will:
- Show you **all available** agents, commands, skills, and hooks
- Let you **choose which ones** to install
- Ask whether to install **globally** or **per-project**
- Track what you've installed in `~/.clode-config.json`

### 3. Add Your API Keys

The installer will create template configs with placeholders. Add your actual keys:

```bash
# Edit your MCP configs
nano ~/.claude.json  # Add keys for global MCP servers
```

See `mcp-configs/SECRETS.md` for where to get each key.

### 4. You're Done!

Test it out:
```bash
claude
# Try: /danger, /think, /help, etc.
```

## 📥 Syncing Updates

### When Machine 1 Adds Something New

**On Machine 1:**
```bash
cd ~/Documents/GitHub/clode
./scripts/sync.sh push
git add .
git commit -m "Add new awesome-agent"
git push
```

**On Machine 2:**
```bash
cd ~/Documents/GitHub/clode
./scripts/sync.sh pull
```

This will:
- Pull latest from GitHub
- **Alert you** to new agents/commands
- Ask if you want to install them
- Let you choose global vs project installation

### When You Want to See What's Available

```bash
cd ~/Documents/GitHub/clode
./scripts/sync.sh diff
```

Shows:
- ✓ Items you have installed
- - Items available but not installed

## 🎯 Different Configs Per Machine

Each machine can have **different** selections! The `~/.clode-config.json` file tracks what **this specific machine** has installed.

### Example Workflow

**Machine 1** (your main laptop):
- Install ALL agents and commands
- Use for heavy development work

**Machine 2** (your travel laptop):
- Install only essential agents (`thinking-partner`, `daily-summarizer`)
- Install only frequently-used commands (`/danger`, `/help`)
- Lighter, faster setup

Both pull from the same repo, but choose different items!

## 🔄 Two-Way Sync

### Push Local Changes to Repo

Created a great new agent on Machine 1?

```bash
# Machine 1
cd ~/Documents/GitHub/clode
./scripts/sync.sh push

# It will find new local items and ask:
# - Should this be in the repo?
# - Is it a global or project item?

git add .
git commit -m "Add new deployment-helper agent"
git push
```

### Pull on Machine 2

```bash
# Machine 2
cd ~/Documents/GitHub/clode
./scripts/sync.sh pull

# Output:
# NEW Agent: deployment-helper - Helps with deployments
# Install this new agent? (y/n): y
# Install location:
#   1) Global (~/.claude/agents)
#   2) Current project
# Choice (1/2): 1
# ✓ Installed deployment-helper
```

## 📦 What You Have Now

### Global Configurations
- **1 global command**: `gigawatt` (Gigawatt prompt engineer)
- **3 global hooks**: Context preservation and injection
- **Global settings**: Bypass permissions mode

### Project Templates (33 commands!)
- **6 custom agents**: thinking-partner, daily-summarizer, interviewer, research-assistant, chat-archiver
- **33 slash commands**: danger, repo, obsidian, elevenlabs, transcribe, and many more
- **1 skill**: folder-organization-skill

### MCP Server Configs
- **Global**: n8n-mcp, elevenlabs, mem0, cloner-mcp, neo4j-thesis
- **Project-specific**: perplexity, railway, supabase, github, vercel, serena

## 🚀 Common Commands

```bash
# See what's installed vs available
./scripts/sync.sh diff

# Pull updates and install new items
./scripts/sync.sh pull

# Push your local changes
./scripts/sync.sh push

# Re-run installation (non-destructive)
./scripts/install.sh
```

## 💡 Pro Tips

### 1. Machine-Specific Preferences

Edit `~/.clode-config.json` to see what's installed:
```bash
cat ~/.clode-config.json | jq
```

### 2. Selective Installation

During `install.sh` or `sync.sh pull`:
- Press `n` to skip items you don't need
- Choose global for items you want everywhere
- Choose project for project-specific items

### 3. One Machine for Experiments

Use one machine to try new agents/commands, then push winners to the repo for the other machine.

### 4. Project-Specific Configs

Each project can have its own `.claude/` directory (see `PROJECT-SPECIFIC-GUIDE.md`):
- Commit `.claude/` to each project repo
- Team members get the same commands
- Use clode for **your personal** customizations

## 🔐 Security Notes

- API keys are **NOT** in the repo (see `.gitignore`)
- Template configs have placeholders like `YOUR_API_KEY_HERE`
- Each machine needs its own keys added manually
- The repo is **public** by default - don't commit secrets!

## 🆘 Troubleshooting

### Script won't run
```bash
chmod +x scripts/*.sh
```

### Git conflicts
```bash
git pull --rebase
```

### Lost track of what's installed
```bash
cat ~/.clode-config.json
```

### Want to start fresh
```bash
rm ~/.clode-config.json
./scripts/install.sh  # Will recreate
```

## 📚 Further Reading

- `README.md` - Full documentation
- `PROJECT-SPECIFIC-GUIDE.md` - Managing project configs
- `mcp-configs/SECRETS.md` - API key setup
- `scripts/sync.sh help` - Sync command help

---

**Next Steps:**
1. Set up Machine 2 using the steps above
2. Test syncing by adding a new command on Machine 1
3. Pull it on Machine 2 and see the magic! ✨
