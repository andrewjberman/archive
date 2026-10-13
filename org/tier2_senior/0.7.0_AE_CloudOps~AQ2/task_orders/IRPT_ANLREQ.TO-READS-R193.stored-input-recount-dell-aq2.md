<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-R193.stored-input-recount-dell-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-13</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read only: Scan/Query/GetItem on the requests table and GetObject on retained artifacts, as the counting script makes them; nothing is changed, deleted, invoked or applied.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN -- by reading the apply record `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ab-2.apply-record.txt` (NFRA_CTLPLN CT-ab-2 COMPLETE: both Dell users are in AdministratorAccessOpalCapital and cloudops-dell-agents-group; the four kept Denies read explicitDeny 4/4 per user; relayed by `2.0.0_SA_COO~C`, msg 7243) and the CTO's msg 7096: whether the group is applied to the identity THIS lane runs as is NOT known to the issuer; step 0 is the dell2 read-back and a missing decrypt is a STOP.
comp-adversary: RUN -- by reading the Y9 and Y10 orders and results against this cell; the lens: a count that names a request or a person, a denied read counted as "reads the same", a count taken before the window and read as if at it. The order requires the read time in the result, a GetObject denial to STOP the run, and no identifier in the result. NOT seen: the real table and bucket (0 live items read by the issuer).
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R22R_Y.md</decomp_doc> round 22, workstream YR round 26: the stored-input recount R0d of the signed r19.3 pair.
<owned_cells>AR-y-241</owned_cells>
</decomp_ref>

  <objective>
    R0d of the signed r19.3 release pair (COO half blob 276cdcc7cc, CTO half @b0eae42e76): ONE read-only run of the counting script of TO-READS-Y9/-Y10, with the reader the release will install (r19.3, sha256 a61cd0c622f8...) as the new reader and the reader live now (r18.1, sha256 83ab9b45d590...) as the old: how many stored upload inputs the r19.3 reader would read differently from the template stored at acceptance, by tenant, and for each it would turn back whether a report was ever generated. COUNTS AND DATES ONLY. Preceded by step 0, dell2's decrypt read-back under the Dell admin group.
  </objective>

  <context>
    Load /cloud-ops first. The Y9 method applies unchanged (org/tier2_senior/0.7.0_AE_CloudOps~ANL/task_orders/IRPT_ANLREQ.TO-READS-Y9.stored-input-count-r18-laptop.md steps 0 to 5 and AMENDMENT 1; its result shape is org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y10_stored_input_count_r19_window.json). The script is org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r16/count_stored_inputs.py (blob 09ddebd883; read it before you run it; any call that writes is a STOP) and its record COUNT_SCRIPT_RECORD.json beside it. Why a Dell lane: kms:Decrypt on the IRPT key was denied to dell2 (Y10 order line 41); no Dell-placed project routes work to a laptop seat (Andrew-direct, msg 6938). The last counts, under r18.1: 56 template inputs (49financial 10, cottonwood 45, inflection 1), 0 turned back, 2026-10-13T00:28:50Z (Y9). Expected now: more inputs, turned back 0.
  </context>

  <the_act>
    RULE 33 (CLAUDE.md, Andrew-direct ~17:4xZ 2026-10-13): every path you post in a report, message or record is ctrl+click accessible: an absolute file:/// URI (forward slashes, a space as %20) or a markdown link to one; a path bound for another box also carries its repo-relative form.
    0. dell2's read-back, in this order, each result in the result file's step0 member (no key material, no object content): (a) the caller identity (`sts get-caller-identity`; record the role or user NAME only); (b) ONE decrypt: `kms:Decrypt`/`DescribeKey` path exercised by reading ONE IRPT-key-encrypted object the script would read anyway (head-object for status, `ServerSideEncryption`, the key ARN's last segment, ContentLength; then the GetObject of that object to /dev/null, bytes counted, nothing kept); (c) the negative control: `iam:SimulatePrincipalPolicy` for your own identity on `s3:DeleteObject` against a production-bucket object ARN, expected `implicitDeny` or `explicitDeny` (a production S3 delete simulates as denied; a simulate that is itself denied is reported as such, not as a pass). Any of (a) to (c) failing to read as stated: STOP, report the status, file a surprise row; the window stays closed.
    1. Y9 step 0 (pre-checks): your checkout carries commit 55d1755d39 (`git cat-file -t`) and the script at blob 09ddebd883 (`git hash-object`); the script's `--self-test` exits 0 in a throwaway worktree detached at 35c3c4bd45 (AMENDMENT 1: the base reader; the self-test takes the checkout's own reader as the old reader). A self-test failure is a STOP.
    2. Write BOTH readers to a folder OUTSIDE the checkout: the old from `git show a665d34dd3:infra/aws/lambda/investor-reporting/intake/template_reader.py` (sha256 must equal 83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58) and the new from `git show 55d1755d39:` at the same path (sha256 must equal a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35).
    3. Resolve the arguments WITHOUT typing a bucket from memory, as under Y7/Y9 (`--table` the requests table; `--bucket` from the `blob.bucket` of ONE artifact row you read; `--region` as before). If the first GetObject is DENIED, STOP and report the error's code.
    4. Run the script ONCE with `--old-reader` and `--new-reader` as above and `--out` outside the checkout. The last stdout line is the one JSON object. A non-zero exit: record the exit code and the one stderr line; no retry with other arguments without reporting.
    5. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r22/R0D_stored_input_count_r193.json: {"read_at", "step0", "count" (the script's object, unchanged), "script_blob", "new_reader_sha256", "old_reader_sha256", "table", "bucket_how_resolved", "identity_arn_tail", "exit_code", "writes_made": [], "reader_version_inputs" (the number of stored template inputs whose stored record names a reader_version, by tenant; if the script does not read that member, read it with the script's own GetItem path in a COPY of the script outside the checkout and say so in not_read), "claim": "measured", "not_read": [...]}. READ it before committing: no request, input, upload or artifact id, file name, ticker, amount, e-mail or link; tenant codes are allowed.
    6. One line first, as soon as step 4 ends, to 2.0.0_SA_COO~Y2 citing this order's path and the push state: template inputs, read differently, turned back, turned back with a report, reader_version_inputs. Then delete the scratch files you made, commit the result and the proof instance, and close your ledger if you opened one.
    Expected: turned back 0. A non-zero turned-back count: STOP, report the number and the tenants to the issuer; the window does not open.
  </the_act>


  <amendments>
    AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-13 ~21:2xZ, after your stop at step 1, msg 7252, row D2-S85; the stop was right and the cause is the issuer's). The script's `--self-test` takes the CHECKOUT's own reader as the old reader (Y9 AMENDMENT 1 said so); at `a665d34dd3` the checkout's reader is the widened r18.1, so the self-test exits 1 there by construction. **Step 1's self-test is met by `--self-test` exiting 0 in a throwaway worktree detached at `35c3c4bd45`** (the base reader, as under Y9), with the script at blob 09ddebd883; record the worktree's commit, the exit code and the reader hash in the result's `step1_self_test` member. The live run's readers are unchanged and explicit: old = `git show a665d34dd3:...template_reader.py` (sha256 83ab9b45...), new = `git show 55d1755d39:...` (sha256 a61cd0c6...), so the checkout's reader plays no part in the count. You have the issuer's word for the ONE live run once step 0 (done), step 1 (i) and (iii) and this self-test pass. Gate limb that graded this amendment: none stated (the issuer amends its own pending order's text).
  </amendments>
  <bounds>
    Read only: Scan / Query / GetItem on the requests table and GetObject on retained artifacts, as the script makes them; sts, kms DescribeKey and iam simulate reads of step 0. No write, no delete, no invoke, no apply, no list call of a bucket, no delete simulated for real. No file content, id, name, holding or address in any file, log or message; no signed link. One run of the script; a second needs the issuer's word.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r22/IRPT_ANLREQ.TO-READS-R193.stored-input-recount-dell-aq2.proof_of_spec.json`.
    <criterion id="R0D-AC1" cell_refs="AR-y-241"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r18/reads9_check.py --result org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r22/R0D_stored_input_count_r193.json</invocation><expect>READS9-OK</expect></criterion>
    <criterion id="R0D-AC2" cell_refs="AR-y-241">The step-0 read-back is recorded: identity, one decrypt with status and key tail, the delete simulation denied.<invocation>grep -cE '"(identity_arn_tail|decrypt_status|delete_simulation)"' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r22/R0D_stored_input_count_r193.json</invocation><expect>^[3-9]$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a Dell READ order under a signed pair (not a worker cell); the cell AR-y-241 is the issuer's, as for TO-APPLY-R20.
