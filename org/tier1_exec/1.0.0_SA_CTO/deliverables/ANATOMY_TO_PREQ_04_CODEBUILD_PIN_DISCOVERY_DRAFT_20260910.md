# DRAFT — ANATOMY.TO-PREQ-04-CODEBUILD-PIN-DISCOVERY~Y

Prepared by: `1.0.0_SA_CTO~Y`

Proposed issuer: `2.0.0_SA_COO~Y` (or acting COO seat)

Proposed assignee: `0.7.0_AE_CloudOps~Y`

Proposed issued path:
`org/tier2_senior/0.7.0_AE_CloudOps~Y/task_orders/ANATOMY.TO-PREQ-04-CODEBUILD-PIN-DISCOVERY~Y.md`

State: **DRAFT / PENDING CVO OPERATIONAL REVIEW AND COO ISSUANCE / NO GO**

This draft is not an assignment and authorizes no AWS or local action. Its
purpose is to make the proposed next operational boundary concrete while the
CVO review order awaits COO issuance.

<task_order>
  <metadata>
    <id>ANATOMY.TO-PREQ-04-CODEBUILD-PIN-DISCOVERY~Y</id>
    <issued_by>REQUIRED: COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Y</issued_to>
    <assignee>0.7.0_AE_CloudOps~Y</assignee>
    <date>2026-09-10</date>
    <status>draft-no-go</status>
    <project_code>ANATOMY</project_code>
  </metadata>

  <objective>
    Refresh the perishable PREQ-04 CodeBuild inventory, enumerate the exact
    Windows images advertised by CodeBuild in `us-east-1`, determine what
    immutable identity (if any) AWS exposes for those images, and return the
    minimum exact facts needed to design a separate provisioning/capability-
    probe order. Do not provision, invoke, copy, contact, or tear down anything.
  </objective>

  <authority_ceiling>
    Andrew selected CodeBuild and directed the Proposal H work to proceed. The
    recorded direction permits preparation of the successor boundary; this
    stage remains deliberately below provisioning and invocation. A later
    order must separately authorize any project/IAM/network/artifact mutation,
    build start, endpoint contact, containment mutation, evidence export, and
    teardown.
  </authority_ceiling>

  <pinned_inputs>
    <input bytes="12600" sha256="0619DEE34A48D5926B09F6F40DD5B518F4E06CEED82C9A0B50A831A67410B410">org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_DISCOVERY_EVIDENCE~Y.md</input>
    <input bytes="20650" sha256="31667406B12D1CC6CC332E0F2EF1A7BB8F773196C1BBC0C632CF5E10E31F3B7C">org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_DISCOVERY_PROOF~Y.json</input>
    <input bytes="7588" sha256="733973603096003DBB1E6DBB6872329385F8649452B2C45F7592304D7B183428">C:/Users/AndrewBerman/Downloads/docs_abcdeg/fabric/PHASE_3_P3_TO_05_PREQ_04_CODEBUILD_EXECUTION_TASK_ORDER_CANDIDATE_20260905.md</input>
    <input bytes="6211" sha256="849F172B0FA6C3F7D5E60A1935662A1B1662343CB3CC463A7CDBEC6068344BBF">C:/Users/AndrewBerman/Downloads/docs_abcdeg/fabric/preq04_codebuild_review_20260905/00_PACKAGE_MANIFEST.md</input>
    <input bytes="2553" sha256="1A88B6314AFA47F2D0E0F10484046B9B0E4A6BA3A5835A5E92F54665B3CF096D">org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_RELAY_20260909_CODEBUILD_H_RESUME_AND_CVO_OPERATIONAL_VALIDATOR.md</input>
  </pinned_inputs>

  <aws_action_allowlist>
    <action id="A1">sts:GetCallerIdentity</action>
    <action id="A2">codebuild:ListCuratedEnvironmentImages</action>
    <action id="A3">codebuild:ListProjects</action>
    <action id="A4">codebuild:BatchGetProjects</action>
  </aws_action_allowlist>

  <exact_work>
    <step id="1">Authenticate the issued order and every pinned input by path, bytes, and SHA256. STOP on mismatch.</step>
    <step id="2">Run `sts:GetCallerIdentity` once and record account, partition, caller ARN, and UTC. Do not read or print credential material.</step>
    <step id="3">Resolve the configured effective region without changing it. It must equal `us-east-1`; otherwise STOP with REFUSE.</step>
    <step id="4">Run `codebuild:ListCuratedEnvironmentImages` once. Return the complete Windows subset with environment type, image identifier, runtime/platform fields, pagination facts, and denominator. State precisely whether the response exposes a digest, immutable version, or only a mutable/provider-managed tag. Do not infer immutability.</step>
    <step id="5">Run `codebuild:ListProjects` once, handle pagination, then run `codebuild:BatchGetProjects` only for the exact returned names. Return the same ordered fields and denominators as the prior discovery so staleness and drift can be compared.</step>
    <step id="6">From local reasoning only, produce a red/green pin matrix for account, partition, region, operating caller, project, image, service role, VPC/routing, contacts, source/artifacts, evidence store, KMS, retention, duplicate refusal, rollback, and teardown. Evidence may close a pin only when it supplies the exact required identity; do not select a Linux project for the Windows workload.</step>
    <step id="7">State which platform requirements remain exercise-only: elevated administrative token, BFE/MpsSvc control, WFP lifecycle, Job Object containment/no-breakaway, ETW/process/DNS/route/socket capture, credential and metadata negative controls, and evidence export/readback. List-curated output cannot by itself PASS any exercise-only row.</step>
    <step id="8">Return one recommendation for the next boundary: REFUSE_CODEBUILD, PROVISIONING_ORDER_READY, or MORE_READ_ONLY_FACTS_REQUIRED. Name exact missing facts and proposed AWS actions if more reads are required; do not perform them.</step>
  </exact_work>

  <constraints>
    <constraint>Exactly A1-A4 and no other AWS API actions. CLI retries that would create additional API calls are disabled or counted and reported; any unexpected retry is REFUSE.</constraint>
    <constraint>No create, update, put, attach, detach, tag, start, stop, retry, delete, import, export, role assumption, secret read, credential inspection, artifact read/copy, or endpoint contact.</constraint>
    <constraint>No CodeBuild run and no capability claim based only on image listing, marketing description, desired configuration, or an existing Linux project.</constraint>
    <constraint>No mutation of `scratchpad_tmp`, `docs_abcdeg`, infrastructure, deployment state, or customer estate. Local writes are limited to the exact CloudOps deliverables named below and a canonical session log.</constraint>
    <constraint>No push.</constraint>
  </constraints>

  <deliverables>
    <evidence>org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_PIN_DISCOVERY_EVIDENCE~Y.md</evidence>
    <proof>org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_PIN_DISCOVERY_PROOF~Y.json</proof>
  </deliverables>

  <acceptance_criteria>
    <criterion id="C1">ACK exact order ID and content before A1.</criterion>
    <criterion id="C2">Pinned inputs authenticate or work stops before AWS.</criterion>
    <criterion id="C3">Every AWS call is A1-A4, with UTC, exact command/action, exit code, stderr, retry count, pagination, and denominator.</criterion>
    <criterion id="C4">The full Windows curated-image subset is reported, including the exact immutable-or-mutable identity finding.</criterion>
    <criterion id="C5">Current project inventory is reconciled against the prior four-project discovery without selecting or mutating a project.</criterion>
    <criterion id="C6">Every pin and exercise-only capability has one evidence-grounded state; unknown remains RED.</criterion>
    <criterion id="C7">No prohibited effect occurred, and the claim is explicitly an executor attestation rather than an independent account-history audit.</criterion>
    <criterion id="C8">Handback to CTO, CVO, COO, and CRO names both deliverable paths, bytes, SHA256, commit, recommendation, and unresolved-row denominator.</criterion>
  </acceptance_criteria>
</task_order>

## Promotion rule

CTO may route this draft for COO issuance only after the CVO operational review
returns `PASS_TO_CUT_CLOUDOPS_PIN_ORDER` or CTO incorporates every exact AMEND.
Formal CRO certification remains required for any later provisioning,
capability-probe, H-payload, or admission order.
