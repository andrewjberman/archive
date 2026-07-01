# TASK ORDER — NFRA_COMPLEARN.P2

<issued_to>0.8.0_AE_CloudComp~E</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete</status>
<!-- LANDED 2026-07-01: comp_learns_score.py 15e88557d (pushed CLOUD); 6/6 self-test + 7/7 pytest; single iteration -> 596-candidate advisory worklist; --goodhart-audit 241 rank-inversions + high-usage-low-value retires (NOT a usage proxy); reuses comp_route L3 outcome-weighting (one signal, two consumers). test exec-land -> COO~B (SoD). Pends CVO~B scorer-honesty verify to close COMPLEARN. -->

<priority>HIGH — Andrew-direct close-out drive (2026-07-01). SEQUENCED behind your NFRA_COMPROUTE.L3 (one lane, no thrash): GO on L3 RAVC. Not gate-lift-gated — reads the LIVE COMPUNIFY map + your own live tool_activity.</priority>
<date>2026-07-01</date>

## Context
NFRA_COMPLEARN = the self-learning loop over tool-use (the TRAINS verb). PRD: `docs/architecture/NFRA_COMPLEARN_PRD.md`. You have P0 (tool_activity = 3rd Trino catalog) + P1 (federated views + gap_heat) + P3 (scheduled nightly refresh) LIVE. P2 is the remaining piece = the VALUE-anchored scorer + single iteration. This is the LOAD-BEARING risk of the whole program (the Goodhart/benchmark-honesty gate, CTO-owned) — it must score VALUE, not usage.

## Objective
Build the **value-anchored scorer** + run a single learning iteration. The scorer ranks tool-demand / coverage-gaps / optimize-merge-retire candidates on a VALUE metric — **escapes-prevented / chains-shortened / drift-caught / cost-per-outcome — NEVER raw usage count** (the Goodhart failure the CTO gate forbids). Output = an ADVISORY worklist the CTO ratifies (never auto-mutates). Mutation space INCLUDES the comp-which routing rules + HUD (LD-0226 = the canonical worked example — routing-misses, not missing tools, are a large share of friction).

## Scope — P2
1. **The scorer** over the live `tool_activity` catalog + the COMPUNIFY coverage map (the gap reference — LIVE, S4-AUDIT GREEN): score each candidate (needed-tool / coverage-gap / merge-retire) on the VALUE metric, not usage.
2. **Single iteration:** produce ONE advisory worklist (ranked) from the seed corpus (3mo backfill: ~8,600 rolling-log rows + ~1,469 session-log Compiler-Tools sections) -> CTO ratifies. Every routing-miss surfaced becomes a candidate (ties to COMPROUTE's disambiguation flywheel — coordinate the signal shape with your own L3 work).
3. **Goodhart guard baked in:** the scorer explicitly rejects a usage-count proxy; every ranked item cites its VALUE evidence (which escape/chain/drift it maps to). CVO verifies scorer honesty + gap-map ground-truth.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>confirm the live tool_activity catalog exposes the OUTCOME dimensions (escapes-prevented/chains-shortened/drift-caught/cost) + the COMPUNIFY coverage map is readable for the gap reference</run>
      <expect>tool_activity carries outcome (not just count); COMPUNIFY map (S4-AUDIT GREEN) queryable for the gap census.</expect>
      <if_mismatch>STOP. If only counts exist, extend the catalog to carry outcome BEFORE scoring (a count scorer is the Goodhart failure). Flag COO~B.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>grep the scorer for any raw-usage-count ranking term; `from __future__ import annotations`; ds-commit-gate; non-ASCII grep</run>
      <expect>Zero usage-count-as-value; every ranked item cites VALUE evidence. ds-commit-gate clean; zero non-ASCII.</expect>
      <if_mismatch>STOP. Replace the usage proxy with the value metric — this is the CTO-owned load-bearing gate.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>run the single iteration -> the advisory worklist</run>
      <expect>A ranked worklist where each item carries its VALUE evidence (specific escape/chain/drift/cost), advisory-only (no auto-mutation). Includes routing-miss candidates.</expect>
      <if_mismatch>Fix before RAVC. An item without value evidence = a Goodhart leak.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: owns the Goodhart/benchmark-honesty gate (the load-bearing risk) + ratifies the advisory worklist. RAVC the P2 scorer.
- 3.0.0_SA_CVO~B: verifies scorer honesty (scores value not usage) + gap-map ground-truth. This is the COMPLEARN close-verify.
- NFRA_COMPROUTE (your L3): COMPLEARN TRAINS, COMPROUTE DECIDES — the tool_activity outcome signal you build here is the SAME learned term L3's history_affinity consumes. Keep the outcome-weighting consistent across both (one signal, two consumers).
- NFRA_COMPUNIFY (~C): the coverage map is your gap reference — read-only.
</cross_domain_coordination>

<acceptance_criteria>
1. The value-anchored scorer ranks candidates on escapes-prevented/chains-shortened/drift-caught/cost-per-outcome — VERIFIED to reject a raw usage-count proxy (grep-clean + each item cites value evidence).
2. A single iteration produced ONE ranked advisory worklist (including routing-miss candidates) from the seed corpus, advisory-only (CTO ratifies, no auto-mutation).
3. Consistent outcome-weighting with the COMPROUTE history_affinity term (one signal, two consumers).
4. Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`. RAVC COO~B + CC CTO + CVO~B — this + CVO scorer-honesty verify closes COMPLEARN.
</acceptance_criteria>

## Note
Sequenced behind L3 (same lane) to avoid thrash — I GO this on your L3 RAVC. Not gate-lift-gated. The Goodhart gate is the whole point: score VALUE, never usage.
