<task_order>
  <metadata>
    <id>NFRA_OPSWKF.TO-READ-S3.four-direct-invokes-dell2</id>
    <issued_by>2.0.0_SA_COO~O2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>NFRA_OPSWKF</project_code>
  </metadata>
<risk>WORLD</risk>
<round>2</round>
<workstream>S</workstream>
<proof_genre>VERIFY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPSWKF/decompositions/NFRA_OPSWKF_DECOMP.md</decomp_doc> (workstream S): issuer cells `OW-sr-2` (FWD-9's reads after the release) and `OW-sr-1` (FWD-8's), the admitted arms left unread at the two releases.
<owned_cells>OW-sr-2, OW-sr-1</owned_cells>
</decomp_ref>

  <objective>
    FOUR direct invokes of two DEPLOYED functions with constructed events (PRD v0.9 @d7de5b9217, FWD-9; and FWD-8's tier arm). No user
    row, no token, no signing-key read, no HTTP call, no apply, no write of any kind. Record a status and one field per invoke.
  </objective>

  <context>
    READ BOTH FILES WHOLE BEFORE THE FIRST ACT, the files and not this restatement:
    - Amendment and COO half (SIGNED): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_SD2_FWD9_RELEASE_PAIR_AMENDMENT_1_DIRECT_INVOKES_20261011.md
      @201b464dcd, sha256 begins d5abdc06839318bd. Its section 1 is the table of the four invokes and its section 2 covers every answer.
    - CTO half (SIGNED, msg 5959): org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_OW_SD2_AMENDMENT_1_DIRECT_INVOKES_20261011.md
      @1c81d207ce. Its six conditions GOVERN; the two that change the amendment's order of acts: **I2 FIRST**, and an admitted arm
      answering 403 is REPORTED AT ONCE and NOTHING is rolled back without the CTO's word.

    Condition 4, done by the issuer and stated here so your report can carry it: the submit handler's log statements at the pin
    `234c3b4b10` are nine `print` calls (lines 339, 343, 349, 368, 371, 380, 382, 385, 396). None prints the event or the body; all sit
    after the `ticket_id` check except the last, which prints an exception's text on the handler's error path. So I1, I2 and I3 write no
    log line of their own on their expected answers. Confirm it against the DEPLOYED bytes you already hold from TO-APPLY-S2 (the
    member diff showed them equal to the pin) and say so in one line.

    The unstorable body, byte for byte as R0 and R1: `{"fund": "PFDE", "ticket_id": "not-a-ticket-id"}`.
    Event shape: `{"rawPath": <path>, "requestContext": {"http": {"method": <M>}, "authorizer": {"lambda": {<claims>}}}, "body": <string>}`
    (no `body` key on I4). Every `email` is a synthetic `@opal.invalid` address of your choosing, different per invoke, named in the report.
  </context>

  <steps>
    0. No deploy ledger: nothing is deployed or written. Open nothing in `.open_deploys/`.
    1. DryRun: `lambda invoke --invocation-type DryRun` on both functions reads 204. Any other answer: STOP (no grant is added).
    2. P0 on both: `get-function-configuration` CodeSha256 reads `vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8=`
       (`trade-submission-handler`) and `lAZbT48kxrNOnfYdO5D/gXxg+4W7xECEczneZx+YoCc=` (`trade-dashboard-api`). Any other value: STOP
       before any invoke.
    3. **I2 FIRST** -- `trade-submission-handler`, context `email`, `tier advisor`, `firmId fwd9-synthetic-nofirm`; POST
       `/api/general/trades/submit`, the unstorable body. Expect handler `statusCode` 403, `message` EXACTLY
       `Forbidden: trade submission answers Opal staff only`. A 400 or a 200: STOP, make no further invoke, report at once.
    4. I1 -- the same function and request, context `email`, `tier advisor`, `firmId opal-capital`. Expect 400, `message`
       `ticket_id is malformed`. A 403: record it, make no further SUBMIT invoke, report at once, roll back NOTHING. A 200: STOP and
       report at once with the submission id; delete nothing.
    5. I3 -- the same function and request, context `email`, `tier internal`, `firmId fwd9-synthetic-nofirm`. Expect 400,
       `message` `ticket_id is malformed`. Other answers as step 4.
    6. I4 -- `trade-dashboard-api`, context `email`, `tier internal`, `firmId fwd9-synthetic-nofirm`; GET
       `/api/general/trades/submissions/pending`, no body. Expect 200; record the status and the body's `count` ONLY. A 403: record
       it, report at once, roll back NOTHING.
    7. After I3: the `by-initiator` Count on `opal-trade-submissions` for EACH synthetic address used in I1, I2 and I3 reads 0, whole
       partition, with ONE non-zero control beside them (the count only).
    8. For each invoke record: the invoke's `StatusCode`, `FunctionError` (absent expected), the handler's `statusCode`, and the one
       field. Delete each response file in the act and print that it is gone. A `FunctionError`, a timeout or a 500 is recorded with
       its error type only and that invoke is retried at most once.
    9. Report once to `2.0.0_SA_COO~O2`: steps 1 and 2, the four invokes in the order made with their times, step 7, and these words
       exactly: "FWD-9's admitted arm and FWD-8's tier arm are EXERCISED ON THE DEPLOYED BYTES BY DIRECT INVOKE. Neither is exercised
       through the portal's authorizer; the tier shape has been shown through no door." (or, if an arm answered otherwise, what it
       answered instead of that sentence). The proof-of-spec instance goes at the flat path the gate accepts.
  </steps>

  <bounds>
    Four invokes, in the order I2, I1, I3, I4, each at most once more on an invoke-level error. No other invoke of any function. No
    call to any API, in particular none to `trade-submission-api` (`w8jnzvs21g`). No row, token, key read, apply, grant or write. No
    payload content beyond the status, the `message` or the `count` is written anywhere. Nothing is rolled back under this order.
  </bounds>

<proof_of_spec>
  <criterion id="OW-sr2-AC2" cell_refs="OW-sr-2" judgment="true"/>
  <criterion id="OW-sr1-AC2" cell_refs="OW-sr-1" judgment="true"/>
</proof_of_spec>
OW-sr2-AC2 (judgment; the CVO's at L9): I2 refused with the new message, I1 and I3 answered 400, no row. OW-sr1-AC2 (judgment; the
CVO's at L9): I4 answered 200.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, hold or gate is created or consumed
comp-iam: DECLARED-NOT-APPLICABLE no grant changes; the principal's permission is read by DryRun at step 1 and nothing is added
comp-adversary: DECLARED-NOT-APPLICABLE a read of deployed behaviour; the refusing twin (I2) is read first so the instrument is shown able to read a refusal
</preflight>

# pipeline-override: a READ order to the dell2 applier for the admitted arms of two issuer cells (OW-sr-2, OW-sr-1), under a signed pair amendment; not a worker cell and nothing is deployed.
</task_order>
