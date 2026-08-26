# Issue tracker: Local Markdown

Issues and specs (you may know a spec as a PRD) for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

This file is the **mechanics** sheet: where files live and what each one is called. The **shape of an
issue body** — its sections and what makes an acceptance criterion checkable — lives in
`~/.claude/skills/reference/issue-format.md`; read it before composing a file. Its
`gh api` relationship commands do not apply here.

**Dependencies are not embedded.** A local markdown tracker has no native relationship store, and a
prose dependency line drifts out of date the moment a ticket closes. So write the issue file clean
and **report the dependency to the terminal** instead:

```
Wrote .scratch/upload-v2/issues/04-map-specimen-types.md
Dependency not recorded: 04 depends on 02 — this tracker has no relationship store.
Work 02 first.
```

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: not recorded in the file. Tickets are numbered in dependency order (blockers first), so map order carries the sequence; where a real gate exists, print it to the terminal as above rather than embedding it.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open and unclaimed; first by number wins, since numbering already runs blockers-first.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
