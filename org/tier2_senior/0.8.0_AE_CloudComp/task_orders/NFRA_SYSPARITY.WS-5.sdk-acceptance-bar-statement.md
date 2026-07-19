<task_order>
<id>NFRA_SYSPARITY.WS-5.sdk-acceptance-bar-statement</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~Z</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P2 -- a STATEMENT, not a build (PRD S4: CTO pre-ruled, can land early, WS-1-independent). Context-reallocation of ~Z (docs/comp-tools lane, WS-7 just landed) per Andrew-direct idle-reallocation-by-context.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-5 = S3 fifth bullet; CTO pre-ruled)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Make the SDK's cloud-acceptance bar EXPLICIT, not silent. The SDK terraform is faithful-by-construction but UNEXERCISED
(Rule 22a: DESIRED, never `terraform apply`'d). CTO has PRE-RULED (make it explicit, do not default): given the consolidation
phase + new-territory discipline, do NOT apply a new tenant to AWS now -- DECLARE local loop-closure as the accepted
acceptance bar for v1, with the Rule-22a caveat LABELED in the SDK header. Deliverable = a durable STATEMENT in the SDK:
"faithful-by-construction, cloud-UNEXERCISED (DESIRED not APPLIED) -- a one-tenant apply-smoke is the post-consolidation proof;
local `genesis verify --local` loop-closure is the accepted v1 acceptance bar." This closes the un-declared Rule-22a caveat
(the brief flagged the SDK's DESIRED-not-EXERCISED state as unlabeled).
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>read the SDK header / manifest (infra/system/sdk/) + confirm the current tier is local (CVO fire-2 confirmed: verify-report.json:2 tier=local)</run>
      <expect>The SDK's current acceptance state (local, unexercised-at-cloud) -- the LABEL must MATCH this reality (CVO-confirmed local), not overclaim.</expect>
      <if_mismatch>If the SDK is already cloud-exercised (contradicts CVO fire-2), STOP + surface to COO -- the WS-5 premise moved.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>grep the SDK header for the acceptance-bar statement + the Rule-22a caveat</run>
      <expect>The SDK STATES the v1 acceptance bar (local loop-closure) + the DESIRED-not-EXERCISED / cloud-unexercised caveat, durably (a reader sees it, it is not silent).</expect>
      <if_mismatch>Add the missing statement -- a silent DESIRED-not-EXERCISED SDK is exactly the Rule-22a gap WS-5 closes.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. The SDK header/manifest STATES (durably, not silent): the v1 acceptance bar = local `genesis verify --local` loop-closure, AND the Rule-22a caveat (faithful-by-construction / cloud-UNEXERCISED / DESIRED-not-APPLIED / a one-tenant apply-smoke is the post-consolidation proof).
2. The label MATCHES reality (CVO fire-2 confirmed tier=local) -- no overclaim of cloud-exercise.
3. LD-0318 CVO-VERIFIED GATE: CVO verifies the stated bar matches reality (per PRD S7, its fire-2 already confirmed tier=local -- so this is a light confirm the LABEL matches). Ping CVO on land.
4. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- WS-5 is CTO-PRE-RULED (local-only + 22a caveat) + WS-1-independent -> proceed now; it is a STATEMENT, not a build.
- The SDK-header touch may overlap ~C's WS-4 Part-B (SDK vocabulary-bound schema) -- coordinate with ~C on the SDK-manifest edit surface (both touch infra/system/sdk/); COO brokers if you two collide on a file. (schema.json is NOT a drift-gate surface per ~A, so no trailer either way.)
- Revisit the cloud-exercise post-consolidation (out of scope for v1).
</cross_domain_coordination>

<notes>
Context-reallocation of ~Z per Andrew-direct (2026-07-19): ~Z just landed WS-7 (system-doc/rail-description work); WS-5 is another
durable-statement-in-a-doc task (the SDK acceptance-bar label) -- same docs/statement muscle, light, WS-1-independent, CTO-pre-ruled.
Keeps ~Z on SYSPARITY. NB coordinate the SDK-manifest surface with ~C's WS-4 Part-B (both touch infra/system/sdk/).
</notes>
</task_order>
