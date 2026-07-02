# TASK ORDER -- NFRA_AGENTBUS.S1 (the 5-control security-model DESIGN -- THE load-bearing design)

<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>staged</status>

<priority>HIGH -- S1 is the load-bearing design; it GATES S2-S4. IN SCOPE under Andrew-direct-auth (design phase). PRD docs/architecture/NFRA_AGENTBUS_PRD.md SS3 + SS5 + SS8-S1.</priority>
<date>2026-07-02</date>

<governance_fence>
DESIGN PHASE -- IN SCOPE under Andrew-direct-auth (MSTR DECOMP-GO 2026-07-02, LD-0239). This TO produces the security-model DESIGN SPEC only. It does NOT wire two real fleets and does NOT activate live cross-principal comms (that is FENCED, held for the un-authored standing-access-class Directive). Design against the SCTY/COMPTEAM interfaces; no live cross-principal message crosses in this TO.
</governance_fence>

## Context
`opal-agent-comms` today is single-principal / single-workspace. AGENTBUS is the multi-tenant, inter-principal extension. The load-bearing framing (binding): **THE SECURITY MODEL IS THE DESIGN.** Cross-principal comms is a real attack surface; get entitlement + attribution + strip + partition right BEFORE any two fleets touch. A working transport with a weak security model is a FAILURE, not an MVP. S1 designs the 5 controls; it GATES S2 (transport), S3 (adapter), S4 (verify).

## Objective
Author the security-model DESIGN SPEC: the 5 fail-closed controls specified against the SCTY_MCPGUARD tiers + SCTY_PREMCP token + the COMPTEAM signature-root; the ACTION-vs-DATA classifier; the strip-list binding. CTO arch-gate is the acceptance.

## Scope (the 5 controls, each specified as a fail-closed design -- PRD SS3)
1. **IAM + KMS per-employee partition:** shared queue-pair per collaboration (A->B, B->A); each fleet `SendMessage` to the pair + `ReceiveMessage` ONLY from its own inbound partition (SQS queue-policy + `sqs:` action scoping + message-group scoping + per-collaboration KMS key). Design the policy shape; fail-closed (an identity outside the grant reaches nothing).
2. **SCTY-guardrail gated ACTION-vs-DATA:** the classifier (DATA-share = information, read-only-by-construction; ACTION-request = do-something, crosses a trust boundary). Specify the SCTY_MCPGUARD-tier + SCTY_PREMCP-token authz gate an ACTION-request must pass before the receiving fleet may act. Coordinate the interface with the SCTY lane (base COO).
3. **Verified signed attribution:** every cross-employee message carries a SIGNED `from_employee+from_agent` resolved off the COMPTEAM signature-verified root-of-trust -- NOT a self-claimed serial. Unverifiable signature -> reject (fail-closed). Specify the signing + verification design.
4. **Egress content-strip / DLP:** reuse the COMPTEAM strip-list (secrets/creds/secret-ARNs/AWS-account-ids/internal-hostnames+bucket-names/firm-PII). Specify the outbound-adapter strip gate (hit -> redact-or-block); fail-closed by construction.
5. **Default read-only / propose:** incoming can REQUEST, never directly MUTATE; the receiving fleet adjudicates anything actionable (human/tier gate per control 2). Specify the propose-only default.
**Composition (specify explicitly):** controls 1+3 gate WHO; control 4 gates WHAT LEAVES; controls 2+5 gate WHAT THE RECEIVER MAY DO. All five apply at the broker-adapter choke point; none optional.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-which "where are the SCTY_MCPGUARD tier authz + SCTY_PREMCP token + the COMPTEAM signature-root + strip-list defined"; read SCTY_MCPGUARD_PRD.md + SCTY_PREMCP_PRD.md + NFRA_COMPTEAM_PRD.md; coordinate the SCTY interface with base COO (SCTY coo_lane)</run>
    <expect>The SCTY authz interface + PREMCP token + COMPTEAM signature-root + strip-list interfaces located; the design binds to their real interfaces (not invented ones).</expect>
    <if_mismatch>If an interface is not yet available (SCTY_MCPGUARD is decomposing), design against the SPECIFIED interface + flag the sequencing dependency to COO~B -- do NOT invent an interface.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>comp-routes / comp-iam review the opal-agent-comms broker + the proposed adapter choke point; assert all 5 controls compose at ONE choke point (the adapter); ds-commit-gate + non-ASCII on any spec artifact</run>
    <expect>The design spec shows all 5 controls applied at the single adapter choke point; each is fail-closed; the intra-fleet path is documented UNCHANGED (extend, not replace).</expect>
    <if_mismatch>STOP. If any control is optional or applied outside the single choke point, the composition is unsafe -- redesign before CTO arch-gate.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>hand the DESIGN SPEC to CTO for the arch-gate (each control is a CTO arch-gate per SS3); RAVC COO~B + CC CTO + the SCTY lane (base COO)</run>
    <expect>CTO arch-gates the 5-control model; on PASS, S2-S4 unlock (simulated-build). The spec is the binding interface S2/S3 build to.</expect>
    <if_mismatch>A control the CTO redlines is re-designed before S2-S4 dispatch -- S1 gates the wave.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- 1.0.0_SA_CTO: ARCH-GATE (each of the 5 controls is a CTO arch-gate). Build the spec to his arch; the CTO arch-gate is the S1 acceptance + the S2-S4 unlock.
- SCTY lane (base COO, SCTY_MCPGUARD/PREMCP coo_lane=2.0.0_SA_COO): control-2 authz interface. Coordinate the entitlement/tier + PREMCP token binding; CC base COO.
- NFRA_COMPTEAM: control-3 signature-root + control-4 strip-list. Design against COMPTEAM's onboarding/identity substrate + strip-kit (reuse, don't re-derive).
- opal-agent-comms (org/mcp/): the broker EXTENDED by the adapter. Intra-fleet path UNCHANGED.
- NFRA_AGENTBUS-S2/S3: build to this spec. It is the binding interface.
</cross_domain_coordination>

<acceptance_criteria>
1. A security-model DESIGN SPEC specifies all 5 controls (SS3) as fail-closed designs bound to the REAL SCTY_MCPGUARD-tier + SCTY_PREMCP-token + COMPTEAM signature-root + strip-list interfaces (not invented ones).
2. The composition is explicit (WHO / WHAT-LEAVES / WHAT-RECEIVER-MAY-DO) and all 5 apply at the single broker-adapter choke point; the intra-fleet opal-agent-comms path is documented UNCHANGED (extend, not replace).
3. CTO arch-gates the model (each control). The spec is the binding interface for S2-S4.
4. NO live cross-principal message is exchanged in this TO (governance-fence honored). Session-log Compiler Tools reproduces every `<run>`. RAVC COO~B + CC CTO + SCTY lane.
</acceptance_criteria>

## Note
The security model is the product. Design it fail-closed at ONE choke point (the adapter) before any transport carries a real message. This TO is design-only (in scope); it GATES the simulated build (S2-S4). The live two-fleet activation is FENCED (a separate Directive), NOT part of this or any currently-authored TO.
