# Audit Reference

## Evidence Bar

A finding must show a likely predictability gain, not merely a style preference. Prefer a controlled walkthrough that exposes the observed process. Use structural inspection or history when a walkthrough is not feasible, and state the limitation. High-confidence findings only; hypotheses belong in residual risks.

Review these failure modes:

- **Premature completion**: a step can be declared complete before its checkable, exhaustive bound is met.
- **Duplication**: one meaning has multiple authoritative homes.
- **Sediment**: stale or irrelevant material remains because removal was avoided.
- **Sprawl**: live, unique material is too large for the branch that needs it.
- **No-op**: an instruction does not change behaviour versus the default.
- **Negation**: a prohibition activates the behaviour it names instead of stating the positive target.

Also check invocation choice, context-pointer wording, progressive disclosure, co-location, leading words, legwork demand, and cross-skill handoffs. Use the `writing-great-skills` glossary for exact definitions when a term is disputed.

## Evidence Card

Every finding contains:

- Severity: `high`, `medium`, or `low`.
- Location: skill path and line or heading.
- Failure mode or lever.
- Evidence: observed walkthrough, structural proof, or history, with its limitation.
- Minimal proposed change.
- Focused validation.

Do not report a finding without all six fields. Do not propose a rewrite when deletion or a local wording change fixes the observed problem.

## Review Matrix

For every in-scope skill, account for:

- Invocation metadata and whether its context load or cognitive load is justified.
- Every branch and disclosed reference, including pointer wording and link resolution.
- Every step's checkable, exhaustive completion criterion.
- Every failure mode that has evidence, not a checklist verdict manufactured without evidence.
- Duplication and contradictions with the other in-scope skills.

## Approval And Change Boundary

Present the complete bounded patch plan before asking for approval. One approval authorizes only the selected findings. A later discovery is a new finding, not implied approval. Apply no speculative cleanup.

## Validation

Structural validation checks:

- YAML frontmatter parses and has the expected `name` and invocation setting.
- Every disclosed relative Markdown link resolves.
- Every changed path is audit-owned and intended.
- The worktree contains no accidental unrelated edit.

Behavioral validation is a controlled walkthrough of each changed branch or handoff. Check that the same ordered process is followed and that each completion criterion is reached before the next step. If no runtime harness exists, record the prompt/process and observed path instead of claiming a test suite passed.
