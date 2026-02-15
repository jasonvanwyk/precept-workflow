# Project Resume

## Right Now
**Phase:** Phase 2 IN PROGRESS -- Telegram bot v2 upgrade
**Last:** Bot v2 features coded -- security fixes, text handling, daily reminders, status enrichment (2026-02-15)
**Next:** Deploy updated bot to dev server, test all features from iPhone, install precept-scan on laptop
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
Bot v2 upgrade -- 7 modified files across 4 priorities:

**Security (Priority 1):**
- `src/laptop-tools/precept-scan.sh` -- Input validation (project name regex), array expansion for nmap/iperf3 args (was string interpolation = command injection), SSH host verification
- `src/telegram-bot/register-scan.py` -- Path traversal protection (resolve + startswith check), project name validation
- `src/telegram-bot/handlers.py` -- File upload limits (100MB max, blocked .exe/.bat/.cmd/.ps1/.sh extensions), rejection logging
- `src/telegram-bot/bot.py` -- Rate limiting in AuthFilter (30 messages/minute sliding window)

**Text Message Handling (Priority 2):**
- `src/telegram-bot/db.py` -- New `quick_notes` table (migration 2), `log_quick_note()` helper, search includes quick notes, project_stats includes note count, visit summary includes note count
- `src/telegram-bot/handlers.py` -- Outside-visit text prompts "Save as quick note?" with Yes/No buttons, `note_save_callback` handler, `quick_note_text()` now logs to DB
- `src/telegram-bot/bot.py` -- `save_as_note` callback handler registered

**Daily Reminders (Priority 3):**
- `src/telegram-bot/config.py` -- Added pytz, TIMEZONE = Africa/Johannesburg
- `src/telegram-bot/requirements.txt` -- Added pytz
- `src/telegram-bot/handlers.py` -- `morning_briefing()` (07:30 SAST), `afternoon_wrapup()` (16:30 SAST), `cmd_reminders()` toggle
- `src/telegram-bot/bot.py` -- `setup_reminders()` using JobQueue.run_daily(), /reminders command registered

**Bot Polish (Priority 4):**
- `src/telegram-bot/handlers.py` -- Status output enriched with quick notes count + active task info, visit summaries include note count

## Deploy Steps
1. Push to GitHub from desktop
2. SSH to dev server, pull latest:
   ```bash
   cd ~/Projects/precept-workflow && git pull
   ```
3. Install pytz:
   ```bash
   pip install pytz
   ```
4. Restart bot service:
   ```bash
   systemctl --user restart precept-bot
   ```
5. Check logs:
   ```bash
   journalctl --user -u precept-bot -n 50
   ```
6. Test from iPhone:
   - Open @preceptserver_bot, send /start
   - Verify inline keyboard buttons appear
   - Set active project, send text outside visit -- should prompt "Save as quick note?"
   - Tap "Yes" -- should save to file + DB
   - Start visit, send text -- should auto-save without prompt
   - Send a document -- should work (test size/type rejection mentally)
   - /search for a note -- should find it
   - /reminders -- should toggle on/off
   - /status -- should show quick notes count + active task

## Key Files
- `STATUS.md` - Full project tracking
- `src/telegram-bot/` - Bot source code (db.py, menus.py, handlers.py, bot.py, config.py)
- `src/laptop-tools/` - Laptop network scan tools
- `docs/ai-services-strategy.md` - AI services strategy
- `src/telegram-bot/deploy/README.md` - Deployment instructions

## Open Items
- [x] Bot v2 coded (security + text handling + reminders + polish)
- [ ] Deploy updated bot to dev server
- [ ] Test all features from iPhone
- [ ] Install precept-scan on laptop (`sudo cp precept-scan.sh /usr/local/bin/precept-scan`)
- [ ] Anthropic Console setup (Prompt Generator, Workbench, Evaluations)
- [ ] Build internal workflow automations (case studies)
- [ ] Package service offering (proposals, pricing)
- [ ] CrewAI POC for automated site visit reporting (future)
