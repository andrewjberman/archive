<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-Y9.stored-input-count-r18-laptop</id>
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
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; no resource is changed by this order.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN -- by reading 2 records: this lane's own TO-READS-Y7 result (it scanned the requests table, 1914 items, and read the retained objects with this identity) and the dell2 applier's refusal (kms:Decrypt on the IRPT key is denied to dell2, which is why this read is the laptop's). Whether the identity still holds the reads is NOT known; step 2 says what to do if it does not.
comp-adversary: RUN -- by reading the script (blob 09ddebd883, the one this lane ran under Y7) and its record against the cell; the lens: an output that carries an id, a file name or a holding, or a denied read counted as "reads the same". NOT seen: the real table and bucket (0 live items read by the issuer).
lane: the applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: READS9-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/IRPT_ANLREQ.TO-READS-Y9.stored-input-count-r18-laptop.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> READS9-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R18_Y.md</decomp_doc> round 18, workstream Y, item 2: the count of stored inputs the repaired reader would turn back (row IRPT_ANLREQ-D2-W52-S29), run by the seat that holds the decrypt.
<owned_cells>AR-y-182</owned_cells>
</decomp_ref>

  <objective>
    ONE READ-ONLY run of the counting script this lane already ran under TO-READS-Y7, now against the reader AS WIDENED by AR-y-181 (READER_VERSION irpt-template-reader.r18.1): how many stored upload inputs
    that reader would read differently from the template stored at their acceptance, by cause, and for each it would turn back whether a report was ever generated from it and when last. COUNTS AND DATES ONLY.
    The Y7 count (56 inputs, 0 read differently) was taken against the round-14 reader; this one is against the reader that will be released. Nothing is written to AWS, deleted, invoked or applied.
    The CTO's round-18 analysis (row S29) asks for exactly this count; each input turned back is then dispositioned by the CTO before the reader's release.
  </objective>

  <context>
    The script and its record are unchanged from Y7: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r16/count_stored_inputs.py` (blob 09ddebd883) and `.../COUNT_SCRIPT_RECORD.json`.
    It reads: a Scan of the requests table for input rows; GetItem of upload and artifact rows; a Query of accepted analysis requests only for a tenant that holds a turned-back input; GetObject (by the key and version each artifact row
    records) of each template input's original and normalized document, and of each such request's composition. It holds file bytes in memory only.
    The two readers it compares: `--old-reader` = the BASE reader (git show 35c3c4bd45:infra/aws/lambda/investor-reporting/intake/template_reader.py, sha256 76795b75313b076488d6c2f0ed7a8480be92b999efb6886a3ede92b11e916409; the reader that wrote the stored templates) and
    `--new-reader` = the widened reader (git show a665d34dd3:infra/aws/lambda/investor-reporting/intake/template_reader.py, sha256 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58). Your checkout's own reader may be either; the order names both files explicitly so it does not matter.
  </context>

  **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-13, after your stop at step 0 (ii); the stop was right and the cause is the issuer's).** The script's `--self-test` takes the CHECKOUT's own reader as the old reader, and your checkout already carries the widened one,
  so it exits 1. The order names both readers explicitly for the live run, so the checkout's reader plays no part there. **Step 0 (ii) is satisfied by the self-test run in a throwaway worktree at `35c3c4bd45` (the base reader) exiting 0**, as you proposed; record the worktree's
  commit, the exit code and the reader hash in the result's `not_read` or a `step0_self_test` member. **You have the issuer's word for the ONE live run** once step 0 (i), (iii) and this (ii) pass. Delete the throwaway worktree afterwards if you created it; deletion of a worktree you made is
  yours to do, and `git worktree remove` of it is not a recursive delete of anyone else's work. Gate limb that graded this amendment: none (the issuer amends its own order).

  <steps>
    0. Pre-checks, STOP and report on any miss: (i) your checkout carries commit a665d34dd3 (`git cat-file -t a665d34dd3`) and the script at blob 09ddebd883 (`git hash-object <script>`); (ii) `python <script> --self-test` exits 0 on your box;
       (iii) read the script before you run it; if you find any call in it that writes, STOP.
    1. Write BOTH readers to a folder OUTSIDE the checkout: the old one from `git show 35c3c4bd45:infra/aws/lambda/investor-reporting/intake/template_reader.py` and the new one from `git show a665d34dd3:` at the same path. Record both sha256 and check they equal the two values above.
    2. Resolve the arguments WITHOUT typing a bucket from memory, exactly as under Y7 (`--table` the requests table; `--bucket` from the `blob.bucket` member of ONE artifact row you read; `--region` as before). If GetObject on the first original is DENIED, STOP and report the error's code.
    3. Run it ONCE: `python <script> --table <T> --bucket <B> --region <R> --old-reader <outside>/old_reader.py --new-reader <outside>/new_reader.py --out <outside>/count.json`. The last stdout line is the one JSON object. If it exits non-zero, record the exit code and the one stderr line; do not retry with other arguments without reporting.
    4. Write `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y9_stored_input_count_r18.json`: `{"read_at": "<UTC>", "count": <the script's JSON object, unchanged>, "script_blob": "09ddebd883", "new_reader_sha256": "<hex>", "old_reader_sha256": "<hex>", "table": "<its name>", "bucket_how_resolved": "<words; NOT the artifact row's id>", "identity_arn_tail": "<the role or user name only>", "exit_code": <n>, "writes_made": [], "claim": "measured", "not_read": [...]}`.
       Before you commit it, READ it: it must hold NO request id, input id, upload id, artifact id, file name, ticker, amount, account value, e-mail address or link. Tenant codes are allowed. The check refuses the rest.
    5. Delete the two reader files and count.json from the folder outside the checkout. Commit the result and the proof instance; report to the issuer citing this order's path, with push state. One line first, as soon as step 3 ends, with the four numbers: template inputs, read differently, turned back, turned back with a report.
  </steps>

<criterion id="READS9-AC1" cell_refs="AR-y-182"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r18/reads9_check.py</invocation><expect>READS9-OK</expect></criterion>
`READS9-AC1`: the result holds the script's twelve members, its counts add up (template inputs = same + differently + unreadable; turned back = with + without a report), names the script blob, both reader hashes, how the bucket was resolved and an empty write list, and holds no id, file name or address.

<expected_criteria>READS9-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - Read only: `Scan` / `Query` / `GetItem` on the requests table and `GetObject` on retained artifacts, as the script makes them. No write, no delete, no invoke, no apply, no list call of a bucket.
    - No file content, id, name, holding or address in any file, log or message. A signed link is never produced by this order.
    - One run. A second run needs the issuer's word.
  </bounds>
</task_order>
