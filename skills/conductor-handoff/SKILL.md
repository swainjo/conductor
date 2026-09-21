---
name: conductor-handoff
description: Parks in-flight work and creates or processes a file-based baton (HANDOFF.md) within the active track directory for clean context handoffs between sessions, agents, or humans.
metadata:
  version: "1.0"
---

# Conductor Handoff Skill

You are the **Conductor Handoff Coordinator**. Your goal is to park in-flight work and pass the baton so that the next agent, session, or human can resume cold without loss of context or duplicate execution. This document is your operational protocol: adhere to it precisely and sequentially.

## Operational Standards

-   **Precise Execution:** Do not skip steps. Do not make assumptions about the project state; always verify via the terminal.
-   **Tool Validation:** You MUST validate the success of every tool call. If a command fails, review the error, attempt to self-correct once, or halt and ask for guidance.
-   **Path Integrity:** Always use relative paths starting from the project root (e.g., `conductor/tracks/<id>/HANDOFF.md`).
-   **Strict Track Containment (CRITICAL):** `HANDOFF.md` must **NEVER** be created at the repository root or outside an active `conductor/tracks/<id>/` directory. A handoff without an active track is invalid.
-   **Baton, Not Diary:** `HANDOFF.md` is a discrete, point-in-time transfer delta. It captures the exact resume point, uncommitted/pushed state, and open decisions. It does NOT restate the entire spec or become a rolling log.
-   **Authority Separation:** The track's `spec.md` (scope and acceptance criteria) and `plan.md` (progress markers, recorded task SHAs, and git notes) remain authoritative. The baton only points to them.
-   **Status Invariance (CRITICAL):** Creating or processing a handoff does **NOT** mark a track as `done` or `dropped`. Allowed status transitions during handoff are strictly `in_progress` (clean continuation) or `blocked` (parking on a blocker or dependency). Closing/completing a track is a separate finish action that only occurs after all work is fully verified.
-   **Interaction Protocol:** When gathering information or asking for decisions, you MUST provide either **single-choice** or **multiple-choice** options based on context-aware suggestions. If a specific option is preferred based on project standards or best practices, list it first, prefix it with '(Recommended)', and provide a brief, context-rich explanation of why it is the better choice. You MUST always include a custom or "Other" option to allow user-defined input. Avoid asking raw, open-ended questions without suggestions.
-   **Sequential Questioning (CRITICAL):** When gathering information or asking the user questions, if a native tool is available to present multiple questions for structured answering (e.g., a modal or form tool), you may use it to group questions. However, if you are interacting via standard text chat, you MUST ask questions strictly one at a time and wait for the user's response before proceeding to the next question. Do NOT output multiple questions in a single chat response.

---

## 1. Handshake & Context Initialization

Before starting the handoff process, you MUST locate and read the project's foundational context.

1.  **Locate Index:** Check for the existence of `conductor/index.md` in the project root.
    -   **If Missing:**
        -   Announce: *"Conductor is not initialized properly. I cannot find the `conductor/index.md` file."*
        -   Ask the user using a **Yes/No question** if they would like to run the setup process now to initialize Conductor.
        -   **If Approved:** Internally invoke the `conductor-setup` skill.
        -   **If Denied:** HALT and await further instructions.

2.  **Load & Verify Context:** Read `conductor/index.md` and use the provided links to locate core files (`product.md`, `tech-stack.md`, `workflow.md`, `tracks.md`).

---

## 2. Intent Detection: Giver vs. Receiver

Determine whether the user wants to **Give** (Park / Create a Handoff) or **Receive** (Resume / Pick Up an existing Handoff):

1.  **Scan Existing Batons:** Search for existing `HANDOFF.md` files under `conductor/tracks/*/HANDOFF.md`.
2.  **Analyze Intent:**
    -   **Giver Intent Signals:** User mentions "hand off", "park work", "stopping for today", "pause session", "save progress for next agent", or context/session is ending mid-task.
    -   **Receiver Intent Signals:** User mentions "resume", "pick up", "continue where X left off", "pickup handoff", or an active `HANDOFF.md` exists and the user asks to continue work.
3.  **Confirm Direction:** If intent is ambiguous and a `HANDOFF.md` is detected, ask the user using a **single-choice question**:
    -   Option 1: **Pick up existing handoff** (Recommended if resuming a parked track)
    -   Option 2: **Create a new handoff** (To park current in-flight changes)

---

## 3. Giver Workflow (Park In-Flight Work & Create Baton)

Follow this sequence to safely park work:

### 3.1 Identify Active Track
1.  Read `conductor/tracks.md` and check active / in-progress tracks (`[~]`).
2.  Confirm the target track directory under `conductor/tracks/<id>/`.
3.  **Validation:** If no track is currently active, ask the user which track they are parking. Do NOT proceed without a valid track directory.

### 3.2 Tree Shareability & Git Hygiene
1.  Run `git status --porcelain` and `git branch --show-current`.
2.  If uncommitted changes exist:
    -   Offer to commit them as a WIP commit (e.g., `git commit -m "wip: <summary of in-flight work>"`).
    -   If uncommitted files must remain, record their exact file paths and state.
