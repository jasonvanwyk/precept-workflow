# Project Resume

## Right Now
**Phase:** Phase 1 - Foundation Setup
**Last:** Project scaffolded, pushed to GitHub, started setup checklist (2026-02-08)
**Next:** Google Cloud OAuth setup (Step 1 of checklist -- see docs/manual.md Section 3.1)
**Blocked:** All MCP testing blocked on credentials

## Quick Context
- Internal tooling project for Precept Systems
- Connects Claude Code to Google Workspace, GitHub, Telegram via MCP servers
- Mobile workflow via Telegram bot + Syncthing + Tailscale
- Prerequisites confirmed: uvx, npx, gh all installed; ~/.config/precept/ created
- Setup checklist is in docs/manual.md -- work through Section 3 step by step

## Recent Progress
- Moved strategy docs and research into dedicated project
- Created practical manual (docs/manual.md)
- Pushed to GitHub (jasonvanwyk/precept-workflow)
- Confirmed prerequisites (uvx 0.9.9, npx/node 25.1.0, gh 2.86.0)
- Created ~/.config/precept/ directory (chmod 700)

## Key Files
- `STATUS.md` - Full project tracking
- `docs/manual.md` - Setup and usage guide
- `docs/integration-strategy-synthesis.md` - Full strategy document
- `docs/research/` - Planning research reports

## Open Items
- [ ] Google Cloud OAuth setup (~30 min)
- [ ] GitHub PAT creation (~5 min)
- [ ] Telegram bot + API credentials (~15 min)
- [ ] Add Telegram MCP to ~/.claude.json
- [ ] Test all MCP servers
- [ ] Install Tailscale, Syncthing, phone apps
