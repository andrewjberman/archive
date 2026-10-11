<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-APPLY-R4-pk3.package-door-firm-list-env-dell2</id>
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
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R4.md</decomp_doc> (round 4, AMENDMENT 2): cell `R4-pk-3`, the second apply of `opal-ticket-api` (env only).
<owned_cells>R4-pk-3</owned_cells>
</decomp_ref>

  <objective>
    Set ONE env value on `opal-ticket-api` with ONE `safe-apply` in `infra/aws/terraform/ticket-center`:
    `PACKAGE_ALLOWED_FIRMS = "49financial,cottonwood,inflection"` (today it is present and EMPTY). ENV ONLY: the code does not
    change. After it, the package door admits the one service subject `svc-irpt-packager` for a body firm on that list. The
    resident is not bound to the packager, so nothing calls the door yet.
  </objective>

  <context>
    THIS APPLY IS THE THIRD WRITE OF ANOTHER PROJECT'S PAIR, and both halves of that pair are SIGNED. Read both before any AWS call:
    - packet and COO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_PACKAGER_MINT_20261011.md`
      (blob `5a202040cd`, the bytes the CTO half hashed; its section 5 is the rollback);
    - CTO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_PACKAGER_MINT_CTO_HALF.md` @65622fbcdc
      (the three firms ACCEPTED; "the order is the packet's: grant, mint, both simulates read, THEN the list").
    The condition for cutting this order is met by the CTO's word (msg 5396): "the simulates read as expected, so cut the second
    apply: PACKAGE_ALLOWED_FIRMS = 49financial,cottonwood,inflection." The grant and the mint were the laptop's and are done
    (the secret created 16:43:56Z, the token never read back), by the CTO's reading of the laptop's return; NOT re-read by this
    seat. One sentence of the CTO half is corrected by that same message: the secret is readable by the host's role AND by any
    administrator of the account. That does not change this apply.
    THE ORDERING CONDITION, yours to hold: you also hold `TCKT_VNEXT.TO-RUN-R4-tr1` (the fifth run), which pins this function's
    build and is live against it. **Start this apply only AFTER that run's process has exited and you have sent its step-6
    report.** Its ledger entry may still be OPEN then (the two-hour row wait on return code 3): that one entry is expected and
    is not a STOP for this apply, because its remaining step touches the users table only, never this function. Do not start
    this apply while the runner process is alive.
    The method is the one you used for TO-APPLY-R4-pk2; do not ride `MSYS_NO_PATHCONV=1` on `safe-apply`. This order mints no
    identity, reads no secret, writes no ticket, touches no other function and sends no request anywhere.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO, after the ordering condition. In order:
    0. Open the NEVER-2 ledger entry FIRST. Read EVERY live worktree's `.open_deploys/`, union them and print the per-tree
       denominator. An open entry naming `opal-ticket-api` other than your own AND other than the fifth run's
       (`TO-RUN-R4-tr1`, expected open on return code 3) is a STOP. State in your entry whether the fifth run's was open.
    1. STOP 1 (the pin): `git diff --name-only e9357d6ea0 HEAD -- infra/aws/lambda/ticket_center/lambda_function.py infra/aws/terraform/ticket-center/main.tf`
       is empty BEFORE your own edit. Anything else is a STOP.
    2. BEFORE: the LIVE `opal-ticket-api` CodeSha256 (expect `d2w1YJ8A...`); the deployed `lambda_function.py` sha256 (expect
       `c40036677aae180cb362f89f2c2aecb62ef53fd0b1a285bb3bd2c813176c1026`, from a package download); the env key NAMES and their
       count (expect 9); a sha256 of EACH env value; `PACKAGE_ALLOWED_FIRMS` length (expect 0); `opal-tickets` ItemCount; the
       status fields of `TCK-20261009-a1052909`. A live handler that is not `c4003667...` is a STOP before any plan.
    3. THE ONE EDIT: in `infra/aws/terraform/ticket-center/main.tf`, change the line `PACKAGE_ALLOWED_FIRMS = ""` to
       `PACKAGE_ALLOWED_FIRMS = "49financial,cottonwood,inflection"` and replace its comment with one saying: the firms the
       package principal may attach for, equal to `COMMENTARY_ALLOWED_FIRMS` on purpose (packager mint pair, CTO half
       @65622fbcdc); never `ALL` (the handler drops it). Commit that file alone. No other line changes.
    4. Plan, then `.tools/safe-apply.sh`. Branch A is `0 to add, 1 to change, 0 to destroy`: the function's environment, ONE
       key's value. **If the plan also shows a source_code_hash change, STOP**: the artifact must be the one already live. Any
       other resource or env key in the diff is a STOP. Read the planfile JSON for the key's rendered value, as you did for pk2.
    5. AFTER:
       - (a) CodeSha256 is UNCHANGED (`d2w1YJ8A...`) and the deployed handler is still `c4003667...`;
       - (b) the env has 9 key names; the 8 other values hash the same as in step 2; `PACKAGE_ALLOWED_FIRMS` reads exactly
         `49financial,cottonwood,inflection` (firm ids are not client data; print it);
       - (c) an unauthenticated POST to `/api/scoped/tickets/TCK-20261009-a1052909/package` through CloudFront is refused 401;
       - (d) ItemCount is unchanged and `TCK-20261009-a1052909` reads the same status fields as in step 2;
       - (e) the replan is 0-diff.
    6. RECORD: run `record-terraform-deploy.sh` for `opal-ticket-api` if the method records an env-only apply; if it refuses or
       records nothing because the artifact did not change, say so and do not force it. STOP 3 as before: a half-landed record
       is reported, never hand-edited.
    7. `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_pk3/clamp_precheck_table.json`
       reads `READ27 27/27` (create the folder first).
    8. Close the ledger. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to
       `complete`, write your session log. Report once to `2.0.0_SA_COO~V2` and send the same first line to `2.0.0_SA_COO~G2`:
       the key's value as read live, CodeSha256 unchanged, the env key count, the precheck line, the measured push state. The
       door's admission and its five codes stay UNEXERCISED: say so, and do not call the door.

    Finish in session or roll back and say so loudly. **Rollback (the mint packet's section 5): the list goes back to EMPTY
    first** (`PACKAGE_ALLOWED_FIRMS = ""`, same method), because a minted token stays valid until it expires.
  </go>

  <bounds>
    ENV ONLY, one key. No code, IAM, route or permission change. No other function. No secret read, no token, no ticket write, no
    call of the package door with any identity. Never `aws lambda update-function-code` or `update-function-configuration`. No
    client data in any tracked file. A surprise is ONE row in
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
  <criterion id="AC1" cell_refs="R4-pk-3"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~13/clamp_precheck/clamp_precheck.py --out org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r4_pk3/clamp_precheck_table.json</invocation><expect>READ27 27/27</expect></criterion>
</proof_of_spec>
AC1 at the issuance: `READ27 27/27` (the issuer's live run, 16:45Z); it is a control that the env change did not disturb the
clamp read, not a proof of the list (the list is read in step 5b).

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one apply, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change by this order; the grant on the host's role was the laptop's act under the same pair).
comp-adversary: RUN -- the unauthenticated POST refused 401 (step 5c) and the precheck's 27-route clamp read (step 7).
</preflight>

# pipeline-override: an APPLY order to the dell2 applier for an issuer cell (R4-pk-3) under a signed never-widen pair (IRPT_ANLREQ's packager mint); not a worker cell.
</task_order>
