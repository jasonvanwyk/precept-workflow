# Project Resume

## Right Now
**Phase:** Phase 1 - Foundation Setup
**Last:** Strategy updated -- replaced Tailscale with Cloudflare Tunnel, bot hosting moved to Proxmox LXC, removed redundant Fetch MCP (2026-02-08)
**Next:** Verify Cloudflare Tunnel SSH route, install Syncthing (desktop + phone), install phone apps
**Blocked:** Nothing

## Quick Context
- Internal tooling project for Precept Systems
- Connects Claude Code to Google Workspace, GitHub, Telegram via MCP servers
- Mobile workflow via Telegram bot + Syncthing + Tailscale
- 3 MCP servers configured in ~/.claude.json (google-workspace, github, telegram); fetch removed (redundant)
- All credentials exported in ~/.bashrc
- Google OAuth first-run will prompt browser auth on first use
- Telegram MCP may need interactive phone verification on first connect

## Recent Progress
- gh CLI authenticated (jasonvanwyk, SSH, key uploaded)
- GITHUB_TOKEN exported dynamically via `gh auth token`
- Google Cloud project created (Precept-AI-Tools, ID: precept-ai-tools)
- 6 Google APIs enabled (Gmail, Calendar, Drive, Docs, Sheets, Slides)
- OAuth consent screen configured, scopes added, published to production
- OAuth client created (Desktop app, "Claude Code Integration")
- Credentials JSON saved to ~/.config/precept/google-credentials.json
- GOOGLE_OAUTH_CLIENT_ID + SECRET exported in .bashrc
- Telegram API app created (Precept Tools), api_id + api_hash in .bashrc
- Telegram MCP server added to ~/.claude.json

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
- [x] Test all MCP servers (all 4 working)
- [ ] Create Telegram bot via @BotFather (Phase 2)
- [ ] Verify Cloudflare Tunnel SSH route
- [ ] Install Syncthing, phone apps
