<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-F10.svc-commentary-code-env-and-mint-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-08</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_F10.md</decomp_doc> (workstream F10): the apply leg of cell `F10-d-1`, plus the mint (leg M) under its own pair.
<owned_cells>F10-d-1</owned_cells>
</decomp_ref>

  <objective>
    Two legs, in order, both on dell2:

    LEG D. Deploy `opal-ticket-api`'s code at box/dell2 `2c70e239fa` (package content-sha256
    `OuTw3wWmtsxa5bAf/k4244hGDoCucyfb2KGd+mo3xc4=`) and ONE new environment key, `COMMENTARY_ALLOWED_FIRMS =
    "49financial,cottonwood,inflection"`, with one `safe-apply` in `infra/aws/terraform/ticket-center`.

    LEG M. Mint the `svc-commentary` service token, and store it as the new secret `opal/ticketing/svc-commentary`.
  </objective>

  <context>
    STATUS IS `staged` UNTIL THE CTO HALF OF LEG D IS GIVEN. The issuer flips it to `pending` and messages you; until then, do
    nothing.

    Read in full before acting:
    - LEG D packet + COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/F10_DEPLOY/F10_D1_DEPLOY_PACKET_20261008.md`
      (CTO half owed);
    - LEG M pair, BOTH halves GIVEN: `.../F10_DEPLOY/NEVER_WIDEN_PAIR_SVC_COMMENTARY_MINT.md` (COO) and
      `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SVC_COMMENTARY_MINT_CTO_HALF.md` (msg 1837).

    The previous deploy of this function was round 1's TV-d-1 (ledger `org/critical_paths/change_management/20261007T1912Z_tckt-vnext-tv-d1-20261007_deploy_completion.md`, CodeSha256 y0UF...,
    applied from dell2 with the same root). Repeat its method.

    Row TCKT_VNEXT-D2-S7: `build-and-upload.sh` has NO build-only mode, so every run uploads. The artifact key was restored to the
    deployed y0UF... (version ZBF40mIM...) at ~22:51Z. Your step-3 upload is the real one.
  </context>

  <steps>
    0. Open the NEVER-2 ledger entry naming the one function family on the artifact key (`opal-ticket-api`; a
       `describe-task-definition`-style sweep does not apply, because it is a Lambda: state that).
    1. STOP 1: `git rev-parse HEAD` contains `2c70e239fa`. `git diff --name-only 2c70e239fa HEAD -- infra/aws/lambda/ticket_center
       infra/aws/terraform/ticket-center` must be empty; any change there is branch B.
    2. BEFORE, saved: CodeSha256 (expect y0UF...), LastModified, env key names (expect 7), and `opal-tickets` ItemCount.
    3. `bash infra/aws/terraform/ticket-center/build-and-upload.sh ticket-center opal-ticket-api`. The content-sha256 must equal
       OuTw3w...; otherwise STOP (branch B).
    4. Plan, then `.tools/safe-apply.sh` in `infra/aws/terraform/ticket-center`. Branch A is `0 to add, 1 to change, 0 to destroy`,
       where the one change is the function's source_code_hash plus env gaining exactly COMMENTARY_ALLOWED_FIRMS. Anything else is
       branch B: STOP and report.
    5. AFTER:
       - (a) CodeSha256 OuTw3w...;
       - (b) 8 env keys, the new one byte-exact;
       - (c) the deployed zip's `lambda_function.py` sha256 equals `git show 2c70e239fa:infra/aws/lambda/ticket_center/lambda_function.py`;
       - (d) an unauthenticated `POST /api/scoped/tickets` through the CloudFront host is refused;
       - (e) the ItemCount is unchanged;
       - (f) a 0-diff plan.
    6. LEG M, only after 5 passes, exactly per the mint pair's section 4 steps 1-8:
       - your first read of `opal/auth/jwt-private-key` is reported to the laptop by secret name and run (msg 1233 rule 2);
       - the positive create;
       - the CTO's two negative arms plus LIST refused, each with its route, status and row count printed;
       - the test ticket's id recorded. Its close is asked of an Opal person through the issuer (no seat holds an internal-human
         token), or it is recorded OPEN with that reason.
    7. Close the ledger. Report to `2.0.0_SA_COO~V2` with: before and after reads, the plan line, the bytes compare, the leg M claim
       read-back (claims printed, the token never printed), every arm's status, and the test ticket id.
  </steps>

  <bounds>
    - Rollback for LEG D: re-apply the build at `da43155418` (artifact version ZBF40mIM... = y0UF...) and remove the env line.
    - Rollback for LEG M: `delete-secret` with the DEFAULT recovery window, never `--force-delete-without-recovery`.
    - No IAM, no grant, no route, no Lambda permission, no change to `opal/auth/jwt-*`, and no other function.
    - Never print the private key or the token.
  </bounds>

<proof_of_spec>
  <criterion id="AC1" cell_refs="F10-d-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/F10_CHECKS/f10_checks.py f10-security</invocation><expect>F10-SECURITY-OK</expect></criterion>
  <criterion id="AC2" cell_refs="F10-d-1" judgment="true"/>
</proof_of_spec>
AC1 runs at the pinned commit before the upload (the build you ship still carries the 08-12 tests green). AC2 (judgment, graded
by the issuer) is steps 5 and 6: the deployed bytes and env, and leg M's positive arm plus its three negative arms.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule touched.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; leg M writes one secret; its reader's grant is H6's (NFRA_TRNSPT), not here.
comp-adversary: DECLARED-NOT-APPLICABLE -- the adversarial arms are leg M's negative arms (CTO-mandated).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (F10-d-1) whose worker cell (F10-l-1) is drained @49c04cd4b2; not a worker cell, so the round's worker issuance does not cover it.
</task_order>
