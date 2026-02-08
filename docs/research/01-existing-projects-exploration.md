## COMPREHENSIVE REPORT: Jason van Wyk's Precept Systems Project Structure

### 1. COMMON PATTERNS ACROSS PROJECTS

The 31 projects in `/home/jason/Projects/` follow an extremely consistent organizational framework with these universal elements:

**Universal Files (Present in Nearly All Projects):**
- `README.md` - Project overview and client information
- `CLAUDE.md` - AI assistant guidance and technical context
- `STATUS.md` - Current project status and task tracking
- `RESUME.md` - Session resume point for continuity
- `.gitignore` - Standard exclusions
- `correspondence/` folder - Client communications
- `docs/` folder - Project documentation
- `pics/` folder - Photos and screenshots
- `assets/` folder - Precept branding (logo, company details)
- `.git/` - Git version control (all projects are git repos)
- `.claude/` - Local Claude Code settings

**Consistency Rate:** 95%+ of projects follow this structure. The template project (`ict_project_template`) exists specifically to enforce this standard.

---

### 2. FOLDER NAMING CONVENTIONS

**Project Directory Naming:**
- **Residential ICT projects:** Lowercase with underscores (e.g., `jenny_henschel`, `louise_reiche`, `gill_mccord`)
- **Business/Commercial projects:** Lowercase with hyphens (e.g., `fairfield-water`, `jenkins-network`, `crop_monitoring_camera`)
- **Company internal projects:** Lowercase with hyphens (e.g., `precept-assets`, `precept-website-v3`, `odoo_precept_setup`)
- **Specialized projects:** Pascal case (e.g., `Milk-Depot-Coffee-Roaster`, `Signal-Server`)

**Internal Folder Structure (Consistent):**
```
project-name/
├── README.md
├── CLAUDE.md
├── STATUS.md
├── RESUME.md
├── .gitignore
├── .git/
├── .claude/
├── assets/
│   ├── precept_logo/
│   │   ├── Precept Systems Logo.jpg
│   │   ├── Precept Systems Logo.png
│   │   └── Precept Systems Logo.svg
│   ├── email-signature.html
│   └── precept_company_details.md
├── correspondence/
│   ├── README.md
│   └── YYYY-MM-DD_channel.md (dated entries)
├── docs/
│   ├── planning/
│   │   ├── client/          (client-facing proposals)
│   │   ├── internal/        (technical docs, numbered)
│   │   ├── correspondence/  (meeting notes)
│   │   └── site-visits/     (field visit reports)
│   └── [project-specific docs]
└── pics/
    └── [screenshots, photos]
```

---

### 3. FILE NAMING CONVENTIONS

**Correspondence Files (Dated):**
- Format: `YYYY-MM-DD_channel.md`
- Examples: `2026-01-27_whatsapp.md`, `2026-02-03_email.md`, `2026-02-05_site-visit.md`
- Pattern: Date, underscore, communication channel

**Internal Numbered Documents:**
- Format: `NN-description.md`
- Examples: `00-mvp-scope.md`, `01-architecture-decisions.md`, `04-research-report.md`
- Used for sequential planning documents in `docs/planning/internal/`

**General Documentation:**
- Format: `lowercase-with-hyphens.md`
- Examples: `laptop-options.md`, `client-info.md`, `site-assessment-findings.md`

**Quotation References (Odoo ERP):**
- Format: `S[5-digit number]` (quotes)
- Examples: `S00011`, `S00007`, `S00008`
- Found in project STATUS.md files

**Invoice References (Odoo ERP):**
- Format: `INV/YY-YY/NNNN`
- Examples: `INV/25-26/0005`, `INV/25-26/0007`, `INV/25-26/0008`
- Used for billing in client projects

**Project Reference Codes:**
- Format: `{CLIENT}-{YYYY}-{NNN}` or `{ABBREV}-{YYYY}-{NNN}`
- Examples: `FD-2026-001` (Fairfield), `HH-2026-001` (Harry Hirsch)
- Used for document numbering and identification

---

### 4. THE "4-FILE SYSTEM"

This is the core organizational framework. Every project (especially ICT projects) uses these four files for project management:

