<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-C173.internal-callers-census-ar2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AR2</issued_to>
    <date>2026-10-12</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; one Scan of the users table and nothing else. No resource is changed.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN -- by reading 1 record: this lane's own census (TO-RUN-YS1 step 1b, result `reserved_rows_census`) scanned the same table (86 rows) with this identity, so `dynamodb:Scan` on it is allowed today; the order's step 0 re-tests it.
comp-adversary: RUN -- by reading the script (blob named in step 0) and its record against the cell; the lens: an output that carries an address or a row counted as active when it could not be read. The script projects only `firmId`, `userType` and `status`, counts an unreadable row as unreadable, and prints no address (the check refuses an at-sign). NOT seen: the live table (this lane reads 0 rows before the run).
lane: this applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: RUNC173-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/IRPT_ANLREQ.TO-RUN-C173.internal-callers-census-ar2.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> RUNC173-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R17_Y.md</decomp_doc> round 17, workstream Y, item 2: the census the status rule's never-widen pair carries; run by an applier that can read the users table.
<owned_cells>AR-y-173</owned_cells>
</decomp_ref>

  <objective>
    ONE READ-ONLY run of an existing counting script: how many INTERNAL users rows there are, by firm, user type and status, and how many hold a status that is
    exactly `active`. COUNTS ONLY. It is the input to the never-widen pair for the status-exactly-`active` rule (cell AR-y-172, built and not released): that rule
    refuses an internal caller that selects another firm unless its users row is `active`. Nothing is written, deleted, invoked or applied.
  </objective>

  <context>
    Script and record (read the record first): `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~51/r17/count_internal_callers.py` and
    `.../r17/CENSUS_SCRIPT_RECORD.json` (drained @f24b805f6b). Part (a) scans the users table (`opal-users-v2`) and projects `firmId`, `userType`, `status` of PROFILE rows.
    Part (b), the callers with no row, is NOT AVAILABLE: no log line carries the caller (the worker's finding), so it prints that and no number.
  </context>

  <steps>
    0. Pre-checks, STOP and report on any miss: (i) `python <script> --self-test` exits 0 and prints `CENSUS-SELFTEST-OK`; (ii) `git hash-object <script>` is recorded as `script_blob`;
       (iii) `iam simulate-principal-policy` on your own ARN for `dynamodb:Scan` on the users table is allowed (state it). A denied simulate is a STOP, never a count of zero.
    1. Run ONCE: `python <script> --region us-east-1 --out <outside the repo>/census.json` (the table defaults to `opal-users-v2`). The last stdout line is the one JSON object. If it exits
       non-zero, record the exit code and the one stderr line (`SCAN_FAILED <code>`); do not retry.
    2. Write `org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/C173_INTERNAL_CALLERS_CENSUS.json`:
       `{"read_at": "<UTC>", "count": <the script's JSON object, unchanged>, "script_blob": "<hash>", "identity_arn_tail": "<role or user name only>", "writes_made": [], "claim": "measured",
       "not_read": [...]}`. Before you commit, READ it: it must hold NO address, name or id. The check refuses an at-sign.
    3. Delete your scratch outside the repo. Commit the result and the proof instance; report to the issuer citing this order's path, with push state. One line first: internal rows, how many exactly active,
       how many not active, unreadable.
  </steps>

<criterion id="RUNC173-AC1" cell_refs="AR-y-173"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r17/runc173_check.py</invocation><expect>RUNC173-OK</expect></criterion>
`RUNC173-AC1`: the result holds the script's part (a) members, its counts add up (internal + external + unreadable = profile rows; the status table sums to internal rows; rows with status `active` equal internal_active), part (b) reads NOT_AVAILABLE, the write list is empty and no address appears.

<expected_criteria>RUNC173-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~AR2/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - Read only: one `Scan` of the users table, projecting three attributes, and `iam simulate-principal-policy` on your own identity. No write, no delete, no invoke, no apply.
    - No address, name or id in any file, log or message. One run. A second run needs the issuer's word.
  </bounds>
</task_order>
