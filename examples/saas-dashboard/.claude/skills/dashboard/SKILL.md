---
name: dashboard
description: Generate the visual dashboard for TenantFlow. Copies the fixed dashboard template to the workspace. The dashboard reads tasks.json and progress.log from disk and auto-refreshes every 5 seconds.
---

# Dashboard

Copies the dashboard template to `.claude/workspace/dashboard.html`.

## Workflow

1. **Copy the template** — copy `references/templates/dashboard.html` to `.claude/workspace/dashboard.html`
2. **Do NOT regenerate the HTML from scratch** — always use the fixed template
3. **Instruct user**: "Open in a browser. Serve with `python -m http.server 8000` from `.claude/workspace/` for auto-refresh."

## How the dashboard works
- Reads `tasks.json` and `progress.log` via fetch (relative paths)
- Auto-refreshes every 5 seconds
- Shows: status counts, overall progress bar, milestone progress bars, task list with status badges, activity timeline
- No generation needed — the same HTML file works for any project because it reads task data dynamically

## Important
- The dashboard must be served from `.claude/workspace/` so it can find `tasks.json` and `progress.log`
- If `tasks.json` is in `.claude/` (one level up), the dashboard tries `../tasks.json` as a fallback
- The template lives in `references/templates/dashboard.html` — do not modify it per project
