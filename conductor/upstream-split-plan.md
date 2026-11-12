# Upstream split plan

Fork-local. Status: **plan only, not dry-run yet.**

## Principle: split at PR-cut time, don't rewrite `main`

Every commit below is already on `origin/main`, three merge commits sit in the
history, and track `plan.md` files record commit SHAs. Rewriting `main` would
break those SHAs and force-push the fork home. Instead, keep `main` as is and
strip fork-only paths **when cherry-picking onto a branch cut from
`upstream/main`**. The four mixed commits only need extra handling during that
pick.

Fork-only paths (from [FORK.md](./FORK.md)):

```
conductor/  gcp-dev/  scripts/linear_cli.py  scripts/linear_create_issue.py
.claude-plugin/marketplace.json  (gcp-dev entry only)
```

## Commit classification (upstream/main..main, merges excluded)

- **Pure fork** (`chore(conductor)`, `conductor(plan)`, `conductor(setup)`): never pick.
- **Pure plugin:** pick as is.
- **Mixed:** pick, then strip fork paths.

| SHA | Subject | Kind | Action |
|---|---|---|---|
| 6dbf804 | Linear-first mode (#1) | plugin | PR A |
| e9f4b43 | Cursor install docs (CON-2) | plugin | PR A |
| a24e58c | conductor-handoff skill | plugin | PR B |
| 6c20837 | handoff workflow/docs | plugin | PR B |
| 8909a1a | Linear-first mode (CON-3) | plugin | PR A (check overlap with 6dbf804) |
| **86e3b18** | handoff reconcile (CON-3) | **mixed** | PR C, strip `conductor/linear.md`, `conductor/workflow.md`, track plan |
| **eb63b28** | GitHub-first template (CON-4) | **mixed** | PR D, strip `conductor/linear.md` |
| 4c4cc10, 684f62f, 18bc80f, d517b71, 5036149 | GitHub-first skills (CON-4) | plugin | PR D |
| **c2a3336** | GitHub-first docs (CON-4) | **mixed** | PR D, keep `README.md`, strip `conductor/*.md` |
| 4c5041c | review fixes for CON-4 (prefix says `fix(conductor)` but touches plugin files only) | plugin | PR D, reword prefix to `fix(skills)` |
| c0d0f78 | stay-on-current-branch, skill-gap-review | fork-only (for now) | Never pick until decided otherwise (see FORK.md) |
| **d207d4a** | gcp-dev plugin (CON-8) | **mixed** | Never pick. Its only plugin-side change is the `VERSION` / `.cursor-plugin` bump 0.3.0 → 0.4.0, which belongs to the fork |

## PR stack (each one builds on the previous)

Upstream PRs 185 and 186 both closed (CLA). Linear-first is the base everything else depends on.

1. **PR A — Linear-first:** 6dbf804, 8909a1a, e9f4b43
2. **PR B — conductor-handoff:** a24e58c, 6c20837
3. **PR C — handoff reconcile:** 86e3b18 (stripped)
4. **PR D — GitHub-first:** eb63b28 (stripped), 4c4cc10, 684f62f, 18bc80f, d517b71, 5036149, c2a3336 (stripped), 4c5041c
5. ~~PR E~~ — c0d0f78 stays fork-only for now.

Either open them as a stack (each branch based on the one before) or wait for each to merge before cutting the next.

Version: leave `VERSION` at upstream's value in every PR and let upstream maintainers bump it. Keep the fork's 0.4.0 on `main` only.

## Recipe for one commit

```bash
git fetch upstream
git checkout -b pr/<slug> upstream/main     # or the previous PR branch

git cherry-pick -n <sha>                     # -n: stage, don't commit
# A "deleted by us" conflict on conductor/... is expected for mixed commits.
git rm -rq --cached --ignore-unmatch -- conductor gcp-dev \
  scripts/linear_cli.py scripts/linear_create_issue.py
rm -rf conductor gcp-dev scripts/linear_cli.py scripts/linear_create_issue.py
git checkout HEAD -- .claude-plugin/marketplace.json VERSION .cursor-plugin/plugin.json
git status                                   # must show no conductor/ or gcp-dev/
git commit -C <sha>                          # reuse original message
```

Add the attribution lines to any rewritten message (e.g. 4c5041c's prefix).

## Verify before opening each PR

```bash
git diff --name-only upstream/main...HEAD \
  | grep -E '^(conductor/|gcp-dev/|scripts/linear_|\.claude-plugin/marketplace\.json|skills/(stay-on-current-branch|skill-gap-review|goldfish-review)/)' \
  && echo LEAK || echo clean
git diff upstream/main...HEAD -- VERSION .cursor-plugin/plugin.json   # expect empty
python -m pytest skills/                                              # setup asset tests
```

After the whole stack: the plugin paths should match the fork, apart from
`VERSION` and `.cursor-plugin` version.

```bash
git diff origin/main -- skills rules README.md plugin.json
```

## FORK.md follow-ups (fork-only commit on main)

- Add `VERSION` and `.cursor-plugin/plugin.json` version to "must not appear" (or "upstream-owned").
- Extend the quick-check grep to include `gcp-dev/` and `marketplace.json`.
- ~~Record the decision on `skill-gap-review` / `stay-on-current-branch`~~ — done: fork-only for now.
- Going forward: keep `conductor/` edits in their own `chore(conductor)` commits so no new mixed commits appear.
