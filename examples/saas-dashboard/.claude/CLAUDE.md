# TenantFlow

## What We're Building
A multi-tenant SaaS dashboard for freelancers to manage clients, track time, and send invoices. Each freelancer gets their own workspace with isolated data. Currently greenfield — building toward MVP.

Built with: Next.js 14 + Prisma + PostgreSQL · Hosted on Vercel + Railway · Client project

---

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| Backend | Next.js API routes, Prisma ORM, PostgreSQL |
| Auth | Clerk (multi-tenant with organizations) |
| Payments | Stripe Billing (subscription tiers: Free, Pro, Team) |
| Hosting | Vercel (app), Railway (PostgreSQL) |
| CI/CD | GitHub Actions → auto-deploy on merge to main |
| Testing | Vitest, Playwright |

---

## Key Domain Concepts
- **Tenant**: A freelancer's workspace. All data is tenant-scoped — queries must always filter by `tenantId`.
- **Client**: A tenant's customer. Has contact info, project history, and billing status.
- **TimeEntry**: Logged hours against a client/project. Billable or non-billable.
- **Invoice**: Generated from billable time entries. States: draft → sent → paid → overdue.
- **Subscription**: Stripe Billing subscription. Controls feature access (Free: 3 clients, Pro: unlimited, Team: multi-user).
- **Tenant isolation is non-negotiable**: Every database query, API route, and server action must scope to the authenticated tenant.

---

## Agent Routing

| Task type | Use |
|---|---|
| Planning, task assignment, validation, coordination | `orchestrator` (always highest priority) |
| Task failure, self-healing, task repair | `problem-solver` |
| Full features (UI + API + DB) | `fullstack-developer` |
| Stripe billing, subscriptions, webhooks | `payments-engineer` |
| Tests, validation, CI quality gates | `test-engineer` |
| PRDs, specs, API docs, client updates | `documentation-writer` |
| Pre-merge review, security, client delivery | `code-reviewer` |

---

## Available Skills (Slash Commands)
- `/run` — Start or resume autonomous execution. `--plan` to generate plan only. `--task [id]` for single task.
- `/status` — Show what's done, in progress, blocked, and next
- `/dashboard` — Generate the visual progress tracker HTML
- `/deploy` — Deploy to Vercel (staging default, `--prod` for production)
- `/test` — Run Vitest unit tests + Playwright e2e
- `/review` — Code review for security, correctness, tenant isolation
- `/migrate` — Run pending Prisma migrations
- `/onboard-tenant` — Walk through new tenant setup (Clerk org + Stripe customer + seed data)

---

## Project Conventions
- API routes live in `src/app/api/` using Next.js App Router conventions
- Components co-located with tests: `Button.tsx` + `Button.test.tsx`
- Prisma schema is the source of truth — never modify the database directly
- Never commit `.env` — update `.env.example` instead
- Use shadcn/ui components first — don't create custom alternatives
- Every database query must include a `tenantId` filter. No exceptions.
- Server actions and API routes must verify tenant ownership before mutations

---

## Project Completion Criteria
- [ ] User can register, create a tenant workspace, and log in
- [ ] Client management: add, edit, archive clients (tenant-scoped)
- [ ] Time tracking: log hours against clients, mark billable/non-billable
- [ ] Invoice generation: create invoices from billable time entries
- [ ] Stripe billing: Free/Pro/Team tiers with feature gating
- [ ] All milestones in tasks.json are complete
- [ ] No tasks remain in status `pending` or `failed`
- [ ] Deployed to staging and smoke-tested

---

## Task Sizing
- A task is the smallest unit of work that produces a testable deliverable
- Do not split work below the file boundary unless sections are independently testable by different agents
- If two pieces of work modify the same file with no external dependencies, they are one task
- If two validation checks read the same file, use the same agent, and share the same dependencies, they are one task
- This is a multi-service app with 30+ files — target 10–15 total tasks
- Tenant isolation validation is part of every code review task, not a separate task

---

## Current Focus
MVP: tenant registration → client management → time tracking → invoice generation. Target: staging deploy by end of sprint.

---

## Assumptions
- Vercel for hosting (inferred — not specified by client)
- GitHub Actions for CI/CD (inferred)
- Feature branches → main (inferred)
- No compliance requirements specified
- Autonomy mode set to supervised. Change in settings.json to autonomous or strict-autonomous.
