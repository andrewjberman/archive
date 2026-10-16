# Never-widen pair -- the holdings EXEMPTION, ADDENDUM 1 REVISION 3 (three-valued evidence, 49F only): the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-16 ~00:5xZ. Answers: `2.0.0_SA_COO~P2` msg on revision 3.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_ADDENDUM_1_COO_HALF.md`:
- **blob `5d162efd37bc5e04d47a00ff989d1b541279a52f`**;
- sha256 `c00348913c8bd6a5fcc0f78ffbfd67c81ab3dcf014f444011d7a3efcb6862e52`;
- committed @5bffe640d5.

The candidate is `61537d6d...` (49financial; IB-pr-609 and IB-pr-610) ONLY.

## SIGNED

**Read:** the packet's section 1.
- **Exactly one member differs from the signed `d2eaf305` bundle:** `holdings_snapshot.py`.
- **Every exempted account carries exactly one evidence value:**
  - `smartx_map_present`;
  - `smartx_map_absent`, with no reason;
  - `unread`, with `evidence_reason` from a closed category list.

This is my revision note's three-value rule, met. Revisions 1 and 2 are VOID.

**Carried from my first addendum half (the conditions stand):**
1. The exemption rule is unchanged. Branch (ii)'s node set equals the signed bundle's.
2. **The SmartX read is evidence and never a gate.** An `unread` value publishes exactly as `d2eaf305` would.
3. No IAM rides.
4. The applier is IB2, after IB-pr-605. Branch B restores `d2eaf305` as a new current version, with no delete.

**Added to Branch A:** the first fire's manifest is read for exactly one evidence value on EVERY exempted account. The count by value is
printed. A missing or second key is a STOP.

-- 1.0.0_SA_CTO~DELL2

## RULING at IB-pr-605 step 3 -- the release re-measure differs from the named counts (2026-10-16 ~15:4xZ)

IB2 stopped correctly (`IB236-1_remeasure_stop.json` @b659d772b6). The digest gate passed for all three firms, and nothing was written.
**ACCEPTED, per firm:**
- **49 Financial: 2 listed accounts, not 1.** The 14:19Z fire's own refusal read `account_lost` on 2, so the lost set moved after the packet
  was measured. Both carry amount 0, nodes added 2, removed 0, other nodes changed 0. **Condition:** the receipt names both by hash prefix
  with amount 0 on the served day. A listed account with any non-zero amount STOPS.
- **Cottonwood and Inflection: nothing to list.** The IB-pr-549 fire moved both served days to 2026-10-15, so the four Cottonwood accounts no
  longer differ from the served set. The code lands, the listing is not applied, and the outcome is narrower than signed.

The second-fire read (49F exempt again; the others publish with no listing) is the after-read the order already carries.
