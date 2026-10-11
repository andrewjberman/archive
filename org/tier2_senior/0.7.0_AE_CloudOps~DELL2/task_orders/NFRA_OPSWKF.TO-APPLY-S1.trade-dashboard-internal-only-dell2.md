<task_order>
  <metadata>
    <id>NFRA_OPSWKF.TO-APPLY-S1.trade-dashboard-internal-only-dell2</id>
    <issued_by>2.0.0_SA_COO~O2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>NFRA_OPSWKF</project_code>
  </metadata>
<risk>WORLD</risk>
<round>1</round>
<workstream>S</workstream>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPSWKF/decompositions/NFRA_OPSWKF_DECOMP.md</decomp_doc> (workstream S): issuer cells `OW-s-d-1` and `OW-s-r-1`, serving drained cell OW-s-2 (merged @abf78fcb7f).
<owned_cells>OW-sd-1, OW-sr-1</owned_cells>
</decomp_ref>

  <objective>
    FWD-8 (PRD v0.6 @ca5f93a729): release the code of ONE function, `trade-dashboard-api`, by ONE `safe-apply` of
    `infra/aws/terraform/trade-pipeline` at box/dell2 pin `abf78fcb7f`, and prove it on the deployed service with a refused read and a
    served read by two synthetic callers. Build input (`infra/aws/lambda/ci/lambda-source-map.json`, three members), sha256 hex at the pin:
    - `dashboard_api.py`    b152580eaf2066ad60789c98503496dbbf464e485f1edd918c70bec76907d564
    - `config.py`           1421ac511f412259cc02f241d68d20491a04f8a66f60f0a8b330eb1cd666fdd5
    - `excel_generator.py`  eaee4072c300389e92a567624ce2bdb4b067c5f70a97e1d1de640b2e7c857734
    Nothing else: no env key, grant, route, table, layer or other function; no portal file.
  </objective>

  <context>
    Packet and COO half (SIGNED): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_S_D1_RELEASE_PAIR_20261011.md
    @b56dc254d1, sha256 begins 51dacf8f0f82ec84. READ IT WHOLE before step 0: sections 2-6 are this order's blast radius, callers,
    reads and rollback.

    CTO half (SIGNED, msg 5609): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_OW_S_D1_FWD8_RELEASE_20261011.md
    @96c9182bdc. It CHANGES the packet in three ways, and where they differ the CTO half governs:
    - **Caller IN-T is REFUSED and is NOT minted.** Only rows OUT and IN-F exist. Read R2 is not made; the tier arm on the deployed
      service is recorded UNEXERCISED, and your report must not say both served arms were read live.
    - The extra data-refresh read is made by **IN-F** (expect refused; an admit is a STOP and cleanup).
    - The ledger closes after the TWO ABSENT reads.

    The two callers (packet section 4): rows in `opal-users-v2`, `SK PROFILE`, conditional put `attribute_not_exists(PK)`:
    - OUT  `PK USER#opswkf-fwd8-out-20261011@opal.invalid`: `tier advisor`, `role user`, `firmId fwd8-synthetic-nofirm`, `userType test-filer`
    - IN-F `PK USER#opswkf-fwd8-inf-20261011@opal.invalid`: `tier advisor`, `role user`, `firmId opal-capital`, `userType test-filer`
    Each: `status active`, a `name` beginning `NFRA_OPSWKF FWD-8 synthetic`, `allowedFirmIds ["fwd8-synthetic-nofirm"]` as a LIST.
    Each token: RS256 with the CURRENT slot of the portal signing key, `iss opal-portal-auth`, `aud opal-portal-api`, the row's claims,
    `exp = iat + the run's length + 5 minutes`; state the run's length before minting. Mint the way TCKT_VNEXT's runs did
    (org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md, v2.2 with AMENDMENTS 1-2).
    Token values are held in memory only: never stored, printed, committed or sent.

    The artifact is a versioned S3 object Terraform pins (`lambdas.tf:107-119`): `trade-pipeline/trade-dashboard-api.zip` in
    `opal-313476888478-lambda-artifacts`, `source_code_hash` from its `content-sha256` metadata. Record the deploy afterwards with
    `record-terraform-deploy.sh`, as the last trade-pipeline deploy did.
  </context>

  <steps>
    PRECONDITION (CTO half condition 1, no grant is added): before step 0, confirm by read that this principal ALREADY holds the plan
       and apply of the `trade-pipeline` root AND the signing-key read. If either is missing: do NOTHING, open no ledger, and report
       to `2.0.0_SA_COO~O2`; the WHOLE act then goes to the laptop's cloud-ops seat. It is never split across boxes.
    0. Open the NEVER-2 ledger entry and COMMIT it immediately, and again after each leg. It states the pin `abf78fcb7f`, the three
       member hashes, and the one family on this artifact key (`trade-dashboard-api`).
    1. STOP 1: `git diff --name-only abf78fcb7f HEAD -- infra/aws/lambda/trade-pipeline infra/aws/terraform/trade-pipeline` is empty.
       Anything else is branch B.
    2. BEFORE: record the function's CodeSha256, its current `s3_object_version` (the ROLLBACK pin), its env key names and its layers.
    3. Write rows OUT and IN-F; mint the two tokens.
    4. **R0, BEFORE the apply:** OUT on `GET /api/general/trades/submissions/pending` through the CloudFront host. Record the status code
       and the response's `count` ONLY (no body to any file or message).
       - 200: the defect is read live. Proceed.
       - 403 or anything else: STOP. Apply nothing. Go to step 9 (cleanup) and report it as a FINDING for `1.0.0_SA_CTO~DELL2`.
    5. Build the zip from the source dir at the pin and upload it with `content-sha256` metadata. Each of the three members must hash to
       the objective's value; otherwise STOP and clean up.
    6. Plan, then `.tools/safe-apply.sh`.
       - Branch A: `0 to add, 1 to change, 0 to destroy`, namely `aws_lambda_function.trade_dashboard_api` (`s3_object_version` and
         `source_code_hash` only).
       - Anything else is branch B: STOP, apply nothing, clean up, report.
    7. AFTER (print each, with its time):
       - (a) CodeSha256 equals the uploaded zip's; the DEPLOYED zip is diffed against the build input MEMBER BY MEMBER (download the
         deployed package; each member's sha256 against the objective; the member count printed, expected 3);
       - (b) env and layers unchanged from step 2;
       - (c) R1: OUT on `.../submissions/pending` -> expect 403. A 200 means the release did not take: re-read (a), then roll back K1;
       - (d) R3: IN-F on `.../submissions/pending` -> expect 200 (status and `count` only). A 403 -> roll back K1. This is the branch 9 of
         the 9 real users pass by;
       - (e) R4: OUT on `GET /api/general/trades/users/me` -> expect 200 carrying its own email (record the status and whether the email
         matches, nothing else). Any other answer is recorded, not a rollback;
       - (f) IN-F on ONE data-refresh GET route -> expect refused. An admit is a STOP: report it, then clean up;
       - (g) the replan is 0-diff.
    8. Record the deploy.
    9. CLEANUP (also the STOP path): keep BOTH rows in place until BOTH tokens' `exp` has passed; then delete each and read it back
       ABSENT with ConsistentRead. Print each exp, each delete time and each ABSENT read. Never delete a row before its token expired.
    10. Close the ledger after the two ABSENT reads. Report once to `2.0.0_SA_COO~O2`: the plan line, (a)-(g) with times, the rollback pin
       recorded at step 2, the two ABSENT reads, and the words "tier arm UNEXERCISED on the deployed service".
  </steps>

  <bounds>
    Rollback of K1, same window: re-point the function to the step-2 `s3_object_version` by one `safe-apply` at the parent of the pin;
    the prior version serves every caller as today. Rollback of K2 is step 9.

    No third row and no tier-internal token, on any reading of the packet. No grant, env, route, table, layer, SES or portal change.
    No other function of the stack moves. No alert or monitor. No client's, partner's or staff member's sign-in is used, and no existing
    service token is read to make a call. No response body from a served read is written anywhere.
  </bounds>

  <amendment_1>
    AMENDMENT 1 (issuer, 2026-10-11 ~20:3xZ; applier msg 5769). The two issuer cells are cited by the ids `OW-sd-1` and `OW-sr-1`
    (the decomposition names them so; the long forms `OW-s-d-1` and `OW-s-r-1` stay as names), because the proof checker's cell-id
    pattern admits no third dashed segment. Only `<owned_cells>` and the three `cell_refs` changed; no step, bound or criterion id did.
    The two judgment criteria are GRADED by the issuer: MET, with the tier arm UNEXERCISED on the deployed service
    (org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_S_D1_ISSUER_GRADE_20261011.md). The applier re-points its
    instance's cell references to the two ids, re-validates, and flips this order `complete`.
  </amendment_1>

