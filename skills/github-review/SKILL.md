---
name: github-review
description: >
  Canonical review protocol for any #N change — the review intent is the
  GitHub issue's acceptance criteria. Derive the diff scope from branch vs base
  (or a track's plan.md SHAs), load repo standards (code_styleguides + workflow.md
  Quality Gates), review the diff, run github-label-review, map findings back to
  the issue, and drive the GitHub state + finish comment. Use when finishing
  or reviewing GitHub-linked work. Activates only when conductor/github.md exists.
  Pairs with github-issues and github-label-review.
---

# GitHub review

The **canonical review protocol** for any `#N` change when GitHub-first is
on (`conductor/github.md` exists). Review intent comes from the **GitHub issue's
acceptance criteria** — the single source of the spec — and close-out updates
the GitHub issue. It applies whether or not the work has a `conductor/tracks/`
directory.

This skill **frames** the diff against the GitHub issue, reviews it, runs
`github-label-review`, then maps the results back onto the issue.

If `conductor/github.md` is absent, do not use this skill; use **conductor-review**
against `spec.md` / `plan.md`. If `linear.md` is also present, **HALT** and ask
which tracker file to keep.

## When this runs

- **On demand:** "review #12", "review this branch / PR", "is this ready to
  merge?", "review my changes" (when GitHub-first is on).
- **At session finish** (per **github-issues** §3) for any non-trivial change
  against a `#N` issue.
- **Via conductor-review** — that wrapper derives the revision range from the
  track's `plan.md` SHAs and adds track archival, then delegates here.

## Protocol

1. **Resolve the issue & scope.**
   - Resolve `#N` via **github-issues** §1 (prompt → branch name → recent
     commit subject). If still unknown, ASK once.
   - Derive the diff range from **branch vs base** (default `origin/main`):
     `git fetch origin main` then review `git diff origin/main...HEAD`. For
     uncommitted work, review the working tree. Confirm the range if ambiguous.

2. **Load the review intent (the issue is the spec).**
   - Fetch the **current** issue via GitHub MCP or `gh issue view N --json
     title,body,state,labels,parent` — **acceptance criteria**, current state,
     labels, parent. If the state/criteria no longer match what was built,
     pause and confirm.
   - If `gh` is unavailable, ask the user to paste the acceptance criteria.

3. **Load standards (repo-wide).**
   - `conductor/code_styleguides/*.md` — violations here are **High** severity.
   - The **Quality Gates** in `conductor/workflow.md` — they apply to every
     change (project test command, coverage target, no secrets).

4. **Review the diff.** Against the issue's acceptance criteria and the
   styleguides: correctness, tests for new logic, no unrelated edits, no
   secrets.

5. **Map findings back to the issue.** Check, against `#N`:
   - **Acceptance-criteria compliance** — did it build what the issue asked?
   - **Test presence** — new logic has tests; the project test command on the
     relevant files is green.
   - **Quality-Gate conformance** — styleguides, coverage, no secrets.

6. **Review GitHub labels.** Invoke **`github-label-review`** on the same
   diff/range. Confirm before applying via `gh issue edit`.

7. **Decide & act.** If there are Critical/High issues, recommend fixing them
   first; offer to apply the fixes, stop for a manual fix, or proceed. Then
   drive the issue **close-out** (below).

## Close out

- **Post the finish/PR-ready comment** to `#N`: what changed (1–3 bullets),
  the PR link if any, how to verify (project test command).
- **Update state** — apply `in-review` (if `github.md` defines it) only when
  the agent's code work is complete (committed + pushed, review findings
  resolved or accepted, checks green, PR open when one was requested).
  **Never close the issue from this skill** unless the user explicitly
  instructs it in the current session. See **github-issues** §3.
- **Apply the label delta** from step 6.
- Confirm the PR title is `#N: …` and the body links the issue **without**
  `Closes #N` unless the user authorized close.

## What this skill does not do

- It does not redefine `github-label-review` — it sequences it and binds the
  results to the GitHub issue.
- It does not create or archive Conductor tracks.
- It does not replace **conductor-review** for file-based (no `github.md`) projects.

## Pairs with

| Need | Skill |
|------|-------|
| Resolve #N, finish comment, state, labels taxonomy | **github-issues** |
| Label add/remove delta | **github-label-review** |
| Track lifecycle (file-based) | **conductor-review** |
