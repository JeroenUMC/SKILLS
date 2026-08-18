---
name: issue-orchestrator
description: Execute one approved milestone issue through research, implementation, verification, review, fixes, and a draft pull request.
disable-model-invocation: true
---

# Issue Orchestrator

This is an internal child workflow. Run it only when delegated by `/milestone-orchestrator` with an approved run ID, issue assignment, worktree, branch, and per-role model metadata. It is not a standalone issue implementation command.

## Authority

- Work only in the assigned Git worktree and branch `agent/issue-<number>-<slug>` based on `main`.
- Do not merge, close issues, change project fields, release, or perform destructive operations.
- The verification agent is read-only. The issue orchestrator owns all edits, including tests and review fixes.
- A draft PR targeting `main` is the terminal success condition. Do not wait for CI.

## Sequence

1. **Research:** spawn a research subagent with the complete issue, repository guidance, acceptance criteria, dependency context, and assigned research model metadata. Return its findings to the milestone orchestrator; require primary sources and code references where applicable.
2. **Implement:** use the research report and issue contract to implement the smallest correct change. Run focused tests regularly. Do not silently invent unresolved product decisions; pause for underspecification.
3. **Verify:** spawn a read-only test/verification subagent. It inspects the diff, runs relevant tests, checks acceptance criteria, and reports failures or missing coverage. It may suggest tests but must not edit files.
4. **Review:** spawn a review subagent after verification. Review the issue contract, research, diff, tests, and repository standards for correctness, security, regressions, and maintainability.
5. **Fix:** implement all actionable review findings. Document rejected or out-of-scope suggestions in the run report. Rerun verification and relevant tests; pause if failures remain unexplained or unresolved.
6. **PR:** commit with an issue-referencing message, push the branch, and open a draft PR to `main`. Include summary, tests, research/verification/review outcomes, and any accepted limitations. Link the PR to the issue without closing it.

## Pauses

Pause only for a defined blocker: subagent failure, unresolved test failure, missing access, underspecified issue, dirty/conflicting branch, human decision, or semantic merge conflict. Preserve the worktree and diagnostics, report exactly what the user must decide or fix, and let the milestone orchestrator add the `agent/blocked` status and update the authoritative `state.json`. Do not continue to PR creation after a blocking failure.

## Reporting

Return a structured result to the milestone orchestrator: issue number, status, branch, worktree, commits, tests and commands, research path/report, verification result, review findings and fixes, PR URL if created, blockers, and recommended next action. Do not write the shared run state; the milestone orchestrator is its sole authoritative writer.
