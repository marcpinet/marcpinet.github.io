+++
title = "Projects"
template = "cards.html"

# Open-source contributions: pull requests to repositories that are not mine. Rendered
# by cards.html as a collapsed dropdown above "Personal projects", newest first.
# One [[extra.contributions]] block per PR:
#   repo    "owner/name" on GitHub (required)
#   pr      PR number -> links to https://github.com/<repo>/pull/<pr>
#           Leave it out (or "" / "X") while the PR isn't opened yet: the entry then
#           shows a WIP chip and links to `link`, or to the repo.
#   link    optional, overrides the link, e.g. the fork's branch before the PR exists:
#           "https://github.com/marcpinet/VUS/tree/perf/vectorize-vus-opt"
#   title   what the PR does
#   status  "open" (shows a PENDING chip) | "merged" | "closed"; ignored for an entry
#           with no PR unless "merged"/"closed" (a patch taken without a PR)
#   date    ISO date: when it was opened (open), merged (merged) or started (no PR)
#   note    optional, inline Markdown, so links work: "See [the issue](https://...)"
# scripts/fetch_stars.py refreshes status and merge date daily into data/github_prs.json,
# which wins over `status` here: a merged PR flips to MERGED without touching this file.
# Entries with no PR number are skipped by the script.

[[extra.contributions]]
repo = "TheDatumOrg/VUS"
pr = "X"
title = "Optimized and vectorized some VUS-PR operations"
status = ""
date = "2026-11-15"
link = "https://github.com/marcpinet/VUS/tree/perf/vectorize-vus-opt"
# note = ""

[[extra.contributions]]
repo = "thedatumorg/TSB-AD"
pr = 79
title = "Fix multivariate normalization in ML detectors"
status = "merged"
date = "2026-10-07"
note = "Thanks to [Magali Parrino](https://magaliparrino.github.io/) for finding the bug!"

[[extra.contributions]]
repo = "scality/shad"
pr = 5
title = ".dropna() makes some anomalies disappear in resulting images"
status = "open"
date = "2026-10-06"
# note = ""

[[extra.contributions]]
repo = "decisionintelligence/TAB"
pr = 9
title = "Python 3.12 support"
status = "open"
date = "2026-07-21"
# note = ""
+++
