#!/usr/bin/env python3
"""Refresh data/citations.json — who cites each publication in content/research/.

Three sources are queried and UNIONed, because they disagree in every direction:
Semantic Scholar's graph API and OpenAlex (fast, structured, open, but they only see a
citation once the citing paper's reference list has been ingested) and Google Scholar
(broadest and first to index new papers, but scraped: see fetch_google_scholar).

Duplicates across the two are collapsed on DOI / arXiv id / normalised title, and the
surviving record is the MOST RECENT version of the citing work (a journal version wins
over the preprint it supersedes), with any field the winner is missing backfilled from
its twin.

Failure of one source is never destructive: that source's share of the previous
data/citations.json is re-injected into the union, so a captcha'd Scholar run leaves the
site exactly as it was instead of silently halving every count.

A source that answers but suddenly reports NO citations for a paper it previously had
some for is treated as a glitch (soft block, index hiccup) rather than believed.

Env:
  SERPAPI_KEY               recommended; Google Scholar through SerpAPI. The only route
                            that reliably gets past Scholar's captcha from CI.
  SCRAPERAPI_KEY            optional; Scholar HTML through ScraperAPI, tried next.
  SEMANTIC_SCHOLAR_API_KEY  optional; the shared unauthenticated pool works fine at this
                            volume, and a key that answers 403 is dropped automatically.
  OPENALEX_API_KEY          optional; OpenAlex's anonymous daily allowance is plenty.
  SKIP_SCHOLAR / SKIP_S2 / SKIP_OPENALEX
                            set to 1 to skip a source (its previous share is kept).
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
OPENALEX = "openalex"
SOURCES = (SCHOLAR, S2, OPENALEX)

# Wall-clock budget per source, so one hung source cannot keep the runner busy for hours
# and still commit nothing.
TIMEOUTS = {S2: int(os.environ.get("S2_TIMEOUT", 300)),
            OPENALEX: int(os.environ.get("OPENALEX_TIMEOUT", 300)),
            SCHOLAR: int(os.environ.get("SCHOLAR_TIMEOUT", 600))}


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
#
# The profile page is NOT a source of citations here, only of cluster ids. Its per-paper
# "Cited by" count is a cache Google refreshes on its own schedule (days, sometimes
# weeks), and the old implementation only followed a paper whose profile count was
# non-zero, then trusted whatever the profile said. The search page behind
# `scholar?cites=<cluster id>` is live: a newly indexed citing paper shows up there long
# before the profile catches up. So: resolve each publication to its cluster id(s) once,
# remember them in data/citations.json, and always query the `cites=` page directly.


class ScholarBlocked(RuntimeError):
    """Google answered with a captcha / rate limit instead of results."""


SCHOLAR_BASE = "https://scholar.google.com"
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/140.0 Safari/537.36")


def split_scholar_byline(line: str) -> tuple[str, str, int | None]:
    """"A Author, B Author - Venue, 2026 - publisher" → (authors, venue, year).

    The same line comes back from the HTML page and from SerpAPI's `summary`. Scholar
    truncates long parts with "…", which is left as is."""
    parts = [p.strip() for p in re.split(r"\s+-\s+", line or "")]
    authors = parts[0] if parts else ""
    middle = parts[1] if len(parts) >= 2 else ""
    year = None
    if m := re.search(r"(?:^|,\s*)((?:19|20)\d\d)\s*$", middle):
        year = int(m.group(1))
        middle = middle[: m.start()].strip(" ,")
    elif re.fullmatch(r"(?:19|20)\d\d", middle):
        year, middle = int(middle), ""
    # With only two parts the second is usually the publisher/site, not a venue.
    venue = middle if len(parts) > 2 or year else ""
    return authors.replace(" ", " "), venue, year


def join_ids(*groups) -> str:
    """Union of comma-separated cluster ids, order-stable. Ids are only ever added: when
    Scholar merges two versions of a paper the profile lists both, and a stale id still
    answers."""
    seen: list[str] = []
    for group in groups:
        for cid in re.split(r"[,\s]+", str(group or "")):
            if cid.isdigit() and cid not in seen:
                seen.append(cid)
    return ",".join(seen)


class SerpApiScholar:
    """Google Scholar through SerpAPI: they solve the captchas, we get JSON. The only
    route that works from a CI runner day after day (free tier: 250 searches/month;
    a run costs 1 + one per 20 citations per cited paper)."""

    label = "SerpAPI"

    def __init__(self, key: str):
        self.key = key
        self.session = requests.Session()

    def _get(self, params: dict) -> dict:
        resp = self.session.get("https://serpapi.com/search.json",
                                params={**params, "api_key": self.key, "hl": "en"}, timeout=60)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        error = data.get("error", "")
        # An empty result set is reported as an "error"; it is a real, valid answer.
        if error and "hasn't returned any results" in error:
            return {"organic_results": []}
        if resp.status_code != 200 or error or not data:
            raise RuntimeError(f"serpapi {resp.status_code}: {error or resp.text[:200]}")
        return data

    def profile_ids(self) -> dict[str, str]:
        out: dict[str, str] = {}
        start = 0
        while True:
            data = self._get({"engine": "google_scholar_author", "author_id": SCHOLAR_AUTHOR_ID,
                              "num": 100, "start": start})
            articles = data.get("articles", [])
            for art in articles:
                cites = (art.get("cited_by") or {}).get("cites_id")
                if cites:
                    out[norm_title(art.get("title", ""))] = cites
            if len(articles) < 100:
                return out
            start += 100

    def search_ids(self, title: str) -> str | None:
        data = self._get({"engine": "google_scholar", "q": f'"{title}"', "num": 10})
        for res in data.get("organic_results", []):
            if norm_title(res.get("title", "")) == norm_title(title):
                links = res.get("inline_links") or {}
                return join_ids((links.get("cited_by") or {}).get("cites_id"),
                                (links.get("versions") or {}).get("cluster_id")) or None
        return None

    def citing(self, cites: str) -> list[dict]:
        out, start = [], 0
        while True:
            data = self._get({"engine": "google_scholar", "cites": cites, "num": 20, "start": start})
            page = data.get("organic_results", [])
            for res in page:
                authors, venue, year = split_scholar_byline(
                    (res.get("publication_info") or {}).get("summary", ""))
                out.append({"title": res.get("title", ""), "url": res.get("link", ""),
                            "authors": authors, "venue": venue, "year": year})
            total = (data.get("search_information") or {}).get("total_results") or 0
            start += 20
            if not page or start >= total or start >= 1000:
                return out


class HtmlScholar:
    """Google Scholar's own HTML, fetched directly or through ScraperAPI. Parsed by hand
    rather than through `scholarly`, whose unpinned dependencies break it every few
    months (bibtexparser 2 removed the module it imports)."""

    def __init__(self, label: str, scraperapi_key: str | None = None):
        self.label = label
        self.scraperapi_key = scraperapi_key
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": BROWSER_UA, "Accept-Language": "en-US,en;q=0.9"})

    def _get(self, path: str, params: dict):
        from bs4 import BeautifulSoup

        url = requests.Request("GET", f"{SCHOLAR_BASE}{path}", params={**params, "hl": "en"}).prepare().url
        if self.scraperapi_key:
            resp = self.session.get("https://api.scraperapi.com/",
                                    params={"api_key": self.scraperapi_key, "url": url}, timeout=90)
        else:
            resp = self.session.get(url, timeout=30)
            time.sleep(4)  # be a slow, boring client
        html = resp.text
        if (resp.status_code in (403, 429, 503) or "/sorry/" in resp.url
                or "gs_captcha" in html or "unusual traffic" in html):
            raise ScholarBlocked(f"{self.label}: blocked ({resp.status_code})")
        resp.raise_for_status()
        return BeautifulSoup(html, "html.parser")

    def profile_ids(self) -> dict[str, str]:
        out: dict[str, str] = {}
        start = 0
        while True:
            soup = self._get("/citations", {"user": SCHOLAR_AUTHOR_ID, "cstart": start, "pagesize": 100})
            rows = soup.select("tr.gsc_a_tr")
            if start == 0 and not soup.select_one("#gsc_prf_in"):
                raise ScholarBlocked(f"{self.label}: profile page has no profile in it")
            for row in rows:
                title = row.select_one("a.gsc_a_at")
                cited = row.select_one("a.gsc_a_ac")
                if title and cited and (m := re.search(r"cites=([\d,]+)", cited.get("href", ""))):
                    out[norm_title(title.get_text())] = m.group(1)
            if len(rows) < 100:
                return out
            start += 100

    def _results(self, soup) -> list:
        if not soup.select_one("#gs_res_ccl"):
            raise ScholarBlocked(f"{self.label}: no result list on the page")
        return soup.select("div.gs_r.gs_or[data-cid]")

    def search_ids(self, title: str) -> str | None:
        soup = self._get("/scholar", {"q": f'"{title}"'})
        for res in self._results(soup):
            head = res.select_one("h3.gs_rt")
            if head:
                for tag in head.select("span.gs_ctc, span.gs_ctg2, span.gs_ct1, span.gs_ct2"):
                    tag.decompose()
                if norm_title(head.get_text()) == norm_title(title):
                    return res["data-cid"]
        return None

    def citing(self, cites: str) -> list[dict]:
        out, start = [], 0
        while True:
            soup = self._get("/scholar", {"cites": cites, "num": 20, "start": start})
            page = self._results(soup)
            for res in page:
                head = res.select_one("h3.gs_rt")
                if not head:
                    continue
                link = head.select_one("a")
                for tag in head.select("span.gs_ctc, span.gs_ctg2, span.gs_ct1, span.gs_ct2"):
                    tag.decompose()
                byline = res.select_one("div.gs_a")
                authors, venue, year = split_scholar_byline(re.sub(r"\s+", " ", byline.get_text()) if byline else "")
                out.append({"title": re.sub(r"\s+", " ", head.get_text()).strip(),
                            "url": link.get("href", "") if link else "",
                            "authors": authors, "venue": venue, "year": year})
            start += 20
            if len(page) < 20 or start >= 1000:
                return out


def scholar_routes() -> list:
    routes = []
    if key := os.environ.get("SERPAPI_KEY"):
        routes.append(SerpApiScholar(key))
    if key := os.environ.get("SCRAPERAPI_KEY"):
        routes.append(HtmlScholar("ScraperAPI", key))
    if os.environ.get("SCHOLAR_DIRECT", "1") == "1":
        routes.append(HtmlScholar("direct"))
    return routes


def fetch_google_scholar(pubs: list[dict], known_ids: dict[str, str]) -> dict[str, list[dict]]:
    """Try each transport in turn; the first that gets through does the whole run.

    From a datacenter IP (and, lately, from many residential ones too) the direct route
    is met with a captcha, so without $SERPAPI_KEY or $SCRAPERAPI_KEY a failure here is
    the expected outcome, and the caller keeps the previous Scholar data."""
    routes = scholar_routes()
    if not routes:
        raise RuntimeError("no route configured (set SERPAPI_KEY)")
    last_error: Exception | None = None
    for route in routes:
        log(f"  GS: trying {route.label}")
        try:
            return _scrape_scholar(route, pubs, known_ids)
        except Exception as exc:  # noqa: BLE001 — try the next transport
            last_error = exc
            log(f"  GS: {route.label} failed ({exc.__class__.__name__}: {exc})")
    raise RuntimeError(f"google scholar unreachable: {last_error}")


def _scrape_scholar(route, pubs: list[dict], known_ids: dict[str, str]) -> dict[str, list[dict]]:
    # The profile is only consulted to learn cluster ids (including ones added when
    # Scholar merges versions); a profile that fails to load is not fatal as long as
    # every publication already has an id.
    try:
        profile = route.profile_ids()
    except ScholarBlocked:
        if not all(known_ids.get(p["slug"]) or p["scholar_cites_id"] for p in pubs):
            raise
        profile = {}

    results: dict[str, list[dict]] = {}
    for pub in pubs:
        ids = join_ids(pub["scholar_cites_id"], known_ids.get(pub["slug"]), profile.get(pub["norm"]))
        if not ids:
            # Uncited according to the (stale) profile: ask the live search index.
            ids = join_ids(route.search_ids(pub["title"]))
        known_ids[pub["slug"]] = ids
        if not ids:
            log(f"  GS: {pub['slug']}: not found on Scholar yet")
            results[pub["slug"]] = []
            continue

        entries = []
        for hit in route.citing(ids):
            entry = make_entry(title=hit["title"], authors=hit["authors"], year=hit["year"],
                               venue=hit["venue"], url=hit["url"], source=SCHOLAR)
            if entry:
                entries.append(entry)
        log(f"  GS: {pub['slug']} (cites={ids}): {len(entries)} citing papers")
        results[pub["slug"]] = entries
    return results


# --------------------------------------------------------------------------- openalex
#
# Free, keyless, and fed by Crossref reference lists, so it tends to see journal papers
# that Semantic Scholar has not linked yet (and vice versa). A preprint and its published
# version are often separate OpenAlex works, hence every work with the exact title counts.

OPENALEX_API = "https://api.openalex.org"


def fetch_openalex(pubs: list[dict]) -> dict[str, list[dict]]:
    session = requests.Session()
    base_params = {}
    if key := os.environ.get("OPENALEX_API_KEY"):
        base_params["api_key"] = key

    def get(path: str, params: dict | None = None) -> dict | None:
        for attempt in range(5):
            resp = session.get(f"{OPENALEX_API}/{path}", params={**base_params, **(params or {})}, timeout=30)
            if resp.status_code == 404:
                return None
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 * 2 ** attempt)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"openalex: giving up on {path} ({resp.status_code})")

    results: dict[str, list[dict]] = {}
    for pub in pubs:
        work_ids: set[str] = set()
        dois = {pub["doi"], f"10.48550/arxiv.{pub['arxiv']}" if pub["arxiv"] else None}
        for doi in filter(None, dois):
            if work := get(f"works/doi:{doi}", {"select": "id"}):
                work_ids.add(work["id"].rsplit("/", 1)[-1])
        found = get("works", {"filter": f"title.search:{pub['title'].replace(',', ' ')}",
                              "select": "id,title", "per-page": 25}) or {}
        for work in found.get("results", []):
            if norm_title(work.get("title") or "") == pub["norm"]:
                work_ids.add(work["id"].rsplit("/", 1)[-1])
        if not work_ids:
            log(f"  OA: no match for {pub['slug']}")
            results[pub["slug"]] = []
            continue

        entries, cursor = [], "*"
        while cursor:
            page = get("works", {
                "filter": f"cites:{'|'.join(sorted(work_ids))}",
                "select": "id,title,doi,publication_year,publication_date,authorships,primary_location,ids",
                "per-page": 200, "cursor": cursor,
            }) or {}
            for work in page.get("results", []):
                doi = clean_doi(work.get("doi"))
                source = ((work.get("primary_location") or {}).get("source") or {})
                arxiv = None
                if doi and (m := re.match(r"10\.48550/arxiv\.(.+)$", doi)):
                    arxiv = m.group(1)
                entry = make_entry(
                    title=work.get("title") or "",
                    authors=", ".join((a.get("author") or {}).get("display_name", "")
                                      for a in work.get("authorships") or []),
                    year=work.get("publication_year"),
                    date=work.get("publication_date") or "",
                    venue=source.get("display_name") or "",
                    url=(work.get("primary_location") or {}).get("landing_page_url") or "",
                    doi=doi,
                    arxiv=arxiv,
                    source=OPENALEX,
                )
                if entry:
                    entries.append(entry)
            cursor = (page.get("meta") or {}).get("next_cursor") if page.get("results") else None
        log(f"  OA: {pub['slug']} ({','.join(sorted(work_ids))}): {len(entries)} citing papers")
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


def load_previous() -> dict[str, dict]:
    """Previous record per slug — the safety net when a source is unavailable, and the
    memory of each paper's Scholar cluster ids."""
    if not OUT_FILE.exists():
        return {}
    try:
        data = json.loads(OUT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {p["slug"]: p for p in data.get("papers", [])}


def main() -> int:
    pubs = read_publications()
    if not pubs:
        log("no publications found in content/research/, nothing to do")
        return 0
    log(f"{len(pubs)} publication(s): {', '.join(p['slug'] for p in pubs)}")

    previous = load_previous()
    cached = {slug: rec.get("citations", []) for slug, rec in previous.items()}
    # Filled in place by the Scholar fetch; seeded so a blocked run forgets nothing.
    scholar_ids = {slug: rec.get("scholar_cites_id", "") for slug, rec in previous.items()}

    fresh: dict[str, dict[str, list[dict]]] = {p["slug"]: {} for p in pubs}
    status: dict[str, dict] = {}

    for name, skip_env, fetch in (
        (S2, "SKIP_S2", fetch_semantic_scholar),
        (OPENALEX, "SKIP_OPENALEX", fetch_openalex),
        (SCHOLAR, "SKIP_SCHOLAR", lambda p: fetch_google_scholar(p, scholar_ids)),
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

    def previous_share(slug: str, name: str) -> list[dict]:
        # Keep only this source's claim on each cached entry: if another source answered
        # and no longer lists the paper, it should not still be credited.
        return [{**e, "sources": [name]} for e in cached.get(slug, []) if name in e.get("sources", [])]

    suspicious: list[str] = []
    papers = []
    for pub in pubs:
        slug = pub["slug"]
        layers = dict(fresh.get(slug, {}))
        for name in SOURCES:
            if name not in status:
                continue
            kept = []
            if not status[name]["ok"]:
                # Re-inject the previous contribution of every source that did not answer,
                # so a blocked run degrades to "unchanged" rather than to "count dropped".
                kept = previous_share(slug, name)
            elif not layers.get(name) and (kept := previous_share(slug, name)):
                # Citations do not vanish. A source that had some and now reports none is
                # far likelier soft-blocked or mid-reindex than right.
                suspicious.append(f"{name} returned nothing for {slug} (had {len(kept)})")
            if kept:
                layers[f"previous:{name}"] = kept
                log(f"  {slug}: kept {len(kept)} cached {name} entries")

        citations = merge_slug(layers)
        record = {
            "slug": slug,
            "title": pub["title"],
            "count": len(citations),
            "by_source": {name: sum(1 for c in citations if name in c["sources"]) for name in SOURCES},
            "citations": citations,
        }
        if scholar_ids.get(slug):
            record["scholar_cites_id"] = scholar_ids[slug]
        papers.append(record)
        log(f"{slug}: {len(citations)} unique citing paper(s) "
            f"({', '.join(f'{k} {v}' for k, v in record['by_source'].items())})")

    # A source that failed is reported to the CI log, not written into the data: recording
    # it would rewrite the file (and so commit) on every flaky Scholar day even when not a
    # single citation changed.
    prefix = "::warning title=Citation source unavailable::" if os.environ.get("GITHUB_ACTIONS") else "WARNING: "
    for name, st in status.items():
        if not st["ok"] and st["error"] != "skipped":
            log(f"{prefix}{name} could not be reached ({st['error']}); its previous results were kept")
    for note in suspicious:
        log(f"{prefix}{note}; previous results were kept")

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
