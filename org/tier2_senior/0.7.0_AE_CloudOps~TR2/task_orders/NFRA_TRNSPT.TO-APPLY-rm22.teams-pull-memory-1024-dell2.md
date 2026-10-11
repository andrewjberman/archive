<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-rm22.teams-pull-memory-1024-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>22</round>
<workstream>pullmem</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R22.md</decomp_doc>
<owned_cells>TR-rm-22</owned_cells>
<decomp_context>Round 22 AMENDMENT 4, cell TR-rm-22: the disarm of the ARMED row NFRA_TRNSPT-D2-S19 (CVO compile @0b5b432e5b). The Teams pull reports Max Memory Used 128 of 128 MB on every invocation that read transcript content. STAGED: wait for the GO message, which is sent when the CTO half lands and names its conditions.</decomp_context>
</decomp_ref>

  <objective>
    Raise the Teams pull's memory from 128 MB to 1024 MB: one setting, `safe-apply` TARGETED at `aws_lambda_function.pull` ONLY, NO rebuild
    of the zip, then ONE invoke. Report statuses, hashes, sizes and counts only. Must be done before the Monday 2026-10-12 13:00Z fire.
  </objective>

  <context>
    The pair binds; read both halves first.
    COO half and packet: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_TR_RM22_MEMORY_PACKET_20261011.md`.
    CTO half, SIGNED: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TR_RM22_TEAMS_PULL_MEMORY_CTO_HALF.md` @16fa3b73b8,
    against the packet @f6f35a8841. Its six conditions are below verbatim and bind over this order where they differ.
    The Terraform edit is YOURS (the file is in the AE lane; the issuer's commit of it was refused by owned-paths): in
    `infra/aws/terraform/transcripts/pull.tf`, resource `aws_lambda_function.pull`, add the three lines of the packet's section 0 between
    `timeout          = 300` and `filename         = local.pull_zip` -- byte for byte, nothing else in the file.
  </context>

  <cto_conditions_verbatim>
    (CTO half SIGNED @16fa3b73b8, section 3; AMENDMENT 1 of this order, issuer, 2026-10-11 ~04:5xZ. They bind over the steps below.)
    1. **The plan changes exactly one resource, and on it exactly one attribute, `memory_size`.** Any other resource or
       attribute in the plan: stop. In particular no reader resource and no `source_code_hash` change.
    2. **After the apply:** `MemorySize` 1024; the pull's CodeSha256 unchanged at `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`;
       the mail pull's sha unmoved; the commentary function still absent.
    3. **The reader-trust variable is READ from applied state** into a tfvars file outside the repo, never typed (row D2-S17).
    4. **The `pull.tf` edit is the packet's three lines, byte for byte,** committed by the applier under its own author line
       before the plan.
    5. **The driven invoke proves the setting is live, not the peak.** Its close states that in words. The first REPORT line
       of a run that lands a transcript is read beside its `run.json` and its `Max Memory Used` is recorded as the first
       measured peak. A peak above 768 MB is a row, not a second raise.
    6. **Not covered:** a rebuild, an untargeted apply, the mail pull, the commentary function, any S3 delete.
  </cto_conditions_verbatim>

  <the_act>
    0. Read the open deploy ledgers per CLAUDE.md NEVER-2. Open a change ledger naming this order, the box/dell2 HEAD you apply from, the
       ONE function that moves and the two that must not.
    0a. Make the three-line edit above; `bash .tools/commit-gate.sh` on the file; commit it with safe-commit under your own author line
       BEFORE the plan, and print `git diff HEAD~1 -- infra/aws/terraform/transcripts/pull.tf` (it must be exactly the packet's diff).
    1. PRECONDITION (no write): print, for `teams-global-transcripts-pull-lambda`, MemorySize (expected 128) and CodeSha256 (expected
       `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`); the mail pull's CodeSha256 (expected
       `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`); the commentary function ResourceNotFound. Print the base64 sha256 of the local
       `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip`: it must EQUAL the pull's live CodeSha256. Any other value = STOP and
       report. Do NOT run `build.sh`.
    2. PLAN then APPLY: `safe-apply` in `infra/aws/terraform/transcripts` with `-target=aws_lambda_function.pull`. The reader-trust
       variable is supplied as for TO-APPLY-ra22: READ from applied state, in a tfvars file outside the repo, never typed (row D2-S17).
       The plan shows exactly ONE resource changing, `aws_lambda_function.pull`, and its ONLY diff is `memory_size 128 -> 1024`. A
       `source_code_hash` diff, or any other resource, = STOP, nothing applied.
    3. AFTER: re-print step 1's reads. MemorySize 1024; the pull's CodeSha256 UNCHANGED; the mail pull unchanged; the commentary function
       still absent.
    4. PROOF, driven: ONE invoke (empty event). Report: no `errorMessage`; the number of series entries (expected 4); per series
       `listed`, `landed`, `held`, `read_refused`, `refused`; that the run record and the listing snapshot exist; and the REPORT line's
       `Memory Size` and `Max Memory Used` as numbers. A landing is not a failure: report its series and count before the ledger closes.
       Per condition 5, your close states in words that this invoke proves the SETTING is live, not the peak; if the invoke LANDS a
       transcript, its `Max Memory Used` is the first measured peak: report it, and a peak above 768 MB is a surprise row, not a second raise.
    5. Close the ledger on step 4's result. If step 3 or 4 fails: ROLL BACK in session (remove the `memory_size` line, re-apply the same
       target, proof MemorySize 128 with the CodeSha256 unchanged) and say so.
  </the_act>

  <bounds>
    - `aws_lambda_function.pull` only, the memory setting only. No rebuild, no other resource, root, key policy or function. Never
      `aws lambda update-function-configuration` or `update-function-code`; never a bare `terraform apply`.
    - No transcript text, no bearer, no meeting id in any file or message.
    - No S3 delete. No second invoke without the issuer's word.
  </bounds>

  <paths>
    infra/aws/terraform/transcripts/pull.tf
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- the act changes a setting of the function behind `teams-global-transcripts-pull-hourly` cron(0 13-22 ? * MON-FRI *); the rule is not touched. Next fire 2026-10-12T13:00Z.
comp-iam: DECLARED-NOT-APPLICABLE -- a memory setting; no role, policy or grant in the target.
comp-adversary: RUN -- a rebuild riding the apply (step 1 binds the local zip to the live sha and the plan must show no source_code_hash diff); the shared root moving the mail pull or creating the commentary function (one-resource targeted plan, sha reads before and after); a typed reader-trust value (row D2-S17: read from applied state); a clean invoke read as proof of the peak (it is not: a run that reads no content does not exercise the peak -- stated in the packet). BLIND: the true peak of a content-reading run, capped at 128 until now.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="TR22-rm22-AC1" cell_refs="TR-rm-22"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R22_CHECKS/r22_checks.py rm22</invocation><expect>R22-RM22-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states step 1's reads, the plan line, step 3's reads, the invoke's per-series counts with its REPORT memory figures, and
  the ledger path. Dry-run before the act: `R22-RM22-FAIL the pull's MemorySize is not 1024` -- FAIL as expected.

<expected_criteria>TR22-rm22-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the precondition reads; the plan line; the after reads; the invoke's status, per-series counts and
    memory figures; the check line; the ledger path and its closed state; commit hashes and the measured push state. Write the proof
    instance; leave the status flip to the issuer.
  </report>
</task_order>
