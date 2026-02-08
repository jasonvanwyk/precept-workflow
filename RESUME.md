# Project Resume

## Right Now
**Phase:** Phase 1 - Foundation Setup
**Last:** Syncthing + LocalSend installed on dev server, Syncthing installed on desktop (not yet enabled/paired), all docs updated for iOS + dev server hub (2026-02-08)
**Next:** Enable Syncthing on desktop and pair with dev server, verify Cloudflare Tunnel SSH from phone, test LocalSend from iPhone to dev server
**Blocked:** Nothing

## Quick Context
- Internal tooling project for Precept Systems
- Connects Claude Code to Google Workspace, GitHub, Telegram via MCP servers
- Dev server (10.0.10.21, VM 105 on Proxmox "pve") is the always-on hub
- iPhone (iOS) is the mobile device -- Telegram bot + LocalSend for bulk transfers
- 3 MCP servers configured in ~/.claude.json (google-workspace, github, telegram)
- Claude Code runs on desktop (10.0.10.101), syncs with dev server via git
- All credentials exported in ~/.bashrc on desktop
- SSH key auth configured: desktop → dev server

## Recent Progress
- All 3 MCP servers tested and working (Google Workspace, GitHub, Telegram)
- Fetch MCP removed (redundant with built-in WebFetch)
- Strategy revised: Cloudflare Tunnel replaces Tailscale, dev server replaces desktop for services
- SSH key auth set up: desktop → dev server (10.0.10.21)
- Syncthing installed and running on dev server (systemd user service)
- LocalSend installed headless on dev server (systemd user service, port 53317)
- ~/incoming-photos/ created on dev server for file staging

## Key Files
- `STATUS.md` - Full project tracking
- `docs/manual.md` - Setup and usage guide
- `docs/integration-strategy-synthesis.md` - Full strategy document
- `docs/research/` - Planning research reports

## Open Items
- [x] Google Cloud OAuth setup
- [x] GitHub PAT creation
- [x] Telegram API credentials
- [x] Add Telegram MCP to ~/.claude.json
- [x] Test all MCP servers (all 3 working + built-in WebFetch)
- [x] SSH key auth to dev server (10.0.10.21)
- [x] Syncthing on dev server (systemd service)
- [x] LocalSend on dev server (headless, systemd service)
- [ ] Enable Syncthing on desktop and pair with dev server (installed, not yet enabled)
- [ ] Verify Cloudflare Tunnel SSH from phone
- [ ] Create Telegram bot via @BotFather (Phase 2)
