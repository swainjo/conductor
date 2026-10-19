---
name: gcp-logs
description: >
  Read, query, and analyse GCP Cloud Logging with Logs Explorer and `gcloud`. Use for any GCP log reading — Cloud Run, Cloud SQL, Cloud Functions, GKE, load balancers, or diagnosing a failed request/job/deploy. Triggers: "check the logs", "why did X fail in prod", "Cloud Run logs", "gcloud logging", "log filter", "find the error".
---

# GCP Logs

Read, query, and analyse GCP Cloud Logging with Logs Explorer and `gcloud`. Use for any GCP log reading — Cloud Run, Cloud SQL, Cloud Functions, GKE, load balancers, or diagnosing a failed request/job/deploy. Triggers: "check the logs", "why did X fail in prod", "Cloud Run logs", "gcloud logging", "log filter", "find the error".

## On load — project and auth

```bash
gcloud config list      # confirm the active project
gcloud auth list        # confirm the active account
```

Use the active `project` in all commands. In sandboxed/agent environments `gcloud logging read` needs full read access to `~/.config/gcloud/`; otherwise credentials fail.

## The query language (quick reference)

Filters are boolean expressions over log-entry fields:

```
resource.type="cloud_run_revision"
resource.labels.service_name="my-service"
severity>=WARNING
textPayload=~"regex here"                 # =~ is regex match
jsonPayload.event="job_failed"            # structured log field
timestamp>="2026-05-16T13:30:00Z"         # absolute, always UTC + trailing Z
```

Combine with `AND` / `OR` / `NOT`. Relative window on the CLI: `--freshness=6h` / `30m`.

Docs, when you need them: [building queries](https://cloud.google.com/logging/docs/view/building-queries), [LogEntry fields](https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry), [`gcloud logging` CLI](https://cloud.google.com/sdk/gcloud/reference/logging).

## Do NOT filter only on `severity>=ERROR`

Structured loggers (structlog, most JSON loggers) frequently emit failures at
`DEFAULT`/`INFO` inside `textPayload` or `jsonPayload`, not at `ERROR`. If you filter
by severity you will miss them. Filter by the **event name / message substring** first,
then narrow by severity only if the volume is too high.

## The UTC time-zone trap (read this before concluding "the job hung")

`gcloud logging read` timestamps are **UTC** (ISO-8601 with a trailing `Z`). The agent's
or IDE's local "now" may be in another zone. **Never** compute elapsed time by
subtracting a local "now" from a UTC log timestamp without converting both to UTC first.

- **Anchor "now" in UTC** before any subtraction:
  ```bash
  date -u +%Y-%m-%dT%H:%M:%SZ
  ```
- **Prefer `--freshness=<N>m/<N>h`** for "recent activity" — it's evaluated server-side
  against real UTC now, sidestepping the local-offset problem entirely.
- **Absolute filters** (`timestamp>="...Z"`) must always be UTC with the `Z`.

A phantom ~1h gap between "now" and the last log line is almost always a UTC-vs-local
mix-up (e.g. a BST/UTC+1 display), **not** a stalled job. Re-check against `date -u`
before you conclude anything hung.

## `gcloud` CLI patterns

```bash
# Cloud Run service, JSON for jq/programmatic reading
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="SERVICE"' \
  --project=PROJECT_ID --limit=100 --freshness=6h --format=json

# One request/trace across a time window (filter by a request or correlation id)
gcloud logging read \
  'resource.type="cloud_run_revision" AND textPayload=~"CORRELATION_ID"' \
  --project=PROJECT_ID --limit=200 --freshness=2h

# Narrow to a structured event set
gcloud logging read \
  'jsonPayload.event=("job_started" OR "job_failed")' \
  --project=PROJECT_ID --limit=50 --freshness=6h
```

Parse JSON with `jq` or a short Python one-liner. **Sort by `timestamp`** when
correlating across services — Cloud Logging does not guarantee return order, and a
downstream service's logs can lag the caller's by 1–3 minutes.

## Correlating across services

For a request that spans services (API → queue → worker → DB), pick a **correlation id**
(request id, job id, session id, trace id) that appears in every hop, then run the same
substring filter against each `resource.type` and merge by `timestamp`. This turns a
"which service actually failed" question into one read per hop.

## Common resource types

| Source | `resource.type` | Notes |
|--------|-----------------|--------|
| Cloud Run | `cloud_run_revision` | filter by `resource.labels.service_name` |
| Cloud Functions (2nd gen) | `cloud_run_revision` | 2nd-gen functions run on Cloud Run |
| Cloud SQL | `cloudsql_database` | Postgres/MySQL server logs |
| GKE | `k8s_container` | `resource.labels.container_name`, `pod_name` |
| Load balancer | `http_load_balancer` | request logs, status codes, latency |
| GCE VM | `gce_instance` | |

## Log-based metrics & alerts

For recurring failure signals, create a **log-based metric** (counter over a filter)
and an alerting policy — but **codify it in a setup script**, not the console (see the
`gcp-deploy` skill). A counter over `textPayload=~"job_failed"` or a success event like
`jsonPayload.event="response_built"` gives you both failure alerts and a success rate.

## Don'ts

- Don't filter only `severity>=ERROR` — structured failures hide at DEFAULT.
- Don't subtract local "now" from a UTC log timestamp — anchor with `date -u`.
- Don't dump thousands of lines into your reply — slice to the failing window and quote the smallest relevant excerpt.
- Don't create alerts/metrics by hand in the console — put them in a setup script.
