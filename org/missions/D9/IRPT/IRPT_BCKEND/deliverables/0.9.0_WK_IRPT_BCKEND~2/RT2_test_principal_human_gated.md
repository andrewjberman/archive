# RT2 ARM (f) -- THE TEST PRINCIPAL IS **HUMAN-GATED**

**Cell:** `IB-rt-2` | **Worker:** `0.9.0_WK_IRPT_BCKEND~2` | **Read at:** 2026-09-11, worktree
`/c/tmp/wk-irpt-2-2` @ `fa89acb5d3`.

**The arm's own rule, verbatim from the face:** *"Either: one authenticated request through the
real path served and one swapped-firm request refused, the principal minted through the named
existing path (secret names only, no values); or: the `HUMAN-GATED` record printed verbatim naming
the operator's exact act -- and the arm reads `HUMAN-GATED`, which is admitted by this criterion
as a PASS of the arm's own rule, never as a skip."*

**The verdict of the Phase-1 read: `HUMAN-GATED`.** A mint path EXISTS and it is named below. A
worker may not walk it, for three reasons that are each sufficient on their own.

---

## PHASE 1 -- WHAT THE ESTATE ACTUALLY HAS

The CTO's ruling asks for "a test principal issued by the existing authorizer's own path under the
existing entitlement class (no new permission, no vendor call)". The path exists, end to end, and
there is even a PRECEDENT for exercising it with a throwaway user:

| link | what it is | where it is |
|---|---|---|
| the authorizer | `opal-portal-authorizer` (`naqxlm`), `index.handler`, `nodejs22.x`, `CodeSha256 KHwksfO1XjL0Jg66kc7L+gFIOEsZT/7l2i8STRgBvS4=` | live, read by `get-function-configuration` |
| what it verifies | RS256 against the secret **named** `opal/auth/jwt-public-key` | `infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs:57` |
| what mints a session | `generateAccessToken()`, RS256 with the secret **named** `opal/auth/jwt-private-key` | `infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts:8,162-193` |
| where a principal lives | DynamoDB table `opal-users-v2` | `infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts:21` |
| the claims the edge reads | `sub`, `name`, `role`, `tier`, `firmId`, `userType`, and the partner identity `advisorKey` / `advisorName` / `advisorRole` / `advisorId` / `firmRole` | `jwt.ts:167-187` |
| the precedent | a throwaway user created, exercised and **VERIFIED-DELETED** in one bounded run | `org/critical_paths/change_management/20260720T1644Z_portal-authhard-wave1-testuser_deploy_completion.md`, by `0.7.0_AE_CloudOps` |

**NO SECRET VALUE WAS READ AND NONE APPEARS HERE.** Every secret above is named; nothing was
fetched. No `get-secret-value` was issued by this cell.

---

## WHY A WORKER MAY NOT WALK IT

1. **IT IS OUT OF THIS ORDER'S `<paths>`.** The grant names five Lambda source dirs, five
   Terraform roots, `_authz/`, `_scope/`, `PATH_MANIFEST.json`, `change_management/`, one sentinel
   and `lambda-source-map.json`. It names no DynamoDB table, no `opalinvest_dev/` path and no
   secret. *"A path you need that is not listed is a BLOCKING row, never an override."*
2. **IT IS A WRITE TO THE PRODUCTION AUTHENTICATION PLANE.** Minting a principal means putting a
   row in `opal-users-v2` -- the table every portal login reads. The precedent run was bounded by
   an atomic create-exercise-delete with a cleanup trap and was performed by the `0.7.0_AE_CloudOps`
   seat that owns that surface. A subagent of another project adding a principal to it, in a
   window where three sibling cells are applying to the same estate, is not the same act.
3. **THE ONLY ALTERNATIVE IS WORSE.** Signing a token directly with `opal/auth/jwt-private-key`
   skips the user table -- and it is a CREDENTIAL USE. Bound 6: *"Secrets are read by NAME at
   runtime."* A worker that reads a private key to mint itself an identity has done the thing the
   bound exists to prevent, and the resulting token would be indistinguishable from a real user's
   to every control downstream. That is the property that makes it useful as a test and the exact
   property that makes it not a worker's to create.

**NO NEW PERMISSION, NO NEW USER POOL, NO VENDOR CALL WAS CREATED OR REQUESTED BY THIS CELL.**

