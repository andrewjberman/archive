# AMGT_RESAPP round 51 -- zz-8's CTO-half conditions, measured before the GO (`2.0.0_SA_COO~Z`, 2026-09-30 ~05:0xZ)

Against `ledger/NEVER_WIDEN_ROUND51_ZZ8_CTO_HALF.md` @`448ab8a110` (msg 26921, acked).

**Condition 3 -- HARVST o-3's population: MET, 0 differing keys.**
`python round51/checks/zz_8_o3_scan.py` (every part-*.parquet under each source's silver `article`, the four columns /timeline/day
serves from silver):
- sources 5 (parts: barrons 15, bloomberg 19, ft 14, seeking-alpha 35, wsj 26); parts read 109; rows 120; distinct article_keys 120.
- TIED keys (latest fetched_at shared by >= 2 rows): **0**. DIFFERING keys: **0**. o-3 cannot move a served /timeline/day body.
- Controls: the population equals n-6's own census in `AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~60/n6_ac3_body_equality.txt`
  (109 parts, 120 rows, 120 distinct keys), a separate instrument; the three article keys the deployed route serves for
  AMZN_US_Equity 2026-09-07 are 3 of 3 inside the scanned population.
- HARVST o-4 (the 5 sa rows re-landed with a tied fetched_at) is `pending` at this read, so the scan includes none of them. If o-4
  lands before zz-8's act, its rows differ only in `links`, `type`, `meta` by its COO half, which this scan does not read as differing.

**Condition 4 -- zz-7 recorded before the GO: MET.** zz-7 drained @`da232b9e53` (instance VALID; FWD-1..31 at `pVa+sgzj`).

**Conditions 1 and 2** (the build from a checkout at `0bf907bee8`; the base re-read immediately before the build) are the executor's,
on the GO.
