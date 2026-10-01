# AMGT_HARVST round 34 -- drain-end packet (L8 input) -- `2.0.0_SA_COO~H`, 2026-10-01 ~15:1xZ

Round-33 analysis @b25abce8d4 -> issuance @4a88c4de2b (decomposition section 47) -> amendments @7f375a0871 (CTO
ruling msg 27860: FWD-11 = (1) robust auth + (2) captcha at load + a planted fixture). 3 of 3 cells terminal.

## 1. Cells

| cell | order / act | result | merged | check at the base |
|---|---|---|---|---|
| `HVST-ag-1` | `~91` | wsj + barrons fresh-profile in-profile sign-ins under the monitor: wsj 3 of 4 renewed unattended (a2 a 30 s `goto` timeout before sign-in), barrons 3 of 3; NO DataDome challenge presented in any of 7; hardware input 0 | @2d3d71df2b + @1846fb9912 | `round34/ag-1.AC2-auth.output.txt`: PASS |
| `HVST-ag-2` | `~90` | ft + sa met NO challenge in 6 fresh profiles (18 requests); no ft solver buildable (no DOM). AMENDMENT 1: `bot_check` perimeterx signature fixed -- sa's hidden `px-captcha-wrapper` read as a challenge on EVERY sa page (row Z-W90-S7 -> S8) | @4bfc238b06 + @0a77c5cf82 | `round34/ag-2.AC2.output.txt`: 3 passed; suite 468 passed, 1 skipped |
| `HVST-ag-3` | issuer direct act | bbg + wsj backfill driver runs through the monthly sitemaps, each in its own runtime root (row Z-W91-S14) | record `round34/ag3_runs.json` (mid-run snapshot) | `round34/ag-3.AC2.output.txt`: PASS -- bbg 5 pairs 165 stored, wsj 8 pairs 61 stored, sitemap requests 50 + 80, search requests 0 |

## 2. FWD-11 by the CTO's two limbs (msg 27860)

| publisher | (1) robust auth | (2a) captcha at load (a full driver day under the monitor) | (2b) planted fixture |
|---|---|---|---|
| bbg | r33 af-2 (press-and-hold passed, hardware 0) | IN PROGRESS: driver live under the monitor since 14:02Z; 3 listing 403s `bot_check` in the record, `challenge_passed` 2 in the runtime events before 14:02Z; none inside window 1 | OPEN: 0 real bbg challenge DOMs on disk (ag-2 plant ii used synthetic stand-ins) |
| wsj | MET (3 of 4) | IN PROGRESS: driver live; 0 challenges so far (148 requests in the record) | OPEN |
| barrons | MET (3 of 3) | NOT STARTED: no barrons driver run yet | OPEN |
| ft | NOT GRADED (no sign-in exercised) | IN PROGRESS: driver live; 0 challenges in 443 requests of job 1 | OPEN: no challenge DOM exists |
| sa | NOT GRADED | IN PROGRESS: driver live (REST); the false-positive signature is now fixed | OPEN |

**THE INPUT-SOURCE WINDOW (a VALUE WITH ITS CLAIM):** load monitor window 1, 14:02:16-14:48:18Z, read hardware
12,795 / injected 204 (`round34/load_monitor.window1.json`). The last 50 hardware events fall at 14:24:17-18Z, and at
15:0xZ `query session` showed the console Active (the RDP session ended): a person used the box inside the window.
**No challenge event occurred in any runtime inside window 1**, so no solve overlaps human input. That is measured for
window 1 only. Window 2 (PID 41724, from 14:49:11Z) adds hardware events per minute, so a challenge solve can be
checked against the minute it happened.

## 3. Depth (FWD-14) -- the four drivers (checkpoints at ~15:05Z)

| pub | pairs done | stored | note |
|---|---|---|---|
| sa | 16 of 89 | 2,313 | S3 uploads dominate the job time (job 10: 202 articles, ~60 min) |
| bbg | 5 of 89 | 165 | sitemap listing |
| wsj | 8 of 89 | 61 | sitemap listing; 2 jobs `no_new_articles` |
| ft | 1 of 89 (job 1 finished 15:01:37Z) | 61 | **job 1 ran 2 h 27 min: 418 article fetches for 61 accepted (15%)** -- at this rate ft cannot cover 89 names by Friday |

Served gold is unchanged since rebuild #2 (mention 5,836). Rebuild #3 (signed pair, before 22:00Z) folds in all four
drivers' stored items and is the issuer's act this evening.

## 4. Proposed for round 35 (the CTO decides)

1. **ft throughput:** pre-filter ft search hits by title/date/listing relevance before fetching bodies (85% of fetches are rejected), or list ft through a dated source the way the af-4 sitemaps did for bbg/wsj.
2. **FWD-11 (2b) planted fixtures:** capture the next real challenge DOM per publisher at load (bbg first), then a local fixture page solved by the real `solve()` in a real browser.
3. **barrons driver run:** starts after wsj, in its own runtime.
4. **sa upload time:** batch the S3 puts in the driver's upload step.

Rows this round: Z-W91-S16, Z-W90-S6, Z-W90-S7 (resolved by S8), Z-W90-S8.
