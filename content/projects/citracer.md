+++
title = "Citracer"
description = "💬 Given a source PDF and a keyword, citracer parses the bibliography with GROBID, finds every occurrence of the keyword in the body, identifies the references cited near each occurrence, downloads those papers, and recursively walks the resulting citation graph. The output is an interactive HTML page."
date = "2026-04-08"
weight = 1

[extra]
remote_image = "/citracer/img.png"
github_link = "https://github.com/marcpinet/citracer"
pinned = true
pin_order = 1
+++

<style>
/* GitHub Alert Styles */
.github-alert {
    border-radius: 6px;
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid;
}

.github-alert-note {
    background-color: #ddf4ff;
    border-color: #0969da;
}

.github-alert-tip {
    background-color: #dcfce7;
    border-color: #1a7f37;
}

.github-alert-important {
    background-color: #f3e8ff;
    border-color: #8250df;
}

.github-alert-warning {
    background-color: #fff8dc;
    border-color: #d1242f;
}

.github-alert-caution {
    background-color: #ffebee;
    border-color: #d1242f;
}

/* Table Wrapper */
.table-wrapper {
    overflow-x: auto;
    margin: 16px 0;
}

.table-wrapper table {
    width: 100%;
    border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
    border: 1px solid #d1d5da;
    padding: 8px 12px;
    text-align: left;
}

.table-wrapper th {
    font-weight: 600;
}

/* Video Styles */
video {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 16px 0;
}

/* Code Block Styles */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
}

