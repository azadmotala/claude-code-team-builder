# Software Project Team Builder — User Guide

## What It Does

You describe a software project. The team builder creates a complete AI development environment — agents, skills, routing rules, and an orchestration layer that can run the project autonomously.

The output is a `.claude/` directory that you drop into your project root. Claude Code reads it at every session start. No re-explaining the project. No manual coordination.

---

## What You Need Before You Start

Four things. That's it.

1. **What you're building.** Type and purpose. "A marketplace for freelance designers" or "An internal dashboard for tracking sales metrics."
2. **Your tech stack.** Frontend, backend, database. "Next.js, Prisma, PostgreSQL" or "HTML, CSS, vanilla JS."
3. **The hard parts.** Payments? Auth? Real-time features? Compliance? This determines which specialist agents get added.
4. **What done looks like.** Even rough completion criteria. "User can sign up, list a product, and check out" is enough.

Everything else — hosting, CI/CD, branching strategy, team size — can be inferred with reasonable defaults.

---

## Installation

Drop the `software-project-team-builder` folder into your Claude Code skills directory:

```
~/.claude/skills/software-project-team-builder/
├── SKILL.md
├── references/
│   ├── question-bank.md
│   └── templates/
│       ├── agents.md
│       ├── skills.md
│       └── claude-md.md
└── software-project-team-builder-guide.md
```

The skill lives in your global Claude Code skills directory (`~/.claude/skills/`), not inside any specific project. Once installed, it's available in every Claude Code session.

---

## How to Use It

### Step 1: Start the setup

In Claude Code, say something like:

- "Set up a new project"
- "Build a team for my marketplace app"
- "Create project setup for a Next.js SaaS platform"

The team builder will ask whether you want **paste mode** (dump everything at once) or **Q&A mode** (guided questions). Pick whichever suits you.

### Step 2: Answer the questions

In paste mode, share your project description and the builder infers the rest. It may ask up to 3 follow-up questions for critical gaps.

In Q&A mode, questions come in sections. Answer them all at once or one by one.

### Step 3: Review the output

The builder generates a `.claude/` directory containing:

- **CLAUDE.md** — your project's brain. Tech stack, domain concepts, agent routing, completion criteria, conventions. Claude reads this at every session start.
- **Agents** — specialists assigned to your project. Always includes four mandatory agents: the orchestrator, problem-solver, test engineer, and documentation writer. Adds developers, reviewers, and domain specialists based on your stack.
- **Skills** — slash commands for common workflows. Always includes `/run`, `/status`, and `/dashboard`. Adds `/deploy`, `/test`, `/review`, and domain-specific skills based on your project.
- **settings.json** — orchestration configuration: autonomy mode, retry policy, self-healing pipeline.
- **Workspace** — an empty directory where agents write result files and the orchestrator writes persistent state during execution.

### Step 4: Plan the work

Run `/run --plan` in Claude Code. The orchestrator reads your CLAUDE.md, decomposes the project into milestones and tasks, assigns each task to the right agent, and shows you the plan.

Review it. Adjust if needed. This is a dry run — nothing executes until you approve.

### Step 5: Execute

Run `/run`. The orchestrator takes over:

1. **Reconciles state** — syncs tasks.json, workspace results, and its own memory
2. Picks the next ready task
3. Assigns it to the right agent
4. The agent does the work and writes a result file
5. The orchestrator validates the result against acceptance criteria
6. If it passes, the task is done
7. If it fails, the self-healing pipeline kicks in — the problem-solver rewrites, splits, or reassigns the task before retrying
8. At milestone boundaries, behavior depends on your autonomy mode
9. Repeat until the project completion criteria are met

### Step 6: Watch progress

Three ways to see what's happening:

- **Session output.** The orchestrator prints a one-liner after every task transition. You'll see `✅ m1-t1 done (frontend-developer) → next: m1-t2` in real time.
- **`/status`** command. Run it any time for a full breakdown: what's done, what's in progress, what's blocked, what's next, and what failed.
- **Dashboard.** Run `/dashboard` to generate `dashboard.html`. Open `.claude/workspace/dashboard.html` in a browser. It auto-refreshes every 5 seconds. For reliable auto-refresh, serve it with `python -m http.server 8000` from the `.claude/workspace/` directory.

