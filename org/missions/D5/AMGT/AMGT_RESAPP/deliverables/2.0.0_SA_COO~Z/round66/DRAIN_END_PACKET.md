# AMGT_RESAPP round 66 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-04 ~00:5xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.74. **Issuance:** `b1aa5a6bb1`.

**Input:**
- The CTO's round-65 analysis @2de1ef2251 (rulings 2 and 3).
- ADDENDUM 1 @1162e9be0e (option (a)) and ADDENDUM 2 @205bd13011 (ANDREW-DIRECT ~20:5xZ, the daily job).
- ANDREW-DIRECT ~20:3xZ cards 4 and 5 (record @9fe6e6f111).
- PRD v0.37.

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `ap-1` FWD-39 word cloud | LOCAL | worker ~217 | complete | drained `2674ac7ba8`; closed `aebf58884b`; plant 9 of 9; c18 local YES |
| `ap-2` FWD-36 price 90/365 build + the daily job's step | WORLD | worker ~218 | complete | drained `8f10187a78` = the daily job's deploy, under the pair COO `b996226a1b` + CTO `682826c8d9`; closed `b642e313f9` |
| `ap-3` the live one-time PX_LAST year pull | WORLD | `0.7.0_AE_CloudOps~A` | complete | `444ad788f4`: 95 of 95; `year_pull.json` 562,248 B write-once; 90/365 generations 94/94/95/95; DELTA=0 exact on deployed |
| `ap-4` the code redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete | `abb9bd85de`: pin `b642e313f9` (355/350/5); `lPTMo20T` -> `FcVBPafw`, 1769; pair COO `ffd60053d9` + CTO `98c2b63401` |

## The real run on the DEPLOYED function (`FcVBPafw...`, 1769 MB), the issuer's re-read

| check | result | detail |
|---|---|---|
| c18 (FWD-39) | YES | BA, AMD and VLO serve 40 terms each, counted and ordered, with no stop word (158 declared, source named) and no company-name word. An empty window serves `terms: []` with "no coverage headlines in this window" |
| c19 (ruling 2) | YES | every chatter window's `tone_reason` reads "window tone is not served on this route yet" |
| c22 (FWD-36 price 90/365) | YES | trending and breakout x 90 / 365 serve 94 / 95 rows with `window_end` 2026-10-02, the last trading day |
| c9, c10 (30-day), c11-c14, c17 | YES | no regression |
| c15 cold (day route) | YES | 3 of 3 at 2.03-2.33 s against 5 s (AE~A) |
| range route cold (CTO's added read) | 2.03-2.55 s | 9 of 12 cold, 0 over 5 s: the word-cloud read is inside c15's band |

## For the CVO's L9 read (JUDGMENT, never self-graded)

1. **FWD-39: read the served terms as a reader would.**
   - BA: 'max', 'jet', 'order', 'software'.
   - AMD: 'market', 'chip', 'explain', 'meta'.
   - VLO: 'ban', 'diesel', 'export', 'oil'.
   - The empty-window block serves the route's clamped `from` (2026-01-01) after its `to` (2025-06-30). That is the route's existing
     floor clamp, served as is.
2. **FWD-36 price 90/365 are now real windows** from a stored year of PX_LAST. They end at the last trading day today, from the
   one-time pull.
   - From the next scheduled run (2026-10-04 11:00Z) the daily job persists its series and rebuilds 90/365 each day (ADDENDUM 2).
   - **Owed by this seat after that run:** the post-run read (the 30-day exit code and row counts, the `daily_30d.json` key, and the
     90/365 branch taken).

## Carried to round 67 (routed by the CTO, not cuttable into the issued round 66)

1. **FWD-38 (d) provenance**: the Model tab prints "1 of 6 inputs have run" and "no source set up yet" at rest (DSGN round-32 grades
   @ff31355b93). The producer half needs a cell.
2. **FWD-36 tone**: HARVST `chatter_window` is served (618 rows, part 20261004T001638Z; COO~H msg 29087). The route serves `tone`
   from it, with "no clear tone" at 0 voters, and drops the "not served on this route yet" reason. Then a redeploy.
3. **DE_US_Equity thesis/peers answer 404** (CORPUS r34 ruling 4, Z-S86): a covered name with no model block must serve its
   designed reason.

## Rows

- `Z-W218-S1`: a fixture stub for the new route read; inside the cell.
- `Z-S344` (AE~A): c10's 90/365 clauses contradicted c22 on the same bytes. Disarmed at `6e1852e03f`: c10 keeps its 30-day clauses,
  and c22 grades 90/365.

Both are OBSERVATION and INERT.
