# Skill Interactions

Inventory: 28 skills. Relationships: 23 declared edges.

Directional edges describe workflow or dependency direction. Non-directional edges describe compatible skills or supporting vocabulary and do not imply sequence.

## Directional Relationships

| Source | Relationship | Target |
| --- | --- | --- |
| `skill-router` | invokes | `orchestrator-idea-to-ship` |
| `skill-router` | invokes | `orchestrator-implement-issue` |
| `skill-router` | invokes | `orchestrator-implement-milestone` |
| `orchestrator-implement-issue` | uses | `tdd` |
| `orchestrator-implement-issue` | uses | `code-review` |
| `orchestrator-implement-milestone` | delegates | `orchestrator-implement-issue` |
| `orchestrator-idea-to-ship` | invokes | `grill-with-docs` |
| `orchestrator-idea-to-ship` | invokes | `to-spec` |
| `orchestrator-idea-to-ship` | invokes | `to-tickets` |
| `orchestrator-idea-to-ship` | uses | `prototype` |
| `orchestrator-idea-to-ship` | uses | `handoff` |
| `orchestrator-idea-to-ship` | hands-off-to | `orchestrator-implement-issue` |
| `diagnosing-bugs` | hands-off-to | `improve-codebase-architecture` |
| `grill-me` | invokes | `grilling` |
| `grill-with-docs` | invokes | `grilling` |
| `grill-with-docs` | uses | `domain-modeling` |
| `refine` | hands-off-to | `orchestrator-implement-issue` |
| `to-tickets` | hands-off-to | `orchestrator-implement-issue` |
| `triage` | hands-off-to | `refine` |
| `wayfinder` | uses | `research` |
| `wayfinder` | hands-off-to | `orchestrator-idea-to-ship` |
| `finalize` | invokes | `skill-audit` |

## Non-Directional Relationships

| Source | Relationship | Target |
| --- | --- | --- |
| `orchestrator-implement-issue` | optional-companion | `finalize` |

## Refresh

Run `python scripts/build-skill-interactions.py --write` after changing skill frontmatter or graph/skills.json.
Use `--check` in CI to fail when committed HTML or Markdown differs from the source.

## Limitations

Relationships are declared in skill frontmatter, not inferred from prose. Directional edges are not a complete ordering: `uses` means dependency or consultation, while `invokes`, `delegates`, and `hands-off-to` represent control transfer.
