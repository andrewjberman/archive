# IRPT_BCKEND round 1, workstream ~PD (the split-adjusted holdings price return: the READ) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~12:2xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @a8b2b72549 on the CTO's ruling @9913bf3ed4 (msg 8251): IB-pr-572 `complete` (merged @af479072d6). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PD"` reads `MAY-CLOSE`. I re-ran IB211-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY: the producer was not run and nothing was written, published or invoked; no CUSIP and no account id is in any tracked file.**

## What the CVO needs to know

- **The defect, in the code:** `holdings_performance.py` line 816 computes the price contribution as `v * (p1 / p0 - 1)` with neither price split-adjusted, so a holding whose value did not change reads as a loss of about (N-1)/N on an N-for-1 split day.
- **The ruled key exists on one firm only.** The CTO ruled the split row is the `(tran_srcde, tr_cd, sb_cd)` STK "STOCK SPLIT" row. 49 Financial's transactions carry those columns (572 partitions, 3,349,750 rows, 1,348 STK rows all describing a STOCK SPLIT, 47 split days, 76 security-days: 75 measurable, 1 `SPLIT_RATIO_ABSENT`). **Cottonwood's Black Diamond feed and Inflection's Orion feed carry none of the three columns**: Cottonwood names splits in text types (Corporate Action Split 70, Reverse Split 74 over the first 124 partitions), and Inflection's 4.63 GB feed was not classifiable by this read. So the split key per firm is a declaration still to be written, and the build cannot be cut as ruled for those two (row W415-S1, BLOCKING for the build).
- **Three numbers the pair must settle:** 17 of the 75 measured custodian ratios disagree with the close-price ratio at the worker's stated 2 percent tolerance (which governs on a disagreement is a ruling); the read counts 985 distinct accounts holding one of five split securities at t-1 on 2026-04-21 (846 hold the 6-for-1 security with no same-day activity) against the ruling's 920 graded account-days, which this read did not reproduce (the 920 is the guard's graded set); 49 Financial alone has 1,291 affected (account, day) pairs over the 47 split days, so the DELTA is a lower bound until the other two firms are keyed.
- **The input:** the producer's declaration names no transactions prefix for any channel (49 Financial's sits in the `irpt_reporting` sources file), so the pure core needs a per-(security, day) ratio table input and a declared split key per firm.
- **Rows:** disposition row D2-S195 (D2-W415-S1 stays ARMED, owner me). Nothing is built; the build and the never-widen pair follow the CTO's answer on the key and the ratio.

## Judgment criteria

None this round (judgment=0).
