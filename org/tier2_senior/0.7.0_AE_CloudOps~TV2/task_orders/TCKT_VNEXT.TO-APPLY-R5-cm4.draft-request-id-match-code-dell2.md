<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R5-cm4.draft-request-id-match-code-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>5</round>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R5.md</decomp_doc> (round 5, AMENDMENT 5): cell `R5-cm-4`, the apply of `R5-cm-3` (drained @b6fcebb514).
<owned_cells>R5-cm-4</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `b6fcebb514` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `b7764fbd63a6b59a79c5d95b2e22bb329fccd13d54d1c0c8da08e2041f5673ef`) with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`, then record the deploy. CODE ONLY. One route's rule NARROWS: the commentary-draft route
    accepts a draft only on the ticket whose own recorded request id equals the request id in the body.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R5_RUN/R5_CM4_DEPLOY_PACKET_20261011.md` @675c87aa34;
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_R5_CM4_DRAFT_REQUEST_ID_MATCH_20261011.md` @15b0cd9a3f
      ("It only narrows. Cut the order. The rollback re-widens and is taken only on a failed apply.").
    The issuer's reads at the GO (21:5xZ): the live CodeSha256 `e1ZHjf21...` (21:27:13Z, your own apply); the pin diff
    `git diff --name-only b6fcebb514 HEAD -- <handler> <terraform folder>` empty; 0 TCKT entries open in the shared tree.
    Your finding in TO-APPLY-R5-ml2 is taken into this order: a 401 does not prove a route exists, so the proof that the routes
    are still in place is the ROUTE CENSUS, before and after. Nothing calls the route today.
    The method is the one you used for TO-APPLY-R5-ml2, without a Terraform edit; do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`.
    This order mints no identity, writes no ticket, sends no mail and touches no other function.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    0. Open the NEVER-2 ledger entry FIRST. Read EVERY live worktree's `.open_deploys/`, union them and print the per-tree
       denominator. An open entry naming `opal-ticket-api` other than your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only b6fcebb514 HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center`
       is empty. Anything else is a STOP.
    2. BEFORE, each printed: the LIVE CodeSha256 (expect `e1ZHjf21...`) and, from a package download, the deployed handler's sha256
       (expect `7113a74945892d663da422261209a2e5bdaf5af579ad63cdf7067dfab1e00a07`; anything else is a STOP before any plan); the
       env key names, their count (9) and a sha256 of each value; the TICKET ROUTE CENSUS (expect 11, each `CUSTOM` behind the
       portal authorizer; list the route keys); `opal-tickets` ItemCount; the status fields of `TCK-20261009-a1052909` and whether
       it carries `draft_commentary` or `commentary_sent`.
    3. Build and upload. The zip's `lambda_function.py` must hash to `b7764fbd...`; otherwise STOP.
    4. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy` (source_code_hash only). ANY route
       change or env diff in the plan is a STOP.
    5. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed handler is `b7764fbd...`;
       - (b) the env is unchanged (9 names, 9 equal hashes);
       - (c) the ticket route census is unchanged: the same 11 route keys, the same authorizer;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads as in step 2;
       - (e) the replan is 0-diff.
    6. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api`. STOP 3: a half-landed record is reported, never hand-edited.
    7. `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r5_cm4/clamp_precheck_table.json`
       (create the folder first); print its totals line(s) as they read. `READ27 27/27` is a regression read of its frozen 27
       routes and is not claimed as coverage of the commentary routes (your row D2-S45). If the precheck in your tree already
       prints a second line `TICKET_HANDLERS n/m`, print that too and report any `UNCLASSED` handler FIRST.
    8. Close the ledger. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to
       `complete`, write your session log. Report once to `2.0.0_SA_COO~V2`: the deployed handler hash FIRST, the new CodeSha256,
       the route census before and after, the recorder's commit, the precheck's line(s), and the measured push state.
       UNEXERCISED, and say so: the route's admission, the match, every arm of its deny and both 409s.

    Finish in session or roll back and say so loudly. **Rollback only on a FAILED apply:** re-apply the build of `33d165b4ef`
    (handler `7113a749...`), same method. That rollback re-widens what `svc-commentary` may write; it is never taken for any
    other reason.
  </go>

  <bounds>
    Code only. No env, IAM, route or permission change. No other function. No ticket write, no identity, no token, no mail.
    Never `aws lambda update-function-code`. No client data in any tracked file. A surprise is ONE row in
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
  <criterion id="AC1" cell_refs="R5-cm-4"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r5_cm4/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` on the build now live (the issuer's run, 21:5xZ). It is a control that the apply and the
record left the frozen 27 routes clamped; it is not the proof of this route, which is step 5.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the authorizer, the routes and the matrix are untouched).
comp-adversary: RUN -- the route census before and after (the same 11 keys behind the same authorizer) and the precheck's 27-route clamp read on the new build.
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (R5-cm-4) under a signed never-widen pair; not a worker cell.
</task_order>