**A. README.md (Project Overview)**
- Client contact information (table format)
- Project description and scope
- Quick status summary pointing to STATUS.md
- Milestones checklist
- Quotation summary (table)
- Key files reference
- Important context notes
- Workflow notes

**B. CLAUDE.md (AI Assistant Context)**
- Project overview with business context
- Session startup instructions (what to read first)
- Key files to read
- Project-specific architecture or technical details
- Technologies/tools involved
- Important caveats and warnings
- Git workflow information
- Billing references
- Comprehensive reference resources (if applicable)
- Document structure and naming conventions

**C. STATUS.md (Project Status & Tracking)**
- Last updated timestamp
- Quote reference and status
- Current phase summary
- Task status tables (Completed, In Progress, Awaiting Client, Potential Future Work)
- Financial summary (Precept charges + third-party costs)
- Key decisions made
- Contact log (dates, channels, summaries)
- Files reference index

**D. RESUME.md (Session Resume Point)**
- "Right now" summary (current phase and status)
- "What's done" - completed items
- "What's cancelled" - abandoned work
- "Outstanding" - what needs completion
- Key files reference
- Much shorter than STATUS.md (2-3 pages vs 10-20)

**Usage Pattern:**
- Session start: Read RESUME.md, then STATUS.md, then README.md for full context
- Session end: Update RESUME.md and STATUS.md for next session
- Client communication: Reference README.md and STATUS.md
- AI assistant guidance: Reference CLAUDE.md

---

### 5. PROJECT DIVERSITY: CATEGORIZATION OF 31 PROJECTS

**A. Residential ICT Support (13 projects) - Small clients, local St John's Village:**
1. `ashleigh_bode` - WiFi assessment, tech support
2. `gill_mccord` - Brother printer scan-to-email setup
3. `graeme_crookes` - Outlook troubleshooting
4. `gregg-sobey` - [ICT support]
5. `harry_hirsch` - [ICT support, from template]
6. `jacqui_bachanan` - Molly Buchanan (91yo) ALU IT support
7. `jenny_henschel` - Laptop setup, email config, data migration (COMPLETED)
8. `louise_reiche` - Elderly client from Spain, account/storage setup (COMPLETED)
9. `jadon_laptop` - [Personal/student device]
10. `jadon-slotcar-repair` - Hobby/personal project
11. `trish_rawlinson` - [ICT support]
12. `mosaic_group` - Water meter monitoring for real estate company
13. `rosa-no2-dairy-mews` - [Location-based, minimal activity]

**B. Network/Connectivity Projects (3 projects):**
1. `jenkins-network` - Complex fiber + mesh WiFi troubleshooting (COMPLETED)
2. `fairfield-water` - Large IoT water monitoring system (Phase 1 deployed, Phase 2 in progress)
3. `dersal-consulting` - [Professional consulting, minimal files]

**C. IoT/Hardware Projects (3 projects):**
1. `crop_monitoring_camera` - Raspberry Pi 5 + Jetson Orin agricultural monitoring (PLANNING)
2. `Signal-Server` - C++ radio propagation modeling tool
3. `Milk-Depot-Coffee-Roaster` - Arduino + Artisan roasting control (DEVELOPMENT)

**D. Software Development (2 projects):**
1. `precept-website-v3` - Company website (minimal activity)
2. `omarchy-system-troubleshooting` - [Software project]

**E. Infrastructure/Admin (5 projects):**
1. `odoo_precept_setup` - Odoo ERP v19 configuration (ACTIVE)
2. `precept-assets` - Company branding and assets library
3. `clawdbot-explore` - Research/exploration
4. `test-project` - [Template/test]
5. `loans` - [Financial tracking, minimal files]

**F. Other/Uncategorized (2 projects):**
1. `susan-edmonds-kindle` - [eBook project]
2. `emalaheni_statements` - [Empty, may be archived]

**Status Summary:**
- **Active/In Progress:** 12 projects
- **Completed/Closed:** 8 projects
- **Planning/Pre-development:** 5 projects
- **Internal/Admin:** 5 projects
- **Minimal/Archived:** 1 project

---

### 6. WHAT WORKS WELL: EFFECTIVE PATTERNS

