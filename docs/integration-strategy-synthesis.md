# Precept Systems Integration Strategy Synthesis

**Author:** Synthesis Agent (Claude Opus 4.6)
**Date:** 2026-02-07
**Inputs:** 4 research reports (Google Workspace, Telegram/Signal bots, MCP server ecosystem, mobile field sync) + template strategy synthesis
**Purpose:** Decisive integration strategy connecting Claude Code, Google Workspace, mobile messaging, and field data capture into a unified system for Precept Systems

---

## 1. MCP Server Stack

**Decision: 3 servers now, 2 more later.**

All MCP servers use stdio transport -- they are spawned as child processes by Claude Code on demand. No always-on daemons required.

> **Note:** Fetch MCP server was removed -- Claude Code has a built-in `WebFetch` tool that provides the same functionality without consuming MCP context tokens.

### Must-Have (Install This Week)

| # | Server | Repo | What It Provides | Priority |
|---|--------|------|------------------|----------|
| 1 | **Google Workspace** | `taylorwilsdon/google_workspace_mcp` | Gmail, Calendar, Drive, Docs, Sheets, Slides -- full read/write | MUST-HAVE |
| 2 | **GitHub** | `github/github-mcp-server` | Issues, PRs, repos, code search, Projects management | MUST-HAVE |
| 3 | **Telegram** | `chigwell/telegram-mcp` | Read/send Telegram messages, manage chats, download media | MUST-HAVE |

### Nice-to-Have (Install Next Month)

| # | Server | Repo | What It Provides | Priority |
|---|--------|------|------------------|----------|
| 5 | **Git** | `mcp-server-git` | Enhanced git operations (diffs, file history, blame) | NICE-TO-HAVE |
| 6 | **WhatsApp** | `lharries/whatsapp-mcp` | Read/send WhatsApp messages (ToS risk -- personal use only) | NICE-TO-HAVE |

### Skip

| Server | Why Skip |
|--------|----------|
| Official Filesystem MCP | Redundant -- Claude Code has built-in file operations |
| Desktop Commander | Redundant -- Claude Code has built-in terminal access |
| Fetch (`server-fetch`) | Redundant -- Claude Code has built-in `WebFetch` tool |
| Signal MCP (rymurr) | Too immature (18 stars), rough edges |
| Google Official MCP (google/mcp) | Not yet mature for CLI use -- watch for GA |

### Configuration for `~/.claude.json`

```json
{
  "mcpServers": {
    "google-workspace": {
      "type": "stdio",
      "command": "uvx",
      "args": ["workspace-mcp", "--tools", "gmail", "calendar", "drive", "docs", "sheets", "slides"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "${GOOGLE_OAUTH_CLIENT_ID}",
        "GOOGLE_OAUTH_CLIENT_SECRET": "${GOOGLE_OAUTH_CLIENT_SECRET}"
      }
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "telegram": {
      "type": "stdio",
      "command": "uvx",
      "args": ["telegram-mcp"],
      "env": {
        "TELEGRAM_API_ID": "${TELEGRAM_API_ID}",
        "TELEGRAM_API_HASH": "${TELEGRAM_API_HASH}"
      }
    }
  }
}
```

**Important**: Environment variables are sourced from `~/.bashrc` or `~/.zshrc`. Never hardcode secrets in `~/.claude.json`.

---

## 2. Google Workspace Integration

### Step-by-Step OAuth Setup (One-Time, ~30 Minutes)

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create project named "Precept-AI-Tools"

2. **Enable APIs** (APIs & Services > Library)
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Google Slides API

3. **Configure OAuth Consent Screen**
   - User type: External
   - App name: "Precept AI Tools"
   - Add all required scopes (see below)
   - Add jason@precept.co.za as test user

4. **Create OAuth Client ID**
   - Type: Desktop application
   - Name: "Claude Code Integration"
   - Download `credentials.json`
   - Store at `~/.config/precept/google-credentials.json`
   - `chmod 600 ~/.config/precept/google-credentials.json`

5. **CRITICAL: Set Publishing Status to Production**
   - Without this, refresh tokens expire every 7 days
   - For apps with <100 users, Google does not require verification
   - After switching, create new OAuth credentials

6. **Export Environment Variables** (add to `~/.bashrc`)
   ```bash
   export GOOGLE_OAUTH_CLIENT_ID="your-id.apps.googleusercontent.com"
   export GOOGLE_OAUTH_CLIENT_SECRET="your-secret"
   ```

7. **First-Run Auth**
   - Start Claude Code
   - Use any Google Workspace tool (e.g., "check my inbox")
   - Browser opens for OAuth consent -- authorise once
   - Tokens cached locally, auto-refresh

### OAuth Scopes

