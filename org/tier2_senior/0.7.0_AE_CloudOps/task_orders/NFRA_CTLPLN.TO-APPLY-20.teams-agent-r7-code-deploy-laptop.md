<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-20.teams-agent-r7-code-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~R</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.inbound7.md</decomp_doc> (workstream INBOUND, round 7, macro COMM): the apply leg of cell `CT-i-13` (built, merged @75420934c2)
<owned_cells>CT-i-13</owned_cells>
</decomp_ref>

  <objective>
    Deploy the Teams agent's round-7 function package (rows S34 and S33, cursor pruning, the Kimi budget): ONE targeted apply
    of ONE module, `module.ldo_001`, in the root `infra/aws/terraform/transcripts/`. CODE ONLY: no policy line, no other
    resource. Now (the End of Day window 20:00Z-21:45Z has closed), and NOT while an End of Day event is in flight (step 3).
  </objective>

  <context>
    BOTH HALVES SIGNED; read both in full before acting:
    - COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_INBOUND_R7_TEAMS_AGENT_CODE_DEPLOY_COO_R_20261008.md` @0a67682d62;
    - CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_COMM_LDO001_CODE_DEPLOY_R7_20261008.md` @54a8846698 (msg 107409).
    The previous deploy of this module is your own TO-APPLY-19 (live 21:48Z 2026-10-08, built at 6f7449dbc5, live CodeSha256
    M67/KipojF79vIGJTxCmQnDQfVyzws1VGU4OsD+7Yt0=, report `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/teams_r6_20261008/REPORT.md`,
    ledger 20261008T2134Z_teams-r6-code-laptop-20261008). Repeat its method step for step: both packages built so the root loads,
    `TF_DATA_DIR` a NEW scratch directory outside every git tree, never `init -reconfigure`, `.tools/safe-apply.sh` with the one
    `-target=module.ldo_001`. The packaged-path diff `6f7449dbc5..75420934c2` is 3 files (`teams_chat/tenant.py`,
    `mail_requests.py`, `assist.py`); nothing under the root changed.
  </context>

  <steps>
    0. Read both halves. Open the NEVER-2 entry naming both function families (`teams-global-chat-assist-handler-lambda`,
       `teams-global-chat-assist-ingress-lambda`).
    1. STOP 1: `git diff --name-only 75420934c2 HEAD` over the packaged paths and the root: a change under `teams_chat/`,
       `ldo.py`, `handlers.py` or `daily_reports/eod/` is branch B; any other change is named file by file.
    2. BEFORE, saved with SHA-256: both `CodeSha256`/`LastModified`; the live zip (`lambda get-function`, hash equal to the live
       `CodeSha256`); the live `cursor.json` as bytes (not printed).
    3. STOP 3: outside 20:00Z-21:45Z; the queue's `ApproximateNumberOfMessagesNotVisible` and the handler log show no End of Day
       event in flight (as in TO-APPLY-19, with a non-zero positive control on the same filter).
    4. Build; record the package SHA-256 and file count; targeted plan with the lock: branch A `0 to add, 2 to change, 0 to
       destroy`, the two functions' `source_code_hash` (and `last_modified`) only; anything else is branch B.
    5. Apply, same target, same `TF_DATA_DIR`; the hour it went live from CloudTrail.
    6. AFTER: both live `CodeSha256` equal the built package's; a targeted re-plan reads no changes; for 5 minutes, `ingress_poll`
       lines continue and no `ingress_step_failed` with `"step": "chats"` (`channel_poll` with `failed=1` is EXPECTED until the
       gateway's release).
    7. Close the ledger entry.
  </steps>

  <rules>
    Invoke neither function; send no test event, text or bus line; read no chat, mail or message content. No untargeted apply.
    Write only your deliverables folder, the ledger entry and its sentinel, and this order's report section.
  </rules>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this act changes no schedule (code hash only).
comp-iam: DECLARED-NOT-APPLICABLE -- denominator: 0 policy lines change (branch A requires `aws_iam_policy.exec` unchanged). BLIND: live inline policies on the role, not listed.
comp-adversary: RUN -- an untargeted apply (one target; branch B); a deploy over an in-flight End of Day event (STOP 3); a rollback that cannot be rebuilt (live zip downloaded and hashed first); a legacy pending draft texted twice (the half names the one case, a retry of a redraft that texted before the deploy; the issuer reads it in the first hour); a test text by the applier (forbidden).
lane: CloudOps applies under both signed halves (COO @0a67682d62, CTO @54a8846698).
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-i-13"><invocation>python data/transcripts/scripts/tests/test_inbound_silent_paths.py</invocation><expect>SILENT-PATHS ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-i-13" judgment="true"/>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~R when the entry closes, or at a STOP (name the step): the packaged-path diff since 75420934c2;
    AC1's line at the build commit; the package's SHA-256 and file count; the saved references' paths and hashes; the End of
    Day read; the targeted plan as read; the live read-back; the targeted re-plan; the first five minutes of ingress lines by
    event (counts only); THE HOUR THE DEPLOY WENT LIVE; the ledger entry's path and close; commit hashes and the measured push
    state. AC2 is the issuer's and the CVO's to grade: do not mark it. Leave the status flip to the issuer.
  </report>
</task_order>
