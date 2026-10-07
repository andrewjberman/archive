# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 14 -- deploy the five rivalfunds Lambdas at CLOUD 22844f744f, republish 2026-10-06 ONCE (Z-S54 A + C; the audit page's size rule)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~04:1xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** Andrew-direct 2026-10-07 ~03:1xZ on row Z-S54: "not needed do a and c" (record @3e040ecbf2); round-13 analysis ADDENDUM 1
and ruling 4 (@594d1be8f8). Issued @7667270270, drained @22844f744f. Issuer re-run on the worker branch: ab-1.AC1, ab-1.AC2,
as-1.AC1 PASS; both proofs VALID; package suite 795 passed, 2 skipped, 0 failed. B (an AI re-run) is not cut and no vendor is
called by this act.

## VERDICT: SIGNED

Conditions: the pin is CLOUD 22844f744f; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (f3b3055a5e, ledger etfs-rivalfunds-lk1 CLOSED)

Measured: `git merge-base --is-ancestor f3b3055a5e 22844f744f` rc=0 (reverse rc=1, the negative control). `git diff f3b3055a5e
22844f744f` over `data/etfs/scripts/rivalfunds`, `infra/aws/lambda/etfs-pipeline`, `infra/aws/terraform/etfs-rivalfunds`: 5
files, 3 of product -- `sweep.py` (+25), `render.py` (+144), `publish_page.py` (+17) -- and 2 new test files. The packager also
stages `lib/opal_naming.py`, `lib/trading_calendar.py`, `lib/research/identity/`; the wider `lib/` diff between the pins is
under `lib/research/scores` and `lib/research/watchlist`, which the packager does not stage (read from `rivalfunds_package.py`
lines 34-36; the three staged lib paths were NOT diffed separately -- the CTO half or the apply's hash read covers that).

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-r14`).
2. **`safe-apply` of `C:/tmp/rv_apply14.tfplan`** from `C:/tmp/rv-r8` detached at 22844f744f after `rivalfunds_package.py`
   (plan text `rv_apply14.plan.txt` beside this half): **0 to add, 5 to change, 0 to destroy**, `source_code_hash` +
   `last_modified` only. Before = the lk-1 set, live (daily VhckkMgd, fetch gWWtaG7i, canonical 6lKYpSsD, silver oUN0tQyQ,
   publish LbqdRy4S); after = daily +q+ZhIAN, fetch PFuw02pT, canonical twgfrYMm, silver /G6WUOac, publish 3LLu4N6N.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-06","mode":"daily","batch_id":"rv-publish-1006r14","sink":"s3","refresh_a1":false}`.
4. Download the served `index.html`, `audit.html`, `manifest.json`; grade against the prediction below; close the ledger.

## BLAST RADIUS -- what the act may touch, and the rollback per key

| key | writer | expected | rollback |
|---|---|---|---|
| five Lambda code hashes | the apply | the five after-hashes above | re-package at f3b3055a5e, plan, `safe-apply` (the lk-1 set) |
| `.../page/date=2026-10-06/index.html` | the republish | 1,279,784 B (was 1,276,544): 24 PASS badges gain `data-build="earlier"` and read "Grounded on an earlier build"; 0 read "served" | the prior object is kept under `revisions/`; republish from the rolled-back code |
| `.../page/date=2026-10-06/audit.html` | the republish | 1,381,244 B, unchanged; no `data-audit-cut` | same |
| `.../page/date=2026-10-06/manifest.json` | the republish | gains `ai_grounding {"earlier": 24, "served": 0}` and `audit_trades_left_out 0`; `fund_sections` 2076 / 2076 / 0 | same |

Prediction source: `real_run_2026-10-06.json` beside this half (the real-run tool at the pin: live S3 read-only, local writes, A1
producers off) plus this seat's read of the rendered index and manifest. The tool has matched the served bytes on each of the
four earlier deploys.

**The served page moves, and that is the act's purpose (C):** every passing account on 2026-10-06 changes its badge from
"Grounded" to "Grounded on an earlier build". No figure, table or account text changes.

## BOTH BRANCHES OF THE NEW SWEEP STEP (A), read from the producer's own rule in `sweep.run_ai_step` at the pin

Writers of the A1 tables in the sweep after this act: 2 -- the new refresh before the AI step, and the republish's own
`produce_a1` (unchanged). Both call the same `publish_page.produce_a1`, which rebuilds a table only when an input is newer.

- **Refresh succeeds:** the stale tables are rebuilt before the AI step, the accounts cite the new revisions, the republish finds
  nothing stale. Expected on the 2026-10-07 sweep (13:00Z): every passing badge reads "Grounded", `ai_grounding.earlier` 0.
- **Refresh raises:** recorded as `a1_refresh {"status": "FAILED"}`; the AI step runs on the tables as they are; the republish's
  own rebuild then runs as it does today, and the badges read "Grounded on an earlier build". No worse than today, and stated.
- **Refresh uses up the invocation (row Z-W1-S49):** the step returns `SKIPPED_TIME` with `a1_refresh`; no AI run and no
  republish in that invocation. The tables are rebuilt but the page is not re-rendered until the next publish. The refresh
  measured about one minute on 2026-10-06 (the worker's figure from the 13:05-13:06Z rebuild stamps, not re-measured by this
  seat). This is the one new reachable state; it is not exercised by this act.

## WHAT THIS ACT DOES NOT PROVE

- The CTO's proof "26 of 26 accounts on the served revision, IDVZ Petrobras equal to the panel" needs an AI step run after the
  deploy: the 2026-10-07 sweep. Not claimed here. Note the real run counts 24 PASS badges, not 26: the other 2 accounts were not
  read by this seat and are not PASS-badged on the page.
- The pk-1 / al-1 proof (ledger `etfs-rivalfunds-pk1-al1`, OPEN) still waits on the 11:00Z vehicle run; this pin descends from
  that code and changes none of its files.
