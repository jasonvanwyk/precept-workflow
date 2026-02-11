# AI-Powered Services Strategy for Precept Systems

**Author:** Claude Opus 4.6 + Jason van Wyk
**Date:** 2026-02-11
**Source:** Analysis of market dynamics, the SaaS repricing event of January 2026, and Precept Systems' existing capabilities
**Purpose:** Define how Precept Systems can leverage AI workflow transformation both internally and as a client-facing service offering

---

## Executive Summary

In January 2026, a 200-line open-source prompt plugin from Anthropic wiped $285 billion from the enterprise software market in 48 hours. The plugin itself was unremarkable -- what it revealed was structural: the per-seat SaaS pricing model that underpins the entire enterprise software economy is breaking. AI agents don't need logins, don't need seats, and don't pay license fees.

Simultaneously, KPMG forced a 14% fee reduction from their auditor Grant Thornton UK -- not by deploying AI, but by using the *existence* of AI as negotiation leverage. This pattern will cascade across every knowledge-work fee structure.

Precept Systems is already building the right foundation with Claude Code, MCP integrations, and agentic workflows. This document outlines how to extend that foundation into a client-facing service offering that positions Precept on the right side of this transition.

---

## 1. The Market Shift

### What Changed

| Before | After |
|--------|-------|
| Software priced per human seat | AI agents do work without logging in -- seat model breaks |
| "Buy" always cheaper than "build" for enterprise tools | AI-powered custom builds now viable for many workflows |
| Professional services fees scale with headcount | Clients can point at AI economics and demand rate cuts |
| Bolting AI onto existing workflows feels productive | Only ground-up workflow rethinking changes outcomes |

### What Survived

Two edges remain durable even as pricing models collapse:

1. **Data edge** -- Proprietary databases, structured workflows, decades of accumulated enterprise data. A startup can't vibe-code Thomson Reuters' case law database in a weekend.

2. **Accountability edge** ("the single ringable neck") -- When something breaks at 2am before a board meeting, enterprises need a phone number to call and a contract that says someone is accountable. AI complexity makes this *more* important, not less.

### The KPMG Precedent

KPMG didn't automate their audit. They used the *existence* of AI as a negotiating weapon against Grant Thornton:

> "We both know AI changes the economics. Your old prices aren't justified anymore."

Grant Thornton blinked. Audit fees dropped from $416K to $357K (14%).

**This playbook will spread to every knowledge-work fee negotiation:** legal, consulting, implementation, design, and IT services. Clients don't need to deploy AI themselves -- they just need to point at the changed economics and ask about your rates.

---

## 2. Precept's Current Position

### Already Building the Right Way

Precept is not "bolting on" AI. The precept-workflow project is a ground-up rethinking of how work flows:

| Component | What It Does | Status |
|-----------|-------------|--------|
| Claude Code + MCP servers | AI agent with direct access to Google Workspace, GitHub, Telegram | Operational |
| Telegram bot | Mobile interface for photo filing, voice transcription, project queries | Deployed (awaiting secrets) |
| LocalSend + dev server | Bulk file transfer pipeline from field to central hub | Operational |
| Cloudflare Tunnel | Remote access from any device, anywhere | Operational |
| Agentic workflows | Slash commands, structured prompts, project conventions | In progress |

This is exactly the pattern Nate B Jones describes as the survival path: **agentic-first architecture** rather than chatbot-on-top.

### Precept's Durable Edges

1. **Domain expertise** -- Jason knows networking, infrastructure, and small/medium business IT intimately. AI can't replace that contextual understanding.

2. **Accountability** -- Precept is the ringable neck. When a client's network goes down or their workflow breaks, there's a real person with a real phone number.

3. **Trust relationships** -- Existing client relationships built over years. AI doesn't have those.

4. **Implementation skill** -- Knowing *which* AI tools to use, *how* to integrate them, and *what* to automate is itself a high-value skill that most businesses lack.

---

## 3. Service Offering: AI Workflow Transformation

### 3.1 Positioning

**Not:** "We'll add AI to your business."
**Instead:** "We'll rethink how your business works, using AI as the foundation -- and we'll be the ones accountable when it matters."

This positions Precept as the accountability layer + the expertise layer, which are the two edges that survive the SaaS repricing.

### 3.2 Service Tiers

#### Tier 1: AI Workflow Audit (Entry Point)

**What:** Assess a client's current workflows and identify where they're "bolting on" AI vs where ground-up rethinking would deliver real value.

**Deliverable:** Written report with prioritised recommendations, estimated impact, and implementation roadmap.

**Value to client:** Clarity on where AI actually helps vs where it's theatre. Prevents wasted spend on chatbots that don't change outcomes.

**Effort:** 1-2 days depending on business complexity.

#### Tier 2: Custom Agentic Solutions (Core Offering)

**What:** Build bespoke AI-powered workflows tailored to the client's specific business. This is the "build" side of the flipping buy-vs-build equation.

