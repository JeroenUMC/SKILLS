"""Render a GitHub issue to PDF: GitHub's own Markdown API for HTML, Edge headless for print.

Usage: python issue_pdf.py <issue-url | owner/repo#N> [--comments] [-o OUT.pdf]
Needs only `gh` (authenticated) and Microsoft Edge; stdlib Python.
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: A4; margin: 15mm 12mm; }
body { font: 10pt/1.45 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1f2328; }
header.meta { border-bottom: 2px solid #d0d7de; margin-bottom: 1em; padding-bottom: .5em; }
header.meta h1 { font-size: 18pt; margin: 0 0 .3em; }
header.meta .sub { color: #59636e; font-size: 9pt; }
.label { display: inline-block; border: 1px solid #d0d7de; border-radius: 1em; padding: 0 .6em; margin: .2em .2em 0 0; font-size: 8pt; }
h2 { border-bottom: 1px solid #d0d7de; padding-bottom: .2em; }
table { border-collapse: collapse; width: 100%; font-size: 8pt; margin: .6em 0; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #d0d7de; padding: 3px 5px; vertical-align: top; overflow-wrap: anywhere; }
th { background: #f6f8fa; }
code { font: 8.5pt Consolas, monospace; background: #f6f8fa; padding: 0 .2em; border-radius: 3px; }
pre { background: #f6f8fa; padding: 8px; border-radius: 4px; white-space: pre-wrap; overflow-wrap: anywhere; }
pre code { padding: 0; }
img { max-width: 100%; }
blockquote { color: #59636e; border-left: 3px solid #d0d7de; margin-left: 0; padding-left: 1em; }
summary { font-weight: 600; }
.appendix { page-break-before: always; }
.comment-head { background: #f6f8fa; border: 1px solid #d0d7de; padding: 4px 8px; margin-top: 1.5em; font-size: 9pt; }
"""


def die(msg):
    print(f"issue_pdf: {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd, stdin=None):
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        die(f"`{' '.join(cmd[:3])} ...` failed:\n{p.stderr.strip()}")
    return p.stdout


def parse_ref(ref):
    m = re.fullmatch(r"https://github\.com/([^/]+/[^/]+)/issues/(\d+)\S*", ref) or re.fullmatch(
        r"([^/\s]+/[^/#\s]+)#(\d+)", ref
    )
    if not m:
        die(f"cannot parse issue reference {ref!r}; use a URL or owner/repo#N")
    return m.group(1), int(m.group(2))


def gfm(text, repo):
    """GitHub's own renderer: same tables, task lists, #refs and line breaks as the web UI."""
    out = run(["gh", "api", "markdown", "--input", "-"], json.dumps({"text": text or "", "mode": "gfm", "context": repo}))
    return re.sub(r"<details(?![^>]*\bopen\b)", "<details open", out)  # print collapsed sections expanded


def day(ts):
    return ts.replace("T", " ")[:16]


def build_html(issue, repo, with_comments):
    e = html.escape
    labels = "".join(f'<span class="label">{e(l["name"])}</span>' for l in issue["labels"])
    parts = [
        f"<!doctype html><html><head><meta charset='utf-8'><title>{e(repo)}#{issue['number']}</title><style>{CSS}</style></head><body>",
        f'<header class="meta"><h1>{e(issue["title"])} <span style="color:#59636e;font-weight:400">#{issue["number"]}</span></h1>',
        f'<div class="sub">{e(repo)} · {issue["state"]} · opened by @{e(issue["author"]["login"])} on {day(issue["createdAt"])}'
        f' · <a href="{e(issue["url"])}">{e(issue["url"])}</a></div><div>{labels}</div></header>',
        gfm(issue["body"], repo),
    ]
    if with_comments:
        parts.append(f'<section class="appendix"><h1>Appendix: Comments ({len(issue["comments"])})</h1>')
        for c in issue["comments"] or []:
            who = c["author"]["login"] if c.get("author") else "ghost"
            parts.append(f'<div class="comment-head"><b>@{e(who)}</b> · {day(c["createdAt"])}</div>')
            parts.append(gfm(c["body"], repo))
        if not issue["comments"]:
            parts.append("<p><i>No comments.</i></p>")
        parts.append("</section>")
    parts.append("</body></html>")
    return "\n".join(parts)


def edge_path():
    for p in EDGE_CANDIDATES:
        if Path(p).exists():
            return p
    return shutil.which("msedge") or die("Microsoft Edge not found")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("issue", help="issue URL or owner/repo#N")
    ap.add_argument("--comments", action="store_true", help="append all comments as one appendix")
    ap.add_argument("-o", "--output", help="output PDF (default: <repo>-<N>.pdf in cwd)")
    a = ap.parse_args()

    repo, num = parse_ref(a.issue)
    fields = "number,title,url,state,author,createdAt,labels,body,comments"
    issue = json.loads(run(["gh", "issue", "view", str(num), "-R", repo, "--json", fields]))
    out = Path(a.output or f"{repo.split('/')[1]}-{num}.pdf").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "issue.html"
        page.write_text(build_html(issue, repo, a.comments), encoding="utf-8")
        run([
            edge_path(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={Path(tmp) / 'profile'}", f"--print-to-pdf={out}", page.as_uri(),
        ])
    if not out.exists() or out.stat().st_size == 0:
        die(f"Edge produced no PDF at {out}")
    print(out)


if __name__ == "__main__":
    main()
