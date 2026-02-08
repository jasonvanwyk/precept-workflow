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
| Add MCP config to ~/.claude.json | 2026-02-07 | 3 of 4 servers (google-workspace, github, fetch) |
| Create dedicated precept-workflow project | 2026-02-08 | Moved scattered files into one place |
| Write setup manual (docs/manual.md) | 2026-02-08 | Setup checklist + usage guide |
| Push to GitHub | 2026-02-08 | git@github.com:jasonvanwyk/precept-workflow.git |
| Verify prerequisites (uvx, npx, gh) | 2026-02-08 | All installed, ~/.config/precept/ created |

### In Progress

| Task | Status | Notes |
|------|--------|-------|
| Google Cloud OAuth setup | TODO | Create project, enable APIs, create credentials |
| GitHub PAT creation | TODO | Generate token, export as GITHUB_TOKEN |
| Telegram bot + API credentials | TODO | @BotFather for bot, my.telegram.org for API |
| Add Telegram MCP to ~/.claude.json | TODO | After API credentials exist |

### Planned

| Task | Status | Notes |
|------|--------|-------|
| Test all MCP servers | TODO | Phase 1: verify each server works |
| Install Tailscale (desktop + phone) | TODO | Phase 1: mesh VPN |
| Install Syncthing (desktop + phone) | TODO | Phase 1: file sync |
| Install phone apps (Termius, Markor, WiFiAnalyzer) | TODO | Phase 1: mobile tools |
| Build Telegram bot (Phase 2) | TODO | Clone claude-telegram-bridge, customise |
| Template integration (Phase 2) | TODO | Add slash commands, project.yml schema |

---

## Key Decisions Made

1. MCP Stack: 4 servers (Google Workspace, GitHub, Fetch, Telegram)
2. Telegram over Signal for mobile bot
3. claude-telegram-bridge as bot starting point
4. Desktop hosting via systemd (not Proxmox/VPS)
5. Syncthing for file sync (peer-to-peer, WiFi-only)
6. Tailscale for remote access (mesh VPN)
7. Environment variables for secrets (not .env files)
