<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R4-pk2.package-door-env-list-code-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>4</round>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R4.md</decomp_doc> (round 4): cell `R4-pk-2`, the apply of `R4-pk-1` (drained @f239b06ad8).
<owned_cells>R4-pk-2</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `f239b06ad8` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `c40036677aae180cb362f89f2c2aecb62ef53fd0b1a285bb3bd2c813176c1026`) and ONE new env key, `PACKAGE_ALLOWED_FIRMS = ""` (EMPTY),
    with ONE `safe-apply` in `infra/aws/terraform/ticket-center`, then record the deploy. The package door then binds the
    packager's firm to that list, which is empty, so the door admits NOBODY. Two creator refusals of the report route gain a `code`.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R4_RUN/R4_PK2_DEPLOY_PACKET_20261011.md` @0e00fc4a32;
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R4_PK2_PACKAGE_DOOR_ENV_LIST_CTO_HALF.md` @0135c6f2c8.
    THE CTO HALF NAMES BRANCH E: "The applier adds PACKAGE_ALLOWED_FIRMS = "" and nothing else. The list is an authorisation and
    is named in the pair that mints the packager." Do NOT add any firm to the list. A list with a firm in it is OUTSIDE this order.
    The issuer's reads at the GO (14:56Z): `opal-ticket-api` CodeSha256 `20v0+vfe...` (13:34:27Z); the pin diff
    `git diff --name-only f239b06ad8 HEAD -- <handler> <terraform folder>` empty; 0 TCKT entries open in the shared tree.
    The method is the one you used for TO-APPLY-R3-rf2; do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`. This order mints no
    identity, writes no ticket, touches no other function and sends no request down the YCharts path.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    0. Open the NEVER-2 ledger entry FIRST. The one function family on the artifact key is `opal-ticket-api`. Read EVERY live
       worktree's `.open_deploys/`, union them and print the per-tree denominator. An open entry naming `opal-ticket-api` other than
       your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only f239b06ad8 HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty BEFORE your own edit of step 3. Anything else is a STOP.
    2. STOP 2 (the rollback target): download the LIVE `opal-ticket-api` package and show the deployed `lambda_function.py` sha256 is
       `dc0cd973c61f4b037e7181f4675ec8ffe2ec68414cfd9e036c01f4096f386a15`. Record CodeSha256 (expect `20v0+vfe...`), the env key
       NAMES and their count (expect 8), a sha256 of EACH env value (never print `TICKET_DL_MAP` or `CLIENT_LINK_MAP` contents),
       `opal-tickets` ItemCount, and the status fields (`status`, `assignee`, `created_by`) of `TCK-20261009-a1052909`.
    3. THE ONE EDIT: in `infra/aws/terraform/ticket-center/main.tf`, inside `environment_variables`, directly after the
       `COMMENTARY_ALLOWED_FIRMS` line (line 258), add a comment line and the line `PACKAGE_ALLOWED_FIRMS = ""`. The comment says:
       declared empty on purpose; the package door admits nobody until the pair that mints the packager names the list (CTO half
       @0135c6f2c8). Commit that file alone. Nothing else in the folder changes.
    4. Build and upload. The zip's `lambda_function.py` must hash to `c4003667...`; otherwise STOP.
    5. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy`: the function's source_code_hash and
       ONE env key added with an empty value. Any other resource, or any other env key in the diff, is a STOP.
    6. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed file is `c4003667...`;
       - (b) the env has 9 key names; the 8 old values hash the same as in step 2; `PACKAGE_ALLOWED_FIRMS` is present and its
         value is the empty string (print its length, 0);
       - (c) an unauthenticated POST to `/api/scoped/tickets/TCK-20261009-a1052909/package` and to `.../report` through CloudFront
         is each refused 401;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads the same status fields as in step 2;
       - (e) the replan is 0-diff.
    7. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api`. STOP 3: if it lands only one of its two halves, STOP and
       report which; do not hand-edit the map (row TCKT_VNEXT-D2-S36).
    8. `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_pk2/clamp_precheck_table.json`
       reads `READ27 27/27` with the `opal-ticket-api` line CLAMPED on the new build (create the folder first).
    9. Close the ledger. Write the proof-of-spec instance in your deliverables folder ROOT (the gate looks there, as you found for
       TO-RUN-R3-tr1), validate it, flip this order to `complete`, and write your session log. Report once to
       `2.0.0_SA_COO~V2`: the deployed file hash FIRST, the new CodeSha256, the env key count and the new key's length, the
       recorder's commit, the precheck line, and the measured push state of your commits. Do not claim the package door's codes
       or its admission were exercised: with an empty list nothing can be admitted, and nothing was.

    Finish in session or roll back and say so loudly. Rollback: re-apply the build of `8ef21584f8` (file `dc0cd973...`) with the
    env line removed, same method.
  </go>

  <bounds>
    No IAM, route or permission change. No env change but the one empty key. No other function. No ticket write, no identity, no
    token. Never `aws lambda update-function-code`. No client data in any tracked file. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (`TCKT_VNEXT-D2-S<k>`, next free id;
    binary append, line endings kept), never a halt on anything but the STOPs above.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/terraform/ticket-center/main.tf
infra/aws/terraform/ticket-center/CHANGELOG.json
infra/aws/lambda/ci/lambda-source-map.json
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R4-pk-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_pk2/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` on the build now live (the issuer's run, 13:55Z); after the apply it must read the same with
the ticket host on the new build, which it does only if the recorder ran (step 7).

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the authorizer and the matrix are untouched; the one env key is empty and admits nobody).
comp-adversary: RUN -- the two unauthenticated POSTs refused 401 (step 6c) and the precheck's 27-route clamp read on the new build (step 8).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (R4-pk-2) under a signed never-widen pair; not a worker cell.
</task_order>
