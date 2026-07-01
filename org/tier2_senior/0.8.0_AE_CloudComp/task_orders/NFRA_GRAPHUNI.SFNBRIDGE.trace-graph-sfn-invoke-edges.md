# TASK ORDER — trace_graph SFN-invoke-edge bridge (comp-blast/comp-iam SFN blast-radius completeness)

<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>staged</status>
<!-- STAGED (not dispatched): a GENUINE net-new COMP* improvement per Andrew's 2026-07-01 carve-out (comp-blast SFN blast-radius completeness, NOT a COMPAWS re-cert). Held pending Andrew's go, since he just gave a deprioritize signal on the comp-aws area. Authored + ready; ~B proposed it + is free; oracle (~A 26-INVOKE census) ready. COO~B surfaces it for the go/no-go. -->
<priority>MEDIUM — CTO-identified real gap (050531Z), not urgent (26 invokes; priority-proportional). Bounded + oracle-ready + your comp-lambdamap/trace_graph domain. NOT a COMPAWS close-blocker (SFN-FIX in comp-aws is by-design-done + certified); this is a SEPARATE comp-blast/trace_graph enhancement.</priority>
<date>2026-07-01</date>

## Context
~B ground-truthed (Rule-22) that comp-aws is the SFN-authoritative tool (StepFunctions class F1=1.0 certified), but comp-blast/comp-iam's trace_graph does NOT model StepFunctions AT ALL -> comp-blast on a Lambda MISSES its SFN-orchestrated dependents (comp-blast YangDataPipeline = NOT-FOUND). CTO ruling (050531Z): comp-aws boundary STANDS for COMPAWS; the SFN->Lambda INVOKE-edge bridge into trace_graph is a REAL, SEPARATE blast-radius gap worth filing (26 SFN invokes = meaningful orchestration). Bounded: invoke/dependency edges ONLY, NOT a full SFN model in trace_graph (deep SFN stays comp-aws).

## Objective
Bridge SFN->Lambda INVOKE edges into trace_graph so comp-blast/comp-iam surface SFN-orchestrated dependents -- blast-radius completeness. A new bounded `sfn_invokes` edge-type (STATE_MACHINE -> LAMBDA), same pattern as trace_graph's existing Lambda->Lambda + IAM edges. Reuse the CERTIFIED walker (do NOT rewrite): a trace_graph extract pass that calls the already-fixed `comp_aws_cli._sfn_task_invokes` (recursive) -> emits the edges.

## Scope
1. New trace_graph extract pass: call `comp_aws_cli._sfn_task_invokes` (the certified recursive walker) -> emit `STATE_MACHINE -> LAMBDA` `sfn_invokes` edges into the trace graph. Bounded to invoke/dependency edges (NOT a full SFN state model).
2. comp-blast/comp-iam surface the new edges (a Lambda's SFN-orchestrated dependents now appear in its blast radius).
3. Oracle: ~A's live census (26 recursive INVOKES, def_hash 5082ce9dba1318fd) is the 0-diff target; ~A re-diffs post-bridge for the CVO cert.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-surface-check (comp-blast/comp-iam are CRITICAL SURFACES) + comp-blast on an SFN-orchestrated Lambda (before-state: SFN dependents MISSING)</run>
      <expect>comp-surface-check baseline captured; before-state confirms the gap (SFN dependents absent from the Lambda's blast radius). The certified _sfn_task_invokes walker is the reuse point.</expect>
      <if_mismatch>STOP. If comp-surface-check flags a break risk, coordinate with CVO~B/COO~B before touching the surface.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-surface-check (post-change) + reuse check (calls _sfn_task_invokes, no walker rewrite) + ds-commit-gate + non-ASCII</run>
      <expect>comp-surface-check CLEAN (no critical-surface regression on comp-blast/comp-iam); reuses the certified walker (no re-implementation); bounded to sfn_invokes edges; ds-gate clean.</expect>
      <if_mismatch>STOP. A comp-blast/comp-iam regression on a SEV1 surface is a blocker -- fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-blast on the SFN-orchestrated Lambda (after) + ~A re-diffs vs the 26-INVOKE oracle</run>
      <expect>The Lambda's SFN dependents now appear (26 invokes bridged, def_hash 5082ce9dba1318fd 0-diff); no regression on non-SFN blast radii.</expect>
      <if_mismatch>Fix before RAVC. A wrong/missing edge = incomplete blast radius.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- CRITICAL SURFACES: comp-blast + comp-iam (SEV1). comp-surface-check before + after; CVO~B cert required. This is why it's a COO-GO'd + CVO-certed change, not a self-land.
- 0.8.0_AE_CloudComp~A: owns the oracle (26-INVOKE census, def_hash 5082ce9dba1318fd) -> re-diffs post-bridge for CVO cert.
- 1.0.0_SA_CTO: identified + scoped the gap (bounded invoke-edges only); RAVC the surface change.
- 3.0.0_SA_CVO~B: certifies the bridged edges vs ~A's oracle + confirms no critical-surface regression.
- comp-aws (SFN-authoritative): unchanged -- trace_graph gets the invoke-edge PROJECTION, not the deep SFN model.
</cross_domain_coordination>

<acceptance_criteria>
1. `sfn_invokes` (STATE_MACHINE -> LAMBDA) edges bridged into trace_graph via a pass reusing the certified `_sfn_task_invokes` walker (no rewrite); comp-blast/comp-iam surface a Lambda's SFN-orchestrated dependents.
2. comp-surface-check CLEAN before + after (zero critical-surface regression on comp-blast/comp-iam).
3. ~A's 26-INVOKE oracle 0-diff post-bridge; CVO~B certifies. Session log reproduces every run. RAVC COO~B + CC CTO + ~A + CVO~B.
</acceptance_criteria>

## Note
Bounded blast-radius-completeness enhancement (invoke edges only). Reuse the certified walker -- do NOT rewrite. SEV1 surfaces -> comp-surface-check + CVO cert are the guardrails. Filed separate from COMPAWS (which closes on the Phase-0 hand-audit alone). Named under GRAPHUNI (the comp-blast/trace_graph substrate lane) for tracking; it's a comp-tool completeness fix, not a COMPAWS leg.
