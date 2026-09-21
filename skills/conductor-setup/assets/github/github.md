# GitHub workspace

Skills in `github-issues`, `github-review`, `github-handoff`, and
`github-label-review` read this file for repo identity and label taxonomy.
Change it here, not in each skill. When this file exists, park GitHub-linked
work with **github-handoff**; file-only tracks use **conductor-handoff**.

GitHub-first is **on** when this file exists. Do not also keep
`conductor/linear.md` in the same project — skills halt and ask which tracker
to use. Do not commit tokens.

| Field | Value |
|-------|-------|
| **Owner** | `{{OWNER}}` |
| **Repo** | `{{REPO}}` |
| **Issue URL** | `https://github.com/{{OWNER}}/{{REPO}}/issues/N` |

**Transport ladder:** GitHub MCP (when authenticated) → `gh` → ask the human.
`gh` uses the user's existing GitHub auth (`gh auth status`). Conductor does
not bundle or authenticate GitHub MCP.

## Status labels (optional)

GitHub native state is Open / Closed. If this project uses workflow labels,
map them here. Leave the table as comments if unused.

| Conductor moment | GitHub |
|------------------|--------|
| Work started | Open + `in-progress` (if you use that label) |
| Agent work complete | Open + `in-review` (if you use that label) |
| Blocked | Open + `blocked` (if you use that label) |
| Done | Closed — **only** on explicit user instruction |

Do **not** put `Closes #N` on a PR until the user authorizes close. GitHub
auto-closes the issue on merge when that keyword is present.

## Label taxonomy

Every issue should carry **2–4 labels** from orthogonal groups.
`github-label-review` reads this section.

### Class (required — pick 1)

| Label | Use when |
|-------|----------|
| Feature | New capability |
| Bug | Defect / regression |
| Improvement | Enhancement of existing behavior |
| Chore | Tooling, refactor, maintenance |
| Spec | Planning / specification-only |

### Surface (required — pick 1)

Map the **dominant changed path** to a Surface label. Replace the examples
with this project's paths during setup.

| Surface label | Repo path |
|---------------|-----------|
| `{{SURFACE_EXAMPLE_NAME}}` | `{{SURFACE_EXAMPLE_PATH}}` |

### Domain (optional — pick 0–1)

| Domain label | Use when |
|--------------|----------|
| *(none yet)* | Add product-area labels here if the team uses them |

### Platform (optional — pick 0–1)

| Platform label | Use when |
|----------------|----------|
| CI & Dev Environment | CI, scripts, dependency files, Conductor/GitHub automation |
| MCP / Claude Code | MCP registration, Claude/Cursor connectors |
| Security | Auth, secrets, path handling |

### Quality (optional — pick 0–1)

| Quality label | Use when it is the **primary** goal |
|---------------|--------------------------------------|
| Performance | Speed / resource use |
| Usability | Human interaction quality |
| AI Output Quality | Agent/LLM output quality |
| Code Quality | Structure, tests, maintainability |
