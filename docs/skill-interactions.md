# Skill Interactions

Inventory: 28 skills. Relationships: 22 reviewed edges.

Direct edges are explicit invocations, delegation, handoffs, or documented uses. Indirect edges are reviewed composition hypotheses and are intentionally weaker.

## Direct Relationships

| Source | Relationship | Target | Basis |
| --- | --- | --- | --- |
| `skill-router` | routes-to | `orchestrator-idea-to-ship` | main flow |
| `skill-router` | routes-to | `orchestrator-implement-issue` | single issue implementation |
| `skill-router` | routes-to | `orchestrator-implement-milestone` | milestone implementation |
| `orchestrator-idea-to-ship` | invokes | `grill-with-docs` | step 1 |
| `orchestrator-idea-to-ship` | branches-to | `prototype` | step 2 |
| `orchestrator-idea-to-ship` | bridges | `handoff` | step 2 |
| `orchestrator-idea-to-ship` | invokes | `to-spec` | step 3 |
| `orchestrator-idea-to-ship` | invokes | `to-tickets` | step 4 |
| `orchestrator-idea-to-ship` | hands-off-to | `orchestrator-implement-issue` | step 5 |
| `orchestrator-implement-milestone` | delegates-to | `orchestrator-implement-issue` | delegated issue execution |
| `orchestrator-implement-issue` | uses | `tdd` | implementation sequence |
| `orchestrator-implement-issue` | uses | `code-review` | review sequence |
| `grill-with-docs` | uses | `domain-modeling` | documented skill contract |
| `grill-me` | uses | `grilling` | documented skill contract |
| `grill-with-docs` | uses | `grilling` | documented skill contract |
| `diagnosing-bugs` | hands-off-to | `improve-codebase-architecture` | post-mortem path |
| `to-tickets` | hands-off-to | `orchestrator-implement-issue` | frontier execution |

## Indirect Relationships

| Source | Relationship | Target | Basis |
| --- | --- | --- | --- |
| `wayfinder` | composes-well | `research` | decision investigation |
| `wayfinder` | composes-well | `orchestrator-idea-to-ship` | wayfinder completion handoff |
| `triage` | composes-well | `refine` | agent-ready issue path |
| `refine` | composes-well | `orchestrator-implement-issue` | refined issue becomes executable |
| `orchestrator-implement-issue` | composes-well | `finalize` | session closeout |

## Refresh

Run `python scripts/build-skill-interactions.py --write` after changing skills or graph data.
Use `--check` in CI to fail when committed HTML or Markdown differs from the source graph.

## Limitations

The graph records documented relationships, not runtime telemetry. Indirect edges are hypotheses supported by the stated basis and should be reviewed when workflows change.
