#!/usr/bin/env python3
"""Refresh data/github_stars.json — the stargazer count of every repo a page links to.

Repos are discovered from `extra.github_link` in content/**/*.md, so a new project needs
nothing beyond its front matter to be picked up here. One REST call per repo: with the
workflow's GITHUB_TOKEN that is a rounding error against the 5000/h allowance.

Failure is never destructive: a repo whose lookup fails keeps its previous count, so a
flaky API call leaves the site as it was instead of dropping the badge.

The file deliberately carries no timestamp: an unchanged count must produce an unchanged
file, or every daily run would commit and redeploy for nothing.

Env:
  GITHUB_TOKEN  recommended; without it the anonymous 60/h limit still covers a local run.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tomllib
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUT_FILE = ROOT / "data" / "github_stars.json"
API = "https://api.github.com/repos"


def log(msg: str) -> None:
    print(msg, flush=True)


def read_repos() -> list[str]:
    """"owner/name" for every github_link in the content, lowercased to match the template."""
    repos = set()
    for path in sorted(CONTENT_DIR.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+", raw, re.S)
        if not match:
            continue
        extra = tomllib.loads(match.group(1)).get("extra", {}) or {}
        link = extra.get("github_link", "")
        if m := re.match(r"https?://github\.com/([\w.\-]+/[\w.\-]+?)(?:\.git)?/?$", link, re.I):
            repos.add(m.group(1).lower())
    return sorted(repos)


def load_previous() -> dict[str, int]:
    if not OUT_FILE.exists():
        return {}
    try:
        data = json.loads(OUT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {r["repo"]: r["stars"] for r in data.get("repos", [])}


def main() -> int:
    repos = read_repos()
    if not repos:
        log("no github_link found in content/, nothing to do")
        return 0
    log(f"{len(repos)} repo(s)")

    previous = load_previous()
    session = requests.Session()
    session.headers["Accept"] = "application/vnd.github+json"
    if token := os.environ.get("GITHUB_TOKEN"):
        session.headers["Authorization"] = f"Bearer {token}"

    out, failed = [], 0
    for repo in repos:
        try:
            resp = session.get(f"{API}/{repo}", timeout=20)
            resp.raise_for_status()
            stars = int(resp.json()["stargazers_count"])
        except (requests.RequestException, KeyError, ValueError) as exc:
            failed += 1
            if repo not in previous:
                log(f"  {repo}: failed ({exc}), no previous count, skipped")
                continue
            stars = previous[repo]
            log(f"  {repo}: failed ({exc}), keeping {stars}")
        else:
            log(f"  {repo}: {stars}")
        out.append({"repo": repo, "stars": stars})

    if failed == len(repos):
        log("every lookup failed, leaving the file untouched")
        return 1

    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps({"repos": out}, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {OUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
