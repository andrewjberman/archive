# RIV-wa-1 J1 -- the issuer's read of the IDVZ dialog on the 2026-10-12 page

Author 2.0.0_SA_COO~V1, 2026-10-12 ~15:3xZ, dell1. Nothing here grades; the grade is the CVO's (row D1-S15 ARMED on wa-1, HELD:
"the IDVZ dialog on the first page published with this code reads a continuous 30d curve near 3.3 across 2026-10-07 and names the
15-for-1 split, the factor from a stored row"). Source: S3 `rivalfunds/etfs/platinum/page/date=2026-10-12/charts/IDVZ.json` (written
2026-10-12 13:07:10Z; `generated_at` 2026-10-12T13:07:06Z; `asof` 2026-10-09).

## Measured

| # | fact | source |
|---|---|---|
| 1 | `TKOMY_US_Equity`, name "Tokio Marine Holdings Inc", currency USD, in IDVZ's chart | `securities/TKOMY_US_Equity` |
| 2 | `adjustment`: one entry, `split`, ratio 15.0, ex_date 2026-10-07, claim **MEASURED**, source_url null (the Bloomberg `corporate_actions` row of 2026-10-09 11:03:55Z, `L2_READ_20261012.md` fact 6) | same node |
| 3 | R30 window starts 2026-09-09: 23 points, 23 drawn, 0 None; min 3.306, max 3.571 (ratio 1.08); the largest one-step change is 6.0%; codes `i` (implied) and `m` (market close) | `ranges.R30`, `points` |
| 4 | Around the ex-date: 10-05 3.31 m, 10-06 3.37 m, 10-07 3.33 m, 10-08 3.35 m, 10-09 3.40 m | `points` |
| 5 | The only gap in the series: 2025-10-09 to 2025-12-31, "no market close on file and no fund reported the holding": outside R30 (R90 starts 2026-07-11, R365 2025-10-09, so it shows only on R365) | `gaps` |
| 6 | Earlier revision for comparison: page `date=2026-10-09` revision `20261009T130829Z` (written 10-09 13:08:30Z, before the 14:49Z deploy), same security: 10-05 49.59, 10-06 50.50, 10-07 3.33, no `adjustment` key | S3, that revision's `charts/IDVZ.json` |
| 7 | Which page is "the first published with this code": `date=2026-10-09/charts/IDVZ.json` was last written 10-09 13:08:33Z (pre-deploy, no `adjustment` key; only IDVZ's file was read); the 2026-10-12 IDVZ chart (13:07Z) is the first read whose bytes carry `adjustment`. A page `date=2026-10-10` does not exist (a Saturday) | S3 listings |

## Not measured

- The dialog rendered in a browser (this reads the JSON the dialog draws from).
- The published-HTML `index.html` text for the dialog's sentence naming the split.
