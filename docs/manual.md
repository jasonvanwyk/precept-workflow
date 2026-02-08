# Precept Workflow - Setup & Usage Manual

**Last Updated:** 2026-02-08

This is the practical guide for setting up and using the Precept Workflow system. For the full strategy and rationale, see `integration-strategy-synthesis.md`.

---

## Table of Contents

1. [What This System Does](#1-what-this-system-does)
2. [Architecture Overview](#2-architecture-overview)
3. [Phase 1 Setup Checklist](#3-phase-1-setup-checklist)
4. [Phase 2 Setup Checklist](#4-phase-2-setup-checklist)
5. [Daily Usage Guide](#5-daily-usage-guide)
6. [Troubleshooting](#6-troubleshooting)
7. [File Locations Reference](#7-file-locations-reference)

---

## 1. What This System Does

Precept Workflow connects your tools so you can manage ICT projects without leaving the terminal or your phone:

- **Claude Code + MCP Servers** -- Read/send email, check calendar, manage GitHub repos, and message via Telegram -- all from within a Claude Code session
- **Telegram Bot** (Phase 2) -- Primary mobile interface: send photos, voice notes, and status queries from your iPhone to the correct project folder; runs on the dev server (10.0.10.21)
- **LocalSend** -- Bulk file/photo transfers from iPhone to dev server over WiFi (no cloud)
- **Cloudflare Tunnel** -- SSH into the dev server from any client site via your phone (already configured)

### What are MCP Servers?

MCP (Model Context Protocol) servers are small programs that Claude Code launches on demand. They give Claude the ability to interact with external services. When you say "check my inbox" in Claude Code, Claude calls the Google Workspace MCP server, which talks to the Gmail API and returns your emails.

They are configured in `~/.claude.json` and run as child processes -- they start when needed and stop when Claude Code exits. No always-on daemons.

### Current MCP Stack

| Server | What It Does | Config Status |
|--------|-------------|---------------|
| **google-workspace** | Gmail, Calendar, Drive, Docs, Sheets, Slides | Working |
| **github** | Issues, PRs, repos, code search | Working |
| **telegram** | Read/send Telegram messages | Working |

> **Note:** Fetch MCP server was removed -- Claude Code has a built-in `WebFetch` tool that provides the same functionality.

---

## 2. Architecture Overview

```
DESKTOP (Arch Linux)
+------------------------------------------+
|  Claude Code                              |
|    MCP: google-workspace, github,         |
|         telegram                          |
|                                           |
|  ~/Projects/ (pulled from GitHub,         |
|    pushed back when done)                 |
+------------------------------------------+
         |              |
    Google APIs       GitHub
         |              |
+------------------------------------------+
|  DEV SERVER (10.0.10.21)                  |
|  VM 105 "ubuntu-gen" on Proxmox "pve"     |
|  ** CENTRAL HUB **                        |
|                                           |
|  Telegram Bot (Phase 2, primary mobile)   |
|  LocalSend (headless, systemd, :53317)    |
|  ~/Projects/ (cloned from GitHub)         |
|  Cloudflare Tunnel (external access)      |
+------------------------------------------+
         |              |
    Telegram API   Cloudflare Tunnel
         |              |
+------------------------------------------+
|  iPHONE                                   |
|    Telegram (primary: photo filing,       |
|      voice transcription, status queries) |
|    LocalSend (bulk file transfers)        |
|    Termius (SSH via CF Tunnel)            |
+------------------------------------------+
```

---

## 3. Phase 1 Setup Checklist

These are the manual steps Jason needs to complete. Estimated total: ~2-3 hours spread across a few days.

### 3.1 Google Workspace (MCP Server)

- [ ] **Create Google Cloud Project** (~5 min)
  1. Go to https://console.cloud.google.com/
  2. Click "New Project"
  3. Name it: `Precept-AI-Tools`
  4. Note the project ID

- [ ] **Enable APIs** (~5 min)
  1. Go to APIs & Services > Library
  2. Search and enable each:
     - Gmail API
     - Google Calendar API
     - Google Drive API
     - Google Docs API
     - Google Sheets API
     - Google Slides API

- [ ] **Configure OAuth Consent Screen** (~10 min)
  1. APIs & Services > OAuth consent screen
  2. User type: External
  3. App name: `Precept AI Tools`
  4. User support email: jason@precept.co.za
  5. Developer email: jason@precept.co.za
  6. Add scopes: `gmail.modify`, `calendar`, `drive`, `documents`, `spreadsheets`, `presentations`
  7. Add test user: jason@precept.co.za
  8. Save

- [ ] **Set to Production** (~2 min)
  1. OAuth consent screen > Publishing status
  2. Click "Publish App"
  3. Confirm (under 100 users = no Google verification needed)
  4. **Why:** Test mode tokens expire every 7 days. Production tokens auto-refresh.

- [ ] **Create OAuth Client ID** (~5 min)
  1. APIs & Services > Credentials
  2. Create Credentials > OAuth client ID
  3. Application type: Desktop application
  4. Name: `Claude Code Integration`
  5. Download the JSON
  6. Save to: `~/.config/precept/google-credentials.json`
  7. Run: `chmod 600 ~/.config/precept/google-credentials.json`

- [ ] **Export Environment Variables** (~2 min)
  Add to `~/.bashrc` (or `~/.zshrc`):
  ```bash
  export GOOGLE_OAUTH_CLIENT_ID="your-id.apps.googleusercontent.com"
  export GOOGLE_OAUTH_CLIENT_SECRET="your-secret"
  ```
  Then run: `source ~/.bashrc`

- [ ] **First-Run Authentication** (~2 min)
  1. Open a new terminal (so env vars are loaded)
  2. Start Claude Code: `claude`
  3. Type: "Check my Gmail inbox"
  4. A browser window will open for OAuth consent
  5. Authorise the app
  6. Tokens are cached automatically after this

- [ ] **Test It** (~5 min)
  Try these in Claude Code:
  - "Show my 5 most recent emails"
  - "What's on my calendar this week?"
  - "List files in my Google Drive root"

### 3.2 GitHub (MCP Server)

- [ ] **Create a Personal Access Token** (~5 min)
  1. Go to https://github.com/settings/tokens
  2. Generate new token (classic) or fine-grained
  3. Scopes needed: `repo`, `read:org`, `read:user`, `workflow`
  4. Copy the token

- [ ] **Export Environment Variable** (~1 min)
  Add to `~/.bashrc`:
  ```bash
  export GITHUB_TOKEN="ghp_your-token-here"
  ```
  Then run: `source ~/.bashrc`

- [ ] **Test It** (~2 min)
  In Claude Code:
  - "List my GitHub repos"
  - "Show open issues on precept-assets"

### 3.3 Telegram (MCP Server)

- [ ] **Get API Credentials** (~5 min)
  1. Go to https://my.telegram.org/
  2. Log in with your phone number
  3. Go to "API development tools"
  4. Create an application if you haven't already
  5. Note your `api_id` and `api_hash`

- [ ] **Create a Bot** (~5 min)
  1. Open Telegram, search for @BotFather
  2. Send `/newbot`
  3. Name: `Precept Bot`
  4. Username: `precept_systems_bot` (or similar, must be unique)
  5. Note the bot token
  6. Save the bot token to `~/.config/precept/bot.env`:
     ```
     TELEGRAM_BOT_TOKEN=your-bot-token
     ```
  7. Run: `chmod 600 ~/.config/precept/bot.env`

- [ ] **Export Environment Variables** (~1 min)
  Add to `~/.bashrc`:
  ```bash
  export TELEGRAM_API_ID="your-api-id"
  export TELEGRAM_API_HASH="your-api-hash"
  ```
  Then run: `source ~/.bashrc`

- [ ] **Add Telegram MCP to Config** (~2 min)
  Ask Claude Code to add the telegram server to `~/.claude.json`, or add manually:
  ```json
  "telegram": {
    "type": "stdio",
    "command": "uvx",
    "args": ["telegram-mcp"],
    "env": {
      "TELEGRAM_API_ID": "${TELEGRAM_API_ID}",
      "TELEGRAM_API_HASH": "${TELEGRAM_API_HASH}"
    }
  }
  ```

- [ ] **Test It** (~2 min)
  In Claude Code:
  - "List my recent Telegram chats"

### 3.4 Cloudflare Tunnel (Remote Access)

Already configured and working (used for the Fairfield water monitoring app).

- [ ] **Verify SSH route exists** (~5 min)
  Check that the Cloudflare Tunnel can route SSH traffic to the desktop or a Proxmox VM.
  If not already configured, add an SSH route in the Cloudflare Zero Trust dashboard.

- [ ] **Test It** (~2 min)
  From phone (Termius or any SSH client):
  ```
  ssh jason@<cloudflare-tunnel-hostname>
  ```

### 3.5 LocalSend (iPhone -> Dev Server Bulk Transfers)

LocalSend is already set up on the dev server (headless, systemd service on 10.0.10.21:53317) and on the iPhone and desktop.

- [ ] **Verify dev server LocalSend is running** (~2 min)
  ```bash
  ssh jason@10.0.10.21
  systemctl status localsend
  ```
- [ ] **Test transfer from iPhone** (~2 min)
  1. Open LocalSend on iPhone
  2. Select photos/files to send
  3. Dev server should appear as a target on the same WiFi network
  4. Verify files arrive in `~/incoming-photos/` on dev server

### 3.6 iPhone Apps

- [ ] Install **Telegram** (App Store) -- Primary mobile interface (bot for photo filing, voice transcription, status queries)
- [ ] Install **LocalSend** (App Store) -- Bulk file/photo transfers to dev server
- [ ] Install **Termius** (App Store) -- SSH client (via Cloudflare Tunnel)

### 3.7 Desktop CLI Tools (Optional)

These are nice-to-have CLI tools that share the same Google OAuth credentials:

- [ ] `go install github.com/steipete/gogcli/cmd/gog@latest` -- Google CLI
- [ ] `pip install gcalcli` -- Terminal calendar viewer
- [ ] Install himalaya (AUR) -- Terminal email client

---

## 4. Phase 2 Setup Checklist

After Phase 1 is working:

- [ ] Clone `claude-telegram-bridge` repo onto dev server (10.0.10.21)
- [ ] Configure with bot token + Claude API key + whitelisted user ID
- [ ] Add custom handlers: photo filing with project routing, voice transcription
- [ ] Deploy bot on dev server with systemd auto-restart
- [ ] Create dev server script: process `~/incoming-photos/` from LocalSend (rename, move to project, commit)
- [ ] Test Telegram workflow: send photo from iPhone via bot, verify it lands in correct project folder
- [ ] Test LocalSend workflow: send batch of photos from iPhone, verify they arrive in `~/incoming-photos/` on dev server
- [ ] Add new slash commands to templates (import-email, site-visit-prep, file-photo)
- [ ] Update project.yml schema with integration section

---

## 5. Daily Usage Guide

### 5.1 Using MCP Servers in Claude Code

Once set up, you just talk naturally in Claude Code. The MCP servers handle the rest.

**Email:**
```
"Search my inbox for emails from andrew@fairfielddairy.co.za this week"
"Draft a reply confirming the site visit for Tuesday"
"Save that email to fairfield-water/correspondence"
```

**Calendar:**
```
"What's on my calendar tomorrow?"
"Book a 2-hour site visit with Fairfield Dairy on Tuesday afternoon"
"Check if I'm free next Thursday morning"
```

**Drive/Docs/Sheets:**
```
"List files in my Precept folder on Google Drive"
"Create a new Google Doc titled 'Fairfield Water Assessment'"
"Read the billing spreadsheet and summarise outstanding amounts"
```

**GitHub:**
```
"Show open issues on the fairfield-water repo"
"Create a PR for the current branch"
"List my repos"
```

**Telegram:**
```
"Show my recent Telegram messages"
"Send a message to [chat] saying the site visit is confirmed"
```

### 5.2 Site Visit Workflow

**Before (at desk):**
1. `claude` in the project directory
2. "What's on my calendar tomorrow?" -- check appointment
3. "Generate a pre-visit checklist" -- or `/project:site-visit-prep`
4. Print checklist, pack equipment

**On-site (phone):**
- Take photos via Telegram bot: send with caption like "fairfield panel-room"
- Record voice note via Telegram: bot transcribes and saves to correspondence/
- Quick status check: `/status` in Telegram bot
- Need credentials: SSH via Termius + Cloudflare Tunnel, read files directly

**After (at desk):**
1. "Update STATUS.md: site visit completed, three APs found"
2. `/project:wrap-up` -- commits everything, pushes, updates RESUME.md

### 5.3 Email Import Workflow

```
"Search Gmail for all emails from andrew@fairfielddairy.co.za in January
and save each one as a dated markdown file in correspondence/"
```

Or use the slash command (once template integration is done):
```
/project:import-email
```

### 5.4 End of Session

Always run `/project:wrap-up` before closing Claude Code. This:
- Updates RESUME.md with what you did and what's next
- Updates STATUS.md task tables
- Commits and pushes to GitHub

---

## 6. Troubleshooting

### MCP Server Not Working

**Symptom:** Claude says it can't access Gmail/GitHub/Telegram.

**Check:**
1. Are environment variables set? Run: `echo $GOOGLE_OAUTH_CLIENT_ID`
2. Did you restart the terminal after adding env vars to `~/.bashrc`?
3. Is the MCP server config in `~/.claude.json`? Check with: `cat ~/.claude.json | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('mcpServers',{}), indent=2))"`
4. Is `uvx` installed? Run: `which uvx`
5. Is `npx` installed? Run: `which npx`

### Google OAuth Token Expired

**Symptom:** Google Workspace tools stop working after ~7 days.

**Fix:** Your OAuth app is probably still in "Testing" mode. Go to Google Cloud Console > OAuth consent screen > Publish App to set it to Production.

### Telegram MCP Can't Connect

**Symptom:** Telegram MCP fails to start.

**Check:**
1. Are `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` set?
2. First run may require interactive phone verification -- run `uvx telegram-mcp` manually once to complete setup.

### LocalSend Not Receiving (Dev Server)

**Check:**
1. Is the LocalSend service running? `ssh jason@10.0.10.21 systemctl status localsend`
2. Is port 53317 accessible? Check firewall rules on dev server
3. Are iPhone and dev server on the same WiFi network?

---

## 7. File Locations Reference

### Credentials & Config

| Purpose | Path | Permissions |
|---------|------|------------|
| Claude Code MCP config | `~/.claude.json` | 600 |
| Google OAuth credentials | `~/.config/precept/google-credentials.json` | 600 |
| Bot tokens & API keys | `~/.config/precept/bot.env` | 600 |
| Precept config directory | `~/.config/precept/` | 700 |
| Google Workspace MCP tokens | `~/.config/workspace-mcp/` (auto-created) | 700 |

### Environment Variables (~/.bashrc)

```bash
# Google OAuth
export GOOGLE_OAUTH_CLIENT_ID="..."
export GOOGLE_OAUTH_CLIENT_SECRET="..."

# Telegram
export TELEGRAM_API_ID="..."
export TELEGRAM_API_HASH="..."

# GitHub
export GITHUB_TOKEN="..."
```

### Project Files

| Purpose | Path |
|---------|------|
| This project | `~/Projects/precept-workflow/` |
| Template system | `~/Projects/precept-assets/` |
| All client/internal projects | `~/Projects/*/` |
| Field capture staging | `~/incoming-photos/` on dev server (LocalSend target) |

### Services

| Service | Where | How to Start | How to Check |
|---------|-------|-------------|-------------|
| LocalSend | Dev server (10.0.10.21) | `systemctl start localsend` | `systemctl status localsend` |
| Cloudflare Tunnel | Dev server (10.0.10.21) | Already running | Check Cloudflare Zero Trust dashboard |
| Telegram Bot (Phase 2) | Dev server (10.0.10.21) | systemd service | `systemctl status precept-bot` |
