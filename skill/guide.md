# Claude Code Team Builder: User Guide

## What It Does

You describe a software project. The team builder sets up an AI development team for it: agents, skills, routing rules, and an orchestrator that can run the project on its own.

Everything goes in a `.claude/` directory in your project root. Claude Code reads it at the start of every session, so you don't have to re-explain the project or hand out the work yourself.

---

## What You Need Before You Start

Have these four ready:

1. **What you're building.** Type and purpose. "A marketplace for freelance designers" or "An internal dashboard for tracking sales metrics."
2. **Your tech stack.** Frontend, backend, database. "Next.js, Prisma, PostgreSQL" or "HTML, CSS, vanilla JS."
3. **The hard parts.** Payments? Auth? Real-time features? Compliance? These decide which specialist agents get added.
4. **What done looks like.** Rough completion criteria are fine. "User can sign up, list a product, and check out" is enough.

The builder needs the first three before it can start. The fourth tells the orchestrator when to stop. It fills in the rest (hosting, CI/CD, branching strategy, team size) with sensible defaults.

---

## Installation

Copy the repo's `skill/` folder into your Claude Code skills directory:

```bash
git clone https://github.com/azadmotala/claude-code-team-builder.git

mkdir -p ~/.claude/skills/claude-code-team-builder
cp -r claude-code-team-builder/skill/* ~/.claude/skills/claude-code-team-builder/
```

You end up with:

```
~/.claude/skills/claude-code-team-builder/
├── SKILL.md
├── guide.md
└── references/
    ├── question-bank.md
    └── templates/
        ├── agents.md
        ├── skills.md
        ├── claude-md.md
        └── dashboard.html
```

The skill lives in your global skills directory, not inside a project, so it's there in every Claude Code session.

---

## How to Use It

### Step 1: Start the setup

In Claude Code, say something like:

- "Set up a new project"
- "Build a team for my marketplace app"
- "Create project setup for a Next.js SaaS platform"

The builder starts by asking whether you want **paste mode** (dump everything at once) or **Q&A mode** (guided questions). Pick whichever suits you.

### Step 2: Answer the questions

In paste mode, share your project description and the builder infers the rest. It asks at most 3 follow-up questions, and only about critical gaps.

In Q&A mode, the questions come a section at a time. Answer them all at once or one by one.

### Step 3: Review the output

The builder writes a `.claude/` directory containing:

- **CLAUDE.md:** your project's brain. Tech stack, domain concepts, agent routing, completion criteria, conventions. Claude reads it at the start of every session.
- **Agents:** specialists for your project. You always get the four mandatory ones (orchestrator, problem-solver, test engineer, documentation writer), plus developers, reviewers, and domain specialists that fit your stack.
- **Skills:** slash commands for common workflows. You always get `/run`, `/status`, and `/dashboard`, plus `/deploy`, `/test`, `/review`, and domain skills when your project calls for them.
- **team.json:** autonomy mode, retry policy, and the self-healing pipeline. Your project's own `.claude/settings.json` is left alone.
- **Workspace:** where agents write their result files and the orchestrator keeps its state. It starts out with only the dashboard file in it.

### Step 4: Plan the work

Run `/run --plan`. The orchestrator reads your CLAUDE.md, breaks the project into milestones and tasks, assigns each task to an agent, and shows you the plan.

Review it and adjust anything that looks wrong. Nothing runs until you start `/run`.

### Step 5: Execute

Run `/run` and the orchestrator takes over:

1. **Reconciles state:** syncs tasks.json, workspace results, and its own memory
2. Picks the next ready task
3. Assigns it to the right agent
4. The agent does the work and writes a result file
5. The orchestrator checks the result against the acceptance criteria
6. If it passes, the task is done
7. If it fails, self-healing kicks in: a simple failure gets one retry, and a structural one goes to the problem-solver to rewrite, split, or reassign the task
8. At milestone boundaries, what happens next depends on your autonomy mode
9. Repeat until the project completion criteria are met

### Step 6: Watch progress

You can follow along three ways:

- **Session output.** The orchestrator prints a one-liner after every task transition, like `✅ m1-t1 done (frontend-developer) → next: m1-t2`.
- **`/status`.** Run it any time for a full breakdown: what's done, in progress, blocked, failed, and next.
- **Dashboard.** Run `/dashboard`, then open `.claude/workspace/dashboard.html` in a browser. It refreshes every 5 seconds. If it's stuck on "Waiting for tasks.json...", which is common when you open it straight from disk, serve it from `.claude/` (one level up, where `tasks.json` lives) with `python -m http.server 8000`, then open `http://localhost:8000/workspace/dashboard.html`.

---

## What Gets Created

```
.claude/
├── CLAUDE.md                              ← project context, read every session
├── team.json                              ← orchestration + autonomy configuration
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
└── workspace/                             ← dashboard.html, result files, orchestrator_state.json, progress.log
```

The builder only writes inside `.claude/`. Source code, PRDs, and architecture docs come later, from the agents, once execution starts.

---

## Key Concepts

### Agents

Agents are specialists. Each one has a defined role, the parts of your stack it works with, and rules for when to use it. The orchestrator reads the routing table in CLAUDE.md to decide which agent gets each task.

Each agent lives in its own subfolder (`agents/[name]/AGENT.md`) and carries its own handoff protocol: the instructions for reporting results back to the orchestrator.

Every project gets four mandatory agents: the **orchestrator** (coordinates everything), the **problem-solver** (fixes failures), the **test engineer** (validates every feature), and the **documentation writer** (writes PRDs before development). The rest depend on your stack and how complex the project is.

### The Orchestrator

The orchestrator doesn't write code or tests. It plans, assigns, validates, and drives. It breaks your project into small, testable tasks, orders them by dependency, hands each one to the right agent, checks the result against its acceptance criteria, and keeps going until the project is done.

It keeps a memory in `orchestrator_state.json` (decisions made, failures hit, context notes), so it remembers what happened even when a session gets interrupted.

### The Problem-Solver

When a task fails, the orchestrator doesn't come straight to you. A simple failure, like a syntax error or a missing import, gets one retry with the same agent plus a hint. A structural one goes to the problem-solver: a wrong task breakdown, a missing dependency, vague criteria, or the wrong agent for the job.

The problem-solver reads the error context, works out what went wrong, and does one of three things. It rewrites the task with clearer instructions, splits it into smaller subtasks, or recommends a different agent. Self-healing gets up to 4 attempts before the orchestrator escalates to you (or skips the task, in strict-autonomous mode).

### State Reconciliation

At the start of every session, the orchestrator checks that its records agree. It reads `tasks.json`, scans the workspace for result files, and checks `orchestrator_state.json` for context from earlier sessions. If something doesn't line up, like a task marked done with no result file, or a result file whose task was never updated, it fixes that before carrying on. That's how it recovers from interrupted sessions, manual file edits, and crashed processes.

### Tasks

A task is the smallest piece of work that produces something testable. Each task has acceptance criteria, and the orchestrator only marks it done when they pass. Tasks can depend on each other, and a task doesn't start until everything it depends on is finished.

The orchestrator sizes tasks to fit the project. A single-file static page is one build task, not one task per HTML section. A multi-service app with 30+ files might have 15. The rule of thumb: if two pieces of work change the same file and have no outside dependencies, they're one task.

Tasks live in `.claude/tasks.json`, which the orchestrator creates when you run `/run --plan`.

### Skills

Skills are slash commands: multi-step workflows you trigger by name. `/run` starts the execution loop and `/status` shows where things stand. `/dashboard` sets up the visual tracker, and `/deploy` ships to staging or production. Domain skills like `/process-refund` or `/onboard-tenant` cover the workflows specific to your project.

### Handoff Protocol

Agents don't talk to each other. When an agent finishes a task, it writes a result file to `.claude/workspace/`. The orchestrator reads it, checks the work, and decides what happens next. That file is the single source of truth for how the task went, and each agent's AGENT.md has the instructions for writing it.