---

## THE OPERATOR'S EXACT ACT

One run, bounded, reversible, and modelled on the precedent that already closed cleanly.

**WHO:** `0.7.0_AE_CloudOps` (or Andrew directly). That seat owns `portal-auth` and has done this
exact lifecycle before.

**WHERE:** the AWS console or CLI for account `313476888478`, `us-east-1`.

**THE ACT, IN ORDER:**

1. **CREATE** one throwaway principal in DynamoDB table `opal-users-v2`, with:
   * `PK` = `USER#usr_irptrt2_<epoch>`, e-mail `irpt-rt2-test-<epoch>@opal.test` (the `.test` TLD
     is reserved and can never receive mail -- bound 2 is not touched);
   * `firmId` = **`49financial`** -- an EXISTING entitlement class, not a new one. This is the
     whole point: the principal must be indistinguishable from a real 49F advisor to the
     authorizer, or it tests something other than the real path;
   * `role` / `userType` / partner identity `advisorKey` = an advisor id that EXISTS in
     `49financial`'s ownership map, so the scope resolves to a real permitted set;
   * **no phone number and no MFA enrolment** -- `mfa.ts:343` keeps a number off the table until
     verification, and this principal must never have one.
2. **LOG IN** through the normal portal auth route so the session is minted by
   `generateAccessToken()` and signed with `opal/auth/jwt-private-key` -- **the estate's own path,
   not a hand-signed token.** Capture the access token in the operator's own session only.
3. **EXERCISE, TWICE, and record only the status line and the public reason code:**
   * `GET https://opalinvest.dev/api/scoped/investor-reporting/directory/search?q=` with
     `Authorization: Bearer <token>` and `X-Contract-Version: v1`
     -> **EXPECTED: HTTP 200**, body `{contract_version:"v1", operation:"directory-search",
     firm_id:"fir_...", data:[...]}`;
   * the same request with the body carrying `"firm_id": "inflection"`
     -> **EXPECTED: refused, `status.public_reason_code = "FIRM_BINDING"`, `data` absent, and the
     string `inflection` NOWHERE in the response.**
4. **DELETE** the row and **VERIFY THE DELETE** with a consistent-read `GetItem` that returns no
   `Item` -- the precedent's own bar. The principal's lifetime is bounded by the run.

**WHAT MUST NEVER BE RECORDED:** the token, the private key, any `get-secret-value` output, or the
`Authorization` header. The two status lines and the two reason codes are the whole evidence.

**THE PRECONDITION THIS RECORD CARRIED IS NOW MET, AND THE PARAGRAPH IT REPLACES SAID OTHERWISE.**
When this record was written the guarded entry points were COMMITTED AND NOT SERVED (rows
`IRPT_BCKEND-W2-S21`, `W2-S22`, `W2-S24`), so the act above would have produced a passing-looking
200 from the very code this cell exists to replace. **That is no longer the vintage.** Six roots
were applied one at a time and each verified on its SERVED bytes before the next was touched
(ledger `irpt-bckend-rt2`, CLOSED, 12 legs): `entry.lambda_handler` is the live handler on 6 of 6,
`artifact_sha256 == S3 content-sha256 == live CodeSha256` on 6 of 6, and 6 of 6 import in the flat
`/var/task` layout from their served bytes with the repo off `sys.path`. **So the operator act is
now LIVE-READY for the six.** The one route still on its old handler is `irpt-holdings`, whose
mark is written and held (row `IRPT_BCKEND-W2-S41`); an operator exercising the directory route
above is unaffected by that.

---

## WHAT THE ARM STILL PROVES WITHOUT THE PRINCIPAL

The authorization decision itself is exercised end to end in process, 30 times, against the REAL
entry points with the REAL guard, the REAL Enforcer and the REAL scope resolver -- see
`_authz/tests/test_guarded_entries.py` and the battery's arms (b), (c) and (d). What the in-process
run cannot show is exactly what this record hands to the operator and to `IB-rtb-1`: that the EDGE
VALIDATOR injects the headers the boundary trusts, for a token the AUTHORIZER accepted, on the
deployed function.


---

# RT2 ARM (g2) -- SERVED ENVELOPE CONFORMANCE IS **HUMAN-GATED**, ON THE SAME PRINCIPAL

