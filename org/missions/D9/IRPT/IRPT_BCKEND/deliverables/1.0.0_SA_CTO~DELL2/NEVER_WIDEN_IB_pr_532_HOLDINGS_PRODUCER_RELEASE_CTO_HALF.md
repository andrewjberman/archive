# NEVER-WIDEN -- IRPT_BCKEND IB-pr-532, one holdings-producer release (the cash rule on both layers + the exemption repair) -- CTO half

**Signed by:** 1.0.0_SA_CTO~DELL2, dell2, 2026-10-14 ~05:3xZ.
**Bound to:** the packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~379/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532.md`,
sha256 `4129abf31f3d402d72de9778c0cc32d7114fd414105cc24ac169893696e28504`. This seat computed the hash with `sha256sum` at signing; it
equals P2's (msg 7547).
**COO half:** `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_532_HOLDINGS_PRODUCER_RELEASE_COO_HALF.md` @26d98874cb.

## SIGNED, on these terms

1. **Writers counted: 2 rules read.** The served `asset_class` of a holding is set at the two returns of `classify_security`: the canonical
   branch (IB-pr-527) and the bd-securities fallback (IB-pr-529). One definition, `apply_cash_rule`, is called at both. It changes
   `asset_class` only, and only where the sub-class reads cash. Sub-class, basis, weights and totals do not move.
2. **Blast radius, as the packet measures it from the producer's own rules on each firm's 2026-10-12 candidate:**
   - 49financial: 32 nodes to cash (32 canonical, 0 fallback); gate unchanged, PUBLISHED.
   - Cottonwood: 249 nodes to cash (38 canonical, 211 fallback). Its gate goes REFUSED to PUBLISHED with ONE lost account listed (count
     only), and no other condition differs.
   - Inflection: 841 nodes to cash (774 canonical, 67 fallback); gate unchanged, PUBLISHED.
3. **Both branches.**
   - Branch A: `--mint-bundle` of the three firm bundles, carried by the next scheduled fire, `irpt-holdings-snapshot`, cron `15 10 ? *
     MON-FRI *` America/New_York.
   - Branch B: restore each bundle's prior object version by version id, read at the release. The manifest version served now per firm
     is named in the packet.
   - What cannot be undone is named: a date already published, and a page already fetched.
4. **The stop rule binds.** At the release, the per-firm canonical and fallback movers, the lost-account count, and the gate outcome and
   conditions must equal this packet, or the release stops and the packet is re-cut. Cottonwood's fallback is compared with 211, not
   round 189's 215 (row D2-W379-S2).
5. **The releasing seat opens its own NEVER-2 ledger at start** (`--mint-bundle` opens none). Its legs:
   - the three mints;
   - the first scheduled fire's after-read per firm (`current/manifest.json` latest_date; for Cottonwood, a business date past 2026-10-08
     with 1 lost account listed);
   - FDRXX and the other cash-sub holdings reading Cash on the published page;
   - 49financial's 2026-10-08 gap unchanged.
   The ledger closes only when every leg carries proof.
6. **The release pin is re-read at the release.** The producer blob `3a19dcf591` at the packet's base `49467335d2` is the claim. If the
   blob at the release pin differs, that is a stop, not a re-sign.
7. **Not covered by this half:**
   - any backfill of 49financial's missing 2026-10-08, lost when its 2026-10-09 fire was killed on the SSM execution timeout (a
     separate act and pair, ruled below);
   - any change to the schedule, Lambda, SSM or IAM configuration.

## Ruling carried (49financial 2026-10-08)

The served index lacks one trading day, 2026-10-08, for 49financial. The release must neither widen nor hide that gap.
- A one-date replay of 2026-10-08 is the remedy, as its own cell with its own pair, after this release's after-read.
- The same cell reads why the 2026-10-09 fire hit the SSM execution timeout, so the next long fire does not repeat it.
- Until then the page shows that date as not published, in words.

## Disarms on this release's after-read

D2-S158 (Cottonwood serving 2026-10-08) and the Holdings-page cash item from Andrew's smoke test (FDRXX reading CASH).

-- 1.0.0_SA_CTO~DELL2
