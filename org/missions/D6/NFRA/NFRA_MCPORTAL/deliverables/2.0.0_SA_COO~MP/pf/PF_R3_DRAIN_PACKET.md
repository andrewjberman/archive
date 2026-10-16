# NFRA_MCPORTAL -- WORKSTREAM PF ROUND 3 DRAIN PACKET (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-16 ~03:5xZ

**Workstream:** PF round 3, the CTO's round-2 analysis (msg 34676, `ledger/ROUND_ANALYSIS.pf-round2.md` @bfe9f3549c): S1, S2, R2. Decomposition v13 (PF3.x).
**Risk:** MP-pf-4 carries WORLD (the L6 gate floors an `infra/` path), MP-pf-5 LOCAL, MP-pf-6 SERVED. **One judgment criterion owed now:** `MP-pf-6` AC3. **Not yet gradable:** S1's served arm and its live screenshots.

## Orders: 3 of 3 terminal

| Order | What it built | Merged / complete |
|---|---|---|
| MP-pf-4 (S1) | two handler tests: an owning-firm `firm:` key outside `tool_index` never makes a segment (negative arm), a `tool_index` `serves` pair does (positive arm); the seam probe over the real catalog | merged @8ef1398867; complete @667694d05f. Handler unchanged. AC1 2 of 2, AC2 PASS (99 tool_index rows, 273 owning-firm keys outside them, 0 extra pairs). Mutant control: a firm read from `channel_artifacts` planted into the handler fails the negative test. Drain check: admin suite 116 passed, 0 failed, 0 seam failures |
| MP-pf-5 (S2) | a CSS-only scroll cue on every `.gateway-scroll` box (four background layers, `local` covers and `scroll` shades in the ink token at 0.18) and one test | mcportal `090b9cd` (LOCAL on branch `wk-NFRA_MCPORTAL-35-mcportal`; asked of MSTR~Z to fast-forward origin DEV from 421f8fb); workspace merged @f9024516fe; complete @667694d05f. bun 71 pass 0 fail, tsc rc 0, build rc 0 |
| MP-pf-6 (R2) | the principal-set comparator with four planted arms, and ONE real read over SSM | merged @92dbb7a07e; complete @21f171d0ef. AC1 4 of 4, AC2 PASS (a measurement criterion) |

`python .tools/round-close-check.py --project NFRA_MCPORTAL --round 3` counts 8 orders in its scope (it counts by the order files' round and workstream tags; I did not re-derive the other 5), 6 proofs structurally valid, verdict=REFUSED on exactly one thing: `JUDGMENT TO-MP-pf-6 AC3 -> UNGRADED`.

## THE JUDGMENT CRITERION FOR THE CVO -- MP-pf-6 AC3

The question: does the grant writer's change history serve as an independent enumeration of who holds a grant (the CTO's ruling 4 on your Z-C-S40)? Evidence: `deliverables/0.9.0_WK_NFRA_MCPORTAL~36/r2_run.json` and `r2_read.txt` (digests and counts only).
The read (SSM command 66e403c1, the host instance role): the grant store's Scan returns **1** principal; the writer's table `mcportal-grant-changes-table` holds **1** item over **1** page, 0 unparsed, giving **1** distinct principal; `equal` false, only_scan 1, only_history 1.
My own read at ~03:2xZ (command a9f00f73) printed the item with its ids masked: `action narrow`, `verdict REFUSED`, `reason NO-OWNER-HEADER`, `who UNVERIFIED`, dated 2026-09-29, ids of the placeholder pattern `00000000-0000-4000-8000-0000000000e5` and `...f6`. So the writer's history holds a refused attempt by a placeholder principal and **no grant**, and the real grant (1 principal in the store) was written another way. The writer is not the only writer today, so its history is not an independent enumeration.
The worker's caveat (scan side hashed raw ids, history side canonical) does not hold: `_scan_principals` returns `canonical_guid` values and the probe canonicalises the history side too.
What it does not show: which side is "correct" beyond the above; any grant written without a changes row beyond this one store; anything past one read at one instant.
Departure from the CTO's wording, ruled by the issuer inside its decomposition (PF3.3): the order grades the MEASUREMENT (both denominators at least 1, one successful read, nothing dropped), not equality, because an equality criterion would FAIL on the world. A source that IS independent (make the writer the only writer, or another enumeration) is the CTO's to name.

## S2 (MP-pf-5) -- the one real run, for your reading (not a judgment criterion on the order)

The fixture rendered through the real `GatewayView` and CSS at mcportal `090b9cd`, in a real browser at a true 390 px: `scrollWidth` 390 of 390; 17 of 17 scroll boxes are cut and carry the cue; a shade sits on the right edge at the start and on the left edge once scrolled to the end. Screenshots `pf/evidence_cue_090b9cd/pf_cue_390_top.png` and `pf_cue_390_scrolled.png`.
One cosmetic note, not changed: at the end of the scroll a faint white band shows on the right, because the cue's cover is white and the summary table sits on the light canvas.

## S1 (MP-pf-4) -- NOT REALIZED, and the served arm is not yet runnable

The segmentation is graded only on the served page (CTO ruling 1). `pf4.served.sh` (mine) reads EC2_MANIFEST `deployed_commit` and `mcportal_commit`, then the SERVED `_compute` over SSM, and prints the denominator. At ~03:5xZ it reads FAIL: deployed `d577e0e7297b` does not descend from `54a75d46ba`, mcportal_commit `17dcbb286` does not descend from `421f8fb`, and the served page lists m365 with 76 tools and no segments. It waits on NFRA_MCPINDEX `TO-MX-r-15` and NFRA_OPLGTW `OG-ap-23` (`2.0.0_SA_COO~O`, queue order per `~MI`: OG-ap-23 first, then MX-r-15). Item (iii), the live screenshots at 1280 and 390 px, is graded by you after that run.

## Rows

`Z-W35-S1` (ARMED, the worker's, the issuer's defect: a check that takes its root from the cwd) is disarmed by `Z-S61` (amendment d4d4311f15). No other row this round. Call f643 (regroup the integration channels by bucket) was ruled KEEP by the CTO at 03:32Z; no cell owed.
