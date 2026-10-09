<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-31.teams-agent-r8-draft-contract-code-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~CTL</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.inbound8.md</decomp_doc> (workstream INBOUND, round 8, macro COMM): the apply leg of cell `CT-i-14` (built, merged @bde0c0fc90)
<owned_cells>CT-i-14</owned_cells>
</decomp_ref>

  <closure>
    COMPLETE (issuer, ~23:2xZ): APPLIED, not yet EXERCISED.
    - Live 23:03Z: both functions at CodeSha256 SFSTGBQX3r49t2YXSrN+6t6Ekmz1NrpxkjX09VHLZEM=. The issuer read both live; the handler's
      LastModified is 23:03:08Z.
    - Branch A 0/2/0. Re-plan clean. ingress_poll 5, ingress_step_failed 0.
    - Ledger 20261009T2245Z_teams-r8-draft-contract-laptop-20261009 CLOSED 23:09:22Z. Proof instance VALID (issuer re-ran the
      check). Report @3af6f043b3.
    DEVIATIONS, graded ACCEPTED:
    (1) The one foreign -var (second_reader_trust_principal_arns), passed at its live value read at the act. This is the A3 method
        on the same root; it widened nothing, and branch A was met exactly.
    (2) STOP 3 widened from 60 to 180 minutes, to avoid reading an uninformative zero as clean. That is stricter, not looser.
    EXERCISE: the issuer's first-hour draft_contract read runs at ~00:05Z. The first real drafting call is the live exercise.
  </closure>

  <precondition>
    STAGED until BOTH halves are signed:
    - COO half: `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_INBOUND_R8_TEAMS_AGENT_DRAFT_CONTRACT_DEPLOY_COO_C_20261009.md`, SIGNED;
    - CTO half: owed by `1.0.0_SA_CTO`.
    The issuer names the CTO half's commit here and flips this order to pending. Do NOT act while it reads staged.
    MET (issuer, ~22:4xZ): CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_INBOUND_R8_TEAMS_AGENT_DRAFT_CONTRACT_DEPLOY_CTO_20261009.md`
    SIGNED @c2fa3eb0b4 (msg 108144), branches A and B adopted unchanged. Pending.
  </precondition>

  <objective>
    Deploy the Teams agent's round-8 function package: the drafting contract, so that only `post` can reach Teams. The act is ONE
    targeted apply of ONE module, `module.ldo_001`, in the root `infra/aws/terraform/transcripts/`.
    - CODE ONLY: no policy line, no environment change, no other resource.
    - Not inside the End of Day window 20:00Z-21:45Z, and not while an End of Day event is in flight (step 3).
  </objective>

  <context>
    Read both halves in full before acting.

    The live state is the COMM_ASSIST CA-d-2 deploy by `0.7.0_AE_CloudOps~CA`:
    - pinned build `2ad98c2e3a`, applied 18:33Z 2026-10-09;
    - ledger entry `org/critical_paths/change_management/20261009T1801Z_comm-assist-r12-mail-deploy-2_deploy_completion.md`, CLOSED;
    - both functions at `CodeSha256` `op92gM7rlR9956tienAEp2Dscy2zhdARV3WEbYDFp/M=`, `MAIL_BEARER_SECRET` set, policy `v4`.

    The packaged-path diff `2ad98c2e3a..bde0c0fc90` is 3 files: `teams_chat/assist.py`, `teams_chat/tenant.py` and
    `daily_reports/eod/post_format.py`. No `.tf` file changed.

    Method: repeat your own predecessors' method step for step, `0.7.0_AE_CloudOps`'s TO-APPLY-19 and TO-APPLY-20 (report
    `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/teams_r7_20261008/REPORT.md`):
    - build both packages so the root loads;
    - `TF_DATA_DIR` is a NEW scratch directory outside every git tree;
    - never `init -reconfigure`;
    - `.tools/safe-apply.sh` with the one `-target=module.ldo_001`.
  </context>

  <steps>
    0. Read both halves. Open the NEVER-2 entry, naming both function families: `teams-global-chat-assist-handler-lambda` and
       `teams-global-chat-assist-ingress-lambda`.
    1. STOP 1: run `git diff --name-only bde0c0fc90 HEAD` over the packaged paths and the root. A change under `teams_chat/`,
       `ldo.py`, `handlers.py` or `daily_reports/eod/` is branch B. Name any other change file by file.
    2. BEFORE, each saved with its SHA-256:
       - both functions' `CodeSha256` and `LastModified`. Either `CodeSha256` not equal to `op92gM7r...` is branch B;
       - `MAIL_BEARER_SECRET` present, by name only;
       - the live zip (`lambda get-function`; its hash equals the live `CodeSha256`);
       - the live `cursor.json`, as bytes, not printed.
    3. STOP 3: be outside 20:00Z-21:45Z. The queue's `ApproximateNumberOfMessagesNotVisible` and the handler log must show no End
       of Day event in flight, with a non-zero positive control on the same filter.
    4. Build. Record the package SHA-256 and its file count. Run the targeted plan with the lock.
       - Branch A: `0 to add, 2 to change, 0 to destroy`, the two functions' `source_code_hash` (and `last_modified`) only, and no
         environment change.
       - Anything else is branch B.
    5. Apply, with the same target and the same `TF_DATA_DIR`. Read from CloudTrail the hour it went live. SEND THE ISSUER THAT HOUR
       AT ONCE, before any proof work: the issuer reads the first hour of `draft_contract` lines from it.
    6. AFTER:
       - both live `CodeSha256` equal the built package's;
       - a targeted re-plan reads no changes;
       - for 5 minutes, `ingress_poll` lines continue, with no `ingress_step_failed`. `channel_poll failed=1` is pre-existing.
    7. Close the ledger entry.
  </steps>

  <rules>
    - Invoke neither function. Send no test event, text or bus line. Read no chat, mail or message content, and no secret value.
    - No untargeted apply.
    - Write only your deliverables folder, the ledger entry and its sentinel, and this order's report section.
  </rules>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this act changes no schedule (code hash only).
comp-iam: DECLARED-NOT-APPLICABLE -- denominator: 0 policy lines change (branch A requires the policy at v4, unchanged). BLIND: live inline policies on the role, not listed.
comp-adversary: RUN -- 5 attacks on the one act: an untargeted apply (one target; branch B); a deploy over an in-flight End of Day event (STOP 3); a deploy over a newer COMM_ASSIST build (BEFORE CodeSha256 must equal op92gM7r..., else branch B); a rollback that cannot be rebuilt (the live zip is downloaded and hashed first); a test text by the applier (forbidden). BLIND: whether the live model answers in the contract; the issuer reads the draft_contract lines in the first hour (the half's named risk) and rolls back the same hour if refusals dominate.
lane: CloudOps~CTL applies under both signed halves (COO @082e0d865a, CTO @c2fa3eb0b4).
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-i-14"><invocation>python data/transcripts/scripts/tests/test_draft_contract.py</invocation><expect>DRAFT-CONTRACT ok=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-i-14" judgment="true"/>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~CTL/deliverables/teams_r8_20261009/NFRA_CTLPLN.TO-APPLY-31.teams-agent-r8-draft-contract-code-deploy-laptop.proof_of_spec.json`.
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step). Send the live hour separately, at once, in
    step 5. The report carries:
    - the packaged-path diff since `bde0c0fc90`;
    - AC1's line at the build commit;
    - the package's SHA-256 and file count;
    - the saved references' paths and hashes;
    - the End of Day read;
    - the targeted plan as read;
    - the live read-back and the targeted re-plan;
    - the first five minutes of ingress lines by event (counts only);
    - the ledger entry's path and close;
    - commit hashes and the measured push state.
    AC2 is the issuer's and the CVO's to grade: do not mark it. Leave the status flip to the issuer.
  </report>
</task_order>