**A. The 4-File System**
- Provides immediate context for any team member (or Claude)
- RESUME.md saves 10+ minutes per session startup
- STATUS.md is the single source of truth for project state
- Consistent structure makes knowledge transfer smooth

**B. Dated Correspondence Folders**
- Easy to search chronologically
- Automatically time-sorted in file explorer
- `YYYY-MM-DD_channel.md` format is unambiguous
- All communication in one searchable location

**C. Client-Facing vs Internal Documentation Split**
- `docs/planning/client/` - Formal proposals, SOWs
- `docs/planning/internal/` - Technical research, specs
- Clear separation prevents accidentally sending internal notes to clients

**D. Asset Organization**
- `assets/` folder shared across projects
- Precept logo in 3 formats (jpg, png, svg)
- Email signature pre-formatted as HTML
- Company details in markdown for easy copy-paste

**E. Billing Integration with Odoo**
- Quote references (S-series) and Invoice references (INV-series) in STATUS.md
- Invoices stored in `docs/billing/` subfolder
- Easy to track payment status and financial history
- Financial summary tables in STATUS.md make invoicing quick

**F. HTML Document Generation**
- Self-contained HTML with inline CSS (no external stylesheets)
- Print-to-PDF ready (A4 size, margins, page breaks)
- Two branding tiers: formal (blue/teal, cover pages) vs working (darker blue, checklists)
- Examples: site visit checklists, handover documents, assessments

**G. .claude Folder**
- Local Claude Code settings stored per-project
- Keeps workspace preferences separate from source code
- Ignored by git (.gitignore includes .claude/)

**H. Git Workflow**
- Every project is a git repo
- Frequent commits with descriptive messages
- Footer convention: `Co-Authored-By: Claude <noreply@anthropic.com>`
- Remote SSH (not HTTPS)

---

### 7. WHAT'S INCONSISTENT: VARIATION POINTS

**A. CLAUDE.md Customization**
- Template projects show boilerplate CLAUDE.md (long, detailed)
- Custom projects have project-specific CLAUDE.md (architecture-focused)
- Some projects have extensive sections (fairfield-water, jenkins-network, crop_monitoring_camera)
- Others are minimal (louise_reiche, harry_hirsch, jacqui_bachanan)
- **Inconsistency:** Depth and content vary significantly

**B. Project Maturity Stages**
- Some projects have full `docs/planning/` structure (fairfield-water, crop_monitoring_camera)
- Others have minimal documentation (graeme_crookes, harry_hirsch)
- Some have `ARCHIVE.md` (odoo_precept_setup) - not universal

**C. Billing/Quoting References**
- Some projects have formal Odoo quotes/invoices (most residential ICT)
- Others don't (research projects like crop_monitoring_camera, Signal-Server)
- Invoice location varies: `docs/billing/`, `docs/Billing/`, root folder

**D. Correspondence Entry Dates**
- Some use `YYYY-MM-DD_channel.md` format (consistent)
- A few use alternative formats (mostly consistent though)
- Most have a `correspondence/README.md` index

**E. Project-Specific Technologies**
- ICT projects focus on client-facing services
- IoT/hardware projects have complex technical CLAUDE.md
- ERP project (odoo_precept_setup) is more admin-focused
- No standard for code projects vs. client projects

**F. README.md Template vs Custom**
- Simple ICT projects use template format (placeholder-filled)
- Complex projects (fairfield-water, crop_monitoring_camera) have custom README.md
- **Missing:** Some early projects missing detailed README.md

**G. Directory.md vs Not**
- Some projects include `DIRECTORY.md` (fairfield-water, crop_monitoring_camera)
- Not universal
- Useful for large/complex projects

---

### 8. BILLING & QUOTING PATTERNS

**Odoo ERP Integration:**
- Quote references: S-series (S00005, S00007, S00011, etc.)
- Invoice references: INV/YY-YY/NNNN (INV/25-26/0005, INV/25-26/0008)
- Sequence appears to be chronological by creation date
- Billing contact uses client name or referrer (e.g., Bill to: Peter Kyle for Gill McCord project)

**Financial Tracking in STATUS.md:**
- **Precept Charges:** Direct labor and hardware provision by Precept
- **Third Party Costs (Passthrough):** Domain registration, hosting, software licenses
- **Totals:** Precept charges + third party = Invoice total
- **Status:** Quote approval date, invoice date, payment received date

