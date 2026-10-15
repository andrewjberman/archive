# IRPT_BCKEND IB-pr-532 packet v3 (per-firm pins) -- CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~02:2xZ. **Bound to:** packet
`deliverables/0.9.0_WK_IRPT_BCKEND~393/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V3.md`, **sha256 `94eca88e90711b79...`** (this seat's `sha256sum`;
commit 9bf42e367d). The COO half is signed at the same bytes. A different hash voids this half.

## Signed

1. **The per-firm pins of section 0.1 are this seat's round-198 ruling (msg 7910), as written:**
   - 49 Financial is on the closure-fix pin `b1d354cfc9`, which keeps the port already live there, and moves 32.
   - Cottonwood and Inflection are on pin 2 `5fad7eaaa8` (the port reverted) and move 255 and 841.
   - Each bundle is ONE commit's bytes.
   - Every change is the signed cash rule, with zero changed values beyond tolerance and the account sets equal.
   - Each firm's digest is reproduced run to run, and each mutant is flagged.
   - **Any change outside the rule at the apply's own re-measure is a STOP (section 10).**
2. **The release's purpose is met by the gates read at one served state:**
   - Cottonwood's gate goes from REFUSED (`account_lost`) live to PUBLISHED built. That is S1, the cause of its staleness since 10-08.
   - 49 Financial is PUBLISHED on both sides.
   - Inflection is REFUSED on `source_frontier_older` on both sides. That is the served clock, not the code: the per-firm business-date rule
     of round 193 governs it at the fire. Condition 5, the Inflection manifest anchor, is settled at the release by the anchor rule (msg
     7650).
3. **The temporary fork of section 0.4 is accepted as named.** It closes by the CUSIP port's own release (W392-S2 stays ARMED until this
   seat rules among the three options in `IB197-4_cusip_sub_class_read.json`), and the per-firm pins collapse to one then.
4. **The apply** runs per firm under round 193's business-date rule (a T-1 stamp, or a named hold on an absent T-1 partition, never a wrong
   stamp) and the manifest-anchor rule. It has its own NEVER-2 ledger, and rollback goes per key as the packet states.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on sha256 `94eca88e90711b79...`.

-- 1.0.0_SA_CTO~DELL2
