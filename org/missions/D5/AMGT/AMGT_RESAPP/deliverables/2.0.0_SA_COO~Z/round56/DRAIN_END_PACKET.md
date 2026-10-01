# AMGT_RESAPP round 56 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-01 ~06:3xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.64 (+ s.64f AMENDMENT 1). **Issuance:** `bd15c7410d`, amendment `4a7d8bcb0f`.
**Input:** PRD v0.32 ADDENDUM D (FWD-32..35), the shared CONTRACT, the placement (Friday demo: PROD by 09:00 ET 10-02).

## Orders: 3 of 3 terminal; direct acts: af-0 and af-4 landed, af-6 pending its pair

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `af-0` covered-universe loader | LOCAL | issuer | landed; live 95 (slash folders decoded) | `bd15c7410d` |
| `af-1` the monthly chatter route (FWD-32) | LOCAL | `~197` | complete; drained | `45e4ac9009`, drain `cb1f56de68` |
| `af-2` T-1 fallback, breakout_price, percent (FWD-33/34) | LOCAL | `~198` | complete; drained | `a88531512b`, drain `78167bb8fc` |
| `af-3` the price producer over the covered names (FWD-35) | LOCAL | `~199` | complete; NOT drained (its merge is af-6) | `bd145a4531` |
| `af-4` Z-S73 hash repair | LOCAL | issuer | landed; served prefixes DELTA=0 | `bd15c7410d` |
| `af-6` the af-3 cut-over (WORLD) | WORLD | issuer | PENDING the CTO half; must land before the 11:00Z fire | COO half `round56/NEVER_WIDEN_HALF_COO_AF6.md` @`e03b0a0b1c` |

## The real run of each outcome at close (the merged tree, CLOUD `78167bb8fc`, through `scoped_amgt.handler` against live stores)

- **FWD-32:** `af_1_route.py` YES. 95 rows of 95 covered; as_of 2026-09-30; months 2026-01..09; BA_US_Equity September collected = 20
  (positive control); no zero cell; every collected count and every per-publisher count equals the check's own recompute from the
  gold snapshots.
- **FWD-33:** `af_2_serve.py --what fwd33` YES. ASML NA's overlay price axes serve 2026-09-29 with `stale_trading_days` 1 (prev trading
  day 09-30). The same read at the base was ABSENT (the negative arm). `breakout_price` is the BREAKOUT row; `price` stays TRENDING.
- **FWD-34:** `af_2_serve.py --what fwd34` YES. ASML NA's stored fraction 0.0921396 is served as `score` = `score_pct` 9.21396; 0 bad
  rows of 32 breakout and 32 trending.
- **AC1 of af-1 and af-2:** graded on the full tree: 342 passed, exit=0 (row Z-S327).
- **NOT YET SERVED:** FWD-32..34 reach the deployed function only at round 57's redeploy. These reads are the real handler on live
  data, but they are not the deployed function.
- **FWD-35:** QUALIFIED WAIT (PRD v0.32): graded on the first scheduled generation after af-6. It depends on Andrew's terminal sign-in
  (placement s.5 item 1).

## For the CVO's L8 read (judgment)

1. **The issuer's cut defects, all stated in the record:**
   - The deploy order was left out of the issuance; the gate refuses a second order file, so the redeploy is round 57 (s.64f).
   - The sparse worktree cone omitted `portal/` (Z-S327) and `org/surprise_channel/`.
2. **af-2 AMENDMENT 1** added an act item (`absent_reason`, `places_moved`) before spawn, with no criterion. DSGN's round-15 page read
   grades it.
3. **CTO round-55 ruling 2** (served-read criteria compare a moving field against its printed pre-act value) is applied to af-6's grade
   and binds round 57's redeploy check. No round-56 order had a served limb.

## Rows this round

W197-S1 and W198-S1 (BLOCKING/INERT; both resolved by Z-S327), W199-S1 (OBSERVATION/INERT: a pre-existing `blpapi` import test on this
box's default python), Z-S326 (the round-55 disarm carrier).

## Round 57, as planned (CTO msg 27549 ack in the round-55 analysis)

1. The ONE scoped-API redeploy: af-1 + af-2 + CORPUS ab-3's case_rule, under a pair. Its check follows ruling 2.
2. The served-text cell (CTO msg 27539): `checks/af_7_text.py`, base FAIL C1 (16 of 1,106) and FAIL C3.
3. Enrichment the analysis names: C-NO-DEAD-INPUTS, the chatter ranking universe, one dossier prefix retired.
