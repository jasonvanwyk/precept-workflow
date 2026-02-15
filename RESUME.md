# Project Resume

## Right Now
**Phase:** Phase 2 IN PROGRESS -- Telegram bot upgrade
**Last:** Bot upgrade coded -- SQLite, menus, site visits, task timer, laptop tools, search (2026-02-15)
**Next:** Deploy updated bot to dev server, test all features from iPhone
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

## What Changed This Session
Major bot upgrade -- 6 new/modified files:
- `src/telegram-bot/db.py` -- SQLite database with migrations, 7 tables (photos, voice_notes, site_visits, network_scans, bot_events, tasks, schema_version)
- `src/telegram-bot/menus.py` -- Inline keyboard builders + persistent reply keyboards
- `src/telegram-bot/handlers.py` -- All handler logic extracted from bot.py, ConversationHandler states, visit mode, task timer, search, document handler
- `src/telegram-bot/bot.py` -- Rewritten to use ConversationHandler with AuthFilter, wires up all states
- `src/telegram-bot/register-scan.py` -- CLI tool for laptop to register scans in SQLite
- `src/laptop-tools/precept-scan.sh` -- Laptop wrapper for nmap/iperf3 with auto-filing + DB registration
- `src/laptop-tools/README.md` -- Usage instructions
- `src/telegram-bot/config.py` -- Added DB_PATH

## Deploy Steps
1. Push to GitHub from desktop
2. SSH to dev server, pull latest:
   ```bash
   cd ~/Projects/precept-workflow && git pull
   ```
3. Restart bot service:
   ```bash
   systemctl --user restart precept-bot
   ```
4. Check logs:
   ```bash
   journalctl --user -u precept-bot -n 50
   ```
5. Test from iPhone:
   - Open @preceptserver_bot, send /start
   - Verify inline keyboard buttons appear
   - Tap Switch project, select a project
   - Start a site visit, send a photo, end the visit
   - Check DB: `sqlite3 -header ~/.config/precept/precept.db 'SELECT * FROM photos; SELECT * FROM site_visits;'`

## Key Files
- `STATUS.md` - Full project tracking
- `src/telegram-bot/` - Bot source code (db.py, menus.py, handlers.py, bot.py, config.py)
- `src/laptop-tools/` - Laptop network scan tools
- `docs/ai-services-strategy.md` - AI services strategy
- `src/telegram-bot/deploy/README.md` - Deployment instructions

## Open Items
- [x] Bot upgrade coded (SQLite + menus + visits + tasks + laptop tools + search)
- [ ] Deploy updated bot to dev server
- [ ] Test all features from iPhone
- [ ] Install precept-scan on laptop (`sudo cp precept-scan.sh /usr/local/bin/precept-scan`)
- [ ] Anthropic Console setup (Prompt Generator, Workbench, Evaluations)
- [ ] Build internal workflow automations (case studies)
- [ ] Package service offering (proposals, pricing)
