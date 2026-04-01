---
name: run
description: Autonomous execution loop for TenantFlow. Plans tasks, assigns agents, validates results, self-heals on failure. Use `/run --plan` to generate a plan without executing. Use `/run` to start or resume execution.
---

# Run

Autonomous execution loop for TenantFlow.

## Usage
- `/run --plan` — decompose project into milestones and tasks, show the plan, don't execute
- `/run` — start or resume execution from current state
- `/run --task m1-t3` — execute a single specific task
- `/run --milestone m2` — execute all tasks in milestone 2

## Execution Loop

### 0. Reconcile State (always first)
- Read `.claude/workspace/orchestrator_state.json` if it exists
- Read `.claude/tasks.json`
- Scan `.claude/workspace/` for result files
- If a task is marked `done` in tasks.json but has no result file → mark as `review`
- If a result file exists but tasks.json shows `pending` → validate and mark `done` if criteria pass
- Write reconciled state to `orchestrator_state.json`

### 1. Generate dashboard
- Copy dashboard template to `.claude/workspace/dashboard.html`

### 2. Pick next ready task
- Find the highest-priority task with status `pending` and all dependencies in status `done`

### 3. Assign to agent
- Use CLAUDE.md agent routing to select the correct agent

### 4. Validate result
- Read the agent's result file from `.claude/workspace/[task-id].result.md`
- Check each acceptance criterion — pass or fail
- If all pass → mark task `done`, log to `progress.log`
- If any fail → enter self-healing pipeline

### 5. Self-healing pipeline (on failure)
- Simple failure → retry once with hint
- Structural failure → invoke problem-solver
- Problem-solver pipeline: refine → split → reassign → escalate

### 6. Milestone boundary
- Auto-advance if `auto_advance_milestones` is true and all tasks pass

### 7. Completion check
- Check project completion criteria from CLAUDE.md
