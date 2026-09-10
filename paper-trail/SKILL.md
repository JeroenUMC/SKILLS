---
name: paper-trail
description: Build the paper trail behind a milestone, epic, or set of issues, and prosecute the claim it made.
disable-model-invocation: true
argument-hint: "<milestone URL | milestone name | label | issue numbers>"
relationships:
  invokes: [research]
---

Work finishes, the issues close, and months later someone asks *"did you really
do all of that?"* — and the only answer is 18 issues and 40 PRs. This skill turns
that into one document that answers them.

It is built on a **claim** and a **question**. The claim is what the set of issues
promised. The question is what your reader actually doubts. Everything the
document contains earns its place by bearing on one of them.

The stance is **prosecution**, not defence. You are trying to break your own
claim; the **verdict** reports what survived. A claim that survives a hostile
read is worth something — one that survives a friendly read is worth nothing, and
your reader knows it.

Two rules carry most of the weight:

- **A tick is not evidence.** Many repos close issues without ever ticking a box.
  Grade every criterion on what the PRs, commits and artifacts actually show.
- **Name every gap.** Anything you could not reach is a **blind spot** printed in
  the document, never a silence.

Scripts live in `scripts/`; run them with `python`. The document spec is
[`OUTPUT.md`](OUTPUT.md), the HTML scaffold
[`assets/paper-trail-template.html`](assets/paper-trail-template.html).

## 1 · Resolve the set

Settle `owner/name` and the selector. Take them from the user's argument; infer
the repo from `git remote get-url origin` when it is absent, and **confirm before
proceeding**.

Run `python scripts/collect_set.py --repo <owner/name>` with one of `--milestone`
(number, URL, or title substring), `--label`, `--issues 42,43`, or `--query`, plus
`--out <tmp.json>`. A project board is not a selector — resolve it to issue
numbers yourself and pass `--issues`.

It emits the issues, their linked PRs, every checkbox as a criterion, and two
derived signals you will use in step 3: `cross_repo_refs` and `path_hints`.

**Trust nothing silently.** The script exits non-zero when `errors` or `warnings`
is non-empty — a truncated set never masquerades as a complete one. Resolve every
entry or surface it to the user before continuing.

Done when: `errors` and `warnings` are empty or explicitly resolved, and the issue
count matches what the user expects.

## 2 · Fix the claim and the question

Two inputs, both confirmed by the human before any evidence work.

**The claim** — what this set promised. Read the milestone/epic description and
the issue titles and bodies, then propose it in one falsifiable sentence, plus any
sub-claims. Sets with no stated claim still made one: a `bug` label's implicit
claim is "these defects no longer occur, each with a regression test". Infer it
and put it up for correction.

**The question** — what the reader doubts. Ask the user directly; their phrasing
is the target ("I find it unlikely you were able to map everything"). It decides
which evidence is load-bearing: the same claim audited against *"did you cover
everything?"* and *"is this reproducible?"* yields two different documents.

Put both to the user with AskUserQuestion, offering an edit path. If the user
rejects every proposed claim, say so plainly and stop rather than writing a
narrative.

Done when: one falsifiable claim sentence and one reader question are written
down and confirmed by the user.

## 3 · Choose the evidence sources

The trail asserts; artifacts show. Both are in scope, **read-only** — read files
at a commit, run no commands.

- **Artifacts.** `path_hints` ranks the files the trail talks about most. Propose
  the handful that bear on the claim and confirm with the user, then read them.
  Count from the file, so "the trail claims 91 values" becomes "the sheet holds 91".
- **Cross-repo.** `cross_repo_refs` lists every reference leaving the home repo.
  Show the user the list and ask which to pull in. Repos you skip, and repos you
  cannot access, become **blind spots** by name.

Done when: every artifact and repo is either read, or recorded as a blind spot
with the reason.

## 4 · Hunt the evidence

For **every** criterion in every issue, find what discharges it and grade it:

- **met** — evidence inside this set: a PR diff, commit, artifact, or comment.
- **met elsewhere** — real evidence, from outside the set (earlier work, another
  repo, a human step recorded in a comment). Say where.
- **no evidence found** — you looked and came back empty. Record where you looked,
  so the reader can tell an absent trail from a shallow search.

`collect_set.py` reports tick state for the record. Grade past it.

Grade every criterion, including those in open issues and in issues closed as
not-planned — a criterion abandoned mid-milestone is exactly what the reader is
asking about.

This is the bulk of the work, so **fan it out**: one sub-agent per issue via the
Agent tool, each returning graded criteria with links. Sub-agents read; they do
not write the document.

When a criterion's status turns on a fact neither the trail nor the artifacts
settle, offer to spawn a background **`/research`** agent rather than guessing.

Done when: every criterion carries a grade and a link or a searched-where note —
no criterion left unexamined.

## 5 · Prosecute the claim

Now attack. Build the strongest case *against* the claim a hostile reader could
make from this evidence, hunting specifically for:

- **Scope quietly cut** — work descoped, deferred, or closed as not-planned.
- **Claims narrowed** — a promise weakened later in the trail. A PR that revises
  an earlier assertion after testing it is the single most valuable document here.
- **Coverage bounded** — verified against one snapshot, sample, or environment,
  and silent about the rest.
- **Evidence resting on one leg** — a claim whose only support is a single
  unreviewed comment or a self-report.
- **The `no evidence found` cluster** — where they concentrate tells you which
  part of the claim is softest.

Then write the **verdict** — *holds*, *holds narrowly*, *partly holds*, or
*unsupported* — as the honest reading of that case, and state what would settle
any part still open.

Done when: the case against is written, each point linked to its issue, PR, or
artifact, and the verdict follows from it rather than from the claim's ambition.

## 6 · Deliver

Write both outputs per [`OUTPUT.md`](OUTPUT.md):

- **Markdown** under `docs/paper-trail/<slug>.md`, so the audit is versioned and
  reviewable. Confirm the location with the user when that folder does not exist.
- **HTML** from the template, published with the Artifact tool, for readers with
  no repo access.

Give the user the file path and the Artifact link, and lead with the verdict and
the case against — that is what they will be asked about.

Done when: both outputs exist, every claim in them links its issue, PR, or
artifact, and the blind spots are printed rather than implied.
