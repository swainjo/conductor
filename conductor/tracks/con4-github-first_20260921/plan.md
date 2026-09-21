**Linear:** [CON-4](https://linear.app/happy-stay-days/issue/CON-4/adapt-linear-for-github-issues)

# Plan: GitHub-first spec management

## Phase 1: Tracker detection contract and GitHub template [checkpoint: 99862a8]

- [x] Task: Write failing tests that setup resume does not require `github.md` or `linear.md` `99862a8`
  - [x] Assert `determine_resumption` required chain is unchanged `99862a8`
- [x] Task: Confirm `resume.py` already treats tracker files as optional (no required-chain change unless a test fails) `99862a8`
- [x] Task: Add `skills/conductor-setup/assets/github/github.md` template `99862a8`
  - [x] Placeholders for owner, repo, issue URL, Class / Surface / optional Domain Platform Quality, optional status labels
  - [x] Transport ladder documented in the template
- [x] Task: Write a failing test that the template contains the required placeholders; then make it pass `99862a8`
- [x] Task: Add Surface **GitHub skills** (`skills/github-*/`) to this fork’s `conductor/linear.md` taxonomy (for CON-4 labeling) `99862a8`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) `4ee554f`

## Phase 2: `github-issues` skill and new-track pointer tracks [checkpoint: 249c5e0]

- [x] Task: Add `skills/github-issues/SKILL.md` and `reference.md` adapted from `linear-issues` `249c5e0`
  - [x] Activate only when `conductor/github.md` exists
  - [x] Dual-file halt if `linear.md` is also present
  - [x] Issue body is the spec; pointer `metadata.json` (`track_id`, `github`, `github_url`)
  - [x] Resolve `#N` from prompt, metadata, `{n}-{slug}` branch, or `(#N)` commits
  - [x] Transport: GitHub MCP → `gh` → human
  - [x] Epics = parent issue + sub-issues; epic track check
  - [x] No `Closes #N` until explicit close instruction; never close without it
- [x] Task: Add GitHub-first branch to `conductor-new-track` (`§2.2-G` / `§2.5-G`) `249c5e0`
  - [x] Create or link `#N`; no `spec.md`; no `tracks.md` row
  - [x] Track-opened comment on the GitHub issue
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) `a07c5e8`

## Phase 3: Setup opt-in [checkpoint: d8846f4]

- [x] Task: Change `conductor-setup` §2.7 to a three-way tracker choice: Skip / Linear-first / GitHub-first `d8846f4`
  - [x] Skip remains recommended default
  - [x] Enabling GitHub copies the template to `conductor/github.md` and links it from `index.md`
  - [x] Do not copy `github-*` skills into `.cursor` / `.claude` / `.agents`
- [x] Task: Update setup `index.md` handshake example and setup `workflow.md` asset handoff routing `d8846f4`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) `419c186`

## Phase 4: Conductor lifecycle skills [checkpoint: 3c2e24c]

- [x] Task: `conductor-implement` — GitHub-first: fetch issue AC, no `spec.md`, status via Open/Closed + optional labels `3c2e24c`
- [x] Task: `conductor-status` — discover tracks from pointer metadata; lifecycle = GitHub issue state `3c2e24c`
- [x] Task: `conductor-revert` — git/plan revert unchanged; optional comment on `#N`; do not auto-close `3c2e24c`
- [x] Task: `conductor-review` — delegate close-out to `github-review` when GitHub-first is on `3c2e24c`
- [x] Task: `conductor-handoff` — route GitHub-linked work to `github-handoff` `3c2e24c`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) `2ad59e5`

## Phase 5: `github-handoff` [checkpoint: 396c685]

- [x] Task: Add `skills/github-handoff/SKILL.md` and `reference.md` `396c685`
  - [x] Baton = child issue `Handoff: #N — …`, labels Handoff + Chore + parent Surface
  - [x] Close only the baton; re-read parent after close
  - [x] Cross-link with `conductor-handoff` and `github-issues`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) `396c685`

## Phase 6: Review and labels [checkpoint: ecc8b01]

- [x] Task: Add `skills/github-review/SKILL.md` — review intent is the GitHub issue AC `ecc8b01`
- [x] Task: Add `skills/github-label-review/SKILL.md` — taxonomy from `github.md` only; confirm before `gh issue edit` `ecc8b01`
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) `7e25e71`

## Phase 7: Docs and plugin discoverability

- [x] Task: README — GitHub-first section beside Linear-first; command table; handoff routing `42f1959`
- [x] Task: `conductor/product.md` and `product-guidelines.md` — file | Linear | GitHub backends `42f1959`
- [x] Task: `conductor/tech-stack.md` — `gh` / GitHub MCP on the transport ladder `42f1959`
- [x] Task: `conductor/workflow.md` — handoff routing includes GitHub-linked tracks `42f1959`
- [x] Task: `plugin.json` / `.cursor-plugin/plugin.json` — confirm `skills/` glob picks up `github-*` with no extra wiring `42f1959`
- [~] Task: Phase Verification & Checkpoint (Refer to workflow.md)

## Phase 8: CON-4 close-out

- [x] Task: Post a CON-4 milestone comment (what shipped, how to verify) `16c094a`
- [ ] Task: Set CON-4 to **In Review** only after commit/push and tests green
- [ ] Task: Mark **CON-4** Done only on explicit user instruction
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)

Parked for **manual testing** before push / In Review. Resume: verify GitHub-first locally, then push `main` and continue close-out.

## Phase: Review Fixes

- [x] Task: Apply review suggestions `33da8da`
