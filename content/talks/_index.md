+++
title = "Talks"
render = false
sort_by = "date"

# Add a talk as content/talks/<slug>.md with frontmatter:
#   title, date (ISO), [extra]: venue, status (accepted / given / invited / upcoming),
#   link? (slides or recording), image? (thumbnail; `logo = true` to show it whole).
# `kind` (default "contributed") decides whether the talk counts as SERVICE: only
#   invited / keynote / panel show under Talks on the Service page. A contributed talk —
#   presenting your own accepted paper — stays off that page; it still gets its own page,
#   a News line, and a link from the publication.
# Optional lifecycle [[extra.milestones]] { date, status, venue } — like publications,
#   each milestone is its own dated News line (e.g. accepted → given); page/list show the latest.
#
# SLIDE DECK — add `template = "talk.html"` and an [extra.slides] table to give the talk its
# own page with an in-browser deck viewer (the Service list and the News line then link there
# instead of to `link`):
#   [extra.slides]
#   dir = "/talks/<slug>"       # static/<dir>/slide-01.webp … slide-NN.webp (1600px wide)
#   count = 28                  #      + static/<dir>/thumbs/slide-NN.webp  (360px wide)
#   appendix_from = 17          # optional: first backup slide
#   pdf  = "/talks/<slug>/....pdf"    # optional download
#   pptx = "/talks/<slug>/....pptx"   # optional download
# Slides are pre-rendered images (no PDF/Office runtime in the browser). To regenerate from a
# .pptx on Windows, export slides as PNG from PowerPoint (File > Export, 1920x1080) and
# downscale to WebP; see the talk page in git history for the sizes used.
+++
