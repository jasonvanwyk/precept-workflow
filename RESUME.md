# Project Resume

## Right Now
**Phase:** Phase 2 IN PROGRESS -- Telegram bot
**Last:** Bot code written and partially deployed to dev server (2026-02-09)
**Next:** Jason provides bot token + OpenAI key + user ID, then start service and test
**Blocked:** Waiting on 3 secrets (TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, ALLOWED_USER_ID)

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
- Telegram bot code written: src/telegram-bot/ (bot.py, config.py, requirements.txt)
- Bot features: /project (fuzzy match), /projects, /status, photo filing + git commit, voice transcription via Whisper + git commit, single-user whitelist
- Systemd service file + deploy README created in src/telegram-bot/deploy/
- Repo cloned to dev server ~/Projects/precept-workflow
- Python venv created + dependencies installed on dev server
- Systemd user service installed (precept-bot.service)
- .gitignore updated with Python entries

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
- `src/telegram-bot/` - Bot source code
- `src/telegram-bot/deploy/README.md` - Full deployment instructions
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
- [x] Bot code written (src/telegram-bot/)
- [x] Bot deployed to dev server (repo cloned, venv, systemd service installed)
- [ ] Create Telegram bot via @BotFather + provide secrets
- [ ] Start service and test from iPhone
- [ ] Enable lingering on dev server (sudo)
