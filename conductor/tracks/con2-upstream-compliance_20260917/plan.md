**Linear:** [CON-2](https://linear.app/happy-stay-days/issue/CON-2/finish-pre-submission-compliance-for-linear-first-upstream-pr)

# Plan: Finish pre-submission compliance for Linear-first upstream PR

## Phase 1: CLA [checkpoint: 111d9af]

- [x] Task: Confirm Google CLA for GitHub identity `swainjo` `111d9af`
  - [x] Open https://cla.developers.google.com/ and confirm a signed agreement
  - [x] Record the result in the CON-2 milestone comment (signed / needs signing)
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 2: README Cursor install [checkpoint: e9f4b43]

- [x] Task: Add Cursor install section to README `e9f4b43`
  - [x] Draft a Cursor section parallel to Antigravity and Claude Code
  - [x] Keep Linear MCP notes; do not claim Cursor is only for Linear
  - [x] Confirm `VERSION` remains `0.3.0`
  - [x] Commit on a branch created from `6dbf804` (not fork `main`)
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 3: Clean upstream branch [checkpoint: e9f4b43]

- [x] Task: Cut PR branch from `6dbf804` `e9f4b43`
  - [x] `git fetch upstream && git checkout -b pr/con-2-linear-first 6dbf804`
  - [x] Cherry-pick or recommit only the README change onto that branch
  - [x] `git diff --name-only upstream/main...HEAD` must not list `conductor/` or root `scripts/linear_*.py`
- [x] Task: Re-run Linear CLI tests (existing suite; no new product code) `e9f4b43`
  - [x] `uv run --with pytest pytest skills/conductor-setup/assets/linear/tests/`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 4: Open upstream PR

- [x] Task: Open a new PR to `gemini-cli-extensions/conductor` `e9f4b43`
  - [x] Title: `CON-2: Finish Linear-first pre-submission compliance`
  - [x] Do not revive #185; do not use `swainjo:main` as the head
  - [x] Test plan: CLI pytest, file-based default without `linear.md`, Linear opt-in smoke (create/link track, handoff, no auto-Done)
- [ ] Task: Confirm CI
  - [ ] `check-changes` green
  - [ ] `cla/google` green
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 5: Linear close-out

- [ ] Task: Post CON-2 finish comment with PR URL and how to verify
- [ ] Task: Set CON-2 to In Review only after commit, push, tests, and PR are done
- [ ] Task: Mark **CON-2** Done in Linear only on explicit user instruction; link PR in issue comment
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
