+++
title = "Home"
template = "index.html"

[extra]
name = "Marc Pinet"
photo = "/homepage/me.jpg"

interests = [
    "Machine Learning",
    "Deep Learning",
    "Time Series Analysis",
    "Anomaly Detection",
    "Anomaly Explanation",
    "Large Language Models (LLMs)",
]

# Homepage "News" feed. Hand-written items shown here are merged chronologically
# with your most recent publications/projects/datasets (which are turned into
# sentences automatically — "I released X", "I published X in Y"). Everything older
# than ~6 months disappears on its own (window = news_window_days in config.toml).
# Use this for things that have no page of their own: papers accepted, reviewer/PC
# roles, posters, talks, a new position, a certification…
#
# `date` is ISO (YYYY-MM-DD) and drives both ordering and the 6-month cutoff.
# `text` is the sentence to show, as inline Markdown — write it first person to
#   match the auto items, e.g. "I'm now a **reviewer** for [NeurIPS 2026](https://…)".
# `link` is optional and adds a trailing "→".
#
# PAPER LIFECYCLE: a publication shows ONE auto line, built from its CURRENT `status`
# + `date`. When a paper moves on (preprint → accepted → published), bump its `date`
# (in the publication's own .md) to the new milestone's date so the line shows on the
# right date. To ALSO keep the earlier step visible, add it here as a custom item with
# its own date — both coexist in the feed until each ages past the 6-month window.
#
# [[extra.news]]
# date = "2026-06-02"
# text = "I joined the program committee of the **NeurIPS 2026** Workshop on Time Series."
#
# [[extra.news]]
# date = "2026-05-15"
# text = "Our paper was accepted as a **poster** at SomeConf 2026."
# link = "https://example.com"
+++

I am currently a PhD Student (from fall 2025) working at [Orange](https://hellofuture.orange.com/fr/) and a member of the [LIG](https://www.liglab.fr/fr), advised by Prof. [Dominique Vaufreydaz](https://scholar.google.com/citations?user=asjEKYYAAAAJ), Dr. [Julien Cumin](https://scholar.google.com/citations?user=byW2uYQAAAAJ) and Dr. [Samuel Berlemont](https://www.researchgate.net/profile/Samuel-Berlemont).
