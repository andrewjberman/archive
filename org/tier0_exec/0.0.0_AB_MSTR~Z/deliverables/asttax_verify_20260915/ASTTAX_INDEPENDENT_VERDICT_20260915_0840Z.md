# ASTTAX independent verdict for the 13:00Z portal promote -- 0.0.0_AB_MSTR~Z, measured 08:10-08:40Z 2026-09-15

VERDICT: PRESENTS PROPERLY at the served bytes -- with ONE VINTAGE QUALIFIER: 23 of 25 holdings are one trading day behind T-1.

## 1. Served bytes (s3api get-object pinned by VersionId; parsed by this seat's own script, probe_chars.py)

- `opal-data-cot/platinum/satellites/characteristics.json` VersionId `PXyBGaqn.0Jk6TwWmXl34FlsDH8Gwd0R`, LastModified 2026-09-15T08:10:03Z, 67764 B, IsLatest (re-read 08:3xZ). Prior version = the rollback pin `74d9.pGWF16Ox7cXKGax.zQw.lhwi5yI` (04:53:42Z).
- `as_of` 2026-09-15; `inputs`: holdings_as_of 2026-09-15 (holdings.json `5tjkvDfus1antRLsbDrLikcMQzH1Hk.F`, 07:00:20Z), bbg_as_of 2026-09-14, bbg_run_class adhoc, bbg_universe_count 172, positioning_data_as_of 2026-09-11.
- `tickers` block: 25 entries = the 25 distinct tickers holdings.json holds (set difference 0 in both directions). name and management_style non-null 25 of 25. Sources: 23 positioning_data, 1 bbg (GLD), 1 none (CASH).
- Per-holding measures non-null of 25: fee 24, aum 24, returns 24 (CASH the null), active 23, yield 22, beta 11, duration 9, credit 7 (the remaining nulls follow asset class; they render `-`).
- Source agreement, checked against the producer's own inputs rather than its output: the 23 positioning_data tickers vs `json/positioning/positioning_data.json` current_holdings (VersionId `AqBtm_5o.2QeiCBRP_veC8HV2Xk0OSaj`, pinned): 345 cells, 0 mismatches. GLD vs `opal-data-etfs/bbg/2026-09-14/characteristics.parquet`: FUND_EXPENSE_RATIO 0.4 = fee 0.4; FUND_TOTAL_ASSETS 143675.09831 = aum 143675.09830982.
- Against the rollback pin, only GLD's record changed (aum and its 8 returns); bbg_as_of moved 09-11 -> 09-14 and holdings_as_of 09-14 -> 09-15.
- Served floats carry full precision by design (a pass-through contract); rounding is the renderer's and is graded in section 2.

## 2. Render (a different instrument from 2.0.0_SA_COO~Z's: not scripts/ui-smoke.mjs, not its fixtures, not its compare)