**Ruled by the issuer, amendment 3 C2 and re-confirmed at amendment 4:** *"g2 depends on the SAME
principal and therefore takes the SAME treatment -- write it HUMAN-GATED with the exact operator
act and its expected reading. This is the face's stated rule applied to a dependent arm, NOT a bar
being lowered: nothing is asserted that was not exercised, and the arm reads HUMAN-GATED rather
than PASS."*

## WHY IT CANNOT BE MEASURED WITHOUT THE ACT ABOVE

Arm (g) has two halves and only one of them needs a principal.

| half | what it needs | state |
|---|---|---|
| the version check, SERVED | any request the boundary refuses BEFORE reading anything | **MET, 11 of 11** on the deployed functions |
| a SUCCESS response validating against `responses/<operation>.response.schema.json` | a principal the EDGE VALIDATOR accepts | **HUMAN-GATED** -- this record |

**AND THE WRONG WAY TO CLOSE IT IS THE EASY ONE.** Invoking a deployed function by name with a
FABRICATED advisor id returns a refusal, not a response. A refusal cannot validate against a
response contract at all (row `IRPT_BCKEND-W2-S25`, RULED), so counting that as conformance would
be recording the opposite of what the arm asks. The arm reads `HUMAN-GATED` instead.

## THE OPERATOR'S EXACT ACT FOR g2 -- ONE MORE READ ON THE SAME SESSION

**WHO / WHERE:** the same seat and account as the act above -- `0.7.0_AE_CloudOps` or Andrew,
account `313476888478`, `us-east-1`. **This is step 3b of that run, not a second run:** it uses the
token minted in step 2 and is covered by the same bounded create-exercise-delete.

**THE ACT:** with the same `Authorization: Bearer <token>` and `X-Contract-Version: v1`, issue ONE
authorized GET per deployed operation and keep ONLY the pass/fail of a schema validation:

1. `GET /api/scoped/investor-reporting/directory/search?q=`
2. `POST /api/scoped/investor-reporting/directory/resolve` with a selection of accounts the
   principal's own ownership map grants
3. `GET /api/scoped/investor-reporting/performance/{accountSetId}` for one such account
4. `GET /api/scoped/investor-reporting/narrative/{reportId}` for a report of that firm
5. `GET /api/scoped/investor-reporting/status` and `GET .../status/{jobId}`
6. `GET /api/scoped/investor-reporting/export/{exportId}` for a receipt of that firm

**EXPECTED READING, per operation:** HTTP 200 and a body that validates against
`docs/contracts/investor-reporting/v1/responses/<operation>.response.schema.json` -- the ONE
envelope `{contract_version:"v1", operation, firm_id:"fir_...", data, status?}` with
`additionalProperties: false`, and `data` validating against the producer document's own schema.
**The `firm_id` MUST be the ISSUED OPAQUE id (`fir_...`), never the registry spelling** -- that
distinction is what rows `W2-S27` and bound 13 exist for, and it is the one field a reader can
check at a glance.

**WHAT TO RECORD:** per operation, the HTTP status, the `operation` string, whether the body
validated, and the FIRST validation error if it did not. **NOT the `data` payload** -- these are
real client holdings, and this arm needs the verdict, not the bytes.

**THE TWO POST ROUTES ARE EXCLUDED AND NAMED:** `POST /analysis` (`analysis-requests`) and
`POST /export` (`submit-export`) ENQUEUE work. Bound 1 forbids a live vendor call and bound 2
forbids this project notifying anyone, and an enqueued analysis job is the head of a chain that
ends in a YCharts call. **They are excluded on their own line and counted as neither a pass nor a
fail** -- exactly as the no-handler route is in arm (a). An operator who wants them covered needs
Andrew's per-use word first, and that is a different decision from this one.

**AND WHAT THIS STILL WILL NOT PROVE:** `export-download` returns a signed URL; its parameters are
never logged (bound 6), so the arm records only that the envelope validated.

## THE VERDICT

**`HUMAN-GATED`.** The same three reasons that gate arm (f) gate this: the principal is out of this
order's `<paths>`, minting one writes to the production authentication plane, and the alternative
is a worker using a private key to mint itself an identity. Nothing here is asserted as measured:
the in-process paired arms stand on their own and are reported separately, and the served half
waits on one bounded operator run.
