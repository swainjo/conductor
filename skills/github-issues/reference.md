# GitHub issues — reference

Repo identity: `conductor/github.md` in the **project**. Replace `owner/repo`
and `#N` below with that file's owner/repo.

## Epics and sub-issues

On GitHub, an **epic is a parent issue with sub-issues**. Sub-issues are normal
issues with a `parent` pointing at the epic issue.

```text
#10  Epic title (epic — parent issue)
├── #12  First sub-issue
└── #13  Second sub-issue
```

| Term | Meaning |
|------|---------|
| Epic | Parent issue that owns child sub-issues |
| Sub-issue | Issue with `parent` = epic number |
| Project / Milestone | Separate release grouping — not the epic |
| Sibling | Another sub-issue under the same parent epic |

**Every epic has an epic track (track check):** before starting sub-issue work,
confirm the parent epic has an epic track (search
`conductor/tracks/*/metadata.json` for `"github": "owner/repo#N"`) and open one
first if it is missing.

Create a sub-issue:

```bash
gh issue create --title "TITLE" --body "…" --parent PARENT-N
```

## Prompt prefixes

```text
GitHub: #12 — Short title
Track: conductor/tracks/<track_id>/
Implement per plan.md against the issue's acceptance criteria; update GitHub at
phase boundaries.
```

## Branch names

```text
12-short-slug
13-another-slug
```

Issue number, kebab-case slug.

## Commit messages

```text
feat(area): add the thing (#12)
```

## PR title and body

**Title:**

```text
#12: Imperative summary
```

**Body (minimal):**

```markdown
## GitHub
<issue URL>

## Summary
- …

## Test plan
- [ ] <project test command from conductor/workflow.md>
```

Do **not** add `Closes #12` until the user has explicitly authorized close in
this session. GitHub auto-closes the issue on merge when that keyword is
present.

## GitHub comment templates

### Phase / milestone

```markdown
**Progress (#12)**

- …

Next: …

Branch: `12-short-slug`
```

### PR opened

```markdown
**PR ready for review (#12)**

PR: https://github.com/…/pull/NNN

Verify:
1. <project test command>
```

### Done

```markdown
**Shipped (#12)**

Merged PR #NNN.

Closing #12.
```

> Post this (and close the issue) **only when the user has explicitly said to
> close the issue**. See SKILL §3 *Status transitions* hard rules.

### Blocked

```markdown
**Blocked (#12)**

Waiting on: …

Branch pushed; will resume when unblocked.
```

## Conductor metadata.json (new tracks — pointer only)

```json
{
  "track_id": "shortname_YYYYMMDD",
  "github": "owner/repo#12",
  "github_url": "https://github.com/owner/repo/issues/12"
}
```

Pointer only — no `type`, `description`, `status`, or `parent_github`. `parent`
(the epic, if any) is read from the GitHub issue via `gh issue view`.

## plan.md header

```markdown
**GitHub:** [#12](https://github.com/owner/repo/issues/12)
```

## plan.md close task

```markdown
- [ ] Close **#12** on GitHub; link PR in issue comment
```

This plan task is a reminder, **not** authorization.
