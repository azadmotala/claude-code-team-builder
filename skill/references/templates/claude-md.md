# CLAUDE.md Template

Fill in every section for the specific project. Remove sections that don't apply. Keep the whole file under 130 lines — it's read at every session start.

---

```markdown
# [Project Name]

## What We're Building
[2–3 sentences: what the product does, who uses it, current status.]

Built with: [frontend] + [backend] + [database] · Hosted on [hosting] · [Client/Internal] project

---

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | [e.g., Next.js 14, TypeScript, Tailwind CSS, shadcn/ui] |
| Backend | [e.g., Node.js, Prisma ORM, PostgreSQL] |
| Auth | [e.g., Clerk / NextAuth / custom JWT] |
| Payments | [e.g., Stripe Connect] |
| Hosting | [e.g., Vercel (frontend), Railway (backend + DB)] |
| CI/CD | [e.g., GitHub Actions → auto-deploy on merge to main] |
| Testing | [e.g., Vitest, Playwright] |

---

## Key Domain Concepts
<!-- Define the entities and rules Claude needs to reason about this project correctly. -->
- **[Entity 1]**: [definition and role in the system]
- **[Entity 2]**: [definition and role in the system]
- **[Key rule]**: [important business logic or constraint]
- **[Key rule]**: [e.g., "Payouts run weekly on Fridays via Stripe Connect transfers"]

---

## Agent Routing
<!-- Be explicit. Claude uses these rules to decide which agent to invoke. -->
<!-- Routing Priority: The orchestrator always has highest priority for planning, assignment, validation, and coordination tasks. -->

| Task type | Use |
|---|---|
| Planning, task assignment, validation, coordination | `orchestrator` (always highest priority) |
| Task failure, self-healing, task repair | `problem-solver` |
| [e.g., UI components, pages, client-side logic] | `frontend-developer` |
| [e.g., API routes, business logic, DB queries] | `backend-developer` |
| [e.g., Stripe, payments, billing, webhooks] | `payments-engineer` |
| [e.g., Schema design, migrations, query optimization] | `database-architect` |
| [e.g., Tests, validation, CI/CD quality gates] | `test-engineer` |
| [e.g., PRDs, specs, API docs, client updates] | `documentation-writer` |
| [e.g., Deployment, infrastructure, pipelines] | `devops-engineer` or `/deploy` |
| [e.g., Security review, pre-client delivery review] | `code-reviewer` |

---

## Available Skills (Slash Commands)
<!-- Execution -->
- `/run` — Start or resume autonomous execution. `--plan` to generate plan only. `--task [id]` for single task.
- `/status` — Show what's done, in progress, blocked, and next
- `/dashboard` — Generate/regenerate the visual progress tracker HTML

<!-- Workflow -->
- `/deploy` — [what it does, e.g., "Deploy to staging (default) or production with --prod flag"]
- `/test` — [e.g., "Run full test suite: unit + integration + e2e"]
- `/review` — [e.g., "Code review staged changes for security, correctness, and quality"]
- `/migrate` — [e.g., "Run pending Prisma migrations against the target environment"]

<!-- Domain -->
- `/[domain-skill]` — [e.g., "/process-refund — Walk through refund workflow for an order"]

---

## Project Conventions
<!-- Rules that apply to ALL work on this project. -->
- [e.g., "All API routes live in `src/app/api/` using Next.js App Router"]
- [e.g., "Components co-located with test files: `Button.tsx` + `Button.test.tsx`"]
- [e.g., "Prisma schema is the source of truth — never modify DB directly"]
- [e.g., "Never commit `.env` — update `.env.example` instead"]
- [e.g., "Design system: use shadcn/ui components first — don't create custom alternatives"]
- [e.g., "Every PR needs at least one passing e2e test for the changed flow"]

---

## Project Completion Criteria
<!-- Deterministic stopping point for the orchestrator. The project is complete when ALL of these are true. -->
- [ ] [e.g., "User can sign up, list a product, and check out"]
- [ ] [e.g., "All milestones in tasks.json are complete"]
- [ ] [e.g., "All acceptance criteria pass"]
- [ ] [e.g., "No tasks remain in status `pending` or `failed`"]
- [ ] [e.g., "No escalations are pending"]
- [ ] [e.g., "Deployed to staging and smoke-tested"]

---

## Task Sizing
<!-- Calibrate task granularity to project complexity. The orchestrator reads this when planning. -->
- A task is the smallest unit of work that produces a testable deliverable
- Do not split work below the file boundary unless sections are independently testable by different agents
- If two pieces of work modify the same file with no external dependencies, they are one task
- If two validation checks read the same file, use the same agent, and share the same dependencies, they are one task — not two
- For projects with 5 or fewer output files, all validation (testing, review, conventions) is one task — do not split into separate test and review tasks
- [e.g., "This is a single-file project — one build task, not one per section"]
- [e.g., "Target: 3–5 total tasks" / "Target: 8–15 total tasks" — scale to project size]

---

## Current Focus
<!-- Update this section as the project evolves. -->
[Describe the current sprint or milestone, e.g.: "MVP: user auth + product catalog. Target: deploy to staging by end of week."]

---

## Assumptions
<!-- Document anything inferred because it wasn't specified. -->
[e.g., "Assumed Vercel for hosting since not specified. Update if different."]
[e.g., "Autonomy mode set to supervised. Change in settings.json to autonomous or strict-autonomous."]
```
