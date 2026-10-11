<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R5-ml2.commentary-routes-and-mail-digest-dell2</id>
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
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R5.md</decomp_doc> (round 5): cell `R5-ml-2`, the apply of `R5-ml-1`, `R5-cm-1` and `R5-cm-2` (all drained; pin 33d165b4ef).
<owned_cells>R5-ml-2</owned_cells>
</decomp_ref>

  <objective>
    Deploy the code of `opal-ticket-api` at box/dell2 `33d165b4ef` (`infra/aws/lambda/ticket_center/lambda_function.py` sha256 hex
    `7113a74945892d663da422261209a2e5bdaf5af579ad63cdf7067dfab1e00a07`) and add TWO API routes, with ONE `safe-apply` in
    `infra/aws/terraform/ticket-center`, then record the deploy. The build adds two write-once routes on the ticket
    (`.../commentary-draft` for the one service subject `svc-commentary`; `.../commentary-sent` for an internal person) and puts a
    digest of the recipient, never the address, on the client mail log lines. NO env change.
  </objective>

  <context>
    Both halves are SIGNED. Read both, with the packet's AMENDMENT 1, before any AWS call:
    - packet and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R5_RUN/R5_ML2_DEPLOY_PACKET_20261011.md` @fb203f854b
      (sections 2 to 5, then AMENDMENT 1: the pin and the handler hash are the AMENDMENT's, not the body's);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_R5_ML2_COMMENTARY_ROUTES_AND_MAIL_DIGEST_20261011.md`
      (signed @c1c7a3b194 on AMENDMENT 1 and confirmed for the build at 33d165b4ef @e1506c3a04).
    Nothing calls either new route today: the commentary drafter still creates a new ticket, and no page calls the sent route.
    The method is the one you used for TO-APPLY-R4-pk2; do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`. This order mints no
    identity, writes no ticket, sends no mail, touches no other function and sends no request down any generation path.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO, on the CTO's confirmation (msg 5826, recorded in its half @e1506c3a04: "The half is signed for that
    build; the expected deployed hash in your steps is 7113a749. Cut the order."). The issuer's reads at the GO (20:5xZ): the live
    CodeSha256 `d2w1YJ8A...` (18:06:52Z); the pin diff empty; 0 TCKT entries open in the shared tree. In order:
    0. Open the NEVER-2 ledger entry FIRST. The one function family on the artifact key is `opal-ticket-api`. Read EVERY live
       worktree's `.open_deploys/`, union them and print the per-tree denominator. An open entry naming `opal-ticket-api` other than
       your own is a STOP.
    1. STOP 1 (the pin): `git diff --name-only 33d165b4ef HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center/main.tf`
       is empty BEFORE your own edit. Anything else is a STOP.
    2. BEFORE, each printed:
       - (a) the LIVE CodeSha256 (expect `d2w1YJ8A...`) and, from a package download, the deployed handler's sha256 (expect
         `c40036677aae180cb362f89f2c2aecb62ef53fd0b1a285bb3bd2c813176c1026`). A different handler is a STOP before any plan;
       - (b) the env key NAMES, their count (expect 9) and a sha256 of EACH value (never print `TICKET_DL_MAP` or
         `CLIENT_LINK_MAP` contents);
       - (c) from the BUILD's handler (the tree at the pin): the tuples `DL_NOTICE_PROHIBITED` and `CLIENT_NOTICE_PROHIBITED`, and
         the lines that choose which ticket members a CLIENT notice carries. State whether `draft_commentary`, `commentary_sent`
         or `package` could reach a client's mail. If one could, STOP and report;
       - (d) an unauthenticated POST through CloudFront to `/api/scoped/tickets/TCK-20261009-a1052909/commentary-draft` and to
         `.../commentary-sent`: record each BEFORE answer (the routes do not exist yet; whatever it answers is the baseline);
       - (e) `opal-tickets` ItemCount, and for `TCK-20261009-a1052909` its `status`, `assignee`, `created_by` and whether it
         carries `draft_commentary` or `commentary_sent`.
    3. THE ONE EDIT: in `infra/aws/terraform/ticket-center/main.tf`, inside `local.ticket_routes`, directly after the `package`
       entry, add a comment and these two entries, and nothing else:
       `commentary_draft = "POST /api/scoped/tickets/{ticketId}/commentary-draft"`
       `commentary_sent  = "POST /api/scoped/tickets/{ticketId}/commentary-sent"`
       The comment says: TCKT_VNEXT R5-cm-1 (FWD-6): the drafter sets the draft on the EXISTING ticket, once; an internal person
       records that the final commentary was sent, once; same integration, same authorizer, same CloudFront behavior; no
       permission added. Commit that file alone.
    4. Build and upload. The zip's `lambda_function.py` must hash to `7113a749...`; otherwise STOP.
    5. Plan, then `.tools/safe-apply.sh`. Branch A is `2 to add, 1 to change, 0 to destroy`: two `aws_apigatewayv2_route`
       resources and the function's source_code_hash. Any env diff, any other resource, or a route whose `authorization_type` is
       not `CUSTOM` with the portal authorizer, is a STOP.
    6. AFTER:
       - (a) CodeSha256 equals the zip, and the deployed handler is `7113a749...`;
       - (b) the env is unchanged: 9 key names, 9 values hashing as in step 2b;
       - (c) an unauthenticated POST to EACH new path through CloudFront is refused 401, and to `.../report` and `.../package`
         still 401. If a new path answers anything but 401, STOP, report, and roll back: a route without the authorizer in front
         of it is the one outcome this apply must not leave;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads as in step 2e (no `commentary_sent`, the same draft state);
       - (e) the replan is 0-diff.
    7. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api`. STOP 3: a half-landed record is reported, never hand-edited.
    8. `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r5_ml2/clamp_precheck_table.json`
       (create the folder first). Print its totals line AS IT READS. `READ27 27/27` with the ticket host CLAMPED on the new build is
       the expectation; if its census of ticket routes does not take in the two new routes, or the total changes, say so and
       file ONE row: that is a finding about the precheck, not a STOP.
    9. Close the ledger. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to
       `complete`, write your session log. Report once to `2.0.0_SA_COO~V2`: the deployed handler hash FIRST, the new CodeSha256,
       the four 401s, step 2c's answer, the recorder's commit, the precheck's totals line, and the measured push state.
       UNEXERCISED, and say so: both routes' admissions, every coded refusal of both, and the digest on a real send.

    Finish in session or roll back and say so loudly. Rollback: ONE apply of the build of `f239b06ad8` (handler `c4003667...`)
    with the two route entries removed, same method.
  </go>

  <bounds>
    No env, IAM or permission change. Two routes, no other. No other function. No ticket write, no identity, no token, no mail.
    Never `aws lambda update-function-code`. No client data in any tracked file. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`: two rows already share D2-S43; binary append, line endings kept), never a halt
    on anything but the STOPs above.
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
  <criterion id="AC1" cell_refs="R5-ml-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r5_ml2/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` on the build now live (the issuer's run, 18:45Z). If after the apply the precheck's own
totals line reads a different denominator because it counts the new routes, record the line as it reads and the row of step 8;
the criterion's expectation is then the issuer's to amend, not yours to force.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; the two routes use the existing authorizer and the existing invoke permission).
comp-adversary: RUN -- the four unauthenticated POSTs refused 401 (step 6c), with the BEFORE answers of step 2d as the control that the two new routes did not exist.
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (R5-ml-2) under a signed never-widen pair; not a worker cell.
</task_order>
