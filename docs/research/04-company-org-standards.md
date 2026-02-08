---

# Comprehensive Report: Document Management, Folder Organization, and Naming Standards for a Small IT Services Company

## Table of Contents

1. ISO 9001 Document Control and Hierarchy
2. ITIL/MSP Client Folder Organization
3. Project Folder Standards (PMI/PRINCE2)
4. Industrial Automation Documentation (ISA-95/IEC)
5. Naming Conventions Across Industries
6. Document Numbering Systems
7. Solo Operator / Freelancer Practical Structures
8. South African Compliance Considerations
9. Synthesis: What Is Realistic for a One-Person Operation

---

## 1. ISO 9001 Document Control and Hierarchy

The ISO 9001 framework defines a four-level documentation pyramid that has become the de facto standard across industries:

**Level 1 -- Quality Manual (the "What")**
- Quality policy and objectives
- Scope of the QMS
- High-level description of business processes

**Level 2 -- Procedures (the "Who/When")**
- Standard Operating Procedures (SOPs)
- Process descriptions defining who does what and when

**Level 3 -- Work Instructions (the "How")**
- Step-by-step task-level guides
- Templates and forms (blank)

**Level 4 -- Records (the "Evidence")**
- Completed forms, checklists, test reports
- Proof that work was done per procedure

**Key principle for small companies:** ISO 9001 explicitly acknowledges that a small organization may include its entire QMS in a single manual. There is no requirement for multiple binders of documentation. The standard cares about *controlled documented information* -- not volume. Version control, access control, and review cycles are the essentials.

**Practical folder mapping:**
```
/quality-management/
    quality-manual.pdf
    /procedures/
    /work-instructions/
    /templates/
    /records/
```

