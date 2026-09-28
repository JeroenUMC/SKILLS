---
name: issue-pdf
description: Render a GitHub issue to PDF (GitHub's Markdown rendering, printed by Edge); optional comments appendix.
disable-model-invocation: true
---

Run once:

```
python ~/.claude/skills/issue-pdf/issue_pdf.py <issue URL | owner/repo#N> [--comments] [-o OUT.pdf]
```

`--comments` puts all comments in one appendix.

`-o`: the user's location if they name one. Otherwise, if an `issue-to-pdf/` folder exists in the current directory, pass `-o issue-to-pdf/<repo>-<N>.pdf`. If it doesn't exist, ask with AskUserQuestion: "Create `issue-to-pdf/`" (pass `-o issue-to-pdf/<repo>-<N>.pdf`; the script creates the folder) or "Save in root" (omit `-o`; the script writes `<repo>-<N>.pdf` in the current directory).

**Done** when the script prints a PDF path: report it as a link. On a non-zero exit, relay its `issue_pdf:` error and stop.
