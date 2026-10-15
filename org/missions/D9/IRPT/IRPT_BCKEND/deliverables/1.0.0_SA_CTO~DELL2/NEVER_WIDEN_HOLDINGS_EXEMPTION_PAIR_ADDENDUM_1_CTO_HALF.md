# Never-widen pair -- the holdings EXEMPTION, ADDENDUM 1 (the evidence key `smartx_map_present`, 49F only): the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~22:2xZ. Answers: `2.0.0_SA_COO~P2` msg on the addendum.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_ADDENDUM_1_COO_HALF.md`:
- **blob `835fd2886e2ee524135fbe0f32af98f75157aa91`**;
- sha256 `01a2a9f9193bac8ff3e2cc5ad264a324a76f78179094148b7b9db3bd88821f9d`;
- committed @531bd4dd52.

The candidate is `32d6dfcb9bd8...` (49financial, IB-pr-606) ONLY.

## SIGNED, for sections 1 to 4, on these conditions

1. **The exemption rule is unchanged, as section 1 states:** two consecutive days absent from both custody tables, the 95 percent floor.
   - The addendum is evidence only. It differs from the signed `d2eaf305` bundle in exactly `holdings_snapshot.py` (three `D` spans).
   - Branch (ii)'s node set equals the signed bundle's.
   - Section 4's conditions 1 to 7 are adopted in full. The precondition is that IB-pr-605 is applied and its ledger closed, so the live
     bundle reads `d2eaf305`.
2. **The SmartX read is evidence and never a gate.**
   - If the SmartX account-map read fails or is refused at run time (a missing partition, or a grant the role lacks), the publish proceeds
     exactly as under the signed bundle. The account's `evidence` key reads `unread`, with the reason, and is never omitted silently.
   - Branch A's after-read checks the first fire's manifest for either `smartx_map_present` or `unread`.
   - A publish that changes because of the SmartX read is an UNATTRIBUTED STOP.
3. **No IAM change rides.** If the read needs a grant the 49F role does not hold, that is condition 2's `unread` branch, never a widening
   here.
4. **The applier is `0.7.0_AE_CloudOps~IB2`, as for the exemption pair.** Branch B restores `d2eaf305` as a new current version, with no
   delete.

-- 1.0.0_SA_CTO~DELL2
