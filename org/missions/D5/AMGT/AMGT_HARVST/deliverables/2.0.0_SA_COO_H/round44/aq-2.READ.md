# HVST-aq-2 -- FWD-5 READ (round 44), `2.0.0_SA_COO~H`, 2026-10-04

**FWD-5 DONE WHEN:** "an analyst has opened a company's timeline, picked a day, and read the articles behind it listed strongest
first". **ACCEPT:** "clicking any day shows the articles behind that day, strongest first".

**Verdict: PASS** (to be graded as judgment at L9). 6 days read on 2 names, 0 order violations.

## What "strongest first" means in the served order

The served day route (`opal-amgt-scoped-api`, `GET /security/{key}/timeline/day/{date}`) lists the articles through
`lib/research/harvest/timeline_api.get_timeline_day` -> `_serve_dissection`. That function sorts by `_dissection_sort_key` =
**(signal_tier A < B < C < D, mention_count DESC, published_utc earliest first)**. So the order is:
1. articles where the company is the subject (tier A) come first, then B, C and D;
2. within a tier, the article that names the company more often comes first;
3. ties go to the earlier publication.
The tier outranks the mention count: on NVDA 2026-01-15 a tier-B article with 2 mentions is listed before a tier-C article with 3.
The day's articles come from the gold `article_security_mention` rows whose UTC publication day is that date.

## The reads (`aq-2.timeline_order.py`, `.out`, `.json`)

For each name, the 3 days with the most gold mention rows (each >= 5) were picked, and each day was confirmed on the served
timeline series (`articles_total`). Every listed article was joined to its gold row by (article_key, security_key).

| name | day | served | gold rows that day | tier sequence served | order violations |
|---|---|---|---|---|---|
| BA_US_Equity | 2026-09-29 | 9 | 9 | AAAAAAACC | 0 |
| BA_US_Equity | 2026-09-28 | 7 | 7 | AAAAACD | 0 |
| BA_US_Equity | 2026-07-20 | 7 | 7 | AAAAACC | 0 |
| NVDA_US_Equity | 2026-01-15 | 8 | 8 | BBCCCDDD | 0 |
| NVDA_US_Equity | 2026-05-20 | 7 | 7 | AAABBCD | 0 |
| NVDA_US_Equity | 2026-09-23 | 6 | 6 | BBCCCC | 0 |

On every day:
- status 200;
- the served count equals the gold rows for that day;
- 0 unjoined articles;
- 0 served tier or mention counts differing from gold;
- 0 exact-key ties (the order is fully determined).

Each article carries its headline. For example, BA 2026-09-29 leads with "Boeing Just Won a Major Navy Fighter Jet Contract, but
Don't Lose Sight of the 737 MAX" (tier A, 19 mentions).

## Scope

The read was read-only: the served Lambda and gold reads only. No write, no collection, no vendor call. NVDA was picked as the
highest-volume name in gold (850 mention rows).
