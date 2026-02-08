# Precept Systems Template Strategy Synthesis

**Author:** Synthesis Agent (Claude Opus 4.6)
**Date:** 2026-02-07
**Inputs:** 4 research reports (existing projects analysis, template analysis, CLI+AI best practices, organization standards)
**Purpose:** Decisive recommendations for building the Precept Systems project template system

---

## 1. How Many Templates: The Template Catalogue

**Decision: 4 templates**, built as layers on a single shared base.

| # | Template Name | Slug | Purpose | Covers |
|---|---------------|------|---------|--------|
| 1 | **precept-base** | `base` | Shared foundation -- never used directly | Common files, AI context, branding, git config |
| 2 | **precept-client-ict** | `client-ict` | Residential and small business ICT service jobs | WiFi, printer setup, laptop config, email, AV, network troubleshooting. Covers ~70% of current projects (ashleigh_bode, gill_mccord, jenny_henschel, harry_hirsch, etc.) |
| 3 | **precept-client-project** | `client-project` | Complex multi-phase client engagements | IoT deployments, network infrastructure, business systems, automation, Odoo implementations. Covers fairfield-water, jenkins-network, mosaic_group, crop_monitoring_camera, Milk-Depot-Coffee-Roaster |
| 4 | **precept-internal** | `internal` | Precept's own company projects | precept-assets, precept-website, odoo_precept_setup, tooling, research/exploration |

**Why not more?** Jason is a one-person operation. Every additional template is a maintenance burden. The difference between templates 2 and 3 is scope/complexity, not fundamental structure. Template 4 exists because internal projects have no client, no quoting, and no correspondence -- they are structurally different.

**Why not fewer?** A single template with conditional sections would leave empty folders in small residential jobs (bloat) or miss critical structure in large multi-phase projects. The 3-template approach (base + 2 client types + 1 internal) hits the sweet spot.

---

## 2. Universal Base Structure (precept-base)

These files and folders appear in EVERY project, regardless of type.

```
project-root/
    README.md                          # Project overview (human-facing)
    CLAUDE.md                          # Claude Code context (AI-facing, Claude-specific)
    AGENTS.md                          # Universal agent context (tool-agnostic)
    STATUS.md                          # Project status and task tracking
    RESUME.md                          # Quick session resume point
    .gitignore                         # Standard exclusions
    project.yml                        # Machine-readable project metadata (NEW)
    .claude/
        settings.local.json            # Claude Code permissions (gitignored)
        commands/
            wrap-up.md                 # /project:wrap-up -- end-of-session routine
            status-report.md           # /project:status-report -- generate status summary
        rules/
            precept-conventions.md     # Always-loaded Precept conventions
    .gemini/
        settings.json                  # Gemini CLI config (points context to AGENTS.md)
```

### What STAYS from existing template (unchanged or minor tweaks)

| File | Status | Notes |
|------|--------|-------|
| `README.md` | **KEEP** | Same placeholder structure. Remove the `credentials.txt` reference from Key Files table (credentials go in `.env` or password manager, not a tracked text file). |
| `STATUS.md` | **KEEP** | Same structure. Add a `## Project Metadata` header at top linking to `project.yml`. |
| `RESUME.md` | **KEEP** | Same structure. It works well -- short, scannable, effective. |
| `.gitignore` | **KEEP + EXTEND** | Add `.claude/settings.local.json`, `.gemini/`, `*.env`, `credentials.txt`, `.copier-answers.yml` to exclusions. Remove `screenshots/` (redundant with `pics/`). |
| `.claude/settings.local.json` | **KEEP** | Same permissions structure. Add `Bash(git log:*)`, `Bash(git diff:*)` to allowed list. |

### What CHANGES from existing template

