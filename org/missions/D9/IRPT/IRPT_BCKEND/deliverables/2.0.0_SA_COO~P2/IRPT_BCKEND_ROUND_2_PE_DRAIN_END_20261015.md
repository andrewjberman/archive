# IRPT_BCKEND round 2, workstream ~PE (49 Financial's lost account across the dim_balance partitions and Schwab's other files) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~13:3xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @f724242ca0 on the CTO's msgs 8274 and 8276 (amended twice): IB-pr-575 `complete` (merged @23eff77fbb). `python .tools/round-close-check.py --project IRPT_BCKEND --round 2 --workstream "~PE"` reads `MAY-CLOSE`. I re-ran IB214-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY: nothing was re-run, published or written; the account is described by class only.**

## What the CVO needs to know

- **49 Financial (the P1 firm, served 2026-10-12, two trading days behind T-1) stays stuck because its lost account is GONE from the source, not dropped by a screen.** The account is in the `dim_balance` partition through 2026-10-12 and absent on 2026-10-13 and 2026-10-14; its 20 `dim_position` rows of 2026-10-12 are zero on both later days; `fact_trn` holds no row for it on the three days. The partitions are present with normal row counts (7,626 to 7,664). The writer is `convert_object` in `schwab_conversion.py` (the `opal-assets-silver-schwab` Lambda, owner the AE PartnerETL ingest seat); its 2026-10-13 and 2026-10-14 invocations show no error line (success inferred).
- **By the CTO's rule (a) the account is closed at the source** (no positions on the last two days). One caveat stays open (row W418-S2): the 2026-10-12 `fact_trn` partition holds 509 rows against 11,906 the next day, a size a truncated write would produce, so a closing transaction on that day could be missing. The CTO's completeness condition (each partition at least 95 percent of the prior day's) is the guard against exactly that.
- **The mechanism:** the guard exempts an account only through the directory's TERMINATED mark, which the directory's writer cannot produce for an account absent from its source (D2-W417-S3). The CTO ruled one never-widen pair for both firms for a gate exemption with a completeness condition and a manifest record (msg 8284); it is being built as IB-pr-576 (workstream ~PG, LOCAL).
- **My defects in this round, fixed and disclosed:** my order's sparse grant omitted the writer's directory (W418-S1) and an unused variable in my own check was caught by the commit gate. No criterion was weakened.
- **Row:** disposition row D2-S198 (D2-W418-S2 stays ARMED, owner me).

## Judgment criteria

None this round (judgment=0).
