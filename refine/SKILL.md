---
name: refine
description: Refine an issue's content — challenge whether and how it should be done, then shape what survives into a right-sized work item with checkable acceptance criteria.
disable-model-invocation: true
relationships:
  hands-off-to: [orchestrator-implement-issue]
---

# Refine

Refinement in the Scrum sense: first **challenge** the issue — is its goal still right, and is this the right way to reach it? — then turn what survives into a **ready-for-human** or **ready-for-agent** work item without prescribing the implementation.

The goal is not a longer issue. The goal is work that is worth doing, clear, bounded, checkable, and actionable. An issue that fails the challenge may leave refinement closed, merged, or reprioritised rather than rewritten.

## When to use

- The reader cannot state the problem and the desired outcome after reading it.
- The issue mixes several outcomes, or looks larger than roughly 2 days of work.
- Acceptance criteria are missing, duplicated, or unverifiable without asking the author.
- Scope, exclusions, edge cases, or dependencies are unclear.
- It prescribes a solution before the problem is understood.
- The value or the intended user is missing.
- Parts of the issue contradict each other.
- It is really an epic, an investigation, or a follow-up rather than one buildable ticket.
- The world has moved since it was written — new facts, linked issues, or decisions may have changed its goal, answered it, or made it moot.

## The body format is not defined here

**Read `~/.claude/skills/reference/issue-format.md` in full before composing a single line of a refined body.** It is the single source of truth for the section template, the bar an acceptance criterion must clear, the evidence table, how blockers and critical path are expressed, and the `gh` commands that set native relationships. This skill governs *how you arrive at* the content; that file governs *what the content looks like*. Writing a body from memory of the format is how issues drift out of sync with it.

## Refinement principles

### Clarify the problem before the solution

Extract the real user, problem, outcome, and value.

Where the work has direct user or product value, write `As a <user>, I want <capability> so that <benefit>` rather than a technical task statement. Where the underlying outcome is reliability, maintainability, security, or operations, state *that* outcome — "replace X with Y" dressed as a user story hides which of them the issue is actually for.

Preserve the technical constraints, ADR decisions, compatibility requirements, and security requirements already recorded. Invent none.

### Ground the context in what you verified

When the issue makes a claim about current behaviour, check it against the source, tests, or history before recording it as fact. What you measured goes in `## Context` with the file, command, or commit you checked; a claim you could not verify is labelled there as unverified.

`## Context` is the section a reader lands on weeks later with none of today's conversation available. Write it for that reader.

### Make scope explicit

State what is included, and what is deliberately excluded when something plausibly creeps in. A strong issue leaves the implementer knowing where to stop.

### Write acceptance criteria a second person can check

Each criterion names a concrete artifact — a file, command, sheet, column, value, exit code, rendered string — and states an outcome someone other than the author can observe. The bar and its worked examples live in `issue-format.md`; apply them to every criterion before filing.

Cover the success paths and the edge or error cases that change the outcome. Where the only check is manual, say what the person runs and what they should see.

The acceptance criteria carry the whole verification burden. Nothing backs them up, so anything that must be true at the end is a criterion or is untracked.

### Right-size against INVEST

Aim for roughly **2 days of work or less** where practical, and check the item is **I**ndependent where practical, **N**egotiable in implementation, **V**aluable, **E**stimable, **S**mall, **T**estable.

When it fails the size test, recommend a split by user-observable outcome rather than by technical layer — a coherent vertical slice stays one ticket even when it touches frontend, backend, and database.

### Preserve uncertainty

Label what you do not know instead of filling it in:

- **Open question** — a decision still owed, which does not block starting. Reach for these; an issue with none usually has unknowns nobody examined.
- **Assumption** — believed true, unverified, surfaced so a wrong one fails early.
- **Out of scope** — deliberately excluded, with where that work goes instead.

A blocker means the work cannot meaningfully start without it. Everything else is a reference.

### Settle the publication metadata

Before publishing or updating, determine:

- the target milestone — existing, new, or none, each considered explicitly;
- the tracking repository and issue, and the implementation repository when it differs;
- workflow readiness: `ready-for-human`, `ready-for-agent`, or `agent/blocked`;
- the domain and team labels already on the issue, which stay;
- native blocking and sub-issue relationships;
- duplicate or overlapping existing issues.

Use the repository's existing canonical labels; `ready-for-agent` and `ready-for-human` are adopted as found, never created or renamed here. Where `agent/blocked` is absent, use the repository's canonical blocked equivalent. Human-owned research, decisions, and external actions are `ready-for-human`; an implementation issue with a critical human decision still open is `ready-for-human` or `agent/blocked`.

