---
name: to-tickets
description: Break a plan, spec, or conversation into SMART, tracer-bullet tickets with explicit acceptance criteria, a Definition of Done, and blocking edges, published to the configured tracker.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into a set of **SMART tickets** — tracer-bullet vertical slices with explicit, testable acceptance criteria, a clear Definition of Done, and the tickets that block them.

## Core standard: a ticket must be SMART

Every published ticket must satisfy all five dimensions,common in SCRUM software development:

- **Specific** — says who needs what, in what context, and what outcome is being changed. Prefer a user story or equivalent user-centered statement.
- **Measurable** — defines observable evidence of completion through explicit acceptance criteria. Avoid words such as “better”, “properly”, “works”, or “support” unless they are made observable.
- **Achievable** — is realistically implementable with the available context, dependencies, and team capacity. Do not invent missing technical or product decisions; surface them as gaps during refinement.
- **Relevant** — explains why the work matters and how it serves the parent goal, user, product, or operational need.
- **Time-bound** — includes a known deadline, target date, milestone, or delivery window when one exists. Never invent a date. When no legitimate time constraint exists, explicitly mark the timing as “No external deadline” rather than fabricating one.

SMART is a quality gate, not a request to force every ticket into an arbitrary deadline.

## common practice
to-tickets is usually invoked with an ADR in mind, which should coincide with a milestone on the tracker.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

Do not silently fill important gaps. Preserve project terminology, decisions, constraints, and unresolved questions from the source material.

### 2. Refine before splitting when necessary

If the source material is ambiguous, contradictory, oversized, or missing enough information to write SMART acceptance criteria, do not hide those problems inside ticket prose.

Use `/refine` first when available. Otherwise, identify the unresolved gaps before drafting the ticket breakdown. In particular, surface missing:

- user/problem and expected value
- scope boundaries and exclusions
- observable acceptance conditions
- business rules and important edge cases
- dependencies or external ownership
- target timing, when relevant
- project-specific Definition of Done expectations

A ticket is not ready merely because it has a title and a checklist.

### 3. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. “Make the change easy, then make the easy change.”

### 4. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every relevant layer — vertical, NOT a horizontal slice of one technical layer.
- A completed slice is demoable or independently verifiable.
- Each slice should be small enough to fit in roughly **2 days of work or less** where practical. If a slice is larger, split it unless there is a compelling reason not to.
- Each slice must have one clear outcome rather than several loosely related outcomes.
- Any prefactoring should be done first when it unblocks simpler slices.

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other tickets that genuinely must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol, etc. — whose blast radius fans across the whole codebase, so a single edit breaks many call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate call sites in batches sized by blast radius, each batch blocked by the expand and keeping CI green. Finally contract: delete the old form once no caller remains, blocked by every migrate batch. When batches cannot stay green alone, use the sequence but let them share an integration branch and a final integrate-and-verify ticket.

### 5. Write the issue around outcomes, not implementation

Each ticket should contain:

1. **Title** — short, specific, and searchable; aim for **under 10 words**.
2. **User story / outcome** — `As a [user], I want [capability] so that [benefit].` Use another concise outcome statement only when a user story genuinely does not fit.
3. **Context** — only the information needed to understand the problem, scope, and value.
4. **Acceptance Criteria** — explicit, observable, testable conditions. Prefer Given/When/Then when it improves clarity.
5. **Definition of Done** — the quality/completion bar that applies after the acceptance criteria are met.
6. **Blocked by** — only true gating dependencies.
7. **Timing** — a real deadline, milestone, or delivery window when known; otherwise explicitly state “No external deadline”.

Do not prescribe an implementation unless an existing decision, ADR, prototype, compatibility constraint, or security requirement makes the technical choice non-negotiable. Explain the constraint, not an imaginary implementation plan.

### 6. Keep Acceptance Criteria separate from Definition of Done

**Acceptance Criteria answer:** “How do we know this behaviour satisfies the requested need?”

**Definition of Done answers:** “What must be true for us to call this issue finished?”

Acceptance criteria should describe product or user-visible behaviour, business rules, data outcomes, and important edge cases.