| Item | Old | New | Rationale |
|------|-----|-----|-----------|
| `CLAUDE.md` | Dual-purpose: template instructions + project context in one file | Split into two concerns: template instructions live in the scaffolding tool, CLAUDE.md is purely project context | Current CLAUDE.md is 192 lines of template docs that get replaced. The new CLAUDE.md starts as a lean project-context file (~20 lines). |
| `assets/` folder in every project | Logo, email sig, company details duplicated per project | Removed from individual projects. Brand assets live in `precept-assets` repo and are referenced by path or symlink. | Eliminates 5+ duplicate files across 31 projects. Logo changes require one update, not 31. |
| `docs/planning/` hierarchy | `docs/planning/client/`, `docs/planning/internal/`, `docs/planning/correspondence/`, `docs/planning/site-visits/` with `.gitkeep` | Flattened to `docs/` only in base. Template-specific structure added by client-project template. | The 4-level planning hierarchy is empty bloat for small residential jobs. Only complex projects need it. |
| `pics/` with `.gitkeep` | Present in base | Present in base but without `.gitkeep` -- folder created on first use | Avoid tracking empty directories. Git tracks files, not folders. |
| `correspondence/README.md` | Template with file naming conventions | Kept but simplified. Naming convention info moves to `AGENTS.md`. | Correspondence README was duplicating info that belongs in agent context. |

### What is NEW

| Item | Purpose |
|------|---------|
| `AGENTS.md` | Universal agent context file. Works with Claude Code, Gemini CLI, Copilot, Codex, and any future AI tool. Contains the shared project context, conventions, and commands that all AI tools need. CLAUDE.md imports this via `@AGENTS.md`. |
| `project.yml` | Machine-readable project metadata. Replaces scattered placeholders. Used by scaffolding tool, AI agents, and status dashboards. See Appendix A for schema. |
| `.claude/commands/wrap-up.md` | End-of-session slash command. Updates RESUME.md and STATUS.md, commits changes. Replaces Jason's mental checklist with an automated routine. |
| `.claude/commands/status-report.md` | Generate a formatted status summary from STATUS.md for WhatsApp/email to client. |
| `.claude/rules/precept-conventions.md` | Always-loaded rules: naming conventions, commit message format, correspondence filing, billing references. Keeps CLAUDE.md cleaner. |
| `.gemini/settings.json` | Configures Gemini CLI to read `AGENTS.md` as its context file. |

---

## 3. Template-Specific Structure

### Template 2: precept-client-ict (small service jobs)

Adds to base:

```
project-root/
    correspondence/                    # Client communications
        README.md                      # Correspondence index and naming guide
    docs/                              # Project documentation
        (files created as needed)
```

That is it. No `pics/`, no `assets/`, no planning hierarchy. A residential WiFi assessment does not need a `docs/planning/client/` folder. The `docs/` folder and `correspondence/` folder are the only additions. Photos go directly in `docs/` if needed (e.g., `docs/site-photos/`).

**Default `project.yml` values:**
```yaml
type: client-ict
billing: true
complexity: simple
```

### Template 3: precept-client-project (complex engagements)

Adds to base:

```
project-root/
    correspondence/
        README.md
    docs/
        planning/
            client/                    # Client-facing proposals, SOWs
            internal/                  # Internal specs, research, numbered docs
            site-visits/               # Site visit checklists and reports
        deliverables/                  # Final outputs to client
    pics/                              # Photos, screenshots, diagrams
```

**Additional files in CLAUDE.md:** Architecture section, phase tracking, document numbering conventions.

**Default `project.yml` values:**
```yaml
type: client-project
billing: true
complexity: complex
phases:
  - assessment
  - proposal
  - delivery
  - handover
```

### Template 4: precept-internal (company projects)

Adds to base:

```
project-root/
    docs/                              # Documentation
    src/                               # Source code (if applicable)
```

No `correspondence/` (no external client). No billing section in STATUS.md. CLAUDE.md focuses on technical context rather than client context.

**Default `project.yml` values:**
```yaml
type: internal
billing: false
complexity: varies
```

---

## 4. Naming Conventions

### One Unified Standard

