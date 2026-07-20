<task_order>
<id>NFRA_ONTOCLARITY.WS-C.process-deterministic-tie-breakers</id>
<project>NFRA_ONTOCLARITY</project>
<issued_to>0.8.0_AE_CloudComp~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<completed>2026-07-20T06:32Z -- CVO-DETERMINISM-PASS (364 role-triples x every permutation -> one answer; totality GUARANTEES min-by-priority.index order-independence). Landed: role_priority @317b3d0af (CTO grantor), comp_ontolint role-resolve @5b98d0ed6 (AE). ONTOCLARITY 3/4.</completed>
<priority>P2 -- definitional, startable after WS-A (parallel-OK with WS-B). Context-owner ~C.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_ONTOCLARITY_PRD.md @b9b132933 (WS-C = S4 third bullet)</ref>
  <ref type="charter">org/tier0/ledger/LD-0320.md</ref>
</references>

<objective>
Resolve the PROCESSES fog: where the ontology leaves a classification/assignment UNDERDETERMINED, supply a DETERMINISTIC
tie-breaker so two agents applying the same rule to the same input reach the SAME verdict (the reproducibility property --
same failure class as MSTR's WS-1 vintage catch, one layer up: a non-deterministic PROCESS is a non-reproducible control).
Cover the enumerated ambiguous processes (PRD S4): the polymorphic-Role assignment, the incorporation-mode decision-rule,
and the pinned C2->C3 ownership hand-off -- each gets a stated, ordered tie-breaker rule (not "use judgment").
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>enumerate (grounded) each ambiguous ontology PROCESS where two reasoners could diverge -- the polymorphic-Role case, incorporation-mode, C2->C3 ownership -- + how each is currently resolved (if at all)</run>
      <expect>The list of underdetermined processes = WS-C's denominator. For each: the current (absent/ambiguous) resolution rule.</expect>
      <if_mismatch>N/A -- grounding.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>for each tie-breaker: construct the ambiguous input + confirm the rule yields ONE deterministic verdict (ideally a check/test, else a worked example in the doc)</run>
      <expect>Each previously-underdetermined process now resolves to a single verdict under its stated rule (reproducible). Prefer an exercised check over a prose rule where the process is machine-checkable.</expect>
      <if_mismatch>A tie-breaker that still admits two verdicts is not deterministic -- tighten the ordering until it is single-valued.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. Each enumerated underdetermined process (polymorphic-Role / incorporation-mode / C2->C3 ownership + any other grounded in phase-1) has a STATED, ORDERED, deterministic tie-breaker -- same input, same verdict, provable by a worked ambiguous case.
2. Machine-checkable processes get a check (EXERCISED), not prose, where feasible.
3. LD-0320/0318 CVO SEMANTIC-VERIFIED GATE: CVO confirms the process ambiguity is GONE (a reasoner can no longer legitimately reach two verdicts), not merely reworded. Ping CVO on land.
4. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- Independent of the SYSPARITY scope contract; start after WS-A (parallel-OK with WS-B). Feeds WS-D (logged in system/sdk).
- Any arch-decision (which way a tie-breaker resolves, when it encodes a real ontology choice) -> ping CTO via COO.
</cross_domain_coordination>

<notes>~C context-owner. The reproducibility property is the point (same class as MSTR's WS-1 vintage catch -- a non-deterministic process is a non-reproducible control). SEMANTIC-axis acceptance.</notes>
</task_order>