| Service | Scope | Level |
|---------|-------|-------|
| Gmail | `gmail.modify` | Read, send, draft, label, archive |
| Calendar | `calendar` | Full read/write |
| Drive | `drive` | Full file access |
| Docs | `documents` | Read/write |
| Sheets | `spreadsheets` | Read/write |
| Slides | `presentations` | Read/write |

### Which MCP Server

**Decision: `taylorwilsdon/google_workspace_mcp`** -- it is the most comprehensive community server (1,300 stars, actively maintained, covers all 10 Google Workspace services). One server replaces what would otherwise require 6 separate tools.

### Email Correspondence Workflow

How client emails get imported into project `correspondence/` folders:

**Interactive (via Claude Code):**
```
User: "Search Gmail for all emails from andrew@fairfielddairy.co.za in January 2026
       and save each one as a dated markdown file in
       /home/jason/Projects/fairfield-water/correspondence/"

Claude: [Uses google-workspace MCP to search Gmail]
        [Reads each email's date, subject, body]
        [Writes files like 2026-01-15_email-subject.md]
        [Follows Precept naming convention: YYYY-MM-DD_channel.md]
```

**File format for imported emails:**
```markdown
# Email: [Subject Line]

**From:** andrew@fairfielddairy.co.za
**To:** jason@precept.co.za
**Date:** 2026-01-15
**Subject:** Re: Water monitoring system update

---

[Email body in markdown]
```

### Calendar Workflow

```
User: "Check my calendar for next Tuesday afternoon and book a 2-hour
       site visit with Fairfield Dairy at their location"

Claude: [Checks free/busy via MCP]
        [Creates event with title, location, attendee email]
        [Updates project STATUS.md contact log]
```

### Google Docs/Sheets/Slides in the Template System

| Google Service | How It Fits | Example |
|----------------|-------------|---------|
| **Docs** | Draft proposals and client reports, export as markdown for project docs/ | Write proposal in Docs, Claude exports to `docs/planning/client/` |
| **Sheets** | Billing tracking, equipment inventories, WiFi survey summaries | Claude reads billing sheet, updates STATUS.md financial section |
| **Slides** | Client presentations (project updates, assessment findings) | Claude creates slides from project STATUS.md and assessment docs |
| **Drive** | Central storage for large files that do not belong in git | Site visit videos, large PDFs, client-shared folders |

### Complementary CLI Tools (Outside Claude Sessions)

| Tool | Install | Purpose |
|------|---------|---------|
| `gogcli` | `go install github.com/steipete/gogcli/cmd/gog@latest` | Unified Google CLI with JSON output -- perfect for scripting |
| `gcalcli` | `pip install gcalcli` | Rich terminal calendar views |
| `himalaya` | AUR: `himalaya` or from GitHub releases | Full terminal email client |

All share the same Google Cloud OAuth credentials.

---

## 3. Mobile Messaging Bot

### Decision: Telegram. Start from claude-telegram-bridge.

### Why Telegram Over Signal

| Factor | Telegram | Signal |
|--------|----------|--------|
| Official Bot API | Yes -- mature, well-documented | No -- community tools only |
| Setup time | 2 minutes (@BotFather) | 30-60 minutes (signal-cli, phone number) |
| Photo/voice handling | Excellent native support | Basic attachment support |
| Delivery mechanism | Webhooks (instant) or polling | Polling only |
| E2E encryption (bots) | No (server-side only) | Yes |
| Rich UI (keyboards, commands) | Yes | No |
| MCP servers available | Multiple mature options | 1 immature option (18 stars) |
| Ecosystem | Massive | Tiny |

**Signal's sole advantage is E2E encryption.** For querying project status and filing photos from a self-hosted bot on your own machine, Telegram's security model is acceptable. Do not send client passwords or financial details through the bot.

### Which Project to Start From

**Decision: `claude-telegram-bridge`** (github.com/viniciustodesco/claude-telegram-bridge)

| Candidate | Verdict | Reason |
|-----------|---------|--------|
| **claude-telegram-bridge** | **USE THIS** | Has vision (photo analysis), Whisper transcription, streaming responses, and session persistence built in |
| claude-code-telegram | Good alternative | Directory navigation and session persistence, but lacks voice transcription |
| OpenClaw/Moltbot | Too heavy | 145K stars but massive complexity for a single-user bot; Jason has explored it already, keep as Phase 3 option |
| Custom bot | Not yet | Build custom only after outgrowing the existing projects |

### Core Features for v1

1. **Project context switching**: `/project fairfield-water` sets the active project
2. **AI queries with project context**: Bot loads CLAUDE.md + STATUS.md + RESUME.md, sends to Claude API with the question
3. **Photo filing**: Send photo with caption -> saved to `~/Projects/{active}/pics/YYYY-MM-DD-{caption}.jpg`
4. **Voice note transcription**: Send voice message -> Whisper transcribes -> saved to `~/Projects/{active}/correspondence/YYYY-MM-DD_voice-note.md`
5. **Status updates**: "Mark site visit as complete" -> Claude updates STATUS.md
6. **Quick file reads**: `/status` shows STATUS.md, `/resume` shows RESUME.md

