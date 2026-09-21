**Linear:** [CON-4](https://linear.app/happy-stay-days/issue/CON-4/adapt-linear-for-github-issues)

# Plan: GitHub-first spec management

## Phase 1: Tracker detection contract and GitHub template

- [ ] Task: Write failing tests that setup resume does not require `github.md` or `linear.md`
  - [ ] Assert `determine_resumption` required chain is unchanged
- [ ] Task: Confirm `resume.py` already treats tracker files as optional (no required-chain change unless a test fails)
- [ ] Task: Add `skills/conductor-setup/assets/github/github.md` template
  - [ ] Placeholders for owner, repo, issue URL, Class / Surface / optional Domain Platform Quality, optional status labels
  - [ ] Transport ladder documented in the template
- [ ] Task: Write a failing test that the template contains the required placeholders; then make it pass
- [ ] Task: Add Surface **GitHub skills** (`skills/github-*/`) to this fork’s `conductor/linear.md` taxonomy (for CON-4 labeling)
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 2: `github-issues` skill and new-track pointer tracks

- [ ] Task: Add `skills/github-issues/SKILL.md` and `reference.md` adapted from `linear-issues`
  - [ ] Activate only when `conductor/github.md` exists
  - [ ] Dual-file halt if `linear.md` is also present
  - [ ] Issue body is the spec; pointer `metadata.json` (`track_id`, `github`, `github_url`)
  - [ ] Resolve `#N` from prompt, metadata, `{n}-{slug}` branch, or `(#N)` commits
  - [ ] Transport: GitHub MCP → `gh` → human
  - [ ] Epics = parent issue + sub-issues; epic track check
  - [ ] No `Closes #N` until explicit close instruction; never close without it
- [ ] Task: Add GitHub-first branch to `conductor-new-track` (`§2.2-G` / `§2.5-G`)
  - [ ] Create or link `#N`; no `spec.md`; no `tracks.md` row
  - [ ] Track-opened comment on the GitHub issue
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 3: Setup opt-in

- [ ] Task: Change `conductor-setup` §2.7 to a three-way tracker choice: Skip / Linear-first / GitHub-first
  - [ ] Skip remains recommended default
  - [ ] Enabling GitHub copies the template to `conductor/github.md` and links it from `index.md`
  - [ ] Do not copy `github-*` skills into `.cursor` / `.claude` / `.agents`
- [ ] Task: Update setup `index.md` handshake example and setup `workflow.md` asset handoff routing
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 4: Conductor lifecycle skills

- [ ] Task: `conductor-implement` — GitHub-first: fetch issue AC, no `spec.md`, status via Open/Closed + optional labels
- [ ] Task: `conductor-status` — discover tracks from pointer metadata; lifecycle = GitHub issue state
- [ ] Task: `conductor-revert` — git/plan revert unchanged; optional comment on `#N`; do not auto-close
- [ ] Task: `conductor-review` — delegate close-out to `github-review` when GitHub-first is on
- [ ] Task: `conductor-handoff` — route GitHub-linked work to `github-handoff`
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 5: `github-handoff`

- [ ] Task: Add `skills/github-handoff/SKILL.md` and `reference.md`
  - [ ] Baton = child issue `Handoff: #N — …`, labels Handoff + Chore + parent Surface
  - [ ] Close only the baton; re-read parent after close
  - [ ] Cross-link with `conductor-handoff` and `github-issues`
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 6: Review and labels

- [ ] Task: Add `skills/github-review/SKILL.md` — review intent is the GitHub issue AC
- [ ] Task: Add `skills/github-label-review/SKILL.md` — taxonomy from `github.md` only; confirm before `gh issue edit`
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 7: Docs and plugin discoverability

- [ ] Task: README — GitHub-first section beside Linear-first; command table; handoff routing
- [ ] Task: `conductor/product.md` and `product-guidelines.md` — file | Linear | GitHub backends
- [ ] Task: `conductor/tech-stack.md` — `gh` / GitHub MCP on the transport ladder
- [ ] Task: `conductor/workflow.md` — handoff routing includes GitHub-linked tracks
- [ ] Task: `plugin.json` / `.cursor-plugin/plugin.json` — confirm `skills/` glob picks up `github-*` with no extra wiring
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 8: CON-4 close-out

- [ ] Task: Post a CON-4 milestone comment (what shipped, how to verify)
- [ ] Task: Set CON-4 to **In Review** only after commit/push and tests green
- [ ] Task: Mark **CON-4** Done only on explicit user instruction
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
