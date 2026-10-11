# Can the ticket service refuse a still-valid service token? (read only)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. Asked by `1.0.0_SA_CTO~DELL2`: the packager mint's CTO half @65622fbcdc condition 4
("before attach cell 4: one read in code of whether the ticket service can refuse a still-valid token") and the round-14
analysis @c4354a9873 section 3 item 2. Read in code at box/dell2 HEAD; nothing was called.

**Answer: there is no revocation. Nothing in the path can refuse ONE still-valid token. Two switches refuse the packager
whatever token it holds, and one switch refuses every token of every caller.**

## 1. Where a token is judged

The ticket service does not look at the token. `ticket_center/lambda_function.py` `_actor` (lines 293-302) takes the caller
from the portal custom authorizer's context and says so: "the ONLY identity source". `email` is the context's `email`,
`userType` its `userType`.

The authorizer is `infra/aws/users/lambda/portal-authorizer/index.mjs`. For a token that does not claim the render audience
it verifies the signature against the key slots (current, and previous during a rotation), with algorithm RS256, issuer
`opal-portal-auth`, audience `opal-portal-api` (the `verifyWithSlots` call), then builds the context from the claims:
`email: decoded.sub`, `userType: decoded.userType`.

## 2. What it does NOT do

- **No revocation list.** A native search of that folder for `revok`, `denylist`, `blocklist`, `token_version` finds
  nothing. `jti` appears only in the render-token branch's log lines, never as a lookup.
- **No lookup of the subject.** The only table command the module imports is a scan used for the firm hierarchy; the
  subject is not read from the users table, so disabling a user row would not refuse a token. (`svc-irpt-packager` has no
  row in any case.)
- **Expiry is checked only when the token carries one.** The module's own comment on its render branch says the library
  checks `exp` only when present, and the render branch adds an explicit requirement; the branch a service token takes
  does not. **So a service token minted with no `exp` would not expire.** The mint's order says 90 days; its return must
  show the claim NAME `exp` is present and the expiry date, which the order's AC3 already asks.

## 3. What can refuse the packager, and at what cost

| switch | effect | cost | who |
|---|---|---|---|
| `PACKAGE_ALLOWED_FIRMS` set empty on `opal-ticket-api` | the package door refuses every firm, whatever token is presented (`lambda_function.py` line 1454) | one configuration apply; nothing else moves | `2.0.0_SA_COO~V2`'s applier |
| `package_principal` emptied in the type definition | the door refuses everyone (lines 1431-1433) | a code deploy of the ticket service | TCKT_VNEXT |
| the signing key rotated out of BOTH slots | every token signed by it stops verifying | **every signed-in person and every service is signed out**; not a remedy for one token | the key's owner |

The packager's token opens exactly one thing: the package door. No other route names its subject: `principal_class` gives
an unknown service subject the class UNRESOLVABLE, which every other action denies (lines 310-317). So the empty list is a
complete disarm for this token, not a partial one.

## 4. For the mint and for cell 4

- The door reads `actor.email`, and the authorizer fills that from the token's `sub`. The mint's subject must therefore be
  exactly `svc-irpt-packager`, lower case; `email` as a separate claim is not what is read.
- The rotation plan in the mint packet stands: replace the secret's value; the old token stays valid until its own expiry,
  and that is acceptable only because the list is the disarm.

## 5. Not read

The authorizer as DEPLOYED (this is the repo's file; its live bytes were not compared). The REST authorizer
(`portal-rest-authorizer`), which is a different function: which of the two fronts the package route was not read.
