---
name: refine
description: Refine an existing issue or work item into a clear, SMART, right-sized item with explicit acceptance criteria, Definition of Done, dependencies, and a Definition of Ready check.
disable-model-invocation: true
relationships:
  hands-off-to: [orchestrator-implement-issue]
---

# Refine

Turn a rough, tangled, or underspecified issue into a **ready-for-human** or **ready-for-agent** work item without prematurely prescribing implementation.

The goal is not to make an issue longer. The goal is to make the work **clear, bounded, testable, valuable, and actionable**.

## When to use

Use `/refine` when an issue has one or more of these smells:

- The reader cannot quickly explain the problem and desired outcome.
- The issue mixes several outcomes or appears larger than roughly 2 days of work.
- Acceptance criteria are vague, incomplete, duplicated, or not testable.
- The Definition of Done is missing or mixed into acceptance criteria.
- Scope, exclusions, edge cases, or dependencies are unclear.
- The issue prescribes a solution before the problem is understood.
- The value or intended user is missing.
- Timing is ambiguous, invented, or absent when timing matters.
- Different parts of the issue contradict each other.
- The issue is actually an epic, initiative, investigation, or follow-up rather than a single buildable ticket.

## Refinement principles

### 1. Clarify the problem before the solution

Extract the real user, problem, desired outcome, and value.

Prefer:

> As a <user>, I want <capability> so that <benefit>.

over a technical task statement when the work has direct user or product value.

Do not turn “replace X with Y” into a user story when the underlying issue is really a reliability, maintainability, security, or operational outcome. State that outcome instead.

Preserve known technical constraints, ADR decisions, compatibility requirements, and security requirements. Do not invent new ones.

### 2. Make scope explicit

State what is included and, when useful, what is explicitly out of scope.

A strong issue should leave the implementer knowing where to stop.

### 3. Make the issue SMART

Check the item explicitly:

- **Specific:** Who, what, context, and outcome are clear.
- **Measurable:** Completion can be observed through testable acceptance criteria.
- **Achievable:** The scope fits known capacity and dependencies.
- **Relevant:** The reason for doing it is clear and connected to the broader goal.
- **Time-bound:** A real deadline, milestone, or delivery window is captured when one exists. Never invent one; use “No external deadline” when appropriate.

Mark missing information as an explicit **gap** rather than silently filling it.

### 4. Write acceptance criteria as behaviour

Acceptance criteria should be independently verifiable and should describe the observable boundary of the work.

Prefer Given/When/Then where it improves precision:

- **Given** the relevant starting state
- **When** the user/system performs an action
- **Then** the observable result is true

Cover important success paths and meaningful edge/error cases. Do not enumerate implementation details as acceptance criteria.

Avoid criteria such as:

- “Code is clean.”
- “The API works.”
- “Handle errors correctly.”
- “Add tests.”

Those belong in the Definition of Done or need to be made observable and concrete.

### 5. Separate Acceptance Criteria from Definition of Done

**Acceptance Criteria** define whether the requested behaviour is correct.

**Definition of Done** defines whether the work is complete enough to be considered finished by the team.

Use the project's established Definition of Done when one exists. Otherwise use this baseline, tailoring only when justified:

- [ ] Acceptance criteria are all verified.
- [ ] Appropriate automated tests are added or updated, and they pass.
- [ ] Existing relevant tests/CI pass.
- [ ] Code meets project conventions and has no known avoidable quality issues.
- [ ] Relevant documentation or operational updates are completed.
- [ ] No unresolved review or verification issues remain.

Do not turn the DoD into a checklist of every possible engineering activity. Keep it relevant to the issue.
Repository/version recording belongs in the DoD unless it is user-observable behavior.

### 6. Check right-sizing and INVEST

Determine whether the item is a coherent vertical slice and whether it is small enough to implement safely.

Aim for roughly **2 days of work or less** where practical.

Check **INVEST**:

- **Independent** where practical
- **Negotiable** in implementation details
- **Valuable**
- **Estimable**
- **Small**
- **Testable**

If the issue fails the size test, recommend a split by **user-observable outcome**, not by technical layer.

### 7. Surface dependencies and unknowns

Identify:

- tickets that genuinely block this work
- external teams or systems that must act
- missing product/design decisions
- missing data, fixtures, credentials, environments, or other prerequisites
- assumptions that must be confirmed

Do not turn every relationship into a blocker. A blocker means the issue cannot meaningfully start without the dependency.

### 8. Preserve uncertainty instead of inventing certainty

When information is unavailable, label it clearly:

- **Open question** — requires a decision.
- **Assumption** — currently believed true but not verified.
- **Dependency** — another party/work item must provide something.
- **Out of scope** — explicitly excluded.

This keeps the issue honest and prevents hidden scope.

### 9. Make publication metadata explicit

Issue metadata is part of a usable work item, not an afterthought. Before publishing or updating an
issue, determine and validate:

- the target milestone;
- whether an existing milestone, a new milestone, or no milestone is the best fit;
- the tracking repository and issue;
- the implementation repository, if different;
- whether implementation follow-up issues are being created now or deferred;
- workflow readiness: `ready-for-human`, `ready-for-agent`, or `agent/blocked`;
- non-workflow labels to preserve, such as domain or team labels;
- true native GitHub blocking relationships;
- duplicate or overlapping existing issues.

Use the repository's existing canonical labels. Do not silently create or rename `ready-for-agent`
or `ready-for-human`. Do not mark an implementation issue `ready-for-agent` while a critical human
decision remains unresolved. Human-owned research, decisions, and external actions are
`ready-for-human`; blocked implementation issues are `agent/blocked`.

