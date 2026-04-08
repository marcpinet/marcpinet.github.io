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

# Citracer

## 📝 Description

Trace citation chains for any keyword across research papers.

Given a source PDF and a keyword, citracer parses the bibliography with GROBID, finds every occurrence of the keyword in the body, identifies the references cited near each occurrence, downloads those papers, and recursively walks the resulting citation graph. The output is an interactive HTML page.

> **Supported sources.** citracer currently resolves cited papers through three external services: [arXiv](https://arxiv.org/), [Semantic Scholar](https://www.semanticscholar.org/), and [OpenReview](https://openreview.net/) (for ICLR / TMLR papers not on arXiv). Workshop proceedings, books, and paywalled journal articles are not retrievable and appear as `unavailable` nodes in the graph.

![citracer interactive graph](readme_data/graph.png)

## ⚙️ Installation

Requirements: Python 3.10+ and Docker.

```bash
pip install -r requirements.txt
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.1
```

GROBID must be reachable on `http://localhost:8070`. Verify with `curl http://localhost:8070/api/isalive`.

A [Semantic Scholar API key](https://www.semanticscholar.org/product/api#api-key) is optional but recommended — without one the public endpoint is throttled to ~3.5s between calls. With a key, the throttle drops to 0.2s.

## 🚀 Usage

```bash
python citation_tracer.py --pdf paper.pdf --keyword "channel-independent" --depth 3
```

| Flag | Default | Description |
|---|---|---|
| `--pdf` | required | Path to the source PDF |
| `--keyword` | required | Term to trace through citations |
| `--depth` | `3` | Maximum recursion depth |
| `--details` | off | Show passages directly in node tooltips |
| `--output` | `./output/graph.html` | Output HTML file |
| `--cache-dir` | `./cache` | Local cache for PDFs and metadata |
| `--grobid-url` | `http://localhost:8070` | GROBID service URL |
| `--s2-api-key` | none | Semantic Scholar API key |
| `--context-window` | sentence-based | If set, fall back to a ±N character window for ref association |
| `--no-open` | off | Do not open the result in a browser |
| `-v, --verbose` | off | Verbose logging |

## 🎨 Output

Nodes are colored by status:

| Color | Status | Meaning |
|---|---|---|
| blue | `root` | The source PDF |
| green | `analyzed` | PDF retrieved and the keyword was found in its text |
| gray | `analyzed (no match)` | PDF retrieved and parsed, but the keyword does not appear |
| red | `unavailable` | PDF could not be retrieved |

Node size scales with the number of keyword occurrences. The interactive graph supports hover for live preview, click to pin a node, click on the legend to toggle visibility by status, and KaTeX rendering of LaTeX in passages.

## 🔍 How it works

1. **PDF parsing.** GROBID processes the PDF and returns TEI XML. citracer walks the `<body>` to reconstruct the plain text while recording the character offset of every inline `<ref type="bibr">` citation. The bibliography is extracted from `<listBibl>`. Figure-diagram paragraphs (detected by their density of mathematical Unicode characters) are skipped to avoid polluting the keyword matcher.

2. **Keyword matching.** The keyword is compiled to a flexible regex that handles morphological variants (e.g. `channel-independent` matches `channel-independence`, `channel independently`, `channelindependence`). The body is segmented into sentences with [pysbd](https://github.com/nipunsadvilkar/pySBD), and each occurrence of the keyword is associated with the references cited in the same sentence or the immediately following one.

3. **Reference resolution.** Each cited paper is resolved through the following cascade:
   1. If GROBID extracted a DOI or arXiv ID, use it directly.
   2. Otherwise, search arXiv by title (phrase first, then keyword fallback, with rapidfuzz validation).
   3. If arXiv has nothing, query Semantic Scholar with 429-aware backoff.
   4. As a last resort, search OpenReview (covers ICLR/TMLR papers not on arXiv).

   Resolved PDFs are cached in `./cache/pdfs/`.

4. **Recursion.** The tracer is a BFS that processes papers in queue order, deduplicating by canonical ID (DOI > arXiv > OpenReview > title hash). When the same PDF is reached via a second path, the new edge is added without re-parsing.

5. **Rendering.** The graph is serialized to an interactive HTML page using [pyvis](https://pyvis.readthedocs.io/), with a custom overlay for the legend filter, side info panel, keyword highlighting, and KaTeX math.

## 📁 Project structure

```
citation_tracer/
├── cli.py                  # argparse entry point
├── pdf_parser.py           # GROBID + TEI walking + figure-noise filter + pymupdf fallback
├── keyword_matcher.py      # morphological regex + sentence-based ref association
├── reference_resolver.py   # arXiv-first cascade resolver with cache
├── tracer.py               # BFS recursion with deduplication
├── visualizer.py           # pyvis rendering + custom overlay
├── models.py               # dataclasses
└── utils.py                # ID normalization, hashing, logging
```

## 🧩 Dependencies

| Package | Used for |
|---|---|
| [GROBID](https://github.com/kermitt2/grobid) | PDF structural parsing (external service) |
| [lxml](https://lxml.de/) | TEI XML processing |
| [pymupdf](https://pymupdf.readthedocs.io/) | PDF text extraction (parser fallback) |
| [arxiv](https://github.com/lukasschwab/arxiv.py) | arXiv search and download |
| [pysbd](https://github.com/nipunsadvilkar/pySBD) | Sentence boundary detection |
| [pyvis](https://pyvis.readthedocs.io/) | Interactive HTML graph rendering |
| [rapidfuzz](https://github.com/rapidfuzz/RapidFuzz) | Fuzzy title matching |
| [requests](https://requests.readthedocs.io/) | HTTP client |
| [tqdm](https://github.com/tqdm/tqdm) | Progress bar |
| [KaTeX](https://katex.org) | LaTeX math rendering in the HTML output (CDN) |

External APIs:

- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/api-docs/graph)
- [OpenReview API](https://docs.openreview.net/reference/api-v2)

## ⚠️ Limitations

- GROBID misclassifies a small fraction of references (especially sub-citations like `Liu et al., 2024b`). These are silently dropped.
- pysbd handles most academic abbreviations but can occasionally split mid-sentence; falling back to `--context-window 300` is sometimes useful.
- arXiv enforces ~3 seconds between requests, so the first run on a deep trace can take several minutes. The local cache makes subsequent runs fast.
- Only three sources are supported for resolving cited papers: [arXiv](https://arxiv.org/), [Semantic Scholar](https://www.semanticscholar.org/) and [OpenReview](https://openreview.net/). Workshop papers, books, and journal articles without an open-access PDF on one of these platforms appear as `unavailable` red nodes.

## ✍️ Authors

- Marc Pinet - *Initial work* - [marcpinet](https://github.com/marcpinet)