code {
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Liberation Mono', 'Consolas', monospace;
    font-size: 85%;
    color: #24292f;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Dark mode support for inline code */
@media (prefers-color-scheme: dark) {
    pre {
        background-color: #161b22;
        color: #f0f6fc;
    }
    
    code {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    pre code {
        background-color: transparent;
        color: inherit;
    }
}
</style>

![citracer logo](https://raw.githubusercontent.com/marcpinet/citracer/main/readme_data/banner.png)

# citracer

<video controls style="max-width: 100%; height: auto;">
    <source src="https://github.com/user-attachments/assets/36855b62-a9ab-4404-90c3-9ac7f418899c" type="video/mp4">
    Your browser does not support the video tag. <a href="https://github.com/user-attachments/assets/36855b62-a9ab-4404-90c3-9ac7f418899c">View video</a>
</video>

## 📝 Description

Trace citation chains for any keyword across research papers.

Given a source PDF and a keyword, citracer parses the bibliography with GROBID, finds every occurrence of the keyword in the body, identifies the references cited near each occurrence, downloads those papers, and recursively walks the resulting citation graph. The output is an interactive HTML page.

> **Supported sources.** citracer currently resolves cited papers through three external services: [arXiv](https://arxiv.org/), [Semantic Scholar](https://www.semanticscholar.org/), and [OpenReview](https://openreview.net/) (for ICLR / TMLR papers not on arXiv). Workshop proceedings, books, and paywalled journal articles are not retrievable and appear as `unavailable` nodes in the graph.

![citracer interactive graph](https://raw.githubusercontent.com/marcpinet/citracer/main/readme_data/graph.png)

## ⚙️ Installation

Requirements: Python 3.10+ and Docker.

### From PyPI (recommended)

```bash
pip install citracer
docker pull lfoppiano/grobid:0.9.0
docker run --rm -p 8070:8070 lfoppiano/grobid:0.9.0
```

After `pip install citracer`, the `citracer` command is available globally on your `PATH`. You can then run it from anywhere in your terminal:

```bash
citracer --pdf paper.pdf --keyword "your keyword"
```

### From source (for development)

```bash
git clone https://github.com/marcpinet/citracer
cd citracer
pip install -e .
docker run --rm -p 8070:8070 lfoppiano/grobid:0.9.0
```

GROBID must be reachable on `http://localhost:8070`. Verify with `curl http://localhost:8070/api/isalive`.

A [Semantic Scholar API key](https://www.semanticscholar.org/product/api#api-key) is optional but recommended. Without one the public endpoint is throttled to ~3.5s between calls. With a key, the throttle drops to ~1.1s (safely under the 1 req/sec limit advertised by Semantic Scholar).

The key can be provided in three ways, in order of precedence:

1. `--s2-api-key <key>` as a CLI flag
2. `S2_API_KEY` environment variable in your shell
3. A persistent **user config** at `~/.citracer/config.json`, set once via:

   

```bash
   citracer config set-s2-key <your-key>
   ```

   Other config commands: `citracer config show`, `citracer config get-s2-key` (masked), `citracer config clear-s2-key`, `citracer config path`. The file is created with mode `600` on POSIX so other local users can't read it.

4. A `.env` file at the project root (copy `.env.example` and fill it in):

   ```
   S2_API_KEY=your_key_here
   ```

   The `.env` file is git-ignored.

If none of these are set, the unauthenticated public endpoint is used as fallback (much slower, frequent 429 backoffs).

## 🚀 Usage

After `pip install citracer` the `citracer` command is on your `PATH`. The examples below use it directly. If you cloned the repo instead, use `python -m citracer` in place of `citracer`.
```bash

# From a local PDF
citracer --pdf test_data/crossad.pdf --keyword "channel-independent" --depth 5

# From an arXiv id (auto-downloads the root PDF)
citracer --arxiv 2211.14730 --keyword "self-attention"

# From a DOI or URL
citracer --doi 10.48550/arxiv.2211.14730 --keyword "patching"
citracer --url https://openreview.net/forum?id=cGDAkQo1C0p --keyword "instance normalization"

# Multi-keyword tracing (union by default, --match-mode all for intersection)
citracer --pdf paper.pdf --keyword "channel-independent" --keyword "patching"

# Reverse trace: find papers that cite the source while mentioning the keyword

# in their citation context. No PDF downloads, pure S2 metadata. Limit is optional.
citracer --arxiv 2211.14730 --keyword "channel-independent" --reverse --reverse-limit 500

# Export the graph for downstream analysis
citracer --pdf paper.pdf --keyword "..." --export out/graph.json --export out/graph.graphml

```

### Source (exactly one required)

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Flag</p></th><th><p>Description</p></th></tr>
</thead>
<tbody>
<tr><td><p><code>--pdf</code></p></td><td><p>Path to a local source PDF</p></td></tr>
<tr><td><p><code>--doi</code></p></td><td><p>DOI of the source paper (e.g. <code>10.48550/arxiv.2211.14730</code>). Generic DOIs are resolved via Semantic Scholar</p></td></tr>
<tr><td><p><code>--arxiv</code></p></td><td><p>arXiv id of the source paper (e.g. <code>2211.14730</code>). Downloaded directly from arxiv.org</p></td></tr>
<tr><td><p><code>--url</code></p></td><td><p>URL of the source paper (arxiv.org, doi.org, or openreview.net)</p></td></tr>
</tbody>
</table>
</div>

### Trace options

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Flag</p></th><th><p>Default</p></th><th><p>Description</p></th></tr>
</thead>
<tbody>
<tr><td><p><code>--keyword</code></p></td><td><p><em>required</em></p></td><td><p>Term to trace through citations. <strong>Repeat</strong> to trace multiple keywords at once</p></td></tr>
<tr><td><p><code>--match-mode</code></p></td><td><p><code>any</code></p></td><td><p>In multi-keyword mode, <code>any</code> marks a paper as matched if at least one keyword appears; <code>all</code> requires every keyword to appear at least once</p></td></tr>
<tr><td><p><code>--depth</code></p></td><td><p><code>3</code></p></td><td><p>Maximum recursion depth</p></td></tr>
<tr><td><p><code>--context-window</code></p></td><td><p>sentence-based</p></td><td><p>If set, fall back to a ±N character window for ref association instead of sentence-based</p></td></tr>
<tr><td><p><code>--consolidate</code></p></td><td><p>off</p></td><td><p>Ask GROBID to consolidate each bibliographic reference against CrossRef (more accurate titles/DOIs but ~2-5s extra per PDF)</p></td></tr>
<tr><td><p><code>--grobid-workers</code></p></td><td><p><code>4</code></p></td><td><p>Number of concurrent GROBID parse requests per BFS level</p></td></tr>
<tr><td><p><code>--grobid-url</code></p></td><td><p><code>http://localhost:8070</code></p></td><td><p>GROBID service URL</p></td></tr>
<tr><td><p><code>--s2-api-key</code></p></td><td><p>none</p></td><td><p>Semantic Scholar API key (see Installation for priority order)</p></td></tr>
<tr><td><p><code>--reverse</code></p></td><td><p>off</p></td><td><p>Reverse trace: instead of walking down the source paper's bibliography, walk UP to papers that cite it. Filters citations by matching the keyword against <a href="https://api.semanticscholar.org/api-docs/graph">Semantic Scholar citation contexts</a> (the 1-2 sentences around each citation), so no PDFs are downloaded. Default <code>--depth</code> remains 1 in this mode</p></td></tr>
<tr><td><p><code>--reverse-limit</code></p></td><td><p><code>500</code></p></td><td><p>Max number of citing papers to fetch per level in reverse mode. Protects against runaway expansion on papers with thousands of citations</p></td></tr>
</tbody>
</table>
</div>

### Output

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Flag</p></th><th><p>Default</p></th><th><p>Description</p></th></tr>
</thead>
<tbody>
<tr><td><p><code>--output</code></p></td><td><p><code>./output/graph.html</code></p></td><td><p>Output HTML file</p></td></tr>
<tr><td><p><code>--export</code></p></td><td><p>none</p></td><td><p>Export the graph to a file. Format is derived from the extension: <code>.json</code> for the citracer JSON format, <code>.graphml</code> for the standard GraphML (Gephi, networkx, yEd). Repeat to export multiple formats</p></td></tr>
<tr><td><p><code>--details</code></p></td><td><p>off</p></td><td><p>Show passages directly in node tooltips</p></td></tr>
<tr><td><p><code>--cache-dir</code></p></td><td><p><code>./cache</code></p></td><td><p>Local cache for PDFs and metadata (SQLite)</p></td></tr>
<tr><td><p><code>--no-open</code></p></td><td><p>off</p></td><td><p>Do not open the result in a browser</p></td></tr>
<tr><td><p><code>-v, --verbose</code></p></td><td><p>off</p></td><td><p>Verbose logging</p></td></tr>
</tbody>
</table>
</div>

## 🎨 Output

Nodes are colored by status:

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Color</p></th><th><p>Status</p></th><th><p>Meaning</p></th></tr>
</thead>
<tbody>
<tr><td><p>blue</p></td><td><p><code>root</code></p></td><td><p>The source PDF</p></td></tr>
<tr><td><p>green</p></td><td><p><code>analyzed</code></p></td><td><p>PDF retrieved and the keyword was found in its text</p></td></tr>
<tr><td><p>gray</p></td><td><p><code>analyzed (no match)</code></p></td><td><p>PDF retrieved and parsed, but the keyword does not appear</p></td></tr>
<tr><td><p>red</p></td><td><p><code>unavailable</code></p></td><td><p>PDF could not be retrieved</p></td></tr>
</tbody>
</table>
</div>

Edges come in two flavors:

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Style</p></th><th><p>Type</p></th><th><p>Meaning</p></th></tr>
</thead>
<tbody>
<tr><td><p>solid dark</p></td><td><p>keyword-associated</p></td><td><p>Paper A cites paper B in the same sentence (or the next) as a keyword occurrence</p></td></tr>
<tr><td><p>dashed blue</p></td><td><p>bibliographic link</p></td><td><p>Paper A's bibliography also references paper B, independently of where the keyword appears. Hidden by default, toggle via the legend</p></td></tr>
</tbody>
</table>
</div>

### Interactive controls

A control panel in the top-left corner of the graph lets you tune the view on the fly:

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Control</p></th><th><p>Options</p></th><th><p>Effect</p></th></tr>
</thead>
<tbody>
<tr><td><p><strong>layout</strong></p></td><td><p>Sugiyama (by year) <em>(default)</em><br>Sugiyama (by depth)<br>Force-directed (BarnesHut)<br>Fruchterman-Reingold (approx)</p></td><td><p>Switches the layout algorithm. Sugiyama-by-year places the oldest papers at the top, making it easy to spot which paper first introduced the concept</p></td></tr>
<tr><td><p><strong>node size</strong></p></td><td><p>in-graph citations <em>(default)</em><br>keyword hits</p></td><td><p><code>in-graph citations</code> scales node size with the number of incoming edges visible in the graph (so nodes get bigger/smaller as you toggle bibliographic links). <code>keyword hits</code> scales by the count of keyword occurrences in the paper's body</p></td></tr>
<tr><td><p><strong>spread</strong></p></td><td><p>slider (0.3× to 3.0×)</p></td><td><p>Rescales all node positions from the graph's centroid, stretching or compressing the layout without deforming it. Works with any layout mode</p></td></tr>
<tr><td><p><strong>nodes (legend)</strong></p></td><td><p>click rows to toggle</p></td><td><p>Hide/show nodes by status</p></td></tr>
<tr><td><p><strong>edges (legend)</strong></p></td><td><p>click rows to toggle</p></td><td><p>Hide/show edges by type (keyword-associated vs. bibliographic link)</p></td></tr>
</tbody>
</table>
</div>

Other interactive features:

- **Hover** any node → side panel updates live with title, authors, year, status, keyword hits (with highlighted occurrences) and a collapsible **abstract** section when available
- **Search** box in the control panel → fuzzy match by title or author, click a result to focus-and-pin the matching node
- **Click** a node → pins the panel; a blue border is drawn around the node to show the pinned state. The pin survives clicks on the empty canvas, hover on other nodes, and pan/zoom. It's only released by clicking the same node again, pressing the × close button on the info panel, or picking **Unpin** from the right-click menu
- **Right-click** any node → context menu with **Hide** (permanently hides the node until you click the "show N manually hidden" banner in the legend), **Pin/Unpin**, and **Open link** (opens the arxiv/OpenReview/DOI page in a new tab)
- **Drag** any node anywhere. After initial placement the layout is released, so nothing snaps back
- **`show N more`** in a panel with many hits → expands the full list
- **LaTeX math** in passages is rendered with [KaTeX](https://katex.org) (`$...$`, `$$...$$`, `\(...\)`, `\[...\]`)
- **Automatic state persistence**. Node positions, filters, pin state, dropdowns, spread slider and manually hidden nodes are all saved to `localStorage` keyed on a hash of the node-id set. A browser refresh restores the exact view you had. A new trace with a different paper set gets a fresh slate. The **reset saved state** link at the bottom of the legend clears everything and reloads. A 💾 icon appears next to the reset link while state is present

## 🔍 How it works

1. **PDF parsing.** GROBID processes the PDF and returns TEI XML. citracer walks the `<body>` to reconstruct the plain text while recording the character offset of every inline `<ref type="bibr">` citation. The bibliography is extracted from `<listBibl>`. Figure-diagram paragraphs (detected by their density of mathematical Unicode characters) are skipped to avoid polluting the keyword matcher. Paragraphs that GROBID splits mid-sentence around narrative citations (a common pattern around `"Since Smith et al. (2020) and Jones et al. (2021) have shown..."`) are glued back together with a length-preserving regex so sentence-based matching still sees the refs and the keyword together.

2. **Inline ref recovery.** GROBID occasionally misses narrative citations like `DLinear Zeng et al. (2023)`, especially when the author name isn't preceded by a parenthesis. A supplementary pass scans the text for canonical author-year patterns (`Surname et al. (Year)`, `Surname & Other (Year)`, `Surname (Year)`) and adds them as inline refs whenever the `(surname, year)` signature matches a unique bibliography entry. In typical ML papers this recovers dozens of refs per document.

3. **Keyword matching.** The keyword is compiled to a flexible regex that handles morphological variants (e.g. `channel-independent` matches `channel-independence`, `channel independently`, `channelindependence`). The body is segmented into sentences with [pysbd](https://github.com/nipunsadvilkar/pySBD), and each occurrence of the keyword is associated with the references cited in the same sentence or the immediately following one.

4. **Reference resolution.** Each cited paper is resolved through the following cascade:
   1. If GROBID extracted a DOI or arXiv ID, use it directly.
   2. Otherwise, search arXiv by title (phrase first, then keyword fallback, with rapidfuzz validation).
   3. If arXiv has nothing, query Semantic Scholar with 429-aware backoff.
   4. As a last resort, search OpenReview (covers ICLR/TMLR papers not on arXiv).

   Resolved PDFs are cached in `./cache/pdfs/`.

5. **Recursion.** The tracer is a BFS that processes papers in queue order. Each level's PDFs are parsed in parallel via a thread pool (`--grobid-workers`, default 4), and the reference resolves inside a single paper are also parallelized. Deduplication uses a canonical ID (DOI > arXiv > OpenReview > title hash). When the same PDF is reached via a second path, the new edge is added without re-parsing. Years from bibliography entries can backfill a node's year when older (e.g. a preprint v1 2022 takes precedence over a publication year 2023), but only within a ±2 year window of the first year we ever saw for that node. This prevents cascading from parser mistakes.

6. **Cross-graph bibliographic links.** After the recursive trace is complete, a post-processing pass scans every parsed paper's bibliography against every other node in the graph and adds dashed "bibliographic link" edges for pairs that cite each other but not in the keyword's neighborhood. Matching is exact on DOI/arXiv IDs and fuzzy (rapidfuzz, threshold 88) on titles. No external API calls are needed: everything runs on the already-in-memory graph, so the cost is negligible.

7. **Rendering.** The graph is serialized to an interactive HTML page using [pyvis](https://pyvis.readthedocs.io/), with a custom overlay providing the layout/size/spread controls, the legend filters, the side info panel, keyword highlighting, and KaTeX math.

### Reverse trace mode (`--reverse`)

The forward algorithm walks DOWN from a root paper into its bibliography. `--reverse` walks UP: "who cites this paper, and which of them mention the keyword in their citation context?".

The key trick is that Semantic Scholar's `/paper/{id}/citations` endpoint returns a `contexts` field for each citing paper: an array of 1-2 sentence snippets around every place that paper cites the source. We apply the same morphological keyword regex to those snippets locally. A paper whose citation contexts don't contain the keyword is rejected without downloading anything. A paper with a matching context is added to the graph with the snippet as its `keyword_hits`, plus its title/authors/year/arxiv-id from S2 metadata. No GROBID call, no arXiv download.

For a paper with 2000+ citations, this runs in ~10-30 seconds and typically surfaces 20-100 relevant papers, depending on how specific the keyword is. Deep recursion (`--depth > 1`) is supported but capped per-level by `--reverse-limit` because each level can multiply the number of S2 calls.

Caveats: reverse trace depends entirely on S2 being reachable and having indexed the citation contexts (they come from S2's own PDF processing pipeline). Papers S2 doesn't know about won't appear. The resulting graph has no cross-graph bibliographic links because we never parse the citing papers' bibliographies.

## 📁 Project structure
```
citracer/
├── cli.py

# argparse entry point + GROBID health check + .env loader
├── pdf_parser.py

# GROBID + TEI walking + figure-noise filter + paragraph merge + narrative ref supplementation + pymupdf fallback
├── keyword_matcher.py

# morphological regex + sentence-based ref association (pysbd)
├── reference_resolver.py

# arXiv-first cascade resolver (arxiv → S2 → OpenReview) with SQLite cache
├── source_resolver.py

# routes --pdf / --doi / --arxiv / --url inputs to a local PDF path
├── metadata_cache.py

# SQLite-backed key/value store for resolver metadata, thread-safe
├── cross_citation.py

# post-trace pass that adds dashed bibliographic-only edges between graph nodes
├── tracer.py

# BFS recursion with parallel parsing, deduplication, year anchoring
├── visualizer.py

# pyvis rendering pipeline
├── exporter.py

# GraphML / JSON export
├── models.py

# dataclasses
├── api_types.py

# TypedDicts for arxiv / Semantic Scholar / OpenReview payloads
├── constants.py

# every tunable threshold and timeout, in one place
├── utils.py

# ID normalization, hashing, tqdm-safe logging setup
└── templates/
    └── overlay.html.tmpl

# the interactive control panel (HTML/CSS/JS) injected into the pyvis output

```

## 🧩 Dependencies

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Package</p></th><th><p>Used for</p></th></tr>
</thead>
<tbody>
<tr><td><p><a href="https://github.com/kermitt2/grobid">GROBID</a></p></td><td><p>PDF structural parsing (external service)</p></td></tr>
<tr><td><p><a href="https://lxml.de/">lxml</a></p></td><td><p>TEI XML processing</p></td></tr>
<tr><td><p><a href="https://pymupdf.readthedocs.io/">pymupdf</a></p></td><td><p>PDF text extraction (parser fallback)</p></td></tr>
<tr><td><p><a href="https://github.com/lukasschwab/arxiv.py">arxiv</a></p></td><td><p>arXiv search and download</p></td></tr>
<tr><td><p><a href="https://github.com/nipunsadvilkar/pySBD">pysbd</a></p></td><td><p>Sentence boundary detection</p></td></tr>
<tr><td><p><a href="https://pyvis.readthedocs.io/">pyvis</a></p></td><td><p>Interactive HTML graph rendering</p></td></tr>
<tr><td><p><a href="https://github.com/rapidfuzz/RapidFuzz">rapidfuzz</a></p></td><td><p>Fuzzy title matching</p></td></tr>
<tr><td><p><a href="https://requests.readthedocs.io/">requests</a></p></td><td><p>HTTP client</p></td></tr>
<tr><td><p><a href="https://github.com/tqdm/tqdm">tqdm</a></p></td><td><p>Progress bar</p></td></tr>
<tr><td><p><a href="https://github.com/theskumar/python-dotenv">python-dotenv</a></p></td><td><p>Loading the Semantic Scholar key from a <code>.env</code> file</p></td></tr>
<tr><td><p><a href="https://katex.org">KaTeX</a></p></td><td><p>LaTeX math rendering in the HTML output (CDN)</p></td></tr>
<tr><td><p><a href="https://visjs.github.io/vis-network/docs/network/">vis-network</a></p></td><td><p>Interactive network rendering (via pyvis, CDN)</p></td></tr>
</tbody>
</table>
</div>

External APIs:

- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/api-docs/graph)
- [OpenReview API](https://docs.openreview.net/reference/api-v2)

## ⚠️ Limitations

- GROBID misclassifies a small fraction of references, in particular sub-citations with letter suffixes like `Liu et al., 2024b`, which the supplementation pass can't disambiguate. These are silently dropped.
- The narrative-citation supplementation pass skips ambiguous `(surname, year)` signatures (e.g. two different Zhou 2022 papers in the bibliography). These missed cases are rare but do happen in survey-heavy papers.
- pysbd handles most academic abbreviations but can occasionally split mid-sentence; falling back to `--context-window 300` is sometimes useful.
- arXiv enforces ~3 seconds between requests, so the first run on a deep trace can take several minutes. The local cache makes subsequent runs fast.
- Only three sources are supported for resolving cited papers: [arXiv](https://arxiv.org/), [Semantic Scholar](https://www.semanticscholar.org/) and [OpenReview](https://openreview.net/). Workshop papers, books, and journal articles without an open-access PDF on one of these platforms appear as `unavailable` red nodes.
- The "Fruchterman-Reingold" layout option is implemented via vis.js's `forceAtlas2Based` solver, which is the closest approximation available natively. A proper Kamada-Kawai implementation isn't offered because vis.js doesn't ship one.

## 🧪 Development
```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

The test suite is hermetic, with no GROBID and no network. GROBID output is
exercised via a pre-baked TEI fixture in `tests/fixtures/sample.tei.xml`,
and every external API (arXiv, Semantic Scholar, OpenReview, PDF downloads)
is mocked. Runs in under a second.

CI runs the suite on Python 3.10 / 3.11 / 3.12 via GitHub Actions on every
push to `main`, every pull request, and on manual dispatch from the Actions
tab. See `.github/workflows/tests.yml`.

## ✍️ Authors

- Marc Pinet - *Initial work* - [marcpinet](https://github.com/marcpinet)