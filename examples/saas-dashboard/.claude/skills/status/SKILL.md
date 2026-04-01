---
name: status
description: Show current project state for TenantFlow. Reports what's done, in progress, blocked, failed, and next. Run any time to see where the project stands.
---

# Status

Reports project state for TenantFlow.

## Workflow

1. **Read state** — load `tasks.json` and `orchestrator_state.json`
2. **Categorize tasks**:
   - ✅ Done — completed and validated
   - 🔄 In progress — currently assigned
   - 🚫 Blocked — dependencies not met
   - ⏳ Pending — ready but not started
   - 🔴 Failed — exceeded retry limit
3. **Show milestone progress** — percentage complete per milestone
4. **Show recent activity** — last 5 entries from `progress.log`
5. **Show next action** — what the orchestrator will do next
6. **Show failures** — any tasks that failed with attempt count and reason

## Output format
Print to console. Group by milestone. Show counts at the top: `Done: X | In Progress: X | Blocked: X | Pending: X | Failed: X`
