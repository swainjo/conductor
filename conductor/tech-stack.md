# Tech Stack

## Languages and formats

- Markdown for skills, rules, and SDD artifacts
- Python 3 for setup resume checks and Linear GraphQL CLIs
- JSON for `plugin.json` and marketplace manifests

## Tooling

- Git + GitHub (`origin`: `swainjo/conductor`, `upstream`:
  `gemini-cli-extensions/conductor`)
- pytest run with `uv` for Linear CLI unit tests (no network)
- Linear MCP when authenticated; `LINEAR_API_KEY` for CLI fallback

## Hosts

- Cursor, Claude Code, Antigravity (plugin skills + UX adapters)

## Out of stack

No application server, database, or frontend framework. This repo is a plugin of
Markdown protocols plus small Python helpers.
