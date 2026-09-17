# Fork workflow: Linear tracks on origin, not in upstream PRs

This file is **fork-local**. Keep it, `conductor/`, and the copied Linear CLIs
off pull requests to `gemini-cli-extensions/conductor`.

## Why

This repository is two things at once:

| Layer | Paths | Destination |
|-------|-------|-------------|
| **Plugin product** | `skills/`, `rules/`, `README.md`, `plugin.json` | PRs to **upstream** |
| **Your SDD workspace** | `conductor/` (this file, `linear.md`, tracks, plans) and root `scripts/linear_*.py` | Commit on **origin** (`swainjo/conductor`) only |

Linear-first is on because `conductor/linear.md` exists. Tracks use the Linear
issue as the spec. Local track folders are thin pointers (`metadata.json` +
`plan.md` + `index.md`).

Do not commit `LINEAR_API_KEY`.

## Remotes

- `origin` → `https://github.com/swainjo/conductor.git` (fork home)
- `upstream` → `https://github.com/gemini-cli-extensions/conductor.git`

## Create a Linear track

1. Stay on the **fork-home** branch (`main` on origin, or a dedicated `sdd`
   branch that already contains `conductor/`).
2. Start a new track (`/conductor:conductor-new-track` or ask in chat).
3. Create or link a `CON-` issue on team **Conductor**. The issue description
   is the spec — do not write `spec.md` or a `tracks.md` entry.
4. Approve `plan.md`. Track artifacts land in `conductor/tracks/<track_id>/`.
5. Commit on the fork-home branch, for example:
   `chore(conductor): initialize track '<track_id>'`.
6. Push to `origin`. Do **not** open an upstream PR from this branch if it
   contains `conductor/` commits.

## Open an upstream PR without fork workspace files

Always branch PRs from `upstream/main`, never from a commit that added
`conductor/`.

```bash
# Implement on fork-home so Linear tracks stay in git on origin
git checkout main
# … product commits plus optional chore(conductor) track commits …

# Cut a clean PR branch from upstream
git fetch upstream
git checkout -b pr/short-slug upstream/main
git cherry-pick <product-commit-sha>   # not chore(conductor) / setup commits
git push -u origin HEAD
gh pr create --repo gemini-cli-extensions/conductor --base main
```

### Must not appear in the upstream diff

- `conductor/` (including `linear.md`, tracks, this file)
- `scripts/linear_cli.py`
- `scripts/linear_create_issue.py`

### May appear in the upstream diff

Plugin product changes: `skills/`, `rules/`, README, tests under
`skills/conductor-setup/assets/linear/`, and other files that already belong
upstream.

### Quick check before you open the PR

```bash
git fetch upstream
git diff --name-only upstream/main...HEAD
```

If that list includes `conductor/` or root `scripts/linear_*.py`, drop those
commits or recut the branch from `upstream/main`.

## Transport ladder (Linear)

1. Linear MCP (Cursor Linear plugin)
2. `scripts/linear_cli.py` / `scripts/linear_create_issue.py` with `LINEAR_API_KEY`
3. Ask the human

Do not copy `linear-*` plugin skills into `.cursor` / `.claude` / `.agents`.
They ship with Conductor and activate when `conductor/linear.md` exists.
