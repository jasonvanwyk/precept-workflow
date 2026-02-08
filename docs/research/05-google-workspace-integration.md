---

# Integrating Claude Code with Google Workspace: A Comprehensive Research Report

**Prepared for:** Jason van Wyk, Precept Systems, South Africa
**Date:** 7 February 2026

---

## Table of Contents

1. Executive Summary
2. Google Workspace APIs and OAuth Scopes
3. MCP Servers for Google Workspace (The Primary Recommendation)
4. Standalone CLI Tools
5. Automation Platforms (n8n / Make / Zapier)
6. Google Apps Script
7. OAuth 2.0 Setup Process
8. Security Considerations
9. Practical Architecture Recommendations
10. Implementation Roadmap

---

## 1. Executive Summary

The best path for a solo Linux CLI power user running Claude Code is to use **MCP (Model Context Protocol) servers** that wrap Google Workspace APIs. The MCP ecosystem has matured significantly, and there are now production-ready servers that give Claude Code direct access to Gmail, Calendar, Drive, Docs, Sheets, and Slides through natural language. This means you can say things like "search my inbox for emails from client X this week and draft a reply" and Claude Code will execute it directly.

There are three tiers of tooling available:

- **Tier 1 (Primary): MCP Servers** -- Direct integration with Claude Code. Claude can read/write all Google Workspace services.
- **Tier 2 (Complementary): Standalone CLI tools** -- `gogcli`, `gcalcli`, `himalaya` for direct terminal use outside of Claude sessions.
- **Tier 3 (Optional): Automation platforms** -- n8n (self-hosted) for scheduled workflows like automated email-to-markdown export.

---

## 2. Google Workspace APIs and OAuth Scopes

### APIs You Need to Enable

In the Google Cloud Console, you will need to enable these APIs for your project:

| API | Purpose |
|-----|---------|
| Gmail API | Read inbox, search, draft, send emails |
| Google Calendar API | View/create/edit events, check availability |
| Google Drive API | List, search, upload, download files |
| Google Docs API | Read/write document content |
| Google Sheets API | Read/write spreadsheet cells and data |
| Google Slides API | Create/edit presentations |

### OAuth 2.0 Scopes Required

Each scope is a URI string that defines the level of access. Here are the scopes you will need, following the principle of least privilege:

**Gmail:**
- `https://www.googleapis.com/auth/gmail.modify` -- Read, send, delete, and manage email (covers reading inbox, drafting, sending, labelling)
- `https://www.googleapis.com/auth/gmail.send` -- If you only want send capability (narrower)
- `https://www.googleapis.com/auth/gmail.readonly` -- If you only need to read (narrower)

**Google Calendar:**
- `https://www.googleapis.com/auth/calendar` -- Full read/write access to calendars and events
- `https://www.googleapis.com/auth/calendar.events` -- Read/write events only (narrower)
- `https://www.googleapis.com/auth/calendar.readonly` -- Read-only (narrower)

**Google Drive:**
- `https://www.googleapis.com/auth/drive` -- Full access to all Drive files
- `https://www.googleapis.com/auth/drive.file` -- Access only to files created/opened by the app (narrower, non-sensitive)

**Google Docs:**
- `https://www.googleapis.com/auth/documents` -- Read/write Google Docs

**Google Sheets:**
- `https://www.googleapis.com/auth/spreadsheets` -- Read/write Google Sheets

**Google Slides:**
- `https://www.googleapis.com/auth/presentations` -- Read/write Google Slides

**Recommended combined scope set for your use case:**
```
gmail.modify
calendar
drive
documents
spreadsheets
presentations
```

The MCP servers handle scope requests automatically, but understanding them is important for security auditing.

Reference: [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes)

---

## 3. MCP Servers for Google Workspace (The Primary Recommendation)

This is the most important section. MCP servers let Claude Code interact with Google Workspace directly within your conversation. Three strong options exist:

### Option A: `taylorwilsdon/google_workspace_mcp` (Recommended -- Most Feature-Complete)

