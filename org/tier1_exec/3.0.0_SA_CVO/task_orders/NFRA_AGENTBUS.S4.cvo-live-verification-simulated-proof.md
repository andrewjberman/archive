# TASK ORDER -- NFRA_AGENTBUS.S4 (CVO live verification of the 5 controls -- on the SIMULATED proof)

<issued_to>3.0.0_SA_CVO~B</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_AGENTBUS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>

<priority>HIGH -- the security controls are worthless unverified. CVO independence, on LIVE state. GATED on S2 + S3. SIMULATED PROOF ONLY. PRD SS5 + SS6.</priority>
<date>2026-07-02</date>

<governance_fence>
VERIFY THE SIMULATED PROOF ONLY (MSTR DECOMP-GO 2026-07-02, LD-0239; PRD SS7). Verify the 5 controls on the single-tenant SIMULATED harness (S2+S3), on LIVE AWS/served state. Do NOT verify (or request) a two-real-fleet live activation -- that is FENCED, held for the un-authored standing-access-class Directive. GATED on S2 + S3.
</governance_fence>

## Context
Cross-principal comms is the attack surface; the 5 controls ARE the project. Each is fail-closed and independently CVO-verifiable on LIVE (PRD SS5/SS6). CVO independence (Constitution Art. XIV): the verifier is not the do-er; grounds against live AWS/served state (get-queue-policy, live signature check, actual strip on a real message), NEVER TF-desired or a producer self-report (PRD SS5.6, CLAUDE.md Rule 22). This TO verifies the controls on the single-tenant simulated proof.

## Objective
Independently run the SS6 acceptance on the live simulated harness: partition-scoped, attribution-signed, strip-fail-closed, action-authz-enforced, metered, intra-fleet-unchanged.

## Scope (the SS6 acceptance run, on LIVE simulated state)
1. **Partition provably-scoped (SS6.1):** simulated-fleet-B receives from ITS inbound; is DENIED (live IAM) a ReceiveMessage on fleet-A's inbound. Live get-queue-policy + a real deny, not TF-desired.
2. **Attribution provably-signed (SS6.2):** a message with invalid/absent signature is REJECTED; a valid one records the true signed `from_employee+from_agent` (not a claimed serial). Test with a forged fixture.
3. **Strip fail-closed (SS6.3):** an outbound message with a planted secret/ARN/internal-hostname is redacted-or-blocked (known-bad PASSES the gate); a clean message flows.
4. **Action-vs-data authz (SS6.4):** an inbound ACTION-request without the SCTY entitlement is DENIED at the authz gate; a DATA-share is delivered read-only; NO cross-boundary mutation without the explicit authz path.
5. **Metering (SS6.5) + intra-fleet regression (SS6.6):** every message appears in tool_activity with the full schema + CloudWatch per-queue-pair counts; intra-fleet opal-agent-comms delivery is UNCHANGED.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read the S1 spec + S2/S3 deliverables; comp-which "how do I live-verify an SQS queue-policy partition + a KMS-scoped receive deny"; establish INDEPENDENT live-verification paths (not re-running S2/S3's own tests)</run>
    <expect>An independent live-verification path per control identified (live aws get-queue-policy / IAM simulate / a real forged-message send), not a re-run of the builder's self-test.</expect>
    <if_mismatch>If the only check is re-running the builder's test, that is not independent -- find the live AWS ground-truth path (sharpest-test-binds).</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>run each SS6 control live on the simulated harness: partition deny-test, forged-signature reject, planted-secret strip, unentitled-action deny, metering presence, intra-fleet regression; capture live evidence per control</run>
    <expect>Each control PASSES fail-closed on LIVE (real deny / real reject / real strip); metering present; intra-fleet unchanged. Any failure = a CONFIRMED finding -> REWORK to the owning TO (S2/S3), not acceptance.</expect>
    <if_mismatch>A control that passes on TF-desired but fails on LIVE = the exact gap this TO exists to catch. Ground on live AWS (Rule 22).</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>emit the S4 verdict (VALIDATED / VALIDATED_WITH_GAPS / REWORK) with per-control `grounding:` (live aws output / file:line); RAVC COO~B + CC CTO + MSTR</run>
    <expect>A verdict on the record with grounding per control; could-not-verify recorded as a finding; the simulated proof is certified (or gaps named).</expect>
    <if_mismatch>No silent pass. An ungrounded security claim is NON-ACTIONABLE (Rule 22) -- withhold the cert until grounded on live.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- NFRA_AGENTBUS-S2 (0.7.0_AE_CloudOps) + S3 (0.4.0_DE): the verification SUBJECTS. CVO is independent -- verify their LIVE artifacts, do NOT co-author.
- 1.0.0_SA_CTO: arch-gated the 5 controls; CVO independence means CVO does NOT verify as CTO's subordinate on the security verdict (Constitution Art. XIV).
- SCTY lane (base COO): control-2 authz path; coordinate the live entitlement-deny test.
- 0.0.0_AB_MSTR: the S4 verdict is the evidence that pairs with the Directive surfacing (the simulated proof is what the standing-access-class Directive would be authorized against).
</cross_domain_coordination>

<acceptance_criteria>
1. All 5 controls verified on LIVE simulated state (partition-scoped deny, signature-reject, strip-fail-closed, action-authz-deny, metered, intra-fleet-unchanged) -- PRD SS6, grounded on live aws NEVER TF-desired/self-report.
2. Every control carries `grounding:` (live aws output / file:line); could-not-verify recorded as a finding (Rule 22).
3. Verdict on the record (VALIDATED / VALIDATED_WITH_GAPS / REWORK) RAVC'd to COO~B + CC CTO + MSTR.
4. Governance-fence honored: only the single-tenant simulated proof is verified; no two-real-fleet activation is verified or requested. Session-log Compiler Tools reproduces every `<run>`.
</acceptance_criteria>

## Note
The controls are worthless unverified, and worthless verified on TF-desired -- the whole point is LIVE fail-closed behavior (a real deny, a real reject, a real strip). This verdict on the simulated proof is precisely the evidence the standing-access-class Directive would be ratified against before any two real fleets are wired.
