# pipeline-override: This task is an ad-hoc read-only discovery order for the separately governed docs_abcdeg Anatomy sequence, not an ajb_workspace registered project or mutation pipeline.

<task_order>
  <metadata>
    <id>ANATOMY.TO-PREQ-04-CODEBUILD-DISCOVERY~Y</id>
    <issued_by>1.0.0_SA_CTO~Y</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Y</issued_to>
    <assignee>0.7.0_AE_CloudOps~Y</assignee>
    <date>2026-09-05</date>
    <status>complete</status>
    <completion>
      Executed and handed back 2026-09-05. Disposition COMPLETE -- no refusal, denial, ambiguity or PARTIAL, and no scope widening.
      Evidence packet: org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_DISCOVERY_EVIDENCE~Y.md (12600 bytes, SHA256 0619dee34a48d5926b09f6f40dd5b518f4e06ceed82c9a0b50a831a67410b410, committed d94ca7c81e; digest independently re-measured and confirmed by both 1.0.0_SA_CTO~Y and 4.0.0_SA_CRO~Y).
      Proof of spec: org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_DISCOVERY_PROOF~Y.json -- proof-of-spec-check.py C1,C2,C3,C4,C5,C6,C7,C8 returns VALID rc=0, acceptance rows=8, violations=0, checker-vintage e3a9d207dc.
      All eight criteria PASS. Exactly three AWS calls made (sts:GetCallerIdentity, codebuild:ListProjects, codebuild:BatchGetProjects), all exit 0, no mutation, no CodeBuild run, no push.
      Headline: 4 live CodeBuild projects, ALL LINUX_CONTAINER -- zero Windows on both the live and declared planes; vpcConfig absent and concurrentBuildLimit unset on 4 of 4.
    </completion>
    <project_code>ANATOMY</project_code>
  </metadata>

  <objective>
    Produce a secret-free immutable evidence packet from bounded read-only AWS and local CodeBuild discovery so CTO can render the six PREQ-04 review byte sets and a later exact candidate execution order for independent CRO review.
  </objective>

  <authority>
    Andrew assigned AWS/container work to 0.7.0_AE_CloudOps~Y and continuation governance to CTO/CRO. CRO passed only the seven-step read-only discovery sequence and amended the runtime predicate for this live Claude seat. The controlling external order is C:/Users/AndrewBerman/Downloads/docs_abcdeg/fabric/PHASE_3_P3_TO_05_PREQ_04_CLOUDOPS_READ_ONLY_DISCOVERY_TASK_ORDER_20260905.md, bytes 3677, SHA256 0F1321F3BA21F962AE36B320CC960811DCE1328F183A9B9CF352AA23D7011FDC.
  </authority>

  <preflight>
    comp-schedule: RUN -- CTO measured the approved 02 sequence immediately before issuance: Phase 3 active; product c71e730 certified; PREQ-04 discovery is the current bounded motion.
    comp-iam: DECLARED-NOT-APPLICABLE -- Caller principal and project ARNs are the unknowns this read-only task measures; no permission sufficiency is claimed, denied reads are evidence, and no mutation action is authorized.
    comp-adversary: DECLARED-NOT-APPLICABLE -- CRO already adversarially bounded the exact discovery actions; CloudOps must report refusals without widening them.
  </preflight>

  <exact_work>
    <step id="1">Run AWS STS caller-identity discovery and record account, ARN, user ID, and partition without exposing credential material.</step>
    <step id="2">Record the effective configured/default AWS region and its evidence source. If absent, report ABSENT and do not choose one.</step>
    <step id="3">Use only codebuild:ListProjects and codebuild:BatchGetProjects to enumerate existing projects and record environment type, image identifier, compute type, service role ARN, source, artifacts, VPC/subnet/security groups, logs, timeout, and queued timeout.</step>
    <step id="4">Inspect the four already identified local CodeBuild Terraform declarations and record exact paths, bytes, SHA256, declared environment types, and relationship or non-relationship to AWS inventory.</step>
    <step id="5">Return one immutable evidence packet in the CloudOps deliverables directory with exact commands/API actions, UTC timestamps, exit codes, stdout/stderr or bounded redactions, caller/region evidence, complete project inventory, local-file evidence, refusals, and non-claims.</step>
  </exact_work>

  <constraints>
    <constraint>No AWS create, update, start, stop, retry, delete, import, export, tag, or other mutation.</constraint>
    <constraint>No IAM change or role assumption; no secret/credential value read or print.</constraint>
    <constraint>No arbitrary endpoint contact, final-project selection, product/source copy, CodeBuild run, product/fabric mutation, deployment, customer-estate action, or push.</constraint>
    <constraint>If a read is denied, ambiguous, absent, or would exceed scope, stop that action and return the partial packet with exact evidence.</constraint>
  </constraints>

  <acceptance_criteria>
    <criterion id="C1">ACK by exact task-order ID and content before the first AWS call.</criterion>
    <criterion id="C2">Every AWS action is one of sts:GetCallerIdentity, codebuild:ListProjects, or codebuild:BatchGetProjects.</criterion>
    <criterion id="C3">Caller identity and region evidence are complete or explicitly ABSENT/REFUSED.</criterion>
    <criterion id="C4">All returned CodeBuild projects are inventoried with the ordered fields, with pagination handled and denominators stated.</criterion>
    <criterion id="C5">The four local Terraform declarations are authenticated and compared without mutation.</criterion>
    <criterion id="C6">Evidence packet states exact commands/actions, timestamps, exit codes, errors/refusals, and non-claims.</criterion>
    <criterion id="C7">No prohibited effect occurred.</criterion>
    <criterion id="C8">Completion handback names packet path, bytes, SHA256, and disposition to CTO and CRO.</criterion>
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/ANATOMY_PREQ_04_CODEBUILD_DISCOVERY_PROOF~Y.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Surprise channel: one line to 1.0.0_SA_CTO~Y and 4.0.0_SA_CRO~Y; take no out-of-scope action.</requirement>
  </requirements>
</task_order>
