#!/usr/bin/env python3
"""Refresh data/github_stars.json — the stargazer count of every repo a page links to.

Repos are discovered from `extra.github_link` in content/**/*.md, so a new project needs
nothing beyond its front matter to be picked up here. One REST call per repo: with the
workflow's GITHUB_TOKEN that is a rounding error against the 5000/h allowance.

It also writes data/github_prs.json: the state (open / merged / closed) and merge date of
every pull request listed under `[[extra.contributions]]` (content/projects/_index.md), so
a contribution's chip flips from "pending" to "merged" without editing the front matter.
The upstream repos of those PRs get a star count like any other repo.

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
PRS_FILE = ROOT / "data" / "github_prs.json"
API = "https://api.github.com/repos"


def log(msg: str) -> None:
    print(msg, flush=True)


def read_extras() -> list[dict]:
    """The `[extra]` table of every content file that has TOML front matter."""
    extras = []
    for path in sorted(CONTENT_DIR.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+", raw, re.S)
        if match:
            extras.append(tomllib.loads(match.group(1)).get("extra", {}) or {})
    return extras


def read_repos(extras: list[dict]) -> list[str]:
    """"owner/name" for every github_link and contribution repo, lowercased to match the template."""
    repos = set()
    for extra in extras:
        link = extra.get("github_link", "")
        if m := re.match(r"https?://github\.com/([\w.\-]+/[\w.\-]+?)(?:\.git)?/?$", link, re.I):
            repos.add(m.group(1).lower())
        for contrib in extra.get("contributions", []) or []:
            if repo := contrib.get("repo"):
                repos.add(repo.lower())
    return sorted(repos)


def pr_number(value: object) -> int | None:
    """The PR number, or None for a contribution with no PR yet (missing, "", "X", 0).

    Accepts 79 or "79", like the template's `int` filter, so both agree on which entries
    are real PRs. A placeholder must never crash the run: it would stop every star count
    and PR state from refreshing.
    """
    if isinstance(value, bool):
        return None
    try:
        number = int(str(value).strip())
    except ValueError:
        return None
    return number if number > 0 else None


def read_prs(extras: list[dict]) -> list[tuple[str, int]]:
    """(repo, number) for every `[[extra.contributions]]` entry that has a PR, repo lowercased."""
    prs = set()
    for extra in extras:
        for contrib in extra.get("contributions", []) or []:
            repo = contrib.get("repo")
            number = pr_number(contrib.get("pr"))
            if repo and number:
                prs.add((repo.lower(), number))
            elif repo:
                log(f"  {repo}: no PR number yet, skipped")
    return sorted(prs)


def refresh_prs(session: requests.Session, prs: list[tuple[str, int]]) -> None:
    """Write data/github_prs.json. A PR whose lookup fails keeps its previous entry."""
    previous = {}
    if PRS_FILE.exists():
        try:
            data = json.loads(PRS_FILE.read_text(encoding="utf-8"))
            previous = {(p["repo"], p["number"]): p for p in data.get("prs", [])}
        except (json.JSONDecodeError, KeyError, TypeError):
            previous = {}

    out, failed = [], 0
    for repo, number in prs:
        try:
            resp = session.get(f"{API}/{repo}/pulls/{number}", timeout=20)
            resp.raise_for_status()
            data = resp.json()
            merged_at = data.get("merged_at") or ""
            state = "merged" if merged_at else data["state"]  # GitHub says "open" | "closed"
        except (requests.RequestException, KeyError, ValueError) as exc:
            failed += 1
            if (repo, number) not in previous:
                log(f"  {repo}#{number}: failed ({exc}), no previous state, skipped")
                continue
            entry = previous[(repo, number)]
            log(f"  {repo}#{number}: failed ({exc}), keeping {entry['state']}")
        else:
            entry = {"repo": repo, "number": number, "state": state}
            if merged_at:
                entry["merged_at"] = merged_at[:10]  # the template only shows month + year
            log(f"  {repo}#{number}: {state}")
        out.append(entry)

    if failed == len(prs):
        log("every PR lookup failed, leaving the PR file untouched")
        return
    PRS_FILE.parent.mkdir(exist_ok=True)
    PRS_FILE.write_text(json.dumps({"prs": out}, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {PRS_FILE.relative_to(ROOT)}")


def load_previous() -> dict[str, int]:
    if not OUT_FILE.exists():
        return {}
    try:
        data = json.loads(OUT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {r["repo"]: r["stars"] for r in data.get("repos", [])}


def main() -> int:
    extras = read_extras()
    repos = read_repos(extras)
    prs = read_prs(extras)

    session = requests.Session()
    session.headers["Accept"] = "application/vnd.github+json"
    if token := os.environ.get("GITHUB_TOKEN"):
        session.headers["Authorization"] = f"Bearer {token}"

    if prs:
        log(f"{len(prs)} pull request(s)")
        refresh_prs(session, prs)

    if not repos:
        log("no github_link found in content/, nothing to do")
        return 0
    log(f"{len(repos)} repo(s)")

    previous = load_previous()

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
