---
name: finalize
description: Close the current session by auditing loose ends, provenance, traces, worktree state, and skill use.
disable-model-invocation: true
argument-hint: "Optional closeout focus or requested trace"
relationships:
  invokes: [skill-audit]
---

# Finalize

Run this skill manually at the end of a session. Finalize establishes an evidence-backed stopping
point. It does not silently finish arbitrary work or clean the repository.

## Sequence

### 1. Reconstruct the session

Identify the user's requested outcomes, decisions, invoked skills, delegated work, artifacts, tests,
issue/PR references, and claimed results. Record uncertainty instead of inferring missing history.

### 2. Find loose ends

Compare requested outcomes with actual results. Classify each gap as `completed`, `blocked`,
`deferred`, `abandoned`, or `needs-decision`. Include unresolved tests, review findings, introduced
TODOs, paused orchestration runs, and missing handoff information.

### 3. Inspect state and provenance

Read repository instructions first, then inspect branch, HEAD, upstream, staged and unstaged changes,
untracked files, relevant ignored artifacts, recent history, and submodule status. Inspect nested
repositories independently. Never edit submodule contents from this closeout.

For each changed path classify provenance as:

- **Owned:** supported by the conversation, touched paths, commits, or explicit attribution.
- **Pre-existing:** evidenced by an initial snapshot.
- **Unattributed:** present but not safely attributable.
- **Generated:** likely test output, cache, orchestration state, or temporary output.

If no initial snapshot exists, say that provenance is uncertain. Never delete, hide, stash, reset, or
clean an unattributed change.

### 4. Reconcile the paper trail

Find existing commits, issues, PRs, ADRs, specs, tickets, handoffs, orchestration state, and session
artifacts. Prefer linking to an existing trace over creating a duplicate. Identify decisions or work
that lack the appropriate durable record:

- implementation decision: ADR or existing decision record;
- work request or bug: configured issue tracker;
- implementation: commit and PR when the repository workflow permits;
- cross-session continuation: `/handoff` artifact;
- orchestration execution: existing run state and reports.

Do not automatically invoke `/to-spec` or `/to-tickets`; report when either is appropriate and ask.

### 5. Audit skills

Invoke `/skill-audit` exactly once as a required phase, including `skill-audit` itself and any
delegated skill use visible in the trace. Keep skill-quality findings separate from finalize findings.
Do not treat the audit as approval to edit, commit, or push.

### 6. Ask before mutating

Read-only inspection, structural checks, a final report, and a temporary `/handoff` artifact are safe.
Require explicit approval before editing source, tests, docs, ADRs, session artifacts, issues, PRs,
labels, project fields, staging, committing, pushing, deleting, changing `.gitignore`, modifying
submodule pins, or resolving decisions by inference.

If approved, make only the bounded actions named by the user. Recheck the worktree and traces after
those actions. Never merge, close issues or PRs, force-push, amend, rebase, or perform destructive
Git operations as part of finalize.

## Completion report

Return a structured closeout containing:

- status: `closed`, `closed-with-loose-ends`, `blocked`, or `needs-approval`;
- requested outcomes and evidence;
- loose ends with owner, state, and next action;
- worktree and submodule inventory;
- provenance confidence and unknowns;
- existing and missing paper trails;
- the `/skill-audit` result and separately pending audit approvals;
- artifacts, commits, issues, PRs, handoff paths, and orchestration run IDs;
- actions performed and explicitly not performed;
- one concise approval request when mutation is needed.

A clean closeout means the stopping point is explicit, not necessarily that the worktree is clean.
