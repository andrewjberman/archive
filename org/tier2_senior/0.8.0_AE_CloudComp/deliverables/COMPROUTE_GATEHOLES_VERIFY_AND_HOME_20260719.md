# NFRA_COMPROUTE gate-holes -- VERIFY-at-source + HOME (2 holes from ~Z's routing survey)

**From:** 0.8.0_AE_CloudComp~D  **For:** 2.0.0_SA_COO (homing/reopen decision) -> 1.0.0_SA_CTO (fix arch-gate)
**Date:** 2026-07-19  **Ask (COO @231245Z, MSTR-ruled):** verify LIVE (not theoretical), home under COMPROUTE (don't re-orphan), fix IF in-lane via the REVISE flow; arch-decisions route via COO to CTO.
**Source of the holes:** ~Z routing/SoD survey @368575ed6 (deliverables/NFRA_COMPREG_ROUTING_SOD_SURVEY_20260719.md).

## Verdicts (both grounded AT SOURCE, not from the survey alone)

### HOLE 1 -- no-rank-1-THEFT assertion -- LIVE + REAL (the sharp one)
**Claim:** comp-which-routing-test asserts self-route regression but NOT whether a NEW tool STEALS an EXISTING tool's rank-1 (comp-genesis stole comp-system's rank-1; the automated test PASSED; caught by hand).
**Verified:**
- `.tools/comp-which-routing-test.py` (full-file grep): ZERO theft/displacement/cross-tool-rank-1 concepts. Its BASELINE is the COVERAGE-metric baseline (cohort-R zero-score rate), NOT a per-tool rank-1-stability comparison.
- `manifest_check_cli.py` member-3 (self-routes): HARD-BLOCK on MISS (a tool doesn't surface for its OWN use_case), WARN on NEARTIE (surfaces, not rank-1). So theft manifests as the VICTIM flipping RANK1->NEARTIE = a NON-BLOCKING WARN, buried among other WARNs -> passes the gate, missed by hand. CONFIRMED real.
**Already homed:** NFRA_COMPROUTE.json follow-ons field ALREADY captures it -- "the CROSS-TOOL RANK-1-THEFT routing-test gap [CTO-routed 2026-07-18, COO-captured]." NOT orphaned; this deliverable confirms + grounds it.

### HOLE 2 -- required routable-flip / curated-rule step -- LIVE but PARTIALLY covered (softer)
**Claim:** a tool can land registered-but-unreachable (comp-describe/comp-kuzu needed a routable false->true flip; 12 tools posterior-only, 2 fail to route live).
**Verified:**
- member-1 (routable) DOES enforce `routable=true` for every tools_index tool (else comp_route.py drops it from candidates BEFORE scoring) -- so registered-AND-routable=false is BLOCKED.
- BUT there is NO hard-required CURATED-RULE step: a tool can be routable=true yet have no curated comp-which rule -> posterior/fuzzy-only -> may not win a live route (member-1's own :108 note records the 2026-07-09 case: comp-routable-check PASS over 42 tools while live routing failed = routable-flag != live-reachability). member-3 WARNs on the NEARTIE/posterior-only case but doesn't hard-require a curated safety net.
- So hole 2 = the missing REQUIRED-curated-rule (live-reachability) step, PARTIALLY mitigated by member-1 (flag) + member-3 (WARN). Real, but softer than hole 1.

## Fixes = ARCH-DECISIONS (route to CTO via COO -- NOT self-built here)
Both are new/sharpened GATE members, and hole 1 hits CTO's OWN doctrine directly:
- **Hole 1 arch-tension (for CTO):** CTO's ruling (in the harness) = "every hard-blocking member asserts a DETERMINISTIC fact; anything THRESHOLD-shaped REPORTS." Rank-1-theft is a SCORE-MARGIN event (a new tool edges out an existing tool) = threshold-shaped -> by that doctrine it WARNs, not hard-blocks. So the fix is likely a SHARPER, DEDICATED theft WARN -- "registration of tool Y DISPLACED tool X's rank-1 on query Q" -- distinct from + more surfaced than the generic buried NEARTIE, computed by comparing per-tool rank-1 verdicts before/after against the frozen cohort. Whether it can be made a DETERMINISTIC hard-block ("a registration commit must not flip any OTHER tool RANK1->not-RANK1") is the CTO call.
- **Hole 2 fix:** a REQUIRED-curated-rule member (a routable=true tool must also have a curated comp-which rule OR a routing_exempt reason) + a live-reachability assertion (routes rank-1-or-top-k on its own use_case, not just routable=true). Also new-gate-member territory (CTO).
Division note: comp-which-routing-test.py is ~Z's NFRA_COMPASSURANCE-authored file; manifest_check_cli.py is the gate. A fix coordinates with ~Z (routing-test author) + the COMPROUTE owner + CTO (arch-gate). I own the LEG/integration shape if/when CTO gates a member (same as my WS-2 leg pattern).

## Homing recommendation (COO's call)
NFRA_COMPROUTE.json = status COMPLETE, no active owner. Hole 1 already sits in its follow-ons field. Recommend: this deliverable is the durable grounded record; COO decides -- (a) reopen NFRA_COMPROUTE as an increment for the 2 fixes with a named owner + CTO arch-gate, or (b) a fresh fast-follow TO citing this record. Either gives a durable home + routes the arch-decision to CTO. NOT self-building the gate members (arch-decisions, per COO step 3). Then per MSTR I HOLD for Andrew's phase-steer.
