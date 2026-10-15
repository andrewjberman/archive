<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-t34.commentary-logger-and-figures-aq2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-15</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>44</round>
<workstream>~T</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R44_T.md</decomp_doc>
<owned_cells>AR-t-34</owned_cells>
<decomp_context>Round 44, cell AR-t-34: the deploy of AR-t-31 (the figure block), AR-t-32 (the logger level) and AR-t-33 (estate tickers and the request's own model keys), merged at 5b438cd6c4, to the transcripts root's THREE functions. The pair is COMPLETE; this order IS the GO.</decomp_context>
</decomp_ref>

  <objective>
    Rebuild the transcripts zip from the pin and apply it, in ONE targeted apply, to the three functions of the root
    (`aws_lambda_function.pull`, `aws_lambda_function.mail_pull`, `aws_lambda_function.commentary`). No environment value moves.
    Then ONE invoke of `outlook-global-commentary-draft-lambda` for the draft that already exists, which must read stage `draft_exists`
    and leave the function's first INFO line in its log. NO model call. Statuses, hashes and counts only.
  </objective>

  <context>
    The pair binds; read both halves first.
    COO half and packet, AS AMENDED (section 7): `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R42_DEPLOY_PACKET_COMMENTARY_LOGGER_AND_FIGURES_20261015.md`, git blob `e3d5c95826` at commit `dc6a56af94`.
    CTO half, RE-SIGNED: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/R42_DEPLOY_COMMENTARY_LOGGER_AND_FIGURES_CTO_HALF_R2.md` @d82fd93048.
    The pin: box/dell2 `5b438cd6c4`, or a descendant that changes NONE of `data/transcripts/scripts/commentary/lambda_handler.py`, `drafter.py`, `entry.py`.
    KNOWN: the three functions read ONE digest `xC1GDXXp...` (the issuer's read 2026-10-15T19:24Z); the commentary function's timeout is 300 s, memory 512 MB, last modified 2026-10-12T01:04:58Z.
    The on-disk `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip`, if present, is build output and is NOT the rollback artifact (on 2026-10-15 a local `check ca23` read its digest as `HsU4OteP`, which is neither the live digest nor the pin's build). Record its hash, then rebuild.
    No Terraform file changes in this act: the code moves through `source_code_hash` only.
  </context>

  <cto_conditions_verbatim>
    (CTO half RE-SIGNED @d82fd93048, msg 8602) Applier AQ2. The built zip may differ from the fetched live zip in exactly the 3 commentary members, because the zip is shared with the pull functions. The plan reads 0/3/0.
    No invoke is made without a non-null commentary_ref. It runs between Teams-pull fires. Before ~G2 ships figures, a test feeds figures_block a dollar amount, a name and an account id and shows all three dropped: MET by AR-t-33 (0 of 4 planted strings reached the prompt).
  </cto_conditions_verbatim>

  <the_act>
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open a change ledger naming this order, the HEAD you build from, and the three functions that move. Check the clock: the Teams pull fires on the hour
       13:00Z to 22:00Z on weekdays, the mail pull at 23:30Z. Finish clear of a fire, or start after that fire's REPORT line; say which.
    1. PRECONDITION reads, no write: the three functions' CodeSha256 (expected `xC1GDXXp` on all three), LastModified, MemorySize, Timeout; the commentary function's environment (NAMES only, and the value of nothing secret); its event source mapping
       (1, Enabled); its log group's invocation count since 2026-10-15T00:00Z (expected 1, at 17:00:52Z). Print the on-disk dist zip's base64 sha256 if present. Any function NOT on `xC1GDXXp` = STOP and report.
    2. ROLLBACK ARTIFACT: fetch the deployed package from `get-function` (any of the three), store it OUTSIDE the repo, print its base64 sha256: it must read `xC1GDXXp`. Extract it to a directory outside the repo.
    3. BUILD from the pin: `bash infra/aws/lambda/transcripts-pull/build.sh`. Print the new zip's base64 sha256 and member count, the HEAD built from, and that none of the three pinned members differs from `5b438cd6c4`. A difference = STOP.
       DIFF the built zip against the extracted deployed zip: exactly the three members `commentary/lambda_handler.py`, `commentary/drafter.py`, `commentary/entry.py` differ (CTO condition). Any other member differing = STOP, nothing applied, and name it.
    4. ADDRESS EQUALITY on the BUILT zip: extract it outside the repo and run
       `python org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R23_CHECKS/addr_equal.py <extracted deployed zip> <extracted built zip>`; it must print `ADDR-EQUAL-OK teams=14/14 mail=7/7 control=discriminates`. Anything else = STOP.
       ZIP IMPORT on the BUILT zip: `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R2_CHECKS/ar2_t22_zip_import.py` from the repo root (it takes no argument: it runs `build.sh` itself and reads `infra/aws/lambda/transcripts-pull/dist/transcripts-pull.zip`, so run it on the same HEAD as step 3 and re-print the zip hash after it); it must admit a valid analysis_ready and refuse its negative control. Anything else = STOP.
    5. PLAN then APPLY: `safe-apply` in `infra/aws/terraform/transcripts` with exactly `-target=aws_lambda_function.pull -target=aws_lambda_function.mail_pull -target=aws_lambda_function.commentary`.
       The plan: 0 to add, 3 to change, 0 to destroy, and on each of the three only `source_code_hash` (and what follows from it). Any other resource, attribute or environment value = STOP, nothing applied.
    6. AFTER reads: all three CodeSha256 equal the built zip's hash and are not `xC1GDXXp`; MemorySize 1024, 1024, 512 and Timeout 300, 600, 300 unchanged (re-read their values at step 1 first and compare to those, not to these); the commentary function's environment has the same NAMES and every value
       unchanged; its event source mapping still 1, Enabled.
    7. PROOF, driven, ONE invoke and no model call:
       (a) PRECONDITION: invoke `irpt-commentary-draft-store-lambda` with `{"op":"get_ref","tenant":"49financial","request_id":"REQ-d47252fe74634d0c5cdd8067"}` (read-only). It must answer `status OK` with a NON-NULL `commentary_ref`. If it does not: the invoke in (b) is NOT MADE (it would reach the model); report and stop.
       (b) Build the body with the repo's own keys module: `keys.queue_message("analysis_ready", {"tenant": "49financial", "request_id": "REQ-d47252fe74634d0c5cdd8067"})`, ASCII bytes; print the body's length and sha256 (the handler admits only the byte-equal rebuild).
           ONE `lambda invoke` of `outlook-global-commentary-draft-lambda`, `RequestResponse`, payload `{"Records":[{"eventSource":"aws:sqs","messageId":"lg-1","body":<the body>}]}`. Record the time. No retry on any outcome.
       (c) Read the response PARSED: `results[0].stage` must be `draft_exists` and `failed` empty. Then read the function's log since the invoke: the INFO line `commentary draft exists request_id=REQ-d47252fe74634d0c5cdd8067` must be present.
           Any other stage, a non-empty `failed`, or no INFO line is a finding: report it BEFORE the ledger closes and ROLL BACK.
       Side effects of (b), stated: one read-only invoke of IRPT's composition reader by the function; no model call; no write; no queue message; no ticket post.
    8. Close the ledger. If step 5's plan, step 6 or step 7 fails: ROLL BACK in session -- the fetched deployed zip back at the root's zip path, the same three targets re-applied, all three reading `xC1GDXXp` -- and say so.
  </the_act>

  <bounds>
    - Exactly the three function resources, code only. No environment value, IAM, schedule, queue, mapping, reader or secret.
    - Never `aws lambda update-function-code`; never a bare `terraform apply`.
    - No transcript text, mail content, prompt text, draft text, bearer or address in any file or message.
    - No S3 delete. ONE commentary invoke (step 7(b)); no second without the issuer's word. No invoke of either pull.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- the act changes the code behind `teams-global-transcripts-pull-hourly` cron(0 13-22 ? * MON-FRI *) and the mail pull's cron(30 23 * * ? *) (read in the round-23 order); neither rule is touched. The CTO's condition keeps the act between fires.
comp-iam: DECLARED-NOT-APPLICABLE -- code only; no role, policy or grant in the three targets. The applier's reads of the draft store and the one commentary invoke use its identity's existing reach, or the step is NOT MADE.
comp-adversary: RUN -- a rollback artifact mistaken for the on-disk zip (step 2 fetches the deployed bytes); other projects' commits riding the rebuild (step 3's member diff must name exactly three members, step 4 on the BUILT zip with its negative control); an invoke that reaches the model (step 7(a) requires a non-null commentary_ref first); a status compared as captured text (step 7(c) reads parsed values). BLIND: a real draft's `COMMENTARY-POST` line and a 200 from the route, and the figures reaching a real prompt -- UNEXERCISED LIVE until a request whose record names a ticket and whose reader returns figures.
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR34-t-AC1" cell_refs="AR-t-34"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R44_CHECKS/r44_checks.py ap1</invocation><expect>R44-AP1-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states the precondition reads, the rollback artifact's hash, the built hash and HEAD, the member diff, the address-equality and zip-import lines, the plan line, the after reads, the `get_ref` answer, the invoke's parsed stage and the INFO line's presence, and the ledger path.
  Dry-run before the act (issuer, 2026-10-15 ~20:0xZ): `R44-AP1-FAIL a function still runs the pre-act zip (xC1GDXXp)` -- FAIL as expected.

<expected_criteria>AR34-t-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the precondition reads; the rollback artifact's hash; the built hash and HEAD; the member diff; the address-equality and zip-import lines; the plan line; the after reads; the `get_ref` answer, the invoke's parsed stage
    and the INFO line's presence, or NOT MADE; the check line; the ledger path and its closed state; commit hashes (read with an author filter) and the measured push state.
    Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
