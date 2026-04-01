# Discovery Question Bank

Use in Q&A mode — present one section at a time. Skip questions whose answers are already clear from context. In paste mode, use this as a checklist to identify gaps.

---

## Section 1: Project Basics
1. What are you building? (what it does, who uses it)
2. Is this for a client, or an internal/personal project?
3. What's the project name? (used to name files and personalize agent descriptions)
4. What stage is this? (greenfield, early MVP, existing codebase being extended)

---

## Section 2: Tech Stack
5. Frontend: framework/library? (React, Next.js, Vue, Nuxt, SvelteKit, React Native, plain HTML, none)
6. Backend: language and framework? (Node/Express, Node/Fastify, Python/FastAPI, Python/Django, Rails, Go, none/serverless)
7. Database: type and ORM? (PostgreSQL, MySQL, MongoDB, SQLite + Prisma/Drizzle/Sequelize/raw SQL)
8. Hosting/deployment: where does this run? (Vercel, Railway, AWS, GCP, Fly.io, self-hosted, unknown)
9. Key third-party integrations? (Stripe, Twilio, SendGrid, Auth0, Supabase, S3, OpenAI, etc.)
10. CI/CD setup? (GitHub Actions, GitLab CI, CircleCI, none yet)
11. Preferred model balance? (cost vs quality — e.g., Sonnet for most agents, Opus only for orchestrator)

---

## Section 3: Domain & Business Logic
12. What are the main entities in this system? (e.g., User, Order, Product, Vendor, Subscription)
13. What's the most financially or reputationally sensitive part of this system? (payments, user data, compliance, etc.)
14. Are there any workflows that need to be rock-solid? (checkout, auth, data pipelines, real-time features)
15. Any regulatory or compliance requirements? (GDPR, PCI, HIPAA, SOC2, etc.)

---

## Section 4: Client Context (for client projects)
16. Does the client have a preferred tech stack or constraints you must work within?
17. Does the client have an existing design system, component library, or brand guidelines?
18. Is there an existing codebase to integrate with, or is this greenfield?
19. What does "done" look like — what will be handed off? (deployed app, source code + docs, training, etc.)
20. Is there a hard deadline or launch target?

---

## Section 5: Team & Workflow
21. Who else is working on this? (solo, pair, small team, larger team)
22. What branching strategy? (trunk-based, feature branches, gitflow)
23. How do deployments work (or how should they work)? (manual, automated on merge, scheduled)
24. Where does the project live? (GitHub org/repo, GitLab, local only)

---

## Section 6: Key Developer Workflows
25. What tasks will you repeat most often during development? (running tests, deploying, seeding the DB, running migrations, generating reports, etc.)
26. Are there any domain-specific workflows that take multiple steps today? (e.g., "to add a new product I have to do X, Y, Z")
27. Are there any workflows that are error-prone or easy to forget steps on?

---

## Section 7: Autonomy Preferences
28. How much autonomy do you want the orchestrator to have? (supervised — pauses at milestones, autonomous — auto-advances when criteria pass, strict-autonomous — no escalation at all)
29. For task failures, should the system retry and self-heal before asking you, or escalate immediately?

---

## Inference Defaults (when information is missing)

| Unknown | Default assumption |
|---|---|
| Hosting | Vercel (frontend) + Railway (backend) |
| CI/CD | GitHub Actions |
| Branching | Feature branches → main |
| Test framework | Vitest (JS/TS), pytest (Python) |
| Team size | Solo developer |
| Timeline | No hard deadline |
| Design system | None (use Tailwind defaults) |
| Compliance | None specified |
| Autonomy mode | Supervised |
| Model balance | Sonnet for all agents |
| Retry policy | 4 retries, refine-then-split strategy |

Always state assumptions explicitly in the CLAUDE.md "Assumptions" section if key details were inferred rather than provided.
