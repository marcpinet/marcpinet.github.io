#!/usr/bin/env python3
"""Refresh data/citations.json — who cites each publication in content/research/.

Two sources are queried and UNIONed, because they disagree in both directions:
Semantic Scholar's graph API (fast, structured) and Google Scholar via `scholarly`
(broader, but scraped and regularly blocked from datacenter IPs).

Duplicates across the two are collapsed on DOI / arXiv id / normalised title, and the
surviving record is the MOST RECENT version of the citing work (a journal version wins
over the preprint it supersedes), with any field the winner is missing backfilled from
its twin.

Failure of one source is never destructive: that source's share of the previous
data/citations.json is re-injected into the union, so a captcha'd Scholar run leaves the
site exactly as it was instead of silently halving every count.

Env:
  SEMANTIC_SCHOLAR_API_KEY  optional; the shared unauthenticated pool works fine at this
                            volume, and a key that answers 403 is dropped automatically.
  SCRAPERAPI_KEY            optional; routes Google Scholar through ScraperAPI, which is
                            the practical way to make it work from CI.
  SKIP_SCHOLAR / SKIP_S2    set to 1 to skip a source (its previous share is kept).
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
import tomllib
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = ROOT / "content" / "research"
OUT_FILE = ROOT / "data" / "citations.json"

SCHOLAR_AUTHOR_ID = "NsXT970AAAAJ"
S2_AUTHOR_ID = "2439961296"
S2_API = "https://api.semanticscholar.org/graph/v1"
S2_CITATION_FIELDS = (
    "title,year,publicationDate,venue,externalIds,url,authors,publicationTypes"
)

SCHOLAR = "scholar"
S2 = "semanticscholar"

# Wall-clock budget per source. Scholar's last-resort route is a pool of free public
# proxies, most of which are dead: without a ceiling a single bad day would keep a CI
# runner busy for hours and still commit nothing.
TIMEOUTS = {S2: int(os.environ.get("S2_TIMEOUT", 300)),
            SCHOLAR: int(os.environ.get("SCHOLAR_TIMEOUT", 900))}


def log(msg: str) -> None:
    print(msg, flush=True)


def with_deadline(fn, arg, seconds: int):
    """Run `fn(arg)` on a daemon thread and give up on it after `seconds`.

    The worker cannot be interrupted mid-request, so on timeout it is simply abandoned —
    being a daemon, it dies with the process instead of holding the run open."""
    box: dict = {}

    def run():
        try:
            box["value"] = fn(arg)
        except BaseException as exc:  # noqa: BLE001 — re-raised on the calling thread
            box["error"] = exc

    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    worker.join(seconds)
    if worker.is_alive():
        raise TimeoutError(f"no answer within {seconds}s")
    if "error" in box:
        raise box["error"]
    return box["value"]


# --------------------------------------------------------------------------- helpers


def norm_title(title: str) -> str:
    """Fold a title down to the part both sources agree on: lowercase alphanumerics."""
    folded = unicodedata.normalize("NFKD", title or "")
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", folded.lower()).strip()


def clean_arxiv(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().lower()
    value = re.sub(r"^arxiv[:/]", "", value)
    value = re.sub(r"v\d+$", "", value)
    return value or None


def clean_doi(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip().lower()
    value = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", value)
    return value or None


def date_key(entry: dict) -> str:
    """Sortable date; a bare year sorts before any dated paper of that same year."""
    if entry.get("date"):
        return entry["date"]
    if entry.get("year"):
        return f"{entry['year']:04d}-00-00"
    return "0000-00-00"


def is_preprint_venue(venue: str | None) -> bool:
    return bool(venue) and bool(
        re.match(r"^\s*(arxiv(\.org)?|corr|ssrn|biorxiv|medrxiv|hal)\s*$", venue, re.I)
    )


def cap_authors(authors: str, limit: int = 8) -> str:
    """Long author lists would dominate the citation row; cut them the way a bibliography
    would. Scholar has usually truncated its own list already."""
    parts = [a.strip() for a in (authors or "").split(",") if a.strip()]
    if len(parts) <= limit:
        return ", ".join(parts)
    return ", ".join(parts[:limit]) + ", et al."


def make_entry(
    *,
    title: str,
    authors: str = "",
    year: int | None = None,
    date: str = "",
    venue: str = "",
    url: str = "",
    doi: str | None = None,
    arxiv: str | None = None,
    source: str,
) -> dict | None:
    title = (title or "").strip()
    if not title:
        return None
    return {
        "title": title,
        "authors": cap_authors(authors),
        "year": year,
        "date": (date or "").strip(),
        "venue": (venue or "").strip(),
        "url": (url or "").strip(),
        "doi": clean_doi(doi),
        "arxiv": clean_arxiv(arxiv),
        "sources": [source],
    }


# ------------------------------------------------------------------ site publications


def read_publications() -> list[dict]:
    """Every content/research/*.md page, with whatever identifiers its links leak.

    The arXiv id and DOI are read straight out of `extra.links`, so a new paper needs no
    extra front-matter to be picked up here. `extra.s2_paper_id` / `extra.scholar_cites_id`
    are honoured as manual overrides when the automatic matching ever gets it wrong.
    """
    pubs = []
    for path in sorted(RESEARCH_DIR.glob("*.md")):
        if path.name == "_index.md":
            continue
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+", raw, re.S)
        if not match:
            continue
        front = tomllib.loads(match.group(1))
        extra = front.get("extra", {}) or {}

        arxiv = doi = None
        for link in extra.get("links", []) or []:
            url = link.get("url", "")
            if m := re.search(r"arxiv\.org/(?:abs|pdf)/([\w.\-/]+?)(?:v\d+)?(?:\.pdf)?$", url, re.I):
                arxiv = arxiv or clean_arxiv(m.group(1))
            if m := re.search(r"doi\.org/(10\.[^\s]+)$", url, re.I):
                doi = doi or clean_doi(m.group(1))

        pubs.append(
            {
                "slug": path.stem,
                "title": front.get("title", path.stem),
                "norm": norm_title(front.get("title", "")),
                "arxiv": clean_arxiv(extra.get("arxiv")) or arxiv,
                "doi": clean_doi(extra.get("doi")) or doi,
                "s2_paper_id": extra.get("s2_paper_id"),
                "scholar_cites_id": extra.get("scholar_cites_id"),
            }
        )
    return pubs


# -------------------------------------------------------------------- semantic scholar


class SemanticScholar:
    def __init__(self, api_key: str | None):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "marcpinet.fr citation sync"
        self.api_key = api_key

    def get(self, path: str, params: dict) -> dict:
        """GET with backoff. The unauthenticated pool is ~1 req/s *globally*, so 429 is
        the normal answer rather than the exception; be patient. A 403 means the key is
        dead, and the public pool is better than nothing."""
        url = f"{S2_API}/{path}"
        for attempt in range(7):
            headers = {"x-api-key": self.api_key} if self.api_key else {}
            resp = self.session.get(url, params=params, headers=headers, timeout=30)
            if resp.status_code == 403 and self.api_key:
                log("  S2: api key rejected (403), falling back to the public pool")
                self.api_key = None
                continue
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(3 * 2 ** attempt, 40))
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"semantic scholar: giving up on {path} (last {resp.status_code})")

    def author_papers(self) -> list[dict]:
        """One request for the whole profile — the per-paper endpoint is far more heavily
        throttled, so every id we can resolve from here is a request we don't make."""
        papers, offset = [], 0
        while True:
            page = self.get(
                f"author/{S2_AUTHOR_ID}/papers",
                {"fields": "title,externalIds", "limit": 100, "offset": offset},
            )
            papers.extend(page.get("data", []))
            if "next" not in page:
                return papers
            offset = page["next"]

    def lookup(self, identifier: str) -> str | None:
        try:
            return self.get(f"paper/{identifier}", {"fields": "paperId"})["paperId"]
        except (requests.HTTPError, RuntimeError, KeyError):
            return None

    def citations(self, paper_id: str) -> list[dict]:
        out, offset = [], 0
        while True:
            page = self.get(
                f"paper/{paper_id}/citations",
                {"fields": S2_CITATION_FIELDS, "limit": 100, "offset": offset},
            )
            out.extend(page.get("data", []))
            if "next" not in page:
                return out
            offset = page["next"]


def fetch_semantic_scholar(pubs: list[dict]) -> dict[str, list[dict]]:
    client = SemanticScholar(os.environ.get("SEMANTIC_SCHOLAR_API_KEY") or None)

    # One index over the author profile, keyed on every identifier it exposes.
    index: dict[str, str] = {}
    for paper in client.author_papers():
        ext = paper.get("externalIds") or {}
        keys = [f"title:{norm_title(paper.get('title', ''))}"]
        if ext.get("ArXiv"):
            keys.append(f"arxiv:{clean_arxiv(ext['ArXiv'])}")
        if ext.get("DOI"):
            keys.append(f"doi:{clean_doi(ext['DOI'])}")
        for key in keys:
            index.setdefault(key, paper["paperId"])

    results: dict[str, list[dict]] = {}
    for pub in pubs:
        paper_id = pub["s2_paper_id"]
        for key in (f"arxiv:{pub['arxiv']}", f"doi:{pub['doi']}", f"title:{pub['norm']}"):
            paper_id = paper_id or index.get(key)
        # Only if the profile knows nothing about it do we pay for a direct lookup.
        for ident in (f"arXiv:{pub['arxiv']}" if pub["arxiv"] else None,
                      f"DOI:{pub['doi']}" if pub["doi"] else None):
            paper_id = paper_id or (client.lookup(ident) if ident else None)
        if not paper_id:
            log(f"  S2: no match for {pub['slug']}")
            results[pub["slug"]] = []
            continue

        entries = []
        for item in client.citations(paper_id):
            citing = item.get("citingPaper") or {}
            ext = citing.get("externalIds") or {}
            entry = make_entry(
                title=citing.get("title", ""),
                authors=", ".join(a.get("name", "") for a in citing.get("authors") or []),
                year=citing.get("year"),
                date=citing.get("publicationDate") or "",
                venue=citing.get("venue") or "",
                url=citing.get("url") or "",
                doi=ext.get("DOI"),
                arxiv=ext.get("ArXiv"),
                source=S2,
            )
            if entry:
                entries.append(entry)
        log(f"  S2: {pub['slug']}: {len(entries)} citing papers")
        results[pub["slug"]] = entries
    return results


# --------------------------------------------------------------------- google scholar


def fetch_google_scholar(pubs: list[dict]) -> dict[str, list[dict]]:
    """Scrape Scholar, trying progressively more desperate transports.

    Google serves a captcha to anything that looks like a datacenter, and often to
    residential IPs too, so a plain request is the least likely route to work. ScraperAPI
    (a key in $SCRAPERAPI_KEY) is the only one that works reliably; the free public proxy
    pool is a slow, unreliable last resort. All of them failing is a normal outcome and
    the caller keeps the previous Scholar data.
    """
    from scholarly import ProxyGenerator, scholarly

    routes: list[tuple[str, object]] = []
    if key := os.environ.get("SCRAPERAPI_KEY"):
        routes.append(("ScraperAPI", lambda pg: pg.ScraperAPI(key)))
    routes.append(("direct", None))
    if os.environ.get("SCHOLAR_FREE_PROXIES", "1") == "1":
        routes.append(("free proxies", lambda pg: pg.FreeProxies()))

    last_error: Exception | None = None
    for label, setup in routes:
        log(f"  GS: trying {label}")
        try:
            if setup is None:
                scholarly.use_proxy(None)
            else:
                generator = ProxyGenerator()
                if not setup(generator):
                    log(f"  GS: {label} unavailable")
                    continue
                scholarly.use_proxy(generator)
            return _scrape_scholar(scholarly, pubs)
        except Exception as exc:  # noqa: BLE001 — try the next transport
            last_error = exc
            log(f"  GS: {label} failed ({exc.__class__.__name__}: {exc})")

    raise RuntimeError(f"google scholar unreachable: {last_error}")


def _scrape_scholar(scholarly, pubs: list[dict]) -> dict[str, list[dict]]:
    author = scholarly.search_author_id(SCHOLAR_AUTHOR_ID)
    author = scholarly.fill(author, sections=["publications"])
    by_title = {norm_title(p.get("bib", {}).get("title", "")): p
                for p in author.get("publications", [])}

    results: dict[str, list[dict]] = {}
    for pub in pubs:
        match = by_title.get(pub["norm"])
        if not match:
            log(f"  GS: no match for {pub['slug']}")
            results[pub["slug"]] = []
            continue
        if not match.get("num_citations"):
            results[pub["slug"]] = []
            continue

        filled = scholarly.fill(match)
        entries = []
        for citing in scholarly.citedby(filled):
            bib = citing.get("bib", {}) or {}
            authors = bib.get("author", "")
            if isinstance(authors, list):
                authors = ", ".join(authors)
            authors = authors.replace(" and ", ", ")
            year = bib.get("pub_year")
            entry = make_entry(
                title=bib.get("title", ""),
                authors=authors,
                year=int(year) if str(year).isdigit() else None,
                venue=bib.get("venue", "") or bib.get("journal", "") or "",
                url=citing.get("pub_url", "") or "",
                source=SCHOLAR,
            )
            if entry:
                entries.append(entry)
        log(f"  GS: {pub['slug']}: {len(entries)} citing papers")
        results[pub["slug"]] = entries
    return results


# ------------------------------------------------------------------------------ merge


def identity_keys(entry: dict) -> list[str]:
    keys = []
    if entry.get("doi"):
        keys.append(f"doi:{entry['doi']}")
        # An arXiv DOI and a bare arXiv id name the same object; make them collide.
        if m := re.match(r"10\.48550/arxiv\.(.+)$", entry["doi"]):
            keys.append(f"arxiv:{clean_arxiv(m.group(1))}")
    if entry.get("arxiv"):
        keys.append(f"arxiv:{entry['arxiv']}")
    if nt := norm_title(entry["title"]):
        keys.append(f"title:{nt}")
    return keys


def group_duplicates(entries: list[dict]) -> list[list[dict]]:
    """Cluster entries that share any identifier, transitively."""
    groups: list[dict] = []  # {"keys": set, "entries": list}
    index: dict[str, int] = {}

    for entry in entries:
        keys = identity_keys(entry)
        hits = sorted({index[k] for k in keys if k in index})
        if not hits:
            groups.append({"keys": set(keys), "entries": [entry]})
            for k in keys:
                index[k] = len(groups) - 1
            continue

        target = hits[0]
        groups[target]["entries"].append(entry)
        groups[target]["keys"].update(keys)
        for other in hits[1:]:
            groups[target]["entries"].extend(groups[other]["entries"])
            groups[target]["keys"].update(groups[other]["keys"])
            groups[other]["entries"] = []
            groups[other]["keys"] = set()
        for k in groups[target]["keys"]:
            index[k] = target

    return [g["entries"] for g in groups if g["entries"]]


def pick_url(ranked: list[dict]) -> str:
    """Where "Cited by" should send the reader: the paper, not a page about the paper.

    Semantic Scholar's own `url` is a landing page that merely links onward, so it ranks
    below every real destination — including an arXiv page reconstructed from an id the
    *other* source supplied. Within a tier the newest version wins, since `ranked` is
    ordered newest-first.
    """
    direct, preprint, doi, landing = [], [], [], []
    for e in ranked:
        url = e.get("url") or ""
        if url and "semanticscholar.org/paper/" not in url:
            direct.append(url)
        elif url:
            landing.append(url)
        if e.get("arxiv"):
            preprint.append(f"https://arxiv.org/abs/{e['arxiv']}")
        # An arXiv DOI just bounces through doi.org to the arXiv page above.
        if e.get("doi") and not e["doi"].startswith("10.48550/arxiv."):
            doi.append(f"https://doi.org/{e['doi']}")

    for tier in (direct, doi, preprint, landing):
        if tier:
            return tier[0]
    return ""


def collapse(group: list[dict]) -> dict:
    """One record per citing work: the newest version, backfilled from its duplicates."""
    ranked = sorted(group, key=lambda e: (date_key(e), len(e.get("venue") or "")), reverse=True)
    winner = dict(ranked[0])

    for field in ("authors", "venue", "doi", "arxiv"):
        if not winner.get(field):
            for other in ranked[1:]:
                if other.get(field):
                    winner[field] = other[field]
                    break

    # Dates are NOT freely backfillable: inheriting the preprint's day from a superseded
    # twin would file the published version under the preprint's date and undo the very
    # "newest version wins" choice made just above. Only take a date that agrees with the
    # winner's own year.
    if not winner.get("year"):
        winner["year"] = max((e["year"] for e in ranked if e.get("year")), default=None)
    if not winner.get("date"):
        for other in ranked[1:]:
            if other.get("date") and (not winner.get("year")
                                      or other["date"][:4] == str(winner["year"])):
                winner["date"] = other["date"]
                break

    # A real venue beats "arXiv.org", whichever version happened to win on date.
    if is_preprint_venue(winner.get("venue")):
        for other in ranked:
            if other.get("venue") and not is_preprint_venue(other["venue"]):
                winner["venue"] = other["venue"]
                break

    winner["url"] = pick_url(ranked)

    if not winner.get("year") and winner.get("date"):
        winner["year"] = int(winner["date"][:4])

    winner["sources"] = sorted({s for e in group for s in e.get("sources", [])})
    return winner


def merge_slug(layers: dict[str, list[dict]]) -> list[dict]:
    flat = [e for entries in layers.values() for e in entries]
    merged = [collapse(g) for g in group_duplicates(flat)]
    merged.sort(key=lambda e: (date_key(e), norm_title(e["title"])), reverse=True)
    return merged


# ------------------------------------------------------------------------------- main


def load_previous() -> dict[str, list[dict]]:
    """Previous citations, per slug — the safety net when a source is unavailable."""
    if not OUT_FILE.exists():
        return {}
    try:
        data = json.loads(OUT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {p["slug"]: p.get("citations", []) for p in data.get("papers", [])}


def main() -> int:
    pubs = read_publications()
    if not pubs:
        log("no publications found in content/research/, nothing to do")
        return 0
    log(f"{len(pubs)} publication(s): {', '.join(p['slug'] for p in pubs)}")

    previous = load_previous()
    fresh: dict[str, dict[str, list[dict]]] = {p["slug"]: {} for p in pubs}
    status: dict[str, dict] = {}

    for name, skip_env, fetch in (
        (S2, "SKIP_S2", fetch_semantic_scholar),
        (SCHOLAR, "SKIP_SCHOLAR", fetch_google_scholar),
    ):
        if os.environ.get(skip_env) == "1":
            log(f"{name}: skipped (${skip_env}=1)")
            status[name] = {"ok": False, "error": "skipped"}
            continue
        log(f"{name}: fetching...")
        try:
            for slug, entries in with_deadline(fetch, pubs, TIMEOUTS[name]).items():
                fresh.setdefault(slug, {})[name] = entries
            status[name] = {"ok": True}
        except Exception as exc:  # noqa: BLE001 — any failure must stay non-fatal
            log(f"{name}: FAILED ({exc.__class__.__name__}: {exc})")
            status[name] = {"ok": False, "error": f"{exc.__class__.__name__}: {exc}"}

    papers = []
    for pub in pubs:
        layers = dict(fresh.get(pub["slug"], {}))
        # Re-inject the previous contribution of every source that did not answer, so a
        # blocked run degrades to "unchanged" rather than to "count dropped".
        for name, st in status.items():
            if not st["ok"]:
                # Keep only this source's claim on each cached entry: if the other source
                # answered and no longer lists the paper, it should not still be credited.
                kept = [{**e, "sources": [name]}
                        for e in previous.get(pub["slug"], []) if name in e.get("sources", [])]
                if kept:
                    layers[f"previous:{name}"] = kept
                    log(f"  {pub['slug']}: kept {len(kept)} cached {name} entries")

        citations = merge_slug(layers)
        papers.append(
            {
                "slug": pub["slug"],
                "title": pub["title"],
                "count": len(citations),
                "by_source": {
                    SCHOLAR: sum(1 for c in citations if SCHOLAR in c["sources"]),
                    S2: sum(1 for c in citations if S2 in c["sources"]),
                },
                "citations": citations,
            }
        )
        log(f"{pub['slug']}: {len(citations)} unique citing paper(s)")

    # A source that failed is reported to the CI log, not written into the data: recording
    # it would rewrite the file (and so commit) on every flaky Scholar day even when not a
    # single citation changed.
    for name, st in status.items():
        if not st["ok"] and st["error"] != "skipped":
            prefix = "::warning title=Citation source unavailable::" if os.environ.get("GITHUB_ACTIONS") else "WARNING: "
            log(f"{prefix}{name} could not be reached ({st['error']}); its previous results were kept")

    payload = {
        "papers": papers,
        "total": sum(p["count"] for p in papers),
    }

    if OUT_FILE.exists():
        try:
            old = json.loads(OUT_FILE.read_text(encoding="utf-8"))
            if {k: v for k, v in old.items() if k != "generated"} == payload:
                log("unchanged, leaving data/citations.json alone")
                return 0
        except json.JSONDecodeError:
            pass

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(
        json.dumps(
            {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **payload},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    log(f"wrote {OUT_FILE.relative_to(ROOT)} ({payload['total']} citations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
