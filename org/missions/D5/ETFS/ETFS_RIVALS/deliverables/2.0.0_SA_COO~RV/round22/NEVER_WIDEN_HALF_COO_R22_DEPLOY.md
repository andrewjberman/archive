# NEVER-WIDEN -- COO HALF: ETFS_RIVALS rounds 15 to 22 -- deploy the five rivalfunds Lambdas at CLOUD beb13d39ff with memory 3,008 MB, republish 2026-10-07 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~17:0xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** Andrew-direct 2026-10-07: "i want mcp.opalinvest.dev/rivalfunds demoable Today"; at ~15:4xZ he read the served page and
saw no dialog chart and no 30d / 90d / 365d switch -- those are rounds 15 to 22, merged and not deployed. Order of acts:
`ledger/ROUND_ANALYSIS.round20.md` R1 (push done, gateway release r26 live, then this deploy, then the backfill). Memory: CTO
ruling msg 31149 on row ETFS_RIVALS-Z-S63. No vendor is called by this act; no wheel is built (source-only packages; the pandas
layer is an existing ARN; the Terraform providers are on disk).

## VERDICT: SIGNED

Conditions: the pin is CLOUD beb13d39ff; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (22844f744f, round 14, ledger `etfs-rivalfunds-pk1-al1` CLOSED)

`git merge-base --is-ancestor 22844f744f <pin>` rc=0 (reverse rc=1, the negative control). Over every path the packager stages:

| path | change |
|---|---|
| `data/etfs/scripts/rivalfunds` (tests aside) | 11 files, +1,055 / -109: `price_series.py` and `trade_markers.py` new; `publish_page.py`, `render.py`, `page_theme.py`, the two A1 tables, `gold_canonical_shape.py`, `enrichment_bloomberg.py`, `bbg_budget.py`, `ai_accounts.py` |
| `infra/aws/terraform/etfs-rivalfunds` | `memory_size` 1024 -> 3008 only (@beb13d39ff); the regeneration changed no policy and no name |
| `lib/opal_naming.py`, `lib/trading_calendar.py`, `infra/logic/registry`, `org/standards/NAMING_SCHEMA.json` | changed through the origin merge. Read on both codes: the page, manifest, market and canonical-shape addresses and `prev_trading_day` for 2026-10-07 and 2026-10-12 are identical. Two dates and four addresses were read, not every caller |
| `lib/research/identity` | 10 files through the origin merge, plus `crosswalk.py` (+84) since my first plan. Not read line by line; the pin-exact run below exercises it and reproduces the earlier run's sizes |

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-r22`), legs: apply; republish;
   served grade; first-run Max Memory Used and Duration per function (CTO term 1).
2. **`safe-apply` of `C:/tmp/rv_apply22.tfplan`** from `C:/tmp/rv-r8` detached at the pin after `rivalfunds_package.py` (plan
   text `rv_apply22.plan.txt` beside this half): **0 to add, 5 to change, 0 to destroy**; per function `memory_size 1024 ->
   3008`, `source_code_hash`, `last_modified`, nothing else. Before = round 14's set, live (daily +q+ZhIAN, fetch PFuw02pT,
   canonical twgfrYMm, silver /G6WUOac, publish 3LLu4N6N); after = daily fRDyQ2eK, fetch OyCwkAJ2, canonical agDnuNLz, silver
   WiQ5KvRF, publish Sh82EnlI. A saved plan refuses if the state moved; then re-plan and re-read, never force.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-07","mode":"daily","batch_id":"rv-publish-1007r22","sink":"s3","refresh_a1":true}`.
   `refresh_a1` is TRUE here (round 14's was false): the two A1 tables must be rebuilt by the new code, whose windows are 30,
   90 and 365 days; with it false the publisher would skip them (no input is newer) and render the new page from old tables.
4. Download the served `index.html`, `audit.html`, `manifest.json` and the 13 chart objects; grade against the prediction;
   read the page and one dialog chart through `mcp.opalinvest.dev/rivalfunds` (the chart route has not been exercised by this
   seat: it returned 404 while no chart object existed); read each REPORT line; close the ledger.

## BLAST RADIUS -- what the act may touch, and the rollback per key

| key (under `s3://opal-data-etfs/rivalfunds/etfs/`) | writer | expected | rollback |
|---|---|---|---|
| five Lambdas: code hash and memory | the apply | the after-hashes; 3,008 MB | re-package at 22844f744f, plan, `safe-apply`: the old code and 1,024 MB return together |
| `gold/holding_contribution/date=2026-10-07/` | the republish (`refresh_a1`) | ONE new object, about 121,538 B, 6,066 rows; earlier objects stay | the stage reads the newest object; after a code rollback, one republish with `refresh_a1` true writes a newer object in the old shape |
| `gold/buying_trend/date=2026-10-07/` | same | ONE new object, about 70,374 B, 1,406 rows | same |
| `platinum/page/date=2026-10-07/index.html` | the republish | 1,690,862 B (served now: 1,286,540 B), 13.3 percent under the 1,950,000 cap; 690 chart frames; the 30d / 90d / 365d switch | the prior object is copied under `revisions/<stamp>/` first; republish from the rolled-back code |
| `.../audit.html` | the republish | 1,255,777 B (now 1,243,556), 0 scripts | same |
| `.../manifest.json` | the republish | 103,640 B; `ai_grounding {"earlier": 25, "served": 0}`; `fund_sections` 2247 / 2243 / **4 missing** | same |
| `.../charts/<FUND>.json`, 13 objects | the republish | FIRST MINT: 13 objects, 5,675,727 B in all, largest 1,130,254 B | none needed: the round-14 page does not reference them; no delete is granted or used |
| `state/publish_page/date=2026-10-07/` | the republish | one run record | none |

Prediction source: the real-run tool run from the deploy tree at the pin for day 2026-10-07 (live S3 read-only, local writes,
A1 producers off, the two tables rebuilt first): `round22/real_run_2026-10-07.prediction.json` (run at a4542de7f9) and the
pin-exact rerun, equal in every byte count above. The tool has matched the served sizes on each of the five earlier deploys.

**The served page moves, and that is the act's purpose:** the tables change from month / quarter / year to date to 30 / 90 /
365 days, every holding gains a dialog with a price chart and its trades, names and month strips change.

## TWO KNOWN FAULTS THE ACT SERVES, stated so the CTO half covers them

1. **4 mentions open an almost empty dialog (served today: 0).** In GQGU's panel, "META PLATFORMS INC" and "ASML HOLDING
   NV-NY REG SHS" in one sentence ("The fund also opened ...", twice each) target the CUSIP-keyed dialogs `30303M102` and `N07059210`, which hold a
   name and nothing else; the full dialogs sit under `META_US_Equity` and `ASML_US_Equity`. CAUSE NOT TRACED (corrected ~17:1xZ: this half first
   said the sentence links by the schedule's raw key; that was a guess. The sentence is in the fund's account text, and a
   dialog shell exists under the CUSIP key with no section; which stage emits the shell was not read). The publisher prints its FAIL line and publishes. Row
   ETFS_RIVALS-Z-S65. The count read 3 from round 17 and 6 from round 21 on day 2026-10-06 and this seat did not report it:
   my miss. REC: deploy with it stated, repair in the next round (one cell).
2. **25 AI badges read "Grounded on an earlier build"** until an AI step runs on the rebuilt tables: the 2026-10-08 13:00Z
   sweep. Same as round 14's deploy. Whether the accounts' month / quarter wording still fits a 30 / 90 / 365-day table until
   then was not read by this seat.

## BOTH BRANCHES OF EACH NEW REACHABLE STATE

- **Memory and time (row Z-S63).** Measured: the deployed daily Lambda used 864 MB of 1,024 MB and 440 s of 900 s on today's
  11:0xZ run; the new two tables and publish peak at 1,552 MB and take 296 s on site Z. Lambda CPU scales with memory, so
  3,008 MB should not be slower; nothing measures it. *Fits:* the republish returns OK; the leg records Max Memory Used and
  Duration. *Does not fit (killed or timed out):* each object is one put, written whole or not at all, in the order read
  from `publish_page.py` lines 934-993: the two tables, the copies under `revisions/`, `index.html`, `audit.html`, the 13
  chart objects, `manifest.json`. A kill before `index.html` leaves the round-14 page served beside new tables it does not
  read. A kill after `index.html` and before the last chart object leaves the NEW page served with chart objects missing:
  those dialogs would read "Chart could not load" and the manifest would be the old one. Remedy for either: one more
  republish if the cause is passing, else roll back as above and republish. **CTO term 2 holds: a first-run Duration above 720 s is a BLOCKING row before backfill day 1.**
  The republish is NOT the daily run: the 2026-10-08 11:00Z run (every stage) and the 13:00Z sweep are the first full runs,
  and their REPORT lines are legs of the same ledger entry, read before it closes.
- **The scheduled runs after the act.** Writers of the page: 3 (the 11:00Z daily, the 13:00Z sweep, a deliberate republish),
  all one `publish_page` code path. *A1 input newer:* tables rebuilt, as today. *None newer:* skip, as today. No new writer.
- **Backfill-marked rows.** None exists in gold today (the backfill has not run). The CTO's term stands for after this act:
  read the DEPLOYED stage ignoring a backfill-marked row before day 1. Local proof: `round20/delta0_2026-10-06.json`.

## MARKERS: the three figures side by side (CTO msg 31149)

| figure | what it counts | reconciles as |
|---|---|---|
| **46** (the CVO's, `ADJUDICATION_v23.Z.md`) | markers in the round-22 run and not in the run before the fold | 43 + 3 markers dated on the page day (GQGU 2, IDVZ 1), which the earlier run could not hold |
| **43** (named, `round22/markers_vs_trade_schedule_2026-10-06.json`) | the same, page-day ones aside: BASG 10, GQGU 33 | each traced by fund, dates and dollars to ONE trade-schedule row recorded under another key: 43 of 43 |
| **BASG +10, GQGU +2** | markers above my ruler built from the trade schedule (a row counts under its recorded key or the key G4's parsekey gives) | the ruler reaches 31 of GQGU's 33 by parsekey, so they are inside it; the 12 left are trades recorded under a CUSIP (BASG 10) or a raw ticker string (GQGU: IBKR 1, META 1) that the publisher maps to the chart key and my ruler does not. Ruler + 12 = markers: BASG 660 + 10 = 670, GQGU 688 + 2 = 690 |

So against the trade schedule: 11 of 13 funds equal outright, and 13 of 13 once those 12 traced rows are counted. The route
for BASG's 10 is named by elimination (not parsekey, not ticker string); the rows themselves are matched, the mapping code
path was not stepped through. Trades in the schedule under a key on no chart (for example CGIC 2,823, SCHY 1,200) are outside
this read: they are securities the page gives no dialog, as before.

## WHAT THIS ACT DOES NOT PROVE

- Not md-1 J1, pd-2 J1, or the re-reads of rows Z-S55 and Z-S57: those are `3.0.0_SA_CVO~RV`'s on the served page after it.
- Not the working-tree vehicle's round-20 enrichment change (row Z-S62): first run 2026-10-08 11:00Z, read then.
- Not the backfill, and not a year of price history: 98 of 690 frames read "No price history is stored for this holding yet."
