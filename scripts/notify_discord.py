#!/usr/bin/env python3
"""Announce on Discord each citation fetch_citations.py saw for the first time.

Usage: notify_discord.py <new_citations.json>

Run by the workflow only once data/citations.json is committed, so a run whose push
fails announces nothing and the next run, still seeing those citations as new, does.

Env:
  DISCORD_WEBHOOK_LINK  required; the channel webhook.
  MY_DISCORD_USER_ID    optional; who to ping in every message.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

import requests

SOURCE_NAMES = {"scholar": "Google Scholar", "semanticscholar": "Semantic Scholar", "openalex": "OpenAlex"}
SUPPRESS_EMBEDS = 1 << 2
DISCORD_LIMIT = 2000


def escape(text: str, limit: int = 300) -> str:
    """Plain text that cannot break out of a masked link or turn into formatting."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return re.sub(r"([\\*_~`|\[\]<>#])", r"\\\1", text)


def link(text: str, url: str) -> str:
    if not url:
        return f"**{text}**"
    # Inside <...> the URL survives parentheses; only these three can still end it early.
    url = url.replace(" ", "%20").replace(">", "%3E").replace(")", "%29")
    return f"**[{text}](<{url}>)**"


def format_message(item: dict, user_id: str | None) -> str:
    paper, cit = item["paper"], item["citation"]
    url = cit.get("url") or f"https://scholar.google.com/scholar?q={quote_plus(cit['title'])}"
    details = " · ".join(filter(None, [
        escape(cit.get("authors", ""), 200),
        escape(", ".join(str(p) for p in (cit.get("venue"), cit.get("year")) if p), 200),
    ]))
    sources = ", ".join(SOURCE_NAMES.get(s, s) for s in cit.get("sources", []))
    count = paper["count"]
    lines = [
        f"{f'<@{user_id}> ' if user_id else ''}📚 **Nouvelle citation !**",
        f"{link(escape(cit['title']), url)}",
        *([f"-# {details}"] if details else []),
        f"cite {link(escape(paper['title']), paper['url'])}",
        f"**Source :** {sources}",
        f"**Total :** {count} citation{'s' if count > 1 else ''} pour ce papier",
    ]
    return "\n".join(lines)[:DISCORD_LIMIT]


def post(webhook: str, content: str, user_id: str | None) -> None:
    payload = {
        "content": content,
        "flags": SUPPRESS_EMBEDS,
        # Ping exactly the configured user, never whatever a paper title might contain.
        "allowed_mentions": {"parse": [], "users": [user_id] if user_id else []},
    }
    for _ in range(5):
        resp = requests.post(webhook, json=payload, timeout=30)
        if resp.status_code == 429:
            time.sleep(float(resp.json().get("retry_after", 2)) + 0.5)
            continue
        resp.raise_for_status()
        return
    raise RuntimeError("discord: still rate limited after 5 attempts")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not path or not path.exists():
        print("no new citations")
        return 0
    webhook = os.environ.get("DISCORD_WEBHOOK_LINK")
    if not webhook:
        print("::warning::DISCORD_WEBHOOK_LINK is not set; new citations not announced")
        return 0
    user_id = (os.environ.get("MY_DISCORD_USER_ID") or "").strip() or None

    items = json.loads(path.read_text(encoding="utf-8"))
    for item in items:
        post(webhook, format_message(item, user_id), user_id)
        time.sleep(1)  # webhooks allow ~5 messages per 2 s; stay well under
    print(f"announced {len(items)} new citation(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
