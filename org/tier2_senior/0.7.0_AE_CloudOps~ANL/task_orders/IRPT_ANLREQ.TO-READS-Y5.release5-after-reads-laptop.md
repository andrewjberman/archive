<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-Y5.release5-after-reads-laptop</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ANL</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; no resource is changed by this order. comp-routes: DECLARED-NOT-APPLICABLE -- no route changes; R6 re-reads the /original route as revision 6's reads did. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger. comp-iam: RUN (by reading) -- these are the reads the same laptop identity made on revision 6 (TO-AR-y-34, result committed 1ebd6f6e0e); no new permission is asked. comp-adversary: DECLARED-NOT-APPLICABLE -- the order produces evidence and decides nothing; a false read is reported, never retried into a pass (step 8).
lane: the applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: READS5-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/IRPT_ANLREQ.TO-READS-Y5.release5-after-reads-laptop.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> READS5-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R3_Y.md</decomp_doc> round 3, workstream ~Y, release 5: the after-reads of cell `AR-y-32`.
<owned_cells>AR-y-32</owned_cells>
</decomp_ref>

  <objective>
    The after-reads R2 to R7 of IRPT_ANLREQ release 5 (`irpt-status` build `Iw3FADFrSt5G97zRTSkvZ7txSlXnaNQNpgPZi+G5tw0=`), run from the laptop
    because it holds the `irpt-requests` decrypt. READ ONLY: nothing is applied, written, deleted or created by this order.
  </objective>

  <context>
    The pair, section 4, is the specification of each read:
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release5/NEVER_WIDEN_PAIR_ANLREQ_RELEASE5_IRPT_STATUS.md` (blob 1b310f3c2a), and the CTO half
    `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE5_IRPT_STATUS_CTO_HALF.md` (msg 4619).
    The apply is the dell2 applier's: `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/task_orders/IRPT_ANLREQ.TO-APPLY-Y5.irpt-status-release5-dell2.md`.
    The method of reads 3 and 4 is the one you used for `IRPT_ANLREQ.TO-AR-y-34` (result `Y1_reads_3_4_rev6_result.json`, commit 1ebd6f6e0e).
  </context>

  <steps>
    **AMENDMENT 1 (issuer `2.0.0_SA_COO~Y2`, 2026-10-11 ~11:0xZ): ONE more recorded member on R2, by the CTO's round-4 analysis
    (@9da283e89f, section 3, row `IRPT_YCDGEN-D2-S38`: "one read of a served section's unit and value before any formatting change: a
    fixture is not evidence of a served shape").** Your R2 to R7 stand as filed (@612ea01ad7; the issuer's run of the reads check on that
    file prints `APPLY5-READS-OK`). Add to the result file, under `reads.R2`, a member `section_unit_read`:
    `{"sections_read": <n>, "units": {"<unit string as served>": <count>}, "value_json_types": {"number": <n>, "string": <n>, "null": <n>},
    "percent_unit_values_with_abs_below_1": <n>, "percent_unit_values_with_abs_1_or_more": <n>, "claim": "measured"}`, over the served
    sections of the READY reports you already read at R2 (14 requests). Counts and unit strings only: no value, no name. The two
    percent counts say whether a section served with a percent unit carries a fraction (0.07) or a whole number (7); that is the
    whole question of the row. Re-commit the result and the proof instance. The criterion and its check do not change.
    Gate limb that graded this amendment: this commit's own gate output is the read.
    0. GATE: `get-function-configuration` on `irpt-status`. If `CodeSha256` is NOT `Iw3FADFr...`, the apply has not landed: do nothing
       further, and wait for the issuer's word that it has. Record the digest and LastModified you read.
       You may run the BEFORE arms (R2, R3, R5 on revision 6, `6idtFvAm...`) while you wait, and should: they are the comparison.
    1. R2 -- `GET .../analysis/{jobId}/sections` for a READY owned job, as its owner: the body carries a `retained_ref` object; before the
       apply the key is absent; `provider`, `request_ref` and the `sections` count are unchanged. A refusal
       `READY_REPORT_RECEIPT_REQUIRED` here is a FAIL (it is the new refusal this release adds; a READY report must still answer).
    2. R3 -- `GET .../analysis/requests` as an owner with at least one accepted request: every row carries `client_id` and a `client_claim`
       in SELECTED / UPLOAD / UNREADABLE; the page carries `unreadable_rows`; the row count equals the count before the apply.
    3. R4 -- the section-date read of a request whose report is `provider: OPAL_ENGINE`. Use `REQ-5e4149d2` if it is readable (CTO
       condition; it is also IRPT_YCDGEN row `D2-S38`'s disarming read): dates are served, not `SECTION_DATE_CENSUS_INVALID`. If no
       OPAL_ENGINE request is readable, the result is the string `ABSENT` with a census `{"count": 0, "denominator": <accepted requests
       scanned>, "scope": "<tenants and table>"}`. ABSENT is not a pass of the branch and the record must not say it is.
    4. R5 -- a YCHARTS-provider request's section-date read: the same dates before and after the apply (the control of R4).
    5. R6 -- reads 3a, 3b, 4_record, 4_route exactly as in `TO-AR-y-34`, on the release build. 3c stays null with its reason if no
       custody-lane request exists. The signed link is NEVER logged or written: its sha256 and expiry only.
    6. R7 -- S3 object versions under the R6 request's three artifact directories, counted before and after R6: equal. State what was
       counted and that DynamoDB was not.
    7. Write `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y5_after_reads_result.json`:
       `{"release_under_test": {"function": "irpt-status", "code_sha256": "<step 0>", "last_modified": "<step 0>", "claim": "measured"},
       "reads": {"R2": {"result": true|false, "before": "<key absent|present>", "after": "<...>"}, "R3": {"result": ..., "rows_before": <n>,
       "rows_after": <n>, "claims": {"SELECTED": <n>, "UPLOAD": <n>, "UNREADABLE": <n>}, "unreadable_rows": <n>},
       "R4": {"result": true|false|"ABSENT", "request": "<id or null>", "census": {...}}, "R5": {"result": ...},
       "R6": {"result": true|false, "3a": ..., "3b": ..., "3c": null, "3c_reason": "...", "4_record": ..., "4_route": ...},
       "R7": {"result": true|false, "versions_before": <n>, "versions_after": <n>, "keys_scope": "<what was counted>"}},
       "method": "<one line>"}`. `R6.result` is true only when 3a, 3b, 4_record and 4_route are all true.
       Booleans, digests, counts, ids and codes only. No URL, no name, no figure, no document content, in the file or in your report.
    8. ANY read false: report to the issuer AT ONCE citing this order's path and naming the read; do not retry it into a pass. The issuer
       orders the rollback on dell2.
    9. Commit the result and the proof instance; report to the issuer citing this order's path, with push state.
  </steps>

<criterion id="READS5-AC1" cell_refs="AR-y-32"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r3/apply5_checks.py reads</invocation><expect>APPLY5-READS-OK</expect></criterion>
`READS5-AC1`: R2, R3, R5, R6 and R7 are true on the release build, and R4 is true or ABSENT with its census.

<expected_criteria>READS5-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - Read only. No apply, no upload, no delete, no new request created unless a read cannot otherwise be made, in which case STOP and ask.
    - The signed link is never logged, written or sent.
  </bounds>
</task_order>