### Data Flow: Phone to Project Folders

**Via Telegram Bot (primary -- per-project routing):**
```
iPhone (Telegram)               Dev Server (Bot Service, 10.0.10.21)
                                         |
+-- Send photo -----> Bot receives ----> Save to ~/Projects/{project}/pics/
|   with caption      file_id            YYYY-MM-DD-{caption}.jpg
|                                        git add + git commit
|
+-- Send voice -----> Bot receives ----> Whisper API/local transcription
|   message           OGG/OPUS file      Save .md to correspondence/
|                                        git add + git commit
|
+-- Text question --> Bot receives ----> Load project context files
|                     text message       Send to Claude API with context
|                                        Return response to Telegram
|
+-- /status --------> Bot reads -------> cat STATUS.md
                      project file       Send content to Telegram
```

**Via LocalSend (bulk transfers):**
```
iPhone (LocalSend)              Dev Server (LocalSend, 10.0.10.21:53317)
                                         |
+-- Send batch -----> LocalSend   ----> ~/incoming-photos/
    of photos         receives           Dev server script processes:
                      files via WiFi     prompt for project, rename,
                                         move to ~/Projects/{project}/pics/
                                         git add + git commit
```

### Hosting Decision

**Decision: Dev server (10.0.10.21, VM 105 "ubuntu-gen" on Proxmox "pve"), accessible via Cloudflare Tunnel.**

| Option | Verdict | Reason |
|--------|---------|--------|
| **Dev server (Proxmox VM)** | **USE THIS** | Always-on (survives desktop reboots), central hub for all services, Jason already runs Proxmox |
| Desktop + systemd | Fallback | Direct filesystem access, but tied to desktop uptime |
| VPS | Not needed | Adds cost; Jason already has equivalent infrastructure with Proxmox + Cloudflare Tunnel |

**Polling mode** eliminates the need for a public IP or webhook endpoint. The bot simply calls out to Telegram servers. Running on the dev server means the bot stays up even when the desktop is off or being rebooted.

Project files are cloned from GitHub (the source of truth) directly onto the dev server. The desktop also pulls from GitHub for Claude Code work and pushes back when done.

### Estimated Costs

| Item | Monthly Cost |
|------|-------------|
| Telegram bot | Free |
| Claude API (Sonnet, ~50-100 queries/day) | R180-540 (~$10-30) |
| Whisper API (5-10 voice messages/day, ~1 min each) | R18 (~$1) |
| Self-hosted Whisper (local, if GPU available) | Free |
| **Total** | **R200-560/month** |

---

## 4. Field Data Capture: Minimum Viable Mobile Workflow

### Photo Pipeline

**Primary: Telegram Bot (per-project routing with captions):**
```
Phone Telegram  ---> Bot receives  --->  Save directly to ---> git commit
"fairfield panel"    photo + caption     ~/Projects/fairfield-water/pics/
                                         2026-02-07-panel.jpg
```

**Bulk: LocalSend to dev server (for large batches of photos/files):**
```
CAPTURE              TRANSFER             PROCESS              FILE
iPhone camera  --->  LocalSend     --->   Dev server script -> ~/Projects/{project}/pics/
(bulk photos)        (WiFi, direct to     (prompt for           YYYY-MM-DD-description.jpg
                      dev server           project, rename)     git add + git commit
                      10.0.10.21:53317)
                      ~/incoming-photos/
```

**Current problem** (visible in `jenkins-network/pics/`): Photos arrive as UUID filenames, "WhatsApp Image" timestamps, "unnamed (1).jpg", and `IMG_4776.HEIC`. The Telegram bot solves this by requiring a caption that becomes the filename. For bulk transfers where individual captioning is impractical, LocalSend delivers files to the dev server's `~/incoming-photos/` directory for batch processing.

### Voice Notes Pipeline

```
RECORD               SYNC/SEND            TRANSCRIBE           FILE
Phone voice    --->   Telegram Bot  --->   Whisper API    ---> ~/Projects/{project}/
recorder or           (sends OGG           ($0.006/min)         correspondence/
Telegram voice        to dev server)                            YYYY-MM-DD_voice-note.md
                                                                git add + git commit
```

**Alternative for offline**: Use phone's voice recorder app. Transfer files via LocalSend to the dev server when on WiFi. Dev server script processes `.m4a`/`.ogg` files through Whisper and outputs `.md`.

**Whisper model choice**: Use OpenAI Whisper API for simplicity ($0.006/min -- at 10 minutes of voice notes per site visit, that costs R1-2 per visit). Self-hosted `whisper.cpp` on desktop is free but slower without a GPU.

### WiFi Survey Data Pipeline

