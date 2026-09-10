# Paper trail — output spec

Two renderings of one audit: Markdown for the repo, HTML for the reader without
repo access. **Same content, same order, same verdict.** This file is the single
source of truth for which sections exist and what each holds;
[`assets/paper-trail-template.html`](assets/paper-trail-template.html) is the
markup those rules produce.

## The order is the argument

The reader is a skeptic with limited patience. They get the verdict and the case
against it **before** any account of the work. Never open with what was
accomplished — that is the shape of a document that is trying to convince, and it
reads as one.

1. **Header** — the set's title, and chips: repo(s), issue count, date range,
   `evidence: trail + artifacts @ <commit sha>`.
2. **The claim** — one falsifiable sentence, quoted where the trail states it,
   with its source linked. Sub-claims as a short list. Below it, verbatim, **the
   question** being answered and who asked it.
3. **Verdict** — one of *holds* / *holds narrowly* / *partly holds* /
   *unsupported*, with a one-paragraph reading. Then, immediately, **what would
   settle the rest**: the concrete check that would close any open part.
4. **The case against** — the strongest hostile reading, as numbered points, most
   damaging first. Every point links its issue, PR, or artifact. When the case is
   genuinely thin, say that and show what was hunted for (step 5's five
   categories) rather than padding it.
5. **What the artifacts show** — counts read from files, not from prose: rows,
   keys, exclusions, tests. Each with the file and commit it came from. This is
   the section that converts assertion into fact, so it carries the numbers the
   claim turns on.
6. **What was excluded, and why** — every deliberate omission with its stated
   reason and source. A skeptic's real question is usually about this section.
   Omit it only when the set excluded nothing, and say so explicitly.
7. **Criteria ledger** — every criterion, grouped by issue, each **met** /
   **met elsewhere** / **no evidence found** with its link or searched-where note.
   Long by nature: collapsed per issue in HTML, a plain table in Markdown.
8. **Blind spots** — what was not read and why: repos skipped, artifacts
   unavailable, checks not run. Never omitted; when there are none, print
   "None — every referenced repo and artifact was read."
9. **Footer** — generated date, selector used, commit audited, and the exact
   `collect_set.py` invocation, so the audit can be reproduced.

## Grade vocabulary — single source of truth

| Grade | Means | Badge |
|---|---|---|
| **met** | Evidence inside this set discharges it | `bg-emerald-100 text-emerald-800` |
| **met elsewhere** | Real evidence, from outside the set — say where | `bg-sky-100 text-sky-800` |
| **no evidence found** | Searched, came back empty — say where you looked | `bg-amber-100 text-amber-800` |

Verdict badges: *holds* `bg-emerald-100 text-emerald-800` · *holds narrowly*
`bg-sky-100 text-sky-800` · *partly holds* `bg-amber-100 text-amber-800` ·
*unsupported* `bg-rose-100 text-rose-800`.

**`no evidence found` is amber, never red.** It reports the state of the trail,
not a failure of the work — much real engineering is verified in ways that leave
no trace. Colouring it as a defect makes the document lie in the other direction.

## Tick state

Never rendered. Not as a count, not as a percentage, not as a caveat. It appears
in `collect_set.py` output for the record and stops there — a repo that closes
issues without ticking would otherwise show a fake completion rate, and the number
is memorable enough to survive any disclaimer printed next to it.

## Voice

Plain and specific. Prefer "873 rows across 91 keys, read from `mappers.xlsx` at
`a1b2c3d`" to "comprehensive coverage". Name people only as issue/PR authors,
never as the cause of a gap. Where the trail and an artifact disagree, print both
and say which you trust and why — that disagreement is the most valuable thing an
audit can find.

## HTML specifics

Self-contained single file, one CDN script (Tailwind). Light editorial stone/slate
palette, one indigo accent, serif headings (`font-serif`), generous whitespace,
badges per the table above. It must open standalone in a browser and read as one
page on a phone.

The criteria ledger is one collapsed `<details>` per issue, its summary line
carrying the issue number, title, and a compact grade tally
(`7 met · 1 elsewhere · 2 no evidence`). The page scans in thirty seconds closed,
and opens to the full evidence.

## Markdown specifics

Save to `docs/paper-trail/<slug>.md`, slug from the set title. Same nine sections
as `##` headings in the same order. The criteria ledger is one table per issue:
`| Criterion | Grade | Evidence |`. Link every issue and PR by URL — the file is
read on GitHub, where bare `#42` resolves to the wrong repo when the trail crosses
repos.
