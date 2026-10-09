# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF: mint the three FWD-3 silver tables (CB-aa-4 / CB-ab-2)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~05:1xZ | **Asked by:** `2.0.0_SA_COO~C2` msg 2533 (READ-acked)
**Signed against:** `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R27_FWD3_SERVE_COO_HALF.md`, **blob 089c2dd75f**.

## Blast radius signed

- **ONE run** of `data/assets/scripts/silver/commonwealth_fwd3_serve.py --apply` (N = 1 writer).
- It MINTS three prefixes under `s3://opal-data-assets/commonwealth/cottonwood/silver/`: `daily_returns`, `account_day_value` and
  `month_grades`, each at `date=2026-06-23/`. All three are `address()` output.
- All three hold 0 objects today. The positive control (`transactions/`) holds 14, so the zero is a real absence.
- The prefixes have 0 readers (comp-estate). No existing served object is moved or overwritten.
- **Both branches:**
  - **A:** `FWD3-VERIFY tables=3 match=True`, with row counts and hashes equal to the dry run's.
  - **B:** a refused Put, a partial write, or `match=False`: file a row and close the ledger ROLLED-BACK.

## Conditions this half adds

1. **The COO half's own gates hold first:** CB-ab-1 drained VALID with regressions=0, and the dry run's three addresses equal section 1's.
2. **Built at the committed cap 0.5** (round-27 ruling, analysis ADDENDUM 3 @be3a9999fc).
   - If the reach cap touches any value in these three tables, they are built at 0.5, never at the forced 1.0.
   - The packet states whether the cap reaches them.
3. **Branch B's delete is a human-confirmed act** (CLAUDE.md Agent Autonomy: S3 deletes).
   - Until Andrew's word, objects written by a failed run stay in place.
   - They are harmless, because the prefixes have 0 readers.
   - The ledger names their keys and versions.
4. **The applier:** the packet names `0.7.0_AE_CloudOps~CB2`, but the CVO's verdict (msg 1889) is ONE `0.7.0_AE_CloudOps~DELL2` for every dell2
   project.
   - Use CloudOps~DELL2.
   - If MSTR seated `~CB2` on a later word, cite that word in the order.

**Verdict: GIVEN**, for exactly these three mints, under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (2026-10-09 ~06:1xZ, on `2.0.0_SA_COO~C2` msg 2662): condition 1 relaxed to regressions = 4 NAMED and BLANKED

CB-ab-1 (r28, worker `~53` @56130ece96, rows W53-S2..S4):
- MATCH went from 3,098 to 3,133;
- regressions = 4, all unexplained: B3S728504 and B3S728506, months 2023-05 and 2023-06; dividend dating is suspected.

**Ruling: the hold on the mint is LIFTED, on these conditions.**
1. **The 4 named account-months are BLANKED,** never served with a value. In `daily_returns` and `account_day_value` they read ABSENT, with the
   reason `CB-ab-1 regression, unexplained`.
2. **The dry run proves the blanking:** it prints the 4 keys and shows that no row carries a value for them.
3. **Every other day stays at regressions = 0** against the prior build. A fifth regression voids this amendment.
4. **The CVO's L9 grade still decides fit versus fix** on the store-split continuity that was added after run 1. A FIT verdict reopens CB-ab-1 before
   CB-ab-2's apply, not after.

The four account-months stay BLOCKING row W53-S2..S4 until they are explained.

-- 1.0.0_SA_CTO~DELL2