### Autonomy Modes

There are three, set with `autonomy.mode` in `team.json`:

| Mode | Behavior |
|---|---|
| `supervised` | The default. Stops at each milestone for your review, and comes to you when self-healing can't fix a failure. |
| `autonomous` | Moves to the next milestone on its own when the acceptance criteria pass. Only stops when a task still fails after self-healing. |
| `strict-autonomous` | Never stops to ask. The problem-solver handles everything, and a task that still fails after max retries gets skipped. |

Start with `supervised`. Move to `autonomous` once you trust its plans. Use `strict-autonomous` for batch runs you'll review afterwards.

### The Dashboard

One self-contained HTML file showing task status, progress bars, and an activity timeline. `/dashboard` sets it up. Open it in a browser and leave it open; it refreshes every 5 seconds.

---

## Common Commands

| Command | What it does |
|---|---|
| `/run --plan` | Create the task plan without running anything. |
| `/run` | Start or resume autonomous execution. |
| `/run --task m1-t3` | Run one task. |
| `/run --milestone m2` | Run every task in one milestone. |
| `/status` | Show what's done, in progress, blocked, failed, and next. |
| `/dashboard` | Generate or regenerate the visual dashboard. |
| `/test` | Run the project's test suite. |
| `/deploy` | Deploy to staging (default) or production. |
| `/review` | Code review for security, correctness, and quality. |

---

## Tips

**Start with `/run --plan`.** Review the plan before the orchestrator runs anything. A bad plan wastes more tokens than planning costs.

**Keep CLAUDE.md current.** The "Current Focus" section tells the orchestrator what to work on, and "Project Completion Criteria" tells it when to stop. Update both when priorities change.

**Start supervised, graduate to autonomous.** Run your first project in supervised mode. Once you've seen self-healing deal with most failures without you, switch to autonomous.

**Use the dashboard on longer projects.** For a 2-task test project, the session output is enough. On a 20-task build, the dashboard shows where everything stands without you scrolling through logs.

**Check `.claude/workspace/` when something fails.** Every agent writes a result file saying what it did, what passed, and what didn't. The problem-solver writes repair reports, and `orchestrator_state.json` logs every attempt and decision.

**Don't expect the problem-solver on every error.** Simple failures go straight back to the same agent for one retry, because a full diagnosis costs more tokens than a quick retry.

---

## Token Optimization

Three things keep token use in step with the size of the project:

**State summarization.** The orchestrator carries a one-line summary of each task in `orchestrator_state.json` and leaves the full result files on disk for debugging. It loads only what the current decision needs, so context grows steadily with the number of tasks and long result files stay out of it.

**Tiered model assignment.** Not every agent needs the same model. The builder asks how you want to balance cost and quality, then writes each agent's model into the `model:` line at the top of its `AGENT.md`:

| Tier | Default | Cost-optimized | Quality-maximized |
|---|---|---|---|
| Planning (orchestrator, problem-solver) | sonnet | sonnet | fable |
| Execution (developer agents, devops) | sonnet | sonnet | sonnet |
| Validation (test-engineer, code-reviewer, docs) | sonnet | haiku | sonnet |

The cost-optimized profile drops validation to haiku, since checking output against criteria is lighter work than planning or writing code. The quality-maximized profile moves planning up to fable, Anthropic's model for the hardest and longest-running work, for better task breakdowns and failure diagnosis. `opus` is the middle ground if Fable costs more than you want. These are Claude Code's model aliases, so each agent always gets the latest model in its family. To change a tier later, edit `model:` in each agent in that tier.

`/run` drives the loop from your main session, so the loop itself runs on that session's model. The planning tier covers the problem-solver, and the orchestrator whenever it runs as a subagent.

**Right-sized tasks.** The task sizing rules (see [Tasks](#tasks)) stop the orchestrator splitting work too finely. On a project with 1–3 output files, the orchestrator aims for 3–5 tasks in total, build and validation included. Fewer tasks means fewer agent runs and fewer result files to read back.
