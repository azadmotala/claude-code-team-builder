# Example Output: SaaS Dashboard

A complete example of what `claude-code-team-builder` generates.

## The Project

**TenantFlow** — a multi-tenant SaaS dashboard for freelancers to manage clients, invoices, and time tracking.

**Stack:** Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui, Prisma, PostgreSQL, Clerk (auth), Stripe Billing.

**Hosted on:** Vercel (frontend) + Railway (database).

## What Was Generated

7 agents (4 mandatory + 3 project-specific), 8 skills (3 execution + 5 workflow/domain), CLAUDE.md, and settings.json with supervised autonomy mode.

### Why These Agents

- **orchestrator** + **problem-solver** — mandatory on every project
- **test-engineer** + **documentation-writer** — mandatory on every project
- **fullstack-developer** — Next.js App Router is full-stack, so vertical slicing beats splitting frontend/backend
- **payments-engineer** — Stripe Billing is central to the business model
- **code-reviewer** — client deliverable, quality matters at handoff

### Why These Skills

- `/run`, `/status`, `/dashboard` — always included (execution skills)
- `/deploy` — Vercel hosting configured
- `/test` — Vitest + Playwright
- `/review` — client project quality gates
- `/migrate` — PostgreSQL with Prisma ORM
- `/onboard-tenant` — most repeated domain workflow
