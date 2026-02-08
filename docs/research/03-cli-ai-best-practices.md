---

# Research Report: Best Practices for CLI+AI Collaborative Project Templates

## Table of Contents
1. [CLAUDE.md Conventions](#1-claudemd-conventions)
2. [AGENTS.md Standard](#2-agentsmd-standard)
3. [Copier (Python Templating Tool)](#3-copier-python-templating-tool)
4. [.claude/commands/ and Skills](#4-claudecommands-and-skills)
5. [GEMINI.md / .gemini/](#5-geminimd--gemini)
6. [AI-First Project Organization](#6-ai-first-project-organization)
7. [Project Metadata and Unified Configuration](#7-project-metadata-and-unified-configuration)
8. [Recommendations for a Small IT Services Company](#8-recommendations-for-a-small-it-services-company)
9. [Adoption Maturity Summary](#9-adoption-maturity-summary)

---

## 1. CLAUDE.md Conventions

**Status: Widely adopted, mature convention (Anthropic-official)**

CLAUDE.md is a special file that Claude Code reads at the start of every conversation. It acts as persistent memory and project-specific instructions. You can bootstrap one with the `/init` command.

### Hierarchy (loaded in order, all merged)

| Location | Scope | Version-controlled? |
|---|---|---|
| `~/.claude/CLAUDE.md` | User-global (personal prefs) | No |
| `./CLAUDE.md` | Project root (team-shared) | Yes |
| `./subdir/CLAUDE.md` | Subdirectory (loaded on demand) | Yes |
| `.claude/rules/*.md` | Modular rule files (always loaded) | Yes |
| `.claude/settings.json` | Project config (permissions, tools) | Yes |
| `.claude/settings.local.json` | Personal overrides | No (gitignored) |

### Recommended Structure for Root CLAUDE.md

Keep the root file under 300 lines (ideally 50-100). Use the `@path/to/file.md` import syntax for detailed docs.

```markdown
# Project Name

## Overview
Brief description of what this project does and its architecture.

## Build & Run Commands
- `npm run dev` - Start development server
- `npm run test` - Run test suite  
- `npm run lint` - Lint codebase

## Architecture
- `/src/api/` - API routes and handlers
- `/src/services/` - Business logic layer
- `/src/models/` - Data models and schemas
- `/infra/` - Terraform infrastructure code

## Code Style
- Use TypeScript strict mode
- Prefer named exports over default exports
- Use functional components with hooks (React)

## Testing
- Every new module requires a test file
- Use vitest for unit tests
- Integration tests go in `__tests__/integration/`

## Important Warnings
- NEVER commit .env files
- Database migrations must be reviewed by a human
- @docs/deployment-checklist.md
```

### Modular Rules via `.claude/rules/`

All markdown files in `.claude/rules/` are automatically loaded with the same priority as your main CLAUDE.md. They support YAML frontmatter with `paths` for file-pattern scoping:

```markdown
---
paths:
  - "src/api/**"
  - "src/middleware/**"
---

# API Development Rules
- All endpoints must validate input with Zod schemas
- Return consistent error response format
- Log all 5xx errors to structured logger
```

**Sources:**
- [Anthropic Official: Using CLAUDE.md Files](https://claude.com/blog/using-claude-md-files)
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Builder.io: The Complete Guide to CLAUDE.md](https://www.builder.io/blog/claude-md-guide)
- [Claude Code Docs: Manage Claude's Memory](https://code.claude.com/docs/en/memory)
- [Claude Code Docs: Best Practices](https://code.claude.com/docs/en/best-practices)
- [Gend.co: Claude Skills and CLAUDE.md 2026 Guide](https://www.gend.co/blog/claude-skills-claude-md-guide)
- [Modular Rules in Claude Code](https://claude-blog.setec.rs/blog/claude-code-rules-directory)

---

## 2. AGENTS.md Standard

**Status: Widely adopted, industry standard (multi-vendor, open format)**

AGENTS.md emerged in mid-2025 as a vendor-neutral alternative to tool-specific files (CLAUDE.md, .cursorrules, etc.). By August 2025, over 20,000 GitHub repositories had adopted it. It is now endorsed by OpenAI (Codex), Google (Gemini CLI, Jules), Sourcegraph, Factory, and ThoughtWorks (Technology Radar).

### What AGENTS.md Is

A plain Markdown file placed at the project root (or in subdirectories) that provides coding agents with project-specific context. It is explicitly designed as a complement to README.md -- containing the precise, step-by-step instructions that agents need but that would clutter a human-facing README.

### Recommended Sections

```markdown
# AGENTS.md

## Build & Commands
- Typecheck and lint: `pnpm check`
- Run all tests: `pnpm test --run --no-color`
- Run single test: `pnpm test --run path/to/test.ts`
- Start dev server: `pnpm dev` (port 3000)
- Build for production: `pnpm build`

## Architecture Overview
This is a monorepo using Turborepo with:
- `packages/core/` - Shared business logic
- `apps/web/` - Next.js frontend
- `apps/api/` - Express API server
- `infra/` - Pulumi infrastructure

## Code Style & Conventions
- Use `snake_case` for database columns, `camelCase` for JS/TS
- All async functions must have error handling
- Prefer composition over inheritance

## Testing
- Unit tests colocated with source files as `*.test.ts`
- Integration tests in `__tests__/integration/`
- Minimum 80% coverage on new code

## Git Workflow
- Branch naming: `feat/`, `fix/`, `chore/`
- Squash merge to main
- Conventional commits required

## Security & Boundaries
- Never hardcode credentials; use environment variables
- API keys stored in AWS Secrets Manager
- Do not modify files in `vendor/` or `generated/`
```

### Hierarchy

Like CLAUDE.md, AGENTS.md supports directory-level nesting. Agents read the nearest file in the directory tree, with the closest one taking precedence. A monorepo can have a root AGENTS.md plus per-package AGENTS.md files.

### Compatibility with CLAUDE.md

There are three practical strategies for projects using both:

1. **Symlink approach**: Make AGENTS.md the canonical file, create `CLAUDE.md -> AGENTS.md` symlink
2. **Reference approach**: In CLAUDE.md, add a line like `@AGENTS.md` to import it
3. **Dual-file approach**: Maintain both -- AGENTS.md for universal agent context, CLAUDE.md for Claude-specific instructions (skills, hooks, tool restrictions)

**Sources:**
- [AGENTS.md Official Site](https://agents.md/)
- [GitHub: agentsmd/agents.md](https://github.com/agentsmd/agents.md)
- [GitHub Blog: How to Write a Great AGENTS.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [ThoughtWorks Technology Radar: AGENTS.md](https://www.thoughtworks.com/en-us/radar/techniques/agents-md)
- [OpenAI: Custom Instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
- [Builder.io: Improve AI Code Output with AGENTS.md](https://www.builder.io/blog/agents-md)
- [Substratia: AGENTS.md vs CLAUDE.md](https://substratia.io/blog/agents-md-vs-claude-md/)

---

## 3. Copier (Python Templating Tool)

**Status: Mature, growing adoption; best-in-class for updatable templates**

### What Copier Does

Copier is a Python library and CLI for rendering project templates. Its distinguishing feature versus Cookiecutter is **template lifecycle management** -- projects generated from Copier templates can be updated when the template evolves. It stores a `.copier-answers.yml` file tracking which template version was used and what answers were given.

### How It Works

1. Create a template directory with a `copier.yml` (or `copier.yaml`) configuration
2. Template files use Jinja2 syntax (files ending in `.jinja` are rendered)
3. Users run `copier copy gh:org/template ./my-project` to scaffold
4. Later, `copier update` pulls in template changes while preserving local modifications

### Example `copier.yml` for a Non-Code Project

```yaml
# copier.yml
_min_copier_version: "9.0"
_subdirectory: template

project_name:
  type: str
  help: "Name of the project"

company_name:
  type: str
  default: "Acme IT Services"

project_type:
  type: str
  help: "What kind of project is this?"
  choices:
    - client-infrastructure
    - internal-tool
    - documentation
    - automation-script

use_terraform:
  type: bool
  default: false
  when: "{{ project_type == 'client-infrastructure' }}"

cloud_provider:
  type: str
  choices:
    - aws
    - azure
    - gcp
  when: "{{ use_terraform }}"

use_ci:
  type: bool
  default: true
  help: "Include GitHub Actions CI pipeline?"

include_claude_config:
  type: bool
  default: true
  help: "Include CLAUDE.md and .claude/ configuration?"
```

### Suitability for Non-Code Projects

Copier is explicitly not limited to code. It can template:
- Documentation sites
- Infrastructure-as-code projects
- Project management scaffolding (directories, config files, context files)
- Any text-based file structure

The `when` conditional means you can have a single template that adapts to different project types, only asking relevant questions.

### Copier vs Cookiecutter vs Alternatives

| Feature | Copier | Cookiecutter | Yeoman |
|---|---|---|---|
| Template updates | Yes (core feature) | No | No |
| Config format | YAML | JSON | JS |
| Conditional questions | Yes (`when`) | Limited (hooks) | Yes |
| Non-code templates | Excellent | Good | Code-focused |
| Ecosystem size | Growing | Largest | Large (JS) |
| Language | Python | Python | Node.js |

**Sources:**
- [Copier Official Documentation](https://copier.readthedocs.io/en/stable/)
- [Copier: Configuring a Template](https://copier.readthedocs.io/en/stable/configuring/)
- [Medium: From Cookiecutter to Copier, uv, and Just](https://medium.com/@gema.correa/from-cookiecutter-to-copier-uv-and-just-the-new-python-project-stack-90fb4ba247a9)
- [DEV.to: Copier vs Cookiecutter](https://dev.to/cloudnative_eng/copier-vs-cookiecutter-1jno)
- [Substack: Template Once, Update Everywhere with Copier](https://aiechoes.substack.com/p/template-once-update-everywhere-build-ab3)

---

## 4. .claude/commands/ and Skills

**Status: Widely adopted within Claude Code ecosystem; skills are the newer, richer format**

### Custom Slash Commands (Legacy but Still Supported)

Place Markdown files in `.claude/commands/` and they become slash commands:

```
.claude/
  commands/
    review.md          -> /project:review
    deploy-check.md    -> /project:deploy-check
    standup.md         -> /project:standup
    ops/
      incident.md      -> /project:ops:incident
```

User-global commands go in `~/.claude/commands/` and are available in all projects.

Commands support positional arguments via `$1`, `$2`, or `$ARGUMENTS` for all args.

#### Example: `.claude/commands/standup.md`

```markdown
Review recent git activity and summarize for standup:

1. Run `git log --oneline --since="yesterday" --author="$(git config user.name)"`
2. Check for any open PRs with `gh pr list --author=@me`
3. List any failing CI checks with `gh run list --limit=5`

Format as:
- **Yesterday**: [completed items]
- **Today**: [planned items based on open PRs/issues]
- **Blockers**: [any failing checks or blocked PRs]
```

#### Example: `.claude/commands/deploy-check.md`

```markdown
Perform pre-deployment verification:

1. Run the full test suite
2. Check for any TODO or FIXME comments in staged changes
3. Verify no .env or secret files are staged
4. Check that CHANGELOG.md has been updated
5. Summarize findings and recommend go/no-go
```

### Skills (Newer, Richer Format)

Skills are the evolution of commands. They live in `.claude/skills/` and use a `SKILL.md` file with YAML frontmatter:

```
.claude/
  skills/
    pr-summary/
      SKILL.md
    code-review/
      SKILL.md
```

#### Example: `.claude/skills/pr-summary/SKILL.md`

```markdown
---
name: pr-summary
description: Summarize changes in a pull request
allowed-tools:
  - Bash(gh *)
  - Read
---

Analyze the current PR and produce a summary:

1. Get the PR diff: `gh pr diff`
2. Get PR comments: `gh pr view --comments`
3. Summarize:
   - What changed and why
   - Risk areas
   - Testing coverage assessment
```

The `allowed-tools` frontmatter restricts which tools the skill can use, providing a security boundary. Skills can also specify `context: fork` to run in an isolated sub-agent.

### Useful Commands/Skills for Project Management

Based on community patterns:
- `/project:standup` -- daily standup summary from git history
- `/project:review` -- structured code review workflow
- `/project:deploy-check` -- pre-deployment verification
- `/project:incident` -- incident response template and checklist
- `/project:onboard` -- new team member project orientation
- `/project:changelog` -- generate changelog from commits

**Sources:**
- [Claude Code Docs: Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Claude Code Docs: Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [Anthropic Engineering: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Builder.io: How I Use Claude Code](https://www.builder.io/blog/claude-code)
- [GitHub: Claude-Command-Suite](https://github.com/qdhenry/Claude-Command-Suite)
- [motlin.com: Claude Code Workflow Commands](https://motlin.com/blog/claude-code-workflow-commands)
- [GitHub: awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

---

## 5. GEMINI.md / .gemini/

**Status: Established convention for Gemini CLI; mirrors CLAUDE.md pattern**

Google's Gemini CLI has its own parallel context file system that closely mirrors Claude Code's approach.

### File Hierarchy

| Location | Purpose |
|---|---|
| `~/.gemini/GEMINI.md` | Global context for all projects |
| `./GEMINI.md` | Project root context |
| `./subdir/GEMINI.md` | Subdirectory context |
| `~/.gemini/settings.json` | CLI configuration |

The CLI searches for context files starting from the current directory upward to the project root (identified by `.git`), then also scans subdirectories below the CWD (up to 200 directories). All found files are concatenated with path-origin separators and included in the system prompt.

### Configuration

The context filename is configurable in `settings.json` via the `context.fileName` property (defaults to `GEMINI.md`). This means you can point it at `AGENTS.md` instead:

```json
{
  "context": {
    "fileName": "AGENTS.md"
  }
}
```

### Modular Imports

GEMINI.md supports importing other Markdown files using `@path/to/file.md` syntax, identical to CLAUDE.md.

### Memory Commands

- `/memory show` -- display the full concatenated context
- `/memory refresh` -- re-scan and reload all GEMINI.md files

### Custom Tools via MCP

Gemini CLI supports custom tools through Model Context Protocol (MCP) servers configured in `~/.gemini/settings.json`. Extensions can be placed in workspace or global directories, each with a `gemini-extension.json` file.

### Dual-AI Project Structure

For projects that use both Claude Code and Gemini CLI:

```
project-root/
  AGENTS.md              # Universal agent context (primary)
  CLAUDE.md              # Claude-specific: imports AGENTS.md, adds Claude skills/hooks
  GEMINI.md              # Symlink to AGENTS.md, or Gemini-specific additions
  .claude/
    settings.json
    commands/
    skills/
    rules/
  .gemini/
    settings.json
```

The practical recommendation is to use AGENTS.md as the single source of truth for shared context, then have tool-specific files for tool-specific features (skills, hooks, tool restrictions).

**Sources:**
- [Gemini CLI Docs: Provide Context with GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)
- [Gemini CLI Docs: Configuration](https://geminicli.com/docs/get-started/configuration/)
- [GitHub: google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
- [Phil Schmid: Gemini CLI Cheatsheet](https://www.philschmid.de/gemini-cli-cheatsheet)
- [Google Codelabs: Hands-on with Gemini CLI](https://codelabs.developers.google.com/gemini-cli-hands-on)

---

## 6. AI-First Project Organization

**Status: Emerging discipline ("context engineering"); principles solidifying in 2025-2026**

### Core Principle: Vertical Slice Architecture

The most AI-friendly project structure organizes code by **feature** rather than by technical layer. Each "slice" contains all components for that feature (handler, service, model, test, docs).

**Why it works for AI agents:**
- Context isolation -- an agent working on a feature can load one directory and have everything it needs
- Reduced token consumption -- no cross-cutting jumps between distant directories
- Easier priming -- point the agent at a single feature folder
- Better for parallel agents -- multiple agents can work on different slices without conflicts

```
# Traditional (layer-based) -- poor for AI
src/
  controllers/
    user.ts
    order.ts
  services/
    user.ts
    order.ts
  models/
    user.ts
    order.ts

# AI-friendly (feature-based / vertical slice)
src/
  features/
    user/
      user.handler.ts
      user.service.ts
      user.model.ts
      user.test.ts
      CLAUDE.md          # Feature-specific AI context
    order/
      order.handler.ts
      order.service.ts
      order.model.ts
      order.test.ts
      CLAUDE.md
  shared/
    database.ts
    logger.ts
```

### Context Engineering Principles

Context engineering is the discipline of curating optimal information for each LLM call. Key strategies:

1. **Write** -- maintain external memory (CLAUDE.md, AGENTS.md, dev docs) that persists across sessions
2. **Select** -- retrieve only relevant context (use scoped rules, feature folders)
3. **Compress** -- summarize large documents; keep context files concise
4. **Isolate** -- each agent/sub-agent sees only the minimum required context

### Practical Guidelines

- **One feature per context window**: Do not ask an agent to implement multiple unrelated changes in one session
- **Colocate related files**: Tests, docs, and configs next to the code they describe
- **Use `/clear` aggressively**: Reset context between unrelated tasks
- **Living documentation**: Include CLAUDE.md changes in commits so context evolves with the code
- **Keep files small**: Smaller, focused files are easier for AI to reason about than large monoliths

### Tools for Context Packing

- [Repomix](https://repomix.com/) -- packs codebases into AI-friendly single-file formats
- [CTX Generator](https://github.com/context-hub/generator) -- organizes codebase information into structured documents for AI

**Sources:**
- [Addy Osmani: My LLM Coding Workflow Going into 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [DEV.to: Coding Agents as First-Class Consideration in Project Structures](https://dev.to/somedood/coding-agents-as-a-first-class-consideration-in-project-structures-2a6b)
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Medium: Optimizing Codebase Architecture for AI Coding Tools](https://medium.com/@richardhightower/ai-optimizing-codebase-architecture-for-ai-coding-tools-ff6bb6fdc497)
- [Promptingguide.ai: Context Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide)

---

## 7. Project Metadata and Unified Configuration

**Status: Fragmented landscape; ai-rulez is the most promising unifier**

### The Problem

Each AI coding tool has its own configuration format:
- Claude Code: `CLAUDE.md`, `.claude/settings.json`, `.claude/rules/`
- Cursor: `.cursor/rules/`, `.cursorrules`
- Windsurf: `.windsurf/rules/`
- Copilot: `.github/copilot-instructions.md`
- Gemini CLI: `GEMINI.md`, `.gemini/settings.json`
- OpenAI Codex: `AGENTS.md`

### ai-rulez: Single Source of Truth

[ai-rulez](https://github.com/Goldziher/ai-rulez) is a CLI tool that generates native configuration files for 18+ AI tools from a single YAML configuration.

**Directory structure:**

```
.ai-rulez/
  config.yaml          # Main configuration
  rules/               # Shared rules (markdown files)
    code-style.md
    testing.md
    security.md
  context/             # Project background
    architecture.md
  skills/              # Specialized AI roles
  agents/              # Agent-specific prompts
  commands/            # Slash commands
```

**Example `.ai-rulez/config.yaml`:**

```yaml
version: "2"
project: "my-project"

presets:
  - claude
  - cursor
  - windsurf
  - copilot
  - gemini
```

Running `ai-rulez generate` produces all the native config files (CLAUDE.md, .cursorrules, .windsurfrules, etc.) from your shared rules.

### Claude Code Settings.json

The `.claude/settings.json` file controls permissions and tool access:

```json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/**)",
      "Bash(rm -rf *)"
    ]
  },
  "disallowedTools": [
    "WebFetch"
  ]
}
```

### Other Project Metadata Standards

- **llms.txt**: An emerging standard for making website content LLM-readable (similar to robots.txt for AI)
- **devcontainer.json**: VS Code dev containers; useful for reproducible AI development environments
- **mise/asdf .tool-versions**: Language version management; useful for AI to know which runtimes are available

**Sources:**
- [GitHub: ai-rulez](https://github.com/Goldziher/ai-rulez)
- [Claude Code Docs: Settings](https://code.claude.com/docs/en/settings)
- [eesel.ai: Developer's Guide to settings.json in Claude Code](https://www.eesel.ai/blog/settings-json-claude-code)
- [idavidov.eu: Master File for VS Code, Cursor, Windsurf](https://idavidov.eu/one-file-to-rule-them-all-cursor-windsurf-and-vs-code)
- [ScaleMath: LLMs.txt Standard](https://scalemath.com/blog/llms-txt/)

---

## 8. Recommendations for a Small IT Services Company

Given a small IT services company that handles diverse projects (client infrastructure, internal tools, automation, documentation), here are concrete recommendations:

### Tier 1: Adopt Now (Mature, High ROI)

1. **AGENTS.md as the universal standard**. Put one in every project repository. It works with Claude Code, Gemini CLI, Copilot, Codex, and any future tool. Include: build commands, architecture overview, conventions, testing instructions, security boundaries.

2. **CLAUDE.md for Claude-specific features**. If Claude Code is your primary tool, maintain a CLAUDE.md that imports AGENTS.md (`@AGENTS.md`) and adds Claude-specific instructions (skills, hooks, tool restrictions). Keep it under 100 lines.

3. **`.claude/rules/` for modular, scoped rules**. Break instructions into focused files with path-based scoping. This scales much better than a monolithic CLAUDE.md as projects grow.

4. **`.claude/commands/` for team workflows**. Create slash commands for your most common operations: standup summaries, pre-deployment checks, incident response, code review workflows. These are version-controlled and shared with the team.

5. **Feature-based project layout**. Organize new projects with vertical slice / feature-folder architecture. This makes AI agents dramatically more effective.

### Tier 2: Adopt Soon (Growing, Good ROI)

6. **Copier for project templates**. Create a company Copier template that scaffolds new projects with the right directory structure, AGENTS.md, CLAUDE.md, `.claude/` directory, CI configuration, etc. The `when` conditional lets one template serve infrastructure, tooling, and documentation projects. The update mechanism means template improvements propagate to existing projects.

7. **`.claude/settings.json` for security boundaries**. Deny access to `.env` files, secrets directories, and destructive commands. Check this into version control.

8. **Skills for specialized workflows**. Create skills for recurring complex tasks: PR summarization, incident postmortems, infrastructure review.

### Tier 3: Evaluate (Emerging, Experimental)

9. **ai-rulez** if the team uses multiple AI tools (Claude Code + Cursor + Copilot). Useful for keeping configuration synchronized, but adds a build step. Evaluate whether the team actually uses enough different tools to justify the complexity.

10. **GEMINI.md** only if the team actively uses Gemini CLI. Otherwise, the AGENTS.md approach covers it (Gemini CLI can be configured to read AGENTS.md by changing `context.fileName` in settings.json).

### Recommended Project Skeleton

```
project-root/
  AGENTS.md                    # Universal agent context
  CLAUDE.md                    # Claude-specific (imports @AGENTS.md)
  .claude/
    settings.json              # Permissions, denied tools
    commands/
      standup.md               # /project:standup
      deploy-check.md          # /project:deploy-check
      review.md                # /project:review
    rules/
      code-style.md            # Auto-loaded rules
      testing.md
      security.md
    skills/
      pr-summary/
        SKILL.md
  .gitignore                   # Ignore .claude/settings.local.json
  src/
    features/                  # Vertical slice architecture
      feature-a/
        CLAUDE.md              # Feature-specific context
        ...
      feature-b/
        CLAUDE.md
        ...
    shared/
  docs/
  infra/
    CLAUDE.md                  # Infra-specific AI context
```

---

## 9. Adoption Maturity Summary

| Convention | Maturity | Adoption | Vendor Lock-in | Recommendation |
|---|---|---|---|---|
| CLAUDE.md | Mature | High (Claude ecosystem) | Claude Code only | Adopt now |
| AGENTS.md | Mature | High (20K+ repos, multi-vendor) | None (open standard) | Adopt now |
| `.claude/rules/` | Mature | Medium-High | Claude Code only | Adopt now |
| `.claude/commands/` | Mature | Medium-High | Claude Code only | Adopt now |
| Claude Skills (SKILL.md) | Stable | Medium | Claude Code only | Adopt for complex workflows |
| GEMINI.md | Stable | Medium | Gemini CLI only | Adopt if using Gemini |
| Copier templates | Mature | Medium (Python ecosystem) | None | Adopt for template management |
| ai-rulez | Early | Low-Medium | None | Evaluate if multi-tool team |
| Vertical slice architecture | Established | Medium | None | Adopt for new projects |
| Context engineering practices | Emerging discipline | Growing | None | Adopt principles now |
| llms.txt | Early | Low | None | Watch |

The strongest pattern emerging across all sources is **layered context**: a universal base (AGENTS.md) for all tools, tool-specific overlays (CLAUDE.md, GEMINI.md) for specialized features, and modular scoped rules for different parts of the codebase. Combined with feature-based project organization, this approach maximizes both human and AI productivity while minimizing vendor lock-in.
