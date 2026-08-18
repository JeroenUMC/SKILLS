#!/usr/bin/env python3
"""Resolve a changelog time-window spec into concrete GitHub search dates.

Emits JSON to stdout:
    {"since": "YYYY-MM-DD", "until": "YYYY-MM-DD",
     "qualifier": "merged:>=SINCE merged:<=UNTIL", "basis": "<how it was derived>"}

`qualifier` is the string to hand straight to `gh pr list --search`. When there
is no lower bound (a release with no predecessor), `since` is null and the
qualifier omits the `merged:>=` half.

Provide exactly one of:
    --since / --until   explicit ISO dates (skips all parsing; most reliable)
    --window "..."      natural language:
                          "last two weeks", "past 3 months", "last 10 days",
                          a bare year "2026",
                          a range "2026-07-01 to 2026-07-29" (also "..", "->")
    --release TAG       the span between the previous release and TAG
                          (requires --repo owner/name; shells out to `gh`)

Options:
    --repo owner/name   required only for --release
    --today YYYY-MM-DD  override "now" for relative windows (default: system date)

On anything it cannot parse it exits non-zero with a message telling the caller
to pass explicit --since/--until instead. The agent is good at date math, so
falling back to explicit dates is always fine.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import re
import subprocess
import sys

WORD_NUMBERS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12,
}
RANGE_SEPARATORS = [" to ", " through ", " until ", "..", "->", "—", " – ", " - "]


def fail(msg: str) -> "None":
    sys.stderr.write(msg.rstrip() + "\n")
    sys.exit(2)


def parse_date(s: str) -> dt.date:
    s = s.strip().replace("/", "-")
    return dt.date.fromisoformat(s)


def months_before(d: dt.date, n: int) -> dt.date:
    """Date n calendar months before d, clamped to the target month's last day."""
    total = (d.year * 12 + (d.month - 1)) - n
    year, month = divmod(total, 12)
    month += 1
    last = calendar.monthrange(year, month)[1]
    return dt.date(year, month, min(d.day, last))


def gh_json(args: list[str]) -> object:
    proc = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="strict"
    )
    if proc.returncode != 0:
        fail(f"gh {' '.join(args)} failed:\n{proc.stderr.strip()}")
    return json.loads(proc.stdout or "null")


def resolve_release(repo: str, tag: str) -> dict:
    if not repo:
        fail("--release requires --repo owner/name")
    view = gh_json(
        ["release", "view", tag, "--repo", repo,
         "--json", "tagName,publishedAt,createdAt"]
    )
    until_iso = view.get("publishedAt") or view.get("createdAt")
    if not until_iso:
        fail(f"release {tag} has no publish/create date")
    until = until_iso[:10]

    rels = gh_json(
        ["release", "list", "--repo", repo, "--limit", "100",
         "--json", "tagName,publishedAt,createdAt"]
    ) or []
    dated = [
        (r["tagName"], (r.get("publishedAt") or r.get("createdAt") or "")[:10])
        for r in rels
        if (r.get("publishedAt") or r.get("createdAt"))
    ]
    # Newest first.
    dated.sort(key=lambda x: x[1], reverse=True)
    since = None
    for _tag, date in dated:
        if date < until:
            since = date
            break
    basis = (
        f"release {tag} ({until}) since previous release {since}"
        if since else
        f"release {tag} ({until}); no previous release, no lower bound"
    )
    return {"since": since, "until": until, "basis": basis}


def resolve_window(window: str, today: dt.date) -> dict:
    w = window.strip().lower()

    # Bare year, e.g. "2026".
    m = re.fullmatch(r"(\d{4})", w)
    if m:
        year = int(m.group(1))
        return {
            "since": f"{year}-01-01",
            "until": f"{year}-12-31",
            "basis": f"calendar year {year}",
        }

    # Explicit range: "A to B", "A .. B", "A -> B", optionally led by "from".
    body = re.sub(r"^from\s+", "", w)
    for sep in RANGE_SEPARATORS:
        if sep in body:
            left, right = body.split(sep, 1)
            try:
                a, b = parse_date(left), parse_date(right)
            except ValueError:
                continue
            lo, hi = sorted((a, b))
            return {
                "since": lo.isoformat(),
                "until": hi.isoformat(),
                "basis": f"explicit range {lo} to {hi}",
            }

    # Relative: "last/past/previous N unit(s)" or "last week/month/year".
    m = re.search(
        r"(?:last|past|previous|recent)\s+"
        r"(?:(\d+|" + "|".join(WORD_NUMBERS) + r")\s+)?"
        r"(day|week|month|year)s?",
        w,
    )
    if m:
        qty_tok, unit = m.group(1), m.group(2)
        qty = 1 if qty_tok is None else int(qty_tok) if qty_tok.isdigit() else WORD_NUMBERS[qty_tok]
        if unit == "day":
            since = today - dt.timedelta(days=qty)
        elif unit == "week":
            since = today - dt.timedelta(weeks=qty)
        elif unit == "month":
            since = months_before(today, qty)
        else:  # year
            since = months_before(today, 12 * qty)
        return {
            "since": since.isoformat(),
            "until": today.isoformat(),
            "basis": f"last {qty} {unit}(s), relative to {today}",
        }

    # Single ISO date → from then until today.
    try:
        d = parse_date(w)
        return {
            "since": d.isoformat(),
            "until": today.isoformat(),
            "basis": f"since {d} through {today}",
        }
    except ValueError:
        pass

    fail(
        f"could not parse window {window!r}. Pass explicit "
        "--since YYYY-MM-DD --until YYYY-MM-DD instead (or --release TAG "
        "with --repo for a release span)."
    )


def build_qualifier(since: "str | None", until: str) -> str:
    parts = []
    if since:
        parts.append(f"merged:>={since}")
    parts.append(f"merged:<={until}")
    return " ".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--window")
    ap.add_argument("--release")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--repo")
    ap.add_argument("--today")
    args = ap.parse_args()

    today = parse_date(args.today) if args.today else dt.date.today()

    if args.since or args.until:
        if not (args.since and args.until):
            fail("--since and --until must be given together")
        res = {
            "since": args.since,
            "until": args.until,
            "basis": "explicit --since/--until",
        }
    elif args.release:
        res = resolve_release(args.repo or "", args.release)
    elif args.window:
        res = resolve_window(args.window, today)
    else:
        fail("provide one of --window, --release, or --since/--until")

    res["qualifier"] = build_qualifier(res.get("since"), res["until"])
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