If `agent/blocked` is unavailable, use the repository's canonical blocked equivalent.

Preserve unrelated labels unless there is an explicit reason to change them. A dependency mentioned
in prose is not automatically a blocker: use a native blocking relationship only when the work
cannot meaningfully proceed without it.

## Process

### 1. Read the issue in full

Use the issue body, comments, linked references, and relevant project context. Do not refine from the title alone.

When the issue makes implementation or current-behaviour claims, verify them against the current source,
tests, documentation, or relevant history before classifying them as defects or requirements. Record the
commit/date checked, or mark the claim as unverified when current evidence is unavailable.

For batches or complex dependencies, delegate parallel issue diagnosis and milestone analysis to subagents; the main agent reconciles findings and owns synthesis, approval, and publication.

### 2. Diagnose before rewriting

Summarize the current problems briefly under:

- Clarity
- Scope
- SMART gaps
- Acceptance criteria gaps
- Definition of Done gaps
- Dependencies / unknowns
- Sizing / INVEST

Only report categories that matter.

### 3. Produce a refined issue

Rewrite the issue into the template below.

Do not preserve bad prose just because it was in the source. Preserve the original intent, decisions, constraints, and useful evidence.

For a proposed split, produce each resulting issue separately and state which issue blocks which.
Check existing issues for duplicates before proposing a new issue.

### 4. Run a Definition of Ready check

A refined issue is **Ready** when:

- [ ] The desired outcome and value are clear.
- [ ] Scope and important exclusions are clear.
- [ ] Acceptance criteria are specific, observable, and testable.
- [ ] The Definition of Done is present and relevant.
- [ ] Dependencies and important unknowns are identified.
- [ ] The work is right-sized or explicitly marked as needing decomposition.
- [ ] The timing expectation is known, or “No external deadline” is explicit.
- [ ] No unresolved question is critical to starting implementation.
- [ ] The target milestone is known, or the issue is explicitly marked outside a milestone.
- [ ] Existing, new, and no-milestone options were considered.
- [ ] The workflow readiness label is correct and compatible with the remaining unknowns.
- [ ] Existing canonical workflow labels and relevant domain labels are identified.
- [ ] Duplicate/overlapping issues were checked.
- [ ] Native blockers are identified separately from external dependencies and informational references.

Do not claim “Ready” when a critical ambiguity remains.

### 5. Present the result for approval

Show:

1. **Diagnosis** — what was wrong with the original issue.
2. **Refined issue** — the complete replacement text.
3. **Open questions / assumptions** — only the ones that matter.
4. **Definition of Ready status** — Ready or Not ready, with the remaining gap. State explicitly what the duplicate check found (or that none was run), per issue.
5. **Publication metadata** — milestone, labels, native blockers, external dependencies, and informational references.

Ask the user to approve the refined issue and its publication metadata before modifying or publishing it, unless the surrounding workflow explicitly authorizes direct edits. Clearly distinguish a proposed refinement from an approved and published issue.

After approval and publication, report the resulting issue number and URL for every created or
updated issue. Apply the approved milestone, labels, and native blocking relationships; do not
silently broaden the scope during publication.

A native blocking relationship is distinct from the "Blocked by" prose section. Create it via
`gh api repos/{owner}/{repo}/issues/{number}/dependencies/blocked_by -F issue_id=<database id>` —
the blocking issue's numeric `id` field (from `gh api .../issues/{number} --jq .id`), not its
display number — or the equivalent GitHub UI control.

## Refined issue template

<issue-template>

# <Short title, ideally under 10 words>

## User story

As a <user>, I want <capability> so that <benefit>.

## Context

What problem exists today and why this work matters.

## Scope

**In scope**

- <bounded outcome>

**Out of scope**

- <explicit exclusion, when useful>

## Acceptance criteria

- [ ] Given <context>, when <action>, then <observable result>.
- [ ] Given <edge/error state>, when <action>, then <observable result>.
- [ ] <Additional measurable criterion as needed>.

## Definition of Done

- [ ] Acceptance criteria are all verified.
- [ ] Appropriate automated tests are added or updated, and they pass.
- [ ] Existing relevant tests/CI pass.
- [ ] Code meets project conventions and has no known avoidable quality issues.
- [ ] Relevant documentation or operational updates are completed.
- [ ] No unresolved review or verification issues remain.

## Blocked by

- <issue/dependency>, or “None — can start immediately”.

## Dependencies

- Native blocker: <issue number>, if applicable.
- External dependency: <person/team/system>, if applicable.
- Informational reference: <issue number or document>, if applicable.

## Timing

<deadline / milestone / delivery window>, or “No external deadline”.

## Open questions

- <decision required before implementation>, if any.

## Assumptions

- <assumption>, if any.

</issue-template>

## What good refinement does not do

- It does not invent acceptance criteria to make a vague requirement look complete.
- It does not convert implementation preferences into requirements.
- It does not bury blockers in prose.
- It does not duplicate the Definition of Done into acceptance criteria.
- It does not split a coherent vertical slice into frontend/backend/database tickets merely because those are separate technical layers.
- It does not add deadlines that nobody provided.
- It does not make every issue maximally detailed; detail should exist where it removes meaningful ambiguity.
- It does not treat every issue reference as a blocker or replace native GitHub relationships with prose alone.
- It does not publish an issue with a missing milestone or incompatible workflow label when the repository uses those controls.

A good refined issue should be understandable by someone who did not attend the original conversation.
