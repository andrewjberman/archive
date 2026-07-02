# TASK ORDER -- NFRA_TOOLHEALTH.TH-B (the fused per-tool 3-axis HEALTH QUERY + action taxonomy)

<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>staged</status>
<!-- GO FIRED 2026-07-02T~19:00Z (COO~B): MSTR spawned base 0.8.0_AE_CloudComp for TH-B (P0 cleared, cap=20 6-free per LD-0115). TH-B is the READY first leg -- ship the 2-live-axis skeleton NOW over the LIVE COMPLEARN substrate (USED via tool_activity + RAIL-CONSISTENT via comp-which-rail.log); full 4-verdict (FIX/PROMOTE) joins TH-A's EFFECTIVE feed later (TH-A gated on COMPPROOF-B1). REUSE comp_learns_score.py + tool_activity un-forked. Flip staged->pending on start; RAVC COO~B CC CTO+CVO~B. -->

<priority>HIGH -- the high-value deliverable (b): ONE query -> per-tool health verdict. The 2 live axes are runnable NOW; the 4th verdict completes on TH-A. PRD SS3 + SS6.1.</priority>
<date>2026-07-02</date>

## Context
The single high-value deliverable: ONE query that answers, per comp-tool -- *"is this tool USED, correctly-ROUTED-to, AND actually EFFECTIVE -- or ignored / misrouted / dead?"* -> a verdict + action. This is a FUSION over three LIVE sources, NOT a new telemetry stack. USED + RAIL-CONSISTENT exist today (COMPLEARN-LIVE); EFFECTIVE arrives via TH-A. Build the query skeleton over the 2 live axes NOW (KEEP/RETIRE-partial verdicts), then join TH-A's EFFECTIVE stream to light up the full 4-verdict taxonomy.

## Objective
Deliver ONE query returning, per tool, `{used, rail_consistent, effective, verdict in [KEEP|FIX|PROMOTE|RETIRE]}` over the live tool_activity + comp-which-rail.log + comproute-routing.jsonl + TH-A's EFFECTIVE probe stream, with the action taxonomy encoded.

## Scope
1. **The fusion query (over LIVE sources, un-forked):** USED = tool_activity frequency/recency/by-role (COMPLEARN P0 catalog); RAIL-CONSISTENT = comp-which-rail.log route-vs-primitive-fallback action-mix + comproute-routing.jsonl; EFFECTIVE = TH-A's probe stream. READ COMPLEARN's substrate + comp_learns_score.py -- do NOT rebuild or fork.
2. **Action taxonomy encoded (PRD SS3):** yes/yes/yes->KEEP; yes/yes/no->**FIX** (load-bearing -- only EFFECTIVE flips it); no/--/yes->PROMOTE (-> COMPROUTE); no/--/no|unknown->RETIRE. The FIX row MUST be distinguishable from KEEP purely by the EFFECTIVE axis (prove it flips on a real tool once TH-A lands).
3. **Value-anchored honesty gate (inherited COMPLEARN SS5, non-negotiable):** a tool scores KEEP/PROMOTE only if it improves a VALUE metric (rail-escapes prevented / diagnose-chains shortened / real drift-or-bug caught / UNVERIFIABLE-rate reduced / cost-per-archetype-outcome) -- NEVER on invocation-count. Scoring health on usage Goodharts the loop.
4. **Two-phase delivery:** Phase-A = query over the 2 live axes (KEEP + RETIRE-partial verdicts, FIX/PROMOTE = "pending EFFECTIVE"); Phase-B = join TH-A's EFFECTIVE stream -> full 4-verdict. Ship Phase-A first (runnable now); Phase-B on TH-A GO.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-which "where is the tool_activity catalog + comp-which-rail routing log queried"; read comp_learns_score.py (the value-anchored scorer, reuse-not-fork) + comp-learns-status; enumerate the exact live source paths (tool_activity Trino catalog, org/mcp/comp-which-rail.log, org/mcp/comproute-routing.jsonl)</run>
    <expect>All 3 live sources located + queryable; comp_learns_score.py understood as REUSE (the value-anchored logic is inherited, not re-implemented). No fork of COMPLEARN tables planned.</expect>
    <if_mismatch>STOP. If a source is missing/stale, ground it on the LIVE stream (Rule 22) before building the query; do not assume a path.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>run the fusion query over the 2 live axes: per-tool {used, rail_consistent} + verdict where computable (KEEP/RETIRE); assert the value-anchored gate (no verdict rests on raw invocation-count); ds-commit-gate + non-ASCII + `from __future__ import annotations`</run>
    <expect>Query returns per-tool rows over the live substrate; KEEP/RETIRE verdicts computed; FIX/PROMOTE correctly report "pending EFFECTIVE (TH-A)"; zero usage-Goodhart (every KEEP cites a VALUE metric).</expect>
    <if_mismatch>STOP. A verdict that scores healthy on usage-count alone violates the inherited SS5 gate -- fix before commit.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>ONCE TH-A lands: join the EFFECTIVE probe stream -> full 4-verdict; demonstrate the FIX row on a real used-but-ineffective tool; hand the query to TH-C (close-loop) + CVO~B (TH-V honesty)</run>
    <expect>ONE query returns {used, rail_consistent, effective, verdict in KEEP|FIX|PROMOTE|RETIRE} over the fully-live fused sources; >=1 real tool surfaces as FIX.</expect>
    <if_mismatch>If FIX never distinguishes from KEEP, the EFFECTIVE join is wrong -- the FIX row is the whole point. Re-check the TH-A join key.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- COMPLEARN owner: comp_learns_score.py + tool_activity catalog are COMPLEARN-owned + LIVE. TH-B READS them un-forked; the value-anchored honesty gate is inherited un-modified. No writes to COMPLEARN tables.
- 0.8.0_AE_CloudComp (TH-A, same fleet): TH-A's EFFECTIVE probe stream is the join input for the full 4-verdict. Agree the join key (tool/class) + row schema with TH-A.
- NFRA_COMPROUTE: consumes PROMOTE verdicts (effective-but-ignored = routing/HUD miss). Coordinate the PROMOTE-verdict handoff shape.
- 3.0.0_SA_CVO~B (TH-V): independently verifies the scorer/health honesty (every KEEP/PROMOTE improves a VALUE metric, zero usage-Goodhart).
- 1.0.0_SA_CTO: arch-gates the value-anchored honesty gate (SS5.1). RAVC him.
</cross_domain_coordination>

<acceptance_criteria>
1. ONE query returns, per comp-tool, `{used, rail_consistent, effective, verdict in [KEEP|FIX|PROMOTE|RETIRE]}` over the live tool_activity + rail-log + comproute-routing.jsonl + TH-A EFFECTIVE feed (PRD SS6.1).
2. The action taxonomy is encoded exactly (PRD SS3); the FIX row is distinguishable from KEEP purely by the EFFECTIVE axis, demonstrated on >=1 real tool (post TH-A).
3. Value-anchored honesty: every KEEP/PROMOTE cites a VALUE metric; zero verdict rests on invocation-count (grep-proof against the query logic).
4. COMPLEARN substrate + scorer are READ-only-reused (no fork/mutation). Session-log Compiler Tools reproduces every `<run>`. RAVC COO~B + CC CTO + CVO~B.
</acceptance_criteria>

## Note
Ship the 2-live-axis skeleton FIRST (runnable now on the COMPLEARN substrate) so the health view exists before TH-A completes; the EFFECTIVE join is the second phase. The FIX row (used-but-ineffective) is the load-bearing catch the whole project exists to surface.
