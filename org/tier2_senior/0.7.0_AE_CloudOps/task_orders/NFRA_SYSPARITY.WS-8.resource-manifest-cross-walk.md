<task_order>
<id>NFRA_SYSPARITY.WS-8.resource-manifest-cross-walk</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.7.0_AE_CloudOps~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P3 -- optional/high-value (PRD S4: sequence last, de-scope if effort outweighs value). Context-reallocation of 0.7.0~B (CloudOps/infra/TF lane, finished its git_bash migrations) per Andrew-direct idle-reallocation-by-context.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-8 = S3 eighth bullet)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Build a MACHINE cross-walk so INFRA parity is auditable against LIVE state, not prose -- an extension of the 06_current_state
auto-gen model to the static infra sections. A command that maps: system doc infra claims <-> the real globgrph/*.tf (+ the
broader in-scope infra) <-> the SDK infra module, and FLAGS a doc<->TF<->SDK divergence. This closes the "infra parity is
asserted in prose, not measured" gap for the infra domain of the WS-1 parity metric.
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-aws / comp-iam (the live TF-modeled infra views) + read infra/system's infra sections + the SDK infra module + WS-1's scope_contract.json (the declared infra scope)</run>
      <expect>The three sides to cross-walk (doc / live-TF / SDK) + the DECLARED infra scope from WS-1 (the cross-walk's denominator = declared scope, NOT the ~90% out-of-scope pipeline estate -- VL#6, same as WS-1).</expect>
      <if_mismatch>If WS-1's scope_contract isn't landed yet, coordinate with ~A -- the cross-walk denominator IS WS-1's declared infra scope; do not invent a parallel one.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>run the cross-walk command you build</run>
      <expect>Emits the doc<->TF<->SDK map + FLAGS a real divergence (seed a known doc-vs-TF drift, confirm it flags = EXERCISED, not asserted). Denominator = declared infra scope, printed; out-of-scope infra never counted as a divergence.</expect>
      <if_mismatch>STOP -- an unexercised cross-walk (never shown to flag a real divergence) is not a control. Exercise it.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. A command produces the doc<->TF<->SDK cross-walk over the DECLARED infra scope (WS-1 denominator; out-of-scope estate excluded, printed).
2. It FLAGS a doc<->TF<->SDK divergence, proven by EXERCISE (seed a known divergence, watch it flag) -- not a prose assertion.
3. Alert-suspension-clean (on-demand / HEAD-advance, no new scheduled CI cadence) + reuses live comp-aws/comp-iam TF views (no parallel infra scan).
4. LD-0318 CVO-VERIFIED GATE: the cross-walk accuracy is CVO-verified per PRD S7 (cron 02d90dce). Ping CVO on land.
5. Session log with Compiler Tools section reproducing each <run> vs <expect>. If effort outweighs value (PRD de-scope clause), surface to COO with the measured effort rather than silently dropping.
</acceptance_criteria>

<cross_domain_coordination>
- Denominator = WS-1's declared infra scope (~A) -- coordinate; the cross-walk is meaningless without the scope boundary (it would flag the out-of-scope pipeline estate as divergence = VL#6).
- Reuse comp-aws/comp-iam live TF views (do NOT build a parallel infra scanner). The 06 auto-gen model (WS-2/~D's comp-system) is the pattern to extend to the static infra sections.
- OPTIONAL: if the effort is disproportionate, de-scope with a measured-effort note to COO (do not silent-drop).
</cross_domain_coordination>

<notes>
Context-reallocation of 0.7.0~B per Andrew-direct (2026-07-19): its lane = CloudOps / infra / TF + comp-tooling; it just closed
the git_bash-class python->bash migrations (@984d0be0c, honest Rule-22 framing -- retired the conditional WSL-stub risk, not
live victims). A machine cross-walk over globgrph/*.tf <-> system doc <-> SDK is its exact-context next -- infra parity made
auditable, reusing the comp-aws/comp-iam views it works in daily. server.py Stage-B stays on its restart event-gate (separate).
</notes>
</task_order>
