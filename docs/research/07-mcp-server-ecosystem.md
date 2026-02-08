---

# MCP Server Ecosystem Research Report

## For a Small IT Services Business Using Claude Code on Linux

---

## 1. What is MCP?

The **Model Context Protocol (MCP)** is an open protocol introduced by Anthropic in November 2024 that standardizes how AI systems (LLMs) integrate with external tools, data sources, and services. It uses a **client-server architecture** transported over **JSON-RPC 2.0**, borrowing concepts from the Language Server Protocol (LSP).

**Key concepts:**

- **Host**: The application the user interacts with (e.g., Claude Code CLI)
- **Client**: Lives inside the host; manages the connection to one MCP server
- **Server**: An external program exposing **Tools** (actions with side effects), **Resources** (read-only data retrieval), and **Prompts** (reusable templates)

When Claude Code starts, it spawns configured MCP servers as child processes (via stdio transport) or connects to remote HTTP endpoints. A handshake exchanges capabilities, and then Claude gains access to the server's tools, which appear as callable functions in the conversation.

**Governance**: In December 2025, Anthropic donated MCP to the **Agentic AI Foundation (AAIF)** under the Linux Foundation, co-founded by Anthropic, Block, and OpenAI.

---

## 2. MCP Server Registries and Discovery

| Registry | URL | Notes |
|----------|-----|-------|
| **Official MCP Registry** | https://registry.modelcontextprotocol.io | Launched September 2025. Community-owned, backed by Anthropic, GitHub, Microsoft, PulseMCP. Metadata catalog (not binaries). |
| **Official Reference Servers** | https://github.com/modelcontextprotocol/servers | 76k+ stars, 223 contributors. Maintained by the MCP steering group. |
| **PulseMCP Directory** | https://www.pulsemcp.com/servers | 8,250+ servers indexed, updated daily. |
| **Awesome MCP Servers** | https://mcp-awesome.com | 1,200+ quality-verified servers. Curated community list. |
| **punkpeye/awesome-mcp-servers** | https://github.com/punkpeye/awesome-mcp-servers | GitHub-based curated collection. |
| **Glama MCP Directory** | https://glama.ai/mcp/servers | Categorized directory with quality assessments. |
| **Smithery** | https://smithery.ai | MCP server marketplace with one-click installs. |

---

## 3. Google Workspace MCP Servers

### 3a. Google Official (Remote, Managed)

Google announced fully-managed remote MCP servers (updated 2026-02-05) covering **Docs, Sheets, Slides, Calendar, and Gmail**. These are enterprise-grade endpoints with MCP-spec-compliant OAuth, IAM controls, and organizational policies.

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/google/mcp |
| **Type** | Official, remote MCP servers |
| **Auth** | OAuth 2.1, IAM-based fine-grained authorization |
| **Services** | Gmail, Calendar, Docs, Sheets, Slides (more coming) |
| **Docs** | https://docs.google.com/cloud/mcp/overview |
| **Verdict** | Best for enterprise/Google Cloud users. May require a Google Cloud project. Most secure and well-maintained option long-term. |

