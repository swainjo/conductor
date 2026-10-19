---
name: compose-logs
description: >
  Read Docker Compose dev-stack logs without flooding context. Use whenever the user mentions logs, errors, 500s, stack traces, crashes, or "why did X fail locally" and a local stack is running. Triggers: "check the logs", "tail logs", "what's the [service] saying", "500 locally", "service won't start".
---

# Compose Logs (local dev stack)

Read Docker Compose dev-stack logs without flooding context. Use whenever the user mentions logs, errors, 500s, stack traces, crashes, or "why did X fail locally" and a local stack is running. Triggers: "check the logs", "tail logs", "what's the [service] saying", "500 locally", "service won't start".

## First: pick the right service, don't tail everything

`docker compose logs` with no service floods every container and interleaves them — it's
only useful for an "is anything moving" sanity check. Map the symptom to one or two
services first.

| Symptom | Read |
|---------|------|
| API 500 / request error | the API/backend service |
| Pipeline/worker wrong output or hang | the worker/agent service (cross-ref any structured trace) |
| Upload/async task stuck | the background-worker service (+ the broker, e.g. redis) |
| Service won't start after a schema change | the migration-owning service (Alembic output), then the DB |
| "connection refused to db" | check `ps` — the DB may still be restoring a seed dump on first boot |

## Branch-isolated stacks

If your dev tooling gives each git branch its own Compose project
(`COMPOSE_PROJECT_NAME=<slug>`), container names are `<slug>-<service>-1` and a different
worktree's stack is a **different project**. Resolve the current project name before
raw `docker compose` reads:

```bash
./dev.sh ps                                   # or: docker compose ps
PROJECT=$(./dev.sh ps --format '{{.Project}}' | head -1)
```

## Bounded reads + noise slicing

```bash
docker compose -p "$PROJECT" logs --tail=200 api
docker compose -p "$PROJECT" logs --since=10m worker
docker compose -p "$PROJECT" logs --tail=1000 api 2>&1 | grep -iE 'error|traceback|exception|critical' -A3
docker compose -p "$PROJECT" logs --tail=2000 api | grep '/api/v1/thing'
```

- **Long follows block** — start a `-f` tail in the background, trigger the action,
  read the captured output, then stop the tail.
- **After a restart** the in-memory buffer is wiped — use `--since=<wall-clock>` rather
  than `--tail` from a previous boot.
- Filter out hot-reload noise (`reloading`, dev-server rebuild lines) when hunting errors.

## Answer, don't dump

Quote the smallest relevant slice (timestamps + traceback head) and point at the failing
line/file. Don't paste hundreds of lines into the reply.
