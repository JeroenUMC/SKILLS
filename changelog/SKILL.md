---
name: changelog
description: Generate a visual, self-contained HTML changelog for a GitHub repo (and optional submodules) over a time window, written from the repo user's perspective and sourced from merged PRs.
disable-model-invocation: true
---

Build a visual HTML changelog for a GitHub repo over a time window, written from
the **user's** point of view — what they run, configure, or get as output. Data
comes strictly from **merged GitHub PRs** via the `gh` CLI; every claim in the
output links the PR behind it. Internal refactors, CI, and dependency bumps are
noted but de-emphasised.

The load-bearing judgement is **functional vs internal** — a change earns a card
only if a repo user would notice it. And you never decide an action is *required*
by reading code; you derive **candidates** and have the human **confirm** them.

Scripts live in this skill's `scripts/` folder; run them with `python`. The output
spec and the fillable scaffold are [`OUTPUT.md`](OUTPUT.md) and
[`assets/changelog-template.html`](assets/changelog-template.html).

## 1 · Target repo

Settle on `owner/name`. If the user gave it, use it. Otherwise infer from the
current repo (`git remote get-url origin`) and **confirm with the user**
(AskUserQuestion) before proceeding — never guess silently.

Done when: you have a confirmed `owner/name`.

## 2 · Submodules

Default is **the main repo only**. Run `python scripts/list_submodules.py
--repo-path <repo>`; if it returns any GitHub submodules, ask the user
(AskUserQuestion) whether to include them, and which. Only add submodule repos the
user opts into.

Done when: the final repo list is fixed.

## 3 · Resolve the window

Turn the user's window into concrete dates with `python scripts/resolve_window.py`.
It accepts natural language (`--window "last two weeks"`, a year `"2026"`, a range
`"from A to B"`), a **release** (`--release TAG --repo owner/name`, resolved to the
span between the previous release and this one), or explicit `--since/--until`. It
prints `since`, `until`, and a ready `qualifier` string. If it can't parse a spec,
compute the dates yourself and pass `--since/--until`.

Done when: you have concrete `since` and `until` dates.

## 4 · Collect the PRs

Run `python scripts/collect_prs.py --repo <a> [--repo <b> ...] --since <A> --until
<B> --out <tmp.json>`. It verifies `gh` auth, searches merged PRs per repo, and
emits consolidated JSON (number, title, url, mergedAt, author, labels, body, plus
`thin` and `hint_internal` flags).

**Trust nothing silently.** Any repo that failed lands in `errors` with its count
as `null` (never `0`); any repo that hit `--limit` lands in `warnings`; and the
script **exits non-zero** if either list is non-empty. A repo showing `0` merged is
only believable when it is absent from both `errors` and `warnings` — otherwise
re-check it directly (`gh pr list --repo <r> --search "<qualifier>" --state merged`)
before concluding nothing changed there. On truncation, re-run with a higher
`--limit` or a narrower window. Surface every error and warning to the user.

For every PR flagged `thin` that might be functional, run `gh pr view <n> --repo
<r> --json title,body,files,commits` and read the changed files to judge its
impact — a one-line PR body is not enough to write a card from.

Done when: every merged PR has a **functional-or-internal** call, every functional
one has a plain-language user-facing impact sentence, and `errors`/`warnings` are
empty or explicitly resolved.

## 5 · Derive candidate actions, then confirm with the human

Some functional changes imply the user must *do* something (re-pull an image,
migrate config, change a command). These are **candidates** — do **not** promote
them to the checklist by reading code, which is error-prone. (A change may be
required for some users and irrelevant to others — e.g. "rebuild the model from the
website" doesn't apply to a user who already has one.)

For each candidate, ask the human (AskUserQuestion) which severity it truly is:
**Required**, **If needed**, **Good to know**, or **drop**. Offer, per uncertain
candidate, to spawn a background **`/research` subagent** (the `research` skill) to
investigate it against the repo rather than answering from memory.

Only confirmed items reach the Action checklist. If none survive, that section is
omitted entirely.

Done when: every candidate is resolved to a confirmed severity or dropped.

## 6 · Write the HTML

Fill `assets/changelog-template.html` following [`OUTPUT.md`](OUTPUT.md) — keep
sections 1–7 (including the section-3 "Where the changes land" journey diagram),
honour the badge palette, and confirm the cut bits (by-repo legend line, Notes &
caveats) are absent. Write one card per functional change, the confirmed checklist
(or none), and the per-repo bars + collapsed full detail. Save it per OUTPUT.md's
location rule, tell the user the absolute path, and offer to open it.

Done when: a self-contained HTML file exists with every kept section, no omitted
section, and every claim linking its PR.
