---

# Mobile Messaging Bot for Precept Systems -- Research Report

## Executive Summary

This report investigates how to build a mobile messaging bot that connects to an AI assistant and Jason's local project management system (`~/Projects/`). The bot would allow querying project files, sending photos and technical data, dictating notes, getting AI assistance, and updating project status -- all from a phone while on-site at client locations.

The research reveals a rich ecosystem of existing solutions, with **Telegram as the clear winner** over Signal for this use case. Three viable architectural paths emerged: (1) an existing project called **claude-code-telegram** that is almost purpose-built for this scenario, (2) **OpenClaw** (formerly Clawdbot/Moltbot) which Jason has already explored and which supports Telegram + Signal + many other channels, and (3) a **custom lightweight bot** built with python-telegram-bot or grammY and the Claude API.

---

## 1. Telegram Bot API

### How It Works

The Telegram Bot API is a well-documented HTTP-based API maintained by Telegram. Bots are special Telegram accounts that do not require a phone number. You create one by talking to `@BotFather` on Telegram, which gives you an API token. Your server then communicates with Telegram via either **polling** (periodically asking for new messages) or **webhooks** (Telegram pushes updates to your HTTPS endpoint).

### Media Capabilities

| Media Type | Receive | Send | Size Limit | Notes |
|-----------|---------|------|------------|-------|
| Photos | Yes | Yes | 20MB download / 50MB upload | Multiple resolutions provided via `file_id` |
| Documents/Files | Yes | Yes | 20MB download / 50MB upload | Any file type |
| Voice Messages | Yes | Yes | 20MB download / 50MB upload | OGG/OPUS, MP3, or M4A format |
| Video | Yes | Yes | 20MB download / 50MB upload | MP4 preferred |
| Location | Yes | Yes | N/A | GPS coordinates |

