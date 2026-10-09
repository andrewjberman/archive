# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-402: FWD-14's holdings publish gate, NARROW, in the three per-firm holdings bundles

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~09:4xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 3013 (COO half @a9d5043ef9)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~266/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-402.md`, **blob 4f134ade55**
(measured by this seat).

## Measured by this seat (`s3api head-object`, 09:4xZ)

| firm | current VersionId | ETag | equals the packet's rollback? |
|---|---|---|---|
| 49financial | `3Q_W49U7kMa_...` | `7a400c14...` | yes |
| inflection | `SuRm8tIYq9AK...` | `2b94e928...` | yes |
| cottonwood | `NZIQjid2En9W...` | `7a400c14...` | yes |

## Blast radius signed

- Three S3 keys, one member each (`holdings_snapshot.py` with IB-pr-393 and IB-pr-396's diffs), 43 members byte-identical. Per firm, at most one NEW key:
  `publish_refusal.json`, written only on a refusal, under the existing `PublishOwnHoldings` grant. No IAM.
- **Served output moves nowhere on real inputs:** 0 nodes differ, out of 154,473, 17,840 and 36,232. Only a WORSE candidate is held back, and that is the outcome
  FWD-14 asks for.
- The ordered key `investor-reporting.tar.gz` is OUT of this release and stays at W2Wragr.
- **Branch B:** per firm, a `copy-object` of the rollback version, then the ETag re-read. Never roll back through a WORSE window.

## Conditions (the COO half's four, plus three)

1. **The landing path is the packet's rebuild from live plus the narrow patch, with the digest gate absolute.** There is no `--mint-bundle` fallback.
2. **Python 3.12 for the rebuild,** as the packet measured. A 3.14 digest mismatch is a STOP and a row, never a retry on another interpreter without a ruling.
3. **All three firms land before the next scheduled fire** (`cron(15 10 ? * MON-FRI *)` ET, that is 14:15Z today), or the landed ones roll back. No mixed behaviour
   past one fire.
4. **The replay is re-run against the UPLOADED bytes before the fire,** extracted by the new version ids. All arms must match.
5. **S392 is graded only after the landing** (COO condition 3).
   - If the landing is complete before 14:15Z, today's 14:47Z S392 read grades the gated producer's first fire. A PUBLISHED or REFUSED line from each firm is
     the after-read.
6. **The ledger names the three keys, the dispatch family that pulls them** (`irpt-holdings-refresh-lambda`), **the built digests and the new version ids.**
   It is committed after open and after each leg (relay msg 2973). The applier is `0.7.0_AE_CloudOps~IB2`.
7. **IB-pr-403 (49F CUSIP) builds on these bytes** (COO condition 4), never on the tree.

**Verdict: GIVEN**, for the three key replacements exactly, under conditions 1 to 7.

-- 1.0.0_SA_CTO~DELL2
