# Task Order: NFRA_TERRAFORM TO-1 -- P1 COVERAGE ASSESSMENT (read-only; the load-bearing unblocker)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-08-nfra-terraform-to1-coverage</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-08</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_TERRAFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>DISPATCHED + GO 2026-07-08 (Andrew-direct NFRA-first mandate via /drive; PRD 168c5d7b1). P1 is READ-ONLY -- no infra change, so no owned-paths write risk; the deliverable is a coverage-matrix doc. FAN-OUT-WORTHY (a reader per service class / per pipeline) -- fan it out if you have capacity. Shared-lane note: 0.5.0 is coordinated with COO~B (Q4 producers done); this TERRAFORM-P1 is base-COO's NFRA lane.</dispatch_state>
    <gate_note>CTO arch-gates the coverage METHOD + completeness; CVO certs LIVE-grounded (not TF-DESIRED-alone). P1 unblocks P2 remediation (the highest-risk phase).</gate_note>
  </metadata>

  <objective>Enumerate EVERY live AWS resource (the APPLIED estate) and reconcile against Terraform state (the DESIRED) -> a per-service + per-resource-group COVERAGE MATRIX classifying each resource MANAGED-CLEAN / MANAGED-DRIFTED / UNMANAGED / ORPHANED / EXEMPT. This is the read-only assess-first that must precede any P2 remediation -- know the full gap before touching anything.</objective>

  <decisions_resolved>PRD SS9 (COO decomposition): Q1 EXEMPT-RULE = a resource is EXEMPT only if TF-managing it would be circular (the TF state backend itself -- state bucket + lock table) OR it is owned by an external/managed system by design (Amplify/console-managed-by-design, third-party); everything else is a gap-to-fix. Build the exempt-LIST with a justification per entry; CTO ratifies it. Q2 DRIFT-DEFAULT = TF-adopts-live (0-diff, no live change) is PRIMARY; apply-to-fix-live only when live is genuinely WRONG -> routes CTO+COO never-widen (P2, not P1). Q4 P3 = adopt-in-place + complete module-map FIRST (not a tidiness restructure). Q3 P4-gate = both CI-on-commit + periodic-scheduled, coverage-query as a comp-aws extension (ratified in P4).</decisions_resolved>

  <requirements>
    <requirement id="1">GROUND ON LIVE AWS, not comp-iam-DESIRED-alone (PRD SS6 -- the load-bearing method): enumerate the APPLIED estate via resourcegroupstaggingapi / AWS Config / per-service describe. comp-iam models the TF-DECLARED graph and CANNOT SEE an unmanaged resource -- the whole point is finding what TF does not know about. Use comp-aws/comp-iam for the DESIRED (TF-declared) side + `.tools/terraform.exe state list` per module for the state side; live describe/tagging-api for the APPLIED side.</requirement>
    <requirement id="2">Cover every service class in the estate (PRD SS4): Lambda, S3, IAM roles/policies, EC2, CloudFront, API Gateway, EventBridge, SQS, DynamoDB, CloudWatch alarms/logs, SNS, KMS, Glue/Athena, VPC/networking, Step Functions, Secrets Manager, CloudTrail -- across all pipelines (bd/cot/inf, globgrph, portal, m365, seeking-alpha, market-data, shared-infra) + firm-separated (never cross bd/cot/inf in the matrix).</requirement>
    <requirement id="3">Classify EACH resource: MANAGED-CLEAN (in TF, plan 0-diff) / MANAGED-DRIFTED (in TF, live!=TF) / UNMANAGED (live, not in TF) / ORPHANED (in TF state, no live) / EXEMPT (per the Q1 rule, justified). The GAP LIST = unmanaged + drifted + orphaned, per resource group.</requirement>
    <requirement id="4">DELIVERABLE: the coverage matrix + the gap list + the justified exempt-list, per resource group -- a doc under infra/aws/ (owned-paths AE lane, your commit). This is READ-ONLY assessment: NO import, NO apply, NO live change in P1 (that is P2, safe-apply + human-sign-off-gated).</requirement>
    <requirement id="5">FAN-OUT: this is a big comprehensive audit -- strongly a fan-out (a reader per service class or per pipeline). Use whatever parallelism you have; report the completeness-basis (which service classes fully enumerated vs sampled) honestly -- roster-is-a-floor: an un-enumerated class is a KNOWN gap, not silently "clean."</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase name="before_write">comp-aws / comp-iam for the TF-declared (DESIRED) side; `.tools/terraform.exe state list` per module. Live AWS describe/Config/tagging-api for APPLIED -- rail-checked as the deliberate LIVE-grounding the PRD mandates (comp-iam-DESIRED cannot see unmanaged).</phase>
    <phase name="after_commit">CVO cert request (LIVE-grounded, not TF-DESIRED-alone). RAVC me + CTO (CTO arch-gates the method + completeness).</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion>Every live resource classified, grounded on LIVE AWS (not TF-DESIRED-alone) -- unmanaged resources actually surfaced, not missed.</criterion>
    <criterion>The gap list (unmanaged+drifted+orphaned) is complete + honest, per resource group; the completeness-basis (enumerated vs sampled per class) stated.</criterion>
    <criterion>Every exemption justified per the Q1 rule (circular-state-backend OR external-by-design), CTO-ratifiable.</criterion>
    <criterion>Firm-separation preserved in the matrix (bd/cot/inf never cross). CVO certs LIVE-grounded.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/NFRA_TERRAFORM_PRD.md (CTO 2026-07-08, Andrew-direct; commit 168c5d7b1)</ref>
    <ref type="builds-on">infra/aws/TERRAFORM_PIPELINE_STRATEGY.md, LAMBDA_TERRAFORM_MAP.json, EC2_MANIFEST.json, AWS_INFRASTRUCTURE_MANIFEST.md, the prior point-in-time AWS_IAM_AUDIT/AWS_INFRASTRUCTURE_AUDIT</ref>
    <ref type="project">org/projects/NFRA_TERRAFORM.json</ref>
  </references>
</task_order>
```

<!-- ZOMBIE-RESOLVED 2026-07-13T08:04Z by 2.0.0_SA_COO.
     This TO was <status>pending</status> -- which means DISPATCHED -- while its assignee was
     NOT REGISTERED. Nobody was there. The board read it as ACTIVE work in flight.
     Flipped pending -> staged: `staged` is the TRUE state (scoped, awaiting a GO when a live
     lane exists). NOT flipped to complete -- THE WORK WAS NEVER DONE.
     Detector: .tools/to-liveness-join.py (e8ed4e1d2) -- the join /to-check and fabric-check
     never made. A dispatch into an unverified lane is a hope, not a drive. -->