Sources: [Advisera - QMS Documentation Structure](https://advisera.com/9001academy/knowledgebase/how-to-structure-quality-management-system-documentation/), [PharmUni - ISO 9001 Document Hierarchy](https://pharmuni.com/2025/03/07/iso-9001-document-hierarchy-made-easy-what-you-must-know/), [QT9 Software - ISO 9001 Document Control](https://qt9software.com/blog/iso-9001-document-control)

---

## 2. ITIL / MSP Client Folder Organization

The IT Glue information hierarchy (industry standard for MSPs) organizes documentation into these categories per client:

**Per-Client Organization:**
- **Assets (Core):** The information needed for every customer and location to deliver IT support -- configurations, locations, contacts, passwords, network diagrams
- **SOPs:** Client-specific procedures (e.g., "How to disable alarm at Client X's Johannesburg office")
- **Strategy:** QBR (Quarterly Business Review) documentation, IT roadmaps, account management notes
- **Projects:** Active and archived project documentation
- **Inbox:** Drafts and un-filed documents awaiting classification

**Internal (Your Company) Documentation:**
- Knowledge base / how-to articles
- Internal SOPs and runbooks
- Vendor documentation and licensing

**Key MSP principle:** One person should serve as the "taxonomist" -- the master organizer who ensures documentation lands in the right place and incomplete docs get completed. For a one-person operation, this means disciplined filing habits with a defined weekly review cycle.

**Practical folder mapping:**
```
/clients/
    /client-name/
        /assets/           (configs, passwords, network diagrams)
        /sops/             (client-specific procedures)
        /strategy/         (roadmaps, QBRs)
        /projects/         (per-project subfolders)
        /correspondence/   (key emails, meeting notes)
```

Sources: [IT Glue - MSP Information Hierarchy](https://www.itglue.com/blog/msp-information-hierarchy/), [MSP360 - ITIL for MSPs](https://www.msp360.com/resources/blog/itil-for-msps-explained/), [ITSM.tools - ITIL Best Practices for MSPs](https://itsm.tools/10-itil-best-practices-for-msps-and-mssps/)

---

## 3. Project Folder Standards (PMI/PRINCE2)

Both PMI's PMBOK and PRINCE2 organize project documentation around the project lifecycle phases. The typical structure:

**Phase-Based Approach:**

```
/project-name/
    /01-initiation/
        project-charter
        business-case
        stakeholder-register
        kickoff-meeting-notes
    /02-planning/
        project-plan
        work-breakdown-structure
        budget
        schedule
        risk-register
        scope-statement
    /03-execution/
        status-reports
        change-requests
        meeting-minutes
        timesheets
        deliverables/
    /04-closure/
        lessons-learned
        final-report
        sign-off
        handover-documentation
```

**Alternative (Type-Based) Approach:**
```
/project-name/
    /admin/           (contracts, briefs, proposals)
    /plans/           (project plan, schedule, budget)
    /reports/         (status, progress)
    /deliverables/    (actual outputs)
    /correspondence/  (emails, meeting notes)
```

**PRINCE2 Specific Documents:**
PRINCE2 defines specific management products: Project Brief, Project Initiation Document (PID), Business Case, Stage Plans, Highlight Reports, End Stage Reports, Lessons Log, Risk Register, Issue Register, and End Project Report. These map neatly into the phase-based structure above.

**Key principle:** The numbered prefix (01-, 02-, 03-, 04-) forces logical ordering rather than alphabetical, which is a widely recommended practice.

Sources: [ProjectManagement.com - Folder Structure Discussion](https://www.projectmanagement.com/discussion-topic/180150/recommended-project-management-folder-structure), [IT Management 101 - Folder Structure Template](https://www.itmanagement101.co.uk/project-management-folder-structure-template/), [KnowledgeHut - PRINCE2 Documents](https://www.knowledgehut.com/blog/project-management/prince2-documents)

---

## 4. Industrial Automation Documentation (ISA-95/IEC)

For a company doing IIoT/SCADA/automation work, the documentation standards draw from ISA-95, ISA-88, IEC 61131-3, and IEC 62443.

**ISA-95 Hierarchy (maps to project organization):**
- Level 4: Business / Enterprise (ERP integration docs)
- Level 3: Manufacturing Operations (MES, SCADA application docs)
- Level 2: Supervisory Control (HMI screens, supervisory logic)
- Level 1: Device Control (PLC programs, I/O lists)
- Level 0: Physical Process (P&IDs, instrument lists)

**Standard Automation Project Deliverables:**
- Functional Design Specification (FDS) -- the single most important document
- Detailed Design Specification (DDS)
- Hardware Design (electrical schematics, pneumatic diagrams, panel layouts)
- Software Design (PLC source code, HMI screen designs, SCADA configurations)
- I/O List and tag database
- Network architecture diagrams
- Factory Acceptance Test (FAT) documentation
- Site Acceptance Test (SAT) documentation
- Commissioning records
- As-built documentation
- Operations and Maintenance manual
- FMEA / Risk Assessment

**Practical folder mapping for an automation project:**
```
/project-name/
    /01-specifications/
        functional-design-specification
        detailed-design-specification
        user-requirements
    /02-hardware/
        electrical-schematics
        panel-layouts
        io-lists
        network-diagrams
    /03-software/
        plc-programs/
        hmi-screens/
        scada-config/
        database-schemas/
    /04-testing/
        fat-documents/
        sat-documents/
        commissioning-records/
    /05-handover/
        as-built-drawings/
        operations-manual
        maintenance-manual
    /06-admin/
        proposals
        contracts
        change-orders
        meeting-minutes
```

Sources: [ISA Standards](https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard), [IACS Engineering - Functional Specifications](https://iacsengineering.com/functional-specifications/), [RealPars - What is an FDS](https://realpars.com/fds/), [Siemens - ISA-95 Framework](https://www.sw.siemens.com/en-US/technology/isa-95-framework-layers/)

---

## 5. Naming Conventions Across Industries

### Case Styles

| Style | Example | Common Use |
|---|---|---|
| kebab-case | `project-plan-v2.pdf` | URLs, web projects, Linux filesystems, modern DevOps |
| snake_case | `project_plan_v2.pdf` | Python projects, databases, older file systems |
| PascalCase | `ProjectPlan.pdf` | Windows applications, .NET projects |
| camelCase | `projectPlan.js` | JavaScript variables (not typically for filenames) |

**Recommendation for business documents:** kebab-case or snake_case are both excellent. kebab-case is slightly more readable; snake_case has wider legacy compatibility. The critical rule is: **pick one and be consistent**.

### Date Formats in Filenames

The only acceptable date format for filenames is **ISO 8601: YYYY-MM-DD** (e.g., `2026-02-07`). This ensures:
- Chronological sorting works automatically
- No ambiguity between DD/MM and MM/DD
- International clarity (important in the South African context where both formats appear)

### Version Numbering

- Simple: `v1`, `v2`, `v3` appended to filename
- Semantic: `v1.0`, `v1.1`, `v2.0` (major.minor)
- Date-based: `YYYY-MM-DD` as version proxy (good for documents that are updated in place)
- Avoid: `_final`, `_final_v2`, `_FINAL_REALLY_FINAL` -- use version numbers instead

### General Rules

1. No spaces in filenames -- use hyphens or underscores
2. No special characters (`@`, `!`, `#`, `&`)
3. All lowercase (prevents case-sensitivity issues across operating systems)
4. Short but descriptive -- aim for clarity without excessive length
5. Leading zeros for numbered sequences (`01`, `02`, ... `10` not `1`, `2`, ... `10`)
6. Date at the start if chronological sorting matters; at the end if categorical sorting matters

Sources: [IT Glue - Naming Conventions Best Practices](https://www.itglue.com/blog/naming-conventions-examples-formats-best-practices/), [Camphouse - Naming Conventions Guidelines](https://camphouse.io/blog/naming-conventions), [FreeCodeCamp - Case Differences](https://www.freecodecamp.org/news/snake-case-vs-camel-case-vs-pascal-case-vs-kebab-case-whats-the-difference/)

---

## 6. Document Numbering Systems

### Common Schemes

**Simple Prefix + Sequential:**
```
SOP-001    (Standard Operating Procedure #1)
WI-012     (Work Instruction #12)
FRM-003    (Form #3)
POL-001    (Policy #1)
```

**Department/Category Prefix + Sequential:**
```
IT-SOP-001     (IT department, SOP #1)
FIN-FRM-002    (Finance, Form #2)
PRJ-PLN-001    (Project, Plan #1)
```

**Client + Document Type + Sequential:**
```
ACME-PRO-001   (Acme Corp, Proposal #1)
ACME-INV-042   (Acme Corp, Invoice #42)
```

**For a small IT services company, a practical scheme:**
```
[CLIENT]-[TYPE]-[SEQ]
e.g., ACME-SOP-001, ACME-NET-001
```

Or even simpler for internal documents:
```
[TYPE]-[SEQ]
e.g., SOP-001, POL-001, TMP-001
```

**Key principles:**
- Minimum 3 digits for sequential numbers (allows growth to 999)
- Keep the scheme simple enough that you will actually use it
- The numbering system must be documented somewhere (even a single line in a README)
- Once assigned, a number is never reused, even if the document is retired

Sources: [The ECM Consultant - Document Control Numbering](https://theecmconsultant.com/document-control-numbering/), [Assai Software - Document Numbering](https://assai-software.com/effective-document-numbering-for-document-control/), [Folderit - Document Numbering System](https://www.folderit.com/blog/document-numbering-system-document-control/)

---

## 7. Solo Operator / Freelancer Practical Structures

Research across freelancer and consultant communities reveals a convergent pattern:

### The "Three Pillars" Structure

Most successful solo operators organize at the top level into:

1. **Clients** (external work)
2. **Business** (your own company operations)
3. **Knowledge** (reference material, templates, learning)

### Per-Client Structure

```
/clients/
    /client-name/
        /_admin/          (contracts, proposals, invoices)
        /_brand/          (client logos, style guides)
        /project-name-1/
            /input/       (what client supplied)
            /wip/         (work in progress)
            /output/      (deliverables sent to client)
        /project-name-2/
            ...
```

### Per-Project Naming

The recommended pattern for project folders is:
```
YYYY-MM_client-name_project-description
```
Example: `2026-02_acme-mining_scada-upgrade`

This ensures chronological sorting while remaining human-readable.

### What Works at 30-50 Concurrent Projects

At this scale, the research consistently recommends:
- **Flat client list, nested projects** -- do not create intermediate grouping folders (by industry, by year, etc.) as they add navigation overhead
- **Consistent templates** -- create a blank project folder template and duplicate it for each new project
- **Active vs. Archive separation** -- move completed projects to an archive folder (or prefix with `_archive/`) to keep the active workspace manageable
- **Weekly filing discipline** -- set aside 30 minutes weekly to move loose files into their proper locations
- **Use the "Inbox" pattern** -- have a single `_inbox/` folder at the top of your workspace for unsorted items. Process it regularly. This prevents "desktop dumping."

### Tools That Scale

For 30-50 projects, a filesystem-based approach (with sync/backup) remains viable and is preferred by many consultants over SaaS tools because:
- No vendor lock-in
- Works offline
- Full-text search via OS tools
- Integrates with git for versioned technical content
- Lower ongoing cost

Sources: [FreelancerMap - How to Organize Folders](https://www.freelancermap.com/blog/organising-files-as-a-freelancer/), [Marc Ashwell - How to Organize Client Folders](https://marcashwell.medium.com/how-to-organize-your-client-folders-24a24d78e2e6), [File Architect - Consulting Deliverables](https://filearchitect.com/blueprints/business-freelance/consulting-deliverables), [World Bank - Folder Naming Conventions](https://worldbank.github.io/template/docs/folders-and-naming.html)

---

## 8. South African Compliance Considerations

### SARS Record-Keeping Requirements

| Legislation | Record Type | Retention Period |
|---|---|---|
| Tax Administration Act (s29) | Tax returns, supporting records | 5 years from date of submission |
| Tax Administration Act | Records where no return required | 5 years from end of relevant tax period |
| Companies Act, 2008 | General company records (documents, accounts, books) | 7 years minimum |
| Companies Act, 2008 | Annual financial statements | 15 years |
| Companies Act, 2008 | Accounting records and supporting schedules | 15 years |

**Critical exceptions:** If SARS has notified you of an audit or investigation, records must be kept until the process concludes. In cases of fraud or misrepresentation, SARS can reopen assessments indefinitely -- meaning records may need to be kept indefinitely.

**What to keep:** Invoices (issued and received), receipts, payroll records, VAT documents, tax returns, bank statements, contracts, and proof of payment. Both paper and digital formats are acceptable, but digital records must be secure and accessible.

### POPIA (Protection of Personal Information Act)

Required documentation and practices:
1. **Data inventory:** Document all personal information your organization processes -- customer data, employee records, supplier contacts
2. **Privacy policy:** A public statement of how you collect, use, and protect personal information
3. **Consent records:** You must be able to verify consent in case of complaint or audit
4. **Operator agreements:** Written contracts with any third party processing data on your behalf
5. **Breach notification procedures:** Documented process for notifying the Information Regulator and affected parties
6. **Data retention schedule:** You may not keep personal information longer than necessary for the purpose it was collected
7. **Information Officer registration:** Must be registered with the Information Regulator

**Practical implication for folder structure:** Client folders containing personal information should be clearly separated from publicly shareable project deliverables. Access controls (even basic file permissions or encrypted folders) are advisable.

### B-BBEE (Broad-Based Black Economic Empowerment)

- Under R10 million annual turnover: Get a B-BBEE Affidavit (self-declared via sworn affidavit)
- R10 million or more: Requires a formal B-BBEE verification certificate from an accredited agency
- Keep records of: ownership structure, management control, skills development spend, enterprise development contributions, preferential procurement

### Other Compliance Documentation

- **CIPC:** Company registration documents, annual returns
- **UIF/SDL/COIDA:** Employment-related statutory registrations and returns (if employing staff)
- **OHS Act:** Occupational Health and Safety records (relevant if you have premises or do on-site work)

Sources: [SARS - Record Keeping](https://www.sars.gov.za/businesses-and-employers/small-businesses-taxpayers/starting-a-business-and-tax/record-keeping/), [Fincor - Retention of Records](https://fincor.co.za/taxpayers-and-retention-of-records-as-per-the-tax-administration-and-companies-acts/), [Ready Accounting - Record Keeping 2025](https://www.readyaccounting.co.za/record-keeping-requirements-south-africa-2025/), [Scytale - POPIA Compliance Checklist](https://scytale.ai/resources/how-to-achieve-popia-compliance-complete-checklist/), [LabourNet - POPIA for SMEs](https://www.labournet.com/a-10-step-popia-compliance-checklist-for-south-african-smes/), [SME South Africa - Legal Requirements](https://smesouthafrica.co.za/sme-guides/legal-requirements-to-start-a-business-in-south-africa/)

---

## 9. Synthesis: What Is Realistic vs. Enterprise Bloat

### Enterprise Bloat (Skip This)

These are practices from large organizations that add overhead without value for a solo or small operation:

- **Separate document controller role** -- you are the document controller
- **Multi-level approval workflows** -- you approve your own work; client sign-off is the only external approval that matters
- **Formal change control boards** -- track changes in git or version numbers; no committee needed
- **Separate quality manual, quality policy, management review** as standalone documents -- combine them into a single business-operations document
- **ITIL service catalogue with formal SLA documentation** for each service tier -- a simple services-and-pricing document suffices
- **Formal risk registers per project** -- a section in the project plan is enough for most projects
- **Complex multi-segment document numbering** (e.g., `DIV-DEPT-CAT-SUB-SEQ-REV`) -- unnecessary below 10 employees

### What Is Realistic and Valuable (Do This)

For a one-person IT services / automation company in South Africa handling 30-50 concurrent projects:

**Top-Level Structure:**
```
/business/
    /admin/                  (company registration, CIPC, B-BBEE affidavit)
    /finance/                (invoices, receipts, bank statements, tax returns)
    /legal/                  (contracts-templates, POPIA-policy, insurance)
    /operations/             (SOPs, internal procedures, service catalogue)
    /templates/              (project templates, document templates, proposal templates)

/clients/
    /client-name/
        /_admin/             (contracts, NDAs, contact details)
        /YYYY-MM_project-name/
            /01-specs/       (requirements, FDS, scope)
            /02-design/      (drawings, configs, source code)
            /03-deliverables/(what goes to the client)
            /04-admin/       (quotes, invoices, change orders, meeting notes)

/knowledge/
    /vendor-docs/            (datasheets, manuals, licence keys)
    /training/               (courses, certifications, study notes)
    /reference/              (standards, code snippets, boilerplate)

/_archive/                   (completed projects moved here annually)
```

**Naming Convention:**
- All lowercase
- kebab-case (hyphens between words)
- Dates as YYYY-MM-DD
- Project folders: `YYYY-MM_client-name_project-description`
- Documents: `descriptive-name_vN.ext` or `YYYY-MM-DD_descriptive-name.ext`
- No spaces, no special characters

**Document Numbering (Keep It Simple):**
- Internal: `SOP-001`, `POL-001`, `TMP-001`
- Client proposals: `PRO-CLIENTCODE-001`
- Client invoices: `INV-CLIENTCODE-YYYYMM-001`
- Only number documents that need formal tracking; not everything needs a number

**Version Control:**
- For code and technical configs: use git
- For documents: append `_v1`, `_v2` etc., or use date-based naming
- Never use `_final` -- use version numbers

**Compliance Minimum:**
- Keep financial records for 5 years (7 years for safety, given Companies Act)
- Have a written POPIA privacy policy (even a single page)
- Maintain a basic data inventory (a spreadsheet listing what personal data you hold and why)
- Keep B-BBEE affidavit current (annual)
- Back up everything -- SARS digital records must be accessible on request

**Weekly Maintenance Routine:**
- Process the inbox/downloads folder
- File loose documents into their project folders
- Back up to offsite/cloud
- Time: 30 minutes per week

This structure is directly informed by ISO 9001 principles (controlled documentation, version control, records retention), ITIL/MSP practices (client-centric organization, SOPs, strategy documentation), PMI lifecycle phases (numbered subfolders within projects), ISA-95 deliverables (specs, hardware, software, testing, handover), and South African compliance requirements (retention periods, POPIA, SARS) -- while stripping away everything that requires a team to maintain.