```
CAPTURE              EXPORT               TRANSFER             FILE
iOS WiFi survey --->  CSV/screenshot --->  LocalSend or   ---> ~/Projects/{project}/docs/
app or laptop-        export on phone      Telegram Bot          wifi-survey-YYYY-MM-DD.csv
based survey                               (send as file)        git add + git commit
```

> **Note:** WiFiAnalyzer is Android-only. On iOS, alternatives like Network Analyzer or WiFi Sweetspots provide basic survey data. For comprehensive WiFi surveys, use a laptop-based tool and transfer results via LocalSend to the dev server.

Optional: Dev server script parses CSV into a markdown summary table for the project docs.

### On-Site Project File Access

**Decision: Cloudflare Tunnel + Termius (SSH)**

```
Phone (Termius)  ---> Cloudflare Tunnel ---> Proxmox VM/Desktop SSH
                      (already configured,
                       no subscription needed)
```

From any client site, Jason can:
- `cat ~/Projects/fairfield-water/STATUS.md` -- check project status
- `cat ~/Projects/fairfield-water/credentials.txt` -- look up credentials (if kept locally)
- `git log --oneline -5` -- see recent work
- Run `git pull` to get latest project changes

**Already in place**: Cloudflare Tunnel is configured and working (used for the Fairfield water monitoring app). Termius on iOS as SSH client.

### Offline-First Considerations

| Challenge | Solution |
|-----------|----------|
| No WiFi at client site | All capture is local-first. LocalSend transfers queue until WiFi available. |
| Expensive mobile data (R100-150/GB) | LocalSend: WiFi-only. Telegram bot: small payloads OK on mobile data. |
| Load shedding kills desktop | Proxmox servers on UPS. Bot runs in LXC container, independent of desktop. |
| HEIC photos from iPhone | Dev server ingestion script runs `heif-convert` as part of pipeline. |
| WhatsApp photos with terrible names | Route through Telegram bot instead, which enforces caption-based naming. |

### iOS App Stack

| App | Source | Purpose | Cost |
|-----|--------|---------|------|
| **Telegram** | App Store | Primary mobile interface (bot for photo filing, voice transcription, status queries) | Free |
| **LocalSend** | App Store | Bulk file/photo transfers to dev server | Free |
| **Termius** | App Store | SSH client (via Cloudflare Tunnel) | Free tier |

---

## 5. Unified Architecture

### Architecture Diagram

```
+================================================================+
|                    JASON'S LINUX DESKTOP                        |
|                    (Arch/Omarchy)                               |
|                                                                 |
|  +------------------+    +----------------------------------+   |
|  | Claude Code CLI  |    | ~/Projects/                      |   |
|  |                  |    |   (pulled from GitHub,            |   |
|  |  MCP Servers:    |    |    pushed back when done)         |   |
|  |  - Google WS     |--->|   fairfield-water/                |   |
|  |  - GitHub        |    |   jenkins-network/                |   |
|  |  - Telegram      |    |   jenny_henschel/                |   |
|  +--------+---------+    |   ...                            |   |
|           |              +------------------+---------------+   |
|  +--------+---------+                       |                   |
|  | Gemini CLI       |                       |                   |
|  | (alternative AI) |                       |                   |
|  +------------------+                       |                   |
|                                             |                   |
+=============================================|===================+
                                              |
               +==============================|===================+
               | DEV SERVER (10.0.10.21)                          |
               | VM 105 "ubuntu-gen" on Proxmox "pve"             |
               | ** CENTRAL HUB **                                |
               |                                                  |
               |  +------------------+  +---------------------+   |
               |  | Telegram Bot     |  | LocalSend           |   |
               |  | (Phase 2)        |  | (headless, systemd) |   |
               |  | - Photo filing   |  | Port 53317          |   |
               |  | - Voice transcr  |  | Receives bulk files |   |
               |  | - Status queries |  | from iPhone         |   |
               |  +--------+---------+  | ~/incoming-photos/  |   |
               |           |            +---------------------+   |
               |           |                                      |
               |  +--------+---------+                            |
               |  | ~/Projects/      |                            |
               |  | (cloned from     |                            |
               |  |  GitHub -- source|                            |
               |  |  of truth)       |                            |
               |  +------------------+                            |
               |                                                  |
               |  Cloudflare Tunnel (already configured)          |
               |  - External access to services                   |
               |  - Hosts Fairfield water monitor app             |
               +===========|======================================+
                           |
                    Telegram API
                    (polling mode)
                           |
+--------------------------+-----+  +-----------------------+
| JASON'S iPHONE                 |  | CLOUD SERVICES        |
|                                |  |                       |
| Telegram App (primary) -------+->| Telegram Servers      |
|   Per-project photo filing     |  | (free, message relay) |
|   Voice transcription          |  |                       |
|   Status queries               |  | Google Workspace APIs |
|                                |  | (Gmail, Calendar,     |
| LocalSend (bulk transfers) ---+->|  Drive, Docs, Sheets, |
|   Bulk photos/files to         |  |  Slides)              |
|   dev server                   |  |                       |
|                                |  | GitHub API            |
| Termius (SSH via CF Tunnel) ---|  | (repos, issues, PRs)  |
+---------------------------------+  |                       |
                                    | Anthropic Claude API  |
                                    | (AI responses)        |
                                    |                       |
                                    | OpenAI Whisper API    |
                                    | (voice transcription) |
                                    |                       |
                                    | Cloudflare            |
                                    | (tunnel, DNS)         |
                                    |                       |
                                    | Odoo ERP              |
                                    | (quotes, invoices)    |
                                    +-----------------------+
```

