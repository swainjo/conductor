---
name: github-label-review
description: >
  Review a completed track or branch diff and recommend the GitHub issue's
  labels (Class / Surface / Domain / Platform / Quality) from the project's
  conductor/github.md taxonomy, then apply or list the add/remove delta. Use
  after implementing work, when finishing a track or PR, or whenever the user
  asks to check, fix, or suggest GitHub labels. Activates only when
  conductor/github.md exists. Pairs with github-issues.
---

# GitHub label review

Map the **actual diff** onto the **project** label taxonomy in
`conductor/github.md` so the GitHub issue's labels reflect what shipped.
This skill *applies* that taxonomy against changed files. It does not
define product-specific domains.

**Activate only when** `conductor/github.md` exists. If `linear.md` is also
present, **HALT** and ask which tracker file to keep.

## When this runs

- **Automatically:** a step inside **github-review** — after the diff review.
- **On demand:** "do the labels reflect this change?", "review / fix the labels
  for #N", "suggest GitHub labels for this branch".

## Taxonomy recap (authoritative list: `conductor/github.md`)

Every issue carries **2–4 labels** from orthogonal groups:

| Group | Pick | Source of the pick |
|-------|------|--------------------|
| **Class** | 1 (required) | Track type or the nature of the diff; names from `github.md` |
| **Surface** | 1 (required) | Dominant changed code path vs `github.md` Surface → path map |
| **Domain** | 0–1 | Product area, **only if** `github.md` defines Domain labels |
| **Platform** | 0–1 | Infra/cross-cutting, **only if** defined |
| **Quality** | 0–1 | Primary quality goal, **only if** defined |

If Domain / Platform / Quality tables are empty, skip those groups.

## Protocol

### 1. Resolve scope + issue

- Reuse the review scope: a track's recorded commit range or the branch diff vs
  the base branch.
- Resolve `#N` per **github-issues** §1.
- Get the changed paths: `git diff --name-only <range>` (and `--stat` for
  dominant surface by churn).

### 2. Fetch current labels (`gh`)

- Fetch the issue's current label set (`gh issue view N --json labels`).
- If `gh` is unavailable, continue read-only: produce the recommendation as a
  checklist for the user to apply by hand.

### 3. Derive recommended labels from the diff

**Class** — `feature→Feature`, `bug→Bug`, `chore→Chore`. No track? Infer: new
capability → **Feature**; fix → **Bug**; enhancement → **Improvement**;
refactor/tooling → **Chore**; planning-only → **Spec**. Use the Class names
listed in `github.md`.

**Surface** — pick the path with the most substantive churn and look it up in
the Surface → path table in `github.md`. A change that genuinely spans two
surfaces equally may carry both — flag it and prefer the dominant one.

**Domain / Platform / Quality** — only from `github.md`. Do not invent labels
from another product's taxonomy.

### 4. Compute the delta

- **Add:** recommended labels not yet on the issue.
- **Remove:** labels that contradict the diff.
- **Keep:** correct labels already present.

If the current set already satisfies "1 Class + 1 Surface" and matches the
diff, report "labels already accurate" and skip the apply.

### 5. Detect taxonomy gaps

If the diff belongs to a Surface/Domain **no existing label covers**, do not
force-fit: propose a new label (name + one-line description) under the right
group. Confirm with the user before creating it. Mirror the name into
`conductor/github.md` in the same change.

### 6. Confirm + apply

- Present the report and **confirm** before mutating GitHub.
- Apply the full intended label set via `gh issue edit N --add-label` /
  `--remove-label`. Skip silently when there is no delta.

## Output format

```
GitHub labels — #N (<title>)
Scope: <track id | branch range>  ·  dominant surface: <path> (<n> files)

Current : <labels or none>
Proposed: Class=<…> · Surface=<…> · Domain=<…> · Platform=<…> · Quality=<…>

+ Add    : <labels>
- Remove : <labels>
= Keep   : <labels>

Taxonomy gap: <none | proposed new label + description>
```

## Guardrails

- Never exceed 4 labels without a reason; Class + Surface are mandatory.
- Don't add a label the diff doesn't justify.
- One Surface unless the change is genuinely split.
- Read-only fallback when `gh` is down: emit the checklist, stop.
- Never hard-code domains that are not listed in `conductor/github.md`.