**Examples:**
- Custom document processing pipelines (invoices, quotes, contracts)
- Automated reporting from multiple data sources into a single dashboard or doc
- Field data capture workflows (photos, voice notes, forms) that auto-file and auto-process
- Client communication automation (email drafts, follow-ups, status updates)
- Project management workflows connecting their existing tools

**Value to client:** A tool designed for *their* company, not every company. No per-seat fees. Precept maintains it.

**Effort:** Days to weeks depending on scope. The "articulation problem" (extracting what the client actually needs vs what they say they need) is the main cost -- the building is fast.

#### Tier 3: SaaS Spend Optimisation

**What:** Review a client's current software subscriptions and identify where AI-powered alternatives or custom builds could replace expensive per-seat tools.

**Deliverable:** Cost-benefit analysis comparing current SaaS spend vs AI-powered alternatives, with risk assessment.

**Value to client:** Direct cost savings. The KPMG playbook applied to their business -- either replace tools or renegotiate vendor pricing using the changed economics as leverage.

**Effort:** 1-2 days for audit, ongoing for implementation.

#### Tier 4: Managed AI Operations (Recurring Revenue)

**What:** Ongoing management and evolution of AI workflows built in Tier 2. Monitor, maintain, update, and expand as the client's needs change and AI capabilities evolve.

**Value to client:** The "ringable neck." They get cutting-edge AI workflows without needing in-house AI expertise. Precept stays current with the tools (which change weekly) so they don't have to.

**Value to Precept:** Recurring revenue. Relationship deepening. First call for new projects.

**Effort:** Retainer model -- hours per month scaled to client size.

### 3.3 Target Clients

| Segment | Why They're a Fit |
|---------|-------------------|
| **Small professional services firms** (accounting, legal, engineering) | Facing the KPMG-style fee pressure from their own clients. Need to cut costs or demonstrate AI adoption. Can't afford enterprise AI consultants. |
| **SMEs with heavy admin overhead** | Document processing, invoicing, reporting, compliance -- all ripe for AI workflow transformation. |
| **Field services businesses** | Photo documentation, site reports, time tracking, job costing -- the exact workflows Precept is already building for itself. |
| **Any business paying >R20K/month in SaaS fees** | Likely candidates for SaaS spend optimisation. Some of those seats may be replaceable. |

---

## 4. Competitive Positioning

### The Articulation Problem

Nate B Jones identifies the hardest problem in AI-powered software: when a client says "I need a better way to track X," that sentence contains less than 5% of the information needed to build a useful tool. The other 95% is buried in how the team actually works -- unspoken conventions, exceptions, priorities, context.

**This is where Precept has a structural advantage over remote AI consultants and generic AI tools.** Precept works closely with local businesses, understands South African business context, and can spend the time extracting the real requirements through conversation, observation, and iteration.

The articulation problem is not solved by better AI. It's solved by a skilled human who understands the client's domain and can translate between what they say and what they need. That's Precept's role.

### Differentiation

| Competitor | Their Approach | Precept's Edge |
|------------|---------------|----------------|
| Generic AI consultancies | Expensive, enterprise-focused, cookie-cutter frameworks | Precept is local, hands-on, SME-focused, builds real things |
| DIY / "vibe coding" | Client tries to build their own tools with ChatGPT | Lacks the articulation layer, no accountability, breaks when it gets hard |
| SaaS vendors "adding AI" | Bolt-on features, same per-seat pricing | Precept builds purpose-built tools, no seat fees |
| Big tech AI platforms | Powerful but generic, requires expertise to use | Precept is the expertise layer that makes these tools actually useful |

---

## 5. Internal Priorities

### Immediate (This Quarter)

1. **Complete Telegram bot deployment** -- This is a live demo of the field-capture workflow. Every client conversation can reference "here's what we built for ourselves."

2. **Build 2-3 internal workflow automations** -- Document processing, project reporting, client communication. These become case studies and templates for client work.

3. **Document the stack** -- What tools, what integrations, what patterns. This becomes the foundation for repeatable client deployments.

### Next Quarter

4. **Pilot with 1-2 existing clients** -- Start with Tier 1 (audit) to identify opportunities, then move to Tier 2 (build) for the highest-value workflows.

5. **Package and price the offerings** -- Formalise the tier structure, create proposal templates, define scope boundaries.

6. **Stay current** -- The tools change weekly. Allocate time to evaluate new capabilities (Claude Co-work, Codex, Frontier, etc.) and update the internal stack accordingly.

---

## 6. Delivery Toolkit: Anthropic Developer Console

The Anthropic Developer Console has evolved from a simple API dashboard into a structured, data-driven prompt engineering platform. These tools are how Precept builds, tests, and deploys AI workflows for clients -- they turn prompt engineering from guesswork into a repeatable, quality-controlled process.

