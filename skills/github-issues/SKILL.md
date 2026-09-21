---
name: github-issues
description: >
  Human-convention workflow for linking agent work to GitHub issues (#N):
  resolve the issue at session start, keep branch/commit/PR traceability during
  work, and post a milestone comment plus status update before finishing. Use
  when the user mentions GitHub Issues, #N, an issue URL, starting or finishing
  issue work, opening a PR for a ticket, or prefixes a prompt with
  "GitHub: #N". Activates only when conductor/github.md exists.
  For Conductor tracks, see §6 — the GitHub issue is the spec.
---

# GitHub issues (#N)

This skill uses **human convention**, not hooks: the human (or prompt) names the
issue; the agent reads it, keeps git/PR traceability, and updates GitHub at
milestones via MCP when authenticated, else `gh`.

**Activate only when** `conductor/github.md` exists in the project. If it is
absent, do not follow this skill — Conductor is in file-based SDD
(`spec.md` / `tracks.md`) or Linear-first.

If `conductor/linear.md` **also** exists, **HALT** and ask which tracker file
to keep. Do not pick silently.

**Workspace:** read `conductor/github.md` in the **project** (not this plugin)
for owner, repo, and label taxonomy. Never hard-code a repo.

## Epics and sub-issues (GitHub model)

On GitHub, an **epic is a parent issue with sub-issues** — not a Project or
Milestone.

| Concept | What it is | `gh` / fields |
|---------|------------|---------------|
| **Epic** | A parent **issue** that groups child work | Has sub-issues; `gh issue view N --json parent,subIssues` |
| **Sub-issue** | A regular issue whose **parent** is another issue | `gh issue create --parent N`; `gh issue edit --parent` |
| **Project / Milestone** | Release grouping — orthogonal to parent-child | Orthogonal to epics |

**Agent rules:**

- Say **parent epic** or **epic issue** when you mean the parent `#N` that owns
  sub-issues. Do not treat "epic" as a synonym for **Project**.
- When fetching context, if the issue has a `parent`, note it. If it has
  `subIssues`, list them.
- **Every epic has a Conductor track (track check).** An epic **must** have a
  corresponding **epic track** — a `conductor/tracks/*/metadata.json` whose
  `github` is the epic id (`owner/repo#N`). Before starting sub-issue work,
  read the sub-issue's parent, search the tracks for that id, and open an epic
  track first if it is missing.
- A sub-issue's parent epic is the issue's GitHub `parent` — read it from
  `gh issue view`, not from a duplicated `metadata.json` field.

## Creating issues (default state)

When creating a new GitHub issue (`gh issue create`, or GitHub MCP):

| Kind | Default | Rule |
|------|---------|------|
| **Top-level** (no `--parent`) | **Open** | No extra status label unless `github.md` defines one and the user named it. |
| **Sub-issue** (`--parent N`) | **Open** | Always stay open. Do not close to match the parent. |

**Hard rules:**

- Do not close a newly created issue.
- Sub-issues are queue work under a parent — leave them **open**.
- Same defaults apply to every create path: GitHub MCP, Conductor new-track,
  and handoff child issues.

## 1. Session start (always)

Copy this checklist and complete before coding:

```
GitHub start:
- [ ] Issue ID resolved (#N from conductor/github.md owner/repo)
- [ ] Issue fetched or user pasted acceptance criteria
- [ ] Status: Open; apply in-progress label if github.md defines it
- [ ] Branch name includes the issue number (mention mismatch once if not — do not create/rename unless user asks)
```

### Resolve the issue ID

Check, in order:

1. **User prompt** — `GitHub: #12 — …` or a GitHub issue URL
2. **Active Conductor track** — `conductor/tracks/<id>/metadata.json` → `github`
3. **Branch name** — `{n}-*` (e.g. `12-short-slug`)
4. **Recent commits** — `(#12)` in subject

If still unknown, **ask once**: "Which GitHub issue (#N) does this work belong to?"

Do not implement feature work without a linked issue unless the user explicitly
says it is a chore with no ticket.

### Fetch context

When **GitHub MCP** is connected, fetch the issue; otherwise use `gh issue view N
--json title,body,state,labels,parent,subIssues,url`. Restate:

- Title and current state (open/closed) plus workflow labels
- Acceptance criteria / body
- Blockers, **parent epic** (if this is a sub-issue), labels
- Sub-issues under the current issue (if it is an epic)
- Parent epic (if this is a sub-issue): run the **track check**

If `gh` is unavailable, ask the user to paste the issue title + acceptance
criteria.

### Set in progress

Keep the issue **Open**. If `github.md` defines an `in-progress` status label,
apply it at start (`gh issue edit N --add-label in-progress`). One status
change per session is enough.

### Prompt prefix (human convention)

```text
GitHub: #12 — Short title
Track: conductor/tracks/<track_id>/   # optional
```

## 2. During work (traceability)

Read owner/repo from `conductor/github.md`.

| Artifact | Convention | Example |
|----------|------------|---------|
| Branch | `{n}-{short-slug}` | `12-get-protocol` |
| Commit subject | `(#N)` suffix or prefix | `feat(server): add get_protocol (#12)` |
| PR title | `#N: <imperative summary>` | `#12: Serve get_protocol from the server` |
| PR body | Link the issue URL. Do **not** put `Closes #N` until the user authorizes close. |

**Do not** comment on the issue for every file save. Comment only at
**milestones** (phase done, PR opened, blocked, ready for review).

## 3. Session finish (before "done" or PR)

```
GitHub finish:
- [ ] Milestone comment posted (summary, PR URL, how to verify)
- [ ] Status updated (in-review label only once agent code work is done — committed, pushed, tests green; Closed only on explicit user instruction)
- [ ] PR title/body include #N; no Closes #N unless the user authorized close
```

### Comment template

Use [reference.md](reference.md) → *GitHub comment templates*. Minimum:

- What changed (1–3 bullets)
- PR link (if any)
- How to verify / test plan pointer (use the project's test command from `conductor/workflow.md`)

### Status transitions

| Situation | GitHub |
|-----------|--------|
| Work started | Open (+ `in-progress` if defined) |
| Agent code work done (committed + pushed, checks green, PR open if requested) | Open (+ `in-review` if defined) |
| User explicitly says to close / mark Done | Closed |
| Blocked | Open + `blocked` (if defined) + comment explaining blocker |

**Hard rules (status changes):**

- **In-review** only when the agent's code work is actually **complete**: changes
  committed and pushed, tests for the touched surfaces green, finish comment
  posted, and the PR open when one was requested. Never apply `in-review` with
  unpushed work, failing checks, or tasks still in flight.
- **Closed** requires an **explicit user instruction in the current session**. A
  merged PR, a `Closes #N` line, or a "Mark Done" plan task is **not**
  authorization — post the finish comment, leave the issue **open**, and ask.
- Do **not** put `Closes #N` in the PR body until that explicit instruction.
  GitHub auto-closes the issue on merge when that keyword is present.

If the user has not asked for a PR yet, post the finish comment and leave the
issue **open**.

## 4. Transport

- **Cursor:** GitHub MCP when authenticated.
- **`gh`:** `gh issue view|create|edit|comment`, `gh issue create --parent N`.
  Prefer `--json parent,subIssues,subIssuesSummary,state,labels,url,title,body`.
- If MCP is unavailable, fall back **deterministically**: **GitHub MCP → `gh` →
  human convention**.
- Do not add a custom GraphQL Python client unless `gh` cannot express a
  required operation. See `conductor/github.md`.
- GHES: sub-issues need 3.17+. GitHub.com is the supported baseline.

## 5. Issue labels

Every issue should carry **2–4 labels** from orthogonal groups defined in
`conductor/github.md` (not in this skill).

### Required

| Group | Pick | Source |
|-------|------|--------|
| **Class** | 1 | `github.md` Class table (defaults: Bug, Feature, Improvement, Chore, Spec) |
| **Surface** | 1 | `github.md` Surface → path map |

### Recommended

| Group | Pick | When |
|-------|------|------|
| **Domain** | 0–1 | Product-facing work, if the project defined Domain labels |
| **Platform** | 0–1 | Infra/cross-cutting, if defined |
| **Quality** | 0–1 | Primary quality goal, if defined |

### Agent behavior

- At **session start**, if the issue has no labels, **propose** Class + Surface
  (+ Domain) before coding, using the maps in `github.md`.
- Map Conductor track type → Class: `feature` → Feature, `bug` → Bug,
  `chore` → Chore.
- Do not duplicate project/release names in labels.
- Do not invent another project's domains. If `github.md` has empty
  Domain/Platform/Quality tables, skip those groups.

## 6. Conductor tracks (GitHub-first)

A Conductor track is a **thin local execution artifact**, not a second copy of
the issue.

- **The GitHub issue is the spec.** Do **not** write a `spec.md` copy.
- **The track directory holds only** a pointer `metadata.json` (`track_id`,
  `github`, `github_url`), the executable `plan.md`, and an `index.md` pointer.
  New tracks are **not** registered in `conductor/tracks.md`.
- **Commands:** `conductor-new-track` still knows the file-based four-file
  shape — **when `github.md` exists, override it** using this section.
  Create/link the issue, write pointer metadata + `plan.md` only, post a
  track-opened comment.
- **Element sub-issues (optional):** one GitHub sub-issue per phase as a child of
  the primary; annotate `plan.md` headings with `(#N)`. The track still
  closes on the **primary** issue.

**Epics (track check):** an epic **must** have an epic track (`github` = epic
id), one phase per sub-issue. Before starting sub-issue work, confirm the parent
epic has an epic track.

**If a command asks for `spec.md` or a `tracks.md` entry while GitHub-first is
on, refuse that part** and follow this contract instead.

## 7. Pair with other skills

| When | Also use |
|------|----------|
| Reviewing a #N change | **github-review** |
| Park in-flight work (GitHub-linked) | **github-handoff** |
| Park in-flight work (file-based / no GitHub issue) | **conductor-handoff** |
| Conductor implement / new track | this §6 |
| Commit message only | user rule |

Templates and examples: [reference.md](reference.md).
