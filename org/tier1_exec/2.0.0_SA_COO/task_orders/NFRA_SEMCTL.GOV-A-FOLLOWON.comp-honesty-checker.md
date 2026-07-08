# Task Order: NFRA_SEMCTL GOV-A follow-on -- the comp-honesty runnable checker (make the honesty doctrine a GATE, not prose)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-semctl-gov-a-comp-honesty</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D (build) + 3.0.0_SA_CVO (exercise-cert)</issued_to>
    <date>2026-07-08</date>
    <status>dispatched</status>
    <prd_ref>docs/architecture/NFRA_SEMCTL_HONESTY_INVARIANTS.md (GOV-A, b9f58b442; CVO co-ratify 7aad2f834) -- SS2/SS4.2 check-specs</prd_ref>
    <dispatch_state>DISPATCHED 2026-07-08 by COO~B (NFRA full-program drive). GOV-A closed; CTO flagged the SS2 check-specs implementation-complete -> this makes the doctrine runnable. ~D freed from COMPILERKIT (closed a805f126c).</dispatch_state>
    <gate_note>Non-critical-path (advisory tooling), but high-leverage: it converts the shared honesty doctrine into a runnable check every future NFRA honesty claim can gate on.</gate_note>
  </metadata>

  <objective>Build `comp-honesty` -- a runnable checker over the 3 GOV-A invariants (I1 honest-missing/LOUD-not-silent, I2 measure-per-case-not-aggregate, I3 control-must-fire-when-exercised), implementing the SS2/SS4.2 check-specs from NFRA_SEMCTL_HONESTY_INVARIANTS.md. Make the doctrine a GATE, not prose: given a claim/artifact + its evidence, the checker returns per-invariant PASS/FAIL/N-A with the grounding, so a verifier (or a commit/deploy gate) can mechanically apply the honesty bar.</objective>

  <requirements>
    <requirement id="1">Implement the SS2 check-specs (they are implementation-complete per CTO) as a runnable tool (a comp-tool, on the rail; register in the graph-call-manifest).</requirement>
    <requirement id="2">I1 check: a claim that asserts completeness/GREEN must show the missing-set was surfaced LOUD (not a silent empty pass) -- the check FAILS an unexercised/silent gate.</requirement>
    <requirement id="3">I2 check: a measure must be per-case, not an aggregate that hides a per-case violation (the A_00-class check).</requirement>
    <requirement id="4">I3 check: a control that gates an action must be shown to FIRE on a known-bad exercise (exists != fires) -- the strip-list/dead-guard class.</requirement>
    <requirement id="5">Self-test on the GOV-A worked corpus (the cot gold-review examples D_02/A_00/build_canonical_prices:584) -- the checker must FLAG each real violation and PASS the honest cases. LOUD, never green-theater (dogfood I1 on itself).</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_SEMCTL.GOV-A (docs/architecture/NFRA_SEMCTL_HONESTY_INVARIANTS.md): the doctrine + SS2 check-specs this implements.
    - 3.0.0_SA_CVO: co-owns the exercise-cert discipline (I3); takes the checker's exercise-cert (does it FIRE on a real violation, not just claim to).
    - The COMPRAIL/comp-tools rail: register comp-honesty as an on-rail tool.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `comp-honesty` runs over the GOV-A worked corpus: FLAGS every real violation (D_02 silent-crash / A_00 aggregate-hide / dead-guard) + PASSES the honest cases -- exercised, not asserted (Rule 22 / GOV-A I3 applied to itself).
    2. Each of I1/I2/I3 has a runnable check with a known-bad + known-good fixture that the check distinguishes.
    3. Registered on the comp-tools rail. CVO exercise-cert PASS. RAVC COO~B + CC CTO.
  </acceptance_criteria>
</task_order>
```
