---
name: skill-gap-review
description: >
  Diff-driven meta-review that mines recent code changes for NEW skills worth
  authoring — gaps where a skill would enforce good practice, codify a repeated
  multi-step procedure, or stop duplicated effort. Use when the user asks "what
  skills should we add", "review changes for skill opportunities", "find skill
  gaps", after landing a track/PR, or periodically to keep the skill catalog
  ahead of the codebase. Always dedupes candidates against the existing
  .claude/skills catalog and the enabled plugin skills (conductor) first,
  preferring to EXTEND an existing skill over creating a near-duplicate. Outputs
  ranked skill proposals with name, trigger description, what they enforce, and
  the exact file footprint to create them.
---

# Skill Gap Review (find new skills worth authoring)

A change can ship clean and still leave a **knowledge gap**: a footgun that will
recur, a multi-file coupling someone will forget, a procedure done by hand that a
checklist would make repeatable, or a convention re-explained in three PRs. This
skill is a **diff-driven audit of those gaps** — it reads recent changes, mines
them for skill-worthy signals, dedupes against the existing catalog, and proposes
the smallest set of new (or extended) skills that would pay off. Output proposals,
not prose.

Treat skills as first-class infrastructure: the repo's own catalog (usually
`.claude/skills/<name>/SKILL.md`, plus any `.agents/skills/` or `.cursor/skills/`
mirror the repo keeps) and the skills its enabled plugins ship (`conductor-*`,
`linear-*`, `github-*`, and any others). A good skill captures a *project-specific shape
of work* that is non-obvious, easy to get wrong, and done more than once. This
review keeps that catalog ahead of the codebase.

## When to use

- The user asks: "what new skills would help here", "review these changes for
  skill opportunities", "find skill gaps", "what should we document as a skill".
- After finishing a track/PR — especially one that fixed a regression, added a
  new subsystem, or touched several services together.
- Periodically (e.g. as a step after `/conductor:review` or a sprint wrap) to
  stop the catalog from drifting behind new patterns.
- When you notice you (or a teammate) re-derived the same convention or footgun
  that already bit a previous change.

This skill **recommends** skills; it does not author them. To actually write a
proposed skill, follow **Authoring footprint** below (or the `skill-creator`
skill).

## What makes a gap skill-worthy (the signal taxonomy)

Not every change deserves a skill. Score a signal on three axes — **frequency**
(will it recur?), **pain** (how bad is getting it wrong?), **durability** (will
the answer stay true?). A skill earns its place when it is high on at least two.
The strongest signals in this codebase:

| Signal | What it looks like in a diff | Why a skill helps |
|---|---|---|
| **Regression-fix / revert** | A commit fixing or reverting a previously-shipped bug; a comment like "do NOT regress", "must be imported before", "post-incident" | Codifies the footgun as a checklist so it can't recur. |
| **Multi-file change-together coupling** | One logical change forced edits in 3+ files that must stay in sync (e.g. a migration + a CHECK constraint + the enum that mirrors it; a config key + its CLI flag + every adapter that reads it) | A skill names the file-set so the next person updates all of them. |
| **Non-obvious invariant** | A guard whose *reason* isn't local to the code: an import that must come first, a fixed random seed, a partition filter every query needs, an idempotency check, a dialect difference between two backends | The invariant is invisible until violated; a skill makes it explicit. |
| **Repeated manual procedure** | A sequence of shell/SQL/gcloud steps done by hand more than once (a data replay for a date range, a seed refresh, a deploy rotation, a single-test invocation) | A skill turns tribal steps into a runbook. |
| **Duplicated effort / re-derivation** | The same explanation appears in multiple PR descriptions, commit bodies, or ad-hoc comments; two places implement the same convention slightly differently | A skill becomes the single source so it's explained once. |
| **New subsystem with conventions** | A new service, table family, frontend surface, or agent type that introduces its own rules (cache headers, gating, naming) | Front-loads the conventions before the second contributor guesses. |
| **Review-comment pattern** | The same class of review feedback recurs across PRs | The fix belongs in a skill, not in N review threads. |

Anti-signals — do **not** propose a skill for these:
- A one-off change unlikely to recur.
- Something a lint rule, type, test, or CI gate already enforces (prefer the
  automated gate; a skill that restates a green check is noise).
- General engineering knowledge already covered by a generic skill
  (`postgres-dev`, `pydantic-v2`, `react-suspense-lazy`, etc.).
- A topic already covered — that's an **extend**, not a **new skill** (see dedup).

## Review procedure

### 1. Scope the changes

Pick the review window and read the whole diff — do not sample.

```bash
git diff origin/main...HEAD                 # branch vs base
git log --oneline origin/main..HEAD         # commits in scope
git diff --stat origin/main...HEAD          # churn by file → dominant surface(s)
```

For a periodic review, widen to a date/commit range
(`git log --since=...`, or the last N merged PRs). For a track, use the recorded
commit range from its `plan.md`.

### 2. Enumerate the existing catalog (the dedup baseline)

Before proposing anything, load what already exists — every proposal is judged
against this list.