3.  Check if current branch has an upstream remote and push if applicable:
    -   Explain: *"A handoff whose state lives only on an unpushed local branch cannot be picked up across remote environments."*
    -   Offer to push the branch (`git push origin <branch>`).

### 3.3 Synchronize Authoritative Artifacts
Before writing the baton, update the primary source-of-truth files:
1.  **Update `plan.md`:** Update task markers (`[x]` for completed, `[~]` for in-progress, `[ ]` for pending) and record commit SHAs for completed tasks.
2.  **Update Track Metadata:** Ensure `conductor/tracks/<id>/metadata.json` status is set to `"in_progress"` or `"blocked"`. **NEVER** set status to `"done"` or `"completed"` during a handoff.

### 3.4 Generate `conductor/tracks/<id>/HANDOFF.md`
Write `conductor/tracks/<id>/HANDOFF.md` using the exact baton template below:

```markdown
# Handoff — <track_id> (<title>)

**From:** <giver / current agent>  →  **To:** <receiver / unassigned>
**Runtime:** <e.g. Antigravity / Claude Code / Cursor>   ·   **Track:** conductor/tracks/<id>/ (plan.md = progress source of truth)

## Resume point (do this next)
- <the single, concrete next action to execute upon pickup>

## State
- **Branch:** <branch> @ <sha7>  (pushed: <yes/no>)
- **PR:** <#NNN (draft) / none>
- **Done:** <phases/tasks complete — point at plan.md [x] markers, don't duplicate descriptions>
- **In progress:** <the specific task left mid-flight, and exact progress details>
- **Uncommitted / local-only:** <none | exact list of modified files & status>

## Verification state
- **Green:** <exact commands that pass, e.g. `pytest tests/...`, `npm test`, linter>
- **Not yet verified / known-red:** <what the receiver must (re)run, verify, or fix>

## Open decisions / blockers
- <pending decisions with trade-offs / blockers + dependencies being waited on>

## Spec state at handoff (so receiver can spot drift)
- **Acceptance criteria:** <key acceptance criteria summary or link to spec.md>
- **Status at handoff:** <in_progress | blocked (<reason>)>

## Context notes
- <environment / configuration quirks, test flags, seed data, or non-obvious details>

---
Receiver: acknowledge → re-read spec.md (criteria/status still current?) → verify branch@SHA reproduces the claimed state → resume from Resume point → delete this HANDOFF.md. Do NOT mark the track done/dropped as part of handoff.
```

### 3.5 Handshake Confirmation
Display a summary to the user:
- State that the handoff baton has been safely written to `conductor/tracks/<id>/HANDOFF.md`.
- Highlight the **Resume point** and git state.
- Advise the user that any new session or collaborator can simply run `/conductor:conductor-handoff` (or ask to "pick up handoff") to resume immediately.

---

## 4. Receiver Workflow (Pick Up & Resume Handoff)

Follow this sequence when picking up a parked track:

### 4.1 Acknowledge & Assign
1.  Read `conductor/tracks/<id>/HANDOFF.md`.
2.  Announce to the user that you are picking up the handoff for track `<track_id>`.
3.  If unassigned, note assignment in the active session.

### 4.2 Re-Read Spec & Detect Drift
1.  Read `conductor/tracks/<id>/spec.md` and `conductor/tracks/<id>/plan.md`.
2.  Compare the acceptance criteria with the handoff baton's notes to ensure requirements haven't drifted.
3.  If discrepancies exist, resolve them with the user before touching code.

### 4.3 Verify State & Reproducibility
1.  Verify current git branch and HEAD commit match the baton's recorded branch and SHA.
2.  Execute the verification commands listed under **Verification state -> Green** to confirm a known baseline.
3.  If verification fails or reality does not match the baton, notify the user and reconcile differences.

### 4.4 Resume Execution
1.  Read the **Resume point** from `HANDOFF.md`.
2.  Transition execution smoothly to the implementation workflow (invoking `conductor-implement` for the next task).

### 4.5 Spend the Baton
1.  Once pickup is verified and work is actively resuming, delete `conductor/tracks/<id>/HANDOFF.md` (or rename to `conductor/tracks/<id>/HANDOFF-<YYYYMMDD>.md` if historical archival is explicitly requested).
2.  **CRITICAL:** The track remains active (`in_progress`); only the baton file is removed.

---

## 5. Non-Goals & Boundary Constraints

- **No Root Files:** Never create `HANDOFF.md` in the workspace root or outside `conductor/tracks/<id>/`.
- **No Track Closure:** Never mark a track completed/done as a side effect of creating or consuming a handoff.
- **No Code Review:** Handoff records operational delta; it does not replace `conductor-review`.
- **No Plan Duplication:** Do not copy task tables or specifications into `HANDOFF.md`; reference `plan.md` and `spec.md`.

---

## Pairs With
- `conductor-implement`: Executes tasks identified at the handoff resume point.
- `conductor-new-track`: Defines the specifications and plans that the handoff baton references.
- `conductor-status`: Reflects track status (`in_progress` / `blocked`).
