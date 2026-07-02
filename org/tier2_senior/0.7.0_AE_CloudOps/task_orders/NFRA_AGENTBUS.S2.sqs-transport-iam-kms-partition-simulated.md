# TASK ORDER -- NFRA_AGENTBUS.S2 (SQS transport + IAM/KMS partition -- SINGLE-TENANT-SIMULATED)

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO~B</issued_by>
<status>staged</status>
<!-- GO FIRED 2026-07-02T~18:52Z (COO~B): all gates MET -- S1 CTO arch-gate PASS (5b7ef1613) + sim-scope CTO-bound + ETL P0 CLEARED (all 3 freezes, ledgers closed, base COO cycle-18 FINALE). Owner 0.7.0_AE IDLE:available. AUTHORIZED to build. SIM-ONLY (second fleet = SAME-ACCOUNT 2nd IAM identity, NOT real cross-principal). Any actual AWS apply rides safe-apply/deploy gates (MSTR guardrail). Flip staged->pending on start; RAVC COO~B CC CTO+SCTY-lane. -->

<priority>HIGH -- the transport + partition (control 1). GATED on S1 CTO arch-gate. SIMULATED-ONLY. PRD SS2 + SS3.1 + SS8-S2.</priority>
<date>2026-07-02</date>

<governance_fence>
SINGLE-TENANT-SIMULATED BUILD ONLY (MSTR DECOMP-GO 2026-07-02, LD-0239; PRD SS7 "design + a scoped single-tenant-simulated proof only"). Build the SQS queue-pair + IAM/KMS partition and PROVE control-1 (partition-scoped) in a single-tenant simulation (both "fleets" are simulated identities under our own principal). Do NOT wire two REAL Opal employees' fleets and do NOT activate live cross-principal comms -- that is FENCED, held for the un-authored standing-access-class Directive. GO for this TO is HELD until (i) S1's 5-control model is CTO-arch-gated and (ii) CTO+MSTR concur the simulated-build scope.
</governance_fence>

## Context
Transport = SQS (durable, decoupled, AWS-native, CloudWatch-metered by construction). A shared queue-pair per collaboration (A->B, B->A), NOT one global multi-tenant queue -- so IAM/KMS scoping is per-collaboration and blast radius is bounded to the two consenting fleets. Control-1 (partition): each fleet reads ONLY its own inbound partition. S2 builds this transport + partition and proves the partition is scoped -- in a single-tenant simulation, per the fence.

## Objective
Provision (in a single-tenant simulation) the per-collaboration SQS queue-pair + queue-policies + message-group scoping + per-collaboration KMS key, and PROVE on LIVE state that a simulated fleet reads its own inbound and is DENIED the other's inbound (control-1, provably-scoped).

## Scope
1. **Queue-pair per collaboration (SIMULATED):** A->B + B->A SQS queues under two SIMULATED fleet identities within our own principal (NOT two real employees). Per-collaboration KMS key.
2. **IAM + KMS partition (control 1, fail-closed):** queue-policy + `sqs:` action scoping + message-group scoping so simulated-fleet-A `SendMessage`s to the pair + `ReceiveMessage`s ONLY from its inbound; DENIED the other's inbound. Ground on LIVE `get-queue-policy` + a live IAM deny test (NOT TF-desired).
3. **CloudWatch metering (SS4.1, zero app-code):** `NumberOfMessagesSent/Received/Deleted`, `ApproximateAgeOfOldestMessage` per queue-pair -- confirm present by construction.
4. **comp-iam before/after any grant:** no permission gap introduced; the partition is the ONLY cross-fleet reach.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read the S1 DESIGN SPEC (the binding interface -- IAM/KMS partition design); comp-iam service <the-adapter-or-fleet-role> to see current grants; confirm the S1 CTO arch-gate PASSED (S2 is gated on it)</run>
    <expect>S1 spec understood as the binding partition design; current IAM grants enumerated; S1 arch-gate confirmed PASS before building.</expect>
    <if_mismatch>STOP. If S1 is not CTO-arch-gated, do NOT build -- S2 is gated on S1. Surface to COO~B.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>safe-apply the SQS queue-pair + queue-policies + KMS key (Terraform only -- never bare apply); comp-iam gaps after the iam.tf change; verify no new permission gap</run>
    <expect>Terraform 0-diff apply; comp-iam gaps clean (no new gap); the partition grant is exactly the designed scope.</expect>
    <if_mismatch>STOP. A comp-iam gap or a broader-than-designed grant = do not proceed; the partition is the load-bearing control.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>LIVE partition-scoped test: simulated-fleet-A ReceiveMessage on its inbound = ALLOW; simulated-fleet-A ReceiveMessage on fleet-B's inbound = DENY (live aws, not TF-desired); confirm CloudWatch send/receive counts per queue-pair</run>
    <expect>Own-inbound ALLOW + other-inbound DENY on LIVE (control-1 provably-scoped, PRD SS6.1); CloudWatch metering present per queue-pair.</expect>
    <if_mismatch>A cross-partition read that succeeds = control-1 BROKEN = a STOP-class finding. Ground on live aws, never TF-desired/self-report (Rule 22).</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- NFRA_AGENTBUS-S1 (0.4.0_DE): the binding partition design. **Binding S1 interface = `docs/briefs/nfra_agentbus_s1_security_model_spec_DRAFT_20260702.md` (committed 4aa59029f, full 5-control spec; the docs/architecture promotion never landed -- use the brief).** S1 CTO arch-gate = PASS (5b7ef1613, S1 COMPLETE), so S2's FLAG-1 gate is MET; S2 execution now yields ONLY to the P0-clear greenlight (MSTR FLAG-2).
- 1.0.0_SA_CTO: arch-gate on control-1 (partition provably-scoped, SS5.2).
- SCTY lane (base COO): the per-collaboration grant model coordinates with SCTY entitlements. CC base COO.
- opal-agent-comms: the transport bridges to the broker via the S3 adapter (not S2). S2 is the SQS + partition layer only.
- NFRA_AGENTBUS-S4 (CVO): live-verifies this partition. Your live deny-test is what S4 re-verifies independently.
</cross_domain_coordination>

<acceptance_criteria>
1. A per-collaboration SQS queue-pair + per-collaboration KMS key + queue-policies exist (Terraform, 0-diff), under SIMULATED fleet identities (no two real employees' fleets).
2. Control-1 provably-scoped on LIVE: simulated-fleet reads its own inbound, DENIED the other's inbound (live aws deny-test, not TF-desired) -- PRD SS6.1.
3. comp-iam gaps clean after the iam.tf change; CloudWatch metering present per queue-pair (SS4.1).
4. Governance-fence honored: single-tenant simulation only, no live cross-principal activation. Session-log Compiler Tools reproduces every `<run>`. RAVC COO~B + CC CTO + SCTY lane.
</acceptance_criteria>

## Note
Control-1 (the partition) is the load-bearing WHO-can-read control. Prove it fail-closed on LIVE state (a real deny), never on TF-desired. SIMULATED-ONLY per the fence: both fleets are simulated identities under our own principal; wiring two real employees is the FENCED activation, not this TO.