```bash
ls .claude/skills/ .agents/skills/ .cursor/skills/ 2>/dev/null   # repo skill sets
grep -h -A3 '^description:' .claude/skills/*/SKILL.md 2>/dev/null # their triggers
# plus the plugin skills listed in the session (conductor-*, linear-*, github-*, …)
```

Read the **descriptions**, not just the names — the
"when to use" line tells you a candidate's true scope and whether your gap is
already in-scope for an existing skill.

### 3. Mine the diff for signals

Walk the diff against the signal taxonomy. Useful tells:

```bash
# Footgun / invariant markers the authors left behind
git diff origin/main...HEAD | grep -niE \
  'do not|don.t|must |never |always |regress|footgun|gotcha|invariant|before any|post-incident|idempoten|spoof|guard'

# Coupled file-sets (same logical change across many files)
git diff --name-only origin/main...HEAD | sort

# New subsystems / entry points / conventions
git diff --name-status origin/main...HEAD | grep -E '^A'   # added files

# Repeated explanation across commit bodies (re-derivation smell)
git log origin/main..HEAD --format='%b'
```

For each hit, capture: the **file:line**, which **signal type** it is, and the
**recurrence evidence** (a revert SHA, a second PR with the same note, a 3-file
coupling). Evidence is what separates a real gap from a hunch.

### 4. Cluster signals into candidate skills

Group related signals — one good skill usually covers a *shape of work*, not a
single line. (E.g. "migration + CHECK + dynamic Enum + downstream reconcile" is
one migration-adjacent cluster, not four skills.) Aim for the smallest
number of candidates that cover the real gaps.

### 5. Dedup against the catalog — new vs. extend

For each candidate, decide one of three verdicts:

- **EXTEND** an existing skill — the gap is in-scope for a skill that already
  exists; recommend the specific section/bullet to add. *Default to this.* The
  catalog is large; most gaps are extensions.
- **NEW skill** — the shape of work is genuinely uncovered. Justify why no
  existing skill's "when to use" reaches it.
- **DROP** — covered by an automated gate, too one-off, or generic knowledge.

Be ruthless: a near-duplicate skill is worse than none — it splits the source of
truth and the next reader trusts the wrong one.

### 6. Score and rank

Rank surviving candidates by `frequency × pain × durability`. Lead with the ones
that prevent a recurring or costly mistake. Note low-confidence ones as "watch"
items rather than dropping them silently.

### 7. Output proposals

Use the template below. Each NEW proposal must be concrete enough that someone
could scaffold it without re-doing the analysis: the trigger description, the
canonical files/symbols it references, and the exact file
footprint.

## Output template

```
SKILL GAP REVIEW — <scope, e.g. branch vs origin/main, N commits>

Existing catalog checked: <count> skills (repo + enabled plugins)

── NEW SKILLS ──────────────────────────────────────────────
1. <skill-name>  [freq: H/M/L · pain: H/M/L · durability: H/M/L]
   Gap: <the recurring footgun/procedure/coupling, with file:line + evidence>
   Trigger (description): <the "use when…" line for the frontmatter>
   Enforces / captures: <the checklist or invariant it would hold>
   References: <canonical files/symbols the skill points at>
   Footprint:
     .claude/skills/<name>/SKILL.md   (+ references/ if the body runs long;
                                       + any mirror tree the repo keeps)

── EXTEND EXISTING ─────────────────────────────────────────
- <existing-skill> — add <section/bullet> covering <gap> (evidence: <…>)

── DROPPED (and why) ───────────────────────────────────────
- <candidate> — <covered by CI gate / one-off / generic / duplicate of X>
```

If the changes surface no real gap, say so plainly:
`SKILL GAP REVIEW: none — changes are covered by existing skills / automated gates.`

## Authoring footprint a proposal must respect

A NEW-skill proposal isn't done until it accounts for how this repo ships skills
(so the recommendation is actionable, not aspirational):

- **One file:** write `.claude/skills/<name>/SKILL.md` (YAML frontmatter:
  `name` matching the directory, `description` where the description *is* the
  trigger). Push long detail into `.claude/skills/<name>/references/`.
- **Mirror if the repo mirrors:** some repos keep `.agents/skills/` or
  `.cursor/skills/` copies; follow the surrounding convention.
- **Don't shadow plugin skills:** if the gap belongs in a plugin skill, propose
  the change to the plugin rather than a repo copy.
- **Cross-link** related skills at the bottom, as the existing skills do.

## Don'ts

- **Don't propose a skill that duplicates an existing one** — extend it instead.
  Run step 2 before step 7, every time.
- **Don't propose what a lint rule, type, test, or CI gate already enforces** —
  recommend tightening the gate, not writing prose around it.
- **Don't propose from a single occurrence** — a skill needs recurrence or high
  pain; cite the evidence.
- **Don't write the skill here** — this review recommends; authoring is a
  separate, deliberate step.
- **Don't write a vague description** — the description is the only trigger;
  a skill nobody's request matches is invisible.

## Related skills

- **`cost-review`** / **`code-review`** / **`linear-label-review`** — sibling
  diff-driven reviews; this one reviews the *skill catalog's* coverage of the diff.
- **`conductor-methodology`** — the track lifecycle this review runs after.
- **`linear-review`** / **`/conductor:review`** — the review flows this can run as
  a final step within.
