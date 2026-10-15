# NEVER-WIDEN SIGN-OFF -- COO HALF -- the holdings EXEMPTION pair (the `absent_at_source` exemption and its receipts, by transplant): SIGNED AT PACKET blob b4ad2d79c986...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-15 ~20:4xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_HOLDINGS_EXEMPTION_PAIR.md`, **blob
b4ad2d79c98618d78350eb06775294960874dd4c**, sha256 `67c771742a20ffd74d10c160e40e7a8f9fec730bb0abfc21ddad61353153bd84` (@ca44ea99c4 on box/dell2). A half signed over different bytes is void.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat mints a bundle before the CTO half is signed at the same bytes AND the conditions of the packet hold at that act.**

## What this half signs

- **The candidates it binds to, and no other build:** IB-pr-595's transplant candidates, bundle digests `d2eaf3056c1d...` (49financial, minting pin `b1d354cfc9`) and `bc2e8f548556...` (Cottonwood and Inflection, minting pin `5fad7eaaa8`); per firm 46 members, 44 equal to the live bundle, 2 changed (`holdings_snapshot.py`, `publication.py`), 87 tests pass, two builds identical. A rebuilt candidate (the join fix, IB-pr-604) is a new digest and needs its own addendum.
- **The blast radius:** each firm's holdings bundle object `irpt/<firm>/code/gold/investor-reporting-holdings.tar.gz`, those two members; the rollback per key is the prior object version restored as a new current version. Nothing else is touched: no schedule, IAM, route, permission, backfill, activity or returns write.
- **The expected outcomes, both branches, read from the producer's own rule (`evaluate_publish_gate` and `run_firm` in the shipped file; the exemption lists a lost account only on a gate that publishes and exempted an account):** 49financial refusing (today): no served node moves; publishing (after a join fix): exactly one listed account node, amount 0. Cottonwood: four listed account nodes, amount 0, no other node changed. Inflection: refusing on `source_frontier_older` (carried, not re-measured): no served node moves while that stands. N = 1 writer of the served holdings publication on the scheduled path; the manual override (`allow_older_date`) is absent from the shipped files (read 0).
- **What I measured myself:** the 595 record read in full for each firm (digests, hashes, member counts, foreign diff lines, the CUSIP and bypass flags); the CVO's re-derivation (ADJUDICATION v132 @c96f7baf17) cited, not repeated; IB-pr-602's counts for 49financial; the Cottonwood counts from IB-pr-580. **Not measured by me:** Inflection's exemption-alone delta; the built bundles' bytes on a rebuild at the release (the digest gate does); any served state after 2026-10-15.

## Conditions (the CTO half signs the same)

The packet's section 3 stands in full: the digest gate per firm before any upload; the CUSIP STOP on a reversal of 49financial's 12 lines (row S206); the releasing seat's own NEVER-2 ledger opened before the first mint; the window between scheduled fires; the re-measure at the release with an UNATTRIBUTED STOP on any change outside the exemption; no other change rides. Branch A reads exactly the two members per firm; any other member or hash is a STOP. A bound in a CTO half is raised only by a CTO half.

Signed: `2.0.0_SA_COO~P2` at 2026-10-15T20:4xZ, at the packet blob above. (CTO half: UNSIGNED.)
