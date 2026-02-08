# Project Status - Precept Workflow

**Last Updated:** 2026-02-08
**Project Metadata:** See `project.yml`

---

## Current Phase: Phase 1 - Foundation Setup

Setting up MCP servers, credentials, and mobile tools so that all Precept projects can use Google Workspace, GitHub, and Telegram integrations from within Claude Code.

---

## Task Status

### Completed

| Task | Completed | Notes |
|------|-----------|-------|
| Research: Google Workspace integration | 2026-02-07 | See docs/research/05-google-workspace-integration.md |
| Research: Telegram/Signal bots | 2026-02-07 | See docs/research/06-telegram-signal-bot.md |
| Research: MCP server ecosystem | 2026-02-07 | See docs/research/07-mcp-server-ecosystem.md |
| Research: Mobile field sync | 2026-02-07 | See docs/research/08-mobile-field-sync.md |
| Write integration strategy synthesis | 2026-02-07 | See docs/integration-strategy-synthesis.md |
| Add MCP config to ~/.claude.json | 2026-02-07 | 3 servers (google-workspace, github, telegram); fetch removed (redundant with built-in WebFetch) |
| Create dedicated precept-workflow project | 2026-02-08 | Moved scattered files into one place |
| Write setup manual (docs/manual.md) | 2026-02-08 | Setup checklist + usage guide |
| Push to GitHub | 2026-02-08 | git@github.com:jasonvanwyk/precept-workflow.git |
| Verify prerequisites (uvx, npx, gh) | 2026-02-08 | All installed, ~/.config/precept/ created |
| Google Cloud OAuth setup | 2026-02-08 | Project: precept-ai-tools, 6 APIs enabled, credentials in .bashrc |
| GitHub PAT creation | 2026-02-08 | gh auth login + dynamic export in .bashrc |
| Telegram API credentials | 2026-02-08 | api_id + api_hash in .bashrc |
| Add Telegram MCP to ~/.claude.json | 2026-02-08 | telegram-mcp server added |
| Test all MCP servers | 2026-02-08 | All 3 MCP servers verified (GitHub, Google Workspace, Telegram) + built-in WebFetch |
| Remove fetch MCP server | 2026-02-08 | Redundant with built-in WebFetch; reduces MCP context token usage |
| Update strategy for Proxmox + Cloudflare Tunnel | 2026-02-08 | Replaced Tailscale with Cloudflare Tunnel, bot hosting moved to Proxmox LXC |
| SSH key auth to dev server | 2026-02-08 | ssh-copy-id to 10.0.10.21, Claude Code can now SSH remotely |
| Install Syncthing on dev server | 2026-02-08 | systemd user service enabled on 10.0.10.21, ~/incoming-photos/ created |
| Install LocalSend on dev server | 2026-02-08 | Headless mode via xvfb-run, systemd user service on port 53317 |
| Update docs for iOS + dev server hub | 2026-02-08 | iOS not Android, LocalSend for bulk transfers, dev server as central hub |

### In Progress

| Task | Status | Notes |
|------|--------|-------|

### Planned

| Task | Status | Notes |
|------|--------|-------|
| Verify Cloudflare Tunnel SSH route | TODO | Phase 1: confirm SSH access from phone via existing tunnel |
| Install Syncthing on desktop | TODO | Phase 1: sync with dev server (for non-git files) |
| Build Telegram bot (Phase 2) | TODO | Clone claude-telegram-bridge, deploy on dev server |
| Template integration (Phase 2) | TODO | Add slash commands, project.yml schema |

---

## Key Decisions Made

1. MCP Stack: 3 servers (Google Workspace, GitHub, Telegram); Fetch removed (redundant with built-in WebFetch)
2. Telegram over Signal for mobile bot
3. claude-telegram-bridge as bot starting point
4. Dev server (10.0.10.21) as central hub -- bot, Syncthing, LocalSend, project files
5. Syncthing for desktop ↔ dev server sync; LocalSend for iPhone → dev server bulk transfers
6. Cloudflare Tunnel for remote access (already configured, no subscription)
7. Environment variables for secrets (not .env files)
8. iOS (not Android) -- Telegram, LocalSend, Termius on iPhone
