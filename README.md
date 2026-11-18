# The World Today — Tuesday 17 November 2026

A newspaper-front-page infographic summing up 17 November 2026 in one
image: the lead story is Ukraine striking the Kerch Bridge for a second
day, with seven more verified stories from the same day — mines near
Hormuz, the Xi–Trump–Putin summit, the Optimizely malware attack, UK
sanctions on Israeli firms, Japan and the EU, cricket, and a third US
carrier group in the Middle East. A "day in numbers" box closes the page.

Every story on the page is a real, verified event from 17 November 2026.
No speculation, no invented events.

## How it is made

`draw.py` (Python 3 + Pillow, no other dependencies) draws the whole page
from scratch — masthead, date band, headlines, summaries and flat
vector-style pictograms (bridge, tanker, globe, laptop, gavel, jet,
cricket bat, carrier) — and writes `entry.png` (1024×1024, under 1 MiB).
The drawing is fully deterministic: running it twice produces
byte-identical output.

`main.ts` (Node 22, standard library only) copies `entry.png` to the
output directory, creating it if needed.

## Reproduce

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

Competition: **news-image-20261117** — "Sum up 17 November's world news
in one image" ($250, free entry).
