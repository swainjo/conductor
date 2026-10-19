---
name: postgres-dev
description: >
  Practical PostgreSQL patterns for JSONB-heavy and vector/text-search schemas: JSONB querying + indexing, pgvector similarity, pg_trgm substring search, partial indexes, CHECK constraints, and reading `EXPLAIN ANALYZE`. Use when writing or reviewing SQL (DDL or DQL). Triggers: "query the JSONB", "pgvector", "vector similarity", "trgm index", "CHECK constraint", "partial index", "is this query slow".
---

# Postgres Dev (JSONB / pgvector / trgm / indexes)

Practical PostgreSQL patterns for JSONB-heavy and vector/text-search schemas: JSONB querying + indexing, pgvector similarity, pg_trgm substring search, partial indexes, CHECK constraints, and reading `EXPLAIN ANALYZE`. Use when writing or reviewing SQL (DDL or DQL). Triggers: "query the JSONB", "pgvector", "vector similarity", "trgm index", "CHECK constraint", "partial index", "is this query slow".

## JSONB

```sql
-- -> returns JSONB, ->> returns text. Don't confuse them in CHECK constraints.
SELECT data -> 'meta' ->> 'name' FROM app.docs WHERE id = $1;

-- @> is "contains" — the workhorse membership test
SELECT * FROM app.docs WHERE data @> '{"kind": "invoice"}'::jsonb;

-- unnest an array into rows
SELECT jsonb_array_elements(data -> 'items') AS item FROM app.docs WHERE id = $1;

-- filter to array elements matching a shape
SELECT data -> 'items' FROM app.docs
WHERE data -> 'items' @> '[{"status": "open"}]'::jsonb;
```

Other operators: `jsonb_path_query` / `jsonb_path_exists` for complex extraction;
`jsonb_typeof(col) = 'array'` is the CHECK-friendly type guard.

**Indexing JSONB — don't reflexively full-GIN everything (they're large):**
- `USING GIN (col)` — broad containment, big, supports many operators.
- `USING GIN (col jsonb_path_ops)` — smaller, only supports `@>`. Prefer when `@>` is all you need.
- Expression index on a hot path: `CREATE INDEX ON app.docs ((data ->> 'public_token'));`

## pgvector

Cosine distance is the common default for embeddings.

```sql
SELECT id, 1 - (embedding <=> $1) AS similarity
FROM app.items
WHERE embedding IS NOT NULL
ORDER BY embedding <=> $1
LIMIT 10;
```

Operators: `<->` L2, `<#>` negative inner product, `<=>` cosine.

**Index op-class MUST match the query operator or you get a silent seq scan:**
```sql
CREATE INDEX ON app.items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
-- lists ≈ sqrt(rows). hnsw is available on pgvector ≥0.5 (faster query, slower build).
```
Mismatched op-class (`vector_l2_ops` index + `<=>` query) → sequential scan, no error,
plausible-but-wrong ranking.

## pg_trgm substring / fuzzy search

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_docs_title_trgm ON app.docs USING GIN (title gin_trgm_ops);
```
Query with `ILIKE '%foo%'` (planner uses the trgm index) or the `%` similarity operator
(tune `pg_trgm.similarity_threshold`).

## Partial indexes (hot-path lookups where most rows don't match)

```sql
CREATE INDEX idx_jobs_active ON app.jobs (started_at) WHERE status IN ('running', 'retrying');
```
Far smaller and faster than a full index when the predicate prunes hard.

## CHECK constraints

Compare on **text** (`->>`) in JSONB CHECKs — never JSONB `=` (equality is exact on key
order + whitespace). When the allowed set comes from application code, generate the value
list from that single source of truth rather than hardcoding it in the DDL, so DB and app
can't drift.

```sql
ALTER TABLE app.feedback
  ADD CONSTRAINT feedback_reason_check
  CHECK (reason IS NULL OR reason IN ('a','b','c'));      -- values generated from the app enum
```

## Reading EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE <query>;
```
Watch for: `Seq Scan` on a table that should be indexed (op-class/expression mismatch);
high `loops:` on the inner side of a nested loop; `Rows Removed by Filter: >> Rows:`
(index doesn't cover the predicate); `Buffers: shared read=` in the millions on a "warm"
query (index unused — run `ANALYZE`).

## Don'ts

- Don't ship DDL outside your migration tool — schema drift breaks single-head checks or, worse, makes prod and dev disagree silently.
- Don't full-GIN every JSONB column — prefer `jsonb_path_ops` or expression indexes on the specific path.
- Don't `ORDER BY (embedding <=> $1) LIMIT n` without a matching index op-class.
- Don't compare JSONB with `=` in a CHECK — use `->>` and compare text.
- Don't hold a pooled connection across `await`-spanning business logic.

## Related skills


- `compose-logs` — container logs for a local Postgres.
- `local-ci-lint` — the changed-files gate for the code around the SQL.
