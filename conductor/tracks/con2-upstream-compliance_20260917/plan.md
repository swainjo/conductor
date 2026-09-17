**Linear:** [CON-2](https://linear.app/happy-stay-days/issue/CON-2/finish-pre-submission-compliance-for-linear-first-upstream-pr)

# Plan: Finish pre-submission compliance for Linear-first upstream PR

## Phase 1: CLA

- [x] Task: Confirm Google CLA for GitHub identity `swainjo`
  - [x] Open https://cla.developers.google.com/ and confirm a signed agreement
  - [x] Record the result in the CON-2 milestone comment (signed / needs signing)
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 2: README Cursor install

- [ ] Task: Add Cursor install section to README
  - [ ] Draft a Cursor section parallel to Antigravity and Claude Code
  - [ ] Keep Linear MCP notes; do not claim Cursor is only for Linear
  - [ ] Confirm `VERSION` remains `0.3.0`
  - [ ] Commit on a branch created from `6dbf804` (not fork `main`)
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 3: Clean upstream branch

- [ ] Task: Cut PR branch from `6dbf804`
  - [ ] `git fetch upstream && git checkout -b pr/con-2-linear-first 6dbf804`
  - [ ] Cherry-pick or recommit only the README change onto that branch
  - [ ] `git diff --name-only upstream/main...HEAD` must not list `conductor/` or root `scripts/linear_*.py`
- [ ] Task: Re-run Linear CLI tests (existing suite; no new product code)
  - [ ] `uv run --with pytest pytest skills/conductor-setup/assets/linear/tests/`
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 4: Open upstream PR

- [ ] Task: Open a new PR to `gemini-cli-extensions/conductor`
  - [ ] Title: `CON-2: Finish Linear-first pre-submission compliance`
  - [ ] Do not revive #185; do not use `swainjo:main` as the head
  - [ ] Test plan: CLI pytest, file-based default without `linear.md`, Linear opt-in smoke (create/link track, handoff, no auto-Done)
- [ ] Task: Confirm CI
  - [ ] `check-changes` green
  - [ ] `cla/google` green
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 5: Linear close-out

- [ ] Task: Post CON-2 finish comment with PR URL and how to verify
- [ ] Task: Set CON-2 to In Review only after commit, push, tests, and PR are done
- [ ] Task: Mark **CON-2** Done in Linear only on explicit user instruction; link PR in issue comment
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
