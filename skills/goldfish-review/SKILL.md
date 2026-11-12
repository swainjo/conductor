---
name: goldfish-review
description: >
  Elephant/goldfish spec check: before a spec is approved, hand the draft to a
  fresh zero-context subagent (the goldfish) and make it explain how it would
  build the work from the text alone; every guess, ambiguity or untestable
  criterion it reports is context still stuck in the author's head (the
  elephant) and gets written into the spec. Use in conductor-new-track after
  drafting spec.md, a Linear issue description or a GitHub issue body and
  BEFORE asking the user to Approve/Revise; optionally on plan.md before plan
  approval and on handoff notes. Also use when the user says "goldfish this",
  "cold-read the spec", or "could a fresh session build from this?".
---

# Goldfish review (elephant/goldfish spec check)

Specs are written by the agent that remembers everything and read later by
agents that remember nothing (`conductor-implement`, a handoff, a new session).
The author can't see its own gaps because it fills them from memory. This skill
makes that failure visible before approval.

| Role | Who | Sees | Job |
|---|---|---|---|
| **Elephant** | The agent running `conductor-new-track` | Whole conversation, project docs, every decision and its reason | Writes the spec; triages goldfish findings; fixes the spec |
| **Goldfish** | A fresh subagent started for this check | Only the draft plus the project docs a future session would also have | Explains how it would build the work; reports every guess |

**The rule:** if the goldfish cannot build from the spec, the spec is not done.
A goldfish guess is a spec gap, not a goldfish failure.

## When to run

| Point | Required? |
|---|---|
| `conductor-new-track` §2.2 step 4 → 5 (file-based `spec.md`), after the draft, before Approve/Revise | Required for MVP / Feature tracks |
| §2.2-L / §2.2-G **Create**: after the issue draft, before `save_issue` / `gh issue create` | Same as above |
| §2.2-L / §2.2-G **Link**: when the fetched issue is the spec | Run it; findings become proposed acceptance-criteria additions on the issue |
| Bug / Chore / Refactor tracks | Offer it; skip if the user declines |
| §2.3 `plan.md`, before plan approval | Optional (plan pass below) |
| Handoff notes (`conductor-handoff`, `linear-handoff`, `github-handoff`) | Optional |

The user can always opt out with "skip goldfish". Say once that it was skipped
and continue.

## Procedure

### 1. Elephant prep

- Make sure the draft records the **why** behind each non-obvious decision
  (a short "Decisions" list is enough). Rationale is exactly what the goldfish
  will lack.
- Write the draft to a scratch file (e.g. the session scratchpad, or
  `conductor/tracks/<track_id>/spec.draft.md` if no scratch dir exists; delete
  it afterwards). The goldfish reads files, not your conversation.

### 2. Build the goldfish packet

Give the goldfish **paths, not summaries**:

- The draft file.
- Project docs a future session would also load: `conductor/product.md`,
  `conductor/product-guidelines.md`, `conductor/tech-stack.md`,
  `conductor/workflow.md`, `conductor/code_styleguides/`.
- Read access to the repo.

Never include: the chat transcript, your own summary of intent, the user's
answers, or hints about what "should" be built. Anything you add that isn't in
the spec or the repo defeats the check.

### 3. Spawn the goldfish

Use a **fresh** subagent (Claude Code: `Agent` tool, general-purpose, not
`fork`; read-only work). Prompt template:

```
You are about to implement a piece of work with NO other context than the
files below. Nobody can answer questions. Do not edit any file.

Spec draft: <path>
Project docs: <paths>
Repository: current working directory (read freely)

Return, in this order:
1. BUILD SKETCH — the steps and files you would change, in order.
2. AMBIGUITIES — terms or requirements with more than one reasonable reading
   (quote the spec line, give the readings).
3. GUESSES — every assumption you had to make to fill the sketch, and what you
   picked.
4. UNTESTABLE CRITERIA — acceptance criteria you could not turn into a concrete
   check, and why.
5. CONTRADICTIONS — spec vs spec, or spec vs project docs / code.
6. SCOPE EDGES — things you are unsure are in or out of scope.
7. VERDICT — READY (you could build it as written) or GAPS.
Be terse. Cite spec lines. Do not suggest features.
```

If no subagent mechanism exists, a true goldfish isn't possible in-session:
tell the user, offer to write the prompt above for them to run in a new
session, or skip with a note.

### 4. Elephant triage

First compare the **build sketch** with what you and the user actually intend.
Where it drifts, the spec is missing something even if the goldfish didn't flag
it.

Then give each finding one verdict:

- **FIX** — you know the answer (it's in your head or the conversation): write
  it into the spec.
- **ASK** — you don't know either: ask the user, one question at a time, per
  `conductor-new-track`'s interaction rules.
- **DISMISS** — only when the answer is already in a file the goldfish could
  read and it missed it. State the file. "I know what was meant" is never a
  reason to dismiss.

### 5. Re-run (bounded)

If FIX/ASK changed requirements or acceptance criteria materially, run one
more goldfish round on the revised draft. **Maximum two rounds.** Remaining
findings go to the user as known open points.

### 6. Report, then hand back to approval

Before the normal Approve/Revise question, show the user:

```
Goldfish review (round N of max 2): VERDICT
- Fixed: <finding → what changed in the spec>
- Asked you: <finding → your answer>
- Dismissed: <finding → file that already answers it>
- Open: <anything left>
```

Then continue `conductor-new-track` exactly as written (Approve/Revise; for
Linear/GitHub, create the issue only after approval).

## Plan pass (optional, §2.3)

Same procedure with a different question. Give the goldfish the approved spec
plus the draft `plan.md`, and ask it to pick the **three riskiest tasks** and,
for each, state: files to touch, the test it would write first, and how it
knows the task is done. A task it can't answer for gets split or expanded.

## Handoff pass (optional)

Give the goldfish only the handoff note plus the track's `plan.md` and ask:
"What is the next action, what state is the branch in, and what must you not
redo?" Any wrong answer is a missing line in the handoff note.

## Wiring it into a project

Skills trigger on their description, but the reliable hook is the project's
`conductor/workflow.md`, which `conductor-new-track` reads during its handshake.
Add:

```markdown
## Spec Review (goldfish pass)

During `conductor-new-track`, after drafting the spec (spec.md, Linear issue
description or GitHub issue body) and before asking for Approve/Revise, run the
**goldfish-review** skill. Required for MVP/Feature tracks, offered for others.
The user may say "skip goldfish".
```

## Don'ts

- Don't leak context into the goldfish prompt (no intent summaries, no user
  answers, no "the user wants…").
- Don't let the goldfish talk to the user or edit files; it reports, the
  elephant acts.
- Don't dismiss a guess because you know the answer. That is the gap.
- Don't loop: two rounds maximum.
- Don't use the goldfish to add features or redesign; it tests clarity, not
  product choices.
- Don't skip the user's Approve/Revise step; this check informs approval, it
  doesn't replace it.

## Related skills

- **`conductor-new-track`**: the spec and plan flow this check plugs into.
- **`linear-issues`** / **`github-issues`**: the issue is the spec in
  tracker-first mode; the goldfish reads the issue draft.
- **`conductor-handoff`** / **`linear-handoff`** / **`github-handoff`**: handoff
  notes benefit from the same cold read.
- **`conductor-implement`**: the real goldfish this check simulates.
