<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-11.teams-agent-inbound-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~R</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.inbound4.md</decomp_doc> (workstream INBOUND, round 4): the apply leg of cell `CT-i-6` (complete as a build, merged @ebc8931b3c)
<owned_cells>CT-i-6</owned_cells>
</decomp_ref>

  <objective>
    Deploy the Teams agent's function package (the inbound-work changes of NFRA_CTLPLN workstream INBOUND) and let its role send
    to the two Dell bus queues: ONE targeted apply of ONE module, `module.ldo_001`, in the root `infra/aws/terraform/transcripts/`.
    QUEUE POSITION, ruled by `1.0.0_SA_CTO` (msgs 106725, 106772): this order runs AFTER the two access applies already ahead
    of it on this seat (TO-APPLY-10; identity plan 1). Do not start it before them.
    AMENDMENT 1 (issuer, 2026-10-08 ~07:2xZ, on `1.0.0_SA_CTO` ruling msg 106821, which re-rules condition 2 of the CTO half):
    "The two acts share no root; the order was a queue, not a dependency. NFRA_CTLPLN's Teams-agent order runs now on
    0.7.0_AE_CloudOps~E, ahead of plan 1, and plan 1 follows when its GO arrives." TO-APPLY-10 is applied and closed. The
    queue gate above is CLEARED: this order runs NOW. Every other condition and stop of both halves stands unchanged.
  </objective>

  <context>
    The change on the trunk: two statements in `chat_assist.tf` `extra_statements` (`TellDell1OnTheBus`, `TellDell2OnTheBus`,
    commit 9734652dbe) and the package built by `infra/aws/lambda/teams-chat-assist/build.sh` from the trunk's
    `data/transcripts/scripts/teams_chat/`, `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json` and
    `infra/logic/registry/*.json`.
    THREE FACTS ABOUT THIS ROOT, all measured by cell CT-i-6 at ~04:5xZ, all in both halves:
    (1) UNTARGETED, the root plans `9 to add, 4 to change, 0 to destroy`: another project's unapplied pull function and
        `aws_lambda_function.mail_pull`. NONE of it is yours to apply.
    (2) The configuration does not load until BOTH packages exist on disk: `pull.tf` and `mail_pull.tf` hash
        `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip`. Build both (`bash infra/aws/lambda/transcripts-pull/build.sh`,
        `bash infra/aws/lambda/teams-chat-assist/build.sh`). Building uploads nothing; the target excludes the pull resources.
    (3) Plan and apply with the environment variable `TF_DATA_DIR` set to a NEW scratch directory outside every git tree. The
        cell's `init` there configured the declared S3 backend with no migration prompt. Do NOT run `init -reconfigure` or
        `init -migrate-state`, and do not write the root's own `.terraform` directory.
    Targeted at `module.ldo_001`, the cell's plan read `0 to add, 3 to change, 0 to destroy`:
    `module.ldo_001.aws_iam_policy.exec` (two statements added, none removed), `module.ldo_001.aws_lambda_function.handler`
    and `module.ldo_001.aws_lambda_function.ingress[0]` (each `source_code_hash` only). The cell's package SHA-256 was
    `c1af3fe33556e895ec97cbf0ad6bd1915596f4daee5c259d1fca55a697d1da32`.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. ONE go, no second message.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_INBOUND_TEAMS_AGENT_DEPLOY_COO_R_20261008.md (@48a5998fd0)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_INBOUND_TEAMS_AGENT_DEPLOY_20261008.md (@e58bcf5d8e)
    Read both in full first and carry every condition of both (the COO's six, the CTO's four). An untargeted apply voids the pair.

    TWO STOPS BEFORE ANYTHING: (a) the End of Day window: do not apply between 20:00Z and 21:45Z; (b) a job in state `bidding`
    on the live agent that you can see from the function's newest log lines: wait for its award or stop and report.

    THE COMMIT: the shared tree at its HEAD on CLOUD, which must contain ebc8931b3c. Print
    `git diff --stat ebc8931b3c HEAD -- data/transcripts/scripts/teams_chat lib/opal_naming.py org/standards/NAMING_SCHEMA.json infra/logic/registry infra/aws/lambda/teams-chat-assist infra/aws/terraform/transcripts daily_reports/eod/post_format.py daily_reports/eod/VOICE.md`.
    A difference under `infra/aws/terraform/transcripts` is a STOP. Any other difference is named, file by file, in the report.

    1. Load /cloud-ops. Run `python infra/aws/terraform/transcripts/tests/check_chat_assist_bus.py` (expect
       `CHAT-ASSIST-BUS ok=True boxes=4 statements=4 matched=4 extra=0`) and
       `python data/transcripts/scripts/teams_chat/gen_bus_devices.py --check` (expect `BUS-DEVICES ok=True`). A failing check is a STOP.
    2. Build both packages. Record the Teams package's SHA-256 and file count.
    3. Set `TF_DATA_DIR` to the scratch directory and run `terraform -chdir=infra/aws/terraform/transcripts init -input=false`.
       If it asks to migrate or reconfigure state, STOP. Print the backend it initialised against. Hash the root's own
       `.terraform/terraform.tfstate` before and after this order: it must be unchanged.
    4. BEFORE: save, with SHA-256 each, the LIVE policy document of the agent's managed policy (the default version) and each
       of the two functions' `CodeSha256` and `LastModified`. These are the rollback references.
    5. Plan TARGETED at exactly `module.ldo_001` (echo the argument back), with the state lock taken (no `-lock=false`).
       - EXACTLY `0 to add, 3 to change, 0 to destroy`, the three addresses above; the policy diff is exactly the two
         statements, each Allow, actions exactly `sqs:GetQueueUrl` and `sqs:SendMessage`, Resource the one Dell queue, ZERO
         removed lines; each function's only changed argument is `source_code_hash` (with `last_modified` known after apply),
         and the new hash decodes to the SHA-256 of the package you built -> go to 6.
       - ANY address outside the module, any add, destroy or replacement, any other function argument, any removed policy
         line, any other action, queue or Sid -> apply NOTHING; report the plan as read and stop.
    6. Open ONE NEVER-2 ledger entry naming the laptop, both functions as the families that take the package, the saved
       references by path and hash, both halves, and the rollback (below).
    7. ONE apply through `.tools/safe-apply.sh`, TARGETED at the same one address, with the same `TF_DATA_DIR`. If the wrapper
       cannot be made to use the scratch data directory or the target, STOP and report rather than apply any other way.
    8. Read-back LIVE: both functions' `CodeSha256` equal the built package's; the live policy equals the saved one plus
       exactly the two statements (parsed, with a planted-mutant control); a targeted re-plan reads no changes; an UNTARGETED
       plan (read-only, `-lock=false`) still reads `9 to add` and now `1 to change`: report its counts, apply none of it.
    9. CTO CONDITION 3, within the first hour after the apply and before the report calls it clean: read both functions'
       error counts and the newest log lines of ONE ordinary invocation each (the scheduled tick is enough; make no
       invocation). Zero new error signatures, or the signature. If an import or address fault shows, run the CODE rollback
       in this same session and say so.
    10. COO CONDITION 4: state, from the fabric manager's record or by asking `0.0.0_AB_MSTR` once, which boxes have pulled
       past 2660df145d (the box half). Name any that has not; the apply does not wait on it.
    Close the entry.
    You invoke neither function, send no test event, no text and no bus line, and read no chat or mail content. Until one
    real request from a person in Teams runs, the deploy is APPLIED, not EXERCISED: say so in those words.

    ROLLBACK, per property. Policy: revert the two statements (commit 9734652dbe's edit) and the same targeted apply; the
    saved policy document is the reference. Code: check out the packaged paths at 55cb79f93c in a scratch worktree, rebuild
    there, confirm the rebuilt hash is `IBrveNQC+Zbry9pHjbJ7C1Ww6EZb95XRXaFrziNSn6E=`, and the same targeted apply.
  </the_act>

  <bounds>
    - This one module only. NEVER an untargeted apply of this root. No `init -reconfigure`, no `init -migrate-state`, no write
      to the root's own `.terraform`, no edit to any file of the root.
    - `safe-apply` only; never `aws lambda update-function-code`. No push of a shared branch.
    - No invocation, no test event, no text, no bus line, no chat or mail read.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing and changes no clock; the function's one-minute ingress clock is unchanged by the plan as read.
comp-iam: RUN at the cut by the cell's check on the written file -- denominator: 4 register boxes, 4 statements, 2 actions each, 0 extra; the grant is send-only on two named queues. BLIND: inline policies attached to the role by hand are not listed; the live read-back is the applier's.
comp-adversary: RUN -- another project's nine creates and one hash applied by accident (targeted plan and targeted apply only; the untargeted count is re-read after); a package that differs from the measured one (the applier diffs the packaged paths since ebc8931b3c and names every file); a fault from the naming files that ride the package (the first-hour log read and the same-session code rollback); a deploy inside the End of Day window or over a job in bidding (two stops); a backend reconfiguration answered by the applier (a stop). BLIND: the model's behaviour on a real message; that is the outcome's own exercise.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-i-6"><invocation>python infra/aws/terraform/transcripts/tests/check_chat_assist_bus.py</invocation><expect>CHAT-ASSIST-BUS ok=True boxes=4 statements=4 matched=4 extra=0</expect></criterion>
  <criterion id="AC2" cell_refs="CT-i-6" judgment="true"/>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~R when the entry closes, or at a STOP (name the step): the packaged-path diff since
    ebc8931b3c; both check lines; the package's SHA-256; the backend initialised against and the proof the root's own
    `.terraform` is unchanged; the saved references' paths and hashes; the targeted plan's count and each change as read; how
    the apply was targeted through the wrapper; the live read-back; the targeted re-plan and the untargeted counts; the
    first-hour error and log read; which boxes hold the box half; THE HOUR THE DEPLOY WENT LIVE (the CTO tells Andrew from
    it); the ledger entry's path and close; the proof-of-spec instance path (genre DEPLOY) and its check result; commit hashes
    and the measured push state. AC2 (the deploy is as both halves describe) is the issuer's and the CVO's to grade: do not
    mark it PASS or FAIL. Leave the status flip to the issuer.
  </report>
</task_order>
