# L8 drain end -- IRPT_BCKEND rounds 75 and 76, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~13:xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (round 76's
IB-pr-363 re-pins a source-map row; nothing was built, uploaded or applied in either round)

**Judgment criteria:** 0. Every order below is terminal, its proof instance VALID, and every mechanical criterion was re-run by the
issuer on the worker's branch before the drain.

## Round 75 -- IB-pr-361, slot ~169 (issuance @2b21386c19, decomposition section 68)

**What it did:** regenerated ~P's four drifting portal wire files (ExportBundle, ExportReceipt, responses, index) from their contracts
(row S388, ~P's share). Portal branch `wk-IRPT_BCKEND-169-portal`: c0291b68 (regen) + f63c5fdd (fixture).

**AMENDMENT 1 @63db9c46c6 (the issuer, on row W169-S1).** The regenerated `ExportReceipt.ts` makes `facts.covered_account_ids` required,
as the contract has since IB-pr-343; one consumer fixture lacked it (TS2741). The issuer granted that one file. The edit is one line:
`covered_account_ids: ['acct_test_1']` added to the fixture's `facts`, nothing else changed. Gate limb: none graded the amendment (a
modification; GATE viii only).

**Graded (re-run by the issuer on branch 169):** IB75-1-AC1 PASS (4 of 4 files equal the generator's output), IB75-1-AC2 PASS (tsc -b
--noEmit rc 0), IB75-G-169 PASS. Proof @2874a10e7f VALID.

**Not moved:** the portal branch is a DEV candidate. DEV lands on Andrew's word; nothing was pushed.

## Round 76 -- the CTO's rounds 69-74 enrichment (issuance @0fdb85697e, decomposition section 69)

### IB-pr-362, slot ~170 (E1): the four ARMED rows

| row | ruling | evidence / disarm act | owner |
|---|---|---|---|
| S334 | ARMED | bound the comp-tagauthz gate's IAM read | `1.0.0_SA_CTO` |
| W140-S1 | DISARMED by W170-S1 | portal DEV d1b21c970c carries IB-pr-341 (5c726cf4); ir-62-overage 10 pass / 0 fail | -- |
| W145-S2 | DISARMED by W170-S2 | `release-census.py irpt-export-render --pin b921635dad`: changed_members=0; `test_retained_finalize_names_accounts.py` 6 passed | -- |
| W165-S2 | ARMED | land portal 63b9382a on DEV (not an ancestor of DEV d1b21c970c) | `0.0.0_AB_MSTR~DELL2` (Andrew's word) |

ARMED after the round: **2 of 4**. Graded: IB76-1-AC1 PASS, IB76-G-170 PASS. Proof @c7c99b2967 VALID.

### IB-pr-363, slot ~171 (E2): the custody release packet

- **Release pin 1e0cdaf90c.** One row, one function: `irpt-export-render`'s `entry.py` `staged_from` row moves 34f71024a1 -> cf6839fe38
  (the IB-pr-355 commit). The issuer confirmed the pinned blob c92600b8 equals HEAD's, and that cf6839fe38 contains b921635dad
  (the IB-pr-349 release). Without the re-pin IB-pr-355's ROUTES lines would not ship.
- **Census at the pin:** entry.py (IB-pr-355), submit_async.py (IB-pr-352), custody_read.py added (IB-pr-355). No rider.
  `reports/custody_write.py` is packaged by no function (IRPT_CUSTDY's producer calls it).
- **Rollback:** artifact version `ZBwAzArTtDSpCIYL8CwhqqmIooS4mVPx`; live CodeSha256 `aRCgH9B0pglos8cPiybPhmJShzjUts/Tr5R9R/AZYJw=`.
- **The route** `GET .../custody-report/{reportId}` is not live; the packet orders the function deploy before the api apply.
- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~171/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md`, **blob 2af2b30af8b62f48062151c9c700c66665db4a9b**
  (the first draft, blob ab5ef617, failed AC2 and is superseded).
- Graded: IB76-2-AC1 PASS (census reproduced at the pin), IB76-2-AC2 PASS, IB76-G-171 PASS. Proof @d0548c5536 VALID.
- **COO half:** `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_363_CUSTODY_RELEASE_COO_HALF.md`, signed against that blob. The CTO
  half is owed by `1.0.0_SA_CTO~DELL2`. No apply follows until both halves are at HEAD and a release order is cut.

## Rows

| row | status |
|---|---|
| W169-S1 | Resolved by AMENDMENT 1 (the fixture). |
| W170-S1, W170-S2 | New, DISMISSED_WITH_REASON; they resolve W140-S1 and W145-S2. |
| W171-S1 | New, OBSERVATION/INERT: `infra/aws/terraform/investor-reporting/api/routes.json` is a stale second carrier that `routes.tf` does not read. |
| S334, W165-S2 | Still ARMED, owners named above. |
| S388 | ~P's share closed by IB-pr-361; AnalysisReport (~G2) and HoldingsSnapshot (dell1 via ~M2) remain with their owners. |

## Drain note

The first shared-tree drain of branch 169 held MERGE_HEAD ~40 min (the row gate is slow on this box) and blocked other seats (MSTR msg
1242). It was aborted clean; CLOUD was merged into 169 in its own worktree (@47fa8554b9), 170 and 171 folded there, and the result
drained once.

**Push state:** LOCAL at the time of writing.
