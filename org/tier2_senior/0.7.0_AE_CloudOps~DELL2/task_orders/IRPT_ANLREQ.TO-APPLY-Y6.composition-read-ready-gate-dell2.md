<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-Y6.composition-read-ready-gate-dell2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: RUN -- by reading: the pair's sections 2 and 3 (one role's inline policy widened by one table in two statements; one function's code, 3 of 16 members; 1 caller, the commentary drafter, found by a census of non-test callers); NOT seen by the issuer: whether the function's module attaches another policy to the role (step 0 reads it). comp-routes: DECLARED-NOT-APPLICABLE -- the function serves no route; it is invoked directly. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger is added or moved; 0 event-source mappings fed the drafter at 06:09Z today (the applier's own read), re-read at step 0. comp-iam: RUN -- by reading 1 role policy of 5 statements: the grant adds one table to a GetItem statement under an unchanged LeadingKeys condition and one table to a kms context list; no action and no principal is added; G1 reads it as applied and A1 proves it effective.
comp-adversary: RUN -- by reading: the CTO half (msg 5241) is the second reader's attempt on the pair, 1 packet read whole and 0 member hunks; it added two conditions (no composition content in any record; the parity skip said in words). The lens the order keeps: code landing before its grant -- step 2 does not start until G1 is recorded.
lane: the applier's own deliverables, the deploy ledger and sentinel, the one source-map entry.
</preflight>
<proof_of_spec>
Criterion ids: APPLY6-AC1, APPLY6-AC2. Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r6/IRPT_ANLREQ.TO-APPLY-Y6.composition-read-ready-gate-dell2.proof_of_spec.json`,
`to_id` the FULL id above, validated with `python .tools/proof-of-spec-check.py <instance> APPLY6-AC1,APPLY6-AC2` AFTER its commit.
</proof_of_spec>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R9_Y.md</decomp_doc> round 9, workstream ~Y, release 6: the apply of cells `AR-y-81` and `AR-y-91`.
<owned_cells>AR-y-91</owned_cells>
</decomp_ref>

  <objective>
    IRPT_ANLREQ release 6 on dell2, in a FIXED ORDER: (1) the role grant of `irpt-commentary-composition-read-lambda` (the jobs table
    in two statements), read back as applied; (2) only then the function's code, build `DbvBUxTGlCsdG4htVOhbI4NBxBMNbmjD6BLpMGu2Yo4=`.
    Live and ROLLBACK is `ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0=`. This release disarms row `IRPT_ANLREQ-D2-S53` and LIFTS the
    no-upload hold on this function FOR THIS ORDER ONLY.
  </objective>

  <context>
    Read the pair FIRST, both halves; they bind and this order only sequences them.
    - COO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release6/NEVER_WIDEN_PAIR_ANLREQ_RELEASE6_COMPOSITION_READ_READY_GATE.md` (blob 5e56a253f7).
    - CTO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE6_COMPOSITION_READ_READY_GATE_CTO_HALF.md` (@6d3aac1d65, msg 5241).
      Its two conditions: (1) G2 and A1 read a real READY request's composition and the records hold a sha256, a status and key names,
      NEVER the body -- no composition content in the ledger, a log, a file or a message; (2) the build uses `BAU_PARITY_SKIP=1`, and
      your close SAYS SO in words.
    - Census: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r9/COMPOSITION_READ_RELEASE_CENSUS.json`.
    Why the order: with the code and without the grant, the job read is denied and EVERY composition read refuses. With the grant and
    the old code, nothing uses the grant. So "grant applied, old code" is the one safe in-between state and may stand if step 2 cannot go.
  </context>

  <steps>
    0. Pre-checks; STOP on any miss, before any write, and report the line that stopped you:
       - the building commit C is on origin and contains `eba5acba8f`; you work in a DETACHED worktree at C;
       - live `CodeSha256` of the function is `ZZmWOFSA...`; record the S3 object version now serving, as the rollback source;
       - `get-role-policy` of the function's role: S1 and S2 name the requests table only; and `list-attached-role-policies` on that
         ONE role: record what is attached (the pair could not read whether the module attaches a managed policy);
       - MAY YOU INVOKE the function? Read it from your identity's policy as you know it, or by the one G2 read below made BEFORE any
         change. If you may not invoke it, STOP: the after-reads cannot be made and the release does not start;
       - a READY request readable by the composition read EXISTS: find one from records you already hold (a request whose job reads
         READY in a tenant the function serves). If none can be found, STOP: a release whose only passing read is a refusal proves
         nothing about READY;
       - no other open ledger entry on the `investor-reporting/export` root, read across every live worktree with the denominator printed;
       - event-source mappings for the commentary drafter's queue: record the count (0 this morning).
    1. Ledger `irpt-anlreq-r6-composition-read-ready-gate-20261011`, opened and COMMITTED before any write, naming C, both digests,
       the rollback version and the two legs (grant, code).
    2. THE GRANT. Plan `investor-reporting/export` TARGETED at the role policy (`aws_iam_role_policy.commentary_composition_read`):
       exactly ONE resource to change, 0 add, 0 destroy; the diff adds the jobs table to S1's Resource and to S2's table-name context
       and nothing else. Any other line is a STOP. Commit the plan text; `safe-apply`.
    3. G1: `get-role-policy` again: both tables in S1 and in S2. G2: ONE direct invoke of the function, on the OLD code, with the
       closed request shape `{"tenant", "request_ref"}` for the READY request: record `status`, the answer's `sha256` member, the sorted
       key names, and the function's `CodeSha256` at that moment (`ZZmWOFSA...`). The grant alone must change nothing.
       DO NOT START STEP 4 UNTIL G1 AND G2 ARE RECORDED.
    4. THE CODE. At C: `BUILD_ONLY=1 BAU_PARITY_SKIP=1` first -- the digest must be `DbvBUxTG...` or STOP. Then upload (the same skip
       flag), download the uploaded object back by version and check its digest; plan TARGETED at the function module: ONE resource to
       change; commit the plan text; `safe-apply`. Live `CodeSha256` = `DbvBUxTG...`; the re-plan reads 0 changes.
    5. A1: the SAME invoke as G2: `status` OK, the same `sha256`, the same key names. A2: the same shape for
       `REQ-4b5155ac2ea9467ab771b414` (tenant 49financial; its job reads RECEIVED by the laptop's record of today): the refusal
       `UNAVAILABLE`. A3: a well-formed request id that does not exist: `UNAVAILABLE`.
    6. BRANCH B -- A1 refuses or differs from G2, or A2 answers instead of refusing, or the live digest is wrong, or a plan shows more
       than its one resource: ROLL BACK THE FUNCTION in this session to the step-0 object version (copy it onto the key, targeted
       apply), re-read the digest and repeat G2's read; the GRANT STAYS; close the ledger ROLLED_BACK; file a BLOCKING row in
       `org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md` with the refusal text; report.
       If step 4 cannot proceed after step 3, the state "grant applied, old code" MAY STAND: say so in the ledger and report.
    7. Record step: the source map's entry for this function states the release -- `artifact_sha256` and `deployed_code_sha256`
       `DbvBUxTG...`, `last_deployed_commit`, `last_deployed_at`, `deploy_ledger`; and the stale `_build_note` sentence that calls the
       entry a draft is corrected (the census's `map_corrections_needed`). No other entry changes.
    8. Write `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r6/R6_apply_record.json`:
       `{"building_commit": "<C>", "step0": {"code_sha256": "...", "replaced_s3_object_version": "...", "may_invoke": true,
       "attached_policies": [...], "event_source_mappings": <n>}, "grant": {"plan": {"resources_to_change": 1, "to_add": 0,
       "to_destroy": 0}, "G1_both_tables_in_S1": true, "G1_both_tables_in_S2": true}, "G2": {"status": "OK", "sha256": "...",
       "keys": [...], "code_sha256_at_read": "ZZmWOFSA..."}, "code": {"built_sha256": "...", "plan": {"resources_to_change": 1,
       "to_add": 0, "to_destroy": 0}, "live_after": "...", "replan_changes": 0}, "A1": {"status": "OK", "sha256": "...", "keys": [...]},
       "A2": {"refusal": "UNAVAILABLE"}, "A3": {"refusal": "UNAVAILABLE"}, "parity_skip_used": true, "rolled_back": false,
       "ledger": "irpt-anlreq-r6-composition-read-ready-gate-20261011", "claim": "measured"}`.
       A sha256, statuses, key names and counts ONLY: no composition body, no name, no figure.
    9. Close the ledger, saying in words that the build used `BAU_PARITY_SKIP=1`. Commit. Report to the issuer citing this order's
       path: the record path, the live digest read at send time, and push state.
  </steps>

<criterion id="APPLY6-AC1" cell_refs="AR-y-91"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r9/apply6_checks.py live</invocation><expect>APPLY6-LIVE-OK</expect></criterion>
`APPLY6-AC1`: the live function runs the release build.

<criterion id="APPLY6-AC2" cell_refs="AR-y-91"><invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r9/apply6_checks.py record</invocation><expect>APPLY6-RECORD-OK</expect></criterion>
`APPLY6-AC2`: the record shows the grant read as applied before the code, G2 on the old code, A1 equal to G2, A2 and A3 refused,
the ledger closed and the map stating the release.

<expected_criteria>APPLY6-AC1 APPLY6-AC2</expected_criteria>

Both checks at the base, run by the issuer on these exact invocations before this cut: FAIL as expected (live reads `ZZmWOFSA`; no
record file). Their default root was checked to be the repository root.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r6/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/irpt-anlreq-r6-composition-read-ready-gate-20261011.json
infra/aws/lambda/ci/lambda-source-map.json
org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

  <bounds>
    - One role policy and one function's code. Nothing else is applied, deleted, granted or created. No S3 delete of any object or version.
    - The drafter is NOT invoked. No model is called, no draft is written, no message is sent, no queue is read.
    - No composition content, name or figure in any file, log or message.
    - Never `aws lambda update-function-code`, never a bare `terraform apply`. A STOP is a report with the line that stopped you.
  </bounds>
</task_order>
