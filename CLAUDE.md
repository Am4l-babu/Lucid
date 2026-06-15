# Claude Instructions — Lucid

This file defines how Claude must behave when helping any team member work on this project.

---

## Commits & Credit

- **Never** add `Co-Authored-By: Claude` or any AI attribution to commits.
- Commits are credited solely to the human working. Use their git config as-is.
- Keep commit messages short and descriptive of what changed.

---

## Workflow — Follow This Every Single Time

Before touching any code, Claude must walk the user through these steps in order. Do not skip or reorder.

### Step 1 — Update PROGRESS.md on main first

Before creating any branch or writing any code:

1. Pull latest main
2. Open `PROGRESS.md`
3. Find the component being worked on
4. Set its status to `🔄 Ongoing`
5. Set `Assigned To` to the current user's GitHub username
6. Commit this change directly to `main` with message: `progress: mark <component> as ongoing [@username]`
7. Push to main

This must happen before any feature branch is created.

### Step 2 — Create a feature branch

Branch naming format:
```
feature/<component-name>
```

Examples:
```
feature/whatsapp-integration
feature/archive-search
feature/ego-analysis
feature/drift-alerts
feature/gmail-connector
```

```bash
git checkout main
git pull origin main
git checkout -b feature/<component-name>
```

### Step 3 — Do the work

Build the component on the feature branch. Commit regularly with clear messages.

### Step 4 — Push to the feature branch

```bash
git push origin feature/<component-name>
```

### Step 5 — Create PR to `development`

- PR must go from `feature/<component-name>` → `development`
- Never PR directly to `main`
- PR title format: `[Component Name] — brief description`
- After PR is created, update `PROGRESS.md` on main: set status to `👀 In Review`

### Step 6 — On merge

Once the PR is merged into `development`, update `PROGRESS.md` on main: set status to `✅ Done`

---

## Branch Rules Summary

| Branch | Purpose |
|---|---|
| `main` | Stable. Only PROGRESS.md updates and hotfixes land here directly |
| `development` | Integration branch. All feature PRs merge here |
| `feature/*` | One branch per component. Short-lived |

---

## PROGRESS.md

`PROGRESS.md` is the single source of truth for what's happening on the project. It lives on `main` and is updated directly (not via PR) to reflect real-time status. Always keep it accurate.

---

## General Rules

- Read `PROGRESS.md` at the start of every session to understand current state
- Never work on a component already marked `🔄 Ongoing` by someone else without checking with that person first
- Ask the user for their GitHub username if it isn't clear from git config
