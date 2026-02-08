# Precept Workflow - AI Agent Context

## Session Startup

**Read these files first, in order:**

1. `RESUME.md` -- Current phase, last/next actions
2. `STATUS.md` -- Task tracking
3. `README.md` -- Project overview

Then check recent git history: `git log --oneline -10`

## Project Overview

Integration and workflow automation for Precept Systems. Connects Claude Code (via MCP servers), Google Workspace, GitHub, Telegram bot, and mobile field capture tools into a unified system.

**Type:** Internal
**Purpose:** Set up and maintain the tooling that connects all Precept projects to external services

## Key Facts

| Item | Value |
|------|-------|
| Company | Precept Systems (Pty) Ltd |
| Director | Jason van Wyk |
| Currency | ZAR (R) |
| Timezone | SAST (UTC+2) |

## What This Project Manages

| Component | What It Does |
|-----------|-------------|
| MCP Servers | Google Workspace, GitHub, Fetch, Telegram -- configured in `~/.claude.json` |
| Telegram Bot | Mobile interface for photo filing, voice transcription, status queries |
| Syncthing | Peer-to-peer file sync between phone and desktop |
| Tailscale | Mesh VPN for remote SSH access to desktop from phone |
| Template Integration | Slash commands and conventions that connect projects to these tools |

## File Organization

| Location | Contents |
|----------|----------|
| `docs/` | Manual, strategy documents |
| `docs/research/` | Research reports from planning phase |
| `src/` | Scripts, bot code (when built) |
| `project.yml` | Machine-readable project metadata |

## Conventions

- **Files:** `lowercase-with-hyphens.ext`
- **Numbered docs:** `NN-description.ext` (zero-padded)
- **Commits:** Descriptive messages summarising the "why", not the "what"
- **Co-author footer:** `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

## Git Workflow

- Remote: `git@github.com:jasonvanwyk/precept-workflow.git`
- Branch: `main`
- Always push after significant work sessions
