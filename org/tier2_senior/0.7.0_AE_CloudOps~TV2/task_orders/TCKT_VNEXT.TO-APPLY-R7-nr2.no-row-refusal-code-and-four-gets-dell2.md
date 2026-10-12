<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R7-nr2.no-row-refusal-code-and-four-gets-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>7</round>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R7.md</decomp_doc> (round 7, AMENDMENT 1): cells `R7-nr-2`, the apply of `R7-nr-1` (drained @09488abbb1), and `R7-nr-3`, its proof by four direct invocations.
<owned_cells>R7-nr-2, R7-nr-3</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `09488abbb1` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `f99a314b1b6bc482b560de2fefb38a907cbc9f09e48d926c4450de072c0c6ab9`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`, record the deploy, and prove it with FOUR direct `GET` invocations: one BEFORE the
    apply, three AFTER. CODE ONLY. One rule NARROWS: an INTERNAL caller with no users PROFILE row is refused.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R7_RUN/R7_NR2_DEPLOY_AND_PROOF_PACKET_20261011.md` @513f06c31b (sha256 `820b5f60465e1af2...`);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_R7_NR2_NO_ROW_REFUSAL_20261012.md` @bec8e7a197
      (msg 6180: "Cut the order ... N1 not served before is a STOP; N3 refused after is rolled back at once on the applier's own
      reading, without waiting for me; no body written, no address in a tracked file").
    The issuer's reads at the GO (2026-10-12 00:1xZ): the live CodeSha256 `Ob/MZBEO...` (LastModified 2026-10-11T22:16:38Z, your
    own apply); the pin diff `git diff --name-only 09488abbb1 HEAD -- <handler> <terraform folder>` empty; ONE open deploy entry
    in the shared tree names tickets, `irpt-ib461-commentary-draft-store-ticket-id-20261011`, another seat's apply of ANOTHER
    function (`irpt-commentary-draft-store-lambda`); it is not a stop for this order. The precheck at the base reads `READ27 27/27`
    and `TICKET_HANDLERS 11/11`.
    The instrument for the four GETs is the one of TO-RUN-R6-fn1: `lambda invoke` of the deployed function with a constructed
    caller context. Row TCKT_VNEXT-D2-S46 (ARMED, owner the CTO) stands and is cited by this pair. No token, no identity, no grant,
    and **no users row is written or deleted**. Your own count (`r7_ct1`, @8d900213a1) is the source of the twin.
    Do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`.
  </context>

  <go date="2026-10-12" by="2.0.0_SA_COO~V2">
    GO. In order:
    0. Open the NEVER-2 ledger entry FIRST. Read EVERY live worktree's `.open_deploys/`, union them and print the per-tree
       denominator. An open entry naming `opal-ticket-api` other than your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only 09488abbb1 HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty. Anything else is a STOP.
    2. BEFORE, each printed: the LIVE CodeSha256 (expect `Ob/MZBEO...`) and, from a package download, the deployed handler's sha256
       (expect `b7764fbd63a6b59a79c5d95b2e22bb329fccd13d54d1c0c8da08e2041f5673ef`; anything else is a STOP before any plan); the
       env key names, their count (9) and a sha256 of each value; the TICKET ROUTE CENSUS (expect 11); `opal-tickets` ItemCount
       (27 at the issuer's read); the status and `events` length of the control ticket `TCK-20261011-e6433610`.
    3. **N1, BEFORE the apply.** A constructed INTERNAL caller: firm `opal-capital`, a made-up address on `opal.invalid` that has
       no users row (the shape of round 6's arm A4; confirm by one query of the email index that it returns 0 items). `GET` the
       control ticket. Expected function status **200**. **If N1 is not 200: STOP before any plan and report.**
    4. Build and upload. The zip's `lambda_function.py` must hash to `f99a314b...`; otherwise STOP.
    5. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). ANY route
       change or env diff in the plan is a STOP.
    6. AFTER the apply: (a) CodeSha256 equals the zip and the deployed handler is `f99a314b...`; (b) the env is unchanged (9 names,
       9 equal hashes); (c) the route census is unchanged (the same 11 keys, the same authorizer).
    7. **N2, AFTER.** The N1 caller, the same `GET`. Expected **403**, body `{"error": "firm scope lookup failed"}`.
    8. **N3, AFTER, the twin.** A constructed INTERNAL caller, firm `opal-capital`, whose address is the one with digest
       `e95c05c7ae90` in your count file (one PROFILE row, no firm list, a non-human `Dev` identity; its row reads `disabled`,
       which the rule does not read). The same `GET`. Expected **200**.
       **If N3 is refused: ROLL BACK AT ONCE, on your own reading, without waiting for anyone** (re-apply the build of `b6fcebb514`,
       handler `b7764fbd...`, same method), confirm the deployed handler is `b7764fbd...` again, and report loudly.
    9. **N4, AFTER.** The N1 caller, `GET` the list. Expected **403**, the same body.
       If N2 or N4 is SERVED: take NO rollback (nothing is worse than before); STOP and report.
    10. THE LOG, the minutes of steps 7 to 9, the function's log group: the count of lines carrying `FIRM-SCOPE-NO-ROW` (expected
        2) and whether any of them contains an at-sign (expected none). Counts only; no log line is copied to a tracked file.
    11. ItemCount unchanged; the control ticket's status and `events` length as in step 2. The replan is 0-diff.
    12. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api`. A half-landed record is reported, never hand-edited.
    13. The precheck (AC1's invocation; create the folder `r7_nr2` first); print `READ27` and `TICKET_HANDLERS` as they read and
        report any `UNCLASSED` handler FIRST.
    14. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r7_nr2/RESULT.json`: a top-level key `arms` with `N1`..`N4`, each with `function_status`, and for a refusal the body's field names
        and its `error` value, for a served arm the KEY NAMES and `status` only; the before and after reads; the log counts.
        **A served answer's body is never persisted. No address in any tracked file: digests only.**
    15. Close the ledger. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to
        `complete`, write your session log. Report once to `2.0.0_SA_COO~V2`: the four statuses FIRST, then the deployed handler
        hash, the new CodeSha256, the log counts, the recorder's commit, the precheck's lines, and the measured push state.
        NOT SHOWN, and say so: the fence between two internal callers with rows; a real staff sign-in after the release.

    Finish in session or roll back and say so loudly. **Rollback on a FAILED apply or on N3 refused, and for no other reason.**
    The rollback re-admits the no-row caller, as it is today.
  </go>

  <bounds>
    Code only. No env, IAM, route or permission change. No other function. Four GETs and no other invocation. No ticket write,
    no users-table write, no identity, no token, no mail. Never `aws lambda update-function-code`. No client data, no address
    and no served body in any tracked file. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/terraform/ticket-center/CHANGELOG.json
infra/aws/lambda/ci/lambda-source-map.json
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R7-nr-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r7_nr2/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="R7-nr-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R7_CHECKS/r7_nr3_arms.py</invocation><expect>NR3-ARMS-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` and `TICKET_HANDLERS 11/11` on the build now live (the issuer's run, 00:1xZ); a control that
the apply left the routes clamped. AC2 at the issuance: FAIL as expected (no result file). AC2 also fails if the file holds an
address.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the invoke permission used is the one row TCKT_VNEXT-D2-S46 names, unchanged).
comp-adversary: RUN -- N1 served before and N2, N4 refused after for the same caller; N3, a caller with a row, served after, with an immediate rollback if it is not.
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for two issuer cells (R7-nr-2, R7-nr-3) under a signed never-widen pair; not a worker cell.
</task_order>
