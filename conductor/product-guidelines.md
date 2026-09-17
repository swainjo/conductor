# Product Guidelines

## Voice

Direct, sequential, and mentor-like. Explain why a Conductor artifact exists
before writing it. Do not skip protocol steps.

## Agent UX

- Ask one question at a time in chat; use native choice UI when available
- Always offer a custom/Other option on choices
- Prefer (Recommended) with a short italic reason when a default is clear
- Treat `conductor/` as source of truth; Linear issue as spec when
  `linear.md` exists

## Prose

Plain language. Lead with what is true or what to do. Use numbered menus
(`[1]`, `[2]`) when native UI is unavailable.

## Contribution split

Plugin skills and rules may go upstream. The local `conductor/` workspace,
Linear identity, tracks, and fork workflow notes stay on the fork and must not
appear in PRs to `gemini-cli-extensions/conductor`.
