<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-sa23.route-switch-front-door-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-12</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>23</round>
<workstream>routeswitchapply</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R23.md</decomp_doc>
<owned_cells>TR-sa-23</owned_cells>
<decomp_context>Round 23 AMENDMENT 2, cell TR-sa-23: the deploy of TR-sw-23 (the drafter posts its draft to the request's own ticket; drained @2fab656082, fix @c942202bf9) to the transcripts root's THREE functions, AND the commentary function's ticket base moved to the portal's front door. The pair is COMPLETE; this order IS the GO.</decomp_context>
</decomp_ref>

  <objective>
    Rebuild the transcripts zip and apply it, in ONE targeted apply, to all three functions of the root
    (`aws_lambda_function.pull`, `aws_lambda_function.mail_pull`, `aws_lambda_function.commentary`), together with ONE environment
    value on the commentary function: `TICKET_API_BASE` becomes the portal's front door. Then ONE invoke of each pull, and ONE
    probe post through the front door with the service bearer. NO invoke of the commentary function. Statuses, hashes and counts only.
  </objective>

  <context>
    The pair binds; read both halves first.
    COO half and packet, AS AMENDED (ADDENDUM 1 replaces section 4 step (c)):
    `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_SA23_ROUTE_SWITCH_DEPLOY_PACKET_20261012.md`, sha256 beginning
    `56d489bdfea6085f` (it began `9f52013cc34cb1c6` when the CTO signed; the only difference is ADDENDUM 1, the CTO's own change).
    CTO half, SIGNED: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_TR_SA_23_ROUTE_SWITCH_20261012.md` @ee3efa0504.
    The pin: box/dell2 `c942202bf9`, or a descendant that changes NONE of `data/transcripts/scripts/commentary/lambda_handler.py`,
    `ticket_client.py`, `post_census.py`.
    KNOWN at step 1: the on-disk `dist/transcripts-pull.zip` hashes `xC1GDXXp...` (the issuer's read, 2026-10-12T00:5xZ). It does NOT
    equal the live digest and is NOT the rollback artifact. Record its hash, then rebuild.
    The Terraform edit is YOURS (the issuer's lane cannot write it): `infra/aws/terraform/transcripts/commentary.tf` line 72, the one
    token `.api_base` becomes `.portal_base` (both are members of `integrations/ticketing/intake/runner_config.json`); bring the
    comment above it into line. Nothing is typed. `local.commentary_ticket_api_base` has one consumer, line 296.
  </context>

  <cto_conditions_verbatim>
    (CTO half SIGNED @ee3efa0504)
    **Step (c) as signed:** ONE post with the service bearer to the same made-up ticket path, with a body carrying ONE EXTRA KEY
    beside the two. The route checks the caller, then the body's keys, before it reads any ticket (`:1543-1550`).
    - **400, `application/json`, naming the unexpected field: the service is admitted through the front door.** This is the pass.
    - 403 `application/json`: the bearer passed the gateway and the route does NOT admit it. A finding; the base is rolled back.
    - 401, an HTML answer, or a 5xx: the front door or the gateway did not carry it. A finding; the base is rolled back.

    It reads no ticket and writes nothing. The bearer is never printed; a denied secret read is NOT MADE, no grant sought.

    Conditions
    1. The plan is exactly three changes as section 5 names them; anything else is a STOP with nothing applied.
    2. Step (d) stands: no invoke of the commentary function with any event.
    3. Each expected status is read from a PARSED value, not from a captured output compared whole (the near-rollback of
       TCKT_VNEXT round 7).
    4. The act clears the scheduled fires as section 5 says.
  </cto_conditions_verbatim>

  <the_act>
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open a change ledger naming this order, the HEAD you build from, the
       three functions that move and the one environment value. Check the clock (condition 4): the Teams pull fires on the hour
       13:00Z to 22:00Z on weekdays, the mail pull at 23:30Z. Finish clear of a fire, or start after that fire's REPORT line; say which.
    1. PRECONDITION reads, no write: the three functions' CodeSha256 (expected `auyn4IvltKLLl6yw+SsMWGi3VVlYZKnmJKFssjJaVNY=` on all
       three), LastModified, MemorySize, Timeout; the commentary function's whole environment (NAMES only, plus the value of
       `TICKET_API_BASE`, expected the `api_base` of the runner config); its event source mapping (1, Enabled) and its invocation
       count in the log since 2026-10-12T00:00Z. Print the on-disk dist zip's base64 sha256. Any function NOT on `auyn4Ivl...` =
       STOP and report.
    2. ROLLBACK ARTIFACT: fetch the deployed package from `get-function` (any of the three), store it OUTSIDE the repo, print its
       base64 sha256: it must read `auyn4Ivl...`. Extract it to a directory outside the repo.
    3. The Terraform edit of the context paragraph, committed in your lane. Then BUILD:
       `bash infra/aws/lambda/transcripts-pull/build.sh`. Print the new zip's base64 sha256 and member count, the HEAD built from, and
       that none of the three pinned members differs from `c942202bf9`. A difference = STOP.
    4. ADDRESS EQUALITY on the BUILT zip: extract it outside the repo and run
       `python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/addr_equal.py <extracted deployed zip> <extracted built zip>`.
       It must print `ADDR-EQUAL-OK teams=14/14 mail=7/7 control=discriminates`. Anything else = STOP, nothing applied.
    5. PLAN then APPLY (condition 1): `safe-apply` in `infra/aws/terraform/transcripts` with exactly
       `-target=aws_lambda_function.pull -target=aws_lambda_function.mail_pull -target=aws_lambda_function.commentary`.
       The plan: 0 to add, 3 to change, 0 to destroy. On `.pull` and `.mail_pull` only `source_code_hash` and what follows from it.
       On `.commentary` `source_code_hash` and the ONE environment value `TICKET_API_BASE`, whose new value equals the runner
       config's `portal_base`. Any other resource, attribute or environment value = STOP, nothing applied.
    6. AFTER reads: all three CodeSha256 equal the built zip's hash; MemorySize 1024, 1024, 512 and Timeout 300, 600, 300
       unchanged; the commentary function's environment has the same NAMES as step 1 and only `TICKET_API_BASE` differs in value;
       its event source mapping still 1, Enabled; its log shows NO new invocation across the act.
    7. PROOF, driven:
       (b) ONE invoke of `teams-global-transcripts-pull-lambda` and ONE of `outlook-global-transcripts-pull-lambda`, graded as in
           TO-APPLY-ca23 step 7. A landing by either is reported with its series and count BEFORE the ledger closes.
       (c) The probe exactly as the CTO signed it (the block above): ONE post to
           `<portal_base>/api/scoped/tickets/PROBE-NOSUCH-0/commentary-draft`, bearer from `opal/ticketing/svc-commentary` (`.token`),
           body `{"draft_commentary": {"text": "probe", "model": "probe", "generated_at": "2026-10-12T00:00:00Z", "status": "DRAFT"},
           "request_id": "PROBE-NOSUCH-0", "probe_extra_key": true}`. Read the status INTEGER and the content type as parsed values.
           Report the status, the content type and whether the body names the unexpected field; never the bearer.
           PASS = 400 `application/json` naming the field. 403, 401, HTML or 5xx = a finding: report it and ROLL BACK THE BASE.
           The secret read denied = step (c) NOT MADE, no grant sought; say so, and do not roll back on that alone.
       (d) NO invoke of `outlook-global-commentary-draft-lambda`, with any event.
    7(c)-AMENDMENT 1 (issuer, 2026-10-12, on the applier's finding msg 6251 and row NFRA_TRNSPT-D2-S33): the made-up id
       `PROBE-NOSUCH-0` fails the ticket service's own id pattern (`infra/aws/lambda/ticket_center/lambda_function.py:156`,
       `^TCK-\d{8}-[0-9a-f]{8}$`) at its dispatcher, so the first post read the service's 404 `no route` and none of the three
       signed branches was reachable. An issuer defect in the packet. The base is not implicated and is NOT rolled back.
       ONE more post, and no third: the same call with the id `TCK-00000000-00000000`, the same body with the extra key. The
       extra-key check (`:1550`) runs before any ticket read, so nothing is read or written whatever that id names. Grade it on
       the CTO's three signed branches, by parsed status and content type. 400 `application/json` naming the field = the pass:
       close the ledger. Anything else = report before acting.
    8. Close the ledger. If step 6, 7(b) or 7(c) fails: ROLL BACK in session -- the fetched deployed zip back at the root's zip path,
       the line-72 token reverted, the same three targets re-applied, all three reading `auyn4Ivl...` and the base reading the
       runner config's `api_base` -- and say so.
  </the_act>

  <bounds>
    - Exactly the three function resources: code, plus the one environment value. No IAM, schedule, queue, mapping, reader or secret.
    - Never `aws lambda update-function-code`; never a bare `terraform apply`.
    - No transcript text, mail content, prompt text, bearer or address in any file or message.
    - No S3 delete. No second invoke of either pull without the issuer's word. Probe posts: the first, and the ONE of 7(c)-AMENDMENT 1; no third.
    - No invoke of the commentary function.
  </bounds>

  <paths>
    infra/aws/terraform/transcripts/commentary.tf
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TR2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- the act changes the code behind `teams-global-transcripts-pull-hourly` cron(0 13-22 ? * MON-FRI *) and the mail pull's cron(30 23 * * ? *); neither rule is touched. Condition 4 keeps the act clear of a fire.
comp-iam: DECLARED-NOT-APPLICABLE -- code and one environment value; no role, policy or grant in the three targets. The applier's own read of the ticket secret is its identity's existing reach or NOT MADE.
comp-adversary: RUN -- a probe that cannot tell an admitted service from a refused one (the CTO's change: the extra key reads 400 only past the caller check); a status compared as captured text (condition 3: parsed integer); other projects' naming commits riding the rebuild (step 4 on the BUILT zip, negative control); the on-disk zip mistaken for the rollback artifact (step 2 fetches the deployed bytes); a second environment value moving with the base (step 6 compares the NAMES and every other value); an invoke of the commentary function used as proof, which would call the outside model (forbidden). BLIND: a real draft's post and a 200 from the route -- UNEXERCISED LIVE until the upstream chain sends a request whose record names a ticket; the stream path's create through the front door.
lane: the applier's deliverables, logs, the change ledger, and the one Terraform file.
</preflight>

<proof_of_spec>
  <criterion id="TR23-sa23-AC1" cell_refs="TR-sa-23"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/r23_checks.py sa23</invocation><expect>R23-SA23-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states the precondition reads, the rollback artifact's hash, the built hash, the address-equality line, the plan
  line, the after reads, both invokes' results, the probe's parsed status and content type, and the ledger path.
  Dry-run before the act: `R23-SA23-FAIL a function still runs the pre-act zip` -- FAIL as expected.

<expected_criteria>TR23-sa23-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the precondition reads; the rollback artifact's hash; the built hash and HEAD; the address-equality
    line; the plan line; the after reads; both invokes' status and counts; the probe's parsed status and content type, or NOT MADE;
    the check line; the ledger path and its closed state; commit hashes (read with an author filter) and the measured push state.
    Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