### Data Flow: Common Scenarios

#### Scenario 1: Receive Client Email, Draft Reply

```
1. Gmail receives email from client
2. Jason opens Claude Code
3. "Search inbox for emails from andrew@fairfielddairy.co.za today"
   -> Google Workspace MCP reads Gmail
4. "Save that email to fairfield-water correspondence"
   -> Claude writes ~/Projects/fairfield-water/correspondence/2026-02-07_email.md
5. "Draft a reply confirming the site visit for Tuesday"
   -> Google Workspace MCP creates Gmail draft
6. Jason reviews draft in Gmail web/app, sends
```

#### Scenario 2: Go to Site Visit

```
BEFORE (at desk):
1. "Check my calendar for tomorrow" -> MCP reads Calendar
2. "Generate a pre-visit checklist for fairfield-water" -> Claude reads project files, generates HTML checklist
3. Print checklist, pack equipment

ON-SITE (phone):
4. Take photos via Telegram bot: send with caption "fairfield panel-room"
   -> Bot saves to ~/Projects/fairfield-water/pics/2026-02-07-panel-room.jpg
5. Record voice note via Telegram: "Found three access points, two on channel 6..."
   -> Bot transcribes via Whisper, saves to correspondence/
6. Quick status check via Telegram: /status
   -> Bot returns STATUS.md content
7. Need credentials: SSH via Termius+Cloudflare Tunnel, cat credentials file

AFTER (at desk):
8. "Update fairfield-water STATUS.md: site visit completed, three APs found, channel conflict on 6"
9. /project:wrap-up -> updates RESUME.md, commits, pushes
```

#### Scenario 3: Update Project Status from Phone

```
1. Open Telegram, message Precept Bot
2. "/project fairfield-water"
3. "Mark the site assessment as complete. Next step: write proposal."
   -> Bot sends to Claude API with STATUS.md context
   -> Claude updates STATUS.md task tables
   -> git commit + push
4. Bot confirms: "Updated STATUS.md. Site assessment moved to Completed. Next action: write proposal."
```

### What Runs Where

| Component | Runs On | Always On? | Network Requirement |
|-----------|---------|------------|---------------------|
| Claude Code + MCP servers | Desktop | No -- on-demand | Internet (for API calls) |
| Gemini CLI | Desktop | No -- on-demand | Internet |
| Telegram Bot | Dev server (10.0.10.21) | Yes (always-on) | Internet (polling) |
| LocalSend | Dev server (10.0.10.21) | Yes (systemd service, port 53317) | WiFi (receives from iPhone) |
| Cloudflare Tunnel | Dev server | Yes (always-on) | Internet |
| Git/GitHub | Desktop + Dev server | No -- on-demand | Internet (for push/pull) |
| Google Workspace APIs | Google Cloud | Always | Internet |
| Anthropic Claude API | Anthropic Cloud | Always | Internet |
| Whisper API | OpenAI Cloud | Always | Internet |

---

## 6. Implementation Roadmap

### Phase 1: This Week (Days 1-3) -- Foundation

| Day | Task | Time | Cost |
|-----|------|------|------|
| 1 | Create Google Cloud project, enable 6 APIs, configure OAuth, create credentials | 30 min | Free |
| 1 | Set OAuth app to Production status, export env vars to `~/.bashrc` | 10 min | Free |
| 1 | Install `uvx` (`pip install uv`) and add google-workspace MCP to `~/.claude.json` | 15 min | Free |
| 1 | First-run OAuth authentication (browser popup) | 5 min | Free |
| 1 | Test: read inbox, check calendar, list Drive files from Claude Code | 15 min | Free |
| 2 | Configure Cloudflare Tunnel for SSH access (if not already routing to dev server) | 15 min | Free |
| 2 | Install Termius on iPhone (App Store), test SSH via Cloudflare Tunnel | 10 min | Free |
| 2 | Set up LocalSend on dev server (headless, systemd service on 10.0.10.21:53317) | 15 min | Free |
| 2 | Verify LocalSend on iPhone and desktop can send to dev server | 10 min | Free |
| 2 | Create Telegram bot via @BotFather, note token | 5 min | Free |
| 2 | Get Telegram API credentials from my.telegram.org, add Telegram MCP to `~/.claude.json` | 10 min | Free |
| 3 | Install `gogcli` on desktop as CLI complement | 15 min | Free |