**Repository:** [github.com/taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)
**Language:** Python (runs via `uvx`)
**Coverage:** Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, Chat, Contacts

This is the most comprehensive Google Workspace MCP server available. It covers every Google Workspace service you need.

**Key capabilities:**
- **Gmail:** Search, read, send, draft, reply, manage labels, archive, trash, mark read/unread
- **Calendar:** List events, create/update/delete events, check free/busy, detect conflicts
- **Drive:** List, search, upload, download files, manage permissions, supports native MS Office formats
- **Docs:** Read and write document content
- **Sheets:** Read/write cells, rich text formatting, conditional formatting, tab management
- **Slides:** Create/edit presentations, markdown-to-slides conversion, text extraction

**Installation for Claude Code:**

```bash
# Add to Claude Code globally (~/.claude.json)
claude mcp add google-workspace \
  -e GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com" \
  -e GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret" \
  -- uvx workspace-mcp
```

Or manually edit `~/.claude.json`:
```json
{
  "mcpServers": {
    "google-workspace": {
      "type": "stdio",
      "command": "uvx",
      "args": ["workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

You can also limit which tools are loaded using `--tools` or `--tool-tier`:
```json
"args": ["workspace-mcp", "--tools", "gmail", "drive", "calendar", "docs", "sheets", "slides"]
```

Or use tiers: `"args": ["workspace-mcp", "--tool-tier", "core"]` (core / extended / complete).

**First-run authentication:** The first time you use it, the server opens a browser window for Google OAuth consent. You authorise once, and tokens are cached locally.

### Option B: `ngs/google-mcp-server` (Lightweight, Go-based)

**Repository:** [github.com/ngs/google-mcp-server](https://github.com/ngs/google-mcp-server)
**Language:** Go (single binary)
**Coverage:** Calendar, Drive, Gmail, Sheets, Docs, Slides

A solid alternative written in Go, meaning it compiles to a single binary with no runtime dependencies. Good if you prefer not to have Python/uvx in the chain.

**Key features:**
- Multi-account support for Calendar, Gmail, and Drive
- Markdown-to-Slides conversion with automatic pagination
- Individual service enable/disable

**Installation for Claude Code:**
```bash
# Build from source
git clone https://github.com/ngs/google-mcp-server.git
cd google-mcp-server
go build

# Add to Claude Code
claude mcp add google /path/to/google-mcp-server
```

Environment variables: `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

### Option C: `GongRzhe/Gmail-MCP-Server` (Gmail-focused)

**Repository:** [github.com/GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server)

If you only want Gmail integration (for email reading/drafting), this is a focused, simpler option. Has auto-authentication support.

### Option D: Composio (Managed service)

