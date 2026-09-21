**Linear:** [CON-3](https://linear.app/happy-stay-days/issue/CON-3/merge-conductor-handoff-and-reconcile-with-linear-handoff)

# Plan: Merge conductor-handoff and reconcile with linear-handoff

Dogfood reconcile on the **fork** first. Upstream PR heads stay the clean
branches (`pr/conductor-handoff`, `pr/linear-first`); do not use fork `main`
(with `conductor/`) as an upstream PR head.

## Phase 1: Clean branch split (Phase A) [checkpoint: done on fork]

- [x] Task: Create `pr/conductor-handoff` from `upstream/main`
  - [x] Cherry-pick / replay `handoff-skill` (`conductor-handoff` + README/workflow)
  - [x] Verify no `linear-*`, no fork `conductor/`
  - [x] Push to `origin` (`6c20837`)
- [x] Task: Create `pr/linear-first` from `upstream/main`
  - [x] Rebuild Linear-first from `6dbf804`; omit `skills/linear-handoff/`
  - [x] Omit Cursor install (decide separately)
  - [x] CLI tests 24/24; push to `origin` (`8909a1a`)
- [x] Task: Close/supersede mixed upstream PR #186
- [x] Task: Merge both clean branches into fork `main` for local dogfood
  - [x] Push fork `main` (`20530cb`)
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 2: Reconcile routing on the fork (Phase B)

- [x] Task: Confirm routing rule against CON-3
  - [x] Linear path: `conductor/linear.md` and/or `metadata.json.linear` → **linear-handoff**
  - [x] Else → **conductor-handoff** (`HANDOFF.md` in track dir)
- [x] Task: Update `skills/conductor-handoff/SKILL.md`
  - [x] Activate / early-exit: if Linear-linked, stop and use **linear-handoff**
  - [x] Pairs with / cross-link to **linear-handoff**
  - [x] Keep shared principles (baton not diary; never finish work as handoff side effect)
- [x] Task: Update `skills/linear-handoff/SKILL.md`
  - [x] If no Linear issue: use **conductor-handoff** by name (not ad-hoc file advice only)
  - [x] Pairs with **conductor-handoff** + **linear-issues**
- [x] Task: Align templates where they intentionally differ
  - [x] File baton create/archive vs close only the Handoff sub-issue
  - [x] Linear: re-read parent after closing baton (auto-complete risk)
- [x] Task: Update discoverability docs
  - [x] README: both handoff paths + routing one-liner
  - [x] Workflow / setup assets if needed
- [x] Task: Local smoke on fork
  - [x] Routing tables present in both skills; CON-3 track has `linear` → would select linear-handoff
  - [x] File-based path documented for tracks without `metadata.json.linear`
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 3: Upstream-ready reconcile artifact (optional before PRs)

- [ ] Task: Cut `feat/handoff-reconcile` from `upstream/main` + both clean heads
  - [ ] Include reconcile skill/doc edits; **exclude** fork `conductor/`
  - [ ] Push to `origin` as upstream PR head when ready
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 4: Linear close-out

- [ ] Task: Tick CON-3 acceptance criteria that Phase A completed; leave reconcile AC open until Phase 2 done
- [ ] Task: Post CON-3 finish comment when reconcile is verified
- [ ] Task: Set CON-3 to In Review only after commit/push (and upstream PR if requested)
- [ ] Task: Mark **CON-3** Done only on explicit user instruction
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
