# Project Status - Precept Workflow

**Last Updated:** 2026-02-09
**Project Metadata:** See `project.yml`

---

## Current Phase: Phase 2 - Semi-Automated Workflows (Phase 1 Complete)

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
| Install LocalSend on dev server | 2026-02-08 | Headless mode via xvfb-run, systemd user service on port 53317 |
| Drop Syncthing from plan | 2026-02-08 | Git + LocalSend + scp covers all sync needs; Syncthing adds unnecessary complexity |
| Update docs for iOS + dev server hub | 2026-02-08 | iOS not Android, LocalSend for bulk transfers, dev server as central hub |
| Fix VLAN for TP-Link WiFi AP | 2026-02-08 | Switch port 10 moved from VLAN 1 → VLAN 10; iPhone WiFi now on Work VLAN |
| Test LocalSend from iPhone to dev server | 2026-02-08 | 2 HEIC photos received in ~/incoming-photos/, auto-accept enabled |
| Cloudflare Tunnel SSH to dev server | 2026-02-08 | cloudflared installed, tunnel "dev-server", browser SSH at ssh.meter-tracker.com, Zero Trust Access with email OTP |
| Desktop SSH via Cloudflare Tunnel | 2026-02-08 | ProxyCommand in ~/.ssh/config, ssh jason@ssh.meter-tracker.com works |
| Laptop setup (jason-laptop, 10.0.10.112) | 2026-02-08 | Cloudflare Tunnel SSH + network diagnostic tools (nmap, wireshark, wavemon, iperf3, etc.) |

### In Progress

| Task | Status | Notes |
|------|--------|-------|
| Build Telegram bot (Phase 2) | In Progress | Code written, deployed to dev server, awaiting bot token + secrets from Jason |

### Planned

| Task | Status | Notes |
|------|--------|-------|
| Template integration (Phase 2) | TODO | Add slash commands, project.yml schema |

---

## Key Decisions Made

1. MCP Stack: 3 servers (Google Workspace, GitHub, Telegram); Fetch removed (redundant with built-in WebFetch)
2. Telegram over Signal for mobile bot
3. claude-telegram-bridge as bot starting point
4. Dev server (10.0.10.21) as central hub -- bot, LocalSend, project files
5. No Syncthing -- git for project sync, LocalSend for iPhone → dev server, scp for ad-hoc
6. Cloudflare Tunnel for remote SSH (tunnel "dev-server", browser SSH at ssh.meter-tracker.com, Zero Trust email OTP)
7. Environment variables for secrets (not .env files)
8. iOS (not Android) -- Telegram, LocalSend, Termius on iPhone
