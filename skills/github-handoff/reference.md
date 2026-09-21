# GitHub handoff — reference

Repo identity: `conductor/github.md` in the **project**. Replace `#N` with the
parent issue number.

## Handoff issue body (copy-paste)

```markdown
## Handoff — #12 (<title>)

**Parent:** #12  (epic: #10)  ·  **From:** <giver>  →  **To:** <receiver>
**Runtime:** <from> → <to>  ·  **Conductor track:** conductor/tracks/<id>/

### Resume point (do this next)
- <the single, concrete next action>

### State
- **Branch:** 12-slug @ a1b2c3d  (pushed: yes)
- **PR:** none
- **Done:** <plan.md [x]>
- **In progress:** <task left mid-flight>
- **Uncommitted / local-only:** none

### Verification state
- **Green:** <project test command>
- **Not yet verified / known-red:** <what to re-run>

### Open decisions / blockers
- None

### Issue state at handoff
- **Acceptance criteria:** <issue URL>
- **State / labels / assignee at handoff:** Open · Feature, <Surface>

### Context notes
- …

---
*Receiver: acknowledge → re-read parent → verify branch@SHA → resume → close **this handoff child only**.*
```

## Comment templates

### Pointer on the PARENT issue (giver)

```markdown
**Handoff out (#12)** → #20

Parked at: <resume point> (pushed on `12-slug` @ a1b2c3d).
Baton: #20. Parent stays Open — **not** Closed.
```

### Acknowledge on the HANDOFF issue (receiver)

```markdown
**Picking up (#20)**

Assigned to me. Re-reading #12, then verifying `a1b2c3d` before I continue.
```

### Close the HANDOFF baton only

```markdown
**Pickup verified — closing baton (#20)**

Re-read #12 — criteria/state unchanged. Checked out `a1b2c3d`; named tests green; resuming on #12.
Handoff baton spent → Closed. Verified after closing: #12 still Open — parent **not** closed.
```

If the parent *was* closed:

```markdown
Note: #12 was Closed after the baton closed. Reopened — the work is not finished.
```

## `gh` shapes

- **Create the handoff child** — `gh issue create --parent N --title "Handoff: #N — …" --label Handoff --label Chore --label "<Surface>" --body-file baton.md`
- **Pointer comment on parent** — `gh issue comment N --body "…"`
- **Parent (giver only)** — stay Open; add `blocked` only when parking on a dependency.
- **Acknowledge / close baton only** — `gh issue close` on the **handoff id**, not the parent.
- **Receiver re-read** — `gh issue view N --json state,title,body,labels` immediately after closing the baton.
