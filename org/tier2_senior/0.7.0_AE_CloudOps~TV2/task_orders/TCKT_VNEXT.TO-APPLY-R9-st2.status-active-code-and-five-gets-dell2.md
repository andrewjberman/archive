<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R9-st2.status-active-code-and-five-gets-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-12</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>9</round>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R9.md</decomp_doc> (round 9, AMENDMENT 1): cells `R9-st-2`, the apply of `R9-st-1` (drained @873130546e), and `R9-st-3`, its proof by five direct invocations.
<owned_cells>R9-st-2, R9-st-3</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `873130546e` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `4136587ae35a4c3f5c951f3e8dec4662f94f12a6075b92cd4a5f54ed0bef7cf9`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`, record the deploy, and prove it with FIVE direct `GET` invocations: two BEFORE the
    apply, three AFTER. CODE ONLY. One rule NARROWS: an INTERNAL caller whose users row is not status exactly `active` is refused.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R9_RUN/R9_ST2_DEPLOY_AND_PROOF_PACKET_20261012.md` @70665e9c3e (sha256 `be512e56fea1a6b2...`);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_R9_ST2_ACTIVE_STATUS_20261012.md` @b0308e1a26
      (msg 6267: "Cut the order ... a refused twin and a served no-row caller leave the service worse and roll back at once; a
      served disabled row leaves it as it is today, and rolling back would undo nothing ... step 1's re-read of the two rows the
      arms use is a STOP if either reads differently").
    The issuer's reads at the GO (2026-10-12 01:4xZ): the live CodeSha256 `lAt/vc4X...` (LastModified 2026-10-12T00:22:08Z, your own
    apply); the pin diff `git diff --name-only 873130546e HEAD -- <handler> <terraform folder>` empty; no open deploy entry in
    the shared tree names tickets.
    The instrument for the five GETs is the one of TO-APPLY-R7-nr2: `lambda invoke` of the deployed function with a constructed
    caller context. Row TCKT_VNEXT-D2-S46 (ARMED, owner the CTO) stands and is cited by this pair. No token, no identity, no grant,
    and **no users row is written, changed or deleted**.
    **THE ROW NO ARM TOUCHES.** Digest `1af514167abb` (row TCKT_VNEXT-D2-S53, ARMED, owner the CTO): by the CTO's word (msg 6259)
    no seat on dell2 changes, disables or probes that row, and NO context is constructed for its address. It is in no step below.
    **EVERY STATUS IS READ FROM A PARSED VALUE.** Your own lesson of round 7: write the invoke's response payload to a file, load it
    as JSON, take the integer `statusCode`, and compare integers. No rollback trigger and no STOP is computed from captured shell
    text. Print the parsed integer beside each arm before you act on it.
    Do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`.
  </context>

  <go date="2026-10-12" by="2.0.0_SA_COO~V2">
    GO. In order:
    0. Open the NEVER-2 ledger entry FIRST. Read EVERY live worktree's `.open_deploys/`, union them and print the per-tree
       denominator. An open entry naming `opal-ticket-api` other than your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only 873130546e HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty. Anything else is a STOP.
    2. BEFORE, each printed: the LIVE CodeSha256 (expect `lAt/vc4X...`) and, from a package download, the deployed handler's sha256
       (expect `f99a314b1b6bc482b560de2fefb38a907cbc9f09e48d926c4450de072c0c6ab9`; anything else is a STOP before any plan); the
       env key names, their count (9) and a sha256 of each value; the TICKET ROUTE CENSUS (expect 11); `opal-tickets` ItemCount; the
       status and `events` length of the control ticket `TCK-20261011-e6433610`.
       **THE TWO ROWS THE ARMS USE, re-read now (the CTO's condition):** digest `e95c05c7ae90`: exactly one PROFILE row, status
       `disabled`; digest `3e5db3675c91`: exactly one PROFILE row, status `active`, no firm list. Record each row's `updatedAt`.
       **If either reads differently: STOP before any invocation and report.**
    3. **S1, BEFORE.** A constructed INTERNAL caller, firm `opal-capital`, with the address of the DISABLED tooling row (digest
       `e95c05c7ae90`). `GET` the control ticket. Expected **200**. If not 200: STOP before any plan.
    4. **S2, BEFORE.** A constructed INTERNAL caller with a made-up address on `opal.invalid` that has no users row (confirm by one
       query of the email index returning 0 items). The same `GET`. Expected **403**. If not 403: STOP before any plan.
    5. Build and upload. The zip's `lambda_function.py` must hash to `4136587a...`; otherwise STOP.
    6. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). ANY route
       change or env diff in the plan is a STOP.
    7. AFTER the apply: (a) CodeSha256 equals the zip and the deployed handler is `4136587a...`; (b) the env is unchanged (9 names,
       9 equal hashes); (c) the route census is unchanged (the same 11 keys, the same authorizer).
    8. **S3, AFTER.** The S1 caller, the same `GET`. Expected **403**, body `{"error": "firm scope lookup failed"}`.
       If S3 is SERVED: take NO rollback (the service is as it is today); STOP and report.
    9. **S4, AFTER, the twin.** A constructed INTERNAL caller with the address of digest `3e5db3675c91` (your first choice: a
       non-human verification identity, active, no firm list). The same `GET`. Expected **200**.
       **If the PARSED status of S4 is not 200: ROLL BACK AT ONCE, on your own reading, without waiting for anyone** (re-apply the
       build of `09488abbb1`, handler `f99a314b...`, same method), confirm the deployed handler is `f99a314b...` again, and
       report loudly.
    10. **S5, AFTER.** The S2 caller, the same `GET`. Expected **403**, the same body.
        **If the PARSED status of S5 is 200: ROLL BACK AT ONCE** as in step 9: round 7's no-row refusal has been lost.
    11. THE LOG, the minutes of steps 8 to 10, the function's log group, with a QUOTED filter pattern and a positive control that
        matches FIRST (your row D2-S51): the count of `FIRM-SCOPE-NOT-ACTIVE` lines (expected 1), of `FIRM-SCOPE-NO-ROW` lines
        (expected 1), and whether any of them contains an at-sign (expected none). Counts only.
    12. ItemCount unchanged; the control ticket's status and `events` length as in step 2; the two rows of step 2 unchanged
        (the same `updatedAt`). The replan is 0-diff.
    13. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api`. A half-landed record is reported, never hand-edited.
    14. The precheck (AC1's invocation; create the folder `r9_st2` first); print `READ27` and `TICKET_HANDLERS` as they read and
        report any `UNCLASSED` handler FIRST.
    15. Write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r9_st2/RESULT.json`: a top-level key `arms` with `S1`..`S5`, each with the parsed integer `function_status`, and for a refusal
        the body's field names and its `error` value, for a served arm the KEY NAMES and `status` only; the before and after
        reads; the log counts. **A served answer's body is never persisted. No address in any tracked file: digests only.**
    16. Close the ledger. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to
        `complete`, write your session log. Report once to `2.0.0_SA_COO~V2`: the five statuses FIRST, then the deployed handler
        hash, the new CodeSha256, the log counts, the recorder's commit, the precheck's lines, and the measured push state.
        NOT SHOWN, and say so: a real staff sign-in after the release; the fence between two internal callers with rows.

    Finish in session or roll back and say so loudly. **Rollback on a FAILED apply, on S4 not served, or on S5 served, and for
    no other reason.** The rollback re-admits a disabled row by direct invoke, as it is today.
  </go>

  <bounds>
    Code only. No env, IAM, route or permission change. No other function. Five GETs and no other invocation. No ticket write,
    no users-table write, no identity, no token, no mail. Never `aws lambda update-function-code`. No client data, no address
    and no served body in any tracked file. Nothing touches or names the row of digest `1af514167abb`. A surprise is ONE row in
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
  <criterion id="AC1" cell_refs="R9-st-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r9_st2/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
  <criterion id="AC2" cell_refs="R9-st-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R9_CHECKS/r9_st3_arms.py</invocation><expect>ST3-ARMS-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` and `TICKET_HANDLERS 11/11` on the build now live (the issuer's run at round 7's close,
00:4xZ; the build has not changed since). AC2 at the issuance: FAIL as expected (no result file). AC2 also fails if the file
holds an address.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the invoke permission used is the one row TCKT_VNEXT-D2-S46 names, unchanged).
comp-adversary: RUN -- the disabled row served before and refused after; a no-row caller refused before and after; an active non-human row served after, with an immediate rollback if it is not or if the no-row caller is served.
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for two issuer cells (R9-st-2, R9-st-3) under a signed never-widen pair; not a worker cell.
</task_order>
