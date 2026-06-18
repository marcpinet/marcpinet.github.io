+++
title = "Anomalies in Multivariate Time Series Benchmarks Are Mostly Univariate"
date = "2026-06-01"

[extra]
authors = "<strong>Marc Pinet</strong>, Julien Cumin, Samuel Berlemont, Dominique Vaufreydaz"
short_author = "Pinet et al."
venue = "12th MILETS Workshop @ KDD 2026"
status = "accepted"
image = "/pub_img/mostly_univariate.jpg"
featured = true
links = [
  { name = "arXiv", url = "https://arxiv.org/abs/2606.02670" },
  { name = "PDF", url = "https://arxiv.org/pdf/2606.02670" },
  { name = "HAL", url = "https://hal.science/hal-05639276" },
  { name = "DOI", url = "https://doi.org/10.48550/arXiv.2606.02670" },
  { name = "Code", url = "https://github.com/marcpinet/mtsad-benchmarks-are-mostly-univariate" },
]
tldr = "Evidence that current multivariate time series anomaly detection benchmarks don't actually test cross-channel modeling."

# Lifecycle milestones (oldest→newest): each is its own dated News line; the page/list show the
# LATEST. With milestones set, the top-level status/venue/date above are display fallbacks only.
[[extra.milestones]]
date = "2026-06-01"
status = "preprint"
venue = "Preprint, arXiv:2606.02670"

[[extra.milestones]]
date = "2026-06-15"
status = "accepted"
venue = "12th MILETS Workshop @ KDD 2026"
+++

## Abstract

Many recent multivariate time series anomaly detection (MTSAD) models incorporate cross-channel modeling, under the implicit assumption that the structure of anomalies may be spread across multiple channels. We evaluate this assumption on eight widely used public benchmarks by introducing a per-segment diagnostic framework that flags, for each labeled anomaly, whether at least one channel deviates individually from its normal history, whether the cross-channel correlation structure changes, or both. The framework shows that no cross-channel rupture occurs without an accompanying univariate deviation across a range of reasonable thresholds. A complementary metric also reveals that on six of the eight benchmarks, at least half of the labeled anomaly segments deviate univariately on 89% to 100% of their timesteps, reaching 100% on three of these datasets. To verify that our framework captures cross-channel structure when present, we construct synthetic data of phase-shifted sinusoidal channels with shared noise. Each anomalous segment is altered through one of two channel-wise corruptions that preserve the per-channel marginal distribution while breaking cross-channel structure, and our framework correctly characterizes these segments as cross-channel-only. On these data, channel-dependent (CD) models successfully exploit the cross-channel signal whereas channel-independent (CI) ones fail. The CI/CD comparison of a recent SOTA detector on real benchmarks further confirms that CD modeling brings no measurable gain. We conclude that current MTSAD benchmarks are unsuitable for validating cross-channel modeling capabilities, and we call for the development of more structurally diverse evaluation sets. The code for this study is publicly available.

## BibTeX

```bibtex
@article{Pinet2026AnomaliesIM,
  title={Anomalies in Multivariate Time Series Benchmarks Are Mostly Univariate},
  author={Marc Pinet and Julien Cumin and Samuel Berlemont and Dominique Vaufreydaz},
  year={2026},
  url={https://doi.org/10.48550/arXiv.2606.02670}
}
```
