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

**AND ONE THING THIS RUN WILL NOT PROVE, stated so it is not over-read:** it exercises the REAL
path only once `IB-rt-2`'s deploy has landed. At this vintage the guarded entry points are
COMMITTED AND NOT SERVED (rows `IRPT_BCKEND-W2-S21`, `W2-S22`, `W2-S24`), so today the same request
would reach the OLD unguarded handler and answer in its ad-hoc envelope. **The operator act above
belongs AFTER the deploy, not before it** -- running it now would produce a passing-looking 200
from the very code this cell exists to replace.

---

## WHAT THE ARM STILL PROVES WITHOUT THE PRINCIPAL

The authorization decision itself is exercised end to end in process, 30 times, against the REAL
entry points with the REAL guard, the REAL Enforcer and the REAL scope resolver -- see
`_authz/tests/test_guarded_entries.py` and the battery's arms (b), (c) and (d). What the in-process
run cannot show is exactly what this record hands to the operator and to `IB-rtb-1`: that the EDGE
VALIDATOR injects the headers the boundary trusts, for a token the AUTHORIZER accepted, on the
deployed function.