| Category | Convention | Example | Notes |
|----------|-----------|---------|-------|
| **Project directories** | `lowercase_with_underscores` for client projects; `lowercase-with-hyphens` for internal/technical projects | `jenny_henschel`, `precept-website-v3` | Underscores for people names (natural word boundary). Hyphens for descriptive names. Matches Jason's existing pattern exactly. |
| **General files** | `lowercase-with-hyphens.ext` | `site-assessment-findings.md` | |
| **Numbered sequences** | `NN-description.ext` | `01-project-brief.md`, `04-research-report.md` | Two-digit zero-padded prefix. Used in `docs/planning/internal/`. |
| **Correspondence files** | `YYYY-MM-DD_channel.ext` | `2026-01-27_whatsapp.md`, `2026-02-03_site-visit.md` | Date + underscore + channel. Multi-day threads: `YYYY-MM-DD-DD_channel.md`. |
| **Date-stamped docs** | `YYYY-MM-DD-description.ext` | `2026-02-07-network-diagram.png` | ISO 8601 dates only. |
| **Billing docs** | Odoo reference as filename | `S00011-quote.pdf`, `INV_25-26_0008.pdf` | Stored in `docs/billing/`. |
| **Folders** | `lowercase-with-hyphens` | `site-visits/`, `docs/planning/` | Always lowercase, never spaces. |

### Client Codes

Client codes are used in formal document numbering. They are 2-3 uppercase letters derived from the client or project name.

| Client/Project | Code | Derivation |
|----------------|------|-----------|
| Fairfield Dairy | FD | First letters |
| Harry Hirsch | HH | Initials |
| Jenkins Network | JN | First letters |
| Mosaic Group | MG | First letters |
| Precept Systems (internal) | PS | Company |

Client codes are recorded in `project.yml` as `client_code`.

### Document Numbering

| Scope | Pattern | Example |
|-------|---------|---------|
| Project reference | `{CODE}-{YYYY}-{NNN}` | `FD-2026-001` |
| Proposals/SOWs | `{CODE}-PRO-{YYYYMM}-{NNN}` | `FD-PRO-202601-001` |
| Correspondence docs | `{CODE}-COR-{YYYYMM}-{NNN}` | `FD-COR-202602-003` |
| Internal company docs | `PS-{TYPE}-{YYYY}-v{X.Y}` | `PS-TARIFF-2026-v1.0` |

### Odoo ERP Integration

| Ref Type | Format | Source |
|----------|--------|--------|
| Quotes | `S{NNNNN}` | Odoo sequence (e.g., S00011) |
| Invoices | `INV/{YY-YY}/{NNNN}` | Odoo sequence (e.g., INV/25-26/0008) |

These references are recorded in `project.yml` and `STATUS.md`. The template does not generate them -- Odoo does. The template just provides placeholders.

---

## 5. AI Context Strategy

### The Three-File System

```
AGENTS.md      -- Universal context (read by all AI tools)
CLAUDE.md      -- Claude-specific context (imports @AGENTS.md, adds Claude features)
.gemini/settings.json -- Points Gemini CLI to AGENTS.md
```

**AGENTS.md** is the single source of truth for project context. It contains everything any AI tool needs to understand and work in the project. **CLAUDE.md** imports it and adds Claude-specific instructions (skills, slash commands, hooks, tool restrictions).

There is no separate `GEMINI.md` file. Gemini CLI is configured via `.gemini/settings.json` to read `AGENTS.md` directly:

```json
{
  "context": {
    "fileName": "AGENTS.md"
  }
}
```

### AGENTS.md Structure (template)

Target: 40-60 lines. Lean and scannable. Contains:

- Project overview (1 paragraph)
- Session startup sequence (read RESUME, STATUS, README + git log)
- Key facts (client, quote ref, type, phase)
- File organization guide
- Conventions summary (file naming, correspondence, commits)
- Git workflow (remote, co-authored-by)
- Precept business context (currency, rates, timezone, Odoo refs)

Detailed conventions go in `.claude/rules/precept-conventions.md`.

### CLAUDE.md Structure (template)

Target: 15-25 lines. Contains:

- `@AGENTS.md` import
- Claude-specific slash commands list
- Tool permissions reference
- Project-specific caveats for Claude

### .claude/rules/precept-conventions.md

Always loaded by Claude Code alongside CLAUDE.md. Contains detailed conventions:

- Naming conventions table
- Document numbering patterns
- HTML document conventions (branding tiers, CSS classes)
- Odoo ERP workflow details
- South African business context (rates, phone format, SARS)
- Correspondence filing rules

