<img width="830" height="300" alt="claude-code-team-builder" src="https://github.com/user-attachments/assets/2d90ba94-7729-4dce-9a30-6c47b1ec5628" />

# claude-code-team-builder

[![MIT License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![v1.0.0](https://img.shields.io/badge/release-v1.0.0-green)](https://github.com/azadmotala/claude-code-team-builder/releases/tag/v1.0.0)


A Claude Code skill that generates a complete, self-healing AI development team for any software project.

Describe what you're building. It creates an orchestrator, specialist agents, routing rules, execution skills, and a project brain — a full `.claude/` directory that Claude Code reads at every session start. The orchestrator plans the work, assigns tasks to the right agent, validates results, and self-heals when things fail. You review the plan, then let it run.

---

## Why This Exists

Most multi-agent setups require external infrastructure, cloud APIs, or Python frameworks. This one is different:

- **Repo-local.** Everything lives in `.claude/` — plain markdown files. No external services, no databases, no cloud dependencies.
- **Claude Code-native.** Built for Claude Code's agent and skill system. Not a generic framework adapted to fit.
- **Self-healing.** Failed tasks get classified, retried, rewritten, or split automatically before asking you for help.
- **Deterministic.** Tasks have explicit acceptance criteria. The orchestrator validates every result. Nothing advances on vibes.
- **Persistent.** State reconciliation across sessions means interrupted work picks up where it left off.

---

## Key Features

**Orchestrator + Problem-Solver architecture.** The orchestrator plans, assigns, and validates. When tasks fail, the problem-solver diagnoses the issue and rewrites, splits, or reassigns the task — up to 4 attempts before escalating.

**Three autonomy modes.** `supervised` pauses at milestones for your review. `autonomous` auto-advances when criteria pass. `strict-autonomous` handles everything without interruption.

**State reconciliation.** Every session starts by syncing `tasks.json`, workspace result files, and `orchestrator_state.json`. Interrupted sessions, manual edits, and crashed processes get corrected automatically.

**Token optimization.** State summarization keeps context growth linear. Tiered model assignment lets you run planning on Opus and validation on Haiku. Right-sized task decomposition prevents over-decomposition — fewer tasks means fewer token-expensive handoffs.

**Visual dashboard.** A self-contained HTML file that reads task state from disk and auto-refreshes every 5 seconds. Milestone progress, task status, activity timeline — all in the browser.

**Project-specific everything.** Every agent description names your actual technologies. Every skill references your actual commands. Every routing rule maps to your actual domain. No generic placeholders survive generation.

---

## Quick Start

### 1. Install the skill

```bash
git clone https://github.com/azadmotala/claude-code-team-builder.git

mkdir -p ~/.claude/skills/claude-code-team-builder
cp -r claude-code-team-builder/skill/* ~/.claude/skills/claude-code-team-builder/
```

### 2. Run it

In Claude Code, say:

```
Set up a new project
```

or

```
Build a team for my Next.js marketplace app
```

### 3. Answer the questions

Choose **paste mode** (dump everything at once) or **Q&A mode** (guided questions). Three things are required:

1. What you're building (type + purpose)
2. Your tech stack (frontend, backend, database)
3. The hard parts (payments, auth, real-time, compliance)

Everything else gets inferred with reasonable defaults.

### 4. Plan and execute

```
/run --plan          # Review the task decomposition first
/run                 # Start autonomous execution
/status              # Check progress any time
/dashboard           # Generate the visual tracker
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
| Domain skills | Derived from project | `/process-refund`, `/onboard-tenant`, etc. |

---

## How It Works

The skill runs through five phases:

1. **Discovery** — collects project details via paste mode or guided Q&A
2. **Agent selection** — picks mandatory + specialist agents based on stack and complexity
3. **Skill selection** — adds execution, workflow, and domain skills
4. **File generation** — creates all `.claude/` files with project-specific content, copying structural sections (state management, self-healing pipeline, task sizing rules) verbatim from templates
5. **Validation** — verifies mandatory agents exist, structural sections are complete, descriptions reference the actual stack, and settings.json has autonomy + self-healing configuration

### The Execution Loop

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

See [`examples/saas-dashboard/`](examples/saas-dashboard/) for a complete generated output — a multi-tenant SaaS dashboard built with Next.js, Prisma, PostgreSQL, Clerk auth, and Stripe billing.

---

## Configuration

### Autonomy Modes

Set in `settings.json`:

| Mode | Behavior |
|---|---|
| `supervised` | Pauses at milestone boundaries for review. Escalates on failure after self-healing. Default. |
| `autonomous` | Auto-advances milestones when criteria pass. Escalates only on catastrophic failure. |
| `strict-autonomous` | No escalation. Problem-solver handles everything. Failed tasks skipped after max retries. |

### Model Tiers

Not every agent needs the same model:

| Tier | Agents | Default | Cost-optimized | Quality-maximized |
|---|---|---|---|---|
| Planning | orchestrator, problem-solver | sonnet | sonnet | opus |
| Execution | developer agents, devops | sonnet | sonnet | sonnet |
| Validation | test-engineer, code-reviewer, docs | sonnet | haiku | sonnet |

---

## Customization

Everything is plain markdown. Edit anything after generation:

- Add agents for roles the builder didn't anticipate
- Modify skill workflows to match your actual commands
- Update CLAUDE.md as the project evolves
- Change autonomy mode or retry policy in settings.json
- Add domain skills as new workflows emerge

---

## Limitations

- Best for scoped features and small-to-medium projects (up to ~25 tasks)
- Very large or highly ambiguous systems may still need significant human oversight
- The builder creates the development environment — not source code, PRDs, or architecture docs
- Quality of output depends on quality of input (more detail = better agents)

---

## Roadmap

- Parallel task execution (multiple agents working simultaneously)
- CLI installer (`npx claude-code-team-builder init`)
- GitHub template repo for one-click setup
- VS Code extension for dashboard integration

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- A project idea (even a rough one works)

---

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Contributions, issues, and feature requests welcome.
