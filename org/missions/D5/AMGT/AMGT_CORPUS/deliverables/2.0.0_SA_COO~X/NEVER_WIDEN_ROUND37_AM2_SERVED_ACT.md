# AMGT_CORPUS round 37 -- never-widen pair for `CRPS-am-2`: one re-derive of the 96 served blocks with a currency on every money figure, and the re-pin of the daily task to the commit carrying it

**Authority:** round-36 analysis @`4c3e3755a7` ruling 1 ("Round-37 cell, SERVED (pair) ... The re-derive runs over all 96 blocks.
Control: a census of money figures with a null currency over every monetary field reads 0"). Decomposition v37.0 @`ece32e98a6`
s.1. The producer change is CRPS-am-1, drained @`3ffe37a57a`.

**Code:** `<p>` = CLOUD at or after `3ffe37a57a`, read at the act. `integrations/bloomberg/research/model_block_pull.py` at `<p>` must
equal its bytes at `3ffe37a57a`. Any other producer change at `<p>` is a STOP.

## TIMING: the legs run AFTER CRPS-am-5 has read the 2026-10-05 13:00Z fire

The 13:00Z fire runs on pin `74e00624b0` and is read as the carried regression of FWD-22 (am-5). There are two reasons the legs
wait for it:
1. A re-derive before 13:00Z would be undone at 13:00Z. That fire re-derives every block with the old producer, which drops the
   labels: served churn.
2. A re-pin before 13:00Z would put new code under the fire being read (the round-35 ak-4 rule).

So legs d and r run together after am-5's read, and the next fire (2026-10-06 13:00Z) is the first on `<p>`.

## THE SERIALIZING DRY RUN OVER EVERY KEY (`checks/round37/am2_dryrun.py` -> `evidence/r37_am2_dryrun.txt`)

The act's exact producer path: the REAL `stage_derive(..., sa_fallback=False)` on each served newest block's own raw stamp, at CLOUD
`3ffe37a57a`. It runs in memory: reads go through, and all 96 puts were captured and never sent.
- **Names:** 96 registered with a block, 96 derived, 0 failed.
- **Money figures** (unit MILLIONS / ABSOLUTE / PER SHARE, never a "(share count)" unit): 31,985.
  - labelled: before 8,578, after 31,934;
  - null with no reason: before 23,365, **after 0**;
  - null with a reason: 51. That is round 25's 42, plus 9 `CRNCY_ADJ_MKT_CAP` on the 9 names whose `CUR_MKT_CAP` round 25 holds out
    (939 HK, AZN LN, BP/ LN, HSBA LN, JD US, PBR US, RIO LN, SHOP CN, ULVR LN). am-1 classifies `CRNCY_ADJ_MKT_CAP` exactly as
    `CUR_MKT_CAP`, so it inherits that measured `UNMEASURED:` null. Verified on 939 HK, AZN LN and BP/ LN.
- **Values moved: 0.** Labels changed: 0. The 8,578 existing labels hold.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r37-am2`)

0. **Gate.**
   - am-5 has read the 2026-10-05 13:00Z fire.
   - `am2_dryrun.py` is re-run at `<p>` on the post-fire raw. It must show `after 0` and `values_moved 0 labels_changed 0`.
   - `schedule_induction.ps1 -Plan -Commit <p>` prints `PLAN python ...\Python311\python.exe (source: live-task)`. STOP on anything
     else.
1. **(d) Re-derive:** one `stage_derive(s3, security, raw_stamp=<newest raw>, sa_fallback=False)` per registered name with a block
   (96). Each writes a NEW write-once `derived/model_block/<key>/<stamp>/model_block.json`.
2. **(r) Re-pin:** `schedule_induction.ps1 -Register -Commit <p>`, then `-Status`.
3. **(v) Verify:**
   - `money_currency_census.py` reads `null_unlabelled 0` over 96 names;
   - every name's newest block is the re-derive's;
   - `checks/round35/v35.py <stamp prefix>`: base values moved 0 (with its positive control on older pairs) and pointer-unit figures 0;
   - `checks/round36/al5_served.py --where deployed`: 1/1 + 1/1;
   - TSM's Model tab is looked at on portal DEV (once am-3's `2e7c5cdb` is pushed there): money rows print USD / TWD and no "currency
     not stated" mark remains on a labelled row;
   - the task reads Start In `<p>`, Python311, 13:00Z.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' RULES (every branch)

- **Writers of the served block:** one function, `stage_derive`, reached by `cmd_derive`, `cmd_admit`, `cmd_refresh` and this leg's
  loop.
- **Writers of a figure's currency:** one rule, `_figure_currency` at `<p>`. N = 1.
- **Branch A (all 96 derive):** the dry run's numbers exactly: 0 null-unlabelled money, 51 reasoned, 0 value moves, 0 label changes.
- **Branch B (a name fails to derive):** it keeps its 13:00Z block, the failure is listed, the other names proceed, and the census's
  0 is read over the names that derived.
- **Branch C (the plan names a non-Python311 interpreter, or the script refuses):** STOP before (r). The blocks stand, and the old
  pin's next fire would re-derive without labels, so the issuer re-runs (d) under the old producer in the same session (below).

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| `derived/model_block/<key>/<stamp>/model_block.json` | up to 96 NEW write-once keys, each becoming the served newest; only `currency` / `currency_basis` differ from the prior block | forward: re-derive from the same raw at `74e00624b0` (mints a newer block with the old labels); exact restore by deleting the new objects needs Andrew's word |
| Scheduled Task `amgt-induction-daily` | its Start In (pin `<p>`), interpreter Python311 (unchanged), trigger unchanged | `-Register -Commit 74e00624b0` |

Never touched: any raw/bronze object, any Bloomberg call (the re-derive reads landed raw only), any Seeking Alpha call
(`sa_fallback=False`), `field_map.json`, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-05 ~00:5xZ, for legs 0, d, r and v, covering branches A, B and C. The legs
run after am-5's read of the 2026-10-05 13:00Z fire.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
