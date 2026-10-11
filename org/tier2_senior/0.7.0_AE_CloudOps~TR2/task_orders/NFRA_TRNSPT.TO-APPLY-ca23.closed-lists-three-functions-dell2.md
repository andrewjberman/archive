<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-ca23.closed-lists-three-functions-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>23</round>
<workstream>closedlistsapply</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R23.md</decomp_doc>
<owned_cells>TR-ca-23</owned_cells>
<decomp_context>Round 23 AMENDMENT 1, cell TR-ca-23: the deploy of TR-cl-23 (the commentary drafter's closed lists, merged @615010e8bf) to the transcripts root's THREE functions together, so the root stays on one digest. The pair is COMPLETE; this order IS the GO.</decomp_context>
</decomp_ref>

  <objective>
    Rebuild the transcripts zip and re-apply it, code only, to all three functions of the root in ONE targeted apply:
    `aws_lambda_function.pull`, `aws_lambda_function.mail_pull`, `aws_lambda_function.commentary`. Then ONE invoke of the Teams pull and
    ONE of the mail pull. NO invoke of the commentary function. Statuses, hashes and counts only.
  </objective>

  <context>
    The pair binds; read both halves first.
    COO half and packet: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_CA23_CLOSED_LISTS_DEPLOY_PACKET_20261011.md` @cc647d5ca2.
    CTO half, SIGNED: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_TR_CA23_CLOSED_LISTS_DEPLOY_20261011.md` @e117673ae2.
    The pin: box/dell2 `615010e8bf`, or a descendant that changes NONE of the 10 members of the packet's section 1.
    KNOWN at step 1 (row NFRA_TRNSPT-D2-S31): the on-disk `dist/transcripts-pull.zip` hashes `8jmhmuWw...`, rebuilt at 14:54Z by an
    unnamed hand. It does NOT equal the live digest and is NOT the rollback artifact. Record its hash, then rebuild.
    The reader-trust variable now comes from the committed `readers.auto.tfvars` (your TO-APPLY-tv23); pass no `-var`.
  </context>

  <cto_conditions_verbatim>
    (CTO half SIGNED @e117673ae2, section "Conditions")
    1. **The plan is exactly three functions' code.** Any diff on memory, timeout, handler, environment, layers, the event
       source mapping, a schedule or IAM is a STOP with nothing applied.
    2. **Before the plan the applier re-runs the address equality on the zip it BUILT,** not on the scratch build the packet
       measured: 14 of 14 and 7 of 7, negative control failing. The zip moves with every other project's naming commit, and
       the build may be at a descendant of the pin. A descendant that changes any of the 10 members of section 1 is a STOP.
    3. **The two driven invokes are the pulls' ordinary runs and may land data.** A landing is reported with its series and
       count before the ledger closes, as the packet says. If the act would straddle the mail pull's 23:30Z fire, it starts
       after that fire has finished or completes before 23:15Z.
    4. The rollback artifact is the FETCHED deployed zip, held outside the repo, its hash printed before the plan.
    5. The applier is seated by `0.0.0_AB_MSTR~DELL2`; this half instructs no applier.

    Not covered: any binding of an upstream sender to the commentary queue; any invoke of the commentary function; any change of
    the event source mapping.
  </cto_conditions_verbatim>

  <the_act>
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open a change ledger naming this order, the HEAD you build from, and the
       three functions that move. Check the clock against condition 3 (the 23:30Z mail fire): if you cannot finish by 23:15Z, wait
       until that fire's REPORT line is logged, and say which you did.
    1. PRECONDITION reads, no write: the three functions' CodeSha256 (expected `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=` on all
       three), LastModified, MemorySize, Timeout; the commentary function's event source mapping (1, Enabled) and its invocation
       count in the log since 2026-10-11T00:00Z (the issuer read 2). Print the on-disk dist zip's base64 sha256 (row D2-S31).
       Any function NOT on `AI4UQD0M...` = STOP and report.
    2. ROLLBACK ARTIFACT (condition 4): fetch the deployed package from `get-function` (any of the three), store it OUTSIDE the repo,
       print its base64 sha256: it must read `AI4UQD0M...`. Extract it to a directory outside the repo.
    3. BUILD: `bash infra/aws/lambda/transcripts-pull/build.sh`. Print the new zip's base64 sha256 and member count. State the HEAD
       built from, and that none of the packet's 10 section-1 members differs from `615010e8bf` (`git diff --stat 615010e8bf HEAD --`
       over the build inputs); a difference in any of the 10 = STOP (condition 2).
    4. ADDRESS EQUALITY on the BUILT zip (condition 2): extract the built zip outside the repo and run
       `python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/addr_equal.py <extracted deployed zip> <extracted built zip>`.
       It must print `ADDR-EQUAL-OK teams=14/14 mail=7/7 control=discriminates`. Anything else = STOP, nothing applied.
    5. PLAN then APPLY (condition 1): `safe-apply` in `infra/aws/terraform/transcripts` with exactly
       `-target=aws_lambda_function.pull -target=aws_lambda_function.mail_pull -target=aws_lambda_function.commentary`.
       The plan: 0 to add, 3 to change, 0 to destroy; on each function only `source_code_hash` and what follows from it. Any other
       resource or attribute = STOP, nothing applied.
    6. AFTER reads: all three CodeSha256 equal the built zip's hash; MemorySize 1024, 1024, 512 and Timeout 300, 600, 300 unchanged;
       the commentary function's event source mapping still 1, Enabled; its log shows NO new invocation across the act.
    7. PROOF, driven: ONE invoke of `teams-global-transcripts-pull-lambda` and ONE of `outlook-global-transcripts-pull-lambda`.
       Graded against the packet's section 4. Teams pull: no `errorMessage`, 4 series, `totals` carrying `read_refused` (expected 4),
       run record and listing snapshot exist. Mail pull: one `MAIL-PULL-FIRE` line, `window_days=7`, `list_refusals=0`. A landing by
       either is reported with its series and count BEFORE the ledger closes (condition 3).
       NO invoke of `outlook-global-commentary-draft-lambda`, with any event.
    8. Close the ledger. If step 6 or 7 fails: ROLL BACK in session -- put the fetched deployed zip at the root's zip path, re-apply
       the same three targets, prove all three read `AI4UQD0M...` -- and say so.
  </the_act>

  <bounds>
    - Exactly the three function resources, code only. No setting, IAM, schedule, event-source or reader resource.
    - Never `aws lambda update-function-code`; never a bare `terraform apply`.
    - No transcript text, mail content, prompt text, bearer or address in any file or message.
    - No S3 delete. No second invoke of either pull without the issuer's word. No invoke of the commentary function.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- the act changes the code behind `teams-global-transcripts-pull-hourly` cron(0 13-22 ? * MON-FRI *) and the mail pull's cron(30 23 * * ? *); neither rule is touched. Condition 3 keeps the act clear of tonight's 23:30Z fire.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; no role, policy or grant in the three targets.
comp-adversary: RUN -- other projects' naming commits riding the rebuild and moving a write address (step 4 on the BUILT zip, with a negative control); a descendant HEAD changing one of the 10 members (step 3's diff); the on-disk zip mistaken for the rollback artifact (step 2 fetches the deployed bytes and proves their hash); an invoke of the commentary function used as proof, which would call the outside model (forbidden; proof is the digest, the plan, a flat invocation count); the act straddling the mail pull's own fire (condition 3). BLIND: what a real draft's withheld counts read -- UNEXERCISED LIVE until the upstream chain sends one.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="TR23-ca23-AC1" cell_refs="TR-ca-23"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/r23_checks.py ca23</invocation><expect>R23-CA23-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states the precondition reads, the rollback artifact's hash, the built hash, the address-equality line, the plan
  line, the after reads, both invokes' results and the ledger path.
  Dry-run before the act: `R23-CA23-FAIL the functions still run the pre-act zip` -- FAIL as expected.

<expected_criteria>TR23-ca23-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the precondition reads; the rollback artifact's hash; the built hash and HEAD; the address-equality
    line; the plan line; the after reads; both invokes' status and counts; the check line; the ledger path and its closed state;
    commit hashes and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
