+++
title = "Anomalies in Multivariate Time Series Benchmarks Are Mostly Univariate"
date = "2026-08-10"
template = "talk.html"

[extra]
venue = "KDD 2026, Mining and Learning from Time Series Workshop (MILETS)"
location = "Jeju, South Korea"
kind = "contributed"
status = "upcoming"
when = "10 August 2026 at 15:30 KST"
period = "Aug 2026"
image = "/pub_img/kdd.png"
logo = true
tldr = "Contributed talk on why today's MTSAD benchmarks can't validate cross-channel modeling."
links = [
  { name = "Paper", url = "/research/anomalies-mtsad-univariate/" },
  { name = "Workshop", url = "https://kdd-milets.github.io/milets2026/" },
  { name = "Camera-ready", url = "https://kdd-milets.github.io/milets2026/accepted%20papers/1camera_ready_paper_anomalies_mostly_univariate.pdf" },
  { name = "arXiv", url = "https://arxiv.org/abs/2606.02670" },
  { name = "Code", url = "https://github.com/marcpinet/mtsad-benchmarks-are-mostly-univariate" },
]

# Slide deck rendered by templates/talk.html. Files live in static/<dir>/:
#   slide-01.webp … slide-NN.webp (1600px wide) + thumbs/slide-NN.webp (360px wide).
# `appendix_from` = index of the first backup slide (optional).
[extra.slides]
dir = "/talks/milets-kdd-2026"
count = 28
appendix_from = 17
pdf = "/talks/milets-kdd-2026/milets-kdd-2026-slides.pdf"
pptx = "/talks/milets-kdd-2026/milets-kdd-2026-slides.pptx"

[[extra.milestones]]
date = "2026-07-30"
status = "upcoming"
venue = "KDD 2026, Mining and Learning from Time Series Workshop (MILETS)"
+++

Contributed talk at the 12th [Mining and Learning from Time Series](https://kdd-milets.github.io/milets2026/) workshop,
co-located with [KDD 2026](https://kdd2026.kdd.org/) in Jeju, South Korea.

Many recent multivariate time series anomaly detection models model cross-channel dependencies, assuming
the anomalies in our benchmarks actually carry cross-channel structure. The talk walks through the
per-segment diagnostic framework we use to test that assumption on eight public benchmarks, the synthetic
sanity check that shows the framework *does* catch cross-channel-only anomalies when they exist, and what
follows for how we should be evaluating these models.

Slides 17 onwards are the backup slides used during questions.
