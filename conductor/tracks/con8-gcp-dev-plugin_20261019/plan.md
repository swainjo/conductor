**Linear:** [CON-8](https://linear.app/happy-stay-days/issue/CON-8/add-gcp-dev-plugin-and-two-workflow-skills-to-the-fork-marketplace)

# Plan: gcp-dev plugin and two workflow skills (fork-only)

Sources: air_engine `main` — `gcp-skill-pack/skills/*.md` (flat, no frontmatter) and
`.agents/skills/{stay-on-current-branch,skill-gap-review}/SKILL.md`.

## Phase 1: Workflow skills in the conductor plugin

- [x] Task: Add `skills/stay-on-current-branch/SKILL.md`, issue prefix read from `conductor/linear.md` / `conductor/github.md` `c2867e3`
- [x] Task: Add `skills/skill-gap-review/SKILL.md`, catalog check covers repo skills + enabled plugins; no project examples `c2867e3`

## Phase 2: gcp-dev plugin

- [x] Task: Add `gcp-dev/.claude-plugin/plugin.json` and `gcp-dev/skills/<name>/SKILL.md` for postgres-dev, local-ci-lint, compose-logs, gcp-logs, gcp-deploy, cost-review (frontmatter from the pack's description line; drop links to skills not shipped) `3f33f7b`
- [x] Task: Register `gcp-dev` in `.claude-plugin/marketplace.json` `3f33f7b`
- [x] Task: Bump `VERSION` and `.cursor-plugin/plugin.json` 0.3.0 → 0.4.0 `3f33f7b`
- [x] Task: Add `gcp-dev/` to FORK.md "must not appear in the upstream diff" (track commit)

## Phase 3: Verify

- [x] Task: `claude plugin validate` on the marketplace and both plugins (passes; pre-existing marketplace description warning)
- [ ] Task: (after push) Fresh session with this worktree as marketplace lists `gcp-dev:*` and the two new skills
