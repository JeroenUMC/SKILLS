# Issue format

The single source of truth for issue bodies written by `/refine`, `/to-tickets`, and any skill
that files a tracker issue. Read this before composing a body.

## Body template

GitHub renders the issue title itself. The body starts at the first `##`.

```markdown
## User story

As a <specific person or role>, I want <capability>, so that <consequence>.

## Context

<Prose. The measured state of things today, the file or command it lives in, and the cost of
leaving it alone. This is the section a reader lands on in three weeks.>

## Scope

**In scope**
- <what this issue changes>

**Out of scope**
- <what it deliberately does not change, and where that work goes instead>

## Acceptance criteria

- [ ] <checkable outcome>
- [ ] <checkable outcome>

## Assumptions

- <what the issue takes for granted, so a wrong one surfaces before the work starts>

## Open questions

- <unresolved, does not block starting>
```

`## User story`, `## Context`, and `## Acceptance criteria` are always present.

`## Scope` is present wherever something plausibly creeps in. Where the boundary matters in only
one direction — nothing to fence in, but real work to fence out — use a plain `## Out of scope`
section in its place. Where the issue's edges are obvious, omit both.

`## Assumptions` and `## Open questions` are emitted only when they carry content. Reach for
`## Open questions` — an issue with none is usually an issue whose unknowns went unexamined.

**Custom sections are welcome.** Where material earns its own heading — a reproduction, a
mechanism, a safety constraint the next person must not rediscover — give it one, placed after
`## Context`. The standard sections are a floor, not a cage; an issue that has outgrown them is a
good issue, and flattening it back into `## Context` costs more than it gains.

## What makes an acceptance criterion checkable

Each criterion names a **concrete noun** — a file, command, sheet, column, value, exit code, or
rendered string — and states an outcome a second person could verify without asking the author.

Write the assertion flat. `Given … when … then …` adds words without adding rigour, and it makes
a vague criterion read as a precise one. Where a precondition genuinely changes the outcome, it
fits in the same clause: "After validation passes, the upload records …".

| | |
|---|---|
| **Weak** | The transfer completes without an unresolved credential, encryption, or transfer error. |
| | *Nothing here can be checked. "Unresolved" and "error" name no artifact and no observable state.* |
| **Strong** | The `SpecimenType` sheet no longer maps a uterus to `Structure of lymph node`. |
| **Strong** | `rumc-build-mappers` run twice on the same TSV produces a byte-identical workbook. |
| **Strong** | `preprocess.py` exits `2` and names the unrecognised modality in its message. |

Apply the test to every criterion before filing. A criterion that survives only because the reader
already knows what the author meant has failed it.

### Test and CI criteria

Probe before asserting either — and probe the **implementation** repository, the one the work lands
in, which is often not the tracking repository the issue is filed in. An issue tracked in a
coordination repo may still take test criteria when its code lives elsewhere; an issue tracked
beside a test suite takes none when its work is a manual procedure.

- A test criterion is legitimate when the repo has a test directory **and** a runner config
  (`pyproject.toml`, `vitest.config.*`, and so on). Name the behaviour under test, not the act of
  testing: "`test_mapping_keys.py` covers the multi-antibody split" beats "tests are added".
- A CI criterion is legitimate only when `.github/workflows` holds a workflow the repo authored.
  Copilot's injected `dynamic/…` entries are not CI.

Where the repo has neither, the acceptance criteria carry the whole verification burden — write
them so a person can walk them by hand.

### Coordination and manual-procedure issues

An issue whose work is a phone call, a UI experiment, or an upload still takes checkable criteria.
They name the recorded result: which environment, which identifier, where the answer landed. Do
not reach for test or code-review language to fill the section out.

### Refining an issue that is already part-done

A checked criterion asserts something that must become true, so a list of them is a poor record of
what already did. Move the delivered outcomes into `## Context` as measured prose — what landed,
in which PR or commit, and what the numbers are now — and leave `## Acceptance criteria` holding
only what remains open. Verify each carried-forward claim against the current state of the code
rather than the issue's own earlier prose; a stale headline number is worse than none.

## Evidence goes in a table

Measured findings — affected values, row counts, before/after states — go in a table, not prose
bullets. A table is the densest reviewable form and makes an incomplete survey visible.

```markdown
| Value | Rows | Effect | Status |
|-------|-----:|--------|--------|
| APas | 142 | maps to the parent concept | answered |
| Dsn | 11 | stays excluded | pending |
```

## Blockers, dependencies, and critical path

Dependencies live in GitHub's native relationships, not in the body. There is no `## Blocked by`
and no `## Dependencies` section.

Add a sentence to `## Context` in exactly two cases:

- **The reason is not evident from the blocker's title.** "The scope above cites `run_dir` and the
  run-scoped output tree, neither of which exists on `main` yet — rebase on #34 before starting."
- **The dependency is not an issue at all** — a missing fixture, an answer owed by another team, a
  dataset that has not arrived. A native relationship cannot hold these, so the prose must.

Check each listed blocker's current state before carrying it forward. A closed blocker whose
blocking *condition* still holds — the issue shipped, the answer it was waiting on never arrived —
is the second case, not the first: drop the relationship and name the real condition in prose.

Critical-path standing belongs in `## Context` when it is true and load-bearing: "This is 90% of
the milestone's remaining rows, so it is the critical path once #62 returns." Deadlines and
delivery windows do not appear in the body at all.

## Setting the relationships

Verified against `gh` 2.90.0. There is no `gh issue` subcommand and no extension for either — both
go through `gh api`.

Both mutations take **node IDs**, and the REST endpoints take the numeric **database `id`**, not
the display number. Resolve first:

```bash
gh api repos/<owner>/<repo>/issues/<number> --jq '{id, node_id}'
```

**Blocked by** — `<blocked>` becomes blocked by `<blocker>`:

```bash
gh api graphql -f query='
  mutation($issue:ID!, $blocker:ID!) {
    addBlockedBy(input:{issueId:$issue, blockingIssueId:$blocker}) { issue { number } }
  }' -f issue=<blocked-node-id> -f blocker=<blocker-node-id>
```

**Sub-issue** — attach `<child>` under `<parent>`:

```bash
gh api graphql -f query='
  mutation($parent:ID!, $child:ID!) {
    addSubIssue(input:{issueId:$parent, subIssueId:$child}) { issue { number } }
  }' -f parent=<parent-node-id> -f child=<child-node-id>
```

Read the current state with `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by` and
`… /sub_issues`.

Create every issue first, then wire the relationships in a second pass — a blocker's number is
unknown until it exists.

### When a relationship cannot be set

File the issue with a clean body and print the relationship that did not land:

```
Created #47.
Could not set: #47 blocked by #42 — <the error>
Wire it manually, or re-run once resolved.
```

The body never absorbs the relationship as a fallback. A `Blocked by: #42` line in prose is
invisible to GitHub and drifts out of date, which is the state this format exists to end.

## Issue types

`gh issue create --type` does not exist in 2.90.0, and org issue-type endpoints require the
`admin:org` scope. Carry category on a label instead.
