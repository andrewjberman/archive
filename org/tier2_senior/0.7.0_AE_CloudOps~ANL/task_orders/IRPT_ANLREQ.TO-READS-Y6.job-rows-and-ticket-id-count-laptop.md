<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-Y6.job-rows-and-ticket-id-count-laptop</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ANL</issued_to>
    <date>2026-10-11</date>
    <status>complete -- flipped by issuer 2.0.0_SA_COO~Y2 2026-10-11 ~16:3xZ: READS6-AC1 prints READS6-OK on its verbatim invocation and the proof instance is VALID rc 0, both run by the issuer on the laptop applier's files (commits b4caac9dec, 9c3968c6eb). Job rows: 14 of 14 read, 14 READY, first REQ-01c903660d7ab222cd08b2ff. Accepted requests scanned 51 of 1904 items: 6 store a ticket_id, 45 do not, 0 unreadable.</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; no resource is changed by this order. comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger. comp-iam: RUN -- by reading 1 record: the dell2 applier's refusal (R6_step0_STOP2_job_row_read_denied.json @834b51387a: kms:Decrypt on the IRPT key is denied to the dell2 identity, and irpt-jobs uses the same key as irpt-requests); the laptop identity scanned irpt-requests today (1894 items, its own snapshot), so it holds that decrypt; whether it may read irpt-jobs is NOT known and step 1 says what to do if it may not.
comp-adversary: DECLARED-NOT-APPLICABLE -- the order produces two counts and a list of states and decides nothing; a denied read is recorded as denied, never as a zero.
lane: the applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: READS6-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/IRPT_ANLREQ.TO-READS-Y6.job-rows-and-ticket-id-count-laptop.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> READS6-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R9_Y.md</decomp_doc> round 9, workstream ~Y, release 6: a read the dell2 applier cannot make.
<owned_cells>AR-y-91</owned_cells>
</decomp_ref>

  <objective>
    Two READ-ONLY reads from the laptop, which holds the decrypt dell2 lacks. (1) The JOB ROW state of 14 candidate requests, so the
    dell2 applier of release 6 can pick one whose job reads READY. (2) A count the CTO asked for (msg 4955): how many accepted
    requests store NO `ticket_id`. Nothing is applied, written to AWS, deleted or invoked.
  </objective>

  <context>
    Release 6 (order `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/task_orders/IRPT_ANLREQ.TO-APPLY-Y6.composition-read-ready-gate-dell2.md`)
    adds a gate: the commentary composition read answers only for a request whose JOB reads READY. Its after-reads need ONE such
    request. Your snapshot `Y5_before_arms_rev6_snapshot.json` (commit b3b3160b25) shows 14 of 50 requests with a SERVED status of
    READY, all in tenant `cottonwood`. A served status is not the job row, and the dell2 applier cannot read the row
    (kms:Decrypt denied on dell2). The release waits on step 1 below; it is the urgent half.
  </context>

  <steps>
    1. For each of the 14 request ids whose `R4R5` entry in your snapshot reads `state: READY` (re-derive the list from the file; do
       not retype it): read its JOB ROW in table `irpt-jobs`, key `tenant` = the tenant in the snapshot, `job` = the request id
       (the key `ycharts/generate/acceptance.py` `_job_key` and `durable_job.py` `get_state` use), with `ConsistentRead`, projecting
       ONLY the `state` attribute. Record the state string per id, or `NO_ROW`, or the refusal's error code if the read is denied.
       If the read is DENIED for every id, STOP, report that, and record 0 of 14 READ: a denied read is never a count of states.
    2. REPORT STEP 1 AT ONCE (do not wait for step 3): one line to the issuer citing this order's path, naming the FIRST id whose row
       reads `READY` and the count `<n> of 14 read READY`.
    3. The count (CTO msg 4955): over EVERY accepted request (the `analysis#<request_id>#1` items of `irpt-requests`, the scan your
       snapshot made: 50 of 1894 items today), how many acceptance records carry a `ticket_id` member and how many do not. Counts by
       tenant; the denominator printed; items you could not read counted separately as unreadable, never as "no ticket_id".
    4. Write `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y6_job_rows_and_ticket_id_count.json`:
       `{"read_at": "<UTC>", "job_rows": {"read": <n>, "of": 14, "states": {"<request id>": "<state>|NO_ROW|<error code>", ...},
       "first_ready": "<request id or null>", "ready_count": <n>}, "ticket_id_count": {"accepted_scanned": <n>, "items_scanned": <n>,
       "with_ticket_id": <n>, "without_ticket_id": <n>, "unreadable": <n>, "by_tenant": {"<tenant>": {"with": <n>, "without": <n>}}},
       "method": "<one line>", "claim": "measured"}`.
       Ids, state strings, counts and codes only. No name, no figure, no document content, no ticket id values.
    5. Commit the result and the proof instance; report to the issuer citing this order's path, with push state.
  </steps>

<criterion id="READS6-AC1" cell_refs="AR-y-91"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r9/reads6_check.py</invocation><expect>READS6-OK</expect></criterion>
`READS6-AC1`: the result file holds a state (or NO_ROW, or an error code) for each of the 14, the first READY id consistent with those
states, and a ticket-id count whose parts add up to its denominator.

<expected_criteria>READS6-AC1</expected_criteria>

The check at the base (run by the issuer before this cut): FAIL as expected (no result file).

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~ANL/logs/
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - Read only: `GetItem` / `Query` / `Scan` on the two tables as your identity already makes them. No write, no invoke, no apply.
    - No composition, name, figure or ticket id value in any file, log or message.
  </bounds>
</task_order>
