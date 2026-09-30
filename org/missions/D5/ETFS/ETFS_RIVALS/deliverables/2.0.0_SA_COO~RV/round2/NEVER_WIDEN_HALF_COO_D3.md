# NEVER-WIDEN -- COO HALF: the ETFS_RIVALS round-2 live join (`RIV-d-3`): deploy in place, G0, import both capture sets, enable the Bloomberg leg, fire

**Signer:** `2.0.0_SA_COO~RV`, 2026-09-30 ~21:2xZ; re-signed ~21:3xZ for Andrew-direct "1b" (PRD v0.5) and RIV-d-3 amendment 2. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).

**Serves:** PRD `org/missions/D5/ETFS/ETFS_RIVALS/prd/ETFS_RIVALS_PRD.md` v0.4 (the peer groups, the Bloomberg channel,
income-clean trades, and the page grouped by Opal fund), task order `ETFS_RIVALS.TO-RIV-d-3` with its ISSUER AMENDMENT 1.

**Andrew-direct, binding on this act** (record `deliverables/2.0.0_SA_COO~RV/ANDREW_DIRECT_20260930_20xxZ_DO_NOT_MODIFY_POSITIONING_PULL.md`):
- *"do not modify the existing daily etfs pull for Positioning"*
- *"Anything we do for this would have to be additive"*

**Code pin:** the merged round-2 HEAD the d-3 worktree is cut from. It carries every other round-2 order, merged. The worker prints
`git log --oneline -3` first.

## VERDICT: SIGNED

The blast radius, per key. BEFORE was measured 2026-09-30 ~21:1xZ, every page, client-side counts.

| # | key | before | after | rollback |
|---|---|---|---|---|
| 1 | `s3://opal-data-etfs/bloomberg/etfs/bronze/holdings/` | 0 | 944 imported captures (503 IDVZ-group + 441 PFOE-group), each raw + `.sidecar.json`, `capture_origin census:*`; then one daily batch per trading day | a delete is a HUMAN word |
| 2 | `.../bloomberg/etfs/silver/holdings/` | 0 | typed silver per report date for RIVALS only; IDVZ and PFOE rows = **0** (CTO ruling (b), msg 27404; e.g. the 45 IDVZ rows of 2026-09-29 land in bronze bytes, never in silver) | same |
| 3 | `.../rivalfunds/etfs/gold/{peer_group_map,holdings_coverage,corporate_actions,flow_reconciliation}/` | 0 each | G0 map_version 1; G2; G3 (import of `dividends.json`, 4780 records + 43 status rows, then daily); G6 | same |
| 4 | `.../rivalfunds/etfs/gold/{canonical_shape,trade_schedule}/` and `.../platinum/page/` | 325 / 324 / 6 objects | NEW revision objects only. The existing BASG objects are never overwritten (never-overwrite, revision ids) | same |
| 5 | `.../rivalfunds/etfs/state/{fetch_bloomberg,build_bloomberg_silver,pull_enrichment,build_peer_group_map,build_coverage,build_flow_reconciliation}/` | 0 each | batch-complete markers | same |
| 6 | the five round-1 Lambdas | round-1 code (source-map stamps @3eaa380467) | in-place `source_code_hash` update carrying the round-2 stages; no create or destroy of a function | re-apply at the prior stamped commit, same window |
| 7 | the five stage role policies | round-1 prefixes | + PutObject on the key-3 and key-5 prefixes and the Bloomberg silver prefix, each builder-generated (`gen_policies.py`); no DeleteObject anywhere | re-apply the prior policies |
| 8 | EventBridge rules / targets / permissions for the new markers (for example `fetch_bloomberg` -> the silver stage) | none | created, names from `name()` | `terraform destroy -target` of the new rules only |
| 9 | `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd` | the gated-OFF `:rivalfunds_bbg_leg` (RIV-b-1) | ONE added line inside that leg enabling it | delete that one line (the gate goes OFF) |
| 10 | Bloomberg requests from the terminal machine (R-21, scripted only) | none by this pipeline | the 08:03 leg: the five IDVZ-group rivals and `issuer_first` funds lacking issuer bronze that day (GQGU excluded, NO-BLOOMBERG-ROUTE); NOT IDVZ, NOT PFOE (Andrew "1b": `home_producer`); enrichment `DVD_HIST_ALL` for G1's securities | key 9's rollback stops them |