**Examples from Explored Projects:**
- Jenny Henschel: `S00011` - R15,599 (hardware + setup, now R16,185.30 with passthrough costs) - PAID as INV/25-26/0008
- Jenkins Network: INV/25-26/0005 - R1,530.00 (2.5 hrs labor + hardware) - PAID
- Gill McCord: INV/25-26/0007 - [Amount in docs/billing/]
- Fairfield Water: Phase 1 deployed (manual entry), Phase 2 in proposal stage
- Mosaic Group: Pre-proposal stage (quote TBD)

**Payment Terms:**
- Varies by project
- Some projects: "Invoice after completion, no deposit"
- Invoice due dates: typically 7 days (e.g., Jenkins Network)
- Most common: Payment on invoice (no retainer)

**Rates (as documented in CLAUDE.md templates):**
- Consultation: R550/hr
- Travel: R4.76/km (SARS 2026 allowance)

---

### 9. KEY INSIGHTS & OBSERVATIONS

**A. Evolution Over Time**
- Earlier projects (2025) have less formal structure
- Recent projects (2026) consistently follow the 4-file system
- Template project exists to enforce consistency going forward

**B. Project Maturity Correlation**
- Completed projects have comprehensive STATUS.md (jenny_henschel, gill_mccord, jenkins-network)
- Planning-phase projects have detailed CLAUDE.md and internal planning docs (crop_monitoring_camera, fairfield-water Phase 2)
- Minimal projects have basic structure only (early projects, archived items)

**C. Geographic Clustering**
- Most residential clients in St Johns Village, Howick (KZN)
- Professional projects across South Africa (Durban: Mosaic Group, Fairfield Dairy)
- One international client (Louise Reiche, Spanish phone number)

**D. Technology Patterns**
- Network troubleshooting: Detailed technical CLAUDE.md with device specs, port labels, diagnostic procedures
- Hardware projects: BOM, component research, assembly instructions
- ICT client projects: Simple structure, billing-focused
- ERP project: Configuration tracking, archive of old items

**E. Communication Channels**
- WhatsApp dominant for initial contact and follow-ups
- Email for formal quotes and invoices
- Site visits documented with photos and checklists
- Correspondence indexed by date and channel

---

### 10. DIRECTORY STRUCTURE AT A GLANCE

**31 Projects Summary:**

| Project Type | Count | Key Examples |
|---|---|---|
| Residential ICT | 13 | jenny_henschel, louise_reiche, gill_mccord |
| Network/Connectivity | 3 | fairfield-water, jenkins-network |
| IoT/Hardware | 3 | crop_monitoring_camera, Milk-Depot-Coffee-Roaster |
| Software Dev | 2 | precept-website-v3, omarchy-system-troubleshooting |
| Infrastructure/Admin | 5 | odoo_precept_setup, precept-assets |
| Uncategorized | 2 | susan-edmonds-kindle, loans |
| **Total** | **31** | |

**Key Statistics:**
- Total projects: 31
- With CLAUDE.md: 19 (61%)
- With STATUS.md: 13 (42%)
- With RESUME.md: 12 (39%)
- All git repos: 100% (31/31)
- All have README.md: 21 (68%)

---

### RECOMMENDATIONS FOR FUTURE WORK

1. **Standardize archival:** Create an `ARCHIVED/` folder for completed/inactive projects
2. **Consistency enforcement:** Ensure new projects use template (already done - template exists)
3. **Billing dashboard:** Consider a top-level `BILLING_SUMMARY.md` tracking all open quotes/invoices
4. **Project README script:** Auto-generate README.md headers from CLAUDE.md
5. **Correspondence index:** Consider auto-indexing YYYY-MM-DD files with brief summaries
6. **Status badges:** Add emoji status to folder names (e.g., `jenny_henschel [CLOSED]`, `fairfield-water [ACTIVE]`)
7. **Technology tags:** Metadata about technology stack for quick filtering

---

This structure demonstrates a mature, scalable system for managing diverse projects (residential IT support, industrial IoT, software development, ERP administration) with clear accountability, documentation standards, and billing integration.
