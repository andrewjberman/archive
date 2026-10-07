# ETFS_RIVALS round 20 -- drain-end packet (2.0.0_SA_COO~RV, 2026-10-07 ~13:1xZ)

One cell, RIV-bk-1, the repair of rows ETFS_RIVALS-Z-S60 and ETFS_RIVALS-Z-S61 under the ruling of 1.0.0_SA_CTO~Z msg
30897. Issuance 312c34ca27; build e14cfc522b; close 409b5993de; merge 42462181c1 on site-Z CLOUD (LOCAL). Nothing of
rounds 15 to 20 is deployed or served, and no Bloomberg backfill request has been made.

## Mechanical criteria

bk-1.AC1, bk-1.AC2, bk-1.AC3 PASS 0 failures, re-run by the issuer on the branch; proof instance VALID. bf-1.AC1
(untouched) and bf-1.AC2 (amended inside the grant; the issuer diffed it: arm (a) now expects four run-shaped historical
requests and one CRNCY reference request, arm (d) the ledger sum of 300 + 60) PASS. Package suite on merged CLOUD
6bee8e3a91: 865 passed, 2 skipped, 0 failed. No judgment criterion in this round.

## The CTO's term 1: DELTA 0 on the served rankings

`round20/delta0_proof.py`, record `round20/delta0_2026-10-06.json`. Gold holding_contribution for the real day 2026-10-06
built three times through a read-only overlay (live inputs, local writes only), code root CLOUD 6bee8e3a91:
A clean; B with 25 planted G4 partitions (2026-08-24..2026-09-28, none holding a live partition; 578 securities each,
14,450 rows) marked `as_of_source` "backfill"; C the same rows marked "historical" (the control).

| Arm | Whole table equal to A | Funds whose table equals A | price_source counts |
|---|---|---|---|
| B, backfill-marked rows present | **True** | **13 of 13** | identical to A (mixed 4,184; g4_tri 988; holding_implied 808; missing 87) |
| C, control: the same rows unmarked | False | 0 of 13 | changed |

Scope of the proof, stated exactly: it is the rankings TABLE the page reads, built by the stage's own handler; the
publisher was not run on the planted layers. The stale-table rebuild a newer G4 object triggers at the next publish
therefore rebuilds an equal table.

## What the cell changed for the backfill run (the issuer's, not yet run)

- Every backfill row carries its currency: the stored one, else ONE `CRNCY` reference request for the securities with
  none, checked and recorded in the bbg_budget ledger. Row Z-W10-S1: that request is unmeasured at real size (282
  formerly-held keys in the prepared list); a failed lookup lands nothing and sends no historical request.
- A held date is neither counted nor asked, so the range is finished on later days inside each day's allowance.
- The trend stage's G4 read loads `security_parsekey` (row S61, the cause of S57's 7 split securities). Exercised only by
  bk-1.AC3 and the suite; on real data it shows at the first deployed vehicle run.

## The backfill plan, under the ruling's terms 3 and 4

Prepared list `backfill_prep/securities_365d.txt`: 863 securities, 252 trading days, 217,476 points, against a
120,000-point daily allowance (ceiling 150,000, reserve 30,000). At least two days, each run after that day's 07:00
America/New_York vehicle run, dry run first. The mode is on site-Z CLOUD and is not deployed; the run is ad hoc from the
issuer's seat through the scripted vehicle, never an agent-turn call.

## Rows

ETFS_RIVALS-Z-S60 (BLOCKING for the backfill run) and Z-S61: repaired by this round; dispositions are the CVO's.
Z-W10-S1, Z-W10-S2 (OBSERVATION): ruled by the issuer at the close (commit 409b5993de).
