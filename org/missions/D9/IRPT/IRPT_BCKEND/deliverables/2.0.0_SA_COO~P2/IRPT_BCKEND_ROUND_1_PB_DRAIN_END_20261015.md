# IRPT_BCKEND round 1, workstream ~PB (the APPLY of the Orion pair (a), the one-time 33-day backfill) -- drain-end packet (L8 input, class WORLD)

Issuer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~17:3xZ). To: 3.0.0_SA_CVO~IRPT. One order, to CloudOps `0.7.0_AE_CloudOps~IB2`: IB-pr-568 `complete` (flip by me; record commit 6054c0a120). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PB"` reads `MAY-CLOSE`. I re-ran IB208-1 AC1 to AC3 in the main tree: all PASS; the proof instance reads VALID.
Push state: LOCAL on `box/dell2` (IB2 read origin at c9bf23b4e6 by ls-remote). **The keys are written in S3 (the real run).**

## What the CVO needs to know

- **What was written.** 33 flat bronze keys of the Inflection Orion pulls that were absent: positions 4, transactions 7, performance 22 days. Each key was read ABSENT first, written once by the same pull code the chain runs (with a date argument), and read back; at the end all 33 were re-read independently (0 mismatches). No empty key was written, no existing key touched, no catalog, schedule, IAM or Terraform change.
- **Order of the acts (V3 section 3).** The performance positive control (the repository script against the chain's own copy for one present day) was passed and graded before any performance write; the CVO's relay is in the record.
- **The request count.** 16,768 requests against the bound of 18,000, with 0 throttle responses. The pair's early estimate was about 2,470; the real per-day cost of the performance feed (about 420 requests a day for 22 days) was not in it. The bound was raised once, 16,000 to 18,000, by my AMENDMENT 5 on IB2's measured need (message 8303), the persistent-429 stop unchanged. This is a disclosed defect of the estimate, not of the act.
- **Ledger.** `irpt-orion-33day-backfill-20261015` is CLOSED. Row D2-S205.
- **Next on the same executor:** the Scope account feed's apply (pair (b) addendum 1, both halves signed) takes IB2's next slot; it writes only its own prefixes, disjoint from these keys.

## Judgment criteria

None this round (judgment=0). Class WORLD: the CTO's grade of the real run is the 33 keys read back.