### 3b. taylorwilsdon/google_workspace_mcp (Community -- Top Pick)

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/taylorwilsdon/google_workspace_mcp |
| **Stars** | ~1,300 |
| **Forks** | ~173 |
| **Last Active** | January 2026 (issues #372, #382 filed Jan 2026) |
| **Language** | Python |
| **Services** | Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat, Forms, Tasks, Contacts, Search |
| **Auth** | OAuth 2.1 with multi-user support |
| **Tools Exposed** | ~10 tools (version 1.4.3) |
| **Known Issues** | OAuth discovery issues with Claude Code (issue #382); multi-account credential handling (issue #372) |
| **Quality Rating** | HIGH -- Most comprehensive community server. Active development, large user base. |

### 3c. MarkusPfundstein/mcp-gsuite

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/MarkusPfundstein/mcp-gsuite |
| **Stars** | ~428 |
| **Forks** | ~85 |
| **Language** | Python (requires >=3.13) |
| **Services** | Gmail, Calendar, Docs, Sheets, Slides |
| **Auth** | OAuth 2.0, multi-account support |
| **Quality Rating** | MEDIUM-HIGH -- Solid alternative. Smaller community but well-documented. |

### 3d. aaronsb/google-workspace-mcp

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/aaronsb/google-workspace-mcp |
| **Stars** | ~107 |
| **Last Updated** | October 2025 |
| **Services** | Gmail, Calendar, Drive |
| **Auth** | OAuth 2.0 with automatic token refresh |
| **Quality Rating** | MEDIUM -- Covers the basics. Less comprehensive, less active. |

### 3e. ngs/google-mcp-server

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/ngs/google-mcp-server |
| **Services** | Calendar, Drive, Gmail, Sheets, Docs, Slides |
| **Quality Rating** | MEDIUM -- Another reasonable option for unified Workspace access. |

### Google Workspace Recommendation

For a small IT services business, **taylorwilsdon/google_workspace_mcp** is the best community option due to its breadth (10 services), active development, and large user base. Watch the **Google official remote MCP servers** (google/mcp) as they mature -- they will likely become the gold standard due to official support, enterprise auth, and no self-hosting burden.

---

## 4. Messaging MCP Servers

### 4a. Telegram

| Server | Stars | Features | Transport | Quality |
|--------|-------|----------|-----------|---------|
| **chigwell/telegram-mcp** | ~657 | Full read/write: send/edit/delete messages, media, contacts, group management, settings. Powered by Telethon (Python). | stdio | HIGH -- Most feature-complete |
| **sparfenyuk/mcp-telegram** | ~163 | Read-only via MTProto. Listing dialogs and messages. Focus on security. | stdio | MEDIUM -- Good for read-only/monitoring |
| **chaindead/telegram-mcp** | N/A | Dialogs, messages, drafts, read status. TypeScript (npm package `@chaindead/telegram-mcp`). | stdio | MEDIUM -- Good TypeScript alternative |

**Telegram Recommendation**: Use **chigwell/telegram-mcp** for full Telegram control (sending messages, managing groups). Use **sparfenyuk/mcp-telegram** if you only need to read/monitor channels safely.

**Important**: All Telegram MCP servers use the **user client API** (MTProto via Telethon), not the Bot API. This means they authenticate as your personal Telegram account, which gives full access but carries the risk of Telegram flagging the account for automated use.

### 4b. WhatsApp

| Server | Stars | Features | Architecture | Quality |
|--------|-------|----------|--------------|---------|
| **lharries/whatsapp-mcp** | N/A (popular) | Search/read messages (text, images, video, audio, docs), search contacts, send messages to individuals/groups. | Go bridge (whatsmeow) + Python MCP server. Messages stored in local SQLite. | HIGH -- Most mature, well-architected |
| **jlucaso1/whatsapp-mcp-ts** | N/A | TypeScript with Baileys library. SQLite storage. Stdio transport. | TypeScript, all-in-one | MEDIUM |
| **FelixIsaac/whatsapp-mcp-extended** | N/A | Extended fork of lharries with **41 tools**: reactions, message editing, polls, newsletters, group management, webhooks. | Go bridge + Python | MEDIUM-HIGH -- Most tools, but fork stability unclear |
| **msaelices/whatsapp-mcp-server** | N/A | Python implementation via GreenAPI (third-party service). | Python | LOW-MEDIUM -- Depends on paid third-party service |

**WhatsApp Recommendation**: **lharries/whatsapp-mcp** is the safest bet -- well-architected with a Go bridge handling WhatsApp Web's protocol and a separate Python MCP server. Requires QR code authentication (like WhatsApp Web). Both the Go bridge and Python server must run simultaneously. Consider **whatsapp-mcp-extended** if you need advanced features like polls or reactions.

**Warning**: WhatsApp's terms of service prohibit unofficial API usage. These servers use the WhatsApp Web multi-device API via reverse-engineered libraries (whatsmeow/Baileys). There is a risk of account suspension. Use with caution for business-critical communications.

### 4c. Signal

| Server | Stars | Features | Quality |
|--------|-------|----------|---------|
| **rymurr/signal-mcp** | ~18 | Send messages to users and groups via signal-cli. Requires signal-cli installed and configured. Python. | LOW-MEDIUM -- Very early stage, minimal features, small community |
| **stefanstranger/signal-mcp-server** | N/A | Read-only access to Signal Desktop's local database. List chats, retrieve messages and attachments. | LOW -- Read-only, limited utility |

**Signal Recommendation**: The Signal MCP ecosystem is **immature**. rymurr/signal-mcp is the only option with send capability, but at 18 stars it is very early-stage. It requires **signal-cli** (a Java-based CLI for Signal) to be installed and registered. This is usable but expect rough edges.

---

## 5. Utility MCP Servers

### 5a. Official Reference Servers (from modelcontextprotocol/servers)

These are maintained by the MCP steering group (76k+ stars on the parent repo). They are the gold standard for reliability.

| Server | Package | Description | Quality |
|--------|---------|-------------|---------|
| **Filesystem** | `@modelcontextprotocol/server-filesystem` | Secure file operations (read/write/create/list/move) with configurable directory access controls. Node.js. | OFFICIAL -- HIGH |
| **Fetch** | `@modelcontextprotocol/server-fetch` | Fetches web URLs, converts HTML to markdown for LLM consumption. | OFFICIAL -- HIGH |
| **Git** | `mcp-server-git` | Read, search, manipulate Git repos. Inspect branches, diffs, logs, files. Python. | OFFICIAL -- HIGH |
| **Memory** | `@modelcontextprotocol/server-memory` | Knowledge graph-based persistent memory system. | OFFICIAL -- HIGH |
| **Sequential Thinking** | `@modelcontextprotocol/server-sequential-thinking` | Dynamic, reflective problem-solving through thought sequences. | OFFICIAL -- HIGH |
| **Everything** | `@modelcontextprotocol/server-everything` | Reference/test server demonstrating all MCP capabilities. | OFFICIAL -- For testing |

### 5b. GitHub Official MCP Server

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/github/github-mcp-server |
| **Stars** | ~26,400 |
| **Last Updated** | January 28, 2026 |
| **Features** | Issues, PRs, repos, code search, Projects management, Copilot integration, OAuth scope filtering |
| **Quality Rating** | OFFICIAL -- VERY HIGH |

### 5c. Desktop Commander

| Detail | Value |
|--------|-------|
| **Repository** | https://github.com/wonderwhy-er/DesktopCommanderMCP |
| **Features** | Terminal execution (with timeout/background), file operations, process management (list/kill PIDs), code editing with surgical replacements, in-memory code execution (Python/Node.js/R), native Excel and PDF support |
| **Quality Rating** | HIGH -- Very popular, actively maintained. Essentially a "supercharged filesystem + terminal" server. |

**Note**: For Claude Code specifically, many Desktop Commander features are redundant since Claude Code already has built-in terminal and file access. It is more useful for Claude Desktop.

### 5d. Image Handling

| Server | Description | Quality |
|--------|-------------|---------|
| **IA-Programming/mcp-images** | Enterprise-grade image processing (resize, crop, format conversion). | MEDIUM |
| **GongRzhe/opencv-mcp-server** | OpenCV-based: manipulation, object detection, tracking. | MEDIUM |
| **omidsrezai/cv-tools** | Computer vision tools: resizing, cropping, OCR text extraction. | MEDIUM |
| **catalystneuro/mcp_read_images** | Read images via OpenRouter vision models. Auto-resize, custom queries. | MEDIUM |

**Image Recommendation**: The image MCP ecosystem is fragmented with many small projects. For basic needs (reading screenshots, extracting text), Claude Code's built-in multimodal capabilities may suffice without a dedicated MCP server. Use **opencv-mcp-server** if you need programmatic image manipulation.

---

## 6. Quality Assessment Summary

| Server | Stars | Official? | Last Active | Auth Method | Recommendation |
|--------|-------|-----------|-------------|-------------|----------------|
| modelcontextprotocol/servers (reference) | 76k | Yes (Anthropic) | Dec 2025 | N/A | MUST HAVE |
| github/github-mcp-server | 26.4k | Yes (GitHub) | Jan 2026 | PAT / OAuth | MUST HAVE |
| google/mcp (official) | N/A | Yes (Google) | Feb 2026 | OAuth 2.1 / IAM | ADOPT when stable |
| taylorwilsdon/google_workspace_mcp | 1.3k | Community | Jan 2026 | OAuth 2.1 | ADOPT now |
| MarkusPfundstein/mcp-gsuite | 428 | Community | 2025 | OAuth 2.0 | ALTERNATIVE |
| chigwell/telegram-mcp | 657 | Community | 2026 | MTProto API keys | ADOPT with caution |
| lharries/whatsapp-mcp | Popular | Community | Active | QR code (WhatsApp Web) | ADOPT with caution (ToS risk) |
| rymurr/signal-mcp | 18 | Community | Apr 2025 | signal-cli registration | EXPERIMENTAL |
| wonderwhy-er/DesktopCommanderMCP | Popular | Community | Active | None (local) | OPTIONAL for Claude Code |

---

## 7. How to Configure MCP in Claude Code

### Configuration Locations

| Scope | File Location | Purpose |
|-------|---------------|---------|
| **User** (all projects) | `~/.claude.json` | Your personal MCP servers, available everywhere |
| **Project** (shared) | `.mcp.json` in project root | Shared with team via version control |
| **Local** (default) | `.claude/` directory | Only for you, only in this project |

### CLI Commands

```bash
# Add a server (user scope, available everywhere)
claude mcp add --scope user --transport stdio my-server -- npx @some/mcp-server

# Add with environment variables
claude mcp add --scope user --transport stdio --env API_KEY=xxx my-server -- node /path/to/server.js

# Add from JSON (useful for complex configs)
claude mcp add-json "google-workspace" '{"type":"stdio","command":"npx","args":["google-workspace-mcp"]}'

# List configured servers
claude mcp list

# Get details for a server
claude mcp get my-server

# Remove a server
claude mcp remove my-server
```

**Important**: All options (`--transport`, `--env`, `--scope`) must come **before** the server name.

### Direct JSON Configuration

The `~/.claude.json` file uses this structure:

```json
{
  "projects": {
    "/home/jason/Projects": {
      "mcpServers": {
        "filesystem": {
          "type": "stdio",
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/jason/Projects"]
        },
        "fetch": {
          "type": "stdio",
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-fetch"]
        }
      }
    }
  }
}
```

For remote/HTTP servers:
```json
{
  "type": "http",
  "url": "https://some-remote-mcp-server.example.com/mcp"
}
```

**After any configuration change, restart Claude Code** for changes to take effect.

---

## 8. Self-Hosting Considerations

**How MCP servers run locally with Claude Code:**

- **stdio transport** (most common for local): Claude Code spawns the MCP server as a **child process** when it starts. The server communicates via stdin/stdout. When Claude Code exits, the child process is terminated. **No always-on daemon needed.**

- **HTTP/SSE transport** (for remote or persistent servers): The server runs independently (as a daemon, Docker container, or cloud service). Claude Code connects to it via URL. This **does** require an always-on service if you want persistent availability.

**Practical implications for Jason:**

- Most MCP servers (filesystem, git, fetch, Google Workspace, Telegram) use stdio and are spawned on-demand. No background services needed.
- **WhatsApp MCP (lharries)** is an exception: the Go bridge must remain running to maintain the WhatsApp Web session. If it stops, you lose the session and must re-authenticate via QR code.
- **Signal MCP** requires signal-cli to be installed (Java dependency).
- Node.js-based servers require Node.js/npx. Python-based servers require Python/uv/pip.

**Docker option**: Many servers can be run in Docker containers for isolation. The Docker MCP Toolkit simplifies adding containerized MCP servers to Claude Code.

---

## 9. Security

### Credential Handling by Transport Type

| Method | How Credentials Work | Risk Level |
|--------|---------------------|------------|
| **Environment variables** | Passed via `--env` flag or `env` object in config. Stored in `~/.claude.json` as plaintext. | MEDIUM -- file permissions matter |
| **OAuth 2.0/2.1** | Browser-based auth flow. Tokens stored in system keychain or credentials file. | LOWER -- tokens rotate, scoped |
| **API keys in env** | Static, long-lived. 79% of MCP servers use this pattern. | HIGHER -- if leaked, persistent access |

### Critical Security Findings (from Astrix Security research, 2025)

- 88% of MCP servers require credentials
- 53% rely on **insecure, long-lived static secrets** (API keys, PATs)
- 79% of API keys are passed via **simple environment variables**
- Only 8.5% use modern auth methods like OAuth
- A scan of ~2,000 public MCP servers found **all verified servers lacked authentication** (meaning anyone could access tool listings)

### Best Practices

1. **Never hardcode secrets** in MCP server code or commit them to version control
2. **Use OAuth 2.1** where available (Google Workspace servers support this)
3. **File permissions**: Ensure `~/.claude.json` is readable only by your user (`chmod 600`)
4. **Environment variable isolation**: Each MCP server process gets its own environment; servers cannot see each other's variables
5. **Consider a secrets manager**: Tools like 1Password-direnv can inject secrets at runtime without storing them in config files
6. **Restrict filesystem access**: The official filesystem server accepts directory allowlists -- use them
7. **Be cautious with .env files**: Claude Code has been reported to automatically load `.env` files. Use deny rules to block `.env` access if it contains sensitive data

### Per-Server Auth Notes

| Server | Auth Method | Notes |
|--------|-------------|-------|
| Google Workspace (taylorwilsdon) | OAuth 2.1 | Browser flow, tokens stored locally. Need to create a Google Cloud OAuth client. |
| Google Official | OAuth 2.1 + IAM | Enterprise-grade. Requires Google Cloud project. |
| Telegram (chigwell) | Telegram API ID + Hash | Get from my.telegram.org. Stored as env vars. Long-lived. |
| WhatsApp (lharries) | QR code scan | Like WhatsApp Web. Session stored locally. Expires if inactive. |
| Signal (rymurr) | signal-cli registration | Phone number + PIN. signal-cli manages the session. |
| GitHub official | Personal Access Token or OAuth | PAT stored as env var. OAuth available for remote mode. |

---

## 10. Practical Recommendations for Jason

### Tier 1: Adopt Now (Low Risk, High Value)

1. **Official Fetch server** (`@modelcontextprotocol/server-fetch`) -- Web content retrieval. Useful for researching client issues, reading documentation.
2. **GitHub MCP server** (`github/github-mcp-server`) -- If you manage any code on GitHub. Official, extremely well-maintained.
3. **Official Git server** (`mcp-server-git`) -- Enhanced Git operations beyond what Claude Code already provides.

### Tier 2: Adopt with Setup Effort (Medium Risk, High Value)

4. **taylorwilsdon/google_workspace_mcp** -- Gmail, Calendar, Drive, Docs, Sheets access. Requires creating a Google Cloud OAuth client and going through the consent flow. The most impactful integration for daily business operations.
5. **chigwell/telegram-mcp** -- Full Telegram control. Requires Telegram API credentials from my.telegram.org.

### Tier 3: Evaluate Carefully (Higher Risk / Less Mature)

6. **lharries/whatsapp-mcp** -- Powerful but violates WhatsApp ToS. The Go bridge must stay running. Good for personal use; risky for client-facing business communications.
7. **rymurr/signal-mcp** -- Very early stage (18 stars). Only if Signal is critical to your workflow and you accept the rough edges.

### Tier 4: Watch and Wait

8. **Google Official MCP** (google/mcp) -- Will eventually supersede community servers. Monitor for general availability and Claude Code compatibility.
9. **Image MCP servers** -- Fragmented ecosystem. Claude Code's built-in multimodal capabilities handle most image reading needs already.

### What to Skip

- **Official Filesystem server** -- Claude Code already has comprehensive file operations built in. Adding this is redundant.
- **Desktop Commander** -- Similarly redundant with Claude Code's built-in terminal and file capabilities. More useful for Claude Desktop.

---

## Sources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [Model Context Protocol - Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [MCP Reference Servers Repository](https://github.com/modelcontextprotocol/servers)
- [MCP Registry Blog Announcement](http://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)
- [Awesome MCP Servers (1200+)](https://mcp-awesome.com/)
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)
- [Configuring MCP Tools in Claude Code](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)
- [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)
- [MarkusPfundstein/mcp-gsuite](https://github.com/MarkusPfundstein/mcp-gsuite)
- [aaronsb/google-workspace-mcp](https://github.com/aaronsb/google-workspace-mcp)
- [Google Official MCP Announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services)
- [Google MCP Repository](https://github.com/google/mcp)
- [Google Cloud MCP Overview](https://docs.google.com/cloud/mcp/overview)
- [chigwell/telegram-mcp](https://github.com/chigwell/telegram-mcp)
- [sparfenyuk/mcp-telegram](https://github.com/sparfenyuk/mcp-telegram)
- [chaindead/telegram-mcp](https://github.com/chaindead/telegram-mcp)
- [lharries/whatsapp-mcp](https://github.com/lharries/whatsapp-mcp)
- [FelixIsaac/whatsapp-mcp-extended](https://github.com/FelixIsaac/whatsapp-mcp-extended)
- [rymurr/signal-mcp](https://github.com/rymurr/signal-mcp)
- [GitHub Official MCP Server](https://github.com/github/github-mcp-server)
- [Desktop Commander MCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)
- [PulseMCP Server Directory](https://www.pulsemcp.com/servers)
- [State of MCP Server Security 2025 - Astrix](https://astrix.security/learn/blog/state-of-mcp-server-security-2025/)
- [MCP Server API Key Management Best Practices - Stainless](https://www.stainless.com/mcp/mcp-server-api-key-management-best-practices)
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)
- [MCP Auth Spec Updates (Auth0)](https://auth0.com/blog/mcp-specs-update-all-about-auth/)
- [Claude Code Security & .env Loading](https://www.knostic.ai/blog/claude-loads-secrets-without-permission)
- [Best MCP Servers for 2026 - Builder.io](https://www.builder.io/blog/best-mcp-servers-2026)
- [The State of MCP in 2025 - Glama](https://glama.ai/blog/2025-12-07-the-state-of-mcp-in-2025)
