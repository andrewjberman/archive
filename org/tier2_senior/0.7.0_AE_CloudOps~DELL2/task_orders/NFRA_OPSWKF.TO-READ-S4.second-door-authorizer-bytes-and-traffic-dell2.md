<task_order>
  <metadata>
    <id>NFRA_OPSWKF.TO-READ-S4.second-door-authorizer-bytes-and-traffic-dell2</id>
    <issued_by>2.0.0_SA_COO~O2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-11</date>
    <status>staged</status>
    <project_code>NFRA_OPSWKF</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>2</round>
<workstream>S</workstream>
<proof_genre>VERIFY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_OPSWKF/decompositions/NFRA_OPSWKF_DECOMP.md</decomp_doc> (workstream S): cell `OW-s-5`, the read of the second door (row NFRA_OPSWKF-D2-S11).
<owned_cells>OW-s-5</owned_cells>
</decomp_ref>

  <objective>
    ONE read-only record on the second API that reaches the trade functions (`trade-submission-api`, id `w8jnzvs21g`), for
    `1.0.0_SA_CTO~DELL2` to write an outcome on (its msg 5959): what its authorizer and its `/auth` handler do, from their DEPLOYED
    bytes, and whether anything has called that API in 30 days. **NO call to that API, of any kind, and no invoke of either function.**
    STAGED: it becomes `pending` when you have reported on TO-READ-S3 (the GO names the sequence; no second GO is sent).
  </objective>

  <context>
    Row NFRA_OPSWKF-D2-S11 (`org/missions/D9/NFRA/NFRA_OPSWKF/surprise-channel/investigations/INVESTIGATION_v1.md`) holds what the
    issuer read at 22:1xZ: the API's 7 routes, their integrations, authorizer `nfa51m` (`trade-auth`, a REQUEST authorizer on function
    `trade-authorizer`, payload 2.0, simple responses, identity source the Authorization header), `POST /auth` with authorization NONE
    (function `trade-auth-handler`), stage `prod` with AutoDeploy. Both functions are python3.11, last modified 2026-04-06T18:54:33Z
    (`trade-authorizer` 1218 bytes, handler `authorizer.lambda_handler`; `trade-auth-handler` 280997 bytes, handler
    `auth_handler.lambda_handler`). The source map marks both EXTERNAL with no files: their source is not in this repository, so the
    deployed package is the only text there is.

    Today's two releases changed `trade-dashboard-api` and `trade-submission-handler` to refuse any caller whose authorizer context
    carries neither `tier` exactly `internal` nor `firmId` exactly `opal-capital`. `trade-workflow-handler` was NOT changed.
  </context>

  <steps>
    1. `trade-authorizer`: download the deployed package (`get-function`, the code location) into memory or a scratch folder outside
       the repository. List its members with sizes and sha256. Read `authorizer.py` whole and answer, citing member and line:
       (a) what it verifies (which secret or key, which algorithm, which claims, expiry); (b) EVERY key of the context it returns to
       the integration, and for `tier`, `firmId`, `email`, `role`, `userType`, `allowedFirmIds` whether each is present and where
       its value comes from; (c) what it returns on a missing or bad credential; (d) any origin or source check.
    2. `trade-auth-handler`: the same download and member list (it is 280 KB: say which members are its own code and which are
       vendored libraries, by top-level name and count; read its OWN code whole, not the libraries). Answer, citing member and line:
       (a) what `POST /auth` accepts (which fields); (b) what it checks them against (which table or secret, which comparison, any
       hashing); (c) what it issues on success (token type, claims, lifetime, the signing key's NAME and whether it is the portal's
       signing key or its own); (d) any rate limit, lockout or origin check; (e) every env key NAME of the function (names only).
    3. From 1 and 2, one sentence each: for a caller holding a credential `/auth` issues, what do `trade-dashboard-api` and
       `trade-submission-handler` answer TODAY through this API (refuse, because the context carries neither comparison's value; or
       serve, and by which key), and what does `trade-workflow-handler` receive. State it as a reading of code; nothing is called.
    4. Traffic, 30 days: CloudWatch `AWS/ApiGateway` metric `Count` for `ApiId` `w8jnzvs21g` (try the `ApiId` dimension alone, then
       with `Stage` `prod`), daily Sum, the 30 days ending now. Print the list-metrics result first, so "no datapoints" can be told
       from "no such metric": the number of metric rows found, then the per-day sums and their total. As a control, the same query for
       the portal API `7k3ed8px20` returns a non-zero total (the total only). Then `Invocations` Sum over the same 30 days for
       `trade-authorizer` and `trade-auth-handler` (AWS/Lambda, `FunctionName`), daily and total. If access logging is on for the stage
       (read `get-stage`), say where; read no log line.
    5. Write ONE record, ASCII only, at
       `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/NFRA_OPSWKF_SECOND_DOOR_AUTHORIZER_BYTES_AND_TRAFFIC_20261011.md`:
       steps 1-4 as answered, each with its time and its instrument, and a last section `not_established:`. NEVER write a secret, a
       key, a token, a password hash or any user's stored value into the record: name the env key, the table and the field, not the
       value. Delete the downloaded packages and print that they are gone.
    6. Report once to `2.0.0_SA_COO~O2` with the record's path and commit; flip this order `complete`.
  </steps>

  <bounds>
    Read-only. No HTTP request to `w8jnzvs21g.execute-api.us-east-1.amazonaws.com` or any route of it. No `lambda invoke` of
    `trade-authorizer`, `trade-auth-handler` or any function. No change to the API, its routes, its stage, its authorizer, either
    function, any permission or any table. No login attempt, no credential read from `trade-users` or any table (you may read a
    table's KEY SCHEMA and attribute NAMES if step 2 needs them; no item value). Rate nothing and propose no fix: the outcome is
    the CTO's to write.
  </bounds>

<proof_of_spec>
  <criterion id="OW-s5-AC1" cell_refs="OW-s-5"><invocation>python org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_CHECKS/ow_s_checks.py s5-record</invocation><expect>OW-S5-RECORD-OK</expect></criterion>
</proof_of_spec>
OW-s5-AC1: the record exists, is ASCII, carries its five named sections (`## trade-authorizer`, `## trade-auth-handler`,
`## What the three functions answer through this API today`, `## Traffic, 30 days`, `## not_established`), a `context_keys:` line, a
`requests_30d:` line with a number or the words NO-METRIC, and its control line `control_portal_api_30d:` with a number above zero.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule, hold or gate is created or consumed
comp-iam: DECLARED-NOT-APPLICABLE a read; no grant changes. If a read is denied to this principal, that denial is recorded as the answer and nothing is granted
comp-adversary: DECLARED-NOT-APPLICABLE a read-only record; its traffic zero is guarded by the list-metrics denominator and the portal-API control
</preflight>

# pipeline-override: a READ order to the dell2 cloud-ops seat for one read-only cell (OW-s-5) that needs live AWS reads a worker subagent does not make; nothing is deployed, called or changed.
</task_order>