### Core Tools

| Tool | Purpose | Link |
|------|---------|------|
| **Anthropic Console** | Central hub for all developer activities | [console.anthropic.com](https://console.anthropic.com) |
| **Prompt Generator** | Describe a task in plain English; it generates a professional, multi-layered system prompt | [Prompt Generator Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator) |
| **Workbench** | Interactive playground to test, refine, and save prompts against real data | [Console Workbench](https://console.anthropic.com/workbench) |
| **Evaluations** | Run a prompt against dozens of test cases simultaneously to compare performance | [Evaluation Docs](https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool) |
| **Prompt Caching** | Reduce costs (up to 90%) and latency for repetitive, long-context prompts | [Prompt Caching Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) |

### How These Tools Map to Service Delivery

#### Automated Troubleshooting Blueprints
Use the Prompt Generator to create a system prompt that takes raw server logs and outputs a standardised "Incident Summary" and "Recommended Fix." Test in the Workbench using actual historical logs to verify the advice is technically sound before deploying to a client.

#### SLA & Contract Analysis
For clients with multiple contracts, use Prompt Caching. Cache the Master Service Agreement text so that when Claude checks a specific ticket against SLA terms, you're not paying to re-read the entire contract every time. Up to 90% cost reduction on repetitive contract queries.

#### Quality Assurance for Support Tickets
Use the Evaluation tool to test a "Customer Response" prompt. Upload 50 sample customer queries and compare two prompt versions side-by-side to see which handles technical jargon more accurately or maintains a better professional tone. Data-driven prompt refinement, not guesswork.

#### Code Documentation & Migration
For legacy system migrations, use the Workbench to build prompts that convert old scripts (Bash, Perl, etc.) into modern Python or Terraform, ensuring consistent documentation styles across the board.

### Why This Matters for the Service Offering

These tools solve the **quality assurance problem** for AI services. When Precept builds a workflow for a client:

1. **Prompt Generator** creates the initial system prompt from a plain-English task description
2. **Workbench** lets you iterate with real client data before deployment
3. **Evaluations** prove the workflow works at scale across many test cases
4. **Prompt Caching** keeps production costs manageable for high-volume workflows

This means Precept can demonstrate measurable, testable quality to clients -- not "we tried a prompt and it seemed to work," but "we tested this against 50 real scenarios and here are the results." That's the difference between a professional service and a DIY experiment.

---

## 7. Risks and Mitigations


| Risk | Mitigation |
|------|-----------|
| **AI capabilities change too fast** -- what you build today may be obsolete in months | Build modular, prompt-driven workflows that can be updated without full rebuilds. Stay current with tools. |
| **Clients don't see the value** -- "we're fine with our current tools" | Lead with the KPMG story and concrete cost savings. Tier 1 audit is low-risk entry point. |
| **The articulation problem** -- building the wrong thing because requirements were misunderstood | Iterate fast, show working prototypes early, maintain close client contact. This is Precept's advantage over remote/automated solutions. |
| **Race to the bottom on fees** -- if AI makes everything cheaper, margins compress | Position on accountability and expertise, not hours. Managed services (Tier 4) provides recurring revenue independent of hourly rates. |
| **Clients try DIY after seeing what's possible** | Fine -- Tier 4 (managed ops) captures clients who try DIY and discover the maintenance burden. The accountability edge means they come back. |

---

## 8. Key Takeaways

1. **The SaaS repricing is real and permanent.** Per-seat pricing is structurally broken. Every business that sells or buys knowledge work will be affected.

2. **The KPMG playbook will cascade.** Clients will use AI economics as leverage in every fee negotiation. Be on the right side of that conversation.

3. **"Bolting on" vs "rebuilding" applies at every scale.** Adding a chatbot to an unchanged workflow is decoration. Rethinking the workflow from the ground up is transformation. Precept should sell transformation.

4. **Data + accountability survive.** These are Precept's durable edges. Domain expertise, local presence, trust relationships, and the ringable neck.

5. **The window is open but compressing.** Every week brings new capabilities. First movers in the SME AI services space will build the client relationships and case studies that create a moat.

---

## References

- Nate B Jones, "The $285 Billion Crash Wall Street Won't Explain Honestly" ([YouTube](https://youtu.be/DGWtSzqCpog), [Channel](https://www.youtube.com/@NateBJones))
- Anthropic Developer Console tools walkthrough (Prompt Generator, Workbench, Evaluations, Prompt Caching)
- KPMG / Grant Thornton fee negotiation (Financial Times, January 2026)
- Bank of America analysis by Vivek Arya on SaaS sell-off internal inconsistency
- Jensen Huang, Cisco AI Summit remarks on software demand
- Nate B Jones' Substack: exercises for individual workflow transformation ([natebjones.com](https://www.natebjones.com/))
- Anthropic Developer Documentation ([docs.anthropic.com](https://docs.anthropic.com))
