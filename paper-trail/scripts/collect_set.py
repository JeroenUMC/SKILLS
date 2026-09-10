#!/usr/bin/env python3
"""Resolve a set of GitHub issues to the raw material of a paper trail.

One `gh` sweep instead of per-run improvisation: the selector is resolved to a
concrete issue list, every issue's linked PRs are pulled from its timeline, and
the trail is scanned for the two things the agent cannot cheaply find by eye —
**cross-repo references** and **artifact paths**.

Usage:
    python collect_set.py --repo owner/name --milestone "Staining vocabulary" --out t.json
    python collect_set.py --repo owner/name --milestone 2
    python collect_set.py --repo owner/name --label bug --state closed
    python collect_set.py --repo owner/name --issues 42,43,44
    python collect_set.py --repo owner/name --query "is:issue label:epic closed:>=2026-01-01"

A project board is not a selector here: resolve it to issue numbers yourself and
pass them via `--issues`.

Output shape (stdout, or --out FILE):
    {
      "set": {"repo","selector","selector_value","title","description","url"},
      "counts": {"issues","open","closed","criteria","linked_prs",
                 "cross_repo_refs","path_hints"},
      "issues": [
        {"number","title","state","url","closedAt","labels":[...],"body",
         "criteria": [{"index","text","ticked","heading"}],
         "linked_prs": [{"repo","number","url","title","state","merged"}]}
      ],
      "pull_requests": [
        {"repo","number","title","url","state","merged","mergedAt",
         "author_login","body","thin"}
      ],
      "cross_repo_refs": [{"ref","repo","count","seen_in":[...]}],
      "path_hints":     [{"path","count","seen_in":[...]}],
      "errors":   [{"where","error"}],
      "warnings": [{"where","warning"}]
    }

Integrity: `ticked` is recorded but is **not** a completion signal — many repos
close issues without ever ticking, so the agent must grade each criterion on
evidence (see SKILL.md step 5). Any failure is isolated and RECORDED in `errors`
rather than shrinking a count silently; hitting a page limit lands in `warnings`.
The process exits **non-zero** whenever either list is non-empty, so a lost
issue can never masquerade as a complete set. All `gh` output is decoded as
UTF-8 — the Windows cp1252 default would otherwise choke on unicode-heavy
bodies and drop the run.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict

THIN_BODY_CHARS = 80
ISSUE_FIELDS = "number,title,state,url,body,closedAt,labels"

CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.*\S)\s*$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*\S)\s*$")

# owner/name#123 — a reference that leaves this repo.
CROSS_REPO_RE = re.compile(r"\b([A-Za-z0-9][\w.-]*/[\w.-]+)#(\d+)\b")
# Bare `owner/name` in prose or a link, no issue number.
BARE_REPO_RE = re.compile(r"\bgithub\.com/([A-Za-z0-9][\w.-]*/[\w.-]+?)(?:\.git)?[/\s)\]]")
# A file that could hold evidence: a path with a known data/code extension.
PATH_RE = re.compile(
    r"(?<![\w/])((?:[\w.-]+/)*[\w.-]+"
    r"\.(?:xlsx|xls|csv|tsv|json|ya?ml|db|sqlite3?|parquet|txt|md|py|sql|toml|ini|cfg))"
    r"(?![\w])"
)
# Paths that are noise rather than evidence.
PATH_NOISE = re.compile(
    r"(^|/)(node_modules|\.venv|venv|site-packages|__pycache__|dist|build)/|"
    r"^(readme|license|contributing|changelog)\.md$|"
    r"^\.github/", re.IGNORECASE
)


def run_gh(args: "list[str]") -> "tuple[int, str, str]":
    """Run a gh command, decoding as UTF-8 regardless of platform default."""
    try:
        proc = subprocess.run(
            ["gh", *args], capture_output=True, check=False,
        )
    except FileNotFoundError:
        return 127, "", "gh CLI not found on PATH"
    decode = lambda b: b.decode("utf-8", errors="replace")  # noqa: E731
    return proc.returncode, decode(proc.stdout), decode(proc.stderr)


def gh_json(args: "list[str]", where: str, errors: list) -> "object | None":
    code, out, err = run_gh(args)
    if code != 0:
        errors.append({"where": where, "error": (err or out).strip()[:500]})
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError as exc:
        errors.append({"where": where, "error": f"bad JSON from gh: {exc}"})
        return None


def check_auth(errors: list) -> bool:
    code, _, err = run_gh(["auth", "status"])
    if code != 0:
        errors.append({"where": "gh auth", "error": err.strip()[:500] or "not authenticated"})
        return False
    return True


def resolve_milestone(repo: str, value: str, errors: list) -> "dict | None":
    """Accept a milestone number, a URL ending in a number, or a title substring."""
    tail = value.rstrip("/").rsplit("/", 1)[-1]
    milestones = gh_json(
        ["api", f"repos/{repo}/milestones?state=all&per_page=100"],
        f"milestones of {repo}", errors,
    )
    if milestones is None:
        return None
    if tail.isdigit():
        for m in milestones:
            if str(m["number"]) == tail:
                return m
        errors.append({"where": "milestone", "error": f"no milestone #{tail} in {repo}"})
        return None
    matches = [m for m in milestones if value.lower() in (m.get("title") or "").lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        errors.append({"where": "milestone", "error": f"no milestone matching {value!r} in {repo}"})
    else:
        titles = ", ".join(repr(m["title"]) for m in matches)
        errors.append({"where": "milestone", "error": f"{value!r} matches several milestones: {titles}"})
    return None


def list_issues(repo: str, args, errors: list, warnings: list) -> "list[dict]":
    """Resolve the selector to concrete issues. Pull requests are excluded."""
    if args.issues:
        wanted = [n.strip().lstrip("#") for n in args.issues.split(",") if n.strip()]
        issues = []
        for num in wanted:
            data = gh_json(
                ["issue", "view", num, "--repo", repo, "--json", ISSUE_FIELDS],
                f"issue #{num}", errors,
            )
            if data is not None:
                issues.append(data)
        return issues

    cmd = ["issue", "list", "--repo", repo, "--state", args.state,
           "--limit", str(args.limit), "--json", ISSUE_FIELDS]
    if args.milestone_title:
        cmd += ["--milestone", args.milestone_title]
    elif args.label:
        cmd += ["--label", args.label]
    elif args.query:
        cmd += ["--search", args.query]

    data = gh_json(cmd, "issue list", errors)
    if data is None:
        return []
    if len(data) >= args.limit:
        warnings.append({
            "where": "issue list",
            "warning": f"hit --limit {args.limit}; the set may be truncated. Re-run with a higher --limit.",
        })
    return data


def extract_criteria(body: str) -> "list[dict]":
    """Every checkbox line, with the heading it sits under.

    `ticked` is reported, never trusted: see the module docstring.
    """
    criteria, heading = [], None
    for line in (body or "").splitlines():
        h = HEADING_RE.match(line)
        if h:
            heading = h.group(1)
            continue
        m = CHECKBOX_RE.match(line)
        if m:
            criteria.append({
                "index": len(criteria) + 1,
                "text": m.group(2),
                "ticked": m.group(1).lower() == "x",
                "heading": heading,
            })
    return criteria


def linked_prs(repo: str, number: int, errors: list) -> "list[dict]":
    """PRs connected to an issue, from its timeline."""
    events = gh_json(
        ["api", f"repos/{repo}/issues/{number}/timeline?per_page=100", "--paginate"],
        f"timeline of #{number}", errors,
    )
    if events is None:
        return []
    found, seen = [], set()
    for ev in events:
        src = None
        if ev.get("event") == "cross-referenced":
            src = (ev.get("source") or {}).get("issue")
        elif ev.get("event") in {"connected", "referenced", "closed"}:
            src = ev.get("source", {}).get("issue") if ev.get("source") else None
        if not src or not src.get("pull_request"):
            continue
        url = src.get("html_url") or src["pull_request"].get("html_url", "")
        m = re.search(r"github\.com/([^/]+/[^/]+)/pull/(\d+)", url)
        if not m:
            continue
        key = (m.group(1), int(m.group(2)))
        if key in seen:
            continue
        seen.add(key)
        found.append({
            "repo": m.group(1),
            "number": int(m.group(2)),
            "url": url,
            "title": src.get("title", ""),
            "state": src.get("state", ""),
            "merged": bool((src.get("pull_request") or {}).get("merged_at")),
        })
    return sorted(found, key=lambda p: (p["repo"], p["number"]))


def fetch_pr(repo: str, number: int, errors: list) -> "dict | None":
    data = gh_json(
        ["pr", "view", str(number), "--repo", repo,
         "--json", "number,title,url,state,mergedAt,author,body"],
        f"PR {repo}#{number}", errors,
    )
    if data is None:
        return None
    body = data.get("body") or ""
    return {
        "repo": repo,
        "number": data["number"],
        "title": data.get("title", ""),
        "url": data.get("url", ""),
        "state": data.get("state", ""),
        "merged": bool(data.get("mergedAt")),
        "mergedAt": data.get("mergedAt"),
        "author_login": (data.get("author") or {}).get("login", ""),
        "body": body,
        "thin": len(body.strip()) < THIN_BODY_CHARS,
    }


def scan_trail(texts: "list[tuple[str, str]]", home_repo: str) -> "tuple[list, list]":
    """Find cross-repo references and artifact paths across every trail text.

    `texts` is [(source_label, text)] — the label lets the agent trace a hit
    back to the issue or PR that mentioned it.
    """
    refs, paths = defaultdict(lambda: {"count": 0, "seen_in": set()}), defaultdict(
        lambda: {"count": 0, "seen_in": set()})
    home = home_repo.lower()

    for label, text in texts:
        if not text:
            continue
        for repo, num in CROSS_REPO_RE.findall(text):
            if repo.lower() == home:
                continue
            entry = refs[f"{repo}#{num}"]
            entry["count"] += 1
            entry["seen_in"].add(label)
        for repo in BARE_REPO_RE.findall(text):
            if repo.lower() == home or "/" not in repo:
                continue
            entry = refs[repo]
            entry["count"] += 1
            entry["seen_in"].add(label)
        for path in PATH_RE.findall(text):
            if PATH_NOISE.search(path):
                continue
            entry = paths[path]
            entry["count"] += 1
            entry["seen_in"].add(label)

    ref_list = [
        {"ref": k, "repo": k.split("#")[0], "count": v["count"],
         "seen_in": sorted(v["seen_in"])}
        for k, v in refs.items()
    ]
    path_list = [
        {"path": k, "count": v["count"], "seen_in": sorted(v["seen_in"])}
        for k, v in paths.items()
    ]
    ref_list.sort(key=lambda r: (-r["count"], r["ref"]))
    path_list.sort(key=lambda p: (-p["count"], p["path"]))
    return ref_list, path_list


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", required=True, help="owner/name holding the issues")
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument("--milestone", help="milestone number, URL, or title substring")
    sel.add_argument("--label")
    sel.add_argument("--issues", help="comma-separated issue numbers")
    sel.add_argument("--query", help="raw gh issue search query")
    ap.add_argument("--state", default="all", choices=["all", "open", "closed"])
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--no-prs", action="store_true", help="skip PR bodies (faster, less evidence)")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    args = ap.parse_args()

    errors: list = []
    warnings: list = []

    if not check_auth(errors):
        json.dump({"errors": errors, "warnings": warnings}, sys.stdout, indent=2)
        return 1

    repo = args.repo.strip().rstrip("/")
    if repo.startswith("http"):
        m = re.search(r"github\.com/([^/]+/[^/]+)", repo)
        repo = m.group(1) if m else repo

    set_meta = {"repo": repo, "selector": None, "selector_value": None,
                "title": None, "description": None, "url": None}
    args.milestone_title = None

    if args.milestone:
        set_meta.update(selector="milestone", selector_value=args.milestone)
        ms = resolve_milestone(repo, args.milestone, errors)
        if ms is None:
            json.dump({"set": set_meta, "errors": errors, "warnings": warnings},
                      sys.stdout, indent=2)
            return 1
        args.milestone_title = ms["title"]
        set_meta.update(title=ms["title"], description=ms.get("description") or "",
                        url=ms.get("html_url"))
    else:
        for name in ("label", "issues", "query"):
            if getattr(args, name):
                set_meta.update(selector=name, selector_value=getattr(args, name),
                                title=f"{name}: {getattr(args, name)}")
                break

    issues = list_issues(repo, args, errors, warnings)

    collected, pr_index = [], {}
    for raw in sorted(issues, key=lambda i: i["number"]):
        body = raw.get("body") or ""
        prs = [] if args.no_prs else linked_prs(repo, raw["number"], errors)
        collected.append({
            "number": raw["number"],
            "title": raw.get("title", ""),
            "state": (raw.get("state") or "").lower(),
            "url": raw.get("url", ""),
            "closedAt": raw.get("closedAt"),
            "labels": [l.get("name") for l in (raw.get("labels") or [])],
            "body": body,
            "criteria": extract_criteria(body),
            "linked_prs": prs,
        })
        for pr in prs:
            pr_index.setdefault((pr["repo"], pr["number"]), pr)

    pull_requests = []
    if not args.no_prs:
        for (pr_repo, pr_num) in sorted(pr_index):
            full = fetch_pr(pr_repo, pr_num, errors)
            if full is not None:
                pull_requests.append(full)

    texts = [(f"issue #{i['number']}", i["body"]) for i in collected]
    texts += [(f"{p['repo']}#{p['number']}", p["body"]) for p in pull_requests]
    if set_meta.get("description"):
        texts.append(("milestone description", set_meta["description"]))
    cross_refs, path_hints = scan_trail(texts, repo)

    result = {
        "set": set_meta,
        "counts": {
            "issues": len(collected),
            "open": sum(1 for i in collected if i["state"] == "open"),
            "closed": sum(1 for i in collected if i["state"] == "closed"),
            "criteria": sum(len(i["criteria"]) for i in collected),
            "linked_prs": len(pull_requests),
            "cross_repo_refs": len(cross_refs),
            "path_hints": len(path_hints),
        },
        "issues": collected,
        "pull_requests": pull_requests,
        "cross_repo_refs": cross_refs,
        "path_hints": path_hints,
        "errors": errors,
        "warnings": warnings,
    }

    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {args.out}: {result['counts']}")
    else:
        sys.stdout.write(text)

    for e in errors:
        print(f"ERROR  {e['where']}: {e['error']}", file=sys.stderr)
    for w in warnings:
        print(f"WARN   {w['where']}: {w['warning']}", file=sys.stderr)
    return 1 if (errors or warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