<proof_of_spec>
  <criterion id="OW-sd1-AC1" cell_refs="OW-sd-1"><invocation>python org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_CHECKS/ow_s_checks.py s2-probe</invocation><expect>OW-S2-PROBE-OK</expect></criterion>
  <criterion id="OW-sd1-AC2" cell_refs="OW-sd-1" judgment="true"/>
  <criterion id="OW-sr1-AC1" cell_refs="OW-sr-1" judgment="true"/>
</proof_of_spec>
OW-sd1-AC1 runs at the pin, before the upload (the handler's own print may appear above the check line; the last line is the verdict).
OW-sd1-AC2 (judgment, graded by the issuer): the plan branch, the member-by-member bytes and the unchanged env. OW-sr1-AC1 (judgment,
graded by the issuer; the outcome's grade is the CVO's): R0 served before, R1 refused after, R3 served after, on the deployed service.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, hold or gate is created or consumed by this deploy
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; CTO half condition 1 forbids adding one for the act
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; the authorization change was probed at the pin by the issuer (80 of 80 refused, 30 of 30 served) and its live negative arm is steps 4 and 7(c)
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for two issuer cells (OW-s-d-1, OW-s-r-1: the release of drained cell OW-s-2 at abf78fcb7f under a signed never-widen pair); not a worker cell.
</task_order>
