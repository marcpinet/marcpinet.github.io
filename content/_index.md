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

# Homepage "News" feed. These hand-written items are merged chronologically with your
# recent publications/projects/datasets (auto-turned into sentences) and your
# experience/education feed entries. Each line starts with a category chip. The feed
# scans everything dated >= config.extra.news_start (no upper bound); items older than
# 1 year collapse behind a "show more". Use this for things with no page of their own:
# reviewer/PC roles, talks, awards, a new position, a certification…
#
# `date`  ISO (YYYY-MM-DD); drives ordering and the show-more cutoff.
# `text`  the sentence, inline Markdown — write it first person, e.g.
#         "I'm now a **reviewer** for [NeurIPS 2026](https://…)".
# `type`  the chip label (default "misc"), e.g. "award", "service", "talk".
# `link`  optional; adds a trailing "→".
# `image` optional path under static/ (e.g. "/pub_img/foo.jpg") — shows a thumbnail.
#
# PAPER LIFECYCLE is handled on the publication itself via [[extra.milestones]] (see a
# publication .md) — each milestone is its own dated News line, so you don't need custom
# items for that. Use custom items only for things that aren't a paper/project/etc.
#
# [[extra.news]]
# date = "2026-06-02"
# type = "service"
# text = "I joined the program committee of the **NeurIPS 2026** Workshop on Time Series."
#
# [[extra.news]]
# date = "2026-05-15"
# type = "award"
# text = "I won a **best poster** award at SomeConf 2026."
# link = "https://example.com"
+++

I am currently a PhD Student (from fall 2025) working at [Orange](https://hellofuture.orange.com/fr/) and a member of the [LIG](https://www.liglab.fr/fr), advised by Prof. [Dominique Vaufreydaz](https://scholar.google.com/citations?user=asjEKYYAAAAJ), Dr. [Julien Cumin](https://scholar.google.com/citations?user=byW2uYQAAAAJ) and Dr. [Samuel Berlemont](https://www.researchgate.net/profile/Samuel-Berlemont).
