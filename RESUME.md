# Project Resume

## Right Now
**Phase:** Phase 1 - Foundation Setup
**Last:** All credentials configured -- Google OAuth, GitHub PAT, Telegram API (2026-02-08)
**Next:** Restart Claude Code and test all MCP servers (Google, GitHub, Telegram)
**Blocked:** Nothing -- ready to test

## Quick Context
- Internal tooling project for Precept Systems
- Connects Claude Code to Google Workspace, GitHub, Telegram via MCP servers
- Mobile workflow via Telegram bot + Syncthing + Tailscale
- All 4 MCP servers configured in ~/.claude.json (google-workspace, github, fetch, telegram)
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
- [ ] Test all MCP servers (restart Claude Code first)
- [ ] Create Telegram bot via @BotFather (Phase 2)
- [ ] Install Tailscale, Syncthing, phone apps
