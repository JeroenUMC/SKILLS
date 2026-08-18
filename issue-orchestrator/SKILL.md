---
name: issue-orchestrator
description: Implement one approved spec or issue through testing, verification, review, and local commit or draft pull request.
disable-model-invocation: true
---

# Issue Orchestrator

This is the canonical workflow for implementing one approved spec or issue. It supports two modes:

- **Standalone:** invoked directly by the user. Work in the current repository, branch, and worktree. Commit locally; do not push or create a pull request unless explicitly requested.
- **Delegated:** invoked by `/milestone-orchestrator` with an approved run ID, issue assignment, isolated worktree and branch, and per-role model metadata. Commit, push, and create a draft PR targeting `main`.

Do not use standalone mode inside a milestone orchestration run.

## Authority

- In delegated mode, work only in the assigned Git worktree and branch `agent/issue-<number>-<slug>` based on `main`.
- In both modes, do not merge, close issues, change project fields, release, or perform destructive operations.
- The verification agent is read-only. The issue orchestrator owns all edits, including tests and review fixes.
- Only `/milestone-orchestrator` writes shared `state.json`.

## Sequence

1. **Research:** in delegated mode, spawn a research subagent with the complete issue and metadata. In standalone mode, inspect the supplied spec and repository guidance directly unless research is needed.
2. **Implement:** make the smallest correct change. Use `/tdd` at agreed seams, working in red-green slices. Run typechecking and focused tests regularly. Do not silently invent unresolved product decisions; pause for underspecification.
3. **Verify:** run relevant tests and check acceptance criteria. Run the full relevant test suite once at the end. In delegated mode, also spawn a read-only verification subagent.
4. **Review:** perform the two-axis `/code-review` covering Standards and Spec. In delegated mode, spawn the review subagent after verification.
5. **Fix:** implement actionable review findings, document rejected or out-of-scope suggestions in the report, then rerun verification and relevant tests.
6. **Finalize:** standalone mode commits locally and reports the result. Delegated mode commits with an issue-referencing message, pushes the branch, and opens a draft PR to `main`. Link the PR to the issue without closing it.

## Pauses

Pause only for a defined blocker: subagent failure, unresolved test failure, missing access, underspecified issue, dirty/conflicting branch, human decision, or semantic merge conflict. Preserve the worktree and diagnostics, and report exactly what the user must decide or fix. In delegated mode, let the milestone orchestrator add the `agent/blocked` status and update the authoritative `state.json`; do not continue to PR creation after a blocking failure.

## Reporting

Return a structured result. In delegated mode include issue number, status, branch, worktree, commits, tests and commands, research path/report, verification result, review findings and fixes, PR URL if created, blockers, and recommended next action. Do not write shared run state; the milestone orchestrator is its sole authoritative writer. In standalone mode report the changed files, tests, review result, commit, and any blocker.
