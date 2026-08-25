# TASK ORDER -- NFRA_AGENTBUS.S3 (the broker adapter = the 5-control choke point + tool_activity meter -- SIMULATED)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_AGENTBUS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active -- CONTROL LEDGER (COO~B 2026-07-09): all 5 controls ARCH-CLEARED. C1 S2-partition live-deny-tested (e29940a74). C2 SCTY authz certed (MCPGUARD 8b24cd2bb + PREMCP). C3 attribution-signing CTO-ratified to bind SCTY RS256 (2026-07-07). C4 egress-strip BUILT + arch-gate-PASSED (CTO 072021Z; 0.7.0 c5c2477ed, control4_egress_strip.py, 14/14 fail-closed, imports the shared _classify_line strip-list gate). C5 propose-only per S1 spec. FULL-ADAPTER CLOSE still awaits: the C2/C3/C4 LIVE IMPLS landing (MCPGUARD decomposing; PREMCP apply-complete/HELD; COMPTEAM active) + swapping the simulated strip-list stub for the live COMPTEAM one + the adapter-integration/app-meter/single-tenant-simulation proof. CTO live-integration CONDITION: the adapter must NOT swallow-and-proceed around egress_or_block (fail-closed must never flip fail-open -- the fail-silent-except pattern). AB-ACTIVATE stays FENCED (Andrew standing-access Directive).</status>
<reconcile_note>RE-LANED DE->0.7.0_AE_CloudOps 2026-07-07 by COO~B (backend-infra, not portal; 0.7.0_AE built S2 live). THIS is the authoritative S3 (full 5-control spec + compiler-mandate + acceptance criteria); it SUPERSEDES the thin stub org/tier1_exec/2.0.0_SA_COO/task_orders/NFRA_AGENTBUS.S3.broker-adapter-simulated.md. File retained in the DE folder for history; owner is 0.7.0_AE_CloudOps. GO held until S3's real deps verified: COMPTEAM strip-list/sig-root (C3/C4) + SCTY authz (C2, PREMCP P1 now certed) landed.</reconcile_note>
<dep_check_verdict date="2026-07-07" by="COO~B (grounded dep-check)">NOT-GO yet -- 3/4 deps READY, 1 hard blocker + 1 caveat:
  - control-1 (S2-bus partition): READY -- e29940a74, tag nfra-agentbus-v1.0.0, live deny-test PASS.
  - control-2 (SCTY authz): READY -- MCPGUARD tier-model CVO-certed 4/4 (8b24cd2bb, live); PREMCP C3-WAF 5/5 (6d73bb889).
  - control-4 (COMPTEAM strip-list): READY-to-reuse (d48e363e8, .tools/comp-kit-striplist-gate) BUT its fail-closed proof (planted-secret/clean-kit fixture) + CTO arch-gate are OPEN -> control-4 cert needs that proof.
  - control-3 (attribution signing): BLOCKER -- the "COMPTEAM signature-root" is a PHANTOM dep (never scoped/built by COMPTEAM). RESOLUTION PROPOSED to CTO (arch-ratify 2026-07-07): bind control-3 to SCTY's EXISTING gateway RS256 identity root (no new auth, per COMPTEAM PRD SS4). ON CTO RATIFY -> GO S3 to 0.7.0_AE + wire control-3 to SCTY RS256.
  Status stays STAGED pending the CTO control-3 ratify + the strip-list fail-closed proof.</dep_check_verdict>

<priority>HIGH -- the adapter is the single choke point where all 5 controls apply. GATED on S1 CTO arch-gate. SIMULATED-ONLY. PRD SS2 + SS3 + SS4.2 + SS8-S3.</priority>
<date>2026-07-02</date>

<governance_fence>
SINGLE-TENANT-SIMULATED BUILD ONLY (MSTR DECOMP-GO 2026-07-02, LD-0239; PRD SS7). Build the broker adapter + apply all 5 controls + the app-layer meter, and PROVE them on a single-tenant simulation (simulated fleet identities under our own principal). Do NOT wire two REAL Opal employees' fleets and do NOT activate live cross-principal comms -- FENCED, held for the un-authored standing-access-class Directive. GO HELD until (i) S1 CTO-arch-gated and (ii) CTO+MSTR concur the simulated-build scope. The intra-fleet opal-agent-comms path MUST stay UNCHANGED (extend, not replace).
</governance_fence>

## Context
The broker adapter is the ONE choke point where all 5 controls apply (PRD SS2/SS3): it (a) signs+attributes outbound cross-fleet messages, (b) strips egress content, (c) classifies action/data + enforces authz, (d) enforces propose-only on inbound, (e) meters both directions. AGENTBUS EXTENDS `opal-agent-comms` -- it is a NEW cross-principal seam bridged by this adapter; the intra-fleet single-tenant path is UNCHANGED. S3 builds the adapter + the app-layer meter into the tool_activity substrate, proven on a single-tenant simulation.

## Objective
Build the broker adapter bridging `opal-agent-comms` <-> the SQS bus (S2), applying all 5 controls at the single choke point, and metering every cross-employee message into the tool_activity substrate -- proven on a single-tenant simulation.

