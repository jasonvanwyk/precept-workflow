# Project Resume

## Right Now
**Phase:** Phase 1 COMPLETE -- ready for Phase 2
**Last:** Phase 1 finished: Cloudflare Tunnel SSH working (browser-based via ssh.meter-tracker.com), LocalSend tested from iPhone to dev server, VLAN fix for TP-Link AP (2026-02-08)
**Next:** Phase 2 -- Create Telegram bot via @BotFather, build and deploy on dev server
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
- LocalSend installed headless on dev server (systemd user service, port 53317)
- LocalSend tested: iPhone → dev server ~/incoming-photos/ working
- Syncthing dropped -- git handles project sync, LocalSend handles phone transfers, scp for ad-hoc
- VLAN fix: switch port 10 moved from VLAN 1 → VLAN 10 so TP-Link WiFi clients can see dev server
- Cloudflare Tunnel SSH: cloudflared on dev server, browser-based SSH via https://ssh.meter-tracker.com
- Desktop SSH via ProxyCommand in ~/.ssh/config (cloudflared access ssh)

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
- [x] LocalSend on dev server (headless, systemd service)
- [x] Syncthing dropped (git + LocalSend + scp covers all sync needs)
- [x] LocalSend tested from iPhone to dev server (HEIC photos received)
- [x] Cloudflare Tunnel SSH from phone (browser-based terminal via ssh.meter-tracker.com)
- [x] Cloudflare Tunnel SSH from desktop (ProxyCommand cloudflared access ssh)
- [x] VLAN fix: TP-Link AP switch port moved to VLAN 10
- [ ] Create Telegram bot via @BotFather (Phase 2)
