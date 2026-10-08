<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-19.teams-agent-r6-code-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~R</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.inbound6.md</decomp_doc> (workstream INBOUND, round 6, macro COMM): the apply leg of cells `CT-i-9` and `CT-i-12` (built, merged @897fbf8e1f and @840de68f9c; hookups @fff0bc0a11)
<owned_cells>CT-i-9,CT-i-12</owned_cells>
</decomp_ref>

  <objective>
    Deploy the Teams agent's round-6 function package: ONE targeted apply of ONE module, `module.ldo_001`, in the root
    `infra/aws/terraform/transcripts/`. CODE ONLY: no policy line, no other resource. NOT BEFORE 21:45Z 2026-10-08 (the End of
    Day window is 20:00Z to 21:45Z), and NOT while an End of Day event is in flight on the agent's queue (STOP 3 below).
  </objective>

  <context>
    BOTH HALVES SIGNED; read both in full before acting:
    - COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_INBOUND_R6_TEAMS_AGENT_CODE_DEPLOY_COO_R_20261008.md` @b07357fa48 (branch A/B, rollback, conditions 1-4);
    - CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_COMM_LDO001_CODE_DEPLOY_R6_20261008.md` @1dd8aa70e7.
    The package is built by `infra/aws/lambda/teams-chat-assist/build.sh` from a trunk that contains `79d7b6cbbe`; since round 5
    its text files are written LF inside the package, so its hash is a function of the commit. The previous deploy of this
    module (TO-APPLY-11, live 08:15Z 2026-10-08, ledger
    `org/critical_paths/change_management/20261008T0810Z_nfra-ctlpln-inbound-teams-agent-deploy-laptop-20261008_deploy_completion.md`)
    is the model for every step: both packages built so the root loads (`pull.tf`/`mail_pull.tf` hash the transcripts-pull
    zip), `TF_DATA_DIR` set to a NEW scratch directory outside every git tree, never `init -reconfigure`, apply through
    `.tools/safe-apply.sh` with the one `-target=module.ldo_001`. Untargeted, the root still carries another project's
    unapplied resources: NONE of them is yours.
  </context>

  <steps>
    0. Read both halves. Open the NEVER-2 ledger entry naming the two function families that take the package:
       `teams-global-chat-assist-handler-lambda` and `teams-global-chat-assist-ingress-lambda`.
    1. STOP 1 (diff): `git diff --name-only 79d7b6cbbe HEAD` over the packaged paths (`data/transcripts/scripts/teams_chat/`,
       `infra/aws/terraform/modules/ldo/runtime/ldo.py`, `infra/aws/lambda/teams-chat-assist/handlers.py`,
       `daily_reports/eod/`, `lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`, `infra/logic/registry/`) and over
       `infra/aws/terraform/transcripts/`: a change under `teams_chat/`, `ldo.py`, `handlers.py` or `daily_reports/eod/`
       is branch B (STOP and report); any other change is named file by file in the report.
    2. BEFORE (saved with SHA-256, paths in the report): both functions' `CodeSha256` and `LastModified`; the live package zip
       (`lambda get-function`, its hash equal to the live `CodeSha256`); the live state object
       `s3://opal-data-transcripts/teams/transcripts/state/chat_assist/global/cursor.json` (read it as bytes into your
       deliverables folder; do not print it).
    3. STOP 3 (End of Day): the time is after 21:45Z; `sqs get-queue-attributes` on `teams-global-chat-assist-queue.fifo`
       reads `ApproximateNumberOfMessagesNotVisible`, and the handler log group has no `"kind": "eod.` line in the last 60
       minutes that is not followed by its `ldo_event` line. Either one open -> wait and re-read; never apply over it.
    4. Build both packages; record the Teams package's SHA-256 and file count. Targeted plan with the lock taken: branch A is
       `0 to add, 2 to change, 0 to destroy`, the two functions, `source_code_hash` (and `last_modified`) only, decoding to the
       built package; anything else is branch B (apply NOTHING, report).
    5. Apply, same target, same `TF_DATA_DIR`. Record the hour it went live from CloudTrail (`UpdateFunctionCode`).
    6. AFTER: both live `CodeSha256` equal the built package's; a targeted re-plan reads no changes; within 5 minutes the
       ingress log shows an `ingress_poll` line carrying `chats_read`, `pages` and `messages`, and no `ingress_step_failed`
       with `"step": "chats"` (one with `"step": "channels"` a minute is EXPECTED until the gateway's release; count them).
    7. Close the ledger entry.
  </steps>

  <rules>
    Invoke neither function; send no test event, text or bus line; read no chat, mail or message content. No untargeted
    apply. Write only your deliverables folder, the ledger entry and its sentinel, and this order's report section.
  </rules>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-i-9"><invocation>python data/transcripts/scripts/tests/test_inbound_poll_cursors.py</invocation><expect>POLL-CURSORS ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-i-9,CT-i-12" judgment="true"/>
</proof_of_spec>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this act changes no schedule; the agent's minute clock and End of Day rules are untouched (code hash only).
comp-iam: DECLARED-NOT-APPLICABLE -- denominator: 0 policy lines change (branch A requires `aws_iam_policy.exec` unchanged); the applier's own access is the one that applied TO-APPLY-11 to this module. BLIND: live inline policies on the role, not listed.
comp-adversary: RUN -- an untargeted apply landing another project's resources (one target, STOP at branch B); a deploy over an in-flight End of Day event (STOP 3); a package whose hash depends on the working tree (LF-normalised since round 5; hash recorded); a rollback that cannot be rebuilt (the live zip is downloaded and hashed before); a v2 cursor the old code cannot read (it reads as a first run, one silent minute; the live cursor is saved); a test text sent by the applier (forbidden). BLIND: the once-key collision found 21:2xZ (row S34) is NOT fixed by this package; it is round 7's first cell.
lane: CloudOps applies under both signed halves (COO @b07357fa48, CTO @1dd8aa70e7).
</preflight>

  <report>
    Report ONCE to 2.0.0_SA_COO~R when the entry closes, or at a STOP (name the step): the packaged-path diff since
    79d7b6cbbe; AC1's line at the build commit; the package's SHA-256 and file count; the saved references' paths and hashes;
    the End of Day read (queue attributes and the log read, with a non-zero positive control on the same filter); the
    targeted plan as read; the live read-back; the targeted re-plan; the first five minutes of ingress lines by event (counts
    only); THE HOUR THE DEPLOY WENT LIVE; the ledger entry's path and close; commit hashes and the measured push state. AC2
    (the deploy is as both halves describe) is the issuer's and the CVO's to grade: do not mark it. Leave the status flip to
    the issuer.
  </report>
</task_order>