Target: 80-120 lines. Loaded automatically, does not consume explicit context-window space.

### .claude/commands/ (Slash Commands)

| Command | File | Purpose |
|---------|------|---------|
| `/project:wrap-up` | `wrap-up.md` | End-of-session: update RESUME.md with current state, update STATUS.md if tasks changed, stage and commit with descriptive message |
| `/project:status-report` | `status-report.md` | Read STATUS.md and RESUME.md, produce a concise client-ready summary suitable for WhatsApp or email |

### No Shared .context/ Directory

A shared `.context/` directory was considered and rejected. The `.claude/rules/` mechanism already provides scoped, modular context loading. Adding a third context location would create confusion about where to put information. The hierarchy is:

1. **AGENTS.md** -- universal project context (all tools)
2. **CLAUDE.md** -- Claude imports + Claude-specific instructions
3. **.claude/rules/** -- detailed conventions and rules (auto-loaded by Claude)
4. **.gemini/settings.json** -- Gemini config (points to AGENTS.md)

---

## 6. Tooling Recommendation

**Decision: Bash function (`precept-init`), not Copier.**

### Rationale

| Factor | Copier | `precept-init` bash function |
|--------|--------|------------------------------|
| Dependency | Requires Python, pip install | Zero dependencies (bash only) |
| Template updates | Built-in `copier update` | Manual (but projects are small and few) |
| Conditional logic | Excellent (`when:` in YAML) | Simple `case` statement |
| Learning curve | Moderate (Jinja2, YAML config) | Zero (Jason already writes bash) |
| CLI integration | Separate tool | Sourced in `.bashrc`, always available |
| Template storage | Separate git repo with Jinja files | Template files in `precept-assets` repo or inline in function |
| Maintenance | Two systems to maintain (Copier config + templates) | One function to maintain |
| Jason preference | New tool to learn | Exactly the `precept-init` function he was already considering |

Copier is the superior engineering choice for a team. For a one-person CLI operation where the operator values simplicity and already had the `precept-init` idea, the bash function wins.

### precept-init Design

```bash
precept-init <project-name> [--type client-ict|client-project|internal]
```

Behavior:
1. Create directory `/home/jason/Projects/<project-name>`
2. Initialize git repo
3. Copy base files from `precept-assets/templates/base/`
4. Copy template-specific files based on `--type` (default: `client-ict`)
5. Run placeholder replacement interactively (client name, phone, email, address)
6. Create GitHub repo via `gh repo create --private`
7. Initial commit and push
8. Open Claude Code in the new project

Template files live in the `precept-assets` repository under a `templates/` directory:

```
precept-assets/
    templates/
        base/                          # Files shared by all templates
            AGENTS.md.template
            CLAUDE.md.template
            STATUS.md.template
            RESUME.md.template
            README.md.template
            project.yml.template
            .gitignore
            .claude/
                settings.local.json
                commands/
                    wrap-up.md
                    status-report.md
                rules/
                    precept-conventions.md
            .gemini/
                settings.json
        client-ict/                    # Additional files for ICT jobs
            correspondence/
                README.md
        client-project/                # Additional files for complex projects
            correspondence/
                README.md
            docs/
                planning/
                    client/.gitkeep
                    internal/.gitkeep
                    site-visits/.gitkeep
                deliverables/.gitkeep
        internal/                      # Additional files for internal projects
            (minimal additions)
    precept_logo/                      # Brand assets (not copied into projects)
        Precept Systems Logo.jpg
        Precept Systems Logo.png
        Precept Systems Logo.svg
    email-signature.html
    precept_company_details.md
```

### Future: Evaluate Copier if Scaling

If Precept ever grows to 2+ people, or Jason finds himself modifying the template frequently and wanting changes to propagate to existing projects, revisit Copier. The template structure above is designed to be compatible with a future Copier migration.

---

## 7. What Changes from the Existing Template

### Summary Table

| Item | Current Template | New Template | Change Type |
|------|-----------------|--------------|-------------|
| README.md | Placeholder template | Same structure, minor refinements | **KEEP** |
| STATUS.md | Placeholder template | Same structure | **KEEP** |
| RESUME.md | Placeholder template | Same structure | **KEEP** |
| CLAUDE.md | 192 lines, dual-purpose (template docs + project context) | ~20 lines, imports @AGENTS.md | **CHANGE** |
| AGENTS.md | Does not exist | ~50 lines, universal agent context | **NEW** |
| project.yml | Does not exist | Machine-readable metadata | **NEW** |
| .gitignore | 39 lines | Extended with new exclusions | **CHANGE** |
| .claude/settings.local.json | Basic permissions | Extended permissions | **CHANGE** |
| .claude/commands/ | Does not exist | wrap-up.md, status-report.md | **NEW** |
| .claude/rules/ | Does not exist | precept-conventions.md | **NEW** |
| .gemini/settings.json | Does not exist | Gemini CLI config | **NEW** |
| assets/ folder | Duplicated in every project | Removed -- lives in precept-assets only | **REMOVE** |
| docs/planning/ hierarchy | 4 subdirs with .gitkeep | Only in client-project template | **CHANGE** |
| pics/.gitkeep | Present | Removed (created on demand) | **CHANGE** |
| correspondence/README.md | Template | Simplified | **CHANGE** |
| credentials.txt reference | In README and RESUME | Removed (use .env or password manager) | **REMOVE** |

### What the 4-File System Becomes

The 4-file system (README, CLAUDE, STATUS, RESUME) is preserved and extended to a **6-file system**:

| File | Role | Audience |
|------|------|----------|
| `README.md` | Project overview, client info, scope | Humans (Jason, clients) |
| `AGENTS.md` | Universal AI context | All AI tools |
| `CLAUDE.md` | Claude-specific instructions | Claude Code only |
| `STATUS.md` | Task tracking, billing, contact log | Humans + AI |
| `RESUME.md` | Quick session resume | Humans + AI |
| `project.yml` | Machine-readable metadata | Scripts + AI |

The session startup sequence remains the same: RESUME.md first, then STATUS.md, then README.md.

---

## 8. Migration Path for Existing Projects

### Principle: Least Disruption

Do NOT attempt a mass migration. Existing projects work fine with their current structure. Apply the new conventions incrementally.

### Tier 1: Immediate (all active projects)

Add these files to all currently active projects. This can be done with a simple script:

1. **Add `AGENTS.md`** -- Generate from existing CLAUDE.md content (extract the universal parts)
2. **Add `.gemini/settings.json`** -- One-liner config file
3. **Add `.claude/commands/wrap-up.md`** -- Copy from template
4. **Add `.claude/rules/precept-conventions.md`** -- Copy from template

**Estimated effort:** 5 minutes per project, scriptable to ~1 minute per project.
**Impact:** Zero disruption. These are additive files that do not conflict with anything existing.

### Tier 2: When Resuming Work (per-project, on-demand)

When Jason next opens a project to do active work:

1. **Slim down CLAUDE.md** -- Move convention details to `.claude/rules/precept-conventions.md`, add `@AGENTS.md` import
2. **Add `project.yml`** -- Fill in project metadata
3. **Remove `assets/` if present** -- Brand assets should reference `precept-assets` repo

**Estimated effort:** 10 minutes per project during a natural work session.
**Impact:** Minimal -- done as part of regular work, not a separate migration effort.

### Tier 3: Never (completed/archived projects)

Do NOT migrate completed projects (gill_mccord, jenkins-network, jenny_henschel, etc.). They are done. Their current structure serves as historical record. Changing them provides zero value.

### Migration Script

Create a `precept-migrate` bash function that handles Tier 1:

```bash
precept-migrate <project-dir>
# 1. Creates AGENTS.md from CLAUDE.md (extracting universal sections)
# 2. Creates .gemini/settings.json
# 3. Copies .claude/commands/ from precept-assets/templates/base/
# 4. Copies .claude/rules/precept-conventions.md from precept-assets/templates/base/
# 5. Commits changes
```

---

## Appendix A: project.yml Schema

```yaml
# project.yml -- Machine-readable project metadata
# This file is read by precept-init, AI agents, and reporting scripts.

project:
  name: "Fairfield Water Monitoring"
  slug: "fairfield-water"
  type: "client-project"
  status: "active"
  created: "2024-12-15"

client:
  name: "Fairfield Dairy"
  code: "FD"
  contact: "Andrew Gillespie"
  phone: "+27 82 XXX XXXX"
  email: "andrew@fairfielddairy.co.za"
  address: "Fairfield Dairy, Howick, 3290"

billing:
  quote_ref: "S00007"
  quote_amount: "R45,000.00"
  invoice_ref: ""
  payment_terms: "50% deposit, 50% on completion"

repo:
  github: "jasonvanwyk/fairfield-water"
  branch: "main"
```

---

## Appendix B: .gitignore (Unified)

```gitignore
# OS generated files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~
.idea/
.vscode/

# Sensitive files
.env
*.env
credentials.txt
credentials/
secrets/

# Claude Code (local settings not committed)
.claude/settings.local.json

# Gemini CLI (local config)
.gemini/

# Copier (if migrated to Copier later)
.copier-answers.yml

# Database files
*.db
*.sqlite

# Node.js (for software projects)
node_modules/
package-lock.json

# Logs
*.log
```

---

## Appendix C: .claude/settings.local.json (Standard)

```json
{
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git status)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git check-ignore:*)",
      "Bash(git branch:*)",
      "Bash(ls:*)",
      "Bash(find:*)",
      "Bash(gh:*)",
      "WebSearch"
    ]
  }
}
```

---

## Appendix D: .claude/commands/wrap-up.md

```
End-of-session wrap-up routine:

1. Read the current RESUME.md and STATUS.md
2. Review git log for changes made this session: git log --oneline --since="4 hours ago"
3. Update RESUME.md with:
   - Current phase and status
   - What was completed this session
   - What the immediate next action is
   - Any blockers
4. Update STATUS.md if:
   - Tasks were completed (move to Completed table)
   - New tasks were identified
   - Contact was made with the client (add to Contact Log)
   - Financial items changed
5. Stage all changes and commit with a descriptive message summarising the session work
6. Push to remote
7. Display a brief summary of what was done and what is next
```

---

## Appendix E: .claude/commands/status-report.md

```
Generate a client-ready status report:

1. Read STATUS.md and RESUME.md
2. Produce a concise summary suitable for WhatsApp or email, including:
   - Current phase
   - What has been completed
   - What is in progress
   - What is waiting on the client
   - Any upcoming deadlines or next steps
   - Outstanding financial items (quotes pending, invoices due)
3. Keep the tone professional but approachable
4. Format for easy reading on a phone screen (short paragraphs, bullet points)
5. Display the report for Jason to copy-paste
```

---

## Appendix F: Decision Log

| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| 4 templates (base + 3) | 1 universal, 2 (just client + internal), 6+ (per service type) | Sweet spot between flexibility and maintenance burden |
| AGENTS.md as primary context | CLAUDE.md only, shared .context/ dir, symlinks | AGENTS.md is the open standard. Future-proofs against tool changes. CLAUDE.md imports it. |
| No separate GEMINI.md | GEMINI.md symlink to AGENTS.md, dedicated GEMINI.md | .gemini/settings.json can point to AGENTS.md directly. One less file to maintain. |
| Bash function over Copier | Copier, Cookiecutter, Yeoman, manual clone | Zero dependencies, matches Jason workflow, he was already planning this |
| Remove assets/ from projects | Keep duplicated assets, symlink to shared repo | Eliminates duplication across 31+ repos. One update point for branding. |
| Incremental migration | Big-bang migration of all projects, no migration | Tier 1 is scriptable and non-disruptive. Tier 2 happens naturally. Tier 3 is do not bother. |
| project.yml for metadata | Frontmatter in README.md, separate JSON file, database | YAML is human-readable, git-friendly, and parseable by scripts and AI agents |
| .claude/rules/ for conventions | All in CLAUDE.md, separate docs/, wiki | Auto-loaded by Claude Code, does not bloat the main context file, version-controlled |
| No credentials.txt | Keep credentials.txt pattern | Security risk. Use .env files (gitignored) or a password manager. |