**Phase 1 Total Cost: R0**
**Phase 1 Total Time: ~3 hours spread across 3 days**

### Phase 2: Next 2 Weeks -- Semi-Automated Workflows

| Task | Time | Cost |
|------|------|------|
| Clone `claude-telegram-bridge`, configure with bot token + Claude API key + whitelisted user ID | 1 hour | Free |
| Add custom handlers: photo filing with project routing, voice transcription | 3 hours | Free |
| Deploy bot to dev server (10.0.10.21) with systemd auto-restart | 30 min | Free |
| Create dev server script: process `~/incoming-photos/` from LocalSend (prompt for project, rename, move, commit) | 2 hours | Free |
| Test full workflow: send photo from iPhone via Telegram bot, verify it lands in correct project folder | 30 min | Free |
| Test bulk workflow: send batch of photos via LocalSend, verify they arrive in `~/incoming-photos/` on dev server | 15 min | Free |
| Add `/project:import-email` slash command to templates (see Section 8) | 30 min | Free |
| Install `gitwatch` for auto-committing incoming files | 30 min | Free |

**Phase 2 Total Cost: Claude API usage starts (~R200-400/month)**
**Phase 2 Total Time: ~8 hours spread across 2 weeks**

### Phase 3: Next Month -- Full Integration

| Task | Time | Cost |
|------|------|------|
| Deploy n8n via Docker for automated email-to-markdown workflows | 2 hours | Free |
| Create n8n workflow: Gmail trigger -> markdown conversion -> save to project folder | 2 hours | Free |
| Add WhatsApp MCP server (personal use only, ToS risk acknowledged) | 1 hour | Free |
| Set up self-hosted Whisper (`whisper.cpp`) on desktop if GPU available | 1 hour | Free |
| Build full photo ingestion pipeline with inotifywait (auto-rename, HEIC convert, commit) | 3 hours | Free |
| Evaluate OpenClaw/Moltbot as enhanced bot platform (already on Proxmox) | 4 hours | Free |
| Create `precept-init` integration: new projects auto-configure MCP and bot routing | 2 hours | Free |

**Phase 3 Total Cost: Same API costs + optional VPS if needed (~R70-180/month)**
**Phase 3 Total Time: ~15 hours spread across a month**

### Cost Summary

| Phase | One-Time | Monthly Recurring |
|-------|----------|-------------------|
| Phase 1 | R0 | R0 |
| Phase 2 | R0 | R200-540 (Claude API + Whisper API) |
| Phase 3 | R0 | R200-720 (same + optional VPS/n8n hosting) |

---

## 7. Security

### Credential Management Strategy

| Credential | Storage Location | Protection |
|------------|-----------------|------------|
| Google OAuth Client ID/Secret | `~/.bashrc` as env vars | File permissions (`chmod 600`) |
| Google OAuth refresh tokens | `~/.config/workspace-mcp/` (auto-managed) | Directory permissions (`chmod 700`) |
| Telegram Bot Token | `~/.config/precept/bot.env` | `chmod 600`, gitignored |
| Telegram API ID/Hash | `~/.bashrc` as env vars | File permissions |
| Claude API Key | `~/.bashrc` as env var (`ANTHROPIC_API_KEY`) | File permissions |
| GitHub PAT | `~/.bashrc` as env var (`GITHUB_TOKEN`) | File permissions |
| OpenAI API Key (Whisper) | `~/.config/precept/bot.env` | `chmod 600`, gitignored |

### Security Rules

1. **Never commit secrets to git.** Global `.gitignore` includes: `credentials.json`, `client_secret*.json`, `token.json`, `.env`, `*.env`, `bot.env`
2. **Telegram bot whitelist.** Only Jason's Telegram user ID is allowed. All other messages are silently dropped.
3. **No sensitive data through Telegram.** Bot conversations are NOT end-to-end encrypted. Do not send client passwords, financial details, or PII through the bot.
4. **File permissions on credential files.** All files containing secrets have `chmod 600` (owner read/write only). Directories have `chmod 700`.
5. **Google OAuth scopes are auditable.** Review at https://myaccount.google.com/permissions periodically.
6. **MCP environment variable isolation.** Each MCP server process gets its own environment. Servers cannot see each other's credentials.
7. **Use GNOME Keyring where supported.** `gogcli` and `himalaya` store credentials in the system keyring (encrypted at rest using login password). Prefer this over plaintext files.
8. **Claude Code `.env` loading.** Claude Code may auto-load `.env` files in project directories. Add deny rules in `.claude/settings.local.json` to block access to `.env` files if they contain sensitive data.
9. **Token rotation.** Google OAuth tokens auto-refresh (when app is set to Production). Telegram Bot tokens and API keys are long-lived -- rotate annually or if compromised.

