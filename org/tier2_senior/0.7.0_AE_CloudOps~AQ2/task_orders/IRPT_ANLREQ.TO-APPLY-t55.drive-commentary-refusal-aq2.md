<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-t55.drive-commentary-refusal-aq2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-16</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>57</round>
<workstream>~T</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R57_T.md</decomp_doc>
<owned_cells>AR-tf-78</owned_cells>
<decomp_context>Round 57, cell AR-tf-78: drive ONE real hop failure on purpose, the COMMENTARY hop, on an existing synthetic job row, leave it in place until the ticket page is read by 2.0.0_SA_COO~V2, then restore the row. No deploy: the writer and the function are live since TO-APPLY-t54.</decomp_context>
</decomp_ref>

  <objective>
    ONE direct invoke of the live commentary function with a record whose body is REFUSED, naming the synthetic request below, so that the live `fail` op sets `hop_failure` = {COMMENTARY, COMMENTARY_DRAFT_REFUSED, at} on that ONE job row (LEG A). The failure STAYS on the row while `2.0.0_SA_COO~V2` reads the ticket page. On the issuer's message (LEG B) remove that one attribute again and read it absent. No model call, no queue message, no generation. Statuses, hashes and counts only.
  </objective>

  <context>
    Authority: the CTO's round analysis `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_TICKET_ROUND_3_20261016.md` @90926d9683, ruling 1 (round 4 drives ONE real hop failure deliberately, with the applier as needed; the hop and input are V2's choice with G2 and T2; the writer must be live), and Andrew's 2026-10-16 word on synthetic objects (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md` @c2b2f1e950). The same write was proven inside TO-APPLY-t54 step 6 under the signed pair R54 (writer, function, row). V2's request: msgs 9513 and 9521; the request was cleared as free by `2.0.0_SA_COO~Y2` (msg 9518); its ticket `TCK-20261015-944c84f8` was read by V2 (no package).
    THE ROW: table `irpt-jobs`, key tenant `49financial`, job `REQ-d47252fe74634d0c5cdd8067` (the accepted request of the earlier FWD-1 run, filed by the synthetic staff user `fwd1-staff-r41b`; state READY; t54 restored it with no `hop_failure`).
    KNOWN (issuer, 2026-10-16 ~15:3xZ): the commentary function runs digest `I/6mirBT...` (t54 artifact 3); the draft-store Lambda `RizVjaXi...`; the refused-body branch is `data/transcripts/scripts/commentary/lambda_handler.py` (refusal, then `_report_hop_failure` with the ids parsed from the body); the function's log line on success is `HOP-FAILURE-REPORTED request_id=<id> hop=COMMENTARY code=COMMENTARY_DRAFT_REFUSED written=True`.
  </context>

  <the_act>
    LEG A (now):
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open ONE change ledger naming this order and the single row it touches; it stays OPEN across both legs and closes at the end of leg B.
    1. PRECONDITION reads, no write (STOP on any mismatch, name it): the commentary function's CodeSha256 (`I/6mirBT...`), the draft-store Lambda's (`RizVjaXi...`); the job row EXISTS with state READY and `hop_failure` ABSENT; record the sha256 of the item as returned (this is PRE); the ticket `TCK-20261015-944c84f8` carries NO package pointers (read its record read-only; any package pointer = STOP, nothing written). Run `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R55_CHECKS/r55_checks.py hopabsent`: it must print `R55-HOPABSENT-OK`.
    2. THE INVOKE, ONE `lambda invoke` of `outlook-global-commentary-draft-lambda`, `RequestResponse`, payload `{"Records":[{"eventSource":"aws:sqs","messageId":"t55-1","body":"{\"kind\":\"t55_forced_refusal\",\"tenant\":\"49financial\",\"request_id\":\"REQ-d47252fe74634d0c5cdd8067\"}"}]}` (the body is NOT the canonical `analysis_ready` bytes, so the handler refuses it as WRONG_KIND and reports the hop failure from the ids it reads in the body). Record the UTC time. No retry on any outcome. Read the response PARSED: `results` empty, `failed` holding one entry with reason `WRONG_KIND`, `batchItemFailures` naming `t55-1` (it is a direct invoke: no SQS message exists, so nothing is redelivered and no dead-letter entry is made; say so).
    3. READ BACK: the function's log since the invoke holds the line `HOP-FAILURE-REPORTED request_id=REQ-d47252fe74634d0c5cdd8067 hop=COMMENTARY code=COMMENTARY_DRAFT_REFUSED written=True`; `get-item` of the row: `hop_failure` = {hop COMMENTARY, code COMMENTARY_DRAFT_REFUSED, at a UTC stamp}, state READY unchanged, every other attribute unchanged (sha256 of the item without `hop_failure` equals PRE). Run `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R55_CHECKS/r55_checks.py hoplog`: it must print `R55-HOPLOG-OK`.
    4. REPORT LEG A to 2.0.0_SA_COO~T2 NOW, with the UTC moment the row read failed and the `at` value; the issuer relays it to `2.0.0_SA_COO~V2` at once. Do NOT remove the attribute. Leave the ledger OPEN and wait for the issuer's message citing this order (leg B). If the invoke's answer or the row read differs from the above: do not invoke again, do not remove, report it and wait.
    LEG B (only on the issuer's message citing this order after V2's page read, or on a STOP/abort word from the issuer):
    5. Record the written `hop_failure` value, then remove ONLY that attribute from that ONE row with a conditional update (condition: its `code` equals the recorded one); read it back ABSENT and the item sha256 equal to PRE. Run `r55_checks.py hopabsent`: `R55-HOPABSENT-OK`.
    6. Close the ledger; write the proof instance beside this order in `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/` (not in a subfolder: the flip gate looks there); report once more.
  </the_act>

  <bounds>
    - ONE invoke, ONE row, ONE attribute, one leg at a time. No other function, row, table, queue, key, schedule or secret. No `put-item` or `delete-item` on `irpt-jobs`; no `aws lambda update-function-code`; no Terraform.
    - The failure stays on the row until the issuer's leg-B message; the time is V2's page read, not yours. If the ledger window would lapse before leg B, say so to the issuer; do not remove on your own.
    - No transcript text, mail content, prompt text, draft text, bearer or address in any file or message.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, trigger, mapping or code moves; one direct invoke of a function whose zip is unchanged.
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the applier's invoke and its reads/updates of one synthetic row use its identity's existing reach, or the step is NOT MADE.
comp-adversary: RUN -- a body that accidentally equals the canonical analysis_ready bytes (it would start a draft and reach the model; the body here carries a different `kind` and is refused before any read); a retry or a second invoke (forbidden); removal before V2's page read (leg B waits for the issuer's message); a package attached to the request's ticket (precondition 1 STOPs); a hop_failure already on the row (precondition 1 STOPs, the writer is set-once); a row removed or created by mistake (the writer's condition needs the row to exist; only one conditional REMOVE is allowed).
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR78-tf-AC1" cell_refs="AR-tf-78"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R55_CHECKS/r55_checks.py hoplog</invocation><expect>R55-HOPLOG-OK</expect></criterion>
  <criterion id="AR78-tf-AC2" cell_refs="AR-tf-78"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R55_CHECKS/r55_checks.py hopabsent</invocation><expect>R55-HOPABSENT-OK</expect></criterion>
</proof_of_spec>
  AC1 (the driven failure was reported by the live function) reads FAIL at the base (`R55-HOPLOG-FAIL events_with_line=0`) and OK after leg A. AC2 is the restore control: it reads OK at the base (`R55-HOPABSENT-OK row exists, hop_failure absent`) and must read OK after leg B; the instance records the row's `hop_failure` value, `at` and the READY state read between the legs. The checker's `--self-test` reads `R55-SELFTEST-OK`.

<expected_criteria>AR78-tf-AC1,AR78-tf-AC2</expected_criteria>

  <report>
    LEG A report to 2.0.0_SA_COO~T2 (statuses only): the precondition reads and PRE hash; the invoke's time and parsed answer; the log line's presence; the row after (hop_failure keys and `at`, state, the item hash without the attribute); the check lines; the ledger id (OPEN). LEG B report: the recorded value, the conditional REMOVE, the read-back ABSENT and the PRE-equal hash; the check lines; the ledger CLOSED; commit hashes (read with an author filter) and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
