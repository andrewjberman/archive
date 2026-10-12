<task_order>
  <metadata>
    <id>NFRA_OPSWKF.TO-APPLY-S2.trade-submit-internal-only-dell2</id>
    <issued_by>2.0.0_SA_COO~O2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>NFRA_OPSWKF</project_code>
  </metadata>
<risk>WORLD</risk>
<round>2</round>
<workstream>S</workstream>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPSWKF/decompositions/NFRA_OPSWKF_DECOMP.md</decomp_doc> (workstream S, the additions of 2026-10-11): issuer cells `OW-sd-2` and `OW-sr-2`, serving drained cell OW-s-3 (merged @234c3b4b10).
<owned_cells>OW-sd-2, OW-sr-2</owned_cells>
</decomp_ref>

  <objective>
    FWD-9 (PRD v0.8 @cfc5091071): release the code of ONE function, `trade-submission-handler`, by ONE `safe-apply` of
    `infra/aws/terraform/trade-pipeline` at box/dell2 pin `234c3b4b10`, and prove the refusal on the deployed service with ONE synthetic
    outsider posting ONE body that cannot be stored. Build input (`infra/aws/lambda/ci/lambda-source-map.json`, three members), sha256
    hex at the pin:
    - `submission_handler.py`  466334f98aa3707c75b177cab14ff4df9c832176dc33bb4d794adab36960ab8c
    - `email_utils.py`         1c6f63a57215843ccbbdfc6552092b51e62373cae769303af8c0390554bc6d6b
    - `config.py`              042efba5f0cf06ed15d0617ec1105f68d5f9131ef42498edb5143853ce59aa56
    Nothing else: no env key, grant, route, table, layer, SES setting or other function; no portal file.
  </objective>

  <context>
    READ BOTH HALVES WHOLE BEFORE STEP 0, the files themselves and not this restatement (your own disclosure on TO-APPLY-S1), and say
    in the ledger's opening entry that you did.
    - Packet and COO half (SIGNED): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_SD2_FWD9_RELEASE_PAIR_20261011.md
      @82acb3a295, sha256 begins c9e414d3e2d8e0b6.
    - CTO half (SIGNED, msg 5817): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_OW_SD2_FWD9_RELEASE_20261011.md
      @1ca1f1ea52. Where it differs from the packet it GOVERNS:
      - **Caller IN is REFUSED and is NOT minted. Read R2 is NOT made.** No Opal-internal identity of any shape is minted.
      - Row OUT only; reads P0, R0 and R1; the `by-initiator` Count for OUT's address with its control.
      - The admitted arm is recorded "UNEXERCISED ON THE DEPLOYED SERVICE" and your report uses those words.
      - The ledger closes after OUT's ABSENT read.

    Caller OUT (packet section 4): row in `opal-users-v2`, `PK USER#opswkf-fwd9-out-20261011@opal.invalid`, `SK PROFILE`, conditional put
    `attribute_not_exists(PK)`: `tier advisor`, `role user`, `firmId fwd9-synthetic-nofirm`, `userType test-filer`, `status active`, a
    `name` beginning `NFRA_OPSWKF FWD-9 synthetic`, `allowedFirmIds ["fwd9-synthetic-nofirm"]` as a LIST. Token: as you minted for
    TO-APPLY-S1 (RS256, the current signing key, `iss opal-portal-auth`, `aud opal-portal-api`), with `sub` AND `email` = the row's
    address (the caller must carry a verified email), the row's claims, and `exp` = run start + the run's stated length + 5 minutes;
    state the length before minting and keep it as short as the acts allow. Token value in memory only.

    THE ONE BODY, the only thing ever posted, to `POST /api/general/trades/submit` through the CloudFront host:
    `{"fund": "PFDE", "ticket_id": "not-a-ticket-id"}` -- no `initiator_email`, no securities. Send it byte for byte; do not add a field.

    With the token you make EXACTLY TWO calls, R0 and R1, both on that one route. No call on any other route or surface, for any
    reason, including to find which hop answered: read the hop from the response's own headers of those two calls.
  </context>

  <steps>
    PRECONDITION: no grant is added. This principal applied this root and read the signing key today; if either now fails, do nothing
       further, clean up what exists, and report. The act is never split across boxes.
    0. Open the NEVER-2 ledger entry and COMMIT it immediately, and again after each leg. It states the pin `234c3b4b10`, the three
       member hashes, the one family on this artifact key (`trade-submission-handler`), and that both halves were read whole.
    1. STOP 1: `git diff --name-only 234c3b4b10 HEAD -- infra/aws/lambda/trade-pipeline infra/aws/terraform/trade-pipeline` is empty.
       Anything else is branch B.
    2. BEFORE: record the function's CodeSha256, its current `s3_object_version` (the ROLLBACK pin), its env key NAMES and its layers.
    3. **P0, before any POST:** download the DEPLOYED package and hash its `submission_handler.py`. It must equal
       `fc59cd256c1797860277a200a39d47a493f06cef56e4c6ac6f10010c1bb146a4`. Any other value: STOP before any row or token exists; the
       body's "stores nothing" rests on those bytes. Report.
    4. Write row OUT; mint its token.
    5. **R0, BEFORE the apply:** OUT posts the ONE body. Record the status code and the `message` field ONLY.
       - `400` with message `ticket_id is malformed`: the defect's path is read live and nothing was stored. Proceed.
       - `403`: STOP. Apply nothing. Clean up (step 10). Report it as a FINDING for `1.0.0_SA_CTO~DELL2`.
       - `200`: STOP and report AT ONCE, before cleanup: a submission was stored and a mail sent. Name the submission id from the
         response. Do NOT delete it. Apply nothing.
       - anything else: STOP, apply nothing, clean up, report the status and which hop answered.
    6. Build the zip from the source dir at the pin and upload it with `content-sha256` metadata. Each of the three members must hash to
       the objective's value; otherwise STOP and clean up.
    7. Plan, then `.tools/safe-apply.sh`, applied from the saved plan file.
       - Branch A: `0 to add, 1 to change, 0 to destroy`, namely `aws_lambda_function.trade_submission_handler` (`s3_object_version`,
         `source_code_hash`, and Terraform's computed `last_modified`).
       - Anything else is branch B: STOP, apply nothing, clean up, report.
    8. AFTER (print each, with its time):
       - (a) CodeSha256 equals the uploaded zip's; the DEPLOYED package diffed against the build input MEMBER BY MEMBER, both directions,
         member count printed (expected 3);
       - (b) env key NAMES and layers unchanged from step 2;
       - (c) **R1:** OUT posts the ONE body again -> expect `403` with message EXACTLY `Forbidden: trade submission answers Opal staff only`,
         answered by the function (not by another hop). A `400` means the release did not take: re-read (a), then roll back K1. A 403
         with any OTHER message is not the new check: treat it as not taken, re-read (a), and report before rolling back;
       - (d) no row: query `opal-trade-submissions` index `by-initiator` for OUT's address -> expect Count 0; and ONE control beside it:
         the same query for an initiator known to have submissions returns a non-zero Count (record the count only, no item);
       - (e) the replan is 0-diff.
    9. Record the deploy as TO-APPLY-S1's step 8 did.
    10. CLEANUP (also the STOP path): keep row OUT in place until its token's `exp` has passed; then delete it and read it back ABSENT
       with ConsistentRead, with a control. Print the exp, the delete time and the ABSENT read.
    11. Close the ledger after the ABSENT read. Report once to `2.0.0_SA_COO~O2`: the plan line, P0, R0, (a)-(e) with times, the rollback
       pin from step 2, the ABSENT read, and the words "admitted arm UNEXERCISED ON THE DEPLOYED SERVICE". Put the proof-of-spec
       instance at the flat path the gate accepts, as you found on TO-APPLY-S1.
  </steps>

  <bounds>
    Rollback of K1, same window: re-point the function to the step-2 `s3_object_version` by one `safe-apply`; the prior version serves
    every caller as today. Rollback of K2 is step 10.

    ONE synthetic row and ONE token, never two. No Opal-internal identity, no tier-internal token, no `opal-capital` firmId on any
    synthetic claim. Exactly two calls with the token, on the one route. No call to data-refresh or to any other surface. No grant,
    env, route, table, layer, SES or portal change; no other function of the stack moves. No alert or monitor. No real person's
    sign-in and no existing service token. No response body beyond the status code and the `message` field is written anywhere.
    A stored submission is never deleted by you.
  </bounds>

<proof_of_spec>
  <criterion id="OW-sd2-AC1" cell_refs="OW-sd-2"><invocation>python org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_CHECKS/ow_s_checks.py s9-probe</invocation><expect>OW-S9-PROBE-OK</expect></criterion>
  <criterion id="OW-sd2-AC2" cell_refs="OW-sd-2" judgment="true"/>
  <criterion id="OW-sr2-AC1" cell_refs="OW-sr-2" judgment="true"/>
</proof_of_spec>
OW-sd2-AC1 runs at the pin, before the upload. OW-sd2-AC2 (judgment, graded by the issuer): the plan branch, the member-by-member bytes
and the unchanged env. OW-sr2-AC1 (judgment, graded by the issuer; the outcome's grade is the CVO's): R0 answered 400 before and R1 the
new 403 after, on the deployed service, with no row stored.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, hold or gate is created or consumed by this deploy
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; the CTO half forbids adding one for the act
comp-adversary: DECLARED-NOT-APPLICABLE at the cut; the authorization change was probed at the pin by the issuer (28 of 28 refused with the new message, 2 of 2 insiders at the 400) and its live refusal is steps 5 and 8(c)
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for two issuer cells (OW-sd-2, OW-sr-2: the release of drained cell OW-s-3 at 234c3b4b10 under a signed never-widen pair); not a worker cell.
</task_order>
