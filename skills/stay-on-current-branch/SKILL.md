---
name: stay-on-current-branch
description: >
  Keeps all code edits on the currently checked-out git branch. Prohibits
  creating, switching to, or renaming branches unless the user explicitly
  requests it in the same turn. Use always at session start, before any git
  command, when implementing features, committing, pushing, or opening PRs —
  and whenever another skill or workflow would create a branch by default.
---

# Stay on current branch

**Default:** work on whatever branch is already checked out. All edits and commits
stay there until the user explicitly asks for a new branch.

## Hard rule

Do **not** create, switch to, or rename a branch unless the user **explicitly**
requests it in the **same turn**, using clear intent such as:

- "create a branch", "new branch", "branch off", "checkout -b", "git switch -c"
- "rename this branch", "move this work to a branch called …"

If the user did not ask, **never** run:

- `git checkout -b …` / `git switch -c …`
- `git branch …` (when the goal is to start work on a new branch)
- `gh pr create` flows that include "Create new branch if needed" without the
  user having asked for a branch first

## Allowed without explicit branch request

- `git status`, `git diff`, `git log`, `git branch` (read-only)
- `git add`, `git commit` on the **current** branch when the user asked to commit
- `git push` on the **current** branch when the user asked to push
- `git checkout <existing-branch>` only when the user explicitly asked to switch
  to that branch by name

## When branch naming is wrong

If another workflow (e.g. **linear-issues** `PREFIX-XXX` or **github-issues** `#N` traceability) expects
`prefix-123-slug` (prefix from `conductor/linear.md`) but the current branch does not match:

1. **Stay on the current branch** and continue editing.
2. **Mention once** that the branch name does not follow convention — do not
   create or rename unless the user asks.

## Explicit branch creation (only when asked)

When the user asks for a new branch:

1. Confirm the base (usually current `HEAD` unless they specify otherwise).
2. Create with their name or a sensible `<prefix>-<num>-<slug>` if they tied it to
   an issue.
3. Then continue edits on that new branch.

## Conflicts with other instructions

This skill **overrides** implicit branch creation in:

- PR-creation workflows ("create new branch if needed")
- Linear / Conductor checklists ("create/rename branch if missing")
- Agent habits (branching "to keep main clean" without being asked)

Only explicit user instruction in the current turn wins over this skill's
prohibition — not inferred intent from issue IDs or naming conventions.