- Own detached worktree of `refs/drains/posn-6-portal` @ebbee2e61a (`C:/tmp/mstrz-verify-portal`), own vite :5191, own playwright-core script (`mstrz_render.mjs`), fixtures built from the six served keys this seat fetched by VersionId (md5 equal to 2.0.0_SA_COO~Z's present_manifest.json 6 of 6), own DOM extraction and cell compare (`mstrz_compare.py`) under the renderer's formatting as read at the ref (HoldingsTab.tsx:1644-1724, performanceUtils.ts:57-63).
- Route /positioning -> Satellites -> Opal Satellite 15 and Opal Satellite 80 -> Holdings Breakdown, Characteristics AND Performance views.
- Opal Satellite 15: 16 served holdings, 16 rendered rows, 272 cells (name, weight, 7 characteristics, 8 returns), 0 mismatches.
- Opal Satellite 80: 16 served holdings, 16 rendered rows, 272 cells, 0 mismatches.
- DISCRIMINATING ARM: the same render with three served values mutated inside the fixture (GLD fee 0.4 -> 0.55, GLD 1Y 17.1187 -> 99.5, VGSH yield 3.49 -> 7.77). Against the unmutated served values exactly those 3 cells mismatch (55, +99.50%, 7.77); against the mutated values, 0. The cells read the served block, not a default.
- Numbers with 3+ decimals anywhere in the page text: 0 (both satellites, both views). Holdings panel footers and headers: `Source: Black Diamond, holdings as of 2026-09-15`. CASH `-` / em dash throughout; GLD Commodities / Metals, fee 40, MC 143.7, Active NO, returns -1.49% .. +17.12%.
- Instrument disclosure: the first compare reported 1 mismatch (VNLA MTD). The served value is -0.0, which JS prints `+0.00%`; my compare printed `+-0.00%`. Fixed in the compare, not a render defect.
- Cosmetic, visible on the PNG, not a float: VGSH credit renders `-0` (served -0.1467 through toFixed(0)).
- Evidence (this folder): mz_sat15_characteristics.png, mz_sat15_performance.png, mz_sat80_characteristics.png, mz_sat80_performance.png, mz_sat15_mut_*.png, the three *_dom.json dumps, and the render script mstrz_render.mjs.
- CORRECTION 08:5xZ (this seat): the version sent over the bus at 08:4xZ said "the three scripts". The two Python instruments (probe_chars.py, mstrz_compare.py) are NOT committed. .tools/commit-gate.sh refused probe_chars.py (undefined-name), and they are scratch instruments, not estate code. They remain in this session's scratchpad, and their method is stated in sections 1 and 2.

## 3. The vintage qualifier

- 23 of 25 holdings carry positioning_data data_as_of 2026-09-11. T-1 for 2026-09-15 is 2026-09-14 (`lib/trading_calendar.prev_trading_day`). Only GLD is at 2026-09-14; CASH has no source.
- Writer and cadence: positioning_data.json is published by this box's Scheduled Task `OPAL_BBGTML_daily_pull` (07:00 ET: the models pull, then `publish_to_portal.py`, then the ETF and constituents legs; `scheduled_daily_pull.cmd`). State Ready, LastRun 09/14 07:00 ET rc 0, NextRun 09/15 07:00 ET. Measured version history: 09-10 11:07Z -> data_as_of 09-09; 09-11 11:06Z -> 09-10; 09-12 11:05Z -> 09-11; no Monday 09-14 ~11:0xZ version (its T-1 was 09-11, already served); the 09-14 21:21Z and 09-15 00:56Z versions are re-publishes still at 09-11.
- An ad-hoc run before ~10:30Z is mechanically possible and NOT recommended by this seat: it is the production models chain, and it moves the served key the live portal's Models mode reads, so it needs never-widen halves first. The 11:00Z scheduled fire would then run the same publish again, which the wrapper's own text warns against. It gains about 40 minutes against a promote the scheduled path already meets.
- The path that meets 13:00Z with no new act on the models key: the 11:00Z scheduled task -> positioning_data at 2026-09-14 (EXPECTED ~11:05Z from the cadence above; a prediction until read) -> characteristics.json re-served either by B6's own rule `cot-satellites-characteristics-producer-daily` cron(30 12 * * ? *) ENABLED (read 08:38Z) at 12:30Z, or sooner by a third driven run under a both-halves amendment (the R2/A2 shape). This seat re-runs sections 1-2 on those bytes and reads the vintage 25 of 25.

## 4. Andrew's words, graded

"a real ad hoc pull": YES -- bbg/2026-09-14 adhoc at 07:52:33Z, carried into the served block for the one holding Bloomberg prices.
"the data presents properly on Asttax": YES on presentation (544 of 544 cells equal the served values, the mutation arm discriminates, no unrounded values). The qualifier: 23 of 25 holdings are one trading day behind T-1 until the ~11:05Z models publish reaches characteristics.json.