### Sensitive Files Directory Structure

```
~/.config/precept/                     # chmod 700
    google-credentials.json            # chmod 600 (OAuth client secret)
    bot.env                            # chmod 600 (bot tokens, API keys)
```

---

## 8. Template System Integration

### Changes Required to the Template System

The template strategy synthesis (from `/home/jason/Projects/template-strategy-synthesis.md`) defines a 4-template system (base + client-ict + client-project + internal). The following additions support the integrations described in this document.

### New Slash Commands

Add to `precept-assets/templates/base/.claude/commands/`:

| Command | File | Purpose |
|---------|------|---------|
| `/project:import-email` | `import-email.md` | Search Gmail for emails from the client (using project.yml client email), save as dated markdown in correspondence/ |
| `/project:site-visit-prep` | `site-visit-prep.md` | Generate pre-visit checklist: read STATUS.md for pending tasks, check calendar for appointment time, list equipment needed |
| `/project:file-photo` | `file-photo.md` | Process photos in the incoming staging area: prompt for descriptions, rename with date prefix, move to pics/, commit |

### New `.claude/commands/import-email.md`

```
Import email correspondence from Gmail:

1. Read project.yml to get client email address and project slug
2. Use the Google Workspace MCP server to search Gmail for messages
   from/to the client email address
3. For each email not already in correspondence/:
   - Extract date, subject, from, to, body
   - Create a markdown file: correspondence/YYYY-MM-DD_email.md
   - Format with frontmatter: date, from, to, subject
4. Stage and commit the new correspondence files
5. Report how many emails were imported
```

### New `.claude/commands/site-visit-prep.md`

```
Generate a pre-visit checklist for the upcoming site visit:

1. Read STATUS.md for current tasks and pending items
2. Read RESUME.md for current context
3. Check Google Calendar (via MCP) for the next scheduled appointment
   with this client
4. Generate a pre-visit checklist HTML document (using Precept working
   branding tier) that includes:
   - Client name, address, phone (from project.yml)
   - Appointment date/time
   - Pending tasks to address on-site
   - Equipment to bring
   - Questions to ask
   - Photo checklist (what to photograph)
5. Save to docs/site-visits/YYYY-MM-DD-pre-visit-checklist.html
6. Report the file location so Jason can print it
```

### Changes to `project.yml` Schema

Add integration metadata:

```yaml
# project.yml additions for integration support
integration:
  telegram_project_alias: "fairfield"    # Short name for /project command in bot
  gmail_search_query: "from:andrew@fairfielddairy.co.za OR to:andrew@fairfielddairy.co.za"
  calendar_keyword: "Fairfield"          # Keyword to match calendar events
```

### Changes to `AGENTS.md` Template

Add a section about available integrations:

```markdown
## Available Integrations

This project has MCP server access to:
- **Google Workspace**: Gmail, Calendar, Drive, Docs, Sheets, Slides
- **GitHub**: Issues, PRs, repository management
- **Telegram**: Read/send messages (via bot or MCP)

Use `/project:import-email` to pull recent client correspondence from Gmail.
Use `/project:site-visit-prep` to generate a pre-visit checklist.
```

### Changes to `.claude/rules/precept-conventions.md`

Add integration conventions:

```markdown
## Integration Conventions

### Email Import Format
Imported emails are saved to correspondence/ as:
- Filename: YYYY-MM-DD_email.md (or YYYY-MM-DD_email-subject-slug.md if multiple emails on same day)
- Content: Markdown with date, from, to, subject header, then body

### Photo Filing Convention
Photos received via Telegram bot or LocalSend are filed as:
- Path: pics/YYYY-MM-DD-description.ext
- Description comes from Telegram caption or manual entry during batch processing
- HEIC files are converted to JPEG during ingestion

### Voice Note Convention
Transcribed voice notes are saved as:
- Path: correspondence/YYYY-MM-DD_voice-note.md
- Content: Raw transcription with timestamp header
- Original audio archived in correspondence/audio/ (gitignored for repo size)
```

### Changes to `.gitignore` (Unified)

Add to the base template `.gitignore`:

```gitignore
# Audio files (transcribed, originals not needed in git)
correspondence/audio/
*.m4a
*.ogg
*.opus
```

### Directory Structure Additions (client-project template only)

```
project-root/
    correspondence/
        audio/                         # Voice note originals (gitignored)
    pics/
        originals/                     # HEIC/RAW originals (optional, gitignored if large)
```

### Summary of Template Changes

| File/Location | Change Type | Description |
|---------------|-------------|-------------|
| `.claude/commands/import-email.md` | NEW | Gmail import slash command |
| `.claude/commands/site-visit-prep.md` | NEW | Pre-visit checklist generator |
| `.claude/commands/file-photo.md` | NEW | Photo processing slash command |
| `project.yml` schema | EXTEND | Add `integration:` section |
| `AGENTS.md` template | EXTEND | Add integrations section |
| `.claude/rules/precept-conventions.md` | EXTEND | Add integration conventions |
| `.gitignore` | EXTEND | Add audio files |
| `correspondence/audio/` | NEW (client-project) | Voice note originals directory |

