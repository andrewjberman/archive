# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 8 -- deploy the five rivalfunds Lambdas at CLOUD 68329a011c, rebuild G0 for 2026-10-05 ONCE, republish 2026-10-05 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~14:3xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** round 8 (11 orders over workstreams A-D) is built, re-graded by the issuer and drained:
- drains cad46984ee, b88cb050f2, 6eb8787b4b, c17854ffff, b930e18d40, 1d5d79ee9f, 0fb70bf7f6, c79332ad2c (13:03Z);
- su-1 hookup ac1b42fcdb (`produce_security_universe`);
- hc-1 amendment 1 (row Z-S26: G4 `total_return_index` is the day's percent return, read as an index ratio), drained 2a91dac5e4;
- drain repair 68329a011c (row Z-S27: `peer_groups.json` map_version 1 -> 2, so G0 takes lg-1 A1's SCHY-rival change).

At the pin: package suite 652 passed, 2 skipped, 0 failed; ruff py39 clean; all 20 round-8 mechanical checks PASS (19 at c79332ad2c,
hc-1.AC2 at 2a91dac5e4). The bound "no deploy before the 13:30Z grades" is met: `3.0.0_SA_CVO~RV` graded at 0fe137ee28 (sa-1 J1 PASS;
ui-5 J1 NOT MET, carried by enrichment item 3).

## VERDICT: SIGNED

Conditions: the pin is CLOUD 68329a011c; every gate below reads as stated; the act stops at the first leg whose read differs.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-round8`).
2. **`safe-apply` of the saved plan** `C:/tmp/rv_apply17.tfplan`, made from `C:/tmp/rv-r8` detached at 68329a011c after
   `rivalfunds_package.py` staged the build (plan text `C:/tmp/rv_plan17.txt`). It reads **0 to add, 5 to change, 0 to destroy**:
   five `aws_lambda_function.stage` `source_code_hash` changes plus the computed `last_modified`, nothing else. The before
   hashes are exactly round 7's verified live set (live `get-function-configuration` at 14:0xZ): daily vK1xwhs0, fetch DOQCSAX9,
   canonical LOORbFv0, silver fTe3LTYg, publish n0h0/K7d; the after hashes daily +PBG7mA/, fetch CJjz9t4B, canonical /ZbAMTsg,
   silver WXNW1ctD, publish jfPkICFz. No role, policy, secret, environment, schedule or trigger changes;
   `RIVALFUNDS_LEG_D12` / `_D13` / `_ENABLE` stay unset on all five.
3. **G0 rebuild:** `etfs-rivalfunds-daily-lambda {"only":["build-peer-group-map"],"date":"2026-10-05","mode":"daily",
   "batch_id":"rv-g0-1005r8","sink":"s3"}`. By the producer's rule (`gold_peer_group_map.py:94-110`): map_version 2 at
   date=2026-10-05 is absent, so it writes ONE new key `gold/peer_group_map/date=2026-10-05/map-2.parquet` (13 rows); map-1 is
   untouched.
4. **ONE real run (the republish):** `etfs-rivalfunds-daily-lambda {"only":["publish-page"],"date":"2026-10-05","mode":"daily",
   "batch_id":"rv-publish-1005r8","sink":"s3","refresh_a1":true}`. `only` stamps run_path "ad_hoc"; `run_ai_step` finds the
   day's account object (research_hypotheses-20261005T130020Z-ai.parquet) and returns SKIPPED_EXISTS: no vendor call.

## EXPECTED OUTCOME -- MEASURED, NOT PREDICTED

Measured by running the pin's own `gold_peer_group_map.handler_entry` and `publish_page.handler_entry` (same events, sink a local
mirror of `s3://opal-data-etfs/rivalfunds/etfs/` synced 14:1xZ, 164 MB; `C:/tmp/r8measure/dry3_result.json`):
- G0: OK, written_new 1, map-2.parquet, 13 rows; the page reads it ("G0 ... map-2.parquet (map_version 2)").
- holding_contribution: refused 28 -> **0**; price_source g4_tri 8 -> 973, holding_implied 1,516 -> 320, missing 790 -> **46**.
- Page: "Benchmarks (SCHY)" 1 -> 0, "SCHY is a benchmark" 1 -> 0; no MTD control; "Data available since" on 8 panels; AI dialogs
  13 with ONE "No AI account" -- SCHY, now a rival, whose first account is the 2026-10-06 09:00 ET AI run.
- security_universe: one new key at date=2026-10-02 (1,016 securities over 504 report dates).
- status PARTIAL with `report_date_freshness` on IDVZ/IDVZ, BIDD, CGIC, SCHY -- unchanged from the served page (the IDVZ group's
  latest report is 09-30: Positioning lag + today's capacity-blocked Bloomberg pull, rows Z-S24/S25).

Branch NOT applied (the apply fails or a verify reads otherwise): stop, close the ledger entry red, the served page stays the
13:07:41Z ai- batch; nothing below runs.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | round 7's set (75ad1e4d2e) | the 68329a011c set | a saved plan from a detached worktree at 75ad1e4d2e after `rivalfunds_package.py`, `safe-apply` |
| gold/peer_group_map/date=2026-10-05/map-2.parquet | absent | 13 rows, map_version 2 | delete that key (human-confirmed S3 delete); map-1 is untouched and is read again |
| gold/{holding_contribution,buying_trend,input_census}/date=2026-10-05/ | 1+ object each | +1 object each (newest) | republish with refresh_a1 after the code rollback writes a newer object each |
| gold/security_universe/date=2026-10-02/ | absent | 1 object | delete that key; no reader on the served page |
| platinum/page/date=2026-10-05/{index.html,manifest.json} | batch ai-2026-10-05-a53411fb (13:07:41Z), kept under revisions/ | batch rv-publish-1005r8 | republish after the code rollback |
| state/{build_peer_group_map,publish_page}/date=2026-10-05/ | present | +1 marker each | none needed |

Not in this act: the terminal-machine Bloomberg leg (lg-1) already runs from the CLOUD working tree at the next 07:00 ET vehicle;
with all three gates unset it pulls as before. The D12 flip and the IDVZ/PFOE import (D12 Step B) are their own half, next.