Re-derive the readiness label from the body you just wrote, and set it explicitly even when it lands on the value it already had. The label the issue arrived with describes the issue as it arrived; refinement is what changes whether work can start, and splitting a blocked issue to free its buildable half is exactly the case where the old label survives and silently discards the gain. `agent/blocked` earns its place only where `## Context` names a live blocking condition. The frontier query reads the label, not the prose.

## Process

### 1. Read the issue in full

Body, comments, linked references, and the surrounding project context. Refining from the title alone is the common failure.

For a batch, or a tangled dependency web, delegate per-issue diagnosis and milestone analysis to subagents; you reconcile the findings and own synthesis, approval, and publication.

### 2. Diagnose before rewriting

Summarize the current problems briefly, reporting only the categories that bite: clarity, scope, acceptance-criteria gaps, dependencies and unknowns, sizing.

### 3. Challenge the content

Question the issue as a sceptical Product Owner would, using the tracker's current state and the evidence gathered in step 1 — not the issue's own framing. Answer each:

- **Goal** — does the outcome still matter, given what has happened since the issue was written?
- **Route** — is there a simpler or different way to the same outcome, or does the stated plan treat a symptom of a deeper problem?
- **Overlap** — does another open or closed issue already cover it, answer it, or make it moot? Cite the issue.
- **Priority** — do its Importance and Urgency (or the repo's equivalent) still fit, given its real deadline and what it blocks?

Give each a verdict — **holds**, **overturned** (with the evidence and a proposed replacement), or **open** (a question only the user can settle) — and state every verdict, including the ones that hold.

The combined result picks the path onward: **rewrite** (continue to step 4), **merge** into another issue, **close** as moot or not worth doing, or **reprioritise**. Every overturned verdict is a proposal the user approves in step 6; the challenge informs the rewrite, and the user decides.

Done when all four questions carry a verdict backed by something checked in this pass, and the path onward is named.

### 4. Rewrite into the issue format

On the **rewrite** path, follow `~/.claude/skills/reference/issue-format.md`. Carry forward the intent that survived the challenge, plus the decisions, constraints, and useful evidence; preserve no prose merely because it was there.

For a proposed split, produce each resulting issue separately and state which blocks which. Check existing issues for duplicates before proposing a new one.

### 5. Run the Definition of Ready check

An issue is **Ready** when:

- [ ] All four challenge questions carry a stated verdict, and the issue's goal is one that held or was replaced with the user's approval.
- [ ] The desired outcome and its value are clear.
- [ ] Scope and important exclusions are clear.
- [ ] Every acceptance criterion names a concrete artifact and an outcome checkable without asking the author.
- [ ] The criteria cover the edge and error cases that matter.
- [ ] Real blockers are separated from references, and each is expressed as a native relationship.
- [ ] The work is right-sized, or explicitly marked as needing decomposition.
- [ ] No unresolved question is critical to starting implementation.
- [ ] The milestone is settled, with existing, new, and none all considered.
- [ ] The workflow readiness label was re-derived from the finished body, not inherited.
- [ ] The duplicate check was run.

Report **Not ready** with the remaining gap whenever a critical ambiguity survives.

### 6. Present for approval

Show:

1. **Diagnosis** — what was wrong with the original.
2. **Challenge** — the four verdicts with their evidence, and the path onward.
3. **Refined issue** — the complete replacement text, or on the merge/close/reprioritise path, the exact change proposed.
4. **Open questions and assumptions** — the ones that matter.
5. **Ready status** — Ready or Not ready with the gap, plus what the duplicate check found for each issue, or that none was run.
6. **Publication metadata** — milestone, labels, native relationships, external dependencies, references.

Ask for approval before modifying or publishing, unless the surrounding workflow authorizes direct edits. Keep a proposal visibly distinct from a published issue.

### 7. Publish, then wire

Where the refinement is a proposal — a review, a dry run, a body the user asked to see — the work ends at approval. Report the body and stop.

Otherwise publish and wire the relationships per `~/.claude/skills/reference/issue-format.md`, apply the approved milestone and labels, and report the number and URL of every issue created, updated, merged, or closed.

Where multiple issues are touched in one pass, re-read each one's live relationships and labels immediately before wiring — never carry forward what an earlier step in this same pass observed. An edge or a label can go stale between two issues in one session as easily as between two days; the tracker's current state is the only source, never a note taken earlier in the conversation. Where the repo has a milestone-drift check (see `issue-format.md`), run it after publishing and report what it finds.

## Guardrails

- A vague requirement earns an open question; acceptance criteria are only written where the outcome is actually known.
- An implementation preference stays a suggestion. Only a required outcome becomes a criterion.
- Detail earns its place by removing ambiguity.

A refined issue is understandable by someone who did not attend the original conversation.