---

## 9. Decision Log

| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| taylorwilsdon/google_workspace_mcp as Google MCP | ngs/google-mcp-server, Google official, MarkusPfundstein/mcp-gsuite, Composio | Most comprehensive (10 services), 1,300 stars, active development, Python/uvx fits the ecosystem |
| Telegram over Signal for bot | Signal via signal-cli | Telegram: official Bot API, 2-minute setup, rich media handling, massive ecosystem. Signal: no official bot API, immature tooling. |
| claude-telegram-bridge as starting point | claude-code-telegram, OpenClaw, custom build | Built-in vision + Whisper transcription + streaming. claude-code-telegram is a good fallback. OpenClaw is overkill for v1. |
| Dev server as central hub | Desktop systemd, VPS, Raspberry Pi | Always-on (survives desktop reboots), runs Telegram bot + LocalSend + project clones, Jason already runs Proxmox, no additional cost. |
| LocalSend for bulk phone transfers | Syncthing, AirDrop, Google Drive, manual USB | Direct WiFi transfer to dev server, no cloud, free, works with iOS. No Syncthing needed -- git handles project sync, scp for ad-hoc. |
| Cloudflare Tunnel for remote access | Tailscale, WireGuard (manual), SSH port forwarding, ngrok | Already configured and working (hosts Fairfield water monitoring app), no subscription needed, no additional setup. |
| Whisper API over self-hosted | Self-hosted whisper.cpp, on-device NotelyVoice, Google Speech-to-Text | API is simplest to start (R1-2 per site visit). Self-hosted added in Phase 3 if cost or privacy becomes a concern. |
| 3 MCP servers initially | More servers, fewer servers | Sweet spot: Google Workspace + GitHub + Telegram cover 90% of use cases. Fetch, Filesystem, and Desktop Commander are redundant with Claude Code built-ins. |
| No n8n in Phase 1 | n8n from day one | n8n adds Docker infrastructure overhead. MCP server handles interactive Google Workspace use. n8n reserved for Phase 3 automated workflows. |
| Environment variables for secrets | .env files, secrets manager, hardcoded | Simplest for solo operator. ~/.bashrc is chmod 600. GNOME Keyring used where tools support it. |

---

## Appendix A: Quick Reference -- What to Install

### Desktop (Arch Linux)

```bash
# MCP dependencies
pip install uv                          # For uvx (runs Python MCP servers)
# Node.js already installed (for npx)

# CLI tools
go install github.com/steipete/gogcli/cmd/gog@latest   # Google CLI
pip install gcalcli                     # Calendar CLI
# himalaya: install from AUR or GitHub releases

# Automation
sudo pacman -S inotify-tools            # For gitwatch/file watchers
pip install gitwatch                    # Auto-commit on file changes

# Remote access -- Cloudflare Tunnel already configured
# No additional VPN software needed
```

### Phone (iPhone)

| App | Install From | Purpose |
|-----|-------------|---------|
| Telegram | App Store | Primary mobile interface (bot for photo filing, voice transcription, status queries) |
| LocalSend | App Store | Bulk file/photo transfers to dev server |
| Termius | App Store | SSH client (via Cloudflare Tunnel) |

### Environment Variables (~/.bashrc)

```bash
# Google OAuth (for MCP + CLI tools)
export GOOGLE_OAUTH_CLIENT_ID="your-id.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="your-secret"

# Telegram (for MCP server)
export TELEGRAM_API_ID="your-api-id"
export TELEGRAM_API_HASH="your-api-hash"

# GitHub
export GITHUB_TOKEN="ghp_your-personal-access-token"

# Claude (already set if using Claude Code)
# export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI (for Whisper API)
export OPENAI_API_KEY="sk-..."
```

---

## Appendix B: File Locations Reference

| Purpose | Path | Permissions |
|---------|------|------------|
| Claude Code MCP config | `~/.claude.json` | 600 |
| Google OAuth credentials | `~/.config/precept/google-credentials.json` | 600 |
| Bot environment file | `~/.config/precept/bot.env` | 600 |
| Precept config directory | `~/.config/precept/` | 700 |
| Google Workspace MCP tokens | `~/.config/workspace-mcp/` (auto-created) | 700 |
| gcalcli OAuth token | `~/.local/share/gcalcli/oauth` | 600 |
| gogcli credentials | System keyring (GNOME Keyring) | Encrypted |
| Telegram bot code | Dev server (10.0.10.21) | Deployed via git clone |
| LocalSend config | Dev server systemd service | 700 |
| Field capture staging | `~/incoming-photos/` on dev server (LocalSend target) | Normal |
