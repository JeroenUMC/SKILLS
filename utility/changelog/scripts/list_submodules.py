#!/usr/bin/env python3
"""List a repo's git submodules as owner/name pairs, read from .gitmodules.

Usage:
    python list_submodules.py [--repo-path .]

Emits JSON to stdout:
    [{"name","path","url","owner_repo"}, ...]

`owner_repo` is filled only for GitHub remotes (github.com), in the "owner/name"
form `gh` and collect_prs.py expect; for non-GitHub or unparseable URLs it is
null. If there is no .gitmodules file, prints [] (the common "no submodules"
case). This only reads .gitmodules — it does not resolve the pinned commit.
"""
from __future__ import annotations

import argparse
import configparser
import json
import os
import re
import sys

GITHUB_URL_RE = re.compile(
    r"github\.com[:/]+(?P<owner>[^/]+)/(?P<name>[^/]+?)(?:\.git)?/?$",
    re.IGNORECASE,
)


def owner_repo_from_url(url: str) -> "str | None":
    m = GITHUB_URL_RE.search(url.strip())
    if not m:
        return None
    return f"{m.group('owner')}/{m.group('name')}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-path", default=".")
    args = ap.parse_args()

    path = os.path.join(args.repo_path, ".gitmodules")
    if not os.path.isfile(path):
        print("[]")
        return

    parser = configparser.ConfigParser()
    # .gitmodules is INI-like: [submodule "name"] with path= and url=.
    try:
        parser.read(path, encoding="utf-8")
    except configparser.Error as exc:
        sys.stderr.write(f"could not parse {path}: {exc}\n")
        sys.exit(2)

    out = []
    for section in parser.sections():
        if not section.startswith("submodule"):
            continue
        m = re.match(r'submodule\s+"(?P<name>.+)"', section)
        name = m.group("name") if m else section
        url = parser.get(section, "url", fallback="")
        out.append({
            "name": name,
            "path": parser.get(section, "path", fallback=""),
            "url": url,
            "owner_repo": owner_repo_from_url(url) if url else None,
        })

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
