# NEVER-WIDEN -- COO HALF: ETFS_RIVALS D12 -- turn the IDVZ/PFOE Bloomberg gate on and import their 2026 history ONCE, purely additively

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~19:4xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Authority:** Andrew-direct @33ff3bdac0 ("not touch anything being done on the Positioning pipeline ... purely additively ... one ad hoc
targeted backfill in the rivalfunds shape for IDVZ and PFOE, then we add the two funds to the daily incremental pull") and its addendum
@4bd948e824 ("Backfill is approved for IDVZ/PFOE"); CTO~Z rulings: msg 29579/29594 (order_key condition MET; "purely additive" per
date), ruling (B) on row Z-S29 (named-fund G5, gate file); round 9 deployed at 8ba7b13b90 (ledger etfs-rivalfunds-round9 CLOSED).
No Bloomberg request is made by this act (the import reads the LOCAL Step A captures), so row Z-S24's capacity hold does not bind it.

## VERDICT: SIGNED

Conditions: every gate below reads as stated; the act stops at the first differing read; the proof after is the per-date census.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-d12-step-b`).
2. **Flip D12 in the gate file:** one commit changing `data/etfs/scripts/rivalfunds/leg_gates.json` `RIVALFUNDS_LEG_D12` "0" -> "1"
   (ENABLE and D13 stay "0"). Read live: no Lambda carries a `RIVALFUNDS_LEG_*` variable, so the file is the only switch.
3. **Deploy the flip:** package at the flip commit, `terraform plan` -> 0 to add, 5 to change, 0 to destroy (code hashes only), saved
   plan, `safe-apply`; read back 5 hashes. Every stage then reads IDVZ and PFOE as `bloomberg_primary`.
4. **The import (the one ad hoc backfill):** on the terminal machine at the flip commit,
   `collector_bloomberg.handler_entry({"mode": "import", "captures": <the 189 local Step A capture .json files under
   C:/bbg_backfill/idvz_pfoe/>, "date": "2026-10-02", "batch_id": "import-d12-idvz-pfoe", "sink": "s3",
   "rebuild_funds": ["IDVZ", "PFOE"]})`. The fetch-bloomberg marker carries `rebuild_funds`; the S3 event rule then runs
   silver -> canonical (windowed, 600 s per pass; the canonical Lambda continues within its budget and the 09:00 ET sweep continues
   any open cursor) -> coverage -> the gated trade schedule, which rebuilds ONLY IDVZ and PFOE and carries every other fund's rows.
5. **Watch the chain to its end** (the canonical marker, the coverage marker, the trade-schedule marker for the batch); if the
   canonical cursor is still open at 20:30Z, continue it once with the canonical Lambda's own event (same date and batch).
6. **ONE republish** of 2026-10-05 with `refresh_a1: true` (retries off): the A1 tables take IDVZ/PFOE's new history.

## EXPECTED OUTCOME -- MEASURED ON THE MIRROR, NOT PREDICTED

The same import, chain and trade schedule run at nf-1's code on a fresh mirror of `rivalfunds/etfs/`, `bloomberg/`, `issuer-site/`
and `bbg/` (C:/tmp/r8measure/stepb_nf1_report.json):
- G1: 189 of 189 report dates rebuilt; **0 other-fund deltas** (row count and content hash per fund, provenance columns aside);
  IDVZ/PFOE read `source_used` bloomberg on every date, +12,798 rows. The named date 09-30: IDVZ 41 + PFOE 25 rows were
  home_producer at the live revision; after, Bloomberg.
- G5: 189 of 189 dates rebuilt; every other fund's rows **value-equal on every column the live object carries**; +367 IDVZ/PFOE
  trade rows. The only difference: `est_price_source` and `key_resolution`, columns newer code added, are present and null on carried
  rows (the render reads `key_resolution` as optional; `est_price_source` is not rendered).
The census is re-run on the served objects after the act against the 19:1xZ snapshot (C:/tmp/r8measure/ov_pin); any other-fund
delta beyond those two columns is a STOP and the rollback.

## THE DAILY JOIN (the second half of Andrew's word)

From the flip on, the vehicle's daily Bloomberg leg (CLOUD working tree, `leg_gates.json` D12 "1") pulls IDVZ and PFOE with the
rivals: about 69 rows a day (row Z-S20), inside the cb-1 budget. The Positioning pipeline is untouched: its files are neither written
nor read differently by its own producer; rivalfunds simply stops reading them for these two funds.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| leg_gates.json + the five Lambdas' code | D12 "0" at 8ba7b13b90 | D12 "1" | commit D12 "0", re-package, `safe-apply` |
| bloomberg/etfs/bronze/holdings/date=2026-10-05/import-d12-idvz-pfoe-* | absent | 189 captures + 189 sidecars | none needed (append-only; unread once D12 is off) |
| rivalfunds/etfs/state/fetch_bloomberg/date=2026-10-02/import-d12-idvz-pfoe.json | absent | 1 marker | none needed |
| bloomberg/etfs/silver/holdings/date=<189 report dates>/IDVZ-*, PFOE-* | absent | 377 objects | none needed (unread once D12 is off) |
| rivalfunds/etfs/gold/canonical_shape/date=<189 dates>/ | newest live revision | +1 newer revision each (IDVZ/PFOE Bloomberg rows added) | D12 off + a canonical replay over 2026-01-02..10-02 writes newer revisions without them |
| rivalfunds/etfs/gold/{holdings_coverage,trade_schedule,flow_reconciliation}/date=<dates>/ | newest live objects | +1 newer object each date (others carried) | a trade-schedule rebuild with `rebuild_funds` IDVZ/PFOE after the canonical replay |
| A1 tables + platinum/page/date=2026-10-05 | 19:34 objects / rv-publish-1005r9 | +1 object each / a new batch | republish with refresh_a1 after the rollback |
