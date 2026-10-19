---
name: local-ci-lint
description: >
  Run the same lint/format gate CI runs, scoped to the files you changed — before you push. Use when finishing work or opening a PR. Triggers: "lint before PR", "run the linters", "does this pass CI", "format my changes".
---

# Local CI Lint (changed files)

Run the same lint/format gate CI runs, scoped to the files you changed — before you push. Use when finishing work or opening a PR. Triggers: "lint before PR", "run the linters", "does this pass CI", "format my changes".

## The principle: gate on changed files, not the whole tree

Many mature repos have a **dirty lint baseline** — hundreds of legacy warnings that
whole-tree lint reports but that are *not* the PR gate. Gating on the whole tree there is
noise. CI enforces lint **only on files changed vs the base branch**, so your local check
must do the same to match CI.

## The mechanism (tool-neutral)

Compute the changed set against the base branch, then run the formatter + linter over just
those paths:

```bash
BASE="${LINT_BASE_REF:-origin/main}"

# Python (ruff) — lint + format only changed .py
CHANGED_PY=$(git diff --name-only "$BASE"...HEAD -- '*.py')
[ -n "$CHANGED_PY" ] && ruff format $CHANGED_PY && ruff check $CHANGED_PY

# Frontend (eslint) — only changed TS/JS
CHANGED_TS=$(git diff --name-only "$BASE"...HEAD -- '*.ts' '*.tsx' '*.js' '*.jsx')
[ -n "$CHANGED_TS" ] && npx eslint $CHANGED_TS
```

Override the diff base when comparing to another branch/SHA:
```bash
LINT_BASE_REF=origin/develop   # or a 40-char SHA
```

Wrap these in whatever your project uses (a `Makefile` target, an npm script, a shell
helper) so the exact command is one word — but the **contract** is always "changed files vs
base", matching CI.

## Do NOT gate on the whole-tree baseline

Whole-tree `ruff check .` / `eslint .` touch legacy files you didn't change and report the
dirty baseline. Use them only for a dedicated baseline-cleanup effort — never as the PR gate.

## If checks fail

1. Run the formatter over the changed set (`ruff format` / `prettier --write`), then re-lint.
2. Fix the remaining lint errors, or `--fix` where the linter can auto-resolve them.
3. Re-run until exit 0.

## Wire it into git hooks

Install a pre-commit hook that runs the formatter + linter on **staged** changed files (and
a pre-push hook for any single-head migration check), matching CI
exactly, so the gate can't be forgotten.

## Map local → CI

Whatever wrapper you use, the local command and the CI job must run the **same** changed-files
lint over the **same** base ref, so a green local run means a green CI lint.