**Self-hosted Bot API server**: By running the [official Telegram Bot API server](https://github.com/tdlib/telegram-bot-api) locally via Docker, these limits increase to **2GB** for both uploads and downloads, and files can be referenced via local filesystem paths (no HTTP transfer needed).

### Hosting Requirements

- A server that can run continuously (Linux desktop, VPS, or LXC container)
- For **polling mode**: No public IP or HTTPS needed (the bot calls out to Telegram)
- For **webhook mode**: Requires a public HTTPS endpoint (ngrok, Cloudflare tunnel, or a VPS with a domain)
- Polling mode is simpler and perfectly adequate for a single-user bot

### Key Frameworks

| Framework | Language | Notes |
|-----------|----------|-------|
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) | Python | Mature, well-documented, async support |
| [grammY](https://grammy.dev/) | TypeScript/JS | Modern, plugin ecosystem, used by OpenClaw |
| [Telegraf](https://telegrafjs.org/) | TypeScript/JS | Popular, middleware-based |
| [aiogram](https://docs.aiogram.dev/) | Python | Async-first, modern Python |

### Sources
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Self-hosting the Telegram Bot API](https://dev.to/joybtw/how-i-self-hosted-the-telegram-bot-api-with-docker-to-bypass-50mb-upload-limits-483a)
- [A Developer's Guide to Building Telegram Bots in 2025](https://stellaray777.medium.com/a-developers-guide-to-building-telegram-bots-in-2025-dbc34cd22337)

---

## 2. Signal Bot/API

### The Reality

Signal does **not** have an official bot API. Signal is privacy-first and intentionally does not support bots as a platform feature. All Signal bot development relies on unofficial community tools.

### signal-cli

The primary tool is [signal-cli](https://github.com/AsamK/signal-cli), an unofficial command-line interface for Signal. It requires registering a real phone number (you need a SIM card or virtual number). It supports:

- Sending and receiving text messages
- Sending and receiving attachments (photos, files)
- Group messaging
- Receiving voice messages (as audio file attachments, no built-in transcription)

### signal-cli-rest-api

[bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) wraps signal-cli in a Docker container with REST endpoints. It runs in three modes:

| Mode | Description | Speed |
|------|-------------|-------|
| Normal | Invokes signal-cli per request | Slow (JVM startup each time) |
| JSON-RPC | Persistent daemon | Fast |
| Native | Pre-compiled binary | Fastest |

**Critical limitation**: There is no push/webhook mechanism. You must **poll** for new messages, and the API recommends calling the receive endpoint regularly. The `AUTO_RECEIVE_SCHEDULE` parameter can automate this, but it is fundamentally less responsive than Telegram's webhook system.

### Signal Bot Frameworks

| Project | Language | Notes |
|---------|----------|-------|
| [signalbot](https://pypi.org/project/signalbot/) | Python | Async framework, requires signal-cli |
| [signal-bot](https://signal-bot.readthedocs.io/) | Python | Another framework option |
| [signal-ai-chat-bot](https://github.com/piebro/signal-ai-chat-bot) | Python | AI chatbot for Signal (uses Gemini) |
| [signal-mcp-client](https://github.com/piebro/signal-mcp-client) | Python | MCP client using Signal as transport |

### Sources
- [signal-cli-rest-api on GitHub](https://github.com/bbernhard/signal-cli-rest-api)
- [signal-cli on GitHub](https://github.com/AsamK/signal-cli)
- [Signal-Bot documentation](https://signal-bot.readthedocs.io/)
- [Bot Development for Messenger Platforms (2025 guide)](https://alexasteinbruck.medium.com/bot-development-for-messenger-platforms-whatsapp-telegram-and-signal-2025-guide-50635f49b8c6)

---

## 3. Claude API Integration

### Direct API Integration

The Anthropic Claude API (`api.anthropic.com`) provides a straightforward HTTP API. A bot would:
1. Receive a message from Telegram/Signal
2. Construct a prompt (potentially including project context from local files)
3. Send it to the Claude API
4. Return the response to the user

Pricing (as of early 2026, for Claude Sonnet): approximately $3/M input tokens, $15/M output tokens. For a personal assistant doing maybe 50-100 queries per day with moderate context, this would cost roughly $5-30/month depending on usage patterns.

### Existing Claude + Telegram Projects

Several purpose-built projects exist:

#### claude-code-telegram (RichardAtCT)
**Repository**: [github.com/RichardAtCT/claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram)

This is the most directly relevant project for Jason's use case. Features include:
- Remote access to Claude Code via Telegram
- **Directory navigation** (`/cd`, `/ls`, `/pwd`) with project switching
- **Session persistence** per project directory (survives bot restarts)
- Multi-layer authentication (whitelist + optional token)
- File upload support (photos, archives, code files)
- Rate limiting with token bucket algorithm
- Both Anthropic SDK and Claude CLI support

#### claude-telegram-bridge (viniciustodesco)
**Repository**: [github.com/viniciustodesco/claude-telegram-bridge](https://github.com/viniciustodesco/claude-telegram-bridge)

Features:
- Real-time streaming of Claude responses
- **Vision/image analysis** -- send photos and Claude analyzes them
- **Audio transcription** via Whisper API -- send voice messages that get automatically transcribed
- Persistent sessions with conversation history
- Interactive permissions for tool use

#### OpenClaw (formerly Clawdbot/Moltbot)
**Repository**: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)

Jason has already explored this (see `/home/jason/Projects/clawdbot-explore/SETUP_NOTES.md`). Key points:
- 145,000+ GitHub stars, massive community
- Supports Telegram, Signal, WhatsApp, Discord, Slack, Matrix, and many more
- Self-hosted on your own hardware -- files never leave your machine except when sent to the AI model API
- 50+ bundled skills and integrations
- Node.js 22+ required, Docker recommended
- Jason already has a Proxmox LXC deployment plan documented

#### Claude Code Hooks Approach
A lighter-weight option: Claude Code has a **hooks system** that can fire shell commands at specific lifecycle events. A [documented approach](https://medium.com/@dan.avila7/step-by-step-guide-connect-telegram-with-claude-code-hooks-1686fadcee65) uses hooks to send Telegram notifications when Claude Code finishes tasks, and can receive commands back via Telegram replies.

### Sources
- [claude-code-telegram on GitHub](https://github.com/RichardAtCT/claude-code-telegram)
- [claude-telegram-bridge on GitHub](https://github.com/viniciustodesco/claude-telegram-bridge)
- [OpenClaw on GitHub](https://github.com/openclaw/openclaw)
- [Step-by-Step Guide: Connect Telegram with Claude Code Hooks](https://medium.com/@dan.avila7/step-by-step-guide-connect-telegram-with-claude-code-hooks-1686fadcee65)
- [How to Use Claude Code From Your Phone With a Telegram Bot](https://medium.com/@amirilovic/how-to-use-claude-code-from-your-phone-with-a-telegram-bot-dde2ac8783d0)

---

## 4. Self-Hosted Options

### Option A: Run on Jason's Linux Desktop

**Pros**:
- Direct filesystem access to `~/Projects/` -- no syncing or remote mounting needed
- No additional cost
- Full control

**Cons**:
- Desktop must be running and connected to the internet
- If the desktop goes to sleep or loses power/internet while on-site, the bot is unreachable
- Requires either a static IP or a tunnel solution (ngrok, Cloudflare Tunnel, Tailscale)

**Mitigation**: Use Telegram polling mode (not webhooks) so no public IP is needed. The bot simply calls out to Telegram's servers. Combined with a `systemd` service to auto-start and auto-restart, this is reliable as long as the machine is on and connected.

### Option B: Proxmox LXC Container (Jason's Existing Plan)

Jason already has detailed setup notes for deploying OpenClaw in a Proxmox LXC container (`/home/jason/Projects/clawdbot-explore/SETUP_NOTES.md`). This is the most robust self-hosted option:

- LXC containers are lightweight (256MB-1GB RAM)
- Always-on if the Proxmox host is always-on
- Can mount `~/Projects/` from the host into the container via bind mount
- Docker nesting supported for sandboxing

### Option C: VPS (e.g., Hetzner, DigitalOcean, Contabo)

**Pros**:
- Always available, even if home internet or desktop is down
- Can be in a nearby data centre (Hetzner has a Johannesburg location)

**Cons**:
- Monthly cost (from ~$4-6/month for a small VPS)
- Project files need to be synced or accessed remotely (rsync, SSHFS, Syncthing)
- Adds complexity for file management

### Option D: Hybrid (Desktop + VPS Fallback)

Run the bot on the desktop as primary. Use a lightweight health-check on a cheap VPS that can notify Jason if the desktop bot goes offline. Or use Tailscale to create a mesh network so the VPS can access the desktop's filesystem.

### Recommendation

**Option B (Proxmox LXC) is best** if Jason has a server that stays on. If his Proxmox host is his desktop (and goes off when he leaves for site visits), then **Option A with Tailscale** or a simple **keep-alive approach** (Wake-on-LAN, disabling sleep) is practical. A VPS is only needed if reliable always-on connectivity from the home network cannot be guaranteed.

---

## 5. Photo/File Handling

### Receiving Photos via Telegram

When a user sends a photo to a Telegram bot, the API provides:
- Multiple resolution versions (thumbnail to full-size)
- A `file_id` for each resolution
- The bot downloads the file using `getFile` + `file_id`, then saves it locally

Using `python-telegram-bot`, the flow is:
1. User sends photo with caption like "fairfield-water site panel"
2. Bot receives update with `message.photo[-1]` (highest resolution)
3. Bot calls `photo.get_file()` then `file.download_to_drive(custom_path="/home/jason/Projects/fairfield-water/pics/2026-02-07-site-panel.jpg")`

### Routing to the Correct Project

The bot needs to know which project context the user is in. Options:
- **Active project state**: User sets current project with a command like `/project fairfield-water`, and all subsequent photos go to that project's `pics/` folder
- **Caption parsing**: Parse the photo caption for project name keywords
- **AI routing**: Send the caption to Claude and ask it to determine the correct project folder
- **Fuzzy matching**: Match partial names ("fairfield" maps to `fairfield-water/`)

### File Naming Convention

Based on Jason's existing conventions in `CLAUDE.md`, photos should follow:
```
pics/YYYY-MM-DD-description.jpg
```

### WiFi Scan Results / Technical Data

Text-based technical data (WiFi scan results, IP addresses, serial numbers) can be:
1. Sent as text messages -- bot parses and files them
2. Sent as file attachments -- bot saves to the project's `docs/` folder
3. Dictated as voice -- transcribed and saved

---

## 6. Voice-to-Text

### Telegram's Built-in Transcription

Telegram Premium offers voice-to-text transcription (launched 2025), but:
- Only available to Telegram Premium subscribers
- Limited language support (English, Spanish, German, French, Italian, Portuguese, Korean, Thai as of late 2025)
- 30-minute maximum per message
- **Not accessible via the Bot API** -- the transcription happens client-side

### OpenAI Whisper (Recommended Approach)

[OpenAI Whisper](https://github.com/openai/whisper) is open-source and can be self-hosted:

**Self-hosted (local)**:
```python
import whisper
model = whisper.load_model("turbo")  # or "base", "small", "medium", "large-v3"
result = model.transcribe("voice_message.ogg")
text = result["text"]
```

- The `turbo` model is optimized for speed with minimal accuracy loss
- The `base` model runs well on CPU (no GPU needed) and is adequate for clear speech
- Requires Python 3.8-3.11, PyTorch, and `pip install openai-whisper`

**Via OpenAI API** (cloud):
- Send the audio file to `api.openai.com/v1/audio/transcriptions`
- Cost: $0.006 per minute of audio
- No local GPU needed

**Workflow**:
1. User sends voice message to Telegram bot
2. Bot downloads the OGG/OPUS audio file
3. Bot sends to Whisper (local or API) for transcription
4. Transcribed text is saved to `correspondence/YYYY-MM-DD_voice-note.md`
5. Bot confirms: "Transcribed and saved to fairfield-water/correspondence/"

The `claude-telegram-bridge` project already implements this exact flow with Whisper API integration.

### Sources
- [OpenAI Whisper on GitHub](https://github.com/openai/whisper)
- [Telegram Bot for Transcribing Voice](https://github.com/soberhacker/telegram-speech-recognition-bot)
- [n8n Workflow: Transcribe Telegram Voice Messages with Whisper](https://n8n.io/workflows/4528-transcribe-voice-messages-from-telegram-using-openai-whisper-1/)

---

## 7. Security Considerations

### Telegram Encryption Limitations

**Critical**: Telegram bot conversations are **NOT end-to-end encrypted**. Telegram's E2EE (Secret Chats) is only available between human users, not with bots. Bot messages are encrypted in transit (TLS) and at rest on Telegram's servers, but Telegram can theoretically read them.

This means:
- Passwords, credentials, and sensitive client data sent to the bot could be visible to Telegram
- This is the same security model as email -- encrypted in transit but not end-to-end
- For Jason's use case (querying project files, sending photos), this is generally acceptable
- Sensitive credentials should be handled carefully -- perhaps the bot should redact or refuse to display passwords

### Signal Security

Signal provides E2EE for all messages, including to bots (since bots are just registered phone numbers). This is Signal's primary advantage. However, the unofficial nature of signal-cli means security depends on the implementation quality of community tools.

### API Token Management

| Secret | Storage Recommendation |
|--------|----------------------|
| Telegram Bot Token | `.env` file with `chmod 600`, never committed to git |
| Claude API Key | `.env` file with `chmod 600`, never committed to git |
| OpenAI API Key (for Whisper) | `.env` file with `chmod 600`, never committed to git |
| Allowed User IDs | Hardcoded whitelist in config (Telegram user IDs are numeric) |

### Access Control

Best practices for a personal bot:
1. **Whitelist Jason's Telegram user ID** -- reject all messages from unknown users
2. **Optional token-based auth** -- require a password on first connection
3. **Rate limiting** -- prevent abuse even from whitelisted users (protects Claude API costs)
4. **Command restrictions** -- limit which directories the bot can access
5. **No shell execution** -- the bot should only read/write files in `~/Projects/`, never execute arbitrary commands (unless using a sandboxed solution like OpenClaw)

### Practical Assessment

For a single-user personal bot running on Jason's own machine:
- Telegram's lack of E2EE is a manageable risk -- the convenience far outweighs the theoretical exposure
- The main security priorities are: protecting API tokens, whitelisting the user, and preventing the bot from being a vector for unauthorized file access
- Do not send client passwords or financial details through the bot as plaintext

### Sources
- [Telegram Bot Security Best Practices](https://alexhost.com/faq/what-are-the-best-practices-for-building-secure-telegram-bots/)
- [Telegram E2EE Documentation](https://core.telegram.org/api/end-to-end)
- [GitGuardian: Remediating Telegram Bot Token Leaks](https://www.gitguardian.com/remediation/telegram-bot-token)

---

## 8. Existing Open-Source Projects

### Tier 1: Directly Relevant (Claude + Telegram + Project Access)

| Project | Stars | Description | Fit for Jason |
|---------|-------|-------------|---------------|
| [claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram) | Active | Remote Claude Code access via Telegram with directory navigation and session persistence | **Excellent** -- almost exactly what Jason needs |
| [claude-telegram-bridge](https://github.com/viniciustodesco/claude-telegram-bridge) | Active | Claude Code + Telegram with Whisper transcription and image vision | **Excellent** -- adds voice and image support |
| [OpenClaw](https://github.com/openclaw/openclaw) | 145K+ | Full-featured self-hosted AI agent with multi-channel support | **Very good** -- more than needed but Jason has already explored it |
| [Claude-Code-Remote](https://github.com/JessyTsui/Claude-Code-Remote) | Active | Control Claude Code via email, Discord, or Telegram | **Good** -- multi-channel remote access |

### Tier 2: Useful Components

| Project | Description |
|---------|-------------|
| [telegram-claude](https://github.com/grorge123/telegram-claude) | Simple Claude Telegram bot with BYO API key |
| [TSGram-MCP](https://github.com/areweai/tsgram-mcp) | Telegram MCP server for Claude Code integration |
| [signal-mcp-client](https://github.com/piebro/signal-mcp-client) | MCP client using Signal as transport |
| [claude-telegram-relay](https://github.com/godagoo/claude-telegram-relay) | Minimal daemon pattern for Claude + Telegram |
| [claude-code-telegram-gcp](https://github.com/stebou/claude-code-telegram-gcp) | GCP-hosted variant |

### Tier 3: Signal-Specific

| Project | Description |
|---------|-------------|
| [signal-ai-chat-bot](https://github.com/piebro/signal-ai-chat-bot) | AI chatbot for Signal (uses Gemini, but adaptable) |
| [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | Dockerized REST API for Signal |
| [signalbot](https://pypi.org/project/signalbot/) | Python framework for Signal bots |

---

## 9. MCP Servers for Telegram and Signal

### Telegram MCP Servers

Multiple MCP servers exist for Telegram, which could allow Claude Code to interact with Telegram as a tool:

| Project | Transport | Capabilities |
|---------|-----------|-------------|
| [mcp-telegram (sparfenyuk)](https://github.com/sparfenyuk/mcp-telegram) | MTProto | Read-only Telegram access |
| [telegram-mcp (chigwell)](https://github.com/chigwell/telegram-mcp) | MTProto/Telethon | Full CRUD: send/edit/delete messages, manage groups, download media |
| [mcp-telegram (dryeab)](https://github.com/dryeab/mcp-telegram) | MTProto/Telethon | Send/edit/delete, search chats, manage drafts, download media |
| [TSGram-MCP](https://github.com/areweai/tsgram-mcp) | Bot API | Claude Code integration, TypeScript |
| [mcp-communicator-telegram](https://github.com/qpd-v/mcp-communicator-telegram) | Bot API | Bidirectional: ask questions to user and receive responses via Telegram |

### Signal MCP

| Project | Description |
|---------|-------------|
| [signal-mcp-client](https://github.com/piebro/signal-mcp-client) | MCP **client** (not server) that uses Signal as the messaging transport |
| [signal-mcp](https://github.com/rymurr/signal-mcp) | MCP server for Signal (less documented) |

### How MCP Fits This Use Case

There are two ways MCP could be used:

1. **MCP Server approach** (e.g., `mcp-communicator-telegram`): Claude Code on the desktop has a Telegram MCP server configured. When Claude needs to ask Jason a question or send him a notification, it uses the MCP tool to message him on Telegram. This is **Claude-initiated** communication.

2. **MCP Client approach** (e.g., `signal-mcp-client`): The messaging bot acts as an MCP client, connecting to MCP servers (filesystem, project management tools). When Jason sends a message, the bot uses MCP tools to read files, update STATUS.md, etc. This is **user-initiated** communication.

For Jason's use case, approach 2 is more relevant -- the bot needs to access project files when Jason asks questions.

### Sources
- [mcp-communicator-telegram on PulseMCP](https://www.pulsemcp.com/servers/qpd-v-telegram-communicator)
- [Telegram MCP (sparfenyuk) on PulseMCP](https://www.pulsemcp.com/servers/sparfenyuk-telegram)

---

## 10. n8n Workflows

### What n8n Offers

[n8n](https://n8n.io/) is an open-source workflow automation platform that can bridge Telegram and other systems. It has native nodes for:
- **Telegram** (trigger on messages, send messages, send photos)
- **Claude/Anthropic** (send prompts, receive responses)
- **Filesystem** (read/write files)
- **HTTP/Webhook** (custom integrations)
- **Code** (run JavaScript/Python for custom logic)

### Relevant n8n Templates

| Template | Description |
|----------|-------------|
| [Telegram Bot Starter + AI Agent](https://n8n.io/workflows/2402-telegram-bot-starter-template-setup-and-ai-agent-chatbot/) | Foundation for a Telegram bot with AI agent backend |
| [Transcribe Telegram Voice with Whisper](https://n8n.io/workflows/4528-transcribe-voice-messages-from-telegram-using-openai-whisper-1/) | Receives voice messages, transcribes with Whisper-1, returns text |
| [AI Telegram Bot Agent](https://n8n.io/workflows/4457-ai-telegram-bot-agent-smart-assistant-and-content-summarizer/) | Smart assistant with content summarization |

### Self-Hosted n8n + Telegram

A [documented approach](https://github.com/flatmarstheory/selfhosted-n8n-telegram-bot) runs n8n in Docker on an Ubuntu VM with ngrok for webhook tunneling. However, **polling mode eliminates the need for ngrok** since n8n's Telegram trigger supports both webhook and polling modes.

### n8n Architecture for Jason's Use Case

```
Phone (Telegram) --> Telegram servers --> n8n (self-hosted)
                                            |
                                            +--> Claude API (for AI responses)
                                            +--> Local filesystem (read/write ~/Projects/)
                                            +--> Whisper API (voice transcription)
```

### Pros and Cons of n8n

**Pros**:
- Visual workflow builder -- easy to modify routing logic
- No coding required for basic flows
- Built-in Telegram + Claude nodes
- Can handle photo downloads, file routing, and status updates via visual workflows
- Self-hosted (Docker) -- free, runs on Jason's machine

**Cons**:
- Adds another service to maintain (n8n itself)
- Less flexible than code for complex context management (session persistence, multi-turn conversations)
- Webhook mode requires a public URL; polling mode is less responsive
- The visual approach becomes unwieldy for complex logic (project fuzzy matching, context assembly)
- Only one Telegram webhook per n8n instance

### Verdict on n8n

n8n is a good option **if Jason wants a no-code approach** and doesn't need sophisticated multi-turn conversations. For the full vision (session persistence, project context, multi-turn Claude conversations with project file awareness), a dedicated bot application (like `claude-code-telegram` or `claude-telegram-bridge`) is more capable. n8n could serve as a useful **complement** -- for example, handling photo routing and voice transcription in a workflow that feeds into the main bot.

### Sources
- [Claude and Telegram Integration on n8n](https://n8n.io/integrations/claude/and/telegram/)
- [Self-hosted n8n Telegram Bot](https://github.com/flatmarstheory/selfhosted-n8n-telegram-bot)
- [How to Build a Telegram AI Bot with n8n](https://blog.elest.io/how-to-build-a-telegram-ai-bot-with-n8n/)

---

## Telegram vs Signal: Head-to-Head Comparison

| Criterion | Telegram | Signal | Winner |
|-----------|----------|--------|--------|
| **Official Bot API** | Yes -- mature, well-documented, actively maintained | No -- community tools only (signal-cli) | Telegram |
| **Setup Complexity** | 2 minutes (talk to @BotFather) | 30-60 minutes (register phone, Docker, signal-cli) | Telegram |
| **Photo Handling** | Excellent -- multiple resolutions, `file_id` system, easy download | Works via attachments, less polished API | Telegram |
| **Voice Messages** | Native support, OGG/OPUS format, easy to download | Supported as attachments | Telegram |
| **File Size Limits** | 50MB (2GB with self-hosted API server) | No documented limit via signal-cli | Tie |
| **Message Delivery** | Webhooks (instant) or polling | Polling only (signal-cli) | Telegram |
| **End-to-End Encryption** | No (bot chats use server-side encryption only) | Yes (all messages E2EE) | Signal |
| **Session/State Management** | Rich API with inline keyboards, commands, callbacks | Basic text messages only | Telegram |
| **Group Chat Support** | Excellent -- bots work in groups, channels | Possible but awkward via signal-cli | Telegram |
| **Rich UI Elements** | Inline keyboards, reply markup, web apps | Plain text only | Telegram |
| **Ecosystem / Community** | Massive -- thousands of bot libraries and examples | Small -- handful of projects | Telegram |
| **Reliability** | Very high -- Telegram's infrastructure is global | Depends on signal-cli stability and registration | Telegram |
| **MCP Support** | Multiple MCP servers available | One MCP client, one early-stage server | Telegram |
| **Multi-device** | Full sync across all devices | Full sync (Signal's current protocol supports this) | Tie |
| **South Africa Availability** | Widely used | Less common but available | Telegram |

**Verdict**: Telegram wins 11 out of 14 categories. Signal's sole advantage is end-to-end encryption, which matters for highly sensitive communications but is not critical for querying project status or filing photos. For a self-hosted bot that runs on your own machine and communicates with your own AI API, the Telegram security model is acceptable.

---

## Recommended Architecture

### Primary Recommendation: claude-code-telegram or claude-telegram-bridge

For Jason's specific needs, starting with one of the purpose-built projects is the fastest path:

```
+------------------+        +-------------------+        +------------------+
|  Jason's Phone   |  <-->  | Telegram Servers  |  <-->  | Jason's Desktop  |
|  (Telegram App)  |        | (cloud, free)     |        | or Proxmox LXC   |
+------------------+        +-------------------+        +------------------+
                                                                  |
                                                         +--------+--------+
                                                         |                 |
                                                    Bot Service      ~/Projects/
                                                         |           (local fs)
                                                   +-----+-----+
                                                   |           |
                                              Claude API   Whisper
                                              (Anthropic)  (local or
                                                            OpenAI API)
```

### How Each Requirement Maps

| Requirement | How It Works |
|-------------|-------------|
| **Query project files** | Bot uses `/cd fairfield-water` to set context, then Claude reads CLAUDE.md, STATUS.md, README.md and answers questions |
| **Send photos** | Bot receives photo + caption, saves to `~/Projects/{active-project}/pics/YYYY-MM-DD-{caption}.jpg` |
| **Send WiFi scans / technical data** | Bot receives text or file, saves to `~/Projects/{active-project}/docs/` |
| **Dictate notes** | Bot receives voice message, transcribes via Whisper, saves to `~/Projects/{active-project}/correspondence/YYYY-MM-DD_voice-note.md` |
| **AI assistance** | Bot sends message + project context to Claude API, returns response |
| **Update project status** | User says "Mark site visit as complete", bot instructs Claude to update STATUS.md |

### Component Selection

| Component | Recommendation | Reason |
|-----------|---------------|--------|
| **Messaging Platform** | Telegram | Superior bot API, richer UI, easier setup |
| **Bot Framework** | Start with `claude-telegram-bridge` | Has vision, voice transcription, and streaming built in |
| **AI Backend** | Claude API (Anthropic) | Direct API access, consistent with Claude Code usage |
| **Voice Transcription** | OpenAI Whisper API (or local Whisper `base` model) | Reliable, affordable, multilingual |
| **Hosting** | Jason's desktop via `systemd` (or Proxmox LXC if available) | Direct filesystem access, no sync needed |
| **Project Routing** | Fuzzy matching on project folder names + active project state | User sets context with `/project fairfield` |

### Alternative: OpenClaw

If Jason wants the full-featured multi-channel agent, OpenClaw (which he has already researched) supports all of this and more. The trade-off is greater complexity and resource usage. His existing setup notes at `/home/jason/Projects/clawdbot-explore/SETUP_NOTES.md` already document a Proxmox LXC deployment plan that would work well. OpenClaw's advantage is that it could also serve as a general-purpose AI assistant beyond just project management.

### Estimated Costs

| Item | Cost |
|------|------|
| Telegram bot | Free |
| Claude API (Sonnet, ~50-100 queries/day with project context) | ~$10-30/month |
| Whisper API (5-10 voice messages/day, ~1 min each) | ~$1/month |
| VPS (if needed) | $4-10/month |
| Self-hosted Whisper (local) | Free (but needs ~1GB RAM) |
| **Total (self-hosted, cloud APIs)** | **~$11-31/month** |

### Next Steps

1. Create a Telegram bot via @BotFather (takes 2 minutes)
2. Clone `claude-telegram-bridge` or `claude-code-telegram`
3. Configure with Telegram bot token, Claude API key, and whitelisted user ID
4. Add custom handlers for photo filing, voice transcription, and project routing
5. Set up as a `systemd` service for auto-start
6. Test the workflow: query a project, send a photo, dictate a note, update status
7. Iterate on project routing logic and Claude system prompts for project-aware responses
