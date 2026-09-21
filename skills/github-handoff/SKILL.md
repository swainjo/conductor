---
name: github-handoff
description: >
  Structured handoff of in-flight work via a GitHub handoff child issue (#N):
  when a session must stop mid-task, hand off between agents or between an agent
  and a human, park on a blocker, or change shift/runtime, the giver creates a
  handoff child issue under the in-flight issue (or its epic) and the receiver
  acknowledges → re-reads the parent → verifies state → resumes → closes only
  that handoff child (never the parent, epic, or other work issues). Use when
  the user says "hand off", "park this", "pick up where X left off" and
  conductor/github.md exists with a GitHub-linked track/issue. If there is no
  GitHub issue, use conductor-handoff (HANDOFF.md) instead. Pairs with
  github-issues and conductor-handoff.
---

# GitHub handoff (#N)

The coordination primitive for parking in-flight work and passing the baton so
the next agent or person resumes cold — without archaeology.

## Routing (read first)

| Condition | Skill to use |
|-----------|----------------|
| Both `linear.md` and `github.md` exist | **HALT** and ask which tracker file to keep |
| `conductor/github.md` exists **and** the work is GitHub-linked (`metadata.json.github` and/or an active `#N` issue) | **This skill** — Handoff child issue under the parent |
| No GitHub issue (file-based track only) | **`conductor-handoff`** — `HANDOFF.md` in `conductor/tracks/<id>/`; do not invent a GitHub baton |

**Activate only when** `conductor/github.md` exists. Read owner/repo from that
file. If `github.md` is absent, use **`conductor-handoff`**.

If the work has **no** GitHub issue even though `github.md` exists, do **not**
improvise a file baton ad hoc — follow **`conductor-handoff`** by name.

## Three principles (do not violate)

1. **Baton, not diary.** A **handoff child issue** is a discrete transfer.
   **Only that baton** closes — the moment the receiver acknowledges and
   verifies pickup — **not** when the feature ships, and **not** the parent
   work issue.
2. **Point, don't duplicate.** The **parent issue** (scope/acceptance criteria)
   and the Conductor `plan.md` stay the source of truth. The handoff captures
   only the **transfer delta**.
3. **Never close work issues as part of a handoff.** The parent stays **Open**
   (add `blocked` if `github.md` defines that label and you are parking on a
   dependency). Closing the real work is **github-issues** / **github-review**
   after the work actually finishes. Re-read the parent after closing the
   baton.

## When to create a handoff

- **Context exhaustion** — a session is about to end with a task half-done.
- **Agent → human** — blocked on a decision or credential only a human can resolve.
- **Human → agent** — parking work for an agent to continue from a known point.
- **Runtime switch** — e.g. Cursor ↔ Claude Code.
- **Blocked-and-parking** — an upstream dependency stalls the work.

If the work simply *finished*, this is not a handoff — close out with
**github-issues** / **github-review** instead.

## Where the handoff issue lives

| Field | Convention |
|-------|-----------|
| **Parent** | The in-flight `#N` being handed off. |
| **Title** | `Handoff: #N — <one-line resume point>` |
| **Labels** | **Handoff** + Class **Chore** + the parent's **Surface** label (from `github.md`) |
| **Assignee** | The named receiver. Leave unassigned only for pool pickup. |
| **Handoff issue state** | **Open** (child default). |
| **Parent issue state** | Stays **Open**, or Open + `blocked` when parking on a dependency. **Never** Closed. |

## Giver protocol (before you stop)

1. **Make the tree shareable.** Commit and **push** the branch.
2. **Update the source of truth first.** Flip `plan.md` markers and record task
   SHAs; keep the parent **Open** (add `blocked` only when parking on a
   dependency).
3. **Create the handoff child** (`gh issue create --parent N`, labels `Handoff`
   + `Chore` + parent Surface). Fill the body template. Do **not** close the
   baton as the giver.
4. **Assign** to the receiver — or leave unassigned for pool pickup.
5. **Do not close the parent.**
6. **Post a pointer comment on the parent** linking the handoff child.

## Receiver protocol (on pickup)

1. **Acknowledge** — comment "Picking up" on the handoff issue and assign it.
2. **Re-read the parent** — fetch the current parent issue; confirm acceptance
   criteria and state still match.
3. **Verify state** — check out the branch at the recorded SHA; named tests green.
4. **Resume** from the handoff's **Resume point**. The parent stays open.
5. **Close only the handoff baton** — `gh issue close` **that** Handoff-labelled
   child. Never close the parent here. (File-based counterpart:
   **conductor-handoff** deletes/archives `HANDOFF.md`.)
6. **Re-read the parent after closing the baton — always.** If it is closed,
   reopen it and say so.

## Handoff body template

```markdown
## Handoff — #N (<title>)

**Parent:** #N  (epic: #E)  ·  **From:** <giver>  →  **To:** <receiver / unassigned>
**Runtime:** <e.g. Claude Code → Cursor>   ·  **Conductor track:** conductor/tracks/<id>/

### Resume point (do this next)
- <the single, concrete next action>

### State
- **Branch:** n-slug @ <sha7>  (pushed: yes/no)
- **PR:** #NNN (draft) / none
- **Done:** <point at plan.md [x] markers>
- **In progress:** <the task left mid-flight>
- **Uncommitted / local-only:** <none | exactly what & where>

### Verification state
- **Green:** <project test command>
- **Not yet verified / known-red:** <what the receiver must (re)run>

### Open decisions / blockers
- <decision pending / blocker>

### Issue state at handoff
- **Acceptance criteria:** <link or key lines, verbatim>
- **State / labels / assignee at handoff:** <…>

### Context notes
- <env/stack quirks>

---
*Receiver: acknowledge → re-read parent → verify branch@SHA → resume → close **this handoff child only**. Never close the parent.*
```

## How this differs from conductor-handoff

| | **github-handoff** (this skill) | **conductor-handoff** |
|--|----------------------------------|------------------------|
| Baton | GitHub child issue labelled Handoff | `HANDOFF.md` in the track folder |
| Spend baton | Close **only** that child | Delete or archive the file |
| Spec | Parent GitHub issue | `spec.md` |
| Extra risk | Re-read parent after closing the baton | None of that tracker behaviour |

## What this skill does not do

- It does **not** close the parent, epic, or siblings — only the baton.
- It does **not** review the code (that's **github-review**).
- It does **not** replace `plan.md`.
- It does **not** handle file-only tracks — use **conductor-handoff**.
- If `gh` / GitHub MCP is unavailable, post the filled template as a comment on
  the parent and create the child when the transport returns. Still do **not**
  close the parent.

## Pairs with

| When | Skill |
|------|--------|
| GitHub issue lifecycle / track pointer | **github-issues** |
| File-based handoff (no GitHub issue) | **conductor-handoff** |
| Diff review after resume | **github-review** |

Templates: [reference.md](reference.md).
