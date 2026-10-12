<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-Y7.stored-input-count-laptop</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ANL</issued_to>
    <date>2026-10-12</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; no resource is changed by this order. comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger. comp-iam: RUN -- by reading 2 records: the dell2 applier's refusal (kms:Decrypt on the IRPT key is denied to dell2; TO-APPLY-Y6 step 0) and the laptop's TO-READS-Y6 result (it scanned the requests table, 1904 items, and read job rows); whether the laptop identity holds s3:GetObject on the retained artifacts is NOT known, and step 2 says what to do if it does not.
comp-adversary: RUN -- by reading 1 script of 1 file at its drain (blob c5481b8768; the cell's check refuses seven write-call strings in it and passed) and its self-test run by the issuer (11 synthetic inputs, exit 0); the lens: an output that carries an id, a file name or a holding, or a denied read counted as "reads the same". The script counts a denied read as unreadable by its code; this order's check refuses a result holding an id, a file name or an address. NOT seen: the real table and bucket.
lane: the applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: READS7-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/IRPT_ANLREQ.TO-READS-Y7.stored-input-count-laptop.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> READS7-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R16_Y.md</decomp_doc> round 16, workstream ~Y, item 1: the count, run by the seat that holds the decrypt.
<owned_cells>AR-y-161</owned_cells>
</decomp_ref>

  <objective>
    ONE READ-ONLY run, from the laptop, of a counting script this lane built and proved offline: how many stored upload inputs a
    NEW upload reader would read differently from the template stored at their acceptance, by cause; and, for each one it would
    turn back, whether a report was ever generated from it and when last. COUNTS AND DATES ONLY. Nothing is written to AWS,
    deleted, invoked or applied. The count goes to the CTO, who rules on it before the reader is re-landed (CTO msg 6304).
  </objective>

  <context>
    The new reader was built, found unsafe for stored inputs, and taken off the trunk (revert 114c77fb01). Its bytes are still in
    history at commit d95cf11106. PRD v0.4 (CONTRACT C-STOREDINPUT) repairs the re-read; the count is item 1 of its round-16 list.
    The script and its record (read the record first):
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r16/count_stored_inputs.py` (blob c5481b8768) and
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r16/COUNT_SCRIPT_RECORD.json`.
    It reads: a Scan of the requests table for input rows; GetItem of upload and artifact rows; a Query of accepted analysis
    requests only for a tenant that holds a turned-back input; GetObject (by the key and version each artifact row records) of
    each template input's original and normalized document, and of each such request's composition. It holds file bytes in
    memory only.
  </context>

  **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-12 ~03:0xZ): the script is FIXED and you have the issuer's word for ONE rerun.**
  Your first run stopped at step 3, exit 3, `SCAN_FAILED ValidationException`, before any item was read; you edited nothing and did
  not retry: right. The fault was the issuer's cell: the scan's projection named an attribute bare, and `identity` is a reserved
  word. THE CAUSE IS INFERRED, not confirmed -- nobody on dell2 can run the scan. The fix: every projected attribute now goes
  through a name placeholder. **The script's blob is now `09ddebd883`** (everywhere this order says `c5481b8768`, read `09ddebd883`,
  in step 0's hash check and in the result's `script_blob`). Run steps 0 to 5 again, ONCE. If step 3 fails again, record the exit
  code and the stderr line, and ALSO the request's own error message text if the script prints it (it names the offending
  expression; it holds no data): do not edit the script and do not retry. Gate limb that graded this amendment: this commit's own
  output is the read.

  <steps>
    0. Pre-checks, STOP and report on any miss: your checkout carries the script at blob c5481b8768
       (`git hash-object <script>`); `python <script> --self-test` exits 0 on your box; your checkout's
       `infra/aws/lambda/investor-reporting/intake/template_reader.py` is the OLD reader
       (`git diff 35c3c4bd45 HEAD -- infra/aws/lambda/investor-reporting/intake/template_reader.py` prints nothing).
       Read the script before you run it; if you find any call in it that writes, STOP.
    1. Write the new reader to a folder OUTSIDE the checkout:
       `git show d95cf11106:infra/aws/lambda/investor-reporting/intake/template_reader.py > <outside>/new_reader.py`. Record its sha256.
    2. Resolve the arguments WITHOUT typing a bucket from memory: `--table` is the requests table you scanned under TO-READS-Y6;
       `--bucket` is the bucket named by the `blob.bucket` member of ONE artifact row you read (record HOW you resolved it, not
       a guess); `--region` as your earlier reads. If `GetObject` on the first original is DENIED, STOP: record the error's code
       and report; a denied read is never a count.
    3. Run it ONCE: `python <script> --table <T> --bucket <B> --region <R> --new-reader <outside>/new_reader.py --out <outside>/count.json`.
       The last stdout line is the one JSON object. If it exits non-zero, record the exit code and the one stderr line that
       names the failure; do not retry with other arguments without reporting.
    4. Write `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y7_stored_input_count.json`:
       `{"read_at": "<UTC>", "count": <the script's JSON object, unchanged>, "script_blob": "c5481b8768", "new_reader_sha256":
       "<hex>", "old_reader_sha256": "<hex of your checkout's reader>", "table": "<its name>", "bucket_how_resolved": "<words; NOT
       the artifact row's id>", "identity_arn_tail": "<the role or user name only>", "exit_code": <n>, "writes_made": [],
       "claim": "measured", "not_read": ["<what the run could not read, by error code and count>"]}`.
       Before you commit it, READ it: it must hold NO request id, input id, upload id, artifact id, file name, ticker, amount,
       account value, e-mail address or link. Tenant codes (a firm's code) are allowed. The check refuses the rest.
    5. Delete `<outside>/new_reader.py` and `<outside>/count.json`. Commit the result and the proof instance; report to the issuer
       citing this order's path, with push state. One line first, as soon as step 3 ends, with the four numbers: template inputs,
       read differently, turned back, turned back with a report.
  </steps>

<criterion id="READS7-AC1" cell_refs="AR-y-161"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r16/reads7_check.py</invocation><expect>READS7-OK</expect></criterion>
`READS7-AC1`: the result holds the script's twelve members, its counts add up (template inputs = same + differently + unreadable;
turned back = with + without a report), names the script blob, both reader hashes, how the bucket was resolved and an empty write
list, and holds no id, file name or address.

<expected_criteria>READS7-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - Read only: `Scan` / `Query` / `GetItem` on the requests table and `GetObject` on retained artifacts, as the script makes them.
      No write, no delete, no invoke, no apply, no list call of a bucket.
    - No file content, id, name, holding or address in any file, log or message. A signed link is never produced by this order.
    - One run. A second run needs the issuer's word.
  </bounds>
</task_order>
