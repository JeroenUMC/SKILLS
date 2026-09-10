---
name: questionnaire
description: Turn an ask for a domain expert into closed questions with a private answer key, then read the replies back against it.
disable-model-invocation: false
---

A question whose answers you cannot enumerate is a question you are not ready to ask. Asking it
anyway spends an expert's goodwill and returns prose you still have to interpret.

This skill produces two artifacts from one ask: the **questionnaire** the expert answers, and the
**answer key** that stays with you — one row per option, naming what that option changes on your
side. The key is the real work. Writing it is what turns "what do you think about X?" into three
options and a decision. An option with no row means you do not yet know why you are asking.

## Drafting

**1. Name the decision.** One decision per question. If you cannot say what you would do differently
under two of its answers, the question is not ready — cut it, or dig until you can.
**Done when** every question names one decision and none is asked out of curiosity.

**2. Enumerate the options.** Close every question on a fixed set the expert picks from. Each option
must be something you could actually record, and every set carries an **escape hatch** as a named
option: *"I don't recognise this"*, *"it has no other name"*, *"we don't distinguish them"*. A hatch
you don't offer comes back as a guess, and once written down a guess is indistinguishable from
knowledge.
**Done when** every question has an option set and every set has its hatch.

**3. Write the answer key.** One row per option, saying what changes if they pick it. The key proves
the option set: two options mapping to the same action mean you are asking for a distinction you
will not use — merge them.
**Done when** every option of every question has a row.

**4. Strip the loading.** Keep the question and its options. Cut your volume counts, your stakes,
your reasoning, and every hint of which answer you hope for. Rank importance in the *order* of the
questions; keep the ranking out of their text.
**Done when** each question reads as though any of its options would suit you equally.

> **Loaded:** Are these sections routinely H&E stained? If so, 1,145 slides finally get a stain
> instead of an empty field — by far the biggest win still on the table.
>
> **Closed:** Are `Dsn`, `Dsn/Mega` and `Dsn/OK` routinely H&E stained?
> ☐ yes, all three ☐ yes, except `Dsn/OK` ☐ no ☐ depends / other: ______

**5. Make the thing recognisable.** Quote the value exactly as it reaches you, and say where it
comes from — which system, which field, what it sits next to. An expert who cannot place the thing
answers nothing, and that reads identically to a question they declined.
**Done when** every question is answerable from what the expert knows, with no knowledge of your
system.

**6. Render it before you send it.** A questionnaire is a form, and a form only works in the format
it is read in — pasted into the mail, printed, exported. Markdown is the source; look at the output.
Two collapses are routine and both dissolve the form: consecutive lines merge into one paragraph, so
an option set arrives as a run-on sentence; and paired underscores are emphasis syntax, so the blank
someone was meant to write in disappears silently. Put each option on its own list line, and give
every fill-in a blank that is inert in the target format.
**Done when** you have looked at the rendered questionnaire and every option stands on its own line
with its blank visible.

## The pre-filled list

**A pre-filled list comes back approved, not reviewed.** If volume forces you to pre-fill, ask them
to mark what is *wrong* rather than confirm what is right, hold the list to what one person reads in
one sitting, and record the outcome in the key as approved in bulk — never as confirmed per item.
Bulk approval of cells you sent *blank* fills nothing at all.

## Reading the answers back

Match every reply to an option in the key. A reply matching none is a **non-answer**: record it
still open, in the expert's own words, and leave it unrounded toward the nearest option. The
recurring shapes:

- bulk approval of a list that went out blank — approves nothing, fills nothing
- a yes with a hedge (*"yes, but check with X"*) — a follow-up, not an answer
- the value's name restated in other words
- *"no idea what this is"* — a real answer about whether a **value** exists (probably obsolete or
  mistyped), and a non-answer to anything about how it was produced

Record the respondent's name and the date beside the answers; without them a round is
unattributable the moment anyone's memory fades. An answer that opens a fresh question belongs to
the next round, not to this one.

## Output

One file: the questionnaire above a horizontal rule, the answer key below it. The rule is the
copy-paste boundary — everything above it goes to the expert, nothing below it does.
