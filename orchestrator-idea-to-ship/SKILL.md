---
name: orchestrator-idea-to-ship
description: Turn a codebase idea into an approved spec, executable tickets, and implementation handoff.
disable-model-invocation: true
argument-hint: "The idea or outcome to develop"
---

# Idea To Ship Orchestrator

Use this workflow when the user has an idea that needs deliberate shaping before implementation.
It coordinates the thinking and planning skills; it does not silently implement unresolved product
decisions.

## Preconditions

- Read the repository instructions and existing domain context before proposing durable changes.
- Use `/setup-skills` when the repository's issue-tracker, triage-label, or domain-doc configuration
  is missing.
- Confirm whether the work belongs in the current repository before publishing anything.

## Sequence

1. **Sharpen:** invoke `/grill-with-docs` for a codebase-bound idea. Use `/grill-me` only when no
   repository exists. Preserve decisions in the repository's documented context and ADRs where
   those skills require it.
2. **Prototype when needed:** if a question cannot be settled reliably in prose, use `/handoff`
   to branch into `/prototype`, then hand the result back before writing the spec.
3. **Specify:** once the idea and decisions are coherent, invoke `/to-spec` to produce the approved
   buildable specification.
4. **Decompose:** invoke `/to-tickets` and present the ticket breakdown, acceptance criteria, and
   blocking edges for approval.
5. **Hand off:** after approval, report the executable frontier and direct the user to
   `/orchestrator-implement-issue` for each ticket, clearing context between tickets. For a large
   dependency graph, direct the user to `/orchestrator-implement-milestone` instead.

## Pauses

Pause for unresolved product decisions, unclear repository ownership, missing tracker configuration,
or a ticket breakdown the user has not approved. Do not publish duplicate issues or begin code
changes from an unapproved plan.

## Completion

The workflow is complete when the idea has a durable, approved spec and an approved set of executable
tickets with dependencies, or when a precise blocker and next decision are reported.
