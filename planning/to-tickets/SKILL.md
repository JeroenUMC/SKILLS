---
name: to-tickets
description: Break a plan, spec, or conversation into vertical-slice tickets with checkable acceptance criteria, published to the configured tracker.
disable-model-invocation: true
relationships:
  hands-off-to: [orchestrator-implement-issue]
---

# To Tickets

Break a plan, spec, or conversation into **tracer bullet** tickets — vertical slices, each carrying acceptance criteria a second person could verify without asking you.

## The body format is not in this file

**Read `~/.claude/skills/reference/issue-format.md` in full before you draft a single ticket body.** It is the one source of truth for the section list, the bar an acceptance criterion must clear, the evidence table, and the `gh api` mutations that set blocking and sub-issue relationships. Compose bodies from that file, never from memory of this one.

The `.scratch` variant is that format with exactly one delta: open the file with a `# <NN> — <title>` heading line, because a local file has no tracker title to render it.

## Sizing and quality

Two lenses on the same question — is this one ticket, and is it ready?

**INVEST** — **I**ndependent where practical, **N**egotiable in implementation, **V**aluable to a user or operational goal, **E**stimable from available context, **S**mall (roughly **2 days of work or less**), **T**estable through its acceptance criteria.

**SMART** — **S**pecific about who needs what and what outcome changes, **M**easurable through observable acceptance criteria, **A**chievable with the context and dependencies actually in hand, **R**elevant to the parent goal.

Where a genuine dependency exists, represent it as a blocking relationship rather than forcing artificial independence.

## Process

### 1. Gather context

Work from the conversation. If the user passes a reference (a spec path, an issue number or URL), fetch it and read its full body and comments.

Preserve the project's terminology, decisions, constraints, and unresolved questions from the source material.

### 2. Refine before splitting

When the source is ambiguous, contradictory, oversized, or too thin to write checkable acceptance criteria, run `/refine` first. Otherwise name the gaps out loud before drafting — user and expected value, scope boundaries, observable acceptance conditions, business rules and edge cases, dependencies and external ownership.

A ticket is not ready merely because it has a title and a checklist.

### 3. Explore the codebase

Read the current state of the code so titles and bodies use the project's domain vocabulary and respect the ADRs in the area you are touching.

Look for prefactoring that makes the implementation easier: make the change easy, then make the easy change.

### 4. Draft vertical slices

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every relevant layer — vertical, NOT a horizontal slice of one technical layer.
- A completed slice is demoable or independently verifiable.
- Each slice has one clear outcome rather than several loosely related ones.
- Prefactoring goes first when it unblocks simpler slices.

</vertical-slice-rules>

Give each ticket its blocking edges — the tickets that genuinely must complete before it can start.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose blast radius fans across the codebase, so a single edit breaks many call sites at once and no vertical slice lands green. Sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate call sites in batches sized by blast radius, each blocked by the expand and keeping CI green. Finally contract: delete the old form once no caller remains, blocked by every migrate batch. When batches cannot stay green alone, give them a shared integration branch and a final integrate-and-verify ticket.

### 5. Write each ticket around outcomes

Title: short, specific, searchable, **under 10 words**.

Body: the format from `~/.claude/skills/reference/issue-format.md`.

The `## User story` reads `As a <specific person or role>, I want <capability>, so that <consequence>.` Name a real role, not "a user". Reach for another concise outcome statement only where a user story genuinely does not fit.

`## Context` carries what the source material knows and the ticket reader will not: the measured state of things today, the file or command the problem lives in, the value this delivers, and the cost of leaving it alone. Describe the end-to-end behaviour the ticket makes work from the user's perspective, rather than a layer-by-layer implementation list.

Prescribe an implementation only where an existing decision, ADR, prototype, compatibility constraint, or security requirement makes the technical choice non-negotiable — and then explain the constraint. Where a prototype encodes a decision more precisely than prose can (a state machine, reducer, schema, or type shape), inline the decision-rich part and note where it came from.

### 6. Quiz the user

Present the breakdown as a numbered list. Per ticket: **title**, **blocked by**, **what it delivers**, and any **remaining gap** — named rather than papered over.

Ask:

- Does the granularity feel right (too coarse / too fine)?
- Does each ticket depend only on tickets that genuinely gate it?
- Should any be merged or split further?
- Are the acceptance criteria checkable by someone who was not in this conversation?

Iterate until the user approves. Publish a ticket with a known unresolved gap only where the user explicitly accepts it.

### 7. Publish to the configured tracker

The tickets are the same either way; only where the blocking edges live changes.

- **Local files** → one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first).
- **A real issue tracker** → one issue per ticket in dependency order, then wire the native relationships in a second pass, per `~/.claude/skills/reference/issue-format.md`. Apply the `ready-for-agent` label unless instructed otherwise. Where a relationship cannot be set, file the issue with a clean body and print the un-set relationship to the terminal.

Leave the parent issue as it stands.

Work the **frontier** — any ticket whose blockers are all done — one ticket at a time with `/orchestrator-implement-issue`, clearing context between tickets.