## Scope
1. **The 5-control choke point (build to the S1 spec):** control-2 (action/data classify + SCTY authz), control-3 (sign+verify attribution off the COMPTEAM root), control-4 (egress strip via the COMPTEAM strip-list), control-5 (propose-only inbound). Control-1 (partition) is enforced at S2's IAM/SQS layer; the adapter respects it. All at ONE choke point; none optional.
2. **App-layer meter (SS4.2) into tool_activity (COMPLEARN-owned -- APPEND, do NOT fork):** log every cross-employee message `{from_employee, from_agent, to_employee, to_agent, subject, classification[data|action], size, ts, signature_verified}` into the SAME tool_activity substrate NFRA_TOOLHEALTH queries. One query surface for collaboration + tool-use.
3. **Extend, not replace:** the intra-fleet opal-agent-comms broker/inbox path is UNCHANGED (regression-proof: intra-fleet delivery still works exactly as before -- S4 re-verifies).
4. **Fail-closed everywhere:** unverifiable signature -> reject; strip-list hit -> redact/block; action-request without SCTY entitlement -> deny; default propose-only.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read the S1 DESIGN SPEC (binding); comp-which "where does the app-layer meter append into the tool_activity substrate"; confirm the tool_activity APPEND path (COMPLEARN-owned, shared with TOOLHEALTH -- do NOT fork); confirm S1 CTO arch-gate PASSED</run>
    <expect>S1 spec understood as binding; the tool_activity append surface identified as ADD-rows (not modify COMPLEARN's tables); S1 arch-gate confirmed PASS.</expect>
    <if_mismatch>STOP. If S1 is not arch-gated, do not build (S3 gated on S1). If metering requires mutating a COMPLEARN table, coordinate the substrate extension with the COMPLEARN owner + COO~B (2-project shared surface).</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>self-test all 5 controls at the choke point on a single-tenant simulation with KNOWN-BAD fixtures: forged/absent signature -> REJECT; planted secret/ARN/internal-host -> redact/block (known-bad PASSES the gate, clean flows); action-request w/o entitlement -> DENY; propose-only default; ds-commit-gate + non-ASCII + `from __future__ import annotations`</run>
    <expect>Every control fires fail-closed on its known-bad fixture; a clean message flows; the adapter is the single choke point (no control bypassable).</expect>
    <if_mismatch>STOP. Any control that a known-bad fixture bypasses = the choke point leaks = do not commit. The strip is fail-closed by construction (a distributed secret is unrecoverable).</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>run a simulated cross-fleet exchange end-to-end; confirm every message appears in tool_activity with the full metering schema; confirm intra-fleet opal-agent-comms delivery is UNCHANGED (regression); hand to CVO (S4) for live verification</run>
    <expect>Cross-employee messages appear in tool_activity `{from_employee,from_agent,to,classification,size,ts,signature_verified}` (SS6.5); intra-fleet path regression-clean (SS6.6); one query surfaces the collaboration graph.</expect>
    <if_mismatch>A metering gap or an intra-fleet regression = incomplete. Ground on the LIVE emitted rows + a real intra-fleet delivery (Rule 22).</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- NFRA_AGENTBUS-S1 (0.4.0_DE, same owner): the binding 5-control design. **Binding S1 interface = `docs/briefs/nfra_agentbus_s1_security_model_spec_DRAFT_20260702.md` (committed 4aa59029f; the docs/architecture promotion never landed -- use the brief; CTO may re-land the architecture home later, same content).** S1 CTO arch-gate = PASS (5b7ef1613). S3 BUILD still hard-gates on the C2/C3/C4 IMPLEMENTATIONS (MCPGUARD/PREMCP/COMPTEAM) landing + the P0-clear greenlight.
- NFRA_AGENTBUS-S2 (0.7.0_AE_CloudOps): the adapter bridges to S2's SQS queue-pair; respects S2's partition (control-1).
- COMPLEARN owner + NFRA_TOOLHEALTH (TH-A/TH-B): tool_activity is COMPLEARN-owned + shared with TOOLHEALTH (2-project surface). S3 APPENDS cross-employee rows; it MUST NOT fork or mutate COMPLEARN's tables. Coordinate the row schema with TH-B (the query consumer).
- NFRA_COMPTEAM: control-3 signature-root + control-4 strip-list (reuse the kit, don't re-derive).
- SCTY lane (base COO): control-2 authz gate (SCTY_MCPGUARD tier + SCTY_PREMCP token).
- 3.0.0_SA_CVO (S4): live-verifies all 5 controls at the choke point + the meter + the intra-fleet regression.
</cross_domain_coordination>

<acceptance_criteria>
1. The broker adapter applies all 5 controls at ONE choke point, each fail-closed against a known-bad fixture (forged signature REJECT, planted secret redact/block, unentitled action DENY, propose-only default) -- proven on a single-tenant simulation.
2. Every cross-employee message appears in tool_activity `{from_employee,from_agent,to,classification,size,ts,signature_verified}` (SS6.5) -- APPEND into COMPLEARN's substrate, no fork/mutation (grep-proof).
3. Intra-fleet opal-agent-comms delivery is UNCHANGED (regression, SS6.6).
4. Governance-fence honored: single-tenant simulation only, no live cross-principal activation. Session-log Compiler Tools reproduces every `<run>`. RAVC COO~B + CC CTO + COMPLEARN owner + SCTY lane.
</acceptance_criteria>

## Note
The adapter is the single point where WHO / WHAT-LEAVES / WHAT-RECEIVER-MAY-DO all bind. If a control is bypassable, the whole model leaks. Extend opal-agent-comms, never replace it -- the intra-fleet path stays exactly as before. SIMULATED-ONLY per the fence.
