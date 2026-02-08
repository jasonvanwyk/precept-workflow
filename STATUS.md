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

### In Progress

| Task | Status | Notes |
|------|--------|-------|

### Planned

| Task | Status | Notes |
|------|--------|-------|
| Verify Cloudflare Tunnel SSH route | TODO | Phase 1: confirm SSH access via existing tunnel |
| Install Syncthing (desktop + phone) | TODO | Phase 1: file sync |
| Install phone apps (Termius, Markor, WiFiAnalyzer) | TODO | Phase 1: mobile tools |
| Build Telegram bot (Phase 2) | TODO | Clone claude-telegram-bridge, deploy to Proxmox LXC |
| Template integration (Phase 2) | TODO | Add slash commands, project.yml schema |

---

## Key Decisions Made

1. MCP Stack: 3 servers (Google Workspace, GitHub, Telegram); Fetch removed (redundant with built-in WebFetch)
2. Telegram over Signal for mobile bot
3. claude-telegram-bridge as bot starting point
4. Proxmox LXC for bot hosting (always-on, survives desktop reboots)
5. Syncthing for file sync (peer-to-peer, WiFi-only)
6. Cloudflare Tunnel for remote access (already configured, no subscription)
7. Environment variables for secrets (not .env files)
