---
name: support
description: Answer an incoming support question — decide if it needs investigation, answer for both a technical and a lay audience, and decide whether it leaves a trace.
disable-model-invocation: true
argument-hint: "The question you were asked"
---

# Support

Someone asked us something as technical support. Start by reading our  [Context](file:///C:/Users/Z768180/Documents/Code/global_workspace/Nexus/CONTEXT.md) in full. 

This skill answers the question.
It does not triage a backlog (`/triage`) and does not drive a fix to completion
(`/tdd`, `/implement`).

## Step 0 — Sharpen before you dig
Optional if the question is vague use `/grilling`.

## Step 1 — Decide: answerable now, or investigate?

You can answer **now** if you can state the cause and your confidence in it without opening any
code — memory, a doc you already know covers it. Otherwise, investigate first.

### Investigating

Resolve which repo the question concerns before touching the filesystem: cross-reference
[Context](file:///C:/Users/Z768180/Documents/Code/global_workspace/Nexus/CONTEXT.md)'s
Components section (which repos make up the relevant service) against the repository table in
the global [AGENTS.md](file:///C:/Users/Z768180/Documents/Code/global_workspace/AGENTS.md)
("Current projects and repositories") for the actual local path. That mapping already exists —
don't glob or search `global_workspace` for a name.

Read-only digging (grep, read source) then happens **inline**, by absolute path into that repo —
no need to switch sessions for read-only work. Reach for `/handoff` into a real session in that
repo only when investigation needs to **execute** something (a repro script, a test suite) that
depends on being rooted there.

When you dig, borrow `/diagnosing-bugs` **Phases 1–3 only** — build a feedback signal, confirm
the reproduction, form **3–5 ranked, falsifiable hypotheses**, per that skill's own rule against
anchoring on the first plausible one. That rule matters more here than in a normal bug hunt: a
support question's wording rarely pins down which of several code paths the asker actually
exercised. If it names a sheet, an entity type, or a config ambiguously, each plausible one is
its own hypothesis to investigate — not a detail to assume away because the first path you
checked panned out. Stop at the ranked list: this skill root-causes enough to answer and to
write a credible issue, it does not fix. A fix (Phases 4–6, or a full `/implement`/`/tdd` run) is
separate work, and per
`file:///C:/Users/Z768180/Documents/Code/global_workspace/Nexus/docs/adr/0002-ownership-decides-the-home-repo.md`
may not even be yours to do.

**Completion criterion**: you can state the root cause (or your ranked hypotheses) and the
evidence for each — and every piece of that evidence (a log line, an error message, a specific
check) has been traced through the actual call path that would produce it, not cited because it
merely sounds relevant nearby.

## Step 2 — Answer

Always produce both, clearly separated:

- **Technical explanation** — root cause, evidence, what you found. Your own record, and becomes
  the issue body if Step 3 files one.
- **Plain-language reply** — short, ready to paste to the asker. Name the concrete specifics
  they'll recognize — the sheet, column, file, or log line involved — that's what lets them
  self-diagnose; don't flatten it into vague reassurance. If investigation left more than one
  live hypothesis, give the reply as branches ("if you did X, that's the cause; if you did Y,
  check Z") rather than picking one to sound certain. Stop short of implementation internals
  (source code, stack traces, algorithms) they have no reason to see.

Skip the plain-language half only when told the asker is technical themself.

## Step 3 — Decide whether this leaves a trace

Follow ADR-0002's routing — this skill applies the existing rule, it doesn't add a new one:

- **Real bug, needs a code fix** → file the issue directly in the code's home repo (admin'd or
  push-only both qualify per ADR-0002 — that's where the code and collaborators are).
- **Nexus gets a stub** only if a Jeroen-side follow-up action remains after filing (waiting on
  review, re-test once merged) — never by default, and never as a duplicate of the repo issue.
- **Expected behavior, no bug** → answer only. Nothing filed.
- **Recurring question, hints at a docs gap** → flag it as a possible `bp-docs` item in your
  reply; filing it is a separate decision, not this skill's.

No blanket record-keeping — a trace is filed because something still needs chasing, not to log
that a question was answered.
