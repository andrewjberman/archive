# TCKT_VNEXT R6-fn-1 -- FWD-2's live proof by DIRECT INVOKE of the deployed ticket function: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~22:5xZ. **Authority:** the CTO's round-6 analysis
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_TCKT_VNEXT_ROUND_6_20261011.md` @0b932076f0, section 3 item 2, and CTO
msg 5987: "a DIRECT INVOKE of the deployed ticket function with a constructed context ... A client of firm B asking for firm A's
ticket, expect the refusal; its twin of firm A, expect served, status and key names only. No identity minted, no grant; who may
invoke is read first. Its pair to me." Cell `R6-fn-1` of `decompositions/TCKT_VNEXT_DECOMP_R6.md`.

**ONE EXPECTATION IN THAT RULING DOES NOT HOLD, READ FROM THE HANDLER'S OWN RULE BEFORE SIGNING: the twin is NOT served.** Section 3.

## 1. Measured at signing (2026-10-11 22:4xZ, by this seat)

| item | value | instrument |
|---|---|---|
| who may invoke `opal-ticket-api` directly: its RESOURCE policy | ONE statement, `AllowPortalAPIGatewayInvoke`: the API Gateway service, `lambda:InvokeFunction`, source ARN the portal API's `*/*` | `aws lambda get-policy` (one function) |
| who may invoke it directly: THIS box's identity | `cloudops-dell2-agent-user`: `lambda:InvokeFunction` `allowed`, `lambda:GetFunction` `allowed` | `iam simulate-principal-policy` on this box's own ARN and the function's ARN |
| who ELSE may invoke it directly | NOT READ: other identities' policies cannot be read or simulated from this box. Every administrator of the account can, by CTO msg 5396's finding | -- |
| the function live | CodeSha256 `Ob/MZBEO...`, 2026-10-11T22:16:38Z, deployed handler `b7764fbd` | `get-function-configuration`; `clamp_precheck.py` at 22:3xZ |
| the ticket to ask for | `TCK-20261011-e6433610`: firm `49financial`, completed, the fifth run's journey ticket, a test artifact of a synthetic filer | the run-5 trace |

**So no grant is needed and none is made: the applier's identity may already invoke the function, by its identity policy. A direct
invoke goes AROUND the portal authorizer: the caller's identity is whatever the event says. That is the instrument, and it is also
the fact this pair states plainly: any holder of `lambda:InvokeFunction` on this function can be any caller.**

## 2. How the handler reads its caller (the rule each expectation below is read from)

`infra/aws/lambda/ticket_center/lambda_function.py` at the live build (`b6fcebb514`): `_actor` (lines 300-309) takes `email`,
`userType`, `firmId`, `allowedFirmIds` from `event.requestContext.authorizer.lambda`. `principal_class` (312-330): a non-service
caller whose `firmId` is `opal-capital` is INTERNAL; any other non-null `firmId` is CLIENT. `get_ticket` (1233-1244):
`authorize("GET", actor)` FIRST; the matrix admits INTERNAL only. Then, for an INTERNAL caller, the firm scope is the caller's own
users PROFILE row, read by email: no row means no scope (line 376-377), and a ticket outside a scope answers 404.

## 3. The arms, each expectation read from that rule

| # | constructed caller | call | expected, from the code | what it shows |
|---|---|---|---|---|
| A1 (FIRST) | CLIENT, `firmId 49financial`, email `tckt-fwd2-probe-a@opal.invalid` | GET the ticket | **403**, body `error`, `action GET`, `principal_class` the client class. **NOT served** | the CTO's twin. A client of the ticket's OWN firm cannot open it either: GET is internal-only by the matrix |
| A2 | CLIENT, `firmId cottonwood`, email `tckt-fwd2-probe-b@opal.invalid` | GET the same ticket | **403**, the SAME status and body as A1 | FWD-2's sentence, "a person at another firm cannot open the request": true, and by CLASS, not by firm |
| A3 | the A2 caller | GET the list | **403** | the other firm's person does not see it in a list |
| A4 (the control that a served answer can be read) | INTERNAL, `firmId opal-capital`, email `tckt-fwd2-probe-internal@opal.invalid`, which has NO users row | GET the ticket | **200**; recorded: the status, and the SORTED KEY NAMES of `ticket` only, never a value | the instrument can tell a refusal from a served answer on this ticket. It is NOT a proof of the firm fence |
| A5 | the A2 caller | GET `TCK-00000000-00000000`, an id that does not exist | **403**, the same as A2 | a client cannot tell an existing ticket from a missing one |

**What this run CANNOT show, said before it runs:** the firm fence for an INTERNAL caller (a staff person whose users row lists
firm B, asking for firm A's ticket: 404). That needs a users row with a firm list for the constructed email, which is an identity
written to a table; this pair writes none. It is proven by tests (`tests/test_profile_firm_scope.py`, 13 tests;
`tests/test_fence_other_firm.py`, 4 tests) and was exercised live by the synthetic filer's census in runs 1 to 5 (the filer's row
listed `49financial` only; other firms' routes refused). **A4 also shows, again, what row TCKT_VNEXT-D2-S20 found: an internal
caller with no users row is unscoped.**

## 4. The act (executor `0.7.0_AE_CloudOps~TV2`; read-only against the ticket table)

0. NO deploy ledger entry: nothing is deployed. The executor states in its log that it holds `lambda:InvokeFunction` by its
   own simulate, and reads every live worktree's `.open_deploys/`: an open entry naming `opal-ticket-api` is a STOP (no direct
   invoke while an apply is in flight).
1. The live CodeSha256 starts with the prefix THE ORDER NAMES (read by this seat at the GO).
2. FIVE invocations, `aws lambda invoke` with `RequestResponse`, in the order A1, A2, A3, A4, A5, each with a payload built as
   API Gateway's payload 2.0 shape: `rawPath`, `requestContext.http.method`, `requestContext.authorizer.lambda` holding exactly
   `email`, `name`, `userType`, `firmId`, `allowedFirmIds`. Every method is GET. No body. Each payload is written to the
   executor's deliverables folder BEFORE the call, so what was sent is on record.
3. For each answer record: the invoke's own status, the function's `statusCode`, and from the body: for a refusal the `error`,
   `action` and `principal_class` values (they name no ticket); for A4 the sorted key names of `ticket` and its `status` value
   ONLY. **The body of A4 is not written to any file and no other value of it is printed.**
4. After: `opal-tickets` ItemCount unchanged against a before-read; the ticket's `status` and `events` LENGTH unchanged (a GET
   writes nothing; this is the read that says so).

## 5. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-tickets` | NOTHING: five GETs. `get_ticket` and `list_tickets` write no item | none needed; step 4 reads it |
| `opal-users-v2` | NOTHING written. A4 makes one read of the email index for an address that has no row | none |
| the function's log group | five invocations' lines, carrying the constructed emails (`.invalid` addresses) and no client data | none; they are true records of the act |
| a real person's view of anything | nothing: no notice is sent by a GET, no ticket changes | none |
| the ticket's content | A4's 200 carries a synthetic filer's test ticket to the executor's process; only key names and the status are kept | the body is not persisted |

No identity is minted, no token is made, no row is written, no grant is added, nothing is deployed.

## 6. Branches (all signed)

- **A.** All five answers as section 3 expects. FWD-2 goes to the CVO stated exactly so: another firm's person is refused, by
  class; the internal firm fence is proven by tests and by the runs' census, not by this act.
- **B.** A1 answers 200 (a client of the ticket's own firm IS served): a finding, not a failure of the act; recorded as served,
  key names only; the order of the remaining arms is unchanged.
- **C.** A2, A3 or A5 answers anything but 403: **STOP at that arm, a BLOCKING and ARMED row at once**, reported to the CTO before
  anything else. The remaining arms are not run.
- **D.** A4 answers anything but 200: recorded as served; the run's claim "a served answer can be read" is then NOT made, and the
  three refusals stand unpaired. No retry.
- **E.** An invoke fails at the AWS call (access denied, throttled): nothing reached the function; recorded; no retry beyond ONE
  for a throttle.

ONE pass of five calls.

## 7. What must hold before an order cites this pair

1. The CTO half matches this text, and accepts or re-rules section 3's A1 (the twin is refused, not served).
2. No apply of `opal-ticket-api` is in flight; this seat re-reads the live CodeSha256 at the GO and writes it in the order.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11, for the blast radius in section 5 and branches A-E, on the conditions of section 7.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
