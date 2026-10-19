**Linear:** [CON-8](https://linear.app/happy-stay-days/issue/CON-8/add-gcp-dev-plugin-and-two-workflow-skills-to-the-fork-marketplace)

# Plan: gcp-dev plugin and two workflow skills (fork-only)

Sources: air_engine `main` — `gcp-skill-pack/skills/*.md` (flat, no frontmatter) and
`.agents/skills/{stay-on-current-branch,skill-gap-review}/SKILL.md`.

## Phase 1: Workflow skills in the conductor plugin

- [x] Task: Add `skills/stay-on-current-branch/SKILL.md`, issue prefix read from `conductor/linear.md` / `conductor/github.md` `c0d0f78`
- [x] Task: Add `skills/skill-gap-review/SKILL.md`, catalog check covers repo skills + enabled plugins; no project examples `c0d0f78`

## Phase 2: gcp-dev plugin

- [x] Task: Add `gcp-dev/.claude-plugin/plugin.json` and `gcp-dev/skills/<name>/SKILL.md` for postgres-dev, local-ci-lint, compose-logs, gcp-logs, gcp-deploy, cost-review (frontmatter from the pack's description line; drop links to skills not shipped) `d207d4a`
- [x] Task: Register `gcp-dev` in `.claude-plugin/marketplace.json` `d207d4a`
- [x] Task: Bump `VERSION` and `.cursor-plugin/plugin.json` 0.3.0 → 0.4.0 `d207d4a`
- [x] Task: Add `gcp-dev/` to FORK.md "must not appear in the upstream diff" `68b97ef`

## Phase 3: Verify

- [x] Task: `claude plugin validate` on the marketplace and both plugins (passes; pre-existing marketplace description warning)
- [x] Task: (after push) Fresh session with this worktree as marketplace lists `gcp-dev:*` and the two new skills (all six `gcp-dev:*` in slash menu; local-scope install)