**Writers counted:**
- **Keys 1 and 10:** 1 writer, the terminal machine's AWS identity `user/Andrew_Berman`. IAM simulator: PutObject on
  `bloomberg/etfs/bronze/holdings/...` is **allowed**. Control: its existing `bbg/.../constituents/` write is also allowed.
- **Keys 2-5:** the stage Lambdas, one role per stage.
- **Keys 6-8:** `safe-apply` only.
- **Key 9:** this act's one line.

**Unmoved** (the positive list the act must not touch):
- the Positioning pull (`etf_constituents_pull.py`, `etf_daily_pull.py`) and every existing line of the vehicle (Andrew-direct);
- `etfs-netassets-daily` and its homes; the bucket's tier-first keys; issuer bronze (650 BASG objects);
- the gateway: NO deploy this round. `/rivalfunds` serves the new page through the routes already live.

## ACT-START GATES (the worker STOPS with a BLOCKING row on any)

0. **The printed daily request holds no IDVZ and no PFOE** (amendment 2).

1. **Keys 1, 3 and 5 still read 0 objects.** A non-zero count means another writer: STOP.
2. **Plans are in-place or create-only.** Each plan is in-place Lambda code updates plus policy widening plus new rules only.
   Any destroy, replace, or change to a non-rivalfunds resource STOPs.
3. **The additive proof holds.** After the enabling line, `b-1.AC3` still PASSES: all 394 base lines of the vehicle survive
   in order, and nothing is edited but the new leg.
4. **The Terminal is signed in before the enable.** `bloomberg_health` is up and one real `reference_data` read succeeds.
   4.0.0_SA_CRO~Z (msg 27377) measured the Terminal logged out during its census. If signed out,
   the enable still lands, and the first 08:03 run reads exit 91 (branch B). The worker records the state; it never retries
   a sign-in.
5. **NEVER-2:** the ledger entry `etfs-rivalfunds-round2` and its sentinel are committed before the first apply, after the
   union read over every live worktree.
6. **The import count is printed before the first landing:** 503 + 441 files, from the device-local captures.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' RULES, BOTH BRANCHES

- **Import:** one bronze object + sidecar per capture file (import is idempotent on sha256). Silver per report date. G1
  selects one source per (fund, report date) by the map. G2 reads the census counts for the IDVZ group within the imported
  window (SCHY 501, INEQ 498, CGIC 496, BIDD 464, TXUE 417 new days, plus or minus 2%).
- **IDVZ and PFOE (Andrew "1b", PRD v0.5):** `home_producer`. RIVALS reads the Positioning pull's landing for them and never
  requests them from Bloomberg. G1 has no home-producer reader this round (row W1-S8), so both read ABSENT on the page with
  their reason. The Positioning pull's own gaps (capture from 2026-08-21, 22 of 27 days) are recorded as ABSENT.
- **Branch A (Terminal signed in at 08:03):** the leg exits 90. A day's batch lands; markers drive silver, G1, G2, G5 and
  G6, and the page publishes grouped.
- **Branch B (signed out, or Bloomberg unreachable):** the leg exits 91, nothing is written by it, and the other four legs
  are unaffected. The page publishes the prior day's data, with each fund's day marked not updated.
- **G5 waits for G3 (row W3-S13, disarmed by amendment 2):** no date's trade schedule is built before its corporate-actions
  marker exists.
- **Trades:** cash and currency lines never trade. Corporate actions are applied. Income types follow `RIV-g-4`'s amendment
  table.
- **No second landing of IDVZ/PFOE (PRD v0.5).** The only IDVZ rows this act lands are inside the imported historical capture
  bytes (bronze keeps bytes as obtained). G1 never reads them. Whether silver keeps them is routed to `1.0.0_SA_CTO~Z`.

## ROLLBACK

- **Keys 6-9:** per the table, same window.
- **Keys 1-5:** new objects under new prefixes, or new revisions nothing else reads. A delete is a HUMAN word, never the
  worker's.
