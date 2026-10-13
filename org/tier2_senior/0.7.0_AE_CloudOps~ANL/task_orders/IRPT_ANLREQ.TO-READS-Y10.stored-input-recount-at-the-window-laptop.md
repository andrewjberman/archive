<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READS-Y10.stored-input-recount-at-the-window-laptop</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ANL</issued_to>
    <date>2026-10-13</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read-only; no resource is changed by this order.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN -- by reading the result of this lane's TO-READS-Y9 (@8a0ae718f2 and its proof): the identity held the reads on 2026-10-13T00:28:50Z; whether it still does is NOT known and step 2 says what to do if it does not.
comp-adversary: RUN -- by reading Y9's own order and result against this cell; the lens: a count that names a request or a person, or a count taken before the window and read as if it were taken at it. The order requires the read time in the result and the issuer's staleness rule (an hour). NOT seen: the real table and bucket (0 live items read by the issuer).
lane: the applier's own deliverables and logs; read-only on the world.
</preflight>
<proof_of_spec>
Criterion id: READS10-AC1. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/IRPT_ANLREQ.TO-READS-Y10.stored-input-recount-at-the-window-laptop.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> READS10-AC1` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R19A_Y.md</decomp_doc> round 8, workstream YR: the stored-input recount the signed pair asks for as R0d (row IRPT_ANLREQ-D2-W52-S35).
<owned_cells>AR-y-204</owned_cells>
</decomp_ref>

  <objective>
    ONE READ-ONLY run of the SAME counting script and the SAME two readers as `IRPT_ANLREQ.TO-READS-Y9.stored-input-count-r18-laptop` (Y9; complete), now at the window of the reader's release: how many stored upload
    inputs the release reader (sha256 83ab9b45...) reads differently from the template stored at acceptance, by cause, and for each it would turn back whether a report was ever generated. COUNTS AND DATES ONLY.
    Also in the result: the number of stored template inputs that carry a stored reader version (`reader_version`), expected 0 before the release. Nothing is written to AWS, deleted, invoked or applied.
    Y9 counted 56 template inputs (49financial 10, cottonwood 45, inflection 1), 0 turned back, at 2026-10-13T00:28:50Z; templates stored since are the difference this order measures.
  </objective>

  <context>
    Everything in Y9's order (`org/tier2_senior/0.7.0_AE_CloudOps~ANL/task_orders/IRPT_ANLREQ.TO-READS-Y9.stored-input-count-r18-laptop.md`, steps 0 to 5 and AMENDMENT 1) applies unchanged, with these differences only:
    (a) the issuer's word for ONE live run is given here; (b) the result file is `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y10_stored_input_count_r19_window.json`; (c) the result carries one extra member,
    `reader_version_inputs`: the number of stored template inputs whose stored record names a `reader_version`, by tenant code (counts only; if the script does not read that member, read it with the script's own
    GetItem path in a copy of the script outside the checkout and say so in `not_read`; a script change is a stop for the issuer, not a fix); (d) the self-test form is Y9's AMENDMENT 1 (a throwaway worktree at `35c3c4bd45`).
    Why this seat: kms:Decrypt on the IRPT key is denied to dell2.
    The result is read by `0.7.0_AE_CloudOps~YC2` within the hour before the resident install; if it is older than 60 minutes at that moment the issuer asks you to run again (a second run needs the issuer's word).
  </context>

  <steps>
    0. As Y9 step 0 and AMENDMENT 1. 1. As Y9 step 1 (both readers outside the checkout; both sha256 checked). 2. As Y9 step 2 (arguments resolved from the table, never typed). 3. Run ONCE as Y9 step 3. 4. Write the result file named in (b), the Y9 members plus `reader_version_inputs`, no id, file name, ticker, amount, e-mail or link.
    5. One line first, as soon as step 3 ends, to the issuer (cite this order's path, push state): template inputs, read differently, turned back, turned back with a report, `reader_version_inputs`. Then delete the scratch files, commit the result and the proof instance.
    Expected: turned back 0. A non-zero turned-back count: STOP, report the number and the tenants to the issuer; the window does not open.
  </steps>

<criterion id="READS10-AC1" cell_refs="AR-y-204"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r18/reads9_check.py --result org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y10_stored_input_count_r19_window.json</invocation><expect>READS9-OK</expect></criterion>
`READS10-AC1`: the result holds the script's twelve members, its counts add up, names the script blob, both reader hashes, how the bucket was resolved and an empty write list, and holds no id, file name or address.

<expected_criteria>READS10-AC1</expected_criteria>

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
# pipeline-override: a laptop READ order under a signed pair (not a worker cell); the cell AR-y-204 is the issuer's, as for TO-READS-Y9.
