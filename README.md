<img width="830" height="300" alt="claude-code-team-builder" src="https://github.com/user-attachments/assets/e0fb3bda-476e-438c-98c3-53f40f0bda67" />

[![MIT License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![v1.0.0](https://img.shields.io/badge/release-v1.0.0-green)](https://github.com/azadmotala/claude-code-team-builder/releases/tag/v1.0.0)


A Claude Code skill that builds a self-healing AI development team for your software project.

Tell it what you're building and it writes a full `.claude/` directory: an orchestrator, specialist agents, routing rules, execution skills, and a CLAUDE.md that Claude Code reads at the start of every session. The orchestrator plans the work, hands each task to the right agent, and checks what comes back. When something fails, it works out why and tries a different approach before it comes to you. You review the plan, then let it run.

---

## Why This Exists

Most multi-agent setups need something running outside your editor: cloud APIs, external services, a Python framework. This one is a folder of files.

- **Lives in your repo.** Everything sits in `.claude/` as plain markdown. No services to run, no database, nothing extra to host.
- **Built for Claude Code.** It's written for Claude Code's own agents and skills from the start, not ported from a general-purpose framework.
- **Fixes its own failures.** A failed task gets classified, then retried, rewritten, split, or handed to another agent. You only hear about it if none of that works.
- **Nothing advances on vibes.** Every task has explicit acceptance criteria, and the orchestrator checks the result against them before anything moves forward.
- **Picks up where it left off.** Close a session halfway through and the next one works out where things stood, then carries on.

---

## Key Features

**An orchestrator and a problem-solver.** The orchestrator plans, assigns, and checks. When a task fails, the problem-solver works out what went wrong and rewrites the task, splits it, or hands it to another agent. It gets up to 4 attempts before it escalates.

**Three autonomy modes.** `supervised` stops at each milestone so you can review. `autonomous` moves on by itself when the criteria pass. `strict-autonomous` never stops to ask.

**State that survives a crash.** Every session starts by syncing `tasks.json`, the workspace result files, and `orchestrator_state.json`. Interrupted sessions, manual edits, and crashed processes all get straightened out before any new work starts.

**Easy on tokens.** The orchestrator keeps a one-line summary of each finished task rather than the full result, so context grows with the number of tasks, not with how much each one wrote. You can run planning on Opus and validation on Haiku. And it won't split work finer than it needs to: fewer tasks means fewer handoffs, and handoffs are where the tokens go.

**A dashboard you can leave open.** One self-contained HTML file that reads task state from disk and refreshes every 5 seconds. Milestone progress, task status, and an activity timeline, all in your browser.

**Nothing generic.** Agent descriptions name your stack, skills call your real commands, and routing follows your domain. If you're on Prisma and Stripe, the files say Prisma and Stripe, not "database" and "payments".

---

## Quick Start

### 1. Install the skill

```bash
git clone https://github.com/azadmotala/claude-code-team-builder.git

mkdir -p ~/.claude/skills/claude-code-team-builder
cp -r claude-code-team-builder/skill/* ~/.claude/skills/claude-code-team-builder/
```

### 2. Run it

In Claude Code, say something like:

```
Set up a new project
```

or

```
Build a team for my Next.js marketplace app
```

### 3. Answer the questions

It'll ask how you want to do this: **paste mode** (dump everything you know in one go) or **Q&A mode** (it asks, you answer). Either way, it needs three things:

1. What you're building, and what it's for
2. Your tech stack (frontend, backend, database)
3. The hard parts: payments, auth, real-time, compliance, whatever's riskiest

It fills in the rest with sensible defaults.

### 4. Plan, then run

```
/run --plan          # see the plan first; nothing runs yet
/run                 # start working through it
/status              # check progress any time
/dashboard           # set up the visual tracker
```

---

## What Gets Generated

```
your-project/
└── .claude/
    ├── CLAUDE.md                              ← project brain, read every session
    ├── settings.json                          ← autonomy, retry policy, model tiers
    ├── agents/
    │   ├── orchestrator/AGENT.md              ← plans, assigns, validates, loops
    │   ├── problem-solver/AGENT.md            ← self-healing, task repair
    │   ├── test-engineer/AGENT.md             ← mandatory quality gate
    │   ├── documentation-writer/AGENT.md      ← PRDs before development
    │   └── [project-specific]/AGENT.md
    ├── skills/
    │   ├── run/SKILL.md                       ← autonomous execution loop
    │   ├── status/SKILL.md                    ← project state reporting
    │   ├── dashboard/SKILL.md                 ← visual progress tracker
    │   ├── deploy/SKILL.md
    │   ├── test/SKILL.md
    │   ├── review/SKILL.md
    │   └── [domain skills]/SKILL.md
    └── workspace/                             ← result files, state, progress log, dashboard
```

### Mandatory Agents (every project)

| Agent | Role |
|---|---|
| `orchestrator` | Plans tasks, assigns agents, validates results, drives execution |
| `problem-solver` | Diagnoses failures, rewrites tasks, splits complex work, suggests reassignment |
| `test-engineer` | Validates every feature against acceptance criteria |
| `documentation-writer` | PRDs before development, specs for handoff |

### Additional Agents (added by stack)

| Signal | Agent |
|---|---|
| Full-stack framework (Next.js, Nuxt, SvelteKit) | `fullstack-developer` |
| Separate frontend and backend | `frontend-developer` + `backend-developer` |
| Complex database / schema-heavy | `database-architect` |
| Deployment / CI/CD | `devops-engineer` |
| Client project / sensitive logic | `code-reviewer` |
| Payments / billing | `payments-engineer` |
| Real-time / WebSockets | `streaming-engineer` |
| Existing client design system | `design-system-integrator` |
| Auth / OAuth / compliance | `auth-security-engineer` |
| ML / AI features | `ml-engineer` |
| Mobile (iOS / Android / React Native) | `mobile-developer` |

### Skills

| Skill | Always | Purpose |
|---|---|---|
| `/run` | Yes | Autonomous execution loop with state reconciliation |
| `/status` | Yes | Project state: done, in progress, blocked, failed, next |
| `/dashboard` | Yes | Generate visual HTML progress tracker |
| `/deploy` | When hosting target exists | Build, test gate, deploy to staging/production |
| `/test` | When tests exist | Run unit + integration + e2e suite |
| `/review` | Client projects | Security, correctness, quality review |
| `/migrate` | Relational database | Run ORM migrations |
| `/pr` | GitHub/GitLab pull requests | Pull request workflow |
| `/seed` | Dev seed data exists | Seed the development database |
| `/changelog` | Client expects release notes | Release notes for versioned deliverables |
| Domain skills | Derived from project | `/process-refund`, `/onboard-tenant`, etc. |

---

## How It Works

The skill works through five phases:

1. **Discovery**: finds out what you're building, from your paste or through Q&A
2. **Agent selection**: picks the four mandatory agents, plus specialists that fit your stack and how complex the project is
3. **Skill selection**: adds execution, workflow, and domain skills
4. **File generation**: writes every file in `.claude/` for your project. The sections that control behavior (state management, the self-healing pipeline, task sizing rules) are copied word for word from the templates, because the agents need the edge cases a summary would drop.
5. **Validation**: checks its own output. The mandatory agents are there, the copied sections are complete, every description mentions your real stack, and `settings.json` has the autonomy and self-healing config.

### The Execution Loop

Once you've approved the plan, `/run` goes round this loop until the project is done or something needs you:

```
/run --plan → Review → /run → Orchestrator loops:
  ↓
  Reconcile state (sync tasks.json ↔ workspace ↔ orchestrator_state.json)
  ↓
  Pick next ready task → Assign to agent → Validate result
  ↓                                          ↓
  Pass → mark done, advance          Fail → classify failure
                                       ↓              ↓
                                    Simple          Structural
                                    (retry once)    (problem-solver)
                                                      ↓
                                                   Refine → Split → Reassign → Escalate
```

---

## Example Output

[`examples/saas-dashboard/`](examples/saas-dashboard/) is a complete example of what the builder generates, for a multi-tenant SaaS dashboard on Next.js, Prisma, PostgreSQL, Clerk auth, and Stripe billing. Have a look before you run it on your own project.

---

## Configuration

### Autonomy Modes

Set `autonomy.mode` in `settings.json`:

| Mode | Behavior |
|---|---|
| `supervised` | The default. Stops at each milestone so you can review, and comes to you when self-healing can't fix a failure. |
| `autonomous` | Moves to the next milestone on its own when the criteria pass. Only stops for a catastrophic failure. |
| `strict-autonomous` | Never stops to ask. The problem-solver handles everything, and a task that still fails after max retries gets skipped. |

### Model Tiers

Planning needs the strongest reasoning. Checking a result against its criteria doesn't. So agents are grouped into three tiers, and you pick a model for each under `model_tiers` in `settings.json`:

| Tier | Agents | Default | Cost-optimized | Quality-maximized |
|---|---|---|---|---|
| Planning | orchestrator, problem-solver | sonnet | sonnet | opus |
| Execution | developer agents, devops | sonnet | sonnet | sonnet |
| Validation | test-engineer, code-reviewer, docs | sonnet | haiku | sonnet |

---

## Customization

It's all plain text in your repo. Once it's generated, change whatever you like:

- Add agents for roles the builder didn't think of
- Rewrite skill workflows to match the commands you actually use
- Keep CLAUDE.md up to date as the project changes
- Switch autonomy mode or retry policy in `settings.json`
- Add a domain skill whenever you catch yourself doing the same steps twice

---

## Limitations

- Works best on scoped features and small-to-medium projects, roughly 25 tasks or fewer
- Very large or very vague projects will still need a lot of human oversight
- The builder sets up the team. It doesn't write source code, PRDs, or architecture docs; the agents it creates do that
- The more detail you give it, the better the agents it builds

---

## Roadmap

- Parallel tasks, so more than one agent can work at once
- A CLI installer (`npx claude-code-team-builder init`)
- A GitHub template repo for one-click setup
- A VS Code extension for the dashboard

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- A project idea (even a rough one works)

---

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues, feature requests, and pull requests are all welcome.