The Definition of Done should cover engineering completion such as appropriate tests, code quality, review/CI expectations, documentation or operational updates when applicable, and a clean working state.

Never duplicate the Definition of Done into every acceptance criterion.

### 7. Apply INVEST as a sizing and quality check

Before proposing publication, check that each ticket is:

- **Independent** where practical
- **Negotiable** in implementation details
- **Valuable** to a user, product, or operational goal
- **Estimable** from the available context
- **Small** enough to complete in roughly 2 days or less where practical
- **Testable** through explicit acceptance criteria

Do not force artificial independence where a genuine dependency exists; represent the dependency with a blocking edge instead.

### 8. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**
- **Blocked by**
- **What it delivers**
- **SMART status** — note any remaining gap rather than pretending it is resolved

Ask the user:

- Does the granularity feel right (too coarse / too fine)?
- Are the blocking edges correct — does each ticket depend only on tickets that genuinely gate it?
- Should any tickets be merged or split further?
- Are the acceptance criteria sufficient and testable?
- Is the Definition of Done appropriate for this work?

Iterate until the user approves the breakdown.

Do not publish a ticket with known unresolved SMART gaps unless the user explicitly accepts that gap and the tracker workflow allows it.

### 9. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured — the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's “Blocked by” lists the numbers/titles it depends on.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order so blocking edges can reference real identifiers. Use native blocking/sub-issue relationships where supported; otherwise write the blocking issues in the body. Apply `ready-for-agent` unless instructed otherwise.

Work the **frontier**: any ticket whose blockers are all done.

Do NOT close or modify a parent issue.

## Default Definition of Done

Use the project's established Definition of Done when one exists. Otherwise use this baseline and remove items that genuinely do not apply:

- [ ] Acceptance criteria are all verified.
- [ ] Appropriate automated tests are added or updated, and they pass.
- [ ] Existing relevant tests/CI pass.
- [ ] Relevant documentation or operational updates are completed.
- [ ] No unresolved review or verification issues remain.

The Definition of Done is allowed to contain conditional items. Do not require irrelevant documentation or tests merely to satisfy a checklist.

## Local ticket template
Use this for the local files under .scratch.

<local-ticket-template>

# <NN> — <Ticket title>

## User story

As a <user>, I want <capability> so that <benefit>.

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Given <context>, when <action>, then <observable result>.
- [ ] <Additional observable criterion or important edge case>.

## Definition of Done

- [ ] Acceptance criteria are all verified.
- [ ] Appropriate automated tests are added or updated, and they pass.
- [ ] Existing relevant tests/CI pass.
- [ ] Relevant documentation or operational updates are completed.
- [ ] No unresolved review or verification issues remain.

## Blocked by

<NN> — <Ticket title>, or “None — can start immediately”.

## Timing

<deadline / milestone / delivery window>, or “No external deadline”.

</local-ticket-template>

## Issue template
Use this to post as the final issue.
<issue-template>

## User story

As a <user>, I want <capability> so that <benefit>.

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

## Why it matters

The user, product, or operational value this delivers.

## Acceptance criteria

- [ ] Given <context>, when <action>, then <observable result>.
- [ ] <Additional observable criterion or important edge case>.

## Definition of Done

- [ ] Acceptance criteria are all verified.
- [ ] Appropriate automated tests are added or updated, and they pass.
- [ ] Existing relevant tests/CI pass.
- [ ] Code meets project conventions and has no known avoidable quality issues.
- [ ] Relevant documentation or operational updates are completed.
- [ ] No unresolved review or verification issues remain.

## Blocked by

- <blocking issue reference>, or “None — can start immediately”.

## Timing

<deadline / milestone / delivery window>, or “No external deadline”.

</issue-template>

Avoid specific file paths or code snippets — they go stale fast. Exception: when a prototype encodes a decision more precisely than prose can (for example a state machine, reducer, schema, or type shape), inline only the decision-rich part and note that it came from the prototype.

Work the frontier one ticket at a time with `/implement`, clearing context between tickets.
