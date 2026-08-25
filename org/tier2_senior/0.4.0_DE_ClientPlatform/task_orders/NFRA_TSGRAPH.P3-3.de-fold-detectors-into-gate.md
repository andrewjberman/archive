<to_id>NFRA_TSGRAPH.P3-3</to_id>
<project>NFRA_TSGRAPH</project>
<title>P3-3 -- fold the highest-signal frontend detectors into the commit-gate / critical-surface scan</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>commit-gate / critical-surface owner (CTO for the gate policy; DT for the hook wiring) -- commit-through the gate owner</consult>
<issued_by>2.0.0_SA_COO (CTO PRD section-9 handoff 151724Z; 2b61ac87e)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_TSGRAPH is complete; this TO was last touched 2026-06-18, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>MEDIUM -- GATED on P3-2 (folds the validated detectors). Closes the loop: detectors become preventive gates.</priority>

<gate>P3-2 <status>complete</status> (validated frontend detectors exist). COO GOes after P3-2 RAVC2.</gate>

<scope>
Fold the highest-signal P3-2 detectors into the commit-gate / critical-surface scan so they catch their bug-class at commit/CI time (preventive, not just diagnostic). Select top-K by signal (frequency x severity from the P3-1 catalog). Wire through the gate owner (commit-through-owner -- the gate is CTO/shared policy, not a DE-unilateral edit). comp-surface-check integration.
</scope>

<compiler_tools_mandate>
  <phase id="3" when="after commit"><step><run>comp-surface-check (gate/critical-surface integration)</run><expect>The folded detectors run in the commit-gate / critical-surface scan; a known exemplar would be CAUGHT at gate-time.</expect><if_mismatch>STOP. A detector that does not fire in the gate is not integrated -- the fold is incomplete.</if_mismatch></step></phase>
</compiler_tools_mandate>

<cross_domain_coordination>Touches the commit-gate / critical-surface infra (shared, CTO/gate-owner policy) -- commit-through the gate owner, not a DE-unilateral change. Same critical-surface registry as the D8 alarm work (NFRA_GRAPHS).</cross_domain_coordination>

<acceptance_criteria>1. Top-K detectors folded into the commit-gate / critical-surface scan, committed through the gate owner. 2. comp-surface-check confirms they fire (a known exemplar caught at gate-time). 3. Session-log Compiler Tools reproduces each <run>. RAVC2 to COO (CC CTO + gate owner).</acceptance_criteria>

<dependencies><dependency project="NFRA_TSGRAPH" task="P3-2" status="staged"/></dependencies>
<references><ref type="prd">docs/architecture/NFRA_TSGRAPH_PRD.md section 9</ref></references>
<lane_note>DE-authored, commit-through the gate owner (CTO/shared policy). Full mandate-triad finalizes at GO (depends on P3-2). COO GOes post-P3-2.</lane_note>
