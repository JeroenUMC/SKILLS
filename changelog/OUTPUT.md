# Changelog HTML — output spec

Fill [`assets/changelog-template.html`](assets/changelog-template.html) — it already
carries the exact Tailwind classes, structure, and section order. Your job is to
swap `{{PLACEHOLDERS}}` for real content and repeat the marked blocks. This file is
the single source of truth for **which sections exist, what each holds, and the
badge palette**; the template is the markup those rules produce.

Self-contained single HTML file. One CDN script (Tailwind). Light editorial
stone/slate palette, one indigo accent, generous whitespace, serif headings
(`font-serif`), badges as below. It must open standalone in a browser.

**Mermaid** is used for exactly one diagram — the "Where the changes land" journey
flow (section 3). The template already imports the Mermaid ESM module; keep the
file self-contained. Add no other diagrams.

## Sections — keep these, in this order

1. **Header** — title; chips (repo(s), `merged SINCE → UNTIL`, `source: merged
   GitHub PRs`); a one-paragraph framing (functional, user-facing lens); and the
   **badge legend**. The legend stays — trim it to the badge types you actually use.
2. **At a glance** — stat cards. Adapt to the real data: PRs merged, changes to
   know, action items, and any notable extra (DB migrations, a repo with zero
   merges). Drop or add cards to fit; do not invent counts to fill five slots.
3. **Where the changes land** — a left-to-right **Mermaid** flow of the repo's user
   workflow (its stages), with the stages touched this window coloured: `:::new`
   emerald for something new, `:::changed` indigo for a change to an existing step.
   Intro line, verbatim: "Highlighted changes affect the following parts, showing
   new (in green) and changes (in indigo)." Cut only if the repo has no meaningful
   staged workflow to draw.
4. **The N changes worth knowing** — the card grid; one `<article>` per functional
   change. Each card: category badge(s), a short plain title, one plain-language
   impact sentence, an optional colour-matched action line, and the linked PR
   (`repo #num · merged YYYY-MM-DD`). The right-aligned **area chip is optional** —
   a generic label or omit it.
5. **Action checklist** — clickable `<input type=checkbox>` items, each tagged
   Required / If needed / Good to know and linking its PR. **Human-confirmed items
   only** (see SKILL.md). If none are confirmed, **omit this whole section**.
6. **By repository** — one bar per merged PR (indigo-500 user-facing · stone-300
   internal), then a collapsed `<details>` itemising and linking every merged PR.
   No explanatory legend line above the bars.
7. **Footer** — generated date, window, source; optional pointer to a prose
   companion file if you wrote one.

## Omit these — the human cut them

- The **legend line** above the By-repository bars ("Each bar is one merged PR…").
- The **"Notes & caveats"** section.

## Badge palette (single source of truth)

Category badges (pill, in cards and the legend):

| Badge          | Classes                                  |
|----------------|------------------------------------------|
| New / feature  | `bg-emerald-100 text-emerald-800`        |
| Bug fix        | `bg-sky-100 text-sky-800`                |
| Removed        | `bg-rose-100 text-rose-800`              |
| DB migration   | `bg-violet-100 text-violet-800`          |
| ⚠ Action needed| `bg-amber-100 text-amber-800`            |
| Docs           | `bg-slate-200 text-slate-700`            |
| CI / deps      | `bg-stone-200 text-stone-600`            |

- **Card left rule** tracks the primary badge: `border-emerald-400` (new),
  `border-sky-400` (fix), `border-rose-400` (removed), `border-slate-300` (docs/internal).
- **Action severity label**: Required → `text-rose-700`; If needed / Good to know → `text-slate-500`.
- **Repo bars**: `bg-indigo-500` user-facing · `bg-stone-300` internal.

## The lens

Write every card from the repo **user's** point of view — what they run,
configure, or get as output. A change is **functional** (earns a card) when a user
would notice it; **internal** (bars/detail only, never a card) when it is a
refactor, CI change, or dependency bump. The `hint_internal` flag in the collected
JSON is a starting guess, not the verdict — you decide.

## Where to write it

Save into the repo's existing reports/changelog folder if one exists (match the
convention); otherwise `docs/reports/`. Name it
`YYYY-MM-DD-<repo>-changelog-<window>.html`. Tell the user the absolute path and
offer to open it (`start` on Windows, `open` on macOS, `xdg-open` on Linux).
