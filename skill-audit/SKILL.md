---
name: skill-audit
description: Evidence-backed review of skills used in this session.
disable-model-invocation: true
---

# Skill Audit

Audit the skills used since the start of this session, including this skill, and any delegated skill use visible in the trace. The goal is a more predictable process, not shorter prose or identical outputs.

Read [`AUDIT.md`](AUDIT.md) before reviewing. It contains the failure modes, evidence bar, finding format, and validation contract.

## Process

### 1. Reconstruct scope

First determine whether any skill files changed during the session, or whether a delegated agent visibly invoked or modified a skill.
If neither occurred, record the current skill as the only in-scope skill and skip full historical reconstruction.
If either occurred, list every skill visibly invoked in the session and every delegated skill use visible in the trace. Include the current skill.
Record uncertainty rather than guessing; an invisible invocation is out of scope.

Completion criterion: when reconstruction is required, the scope list accounts for every observable skill invocation and names every missing trace entry. Otherwise, the audit records why reconstruction was skipped.

### 2. Inspect the skills

Read each in-scope `SKILL.md` and its directly disclosed references. Inspect the invocation metadata, links, branches, steps, completion criteria, and single sources of truth. Review each skill independently, then inspect the chain for contradictory instructions, duplicated meanings, and broken handoffs.

Use git history in this checkout when it can distinguish a recurring or stale problem from a current one. Do not treat an untested hypothesis as a finding.

Completion criterion: every in-scope skill and every observed cross-skill handoff has either a finding with evidence or an explicit no-finding note.

### 3. Test candidate improvements

For each candidate, run a focused behavioral check when feasible: use a controlled walkthrough of a representative prompt/process and compare the observed path with the skill's completion criteria. Otherwise perform structural checks and label the remaining uncertainty. Prefer deletion for redundant or no-op content. Keep only high-confidence findings that are likely to improve predictability.

Completion criterion: every reported finding has an observed or structurally verified basis, and every unverified idea is excluded from the patch plan.

### 4. Present the audit

Report findings first, ordered by severity. Use the evidence card format in `AUDIT.md`. For each finding provide the smallest proposed change and its validation. Then state the reviewed scope, checks performed, and residual risks. If no evidence-backed improvement remains, say that no change is justified.

Ask for one approval covering the selected findings. Do not edit files, commit, or push before approval.

Completion criterion: the user has either approved a bounded set of findings or declined/no changes are justified; no ambiguous approval is treated as authorization.

### 5. Apply and validate the approved batch

Apply only the approved minimal patch to the canonical checkout at `C:\Users\Z768180\.claude\skills`. Include any required skill files, disclosed references, agent metadata, and invocation plumbing that are part of the approved plan. Preserve unrelated worktree changes.

Run structural checks for frontmatter, required files, relative links, and repository status. Run the focused behavioral check for every changed behavior. Report failures and residual risks; do not claim completion while any approved change lacks validation.

Completion criterion: every approved change is present, every changed link and metadata field resolves, every changed behavior has a focused check, and unrelated changes remain untouched.

### 6. Keep the paper trail

When changes were applied, commit all audit-owned changes in the canonical checkout with a concise message. Verify that `origin` is exactly `https://github.com/JeroenUMC/SKILLS.git` (or its equivalent SSH URL) and that the target branch is `main` before pushing. Push the commit to `main`. If push is unavailable, retain the local commit and report the blocker and commit ID. A clean audit creates no commit or push.

Completion criterion: applied changes are committed; the commit is pushed to the verified `JeroenUMC/SKILLS` `main`, or the local commit and push blocker are explicitly reported.
