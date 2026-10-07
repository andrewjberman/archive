# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 23 (RIV-ks-1) -- deploy the five rivalfunds Lambdas at CLOUD 6124b079f3, republish 2026-10-07 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~19:2xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** CTO ruling msg 31267 on this seat's msg 31266: deploy RIV-ks-1 today as its own act (a render-only deploy does
not wait for the 11:00Z run). It removes the one fault the round-15-to-22 deploy served by statement: 4 mentions in GQGU's
panel that open a dialog holding only a name (rows Z-S65, Z-S66). No vendor is called; no wheel is built; nothing is
fetched (source-only packages, the existing layer ARN, providers on disk; the packager is not in the install census).

## VERDICT: SIGNED

Conditions: the pin is CLOUD 6124b079f3; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (beb13d39ff, live since 17:3xZ, ledger `etfs-rivalfunds-r22`)

`git diff beb13d39ff 6124b079f3` over every path the packager stages (the rivalfunds package without tests, the Lambda
wrappers, the Terraform root, `lib/opal_naming.py`, `lib/trading_calendar.py`, `lib/research/identity`,
`infra/logic/registry`, `NAMING_SCHEMA.json`, `etf_positioning_gold.py`): **1 file, `render.py`, +13 / -3**. Nothing else.
The repair: packet `round23/DRAIN_END_PACKET.round23.md` @ce0b3a783b.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (slug `etfs-rivalfunds-r23`): apply; republish; served read.
2. **`safe-apply` of `C:/tmp/rv_apply23.tfplan`** from `C:/tmp/rv-r8` detached at the pin after `rivalfunds_package.py`
   (plan text `round23/rv_apply23.plan.txt`): **0 to add, 5 to change, 0 to destroy**; `source_code_hash` and
   `last_modified` only; memory stays 3,008 MB. Before = the live set (daily fRDyQ2eK, fetch OyCwkAJ2, canonical agDnuNLz,
   silver WiQ5KvRF, publish Sh82EnlI); after = daily cTM1SBuG, fetch 99BqkcrG, canonical tyGN8WS/, silver TLYlfz3r, publish
   RHlHCL0l. A saved plan refuses if the state moved; then re-plan and re-read, never force.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-07","mode":"daily","batch_id":"rv-publish-1007r23","sink":"s3","refresh_a1":false}`.
   `refresh_a1` is FALSE: no table's code changed. A request that drops at the client is re-fired only after the log shows
   no START and the page objects are unmoved (as at 17:38Z today).
4. Download the served objects; grade against the prediction with `round22/served_grade.py`; close the ledger.

## THE WRITE SET, READ FROM THE CODE PATH (analysis R4), with the rollback per key

`publish_page.py` at the pin, lines 804 and 926 to 993. Under `s3://opal-data-etfs/rivalfunds/etfs/`:

| key | when it is written | expected | rollback |
|---|---|---|---|
| five Lambda code hashes | the apply | the after-set | re-package at beb13d39ff, plan, `safe-apply` |
| `gold/holding_contribution`, `gold/buying_trend`, `gold/input_census` at `date=2026-10-07` | `produce_a1` (line 804) rebuilds a table ONLY when a G1 or G4 input is newer than its newest object | **no write**: the tables were rebuilt 17:45-17:46Z and no ingest runs before 2026-10-08 11:00Z. If one is written, it is one new write-once object in the same shape and it is reported | none needed |
| `platinum/page/date=2026-10-07/revisions/<stamp>/` index.html, audit.html, manifest.json, charts/ 13 objects | line 934 on: the served objects are copied here first, because the page's bytes change | 16 copies of the objects served since 17:47Z | none; they are the rollback |
| `.../index.html` | line 962 | 1,690,296 B (served 1,690,862); `fund_sections` 2247 / 2247 / 0; dialogs 410 -> 408 | republish from the rolled-back code, or copy back from `revisions/` |
| `.../audit.html` | line 964, written whenever the page changes | 1,255,777 B, the same size as served | same |
| `.../charts/<FUND>.json`, 13 | line 966, rewritten whenever the page changes | 13 objects, 5,675,727 B, 5,894 markers: the same sizes as served | same |
| `.../manifest.json` | line 993 | `fund_sections.missing` 0; `ai_grounding {"earlier": 25, "served": 0}` | same |
| `state/publish_page/date=2026-10-07/rv-publish-1007r23.json` | the run's record | one object | none |

If the rendered bytes equalled the served bytes the publisher would write nothing (line 926); they do not, by the 4 links.

Prediction source: the real-run tool run from the worker branch for day 2026-10-07 (`round23/real_run_2026-10-07.after_ks1.json`);
the package code of that branch equals the pin's (`git diff 97149dd163 6124b079f3` over the package: empty). That tool
rebuilds the two tables locally first, which the Lambda will not; the page it renders is drawn from tables of the same
inputs, and this afternoon its sizes matched the served ones exactly.

## BOTH BRANCHES

- **The run fits** (this afternoon: 164.5 s and 1,009 MB with the tables rebuilt; less without): status OK, the reads above.
- **Killed or timed out:** the order is copies, index, audit, charts, manifest. Before `index.html`: the page served since
  17:47Z stays. After it and before the last chart object: the new page with the chart objects of 17:47Z, which hold the same
  data, so the charts still draw; the manifest is the old one. CTO condition C1 of the last half applies again: manifest not
  older than index and 13 chart objects, or one more republish, else roll back.
- **A table IS rebuilt** (an input newer than expected): the page is then drawn from tables one revision newer; the sizes
  may differ from the prediction. It is reported with the newer input's uri from the manifest, not treated as a fault.

## WHAT THIS ACT DOES NOT PROVE

- Not RIV-ks-1 J1: that is `3.0.0_SA_CVO~RV`'s, on the served page after it.
- Not the first full daily run on the new code: legs L4 and L5 of `etfs-rivalfunds-r22` stay open for 2026-10-08.
- The 20 AI accounts naming to-date figures stand until the 2026-10-08 13:00Z sweep.
