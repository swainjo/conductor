---
name: gcp-deploy
description: >
  Author and edit idempotent GCP deployment scripts (Cloud Run, Cloud SQL, Secret Manager, Cloud Tasks, Cloud Scheduler, IAM, API enablement, load balancer/CDN). Use when the user asks to deploy/release/promote, change Cloud Run config, add a secret binding, enable an API, wire an IAM role, or "fix prod". Triggers: "deploy script", "Cloud Run env", "secret binding", "service account", "enable API", "Cloud Tasks queue", "Cloud Scheduler".
---

# GCP Deploy

Author and edit idempotent GCP deployment scripts (Cloud Run, Cloud SQL, Secret Manager, Cloud Tasks, Cloud Scheduler, IAM, API enablement, load balancer/CDN). Use when the user asks to deploy/release/promote, change Cloud Run config, add a secret binding, enable an API, wire an IAM role, or "fix prod". Triggers: "deploy script", "Cloud Run env", "secret binding", "service account", "enable API", "Cloud Tasks queue", "Cloud Scheduler".

## The iron rule: script-first, console-second

Any GCP change that must survive a redeploy or be reproducible in a new environment —
a permission, secret, enabled API, env var, Cloud Run config, queue, scheduler job,
IAM binding, LB/CDN — **must be codified in a deploy/setup script.** Ad-hoc `gcloud`
or console clicks are fine to *diagnose* or *emergency-unblock*; they are **not** the
fix. If it worked from the console, put it in the script before you call it done.

## Hard rules

1. **Idempotency.** Every step must be safe to re-run. Use existence checks
   (`gcloud ... describe ... >/dev/null 2>&1 || gcloud ... create ...`), `|| true` on
   benign already-exists errors, and `--update-env-vars` (additive) vs `--set-env-vars`
   (replace) deliberately.
2. **Secrets via Secret Manager, never `--set-env-vars`.** Sensitive values are bound as
   `--set-secrets ENV=secret-name:latest`. Passing a secret via `--set-env-vars` leaks it
   into deploy logs and Cloud Run revision metadata. Assemble compound secrets (e.g. a
   `DATABASE_URL`) as a single Secret Manager entry rather than echoing the password.
3. **Enable required APIs in the script.** `gcloud services enable ...` for every API the
   deploy depends on, so a fresh environment doesn't break-fix on first deploy.
4. **IAM bindings live in the script.** `gcloud projects add-iam-policy-binding` (or
   resource-scoped bindings) for every role the runtime service account needs — Secret
   Manager accessor, Cloud SQL client, Cloud Tasks enqueuer, etc.
5. **Least privilege.** `roles/owner` and `roles/editor` are banned for service accounts.
   Grant the narrowest role that works; prefer resource-scoped over project-scoped.
6. **Schema goes through migrations, not deploy scripts.** No `CREATE TABLE`/`ALTER` in a
   deploy script. Run `migrate ... up` (Alembic/Flyway/etc.) as a step; keep DDL in
   versioned revisions (Alembic, Flyway, dbt or plain SQL files).

## Pattern: add an env var to a Cloud Run service

1. Edit the service's deploy script; find the `--update-env-vars` block.
2. Add `MY_VAR=$MY_VAR_VALUE`. If it's **sensitive**, instead create the Secret Manager
   entry (in your secrets script) and add it to the `--set-secrets` batch.
3. Echo the non-secret value in the script preamble so deploys are inspectable.
4. Document user-facing vars in your `CLAUDE.md` "Environment setup".

## Pattern: add a Cloud Tasks / Scheduler background job

1. **Queue** — `gcloud tasks queues create <id>` with a retry config, in a setup script.
2. **Enqueuer IAM** — the producer SA needs `roles/cloudtasks.enqueuer`; the queue needs
   `roles/iam.serviceAccountUser` on the invoker SA (missing this is the classic
   Cloud Tasks `NOT_FOUND`).
3. **Receiver** — the worker service exposes the target route; set a per-task
   `dispatchDeadline` and make the handler **request-bound** (return 5xx on failure so
   the queue retries) and **idempotent** (a claim/dedupe guard against duplicate delivery).
4. **Cron** — `gcloud scheduler jobs create http` pointing at the receiver route.

## Pattern: greenfield bootstrap order

```
verify-config → enable-apis → create service accounts + IAM
   → create Cloud SQL → create secrets → deploy services → wire queues/scheduler → CDN/LB
```

Keep each stage its own idempotent script; a top-level `deploy-all.sh` orchestrates order
and takes `--skip-*` flags. Prefer running the targeted script over the full stack.

## Verification

1. **Lint the script:** `shellcheck deploy.sh`.
2. **Inspect the deployed revision:** `gcloud run services describe SERVICE --region REGION --format yaml` — confirm env vars and secret bindings landed, and no secret leaked into plain env.
3. **Tail logs after deploy** (see `gcp-logs`); hit the service once and confirm migrations applied and it's healthy.
4. **Re-run the script** against the existing environment — it must complete idempotently with no diff.

## Don'ts

- Don't leave an ad-hoc `gcloud`/console change as the only fix — codify it.
- Don't pass secrets via `--set-env-vars`.
- Don't grant `owner`/`editor` to a service account.
- Don't put DDL in a deploy script — migrations own schema.
- Don't stage build bundles inside the tracked working tree — use `mktemp -d` with a cleanup trap so a killed deploy leaves no orphans.

## Related skills

- `gcp-logs` — build + runtime log queries after a deploy.
- `cost-review` — check spend before shipping a scheduled job.
