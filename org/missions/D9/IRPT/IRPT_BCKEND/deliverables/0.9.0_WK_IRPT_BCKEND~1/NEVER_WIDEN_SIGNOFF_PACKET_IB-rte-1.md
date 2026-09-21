# NEVER-WIDEN SIGN-OFF PACKET -- IB-rte-1: the bounded test advisor principal

**For:** the two sign-off halves required before IB-rte-2 may create the principal (CLAUDE.md:
never-widen sign-off is CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`. **Prepared by:**
`0.9.0_WK_IRPT_BCKEND~1` (`IRPT_BCKEND.TO-IB-rte-1`). **Andrew-direct 2026-09-18 ~17:3xZ
"Approved"** (record `org/tier1_exec/2.0.0_SA_COO~B/deliverables/ANDREW_DIRECT_20260918_173xZ_TWO_OPEN_CALLS_APPROVED_IRPT_BCKEND.md`
@`af794c77e3`), CTO round-4 analysis s.6/s.8 @`561d6e1cc9`. **Nothing here is applied. This cell
is READ-ONLY on every live plane. Plans only.**

A half signs the **blast radius** of the act below: what each key may touch, and the rollback
for each key. It does not sign an intention. A half that names fewer keys than this packet is
IB-rte-2's stop condition (the same rule `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtc-6.md` states).

---

## The act, in one paragraph

ONE throwaway DynamoDB item in `opal-users-v2` (the production authentication table), carrying
`firmId = 49financial` and an advisor identity that maps to an **EXISTING** advisor already
present in 49financial's own live ownership map (`abby_horton`) -- so **zero new entitlement is
minted anywhere**: no ownership-map row is written, no directory is annotated, no policy
changes. A normal login mints the session (`generateAccessToken()`, the estate's own RS256 path,
never a hand-signed token). The principal is exercised by IB-rte-2 and then **DELETED**, verified
deleted by a consistent read that then finds nothing. This is the SAME lifecycle
`RT2_test_principal_human_gated.md` (`0.9.0_WK_IRPT_BCKEND~2`, 2026-09-11) already named as the
one existing mint path, narrowed here to the firm this round's terminated-client requirement
picks and re-verified live at this vintage.

**WHO EXECUTES IT:** a worker may not walk this path (out of every `<paths>` grant on this
project; a write to the production auth plane; the only alternative is a private-key signature,
which bound 6 forbids -- the three reasons `RT2_test_principal_human_gated.md` gives, unchanged
at this vintage). The operator is `0.7.0_AE_CloudOps` or Andrew, exactly as that record names.

---

## Why 49financial (measured, not assumed)

Terminated-client count per firm, read live this run from each firm's own `latest.json` pointer
(never a hand-typed date):

| firm | bucket | key | as_of | entries | TERMINATED |
|---|---|---|---|---|---|
| **49financial** | `opal-data-bd` | `investor-reporting/directory/2026-09-17/directory.json` | 2026-09-17 | 4,576 | **71** |
| inflection | `opal-data-inf` | `investor-reporting/directory/2026-09-17/directory.json` | 2026-09-17 | 291 | 0 |
| cottonwood | `opal-data-cot` | `investor-reporting/directory/2026-09-17/directory.json` | 2026-09-17 | 260 | 0 (all 260 carry `indicator: "UNKNOWN"`, never `"TERMINATED"` -- filed `IRPT_BCKEND-W1-S24`) |

**49financial is the only firm with >= 1 TERMINATED entry**, so it is the firm this packet plans
against. (The task face's example prefix, `.../directory/2026-09-16/`, is one day stale against
every firm's live `latest.json`, which now reads `2026-09-17` for all three -- filed
`IRPT_BCKEND-W1-S23`; it does not change which firm is chosen.)

---

## The advisor id -- what it actually is, measured against the task face's own assumption

The face asks for "an ISSUED opaque id per bound 13, minted by the same instrument the directory
uses." **Measured: this is not how advisor ids work anywhere in this estate.**
`infra/aws/lambda/investor-reporting/_ids/ids.py` `KINDS = {"account", "relationship", "client",
"firm"}` -- there is no `"advisor"` kind, and bound 13's own enumerated list of typed
identifiers (*"Firm, client, relationship, account, report, export and job ids"*) also excludes
advisor. The real advisor id is a **raw string from the identity plane itself**: the ownership
map's own key (`abby_horton`), matched 1:1 to the JWT's `advisorKey`/`advisorId` claim
(`RT2_test_principal_human_gated.md`'s own citation, `jwt.ts:167-187`) and to the trusted
`X-Advisor-Id` header `_scope/resolve.py:95` reads. **Filed `IRPT_BCKEND-W1-S21`.** The plan
below uses that real shape rather than the face's assumed one.

**Chosen advisor: `abby_horton`** (49financial), an existing key in the live ownership map with
43 granted accounts and 18 granted relationships (measured live this run).

---

## The keys (a half names every one)

| key | object | change | rollback |
|---|---|---|---|
| **K1** | one DynamoDB item, table `opal-users-v2`, `PK = USER#usr_irptrte_<epoch>`, `firmId = 49financial`, `advisorKey`/`advisorId = abby_horton`, e-mail `irpt-rte1-test-<epoch>@opal.test` (the `.test` TLD is reserved, bound 2 untouched), **no phone number, no MFA enrolment** | **create** | `DeleteItem` on the same PK, **verified** by a consistent-read `GetItem` on the same PK returning no `Item` key at all (the precedent's own bar) |
| **K2** | the session access token minted by `generateAccessToken()` (RS256, secret **named** `opal/auth/jwt-private-key`, never read) on a normal login through the real portal auth route | **ephemeral -- never persisted, never logged, never committed** | not a stored resource; it expires on its own TTL. **What must never be recorded:** the token, the `Authorization` header, any `get-secret-value` output (bound 6) |
| **K3 (NOT NEEDED, named so a half cannot assume it)** | an `ownership_map.json` row for `abby_horton` | **NONE** -- the plan reuses `abby_horton`'s EXISTING grant rather than minting a new one | n/a |
| **K4 (NOT NEEDED, named so a half cannot assume it)** | a directory annotation in 49financial's `directory.json` | **NONE** | n/a |

**Blast radius, K1:** the row is readable by whatever the LIVE identity-plane writer census below
already shows can read/write `opal-users-v2`; the row itself grants the bearer of a token minted
against it exactly `abby_horton`'s existing, already-live entitlement in 49financial -- no
broader, no narrower, since no new grant is minted. Deleting it removes the row and every future
login attempt against it; a session token already issued before deletion remains valid only
until its own TTL expires (named, not measured further -- this packet creates nothing to time).
**Blast radius, K2:** the token, while it exists, is indistinguishable from a real
`abby_horton` session to every downstream control (the same property RT2's record names as
"exactly what makes it useful as a test and the exact property that makes it not a worker's to
create") -- which is why K2 is never captured anywhere outside the operator's own session.

---

## The identity-plane writer census (R-44's pattern, `writer_census_ib_rtc_6.py` adapted --
`identity_writer_census_ib_rte_1.py`, run live this turn)

Subject: `dynamodb:PutItem` / `dynamodb:UpdateItem` on
`arn:aws:dynamodb:us-east-1:313476888478:table/opal-users-v2` (79 live items at this run).

- **RESOURCE plane:** no resource-based policy is attached to the table (DynamoDB default);
  authorization is identity-plane only.
- **IDENTITY plane:** **263** principals simulated (256 roles, 7 users), **0** unsimulated,
  **0 UNKNOWN** (111 settled by direct statement reading after the simulator flagged an
  irrelevant missing context key).
- **WRITERS: 6 of 263** -- `opal-news-lambda-role`, `opalinvest-auth-lambda-role`,
  `trade-submission-lambda-role`, and users `Andrew_Berman`, `Andrew_Berman_Console`,
  `Opal_Terminal`. `opalinvest-auth-lambda-role` is the `auth-handler` Lambda's own role -- the
  estate's own mint path, corroborating `RT2_test_principal_human_gated.md`'s citation of
  `auth-handler/src/db.ts:21`.
- **THE BLIND SPOT, NAMED (the face's own words):** this census is IAM-shaped. **An identity
  provider's own ADMIN SURFACE is not IAM** -- if a signup/admin flow inside
  `opalinvest-auth-lambda-role`'s own Lambda accepts calls from a wider population than the six
  IAM principals above (an authenticated admin console session, for instance), this census
  cannot see that population; it would need the Lambda's own authorization surface censused
  separately, which this cell does not do.

---

## What this packet does NOT solve -- named for `3.0.0_SA_CVO` at L9

**Measured live this run, against the REAL `Enforcer` wired EXACTLY as
`infra/aws/lambda/investor-reporting/directory/entry.py` wires it in production
(`deps=_loaders.deps`, `id_projection` NOT passed -- the real, deployed construction, not a
test's):** a real `abby_horton` / `49financial` request is refused **`UNPROJECTED_GRANT`**
(*"43 of 43 ownership grants carry ids in a key space this directory cannot be joined on"*),
**before the served/empty-grant branch is ever reached.** Re-measured for EVERY advisor in the
firm's live ownership map: **0 of 22,646** ownership-map account grants (179 advisors) join the
live directory even WITH `_ids.projection_for` applied by hand -- the ownership map's raw
custodian keys (`z0819594401`-shaped) are not the raw key `_ids/raw_keys.json` declares for
49financial's directory mint (*"the crosswalk's account id, zero-padded to 10 digits"*).
**And separately: 0 of 13 live `entry.py`/`handler.py`/`dispatch.py` modules in this project ever
pass `id_projection` to `Enforcer`/`Entry` at all**, so this refusal is not a property of which
advisor or which firm is chosen -- it fires for every live FIRM_ADVISOR request against real
49financial data today. **Filed `IRPT_BCKEND-W1-S22`, ARMED.** The bounded test principal this
packet plans is still the correct next step (Andrew's word, the CTO's placement, and IB-rte-2's
own exercise of the REFUSAL mechanism itself are all still valid work) -- but it does **not**, by
itself, make FWD-1/FWD-2/FWD-5's SERVED (200) path exercisable against live data, and a reader
who assumed otherwise from the round-4 analysis's s.6(a) framing would be wrong to.

**FWD-11 cannot be exercised by ANY identity today, bounded or not:** the SSM parameter
`/opal/irpt/opal-principal-roster` that `_scope/global.py` reads for the OPAL_GLOBAL roster does
not exist (`ParameterNotFound`, measured live this run). Creating it is a separate infrastructure
act with its own sign-off, prior to either a one-identity or a two-identity plan.

---

## The lifetime bound and the negative controls

**Lifetime:** the principal is created only when IB-rte-2 executes this packet's act, and is
**DELETED at round close by IB-rte-2's own last arm, or earlier on any STOP** -- never a standing
account, per Andrew's word and the CTO's placement.

**Negative controls IB-rte-2 runs (unchanged from `RT2_test_principal_human_gated.md`'s own
design, re-stated here against the firm this round selects):**
1. the resolve/search swapped to `firm_id: "inflection"` (or `"cottonwood"`) -> refused
   `FIRM_BINDING`, the swapped value never echoed;
2. every one of the 11 DECLARED routes' identifier swapped (firm/advisor/account/relationship/
   report/pdf) -> refused, 0 protected bytes;
3. the K1 row deleted, then a consistent-read `GetItem` on the same key -> no `Item` (the
   rollback's own verification, run as a control rather than assumed);
4. a request against the deleted principal's token (if still within its TTL) is a SEPARATE,
   known-open question this packet does not resolve -- a revoked-DynamoDB-row does not
   necessarily invalidate an already-issued JWT before its own expiry, since `resolve_now`
   re-checks the OWNERSHIP GRANT on every request but the ROW's own existence is never itself
   part of `_scope.resolve`'s inputs. Named for IB-rte-2, not solved here.
