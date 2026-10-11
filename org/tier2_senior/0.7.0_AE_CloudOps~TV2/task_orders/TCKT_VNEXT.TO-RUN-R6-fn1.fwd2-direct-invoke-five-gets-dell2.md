<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RUN-R6-fn1.fwd2-direct-invoke-five-gets-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>6</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R6.md</decomp_doc> (round 6): cell `R6-fn-1`, FWD-2's live proof for the TICKET by direct invoke.
<owned_cells>R6-fn-1</owned_cells>
</decomp_ref>

  <objective>
    FIVE read-only invocations of the deployed Lambda `opal-ticket-api`, made DIRECTLY (around the portal authorizer) with
    constructed caller contexts, to show on the live function that a person at another firm cannot open a ticket or see it in a
    list. Every call is a GET. Nothing is written, no identity or token is minted, nothing is deployed.
  </objective>

  <context>
    Both halves are SIGNED. Read both before any AWS call:
    - pair and COO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R6_RUN/R6_FN1_DIRECT_INVOKE_PAIR.md` @942f1c7bf9
      (section 3 is the five arms with each expected answer read from the handler's own rule; section 6 the branches);
    - CTO half: `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/1.0.0_SA_CTO~DELL2/CTO_HALF_R6_FN1_FWD2_DIRECT_INVOKE_20261011.md` @16308d2aae
      (signed for A1 to A5 and branches A to E; the attached FILE's arm is NOT in this order and comes by an amendment later).
    A direct invoke goes around the authorizer: the function believes whatever the event says about the caller. That is the
    instrument here and the reason every payload is written down before it is sent.
    The issuer's reads at the GO (22:4xZ): the live CodeSha256 `Ob/MZBEO...` (22:16:38Z), deployed handler `b7764fbd`; 0 entries
    naming the ticket service open in the shared tree's `.open_deploys/`; the function's resource policy admits the API Gateway
    service only; this box's identity simulates `allowed` on `lambda:InvokeFunction` for this function.
    Read `/cloud-ops` first. This is NOT a deploy: open NO deploy ledger entry.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO under the pair as signed. In order:
    0. Read EVERY live worktree's `.open_deploys/`, union them, print the per-tree denominator: an open entry naming
       `opal-ticket-api` is a STOP (no direct invoke while an apply is in flight). Run your OWN simulate of
       `lambda:InvokeFunction` on the function's ARN for your identity and print the decision; anything but `allowed` is a STOP
       (do not ask for a grant).
    1. The live CodeSha256 starts with `Ob/MZBEO`; otherwise STOP and report the value.
    2. BEFORE: `opal-tickets` ItemCount; and for `TCK-20261011-e6433610`, by a ConsistentRead `get-item` with a projection, its
       `status` and the LENGTH of its `events` list only.
    3. Create `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r6_fn1/`. Write the FIVE payloads there as
       `A1.json` .. `A5.json` BEFORE any call. Each is API Gateway payload 2.0 shape with exactly: `version "2.0"`,
       `rawPath`, `requestContext.http.method "GET"`, and `requestContext.authorizer.lambda` holding exactly the five keys
       `email`, `name`, `userType`, `firmId`, `allowedFirmIds`. No body, no query string. The callers:
       - A1: `email tckt-fwd2-probe-a@opal.invalid`, `name "TCKT FWD-2 probe A"`, `userType "client"`, `firmId "49financial"`,
         `allowedFirmIds "49financial"`; `rawPath /api/scoped/tickets/TCK-20261011-e6433610`
       - A2: `email tckt-fwd2-probe-b@opal.invalid`, `name "TCKT FWD-2 probe B"`, `userType "client"`, `firmId "cottonwood"`,
         `allowedFirmIds "cottonwood"`; the same `rawPath`
       - A3: the A2 caller; `rawPath /api/scoped/tickets`
       - A4: `email tckt-fwd2-probe-internal@opal.invalid`, `name "TCKT FWD-2 probe internal"`, `userType "null"`,
         `firmId "opal-capital"`, `allowedFirmIds ""`; `rawPath /api/scoped/tickets/TCK-20261011-e6433610`
       - A5: the A2 caller; `rawPath /api/scoped/tickets/TCK-00000000-00000000`
    4. FIVE invocations, in the order A1, A2, A3, A4, A5: `aws lambda invoke --invocation-type RequestResponse` with the payload
       file. Write each response to a file in your SCRATCH space outside the repository, not under `deliverables/`.
    5. From each response record, in `r6_fn1/RESULT.json` (a list of five objects): the arm; the invoke's own status code; whether
       a `FunctionError` was returned; the function's `statusCode`; and from the body:
       - for a refusal: the values of `error`, `action` and `principal_class` (they name no ticket);
       - for A4 ONLY IF it is 200: the SORTED KEY NAMES of `ticket` and the value of `ticket.status`. NOTHING ELSE of that body is
         written or printed anywhere: no title, description, requester, answers, attachment or event content.
       Expected, from the pair: A1 403, A2 403 with the same `error`/`action`/`principal_class` as A1, A3 403, A4 200, A5 403.
    6. BRANCH C IS A STOP: if A2, A3 or A5 answers anything but 403, STOP at that arm, do not run the remaining arms, file ONE
       row (class BLOCKING, hazard ARMED) and report to `2.0.0_SA_COO~V2` and `1.0.0_SA_CTO~DELL2` at once. A1 answering 200
       (branch B) or A4 answering other than 200 (branch D) is recorded as served and the order CONTINUES.
       An invoke that fails at the AWS call is recorded; ONE retry for a throttle, none otherwise.
    7. AFTER: the reads of step 2 again: ItemCount unchanged, the ticket's `status` and `events` length unchanged. Then delete
       the response files from your scratch space.
    8. Write the proof-of-spec instance in your deliverables folder ROOT (AC1 `PASS-by-output` or as it reads; AC2
       `UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming `3.0.0_SA_CVO`), validate it with
       `python .tools/proof-of-spec-check.py <instance> AC1,AC2`, flip this order to `complete`, write your session log, and report
       once to `2.0.0_SA_COO~V2`: the five function status codes FIRST, the branch, and step 7's two comparisons.
  </go>

  <bounds>
    FIVE GETs and nothing else. No POST, no other route, no other ticket id, no other firm, no sixth call. No row written to any
    table, no token, no secret read, no grant asked, no deploy, no ledger entry. The attached FILE is not read under this order.
    No client data in any tracked file. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (read the file's headings AND its JSON
    ids for the next free `TCKT_VNEXT-D2-S<k>`; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R6-fn-1"><invocation>python -c "import json;d=json.load(open('org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r6_fn1/RESULT.json',encoding='utf-8'));s={x['arm']:x['statusCode'] for x in d};print('FN1-ARMS-OK' if s=={'A1':403,'A2':403,'A3':403,'A4':200,'A5':403} else 'FN1-ARMS-DIFFER %s' % s)"</invocation><expect>FN1-ARMS-OK</expect></criterion>
  <criterion id="AC2" cell_refs="R6-fn-1" judgment="true"/>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the result file does not exist). Name the keys `arm` and `statusCode` in each object so
the check reads it. AC2 (judgment, graded by the CVO at L9 on the result file): FWD-2's ACCEPT for the TICKET, "a person at
another firm cannot open the request": shown by A2, A3 and A5 refused with A4 served as the control. Stated with it by both
halves: the refusal is by class, not by firm; the internal firm fence rests on tests and the runs' census; the attached FILE is
not read by this order.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one pass of five calls, no schedule).
comp-iam: RUN -- the function's resource policy read by the issuer (the API Gateway service only) and the executor's own simulate of lambda:InvokeFunction at step 0; no grant is added.
comp-adversary: RUN -- this order IS the adversarial act: a caller of another firm on the ticket, the list and a missing id, with a served control.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R6-fn-1) under a signed never-widen pair; not a worker cell.
</task_order>
