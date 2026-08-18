#!/usr/bin/env python3
"""Collect merged GitHub PRs for one or more repos over a resolved window.

Verifies `gh` auth once, then for each repo runs a single `gh pr list` search
and emits one consolidated JSON document the agent can interpret directly —
instead of hand-rolling `gh` incantations and paging per run.

Usage:
    python collect_prs.py --repo owner/name [--repo owner/name ...] \
        --since 2026-07-15 --until 2026-07-29 [--limit 200] [--out FILE]

    # or pass a ready-made qualifier from resolve_window.py:
    python collect_prs.py --repo owner/name --qualifier "merged:>=2026-07-15 merged:<=2026-07-29"

Output shape (stdout, or --out FILE):
    {
      "window": {"since","until","qualifier"},
      "repos": ["owner/name", ...],
      "counts": {"total": N, "per_repo": {"owner/name": N | null, ...},  # null = failed, not 0
                 "hint_internal": M, "thin": K},
      "pull_requests": [
        {"repo","number","title","url","mergedAt","author_login",
         "author_is_bot","labels":[...], "body",
         "thin": bool,          # body too short to judge impact -> `gh pr view` it
         "hint_internal": bool} # HEURISTIC only; the agent makes the real call
        ...
      ],
      "errors": [{"repo","error"}, ...],     # a repo that failed for ANY reason
      "warnings": [{"repo","warning"}, ...]  # a repo that hit --limit (maybe truncated)
    }

Integrity: any per-repo failure (unreachable, decode error, bad JSON — anything)
is isolated and RECORDED in `errors`, with that repo's count set to `null` (never a
silent 0); a repo that hit `--limit` is recorded in `warnings`. The process exits
**non-zero** whenever either list is non-empty, so a lost or truncated repo can
never masquerade as a clean "0 merged". Each repo's existence/access is verified
(`gh repo view`) before its PRs are searched — a mistyped or unauthorised repo
lands in `errors` rather than a false `0` (the `--search` path returns empty+exit-0
for a nonexistent repo). All `gh` output is decoded as UTF-8 — the Windows cp1252
default would otherwise choke on unicode-heavy PR bodies and drop a whole repo.
`hint_internal` is a cheap guess (bots, deps/ci labels, "chore/bump/…"
titles) to save the agent legwork — never a verdict.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

THIN_BODY_CHARS = 80
INTERNAL_LABELS = {
    "dependencies", "deps", "ci", "chore", "build", "tooling",
    "github_actions", "github-actions", "test", "tests", "refactor",
}
INTERNAL_TITLE_RE = re.compile(
    r"^\s*(chore|ci|build|deps|dep|bump|dependabot|test|refactor|style)\b|"
    r"\bbump\b", re.IGNORECASE
)
BOT_LOGINS = {
    "dependabot", "dependabot[bot]", "app/dependabot",
    "github-actions[bot]", "renovate[bot]",
}

PR_FIELDS = "number,title,url,mergedAt,author,labels,body"


def check_auth() -> "str | None":
    """Return None if authenticated, else an error string."""
    try:
        proc = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True
        )
    except FileNotFoundError:
        return "the `gh` CLI is not installed or not on PATH"
    if proc.returncode != 0:
        return "gh is not authenticated (`gh auth status` failed); run `gh auth login`"
    return None


def list_prs(repo: str, qualifier: str, limit: int) -> list[dict]:
    proc = subprocess.run(
        ["gh", "pr", "list", "--repo", repo, "--state", "merged",
         "--search", qualifier, "--limit", str(limit), "--json", PR_FIELDS],
        capture_output=True, text=True, encoding="utf-8", errors="strict",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "gh pr list failed")
    return json.loads(proc.stdout or "[]")


def verify_repo(repo: str) -> None:
    """Raise if the repo is missing or inaccessible.

    `gh pr list --search` runs through the Search API, which returns an empty
    set (exit 0) for a nonexistent `repo:` qualifier — so a typo'd or unauthorised
    repo would otherwise masquerade as a clean "0 merged". A direct `gh repo view`
    fails loudly instead, turning that into a recorded error.
    """
    proc = subprocess.run(
        ["gh", "repo", "view", repo, "--json", "nameWithOwner"],
        capture_output=True, text=True, encoding="utf-8", errors="strict",
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "repo not found or not accessible: "
            + (proc.stderr.strip() or "gh repo view failed")
        )


def is_internal_hint(title: str, label_names: list[str], is_bot: bool) -> bool:
    if is_bot:
        return True
    if any(name.lower() in INTERNAL_LABELS for name in label_names):
        return True
    return bool(INTERNAL_TITLE_RE.search(title or ""))


def normalize(repo: str, pr: dict) -> dict:
    author = pr.get("author") or {}
    login = author.get("login") or "unknown"
    is_bot = bool(author.get("is_bot")) or login.lower() in BOT_LOGINS
    label_names = [l.get("name", "") for l in (pr.get("labels") or [])]
    body = pr.get("body") or ""
    thin = len(body.strip()) < THIN_BODY_CHARS
    return {
        "repo": repo,
        "number": pr.get("number"),
        "title": pr.get("title", ""),
        "url": pr.get("url", ""),
        "mergedAt": (pr.get("mergedAt") or "")[:10],
        "author_login": login,
        "author_is_bot": is_bot,
        "labels": label_names,
        "body": body,
        "thin": thin,
        "hint_internal": is_internal_hint(pr.get("title", ""), label_names, is_bot),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", action="append", required=True,
                    help="owner/name; repeat for multiple repos")
    ap.add_argument("--qualifier", help="e.g. 'merged:>=A merged:<=B'")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.qualifier:
        qualifier = args.qualifier
    elif args.since and args.until:
        qualifier = f"merged:>={args.since} merged:<={args.until}"
    else:
        ap.error("provide --qualifier, or both --since and --until")

    auth_err = check_auth()
    if auth_err:
        json.dump({"error": auth_err}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        sys.exit(1)

    prs: list[dict] = []
    errors: list[dict] = []
    warnings: list[dict] = []
    per_repo: "dict[str, int | None]" = {}
    for repo in args.repo:
        try:
            verify_repo(repo)  # a typo'd/inaccessible repo must error, not masquerade as "0 merged"
            raw = list_prs(repo, qualifier, args.limit)
        except Exception as exc:  # noqa: BLE001 — isolate AND record any per-repo failure; never swallow it
            errors.append({"repo": repo, "error": f"{type(exc).__name__}: {exc}"})
            per_repo[repo] = None  # unknown, NOT zero — a failure is not "0 merged"
            continue
        normalized = [normalize(repo, pr) for pr in raw]
        prs.extend(normalized)
        per_repo[repo] = len(normalized)
        if len(raw) >= args.limit:
            warnings.append({
                "repo": repo,
                "warning": f"hit --limit {args.limit}; result may be truncated — "
                           "re-run with a higher --limit or a narrower window",
            })

    prs.sort(key=lambda p: (p["repo"], p["mergedAt"]))
    doc = {
        "window": {"since": args.since, "until": args.until, "qualifier": qualifier},
        "repos": args.repo,
        "counts": {
            "total": len(prs),
            "per_repo": per_repo,
            "hint_internal": sum(1 for p in prs if p["hint_internal"]),
            "thin": sum(1 for p in prs if p["thin"]),
        },
        "pull_requests": prs,
        "errors": errors,
        "warnings": warnings,
    }

    text = json.dumps(doc, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        sys.stderr.write(f"wrote {len(prs)} PRs across {len(args.repo)} repo(s) to {args.out}\n")
    else:
        print(text)

    # Loud, non-zero signal on ANY integrity concern — a failed or truncated repo
    # must never look like a clean "0 merged". The agent MUST read errors/warnings.
    for e in errors:
        sys.stderr.write(f"ERROR  {e['repo']}: {e['error']}\n")
    for w in warnings:
        sys.stderr.write(f"WARN   {w['repo']}: {w['warning']}\n")
    if errors or warnings:
        sys.stderr.write(
            f"\n{len(errors)} repo error(s), {len(warnings)} truncation warning(s). "
            "Do NOT treat any affected repo's count as authoritative; re-check it directly.\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
