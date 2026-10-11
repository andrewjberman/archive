<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-ra22.teams-pull-refused-read-fix-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>22</round>
<workstream>pullapply</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R22.md</decomp_doc>
<owned_cells>TR-ra-22</owned_cells>
<decomp_context>Round 22 AMENDMENT 2, cell TR-ra-22: the deploy of TR-rf-22's merged fix. The scheduled Teams pull has failed on every fire since 2026-10-09T16:00Z (row NFRA_TRNSPT-D2-S16). The pair is COMPLETE; this order IS the GO.</decomp_context>
</decomp_ref>

  <reassignment>
    AMENDMENT 1 (issuer, 2026-10-11 ~03:2xZ): re-addressed from 0.7.0_AE_CloudOps~DELL2 to 0.7.0_AE_CloudOps~TR2, the fresh NFRA_TRNSPT applier
    lane 0.0.0_AB_MSTR~DELL2 spawned (msg 3943): ~DELL2 holds open orders on two other projects (the seating check, to-decomp-ref-lint, ANNOUNCE).
    Nothing else in the order changed. 0.7.0_AE_CloudOps~DELL2 does NOT run this order.

    AMENDMENT 2 (issuer, 2026-10-11 ~03:3xZ): RE-PINNED after the HALT of 03:08Z. The first pin (fd74f984ac) did not handle a LISTING error;
    TR-rl-22 fixed it (drained @5ae3b3ddd9). The pin is now `data/transcripts/scripts/teams/pull.py` at blob `8aef45f2fc` (build commit
    2e86e331ad). The first CTO half is VOID; the FRESH HALF @ee82091502 is the only one that covers the act, and its six conditions are
    below verbatim. Step 5's expectation is the packet's A4 dry run. The HALT is lifted by the GO message that names this amendment.
  </reassignment>

  <objective>
    Deploy the Teams pull fix: rebuild the transcripts-pull zip, safe-apply it TARGETED at `aws_lambda_function.pull` ONLY, then ONE invoke
    of `teams-global-transcripts-pull-lambda`. Report statuses, hashes and counts only. The next scheduled fire is Monday 2026-10-12 13:00Z.
  </objective>

  <context>
    The pair binds; read both halves first.
    COO half and packet: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_TR_RA22_DEPLOY_PACKET_20261011.md` @eb2d9e5451, ADDENDUM 1 (A1 to A7; its section 3 is withdrawn where it differs).
    CTO half, SIGNED: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TR_RA22_TEAMS_PULL_FIX_CTO_HALF.md` @ee82091502, the section headed FRESH HALF only.
    The fix: `data/transcripts/scripts/teams/pull.py` at blob `8aef45f2fc` (box/dell2 `5ae3b3ddd9`; build commits 12c64f3c1f and 2e86e331ad).
    ONE zip feeds THREE functions in this Terraform root; only the Teams pull may move.
  </context>

  <cto_conditions_verbatim>
    (FRESH HALF, section F2, @ee82091502 -- these replace the six conditions of the VOID half)
    1. **Precondition:** the pull function's live CodeSha256 reads `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=` at step 0.
       Any other value: stop and report.
    2. **The plan changes exactly one resource,** `aws_lambda_function.pull`. Anything else in the plan: stop.
    3. **After the apply:** the mail pull still reads `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`; the commentary function is
       still absent.
    4. **The driven invoke is graded against A4, both ways.** Expected: no `errorMessage`, 4 series entries, `monday_meeting`
       `read_refused` 4, `research_meeting` `refused` 1, a run record and a listing snapshot that exist. One `ocio_ic` landing
       is covered. A landing count ABOVE what A4 measured is not a failure, but it is reported with its series and count
       before the ledger closes.
    5. **Not covered:** an untargeted apply, the mail pull, the commentary function, any S3 delete, any recovery landing of
       the four aged-out Monday meetings (2026-04-10, 04-13, 05-04, 06-01).
    6. **Rollback:** rebuild with `pull.py` at `0096e67747`, same target, proof CodeSha256 back at `taFbGTCU...6HA=`. Finished
       or rolled back in session; the ledger opens at start.
  </cto_conditions_verbatim>

  <the_act>
    0. Before anything: read the open deploy ledgers per CLAUDE.md NEVER-2 (every live worktree, `ls-tree`). The entry
       `irpt-anlreq-t1-commentary-store-and-lambda-20261009` is another seat's (2.0.0_SA_COO~Y2) and is NOT touched by this order.
       Open a change ledger in `org/critical_paths/change_management/` naming: this order, the pin (pull.py blob `8aef45f2fc`; the box/dell2 HEAD
       you build from, with the statement that none of the packet's 12 files differs from 5ae3b3ddd9), and all three functions that read
       the zip with which one moves.
    1. PRECONDITION (condition 1, no write): print the LIVE CodeSha256 of `teams-global-transcripts-pull-lambda`. It must read
       `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=`. Print the mail pull's (`outlook-global-transcripts-pull-lambda`, expected
       `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`) and confirm `outlook-global-commentary-draft-lambda` reads ResourceNotFound.
       Any other value = STOP and report.
    2. BUILD: `bash infra/aws/lambda/transcripts-pull/build.sh` from a tree whose `data/transcripts/scripts/teams/pull.py` is blob
       `8aef45f2fc` (print `git rev-parse HEAD:data/transcripts/scripts/teams/pull.py`). Print the new zip's base64 sha256 and record it in the ledger.
    3. PLAN then APPLY (condition 2): `safe-apply` in `infra/aws/terraform/transcripts` with `-target=aws_lambda_function.pull`.
       The plan shows exactly ONE resource changing, `aws_lambda_function.pull` (an in-place update of its code hash). Anything else = STOP,
       nothing applied.
    4. AFTER (condition 3): re-print the three reads of step 1. The pull's CodeSha256 equals step 2's zip hash; the mail pull's is
       unchanged; the commentary function is still absent.
    5. PROOF, driven: ONE invoke of `teams-global-transcripts-pull-lambda` (empty event). Report from its returned record, counts and
       statuses only: no `errorMessage`; the number of series entries (expected 4); per series `listed`, `landed`, `held`, `expired`,
       `read_refused`, `refused`; `state_key`, and that the run record AND the listing snapshot objects exist. Graded against the
       packet's A4 (condition 4): `monday_meeting` 20 listed, 16 held, 4 `read_refused`; `ocio_ic` 8 listed, 7 held, 1 LANDED;
       `asset_management_ic` 7 listed, 7 held; `research_meeting` `refused` 1. A landing count ABOVE A4's is not a failure: report
       its series and count BEFORE the ledger closes.
    6. Close the ledger on step 5's result. If step 4 or 5 fails: ROLL BACK in session per condition 6 and say so.
  </the_act>

  <bounds>
    - `aws_lambda_function.pull` only. No other resource, root, key policy or function. Never `aws lambda update-function-code`; never a
      bare `terraform apply`.
    - No transcript text, no bearer, no meeting id in any file or message: hashes, dates, statuses and counts only.
    - No S3 delete. No second invoke without the issuer's word.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- the act changes the code behind `teams-global-transcripts-pull-hourly` cron(0 13-22 ? * MON-FRI *) (pull.tf:126-127); the rule itself is not touched. Next fire 2026-10-12T13:00Z.
comp-iam: DECLARED-NOT-APPLICABLE -- no new AWS call in the changed code; the pull role, its policy and its KMS grant are unchanged and outside the target.
comp-adversary: RUN -- the shared zip moving the mail pull or creating the commentary function (a one-resource targeted plan, three sha reads before and after); a zip built from a tree carrying other seats' uncommitted edits (the build tree's 12 files are stated against 5ae3b3ddd9); another act having moved the function (the precondition sha); a refused read mistaken for success (the invoke's per-series counts). BLIND: whether ocio_ic and asset_management_ic hold unlanded readable rows -- the invoke measures it.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="TR22-ra22-AC1" cell_refs="TR-ra-22"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R22_CHECKS/r22_checks.py ra22</invocation><expect>R22-RA22-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states step 1's three reads, the plan line, step 4's three reads, the invoke's per-series counts and the ledger path.
  Dry-run before the act: `R22-RA22-FAIL the pull still runs the pre-fix zip` -- FAIL as expected.

<expected_criteria>TR22-ra22-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the precondition reads; the plan line; the after reads; the invoke's status and per-series counts;
    the check line; the ledger path and its closed state; commit hashes and the measured push state. Write the proof instance; leave the
    status flip to the issuer.
  </report>
</task_order>