---

## What Gets Created

Here's the full directory structure the builder produces:

```
.claude/
├── CLAUDE.md                              ← project context, read every session
├── settings.json                          ← orchestration + autonomy configuration
├── agents/
│   ├── orchestrator/AGENT.md              ← plans, assigns, validates, loops
│   ├── problem-solver/AGENT.md            ← self-healing, task repair
│   ├── test-engineer/AGENT.md             ← validates every feature
│   ├── documentation-writer/AGENT.md      ← PRDs before development
│   └── [project-specific]/AGENT.md
├── skills/
│   ├── run/SKILL.md                       ← autonomous execution loop
│   ├── status/SKILL.md                    ← project state reporting
│   ├── dashboard/SKILL.md                 ← visual progress tracker
│   └── [workflow + domain skills]
└── workspace/                             ← result files, orchestrator_state.json, progress.log
```

The builder does **not** create source code, PRDs, architecture docs, or anything outside `.claude/`. The agents do that once execution starts.

---

## Key Concepts

### Agents

Agents are specialists. Each one has a defined role, a specific tech stack it works with, and rules about when to use it. The orchestrator reads the routing table in CLAUDE.md and assigns tasks to the right agent.

Every agent lives in its own subfolder (`agents/[name]/AGENT.md`) and carries its own handoff protocol — the instructions for how it reports results back to the orchestrator.

Every project gets four mandatory agents: the **orchestrator** (coordinates everything), the **problem-solver** (fixes failures), the **test engineer** (validates every feature), and the **documentation writer** (PRDs before development). Additional agents are added based on your stack and complexity.

### The Orchestrator

The orchestrator doesn't write code or tests. It plans, assigns, validates, and drives. It decomposes your project into atomic tasks, sequences them by dependency, assigns each one to the right agent, checks results against acceptance criteria, and loops until the project is done.

It maintains persistent memory in `orchestrator_state.json` — decisions made, failures encountered, context notes — so it remembers what happened even across interrupted sessions.

### The Problem-Solver

When a task fails, the orchestrator doesn't immediately ask you for help. It sends the failure to the problem-solver agent first. The problem-solver reads the error context, diagnoses the issue, and takes one of three actions: rewrite the task with clearer instructions, split it into smaller subtasks, or recommend a different agent.

This self-healing pipeline runs up to 4 attempts before escalating (or skipping, in strict-autonomous mode). The result: fewer interruptions, more autonomous progress.

### State Reconciliation

At the start of every session, the orchestrator reconciles its state. It reads `tasks.json`, scans the workspace for result files, and checks `orchestrator_state.json` for context from previous sessions. If anything is out of sync — a task marked done with no result file, or a result file with no corresponding task update — it corrects the discrepancy before continuing.

This prevents drift from interrupted sessions, manual file edits, or crashed processes.

### Tasks

A task is the smallest unit of work that produces a testable deliverable. Each task has acceptance criteria that must pass before the orchestrator marks it done. Tasks have dependencies — nothing starts until everything it depends on is finished.

The orchestrator calibrates task granularity to the project's complexity. A single-file static page is one build task — not four tasks per HTML section. A multi-service app with 30+ files might have 15 tasks. The rule: if two pieces of work modify the same file with no external dependencies, they're one task.

Tasks live in `.claude/tasks.json`, which the orchestrator creates when you run `/run --plan`.

### Skills

Skills are slash commands — multi-step workflows you can trigger by name. `/run` starts the execution loop. `/status` shows project state. `/dashboard` generates the visual tracker. `/deploy` ships to staging or production. Domain skills like `/process-refund` or `/onboard-tenant` handle project-specific workflows.

### Handoff Protocol

