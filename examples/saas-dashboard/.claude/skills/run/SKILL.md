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
- Read `.claude/team.json` for the autonomy `mode` and the `retry_policy`
- Read `.claude/workspace/orchestrator_state.json` if it exists
- Read `.claude/tasks.json`
- Scan `.claude/workspace/` for result files
- If a task is marked `done` in tasks.json but has no result file → mark as `review`
- If a result file exists but tasks.json shows `pending` → validate and mark `done` if criteria pass
- If a task is `in_progress` with no result file → the last session ended mid-task; set it back to `pending`
- If a task is `in_progress` with a result file → validate it now (step 4)
- If a task is `review` → check its acceptance criteria against the project files; mark `done` if they pass, otherwise `pending`
- If a task is `failed` and `attempts` is below `max_retries` → run the self-healing pipeline (step 5) for it before picking new work; at `max_retries`, escalate or skip
- Write status changes to `tasks.json` and the reconciled state to `orchestrator_state.json`
- This prevents drift from interrupted sessions or manual edits

### 1. Generate dashboard
- Copy `references/templates/dashboard.html` to `.claude/workspace/dashboard.html`
- Do NOT regenerate from scratch — always use the fixed template
- The dashboard reads `tasks.json` and `progress.log` dynamically via fetch

### 2. Pick next ready task
- Find the highest-priority task with status `pending` and all `depends_on` tasks in status `done`
- If no tasks are ready, check for blocked tasks and report why

### 3. Assign to agent
- Use CLAUDE.md agent routing to select the correct agent
- Mark the task `in_progress` in `tasks.json`
- Invoke the agent with the task definition and acceptance criteria

### 4. Validate result
- Read the agent's result file from `.claude/workspace/[task-id].result.md`
- Check each acceptance criterion — pass or fail
- If all pass → mark task `done`, log to `progress.log`
- If any fail → mark `failed` and add 1 to `attempts` in `tasks.json`, then enter self-healing pipeline

### 5. Self-healing pipeline (on failure)
Read retry policy from `.claude/team.json`. Classify the failure first:

**Simple failure** (syntax error, missing import, typo, wrong path):
- Retry once with the same agent plus a hint describing the error
- Do NOT invoke the problem-solver — the round-trip costs more than a retry
- If retry also fails → escalate to problem-solver

**Structural failure** (wrong decomposition, missing dependency, vague criteria):
- Invoke the problem-solver immediately

**Problem-solver pipeline** (when invoked):
1. **Refine** (attempts 1–2): problem-solver rewrites the task
2. **Split** (attempt 3): problem-solver decomposes into subtasks
3. **Reassign** (attempt 4): try a different qualified agent
4. **Escalate or skip**: in `supervised` or `autonomous` mode, pause and ask the human; in `strict-autonomous` mode, mark the task `skipped` and move on

Once the problem-solver has repaired a task, set it back to `pending` so step 2 picks it up again.

### 6. Milestone boundary
- When all tasks in a milestone are `done`:
  - If `mode` is `supervised` → pause and ask for human review
  - Otherwise → validate milestone outputs and advance

### 7. Completion check
- After each milestone, check project completion criteria from CLAUDE.md
- If all criteria met → report project complete
- If not → continue to next milestone
