<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-mp23.mail-pull-onto-the-root-zip-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-11</date>
    <status>staged</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>23</round>
<workstream>mailpull</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R23.md</decomp_doc>
<owned_cells>TR-mp-23</owned_cells>
<decomp_context>Round 23 cell TR-mp-23 (CTO round-23 analysis @b8a07a7e17, item 1): the mail pull re-applied, code only, onto the Teams pull's live package. It disarms row NFRA_TRNSPT-D2-S22 (three functions of the root on one digest). STAGED: do NOT begin. The GO is a separate message, sent when the pair is complete; it names the packet, the CTO half and its conditions, which bind over the steps below.</decomp_context>
</decomp_ref>

  <objective>
    Re-apply `outlook-global-transcripts-pull-lambda` (Terraform resource `aws_lambda_function.mail_pull`), code only, onto the package
    the Teams pull runs today, so all three functions of the transcripts root read one CodeSha256. The package is FETCHED (the zip whose
    hash equals the Teams pull's live digest), not rebuilt. Then ONE driven invoke of the mail pull. Statuses, hashes and counts only.
  </objective>

  <context>
    Why: row D2-S22 (ARMED). One dist zip path feeds three functions; the mail pull has run a different, older digest (`VGIq85Xx...`)
    since 2026-10-07, so an untargeted apply from any tree would move it unannounced. The CTO ruled it is re-applied now, deliberately,
    under its own pair, in the shape of the commentary function's re-apply (`2287c83ba4`).
    The pair, COMPLETE: the issuer's packet `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_MP23_MAIL_PULL_PACKET_20261011.md`
    @b73b89ddbd (COO half in its section 8) and the CTO half
    `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_TR_MP23_MAIL_PULL_ONE_ZIP_CTO_HALF.md` @f4ec64d888. Read both first.
    Step 5's grade is the packet's section 4. Sequence: finish NFRA_TRNSPT.TO-APPLY-tv23 first if it is in hand (condition 3 covers either case).
  </context>

  <cto_conditions_verbatim>
    (CTO half SIGNED @f4ec64d888, section 3; AMENDMENT 1 of this order, issuer, 2026-10-11 ~07:1xZ. They bind over the outline below.)
    1. **The bytes are the Teams pull's package, not a rebuild.** Before the plan the file at the root's zip path hashes to
       `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`, and the Teams pull's live CodeSha256, re-read then, equals it. The tree is
       ahead of that zip (TR-tt-23 @5374271f5c): a `build.sh` anywhere in this act is a STOP.
    2. **The plan is 0 to add, 1 to change, 0 to destroy;** the one resource is `aws_lambda_function.mail_pull` and its changed
       argument is `source_code_hash` with what follows from it. `memory_size`, `timeout`, the handler, the environment and the
       layer are unchanged in the plan. No reader resource appears. Anything else: stop.
    3. **The reader-trust variable** comes from the committed `readers.auto.tfvars` if TR-tv-23 has landed it, else it is read
       from applied state into a file outside the repo. Never typed.
    4. **After the apply:** the three functions read one CodeSha256; the Teams pull's and the commentary function's LastModified
       are unchanged; the mail pull's MemorySize reads 1024 and Timeout 600.
    5. **The driven invoke is graded against the packet's section 4:** no `errorMessage`; one `MAIL-PULL-FIRE` line with
       `window_days=7` and `list_refusals=0`. A message admitted and landed is covered and is reported with its counts before the
       ledger closes. A `list_refusals` above 0 or any `[ERROR]` is Branch B: the kept `VGIq85Xx` zip is re-applied on the same
       target, and then the root zip is put back at its path and re-hashed.
    6. **Not covered:** a rebuild, an untargeted apply, either other function, any setting, any S3 delete.
  </cto_conditions_verbatim>

  <the_act>
    (Outline only. The GO message's conditions are the binding text.)
    0. NEVER-2 ledger read; open a change ledger naming the one function that moves and the two that must not.
    1. PRECONDITION reads: the three functions' CodeSha256 and LastModified; the local dist zip's base64 sha256. The local zip must
       EQUAL the Teams pull's live digest. No `build.sh`.
    2. KEEP the mail pull's current package for rollback: fetch the deployed zip (`get-function` code location), store it outside the
       repo, and record its base64 sha256; it must read the live `VGIq85Xx...` digest.
    3. PLAN then APPLY: `safe-apply` in `infra/aws/terraform/transcripts`, `-target=aws_lambda_function.mail_pull`. The plan changes
       exactly ONE resource and on it only the code hash (and its timestamp). Anything else = STOP.
    4. AFTER reads: the mail pull's CodeSha256 equals the Teams pull's; the Teams pull and the commentary function are unmoved, with
       their LastModified unchanged; the mail pull's MemorySize, Timeout, handler and environment are unchanged.
    5. PROOF, driven: ONE invoke of the mail pull, graded against its last SCHEDULED run as the packet states.
    6. Close the ledger. On a failed step 4 or 5: roll back in session to the kept zip and say so.
  </the_act>

  <bounds>
    - `aws_lambda_function.mail_pull` only, code only. No rebuild, no setting, no IAM, no schedule, no other function.
    - Never `aws lambda update-function-code`; never a bare `terraform apply`.
    - No mail content, no transcript text, no bearer, no address in any file or message.
    - No S3 delete. No second invoke without the issuer's word.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- the act changes the code behind the mail pull's daily rule `cron(30 23 * * ? *)` (mail_pull.tf:123); the rule is not touched. Its next fire after the act runs the new bytes; the driven invoke is the deliberate arm.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; the mail pull's role and policy are outside the target.
comp-adversary: RUN -- the changed files reaching the mail handler's import closure (the packet's closure read against the 12 changed members); a rebuild riding the apply (step 1 binds the local zip to the Teams pull's live digest); the mail pull writing to different keys under the newer naming files (the packet's key-producer equality); no way back (step 2 keeps the deployed zip and proves its hash). BLIND: what the mail pull's next scheduled run lists -- the driven invoke measures it.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="TR23-mp23-AC1" cell_refs="TR-mp-23"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/r23_checks.py mp23</invocation><expect>R23-MP23-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states the precondition reads, the kept zip's hash, the plan line, the after reads, the invoke's result and the ledger path.
  Dry-run before the act: `R23-MP23-FAIL 2 distinct digests across 3 functions` -- FAIL as expected.

<expected_criteria>TR23-mp23-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2 after the GO and the act. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
