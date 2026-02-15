# Project Resume

## Right Now
**Phase:** Phase 2 IN PROGRESS -- Telegram bot + AI services strategy
**Last:** Telegram bot fully operational -- all features tested (2026-02-15)
**Next:** Add SQLite operational database; Anthropic Console setup
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
- Telegram bot live and tested (2026-02-15) -- @preceptserver_bot, photo filing, voice transcription (Whisper), project/status commands
- SQLite operational database added to roadmap (structured data, not vector DB)
- AI services strategy doc written (docs/ai-services-strategy.md) -- defines 4-tier service offering for AI workflow transformation, covers the $285B SaaS repricing, KPMG precedent, Anthropic Developer Console toolkit
- Telegram bot code written: src/telegram-bot/ (bot.py, config.py, requirements.txt)
- Bot deployed to dev server (repo cloned, venv, systemd service installed)

## What Jason Needs To Do Before Next Session
1. Create bot via @BotFather on Telegram -- get the bot token
2. Message @userinfobot on Telegram -- get your user ID
3. Get an OpenAI API key from https://platform.openai.com/api-keys
4. SSH to dev server and create the env file:
   ```bash
   cat > ~/.config/precept/telegram-bot.env << 'EOF'
   TELEGRAM_BOT_TOKEN=your-bot-token-here
   OPENAI_API_KEY=sk-your-openai-key-here
   ALLOWED_USER_ID=your-telegram-user-id
   EOF
   chmod 600 ~/.config/precept/telegram-bot.env
   ```
5. Enable lingering (needs sudo on dev server):
   ```bash
   sudo loginctl enable-linger jason
   ```

## Key Files
- `STATUS.md` - Full project tracking
- `docs/ai-services-strategy.md` - AI services strategy (4-tier offering, delivery toolkit)
- `src/telegram-bot/` - Bot source code
- `src/telegram-bot/deploy/README.md` - Full deployment instructions
- `docs/manual.md` - Setup and usage guide
- `docs/integration-strategy-synthesis.md` - Integration strategy document
- `docs/research/` - Planning research reports

## Roadmap (from AI services strategy)
1. Get bot running + tested (blocked on secrets)
2. Add SQLite operational database (bot event log, photo metadata, task/time tracking)
3. Anthropic Console account setup (Prompt Generator, Workbench, Evaluations)
4. Build 2-3 internal workflow automations (case studies for client work)
5. Document the stack (repeatable playbook)
6. Package service offering (proposal templates, pricing for 4 tiers)
7. Pilot with 1-2 existing clients (start with Tier 1 audit)

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
- [x] Bot code written (src/telegram-bot/)
- [x] Bot deployed to dev server (repo cloned, venv, systemd service installed)
- [x] AI services strategy document written
- [x] Create Telegram bot via @BotFather + provide secrets
- [x] Start service and test from iPhone
- [x] Enable lingering on dev server (sudo)
- [ ] Add SQLite database (bot event log, photo metadata, task/time tracking, client touchpoints)
- [ ] Anthropic Console setup (Prompt Generator, Workbench, Evaluations)
- [ ] Build internal workflow automations (case studies)
- [ ] Package service offering (proposals, pricing)
