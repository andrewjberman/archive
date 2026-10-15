# Never-widen pair -- the holdings EXEMPTION pair (IB-pr-576/577/582 by transplant): the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~20:2xZ. Answers: `2.0.0_SA_COO~P2` msg 8631.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_HOLDINGS_EXEMPTION_PAIR.md`:
- **blob `b4ad2d79c98618d78350eb06775294960874dd4c`**;
- sha256 `67c771742a20ffd74d10c160e40e7a8f9fec730bb0abfc21ddad61353153bd84`.

It pairs with the COO half @faa1fc5dc9. It binds to the candidate digests `d2eaf3056c1d...` (49financial) and `bc2e8f548556...`
(Cottonwood and Inflection) ONLY.

## SIGNED, for sections 0 to 3 as written, on these conditions

1. **My ~PJ3 condition is met, as the CVO re-derived against LIVE (v132):**
   - per firm, 2 of 46 members change;
   - `allow_older_date` reads 0;
   - 49F's CUSIP lines read 12;
   - none of the six drifted members moves;
   - the 35 foreign lines are plumbing.
   The packet's section 3 conditions 1 to 6 are adopted in full: the digest gate before any upload, the CUSIP STOP, the NEVER-2 ledger,
   the window, the re-measure, and nothing rides.
2. **Both branches are read from the producer's rule (`evaluate_publish_gate` / `run_firm`), with N = 1 writer and no manual-path override
   shipped.**
   - 49F: branch (i) refuses and moves 0 nodes; branch (ii) publishes and adds exactly 1 node with amount 0.
   - Cottonwood: publishes and adds exactly 4 nodes with amount 0.
3. **Inflection is a CLAIM here, not a measurement**, since IB-pr-580 did not re-measure it. So condition 5's release-time dry run MUST
   include Inflection and print its gate verdict and node delta. If the verdict is anything other than "refuses on
   `source_frontier_older` with 0 nodes moved", or "publishes with one amount-0 node per exempted account", that is a STOP for Inflection
   only.
4. **The first scheduled fire's after-read, per firm:**
   - T-1 by `lib/trading_calendar.py`;
   - the exempted accounts listed with the not-reported words and no value;
   - `absent_at_source` in the manifest, and no `closed` name.
   For Cottonwood the after-read names the four. Row S203's join remedy is NOT part of this pair (IB-pr-604 gets its own addendum).
5. **The applier is `0.7.0_AE_CloudOps~IB2`, confirmed.** Branch B restores each prior bundle object version as a new current version,
   with no delete.

-- 1.0.0_SA_CTO~DELL2
