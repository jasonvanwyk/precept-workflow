# Project Resume

## Right Now
**Phase:** Phase 2 IN PROGRESS -- Telegram bot v2 + Precept Field PWA
**Last:** Scaffolded Precept Field PWA (separate repo, 35 files, pushed to GitHub) (2026-02-16)
**Next:** Deploy bot v2 to dev server, deploy Precept Field PWA (DNS + Cloudflare Tunnel + systemd)
**Blocked:** Nothing

## Quick Context
- Internal tooling project for Precept Systems
- Connects Claude Code to Google Workspace, GitHub, Telegram via MCP servers
- Dev server (10.0.10.21, VM 105 on Proxmox "pve") is the always-on hub
- iPhone (iOS) is the mobile device -- Telegram bot + LocalSend for bulk transfers
- 3 MCP servers configured in ~/.claude.json (google-workspace, github, telegram)
- Claude Code runs on desktop (10.0.10.101), syncs with dev server via git
- All credentials exported in ~/.bashrc on desktop
- SSH key auth configured: desktop -> dev server

## What Changed This Session
Scaffolded Precept Field PWA as a new project (`~/Projects/precept-field/`):

**Backend (src/api/) -- 11 Python files:**
- `main.py` -- FastAPI app with lifespan, CORS, static file mount
- `config.py` -- Environment vars (API key, OpenAI, paths, timezone)
- `db.py` -- Full SQLite database ported from Telegram bot (same schema, separate DB file)
- `auth.py` -- Bearer token middleware via FastAPI Depends()
- `transcribe.py` -- OpenAI Whisper helper
- `routes/` -- 6 modules: projects, captures (photo/voice/note/document), visits, tasks, search, activity

**Frontend (src/static/) -- 10 files:**
- `index.html` -- SPA shell with 4-tab bottom nav (Dashboard, Capture, Visits, Menu)
- `manifest.json` -- PWA manifest (Precept purple #5E35B1)
- `sw.js` -- Service worker (cache-first shell, network-first API)
- `css/app.css` -- Mobile-first responsive, dark mode, iOS safe areas
- `js/` -- 6 modules: app.js (router/state), api.js (fetch wrapper), camera.js (MediaDevices), voice.js (MediaRecorder + visualizer), sync.js (IndexedDB offline queue), ui.js (DOM helpers/toasts)
- `icons/` -- Placeholder PNGs (192px + 512px)

**Deploy (src/deploy/) -- 2 files:**
- `precept-field.service` -- systemd user service (port 8001)
- `README.md` -- Step-by-step deploy instructions

**Root files:** README.md, CLAUDE.md, AGENTS.md, STATUS.md, RESUME.md, project.yml, requirements.txt, .gitignore

Repo pushed to: `git@github.com:jasonvanwyk/precept-field.git`

## Deploy Steps (Precept Field)
1. On dev server:
   ```bash
   cd ~/Projects
   git clone git@github.com:jasonvanwyk/precept-field.git
   cd precept-field
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create env file: `~/.config/precept/precept-field.env`
3. Install + start service:
   ```bash
   cp src/deploy/precept-field.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable --now precept-field
   ```
4. Add Cloudflare Tunnel ingress rule (needs sudo on dev server)
5. Add DNS CNAME: `field.precept.co.za` -> tunnel UUID

## Deploy Steps (Bot v2 -- still pending from last session)
1. SSH to dev server, pull latest: `cd ~/Projects/precept-workflow && git pull`
2. Install pytz: `pip install pytz`
3. Restart bot: `systemctl --user restart precept-bot`
4. Test from iPhone (see previous session notes)

## Key Files
- `STATUS.md` -- Full project tracking
- `src/telegram-bot/` -- Bot source code
- `~/Projects/precept-field/` -- PWA project (separate repo)
- `docs/ai-services-strategy.md` -- AI services strategy

## Open Items
- [x] Bot v2 coded (security + text handling + reminders + polish)
- [x] Precept Field PWA scaffolded (35 files, pushed to GitHub)
- [ ] Deploy bot v2 to dev server
- [ ] Test bot v2 from iPhone
- [ ] Deploy Precept Field PWA to dev server
- [ ] Configure DNS + Cloudflare Tunnel for field.precept.co.za
- [ ] Generate proper Precept-branded app icons
- [ ] Smoke test PWA endpoints + iPhone install test
- [ ] Install precept-scan on laptop
- [ ] Anthropic Console setup
- [ ] Build internal workflow automations (case studies)
- [ ] Package service offering (proposals, pricing)
