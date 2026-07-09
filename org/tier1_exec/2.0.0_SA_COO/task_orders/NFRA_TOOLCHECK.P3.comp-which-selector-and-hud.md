# Task Order: NFRA_TOOLCHECK P3 -- COMP-WHICH SELECTOR + HUD ASSESSMENT (routing-oracle green + HUD calibration)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-toolcheck-p3-selector-hud</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp (comp-which selector + the HUD/COMPHUD rail) -- EXECUTED as base 0.8.0_AE_CloudComp post-respawn 2026-07-09 (TO originally named the ~D lane; base lane carried it after the 073939Z wedge-respawn) | CTO arch-gate + CVO routing-oracle-green + HUD-measured cert (ALL MET)</issued_to>
    <date>2026-07-08</date>
    <status>complete 2026-07-09 -- both legs CVO-certed + CTO P3-phase-close DECLARED (084508Z). SELECTOR leg: comp-system router-wire (5d21baa6f), live oracle 37/38 -> 38/38 GREEN, CVO oracle-GREEN cert 080106Z (deeper cause = candidate-set exclusion, system-compiler not in _ROUTABLE_META_ROLES; fix = role-add + curated rule, non-regression exercised). HUD leg: req#3 a-d (c37c6ab27), each exercised against the live hook, self-gating log-truncation found+fixed (head -c 80 multi-line split), AC#2 honestly measured (35.2% false-fires-gated baseline; 2 own-confounds disclosed not shipped), CVO HUD-cert 084324Z. CTO dispositioned the 35.2% as an honestly-measured BASELINE (not a threshold-pass) -> no reopen. AUA interleave (base COO thread, non-NFRA) also landed clean. TOOLCHECK DONE -- P3 was the last phase.</status>
    <prd_ref>docs/architecture/NFRA_TOOLCHECK_PRD.md (SS2 selector+HUD findings, SS4 P3, SS8 Q3)</prd_ref>
    <dispatch_state>STAGED. Gated on P2. ROUTE-BEFORE-BUILD: the coverage-gap tools (comp-symbols/comp-types) may be a ROUTING miss not an absent tool -- resolve here before P2 authorizes any new-tool build (Q4).</dispatch_state>
    <gate_note>The selector + HUD are the shared cognition's entry point -- a mis-route or a banner-blind HUD degrades every agent invisibly. Part 0 did the first pass; P3 fixes + measures it.</gate_note>
  </metadata>

  <objective>Assess whether comp-which routes properly + the HUD is well-calibrated; land the selector fixes/optimizations + the HUD behavioral adjustments, each exercised + measured.</objective>

  <requirements>
    <requirement id="1" priority="SELECTOR FIXES">FIX: (a) comp-fedobs UNREACHABLE (routing-regression oracle RED 36/37 -> add rule/keywords -> GREEN); (b) over-disambiguation on clear intents (portal-vocab collision -- the router disambiguates 247 > decides-confidently 152). Verify the routing-oracle GREEN.</requirement>
    <requirement id="2" priority="SELECTOR OPTIMIZE">OPTIMIZE: (a) derive curated keywords from the LEDGER (COMPUNIFY-#1 -- retire the hand-maintained parallel RULES catalog; Q3 aggressiveness CTO-ratified) + strengthen the fuzzy backstop; (b) the BASE-POSTERIOR (the in-flight POTION semantic-relevance) is the HIGHEST-VALUE lever -- held-out recall@surf 60% is the headline gap (40% of novel intents' right tool not even surfaced); (c) HOLD the affinity flip (no-op on the vetted corpus + NEGATIVE at cold-start / 53% of live routes -- fix authoritative role-propagation FIRST).</requirement>
    <requirement id="3" priority="HUD / COMPHUD behavioral">(a) INVERT the throttle (the least-specific catch-all fires EVERY time / precise classes once -- backwards); (b) gate on the command's LEADING verb (suppress compound-operational false-fires: git push && terraform plan, echo && ls); (c) stop nudging cmd | grep pipes the rail itself deems legit; (d) convert the catch-all from "a tool exists" boilerplate to "the tool + its EXACT call" -- fire only when comp-which actually ROUTES (a specific nudge is far less ignorable than a standing banner).</requirement>
  </requirements>

  <acceptance_criteria>
    1. The routing-regression oracle is GREEN (comp-fedobs reachable + no regressions).
    2. The HUD calibration measurably improved on comp-tool-hud.log (fewer false-fires: compound-op, legit pipes; the catch-all now fires a specific route not a banner).
    3. CTO arch-gate + CVO cert (routing-oracle-green + HUD-measured). Further breaks P3 surfaced -> routed back to P2. RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