**Website:** [composio.dev](https://composio.dev/toolkits/gmail/framework/claude-code)

Composio provides a hosted MCP endpoint for Gmail and other Google services. It handles OAuth and token management for you. Trade-off: your data transits through their servers, and it requires an API key.

```bash
claude mcp add --transport http gmail-composio "YOUR_MCP_URL" \
  --headers "X-API-Key:YOUR_COMPOSIO_API_KEY"
```

SOC 2 Type 2 compliant, but adds a third-party dependency. Best avoided for a self-hosted power user.

### Recommendation

**Use `taylorwilsdon/google_workspace_mcp`** as your primary integration. It has the broadest coverage, active maintenance, and the most complete toolset. It is the single MCP server that covers all six of your requirements (Gmail, Calendar, Drive, Docs, Sheets, Slides).

---

## 4. Standalone CLI Tools

These complement the MCP approach for when you want to interact with Google services directly from the terminal without being inside a Claude Code session.

### `gogcli` (gog) -- Unified Google Suite CLI

**Repository:** [github.com/steipete/gogcli](https://github.com/steipete/gogcli)
**Website:** [gogcli.sh](https://gogcli.sh/)
**Language:** Go (single binary)

This is the most comprehensive standalone CLI tool for Google Workspace. It covers Gmail, Calendar, Drive, Contacts, Tasks, Sheets, Docs, Slides, and People under one unified command.

**Key commands:**
```bash
gog auth credentials ~/Downloads/client_secret.json
gog auth add you@gmail.com
export GOG_ACCOUNT=you@gmail.com

# Gmail
gog gmail labels list
gog gmail search "from:client@example.com after:2026/02/01"
gog gmail send --to client@example.com --subject "Quote" --body "..."

# Calendar
gog calendar events list --max 10
gog calendar events create --summary "Client meeting" --start "2026-02-10T14:00:00"

# Drive
gog drive ls
gog drive download <file-id>

# All output is JSON-first, perfect for scripting
```

**Why this matters for your workflow:** Because `gogcli` outputs JSON, you can pipe it into scripts that convert emails to dated markdown files in your project `correspondence/` folders. Claude Code can also invoke `gogcli` via bash if the MCP server is not available.

**Installation:**
```bash
brew install steipete/tap/gogcli
# or build from source
git clone https://github.com/steipete/gogcli.git && cd gogcli && make && sudo make install
```

### `gcalcli` -- Google Calendar CLI

**Repository:** [github.com/insanum/gcalcli](https://github.com/insanum/gcalcli)
**Language:** Python

A mature, well-established tool specifically for Google Calendar.

```bash
pip install gcalcli
gcalcli --client-id=xxxx.apps.googleusercontent.com init
gcalcli agenda          # Show upcoming events
gcalcli calw            # Weekly calendar view
gcalcli add             # Add new event
gcalcli search "client" # Search events
```

Tokens are stored at `~/.local/share/gcalcli/oauth` on Linux. Supports shell completion for bash, zsh, and fish.

### `himalaya` -- CLI Email Client

**Repository:** [github.com/pimalaya/himalaya](https://github.com/pimalaya/himalaya)
**Language:** Rust (single binary)

A proper terminal email client with Gmail OAuth2 support. More full-featured than just an API wrapper -- it is a real email client for the terminal.

**Features:**
- Multi-account support
- IMAP/SMTP with OAuth2 for Gmail
- PGP encryption
- Notmuch integration
- Scriptable output

**Gmail IMAP config (TOML):**
```toml
[accounts.precept]
email = "jason@preceptsystems.co.za"
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.auth.type = "oauth2"
backend.auth.method = "xoauth2"
backend.auth.client-id = "your-client-id"
backend.auth.client-secret = "your-client-secret"
backend.auth.scopes = ["https://mail.google.com/"]
```

Himalaya is excellent for quick email checks from the terminal and for scripting email exports to markdown.

---

## 5. Automation Platforms (n8n / Make / Zapier)

### n8n (Recommended for self-hosted automation)

**Website:** [n8n.io](https://n8n.io)
**Deployment:** Self-hosted via Docker, free for self-hosted use

n8n is the strongest option here because it is **open source and self-hostable**. Your data stays on your machine. It provides a visual workflow builder with 400+ integrations.

**Relevant use case: Automated email-to-markdown export**

You could create an n8n workflow that:
1. Triggers on a schedule (e.g., every hour) or via webhook
2. Fetches new emails from Gmail using the Gmail Trigger node
3. Converts email body to markdown
4. Writes a dated markdown file to a local directory or Google Drive
5. Optionally commits to git

**Docker deployment:**
```bash
docker run -d --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

n8n supports custom JavaScript/Python code at any workflow step, which is useful for the email-to-markdown conversion logic.

**Trade-off:** n8n adds infrastructure overhead (Docker container, web UI). For a solo user, the MCP server approach is simpler for interactive use. n8n is best for **scheduled/automated** workflows that run without your intervention.

### Make and Zapier

Both are cloud-hosted (not self-hosted), so your data transits through their servers. They have robust Google Workspace integrations but:
- **Make:** Good middle ground, visual workflow builder, can call webhooks
- **Zapier:** Easiest to set up, 6000+ integrations, but most expensive and fully cloud-based

For a privacy-conscious, self-hosted Linux user, **n8n is the clear winner** in this category. Make and Zapier are better suited for non-technical users or teams that need cloud-native solutions.

---

## 6. Google Apps Script

Google Apps Script runs server-side inside Google's infrastructure. It is useful for automations that live entirely within Google Workspace.

### Email-to-Markdown Conversion

You can write an Apps Script that:
1. Runs on a time-driven trigger (e.g., every hour)
2. Searches Gmail for new messages matching criteria
3. Extracts sender, date, subject, and body
4. Converts to markdown format
5. Saves to a file in Google Drive

**Key Apps Script methods:**
- `GmailApp.search(query)` -- Search emails using Gmail query syntax
- `message.getPlainBody()` -- Get plain text body
- `message.getFrom()`, `message.getDate()`, `message.getSubject()`
- `DriveApp.createFile(name, content, mimeType)` -- Save to Drive

**Google Docs to Markdown:**
Google Docs now supports native markdown export. Apps Script can use the Drive API export endpoint:
```
https://docs.google.com/feeds/download/documents/export/Export?exportFormat=markdown&id=${documentId}
```

Reference: [Convert Google Document to Markdown using Apps Script](https://gist.github.com/tanaikech/0deba74c2003d997f67fb2b04dedb1d0)

**Limitation:** Apps Script runs in Google's cloud, not on your local machine. To get files onto your local system, you would need a sync mechanism (Google Drive desktop sync, or a script that pulls from Drive via API).

**Verdict:** Apps Script is a useful supplement for server-side automation within Google Workspace, but it cannot directly write to your local project directories. Use it for transformations that stay within Google's ecosystem (e.g., auto-labelling emails, converting docs to markdown in Drive), then use the MCP server or `gogcli` to pull those files locally.

---

## 7. OAuth 2.0 Setup Process

This is a one-time setup that all tools above depend on. Here is the step-by-step process:

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project" -- name it something like "Precept-AI-Tools"
3. Select the project

### Step 2: Enable APIs

Navigate to **APIs & Services > Library** and enable:
- Gmail API
- Google Calendar API
- Google Drive API
- Google Docs API
- Google Sheets API
- Google Slides API

### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**
2. Select **External** user type (required for personal Gmail; if you have Google Workspace with admin access, you can choose Internal)
3. Fill in:
   - App name: "Precept AI Tools" (or similar)
   - User support email: your email
   - Developer contact email: your email
4. Add the scopes listed in Section 2
5. Add your own email as a test user
6. Save

### Step 4: Create OAuth Client ID

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Select **Desktop app** as application type
4. Name it (e.g., "Claude Code Integration")
5. Click **Create**
6. **Download the JSON file** -- this contains your client ID and client secret

### Step 5: Important Note on Publishing Status

**Critical gotcha:** When your app is in "Testing" status (the default), refresh tokens expire after **7 days**. This means you would need to re-authenticate weekly.

**Workaround:** Push the app to "Production" status. For apps with fewer than 100 users that only your own account uses, Google does not require verification. You and your limited number of users can continue using the app without going through the verification process. After changing to Production, **create new OAuth credentials** (the old ones from Testing may not work correctly).

Reference: [Setting up OAuth 2.0](https://support.google.com/googleapi/answer/6158849)

---

## 8. Security Considerations

### Token Storage on Linux

**Where tokens are stored:**
- MCP servers typically store OAuth tokens in their own data directory (e.g., `~/.config/workspace-mcp/` or similar)
- `gcalcli` stores tokens at `~/.local/share/gcalcli/oauth`
- `gogcli` uses the OS keyring (GNOME Keyring on Linux) or an encrypted on-disk keyring
- Application Default Credentials live at `~/.config/gcloud/application_default_credentials.json`

**Best practices:**

1. **File permissions:** Ensure token files are readable only by your user:
   ```bash
   chmod 600 ~/.config/workspace-mcp/token.json
   chmod 700 ~/.config/workspace-mcp/
   ```

2. **Use GNOME Keyring or KDE Wallet:** Tools like `gogcli` and `himalaya` support storing credentials in the system keyring via the `secret-tool` / D-Bus Secret Service API. GNOME Keyring encrypts secrets at rest using your login password.

3. **Environment variables for MCP:** Store your `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` in `~/.bashrc` or `~/.zshrc` rather than in `.claude.json`:
   ```bash
   export GOOGLE_OAUTH_CLIENT_ID="your-id.apps.googleusercontent.com"
   export GOOGLE_OAUTH_CLIENT_SECRET="your-secret"
   ```
   Then reference them in the MCP config without hardcoding values.

4. **Never commit credentials to git:** Add these to your global `.gitignore`:
   ```
   credentials.json
   client_secret*.json
   token.json
   .env
   ```

5. **Scope minimisation:** Only request the scopes you actually need. The MCP servers request scopes based on which tools/services you enable.

6. **Audit access:** Periodically review which apps have access to your Google account at [myaccount.google.com/permissions](https://myaccount.google.com/permissions).

Reference: [GNOME Keyring - ArchWiki](https://wiki.archlinux.org/title/GNOME/Keyring)

---

## 9. Practical Architecture Recommendations

Here is the recommended architecture for your setup, from highest to lowest priority:

### Layer 1: MCP Server (Interactive AI Use)

```
Claude Code CLI
    |
    |-- MCP Protocol (stdio) ---> google_workspace_mcp (Python/uvx)
                                      |
                                      |-- Google Workspace APIs
                                      |     Gmail, Calendar, Drive,
                                      |     Docs, Sheets, Slides
                                      |
                                      |-- OAuth 2.0 tokens (local)
```

**What this gives you:**
- Ask Claude to "read my last 5 emails from client X" -- it does it
- Ask Claude to "create a Google Doc with this project proposal" -- it does it
- Ask Claude to "check my calendar for next Tuesday and book a 1-hour meeting" -- it does it
- Ask Claude to "read the billing spreadsheet and summarise outstanding invoices" -- it does it
- Ask Claude to "create a slide deck from this markdown outline" -- it does it

### Layer 2: CLI Tools (Direct Terminal Use)

```
Terminal
    |
    |-- gogcli (gog) ---> Gmail, Calendar, Drive, Docs, Sheets, Slides
    |-- gcalcli ---------> Google Calendar (rich terminal display)
    |-- himalaya --------> Gmail (full email client in terminal)
```

**What this gives you:**
- Quick email checks without starting a Claude session
- Calendar views in the terminal
- Scriptable email export (pipe `gogcli` JSON output through `jq` into markdown files)
- Claude Code can also invoke these tools via bash when needed

### Layer 3: Automated Workflows (Optional)

```
n8n (Docker, self-hosted)
    |
    |-- Gmail Trigger: New email arrives
    |     |-- Convert to markdown
    |     |-- Save to project correspondence/ folder
    |     |-- (Optional) git commit
    |
    |-- Scheduled: Daily calendar digest
    |     |-- Fetch today's events
    |     |-- Format as markdown
    |     |-- Save to project file
```

**What this gives you:**
- Automated email-to-markdown without manual intervention
- Runs in the background on your machine
- Optional: trigger via webhook from Claude Code

### Email-to-Markdown Pipeline (Your Specific Use Case)

For importing email correspondence into project files with dated markdown format, you have several options:

**Option A: Claude Code + MCP (Interactive)**
Simply tell Claude: "Search Gmail for all emails from client@example.com in January 2026, and save each one as a dated markdown file in /home/jason/Projects/clientname/correspondence/"

Claude Code can do this directly through the MCP server -- search Gmail, extract content, and write local files.

**Option B: Shell Script + gogcli (Automated)**
Write a shell script that uses `gogcli` to fetch emails and format them:
```bash
gog gmail search "from:client@example.com after:2026/01/01" --json | \
  jq -r '.messages[] | ...' > correspondence/2026-01-15-subject.md
```

**Option C: n8n Workflow (Fully Automated)**
Set up a trigger-based workflow that runs automatically when new emails arrive.

---

## 10. Implementation Roadmap

### Phase 1: Foundation (Day 1)

1. Create a Google Cloud project and enable all six APIs
2. Configure OAuth consent screen and create Desktop App credentials
3. Set publishing status to Production (to avoid 7-day token expiry)
4. Download `credentials.json` and store securely

### Phase 2: MCP Server (Day 1-2)

1. Install `uvx` (Python package runner): `pip install uvx` or `pipx install uv`
2. Add the `taylorwilsdon/google_workspace_mcp` to `~/.claude.json`
3. Start Claude Code, trigger first authentication (browser popup)
4. Test: Ask Claude to read your inbox, check your calendar, list Drive files

### Phase 3: CLI Tools (Day 2-3)

1. Install `gogcli`: `brew install steipete/tap/gogcli` or build from source
2. Configure with your OAuth credentials: `gog auth credentials ~/path/to/client_secret.json`
3. Install `gcalcli`: `pip install gcalcli`
4. Optional: Install `himalaya` for terminal email

### Phase 4: Workflow Automation (Week 2, Optional)

1. Deploy n8n via Docker for automated email-to-markdown conversion
2. Create a Gmail trigger workflow
3. Configure output to your project correspondence directories

### Phase 5: Refinement (Ongoing)

1. Build shell scripts/aliases for common operations
2. Create project-specific `.mcp.json` files if different projects need different tool configurations
3. Set up Claude Code custom instructions (CLAUDE.md) in each project explaining the correspondence folder structure so Claude knows where to save files

---

## Summary of Tools

| Tool | Type | Covers | Best For |
|------|------|--------|----------|
| [google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) | MCP Server | All 6 services | Claude Code integration (primary tool) |
| [google-mcp-server (ngs)](https://github.com/ngs/google-mcp-server) | MCP Server | All 6 services | Alternative if you prefer Go/single binary |
| [Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server) | MCP Server | Gmail only | Lightweight Gmail-only option |
| [gogcli](https://github.com/steipete/gogcli) | CLI Tool | All services | Direct terminal use, scripting, JSON output |
| [gcalcli](https://github.com/insanum/gcalcli) | CLI Tool | Calendar only | Rich terminal calendar display |
| [himalaya](https://github.com/pimalaya/himalaya) | CLI Tool | Email (IMAP) | Full terminal email client |
| [n8n](https://n8n.io) | Automation | All (via integrations) | Scheduled/automated workflows |
| [Composio](https://composio.dev/toolkits/gmail/framework/claude-code) | Managed MCP | All services | Hosted solution (data leaves your machine) |

---

## Key References

- [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes)
- [Create OAuth Credentials](https://developers.google.com/workspace/guides/create-credentials)
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)
- [Setting up OAuth 2.0](https://support.google.com/googleapi/answer/6158849)
- [Choose Gmail API Scopes](https://developers.google.com/workspace/gmail/api/auth/scopes)
- [Choose Calendar API Scopes](https://developers.google.com/workspace/calendar/api/auth)
- [Choose Drive API Scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth)
- [GNOME Keyring - ArchWiki](https://wiki.archlinux.org/title/GNOME/Keyring)
- [Google OAuth for CLI Applications (Simon Willison)](https://til.simonwillison.net/googlecloud/google-oauth-cli-application)
- [Convert Google Docs to Markdown via Apps Script](https://gist.github.com/tanaikech/0deba74c2003d997f67fb2b04dedb1d0)
- [Configuring MCP Tools in Claude Code (Scott Spence)](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)
- [n8n Docker Installation](https://docs.n8n.io/hosting/installation/docker/)
- [n8n Gmail Trigger Integrations](https://n8n.io/integrations/gmail-trigger/)
- [Google Workspace MCP (workspacemcp.com)](https://workspacemcp.com/)

---

## Bottom Line

You do not need to build anything from scratch. The `taylorwilsdon/google_workspace_mcp` server is a mature, actively maintained MCP server that covers all six Google Workspace services you need. Combined with your existing Claude Code CLI workflow, you can have Claude reading your email, checking your calendar, editing spreadsheets, and creating documents within a day of setup. The OAuth setup is the only significant hurdle, and it is a one-time process. Supplement with `gogcli` for quick terminal access outside Claude sessions, and optionally add n8n if you want fully automated background workflows like email-to-markdown export.
