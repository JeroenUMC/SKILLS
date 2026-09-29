---
name: explain
description: Brief me in plain English, as a non-technical stakeholder, on this session or on GitHub work (issues, sub-issues, milestones).
argument-hint: "Optional: #187 and its subissues | milestone #2 | #177, #178, #179 — or a focus for the session briefing"
disable-model-invocation: true
---

# Explain

Give a **status briefing** to a **sponsor**: someone smart and busy who is paying for this work but has never seen the code. They care about why the work exists, what it means, and what you need from them. How it works doesn't matter to them.

## Subject

The arguments decide what the briefing covers:

- **No arguments, or a plain-words focus** → the **session**: where this conversation stands. Lead with the focus if there is one.
- **Issue numbers, a milestone, or "and its subissues"** → **GitHub work** in the current repo (or `owner/repo#N` if given). Treat any wording like "their overarching goal" as the focus.

## Steps

1. **Gather.** 
   - *Session*: not applicable, only current context relevant.
   - *GitHub work*: read every item in scope with `gh`. That includes the title, body, state (and whether it was closed as completed or not planned), labels, comments, and linked PRs:
     - an issue: `gh issue view N --comments`
     - its sub-issues: `gh api repos/{owner}/{repo}/issues/N/sub_issues`, then view each one, going down every level
     - a milestone: `gh api repos/{owner}/{repo}/milestones/N`, then `gh issue list --milestone "<title>" --state all`, then view each issue

   Done when every item in scope has been read, not just listed.

2. **Take stock.** Sort what you found into piles:
   - **Goal**: why this work exists, as one outcome the sponsor would recognise. For a group of items, this is what they add up to. For the session, it's what the user asked for.
   - **Asks**: every open question, approval, or decision waiting on the user. For GitHub work, that means unanswered questions in comments, `needs-info` or `blocked` items, PRs waiting for review, and choices an issue leaves open.
   - **Done**: the outcomes reached so far. An issue closed as not planned counts as dropped, not done.
   - **Next**: what's still open, and what happens once the asks are answered.

   Done when every point that waits on the user sits in **Asks**. An empty pile is a valid result.

3. **Translate.** Put each item into everyday words. Describe what something does for the sponsor ("the upload now checks the files before sending them"), not what was touched ("edited validator.py"). Name things by their role, not by file, command, branch, label, or error message. Issue numbers may appear once, in brackets, as a reference. If a technical term is unavoidable, explain it in one short clause.

4. **Brief.** Reply in this shape and nothing else:

   **What this is about**: the Goal in one or two sentences. Only include this for GitHub work, or if the session's goal isn't obvious.

   **What I need from you**: each ask is a decision the sponsor can make. Give the question, the options in plain words, what each option means for them, and your recommendation. If there are no asks, write "Nothing right now."

   **Where things stand**: 3–5 bullets, biggest first. This is an overview, not an inventory: fold many small items into one outcome. For GitHub work, give a rough sense of progress (e.g. "about two-thirds done").

   **What happens next**: one or two sentences.

   **Heads-up**: only when there's a real risk, delay, or surprise, told in terms of its effect on the sponsor.

   Done when a reader with no technical background could answer every ask without having to ask what a word means.

Then stop and wait for the reply.