Agents don't talk to each other directly. When an agent finishes a task, it writes a result file to `.claude/workspace/`. The orchestrator reads it, validates the work, and decides what happens next. Every agent carries its own handoff instructions in its AGENT.md file.

Result files are the single source of truth for task outcomes.

### Autonomy Modes

Three modes, configured in `settings.json`:

| Mode | Behavior |
|---|---|
| `supervised` | Pauses at milestone boundaries for human review. Escalates on failure after self-healing exhausted. Default. |
| `autonomous` | Auto-advances milestones when acceptance criteria pass. Escalates only on catastrophic failure. |
| `strict-autonomous` | No escalation. The problem-solver handles everything. Failed tasks are skipped after max retries. |

Start with `supervised`. Move to `autonomous` once you trust the task decomposition. Use `strict-autonomous` for batch execution where you'll review results afterward.

### The Dashboard

A self-contained HTML file that shows task status, progress bars, and an activity timeline. Generated by `/dashboard`. Open it in a browser and leave it running — it refreshes every 5 seconds.

---

## Common Commands

| Command | What it does |
|---|---|
| `/run --plan` | Create a task plan without executing. Review before you start. |
| `/run` | Start or resume autonomous execution. |
| `/run --task m1-t3` | Execute a single specific task. |
| `/run --milestone m2` | Execute all tasks in a specific milestone. |
| `/status` | Show what's done, in progress, blocked, failed, and next. |
| `/dashboard` | Generate/regenerate the visual dashboard HTML. |
| `/test` | Run the project's test suite. |
| `/deploy` | Deploy to staging (default) or production. |
| `/review` | Code review for security, correctness, and quality. |

---

## Tips

**Start with `/run --plan`.** Always review the task decomposition before letting the orchestrator execute. A bad plan wastes more tokens than the planning step costs.

**Keep CLAUDE.md updated.** The "Current Focus" section tells the orchestrator what to work on. The "Project Completion Criteria" section tells it when to stop. Update both when priorities shift.

**Start supervised, graduate to autonomous.** Run your first project in supervised mode. Once you see that the self-healing pipeline handles most failures without your input, switch to autonomous.

**Use the dashboard for longer projects.** For a 2-task test project, session output is enough. For a 20-task build, the dashboard gives you a birds-eye view without scrolling through logs.

**Check `.claude/workspace/` when something fails.** Every agent writes a result file explaining what it did, what passed, and what didn't. The problem-solver writes repair reports. `orchestrator_state.json` tracks every attempt and decision.

**The problem-solver handles structural failures, not every error.** Simple failures — a missing import, a syntax error — get one retry with the same agent plus a hint. The problem-solver only gets invoked for structural issues: wrong task decomposition, missing dependencies, contradictory acceptance criteria. This avoids burning tokens on a full diagnosis round-trip for trivial errors.

---

## Token Optimization

Three mechanisms keep token usage proportional to project complexity:

**State summarization.** The orchestrator carries one-line task summaries in `orchestrator_state.json`, not full result files. The detailed results stay on disk for debugging. The context window only loads what's needed for the current decision. This keeps context growth linear with task count, not exponential with output size.

**Tiered model assignment.** Not every agent needs the same model. Configure `model_tiers` in `settings.json`:

| Tier | Default | Cost-optimized | Quality-maximized |
|---|---|---|---|
| Planning (orchestrator, problem-solver) | sonnet | sonnet | opus |
| Execution (developer agents, devops) | sonnet | sonnet | sonnet |
| Validation (test-engineer, code-reviewer, docs) | sonnet | haiku | sonnet |

The cost-optimized profile drops validation to haiku — checking criteria against output is lighter work than planning or code generation. The quality-maximized profile upgrades planning to opus for better task decomposition and failure diagnosis.

**Right-sized decomposition.** The orchestrator's task-sizing rules prevent over-decomposition. A single-file project gets 3 tasks, not 8. Fewer tasks means fewer agent invocations, fewer result files, fewer context loads. The biggest token savings come from not creating unnecessary work in the first place.
