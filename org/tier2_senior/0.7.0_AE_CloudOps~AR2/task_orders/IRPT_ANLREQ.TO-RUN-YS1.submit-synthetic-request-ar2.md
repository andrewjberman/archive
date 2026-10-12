<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-YS1.submit-synthetic-request-ar2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AR2</issued_to>
    <date>2026-10-12</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: RUN -- by reading 1 record of the script (`deliverables/0.9.0_WK_IRPT_ANLREQ~53/r16/SUBMIT_SCRIPT_RECORD.json`, key `literal_keys_a_successful_run_would_create`): the kinds a successful run writes are the upload original and normalization records, the retained objects, the resolve message, the normalized input record, the request record, the job item, the composition object and the analysis queue message. The record states what it could NOT read (deployed bytes, live rows, the artifacts bucket, IAM, the resident).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called through the portal; the deployed function is invoked directly, as TO-APPLY-Y75 did. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger is touched.
comp-iam: RUN -- by reading 2 records: the Y75 precedent (a direct invoke of `irpt-ycharts-generate` from this box's CloudOps identity, `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_y75/y75_x1_arms.py`) and the script's own record (what it reads: the filer's users row, a scan of the users table). Whether THIS identity holds `lambda:InvokeFunction` and the two reads today is NOT known; step 0 says what to do if it does not.
comp-adversary: RUN -- by reading the CTO's ruling (msg 6575, section 7 of `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_DELL2_RELAUNCH_THREE_ASKS_READ_AND_RULED_20261012.md`) against the script; the lens: a request owned by a real person. The script refuses to invoke unless the resolved advisor is on a reserved domain, and the self-test shows it (22 of 22 arms). NOT seen: the live users table and the deployed function.
lane: this applier's own deliverables and logs; the world write is the script's, bounded below.
</preflight>
<proof_of_spec>
Criterion id: RUNYS1-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/IRPT_ANLREQ.TO-RUN-YS1.submit-synthetic-request-ar2.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> RUNYS1-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R16D_Y.md</decomp_doc> workstream YS, the direct act of CTO msg 6575: the script is cell AR-y-166 (drained @07c7b3463c); this order is its one run.
<owned_cells>AR-y-166</owned_cells>
</decomp_ref>

  <objective>
    Run ONE existing script, ONCE to completion (several passes only while the upload is still resolving), that files ONE synthetic analysis
    request in tenant `cottonwood`, as the project's existing synthetic filer, naming the ticket `TCK-20261012-13cd3a1d` that
    `2.0.0_SA_COO~V2` filed. The request exists so the NFRA_TRNSPT round-24 driven draft has an accepted request whose record carries a
    ticket id. No identity is minted, no users row is written, nothing is deleted afterwards (a delete is a human act).
  </objective>

  <context>
    Ruled by `1.0.0_SA_CTO~DELL2`, msg 6575 and msg 6588, section 7 of the document above: the existing synthetic filer, synthetic holdings,
    the write set listed in the script's record, nothing deleted after. The script and its record:
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r16/submit_synthetic_request.py` (read it first; 516+ lines, ASCII)
    and `.../r16/SUBMIT_SCRIPT_RECORD.json`. Its modes: `--plan`, `--self-test`, `--run`. `--run` reads the filer's users row and STOPS before any
    invoke if it does not list `cottonwood`; resolves the advisor named by an opaque label among ACTIVE cottonwood users and STOPS before any
    invoke unless that address is on a reserved domain; invokes the deployed `irpt-ycharts-generate` for the on-behalf upload, and, only when the
    answer carries an `input_id`, a second time for the submission. Upload and request ids are fixed per ticket, so a re-run reads the same upload.
    The upload answers RESOLVING first (a resident resolves the tickers); the script then stops, and a later pass reaches the submission.
  </context>

  <steps>
    0. Pre-checks, STOP and report on any miss: (i) `git hash-object` of the script equals `326f2909559410750481fc65cdd84fe45262fc95`;
       (ii) `python <script> --self-test` exits 0 and prints `SUBMIT-SELFTEST-OK`; (iii) your identity may invoke `irpt-ycharts-generate`
       and read the users table (`iam simulate-principal-policy` on your own ARN for `lambda:InvokeFunction`, `dynamodb:GetItem`,
       `dynamodb:Scan`; state the result); (iv) no open deploy-ledger entry names `irpt-ycharts-generate` in ANY
       live worktree (`git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`; print
       the denominator). An open entry naming it is a STOP: no invoke while an apply is in flight. If (iii) fails, STOP and say so: the issuer
       then routes the run to the seat that holds the access.
    1. Choose the advisor, in memory only: scan the users table; take the ACTIVE users whose firm is `cottonwood` and whose address is on a
       RESERVED domain (the part after the last at-sign, lower-cased, equal to `example.com`, `example.org` or `example.net`, or ending
       `.invalid`, `.test` or `.example`). Record ONLY their COUNT. If the count is 0, STOP: no identity is minted to supply one. Otherwise
       take the first by sorted address and compute its opaque label `adv-` plus the first 12 hex of the sha256 of the lower-cased address.
       Never print, write or log the address.
    2. Run: `python <script> --run --tenant cottonwood --ticket TCK-20261012-13cd3a1d --i-have-the-ctos-word msg-6575 --advisor-opaque <label>`.
       Capture its stdout. Record each pass: time, the printed state and where it stopped. If it stops with `STOP: the upload answer carries no
       upload id`, or the filer row does not admit cottonwood, or the advisor is not synthetic, END the run: do not edit the script, do not
       retry with other arguments, report the printed STOP line.
    3. If it stops because there is no `input_id` (the upload is still RESOLVING), wait five minutes and run the SAME command again. At most
       EIGHT passes in all. If the upload answers `NEEDS_CORRECTION`, or the eighth pass still has no `input_id`, END the run and report the
       state. NEVER run the submission event by hand and NEVER send a second, different upload.
    4. On `RUN-OK` (the submission was accepted): write
       `org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/SUBMIT_RUN_RESULT.json` =
       `{"ran_at": "<UTC>", "tenant": "cottonwood", "ticket_id": "TCK-20261012-13cd3a1d", "passes": [{"at": "<UTC>", "state": "<printed>",
       "stopped_at": "<printed or null>"}...], "final": "ACCEPTED" | "STOPPED: <reason>", "ids": {"upload_id": "...", "input_id":
       "portfolio_<64 hex>", "request_id": "REQ-<24 hex>"}, "filer_row_admits_cottonwood": <bool>, "advisor_domain_class": "reserved",
       "reserved_advisors_counted": <n>, "identity_arn_tail": "<role or user name only>", "literal_keys_created": [{"kind": "...", "id":
       "..."}...], "writes_made": ["<kind>"...], "claim": "measured", "not_read": [...]}`. `request_id` is the id the ACCEPTANCE minted (the
       `REQ-` form, read from the answer's identity), NOT the client's `anlreq-y166-...` token; if the printed id is not of that form, say so
       in `not_read` and put what the answer carried. `literal_keys_created` lists the kinds the script's record names, with the ids you can
       read from the answers (upload id, input id, request id); say what you could not read. A STOPPED result is also written, with `ids`
       empty. Before you commit, READ the file: no address, no link, no body, no holding value.
    5. Commit the result and the proof instance; report to the issuer citing this order's path, with push state. One line first: the final
       state, the request id (or the STOP line) and the number of passes.
  </steps>

<criterion id="RUNYS1-AC1" cell_refs="AR-y-166"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r16/runys1_check.py</invocation><expect>RUNYS1-OK</expect></criterion>
`RUNYS1-AC1`: the result is complete and consistent (an ACCEPTED result carries a `REQ-<24 hex>` request id, an `portfolio_<64 hex>` input id and the kinds written; a
STOPPED result carries its reason and no request id), names the ticket V2 filed, and holds no address or link.

<expected_criteria>RUNYS1-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~AR2/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - The world write is exactly the script's `--run`: at most two invokes of `irpt-ycharts-generate` per pass (the on-behalf upload, then the
      submission), plus reads of the users table. The CTO's conditions bind: synthetic holdings (the script's own CSV), the write set is the
      literal keys the run creates (listed in your result), the draft posts only to that ticket, NOTHING IS DELETED AFTERWARDS.
    - No users row, token, grant or identity is made. No second ticket, no second request, no edit of the script. No address, link, holding or
      file body in any file, log or message.
    - A refusal or error is reported with its printed line and NOT worked around. Only the issuer rules a second approach.
  </bounds>
</task_order>
