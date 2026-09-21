# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtf-9: the bounded test advisor principal, re-declared on the deployed mint path (two keys, not one)

**For:** the two sign-off halves required before IB-rtf-3 may create the principal (CLAUDE.md never-widen: CTO + COO): `1.0.0_SA_CTO` and `2.0.0_SA_COO~B`.
**Prepared by:** `0.7.0_AE_CloudOps~V` (`IRPT_BCKEND.TO-IB-rtf-9`).
**Authority for the act:** Andrew-direct 2026-09-18 ~17:3xZ *"Approved"* (record `org/tier1_exec/2.0.0_SA_COO~B/deliverables/ANDREW_DIRECT_20260918_173xZ_TWO_OPEN_CALLS_APPROVED_IRPT_BCKEND.md` @af794c77e3). It covers one BOUNDED test principal under both halves, deleted at round close.
**Replaces the key list of:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/NEVER_WIDEN_SIGNOFF_PACKET_IB-rte-1.md`, blob `3d9f57335b9893753973132ba5c4958b2622e24f` (row IRPT_BCKEND-S86).

**NOTHING IS CREATED BY THIS PACKET.** It is a declaration. Every line citation below is at `@b95c935160`, the HEAD the battery read.

A half signs the **blast radius** of the act below: what each key may touch, and the rollback for each key. It does not sign an intention. A half that names fewer keys than this packet is IB-rtf-3's stop condition.

---

## What changed from the first packet, and why

The first packet shaped K1 as one `opal-users-v2` item carrying `advisorKey/advisorId = abby_horton`. The deployed login never reads those attributes from that row.

- **Where the advisor claim really comes from.** The deployed `opalinvest-auth-handler` (zip sha256(b64) `h1tnQVRpRA52eWyfAia6CfBsJmn6xKwHa8IUC0zBSsQ=`, equal to the live `CodeSha256`) takes the token's `advisorKey` and `advisorId` only from `opal-partner-<firm>`, via `GetItem Key {email}`:
  - `infra/aws/lambda/lib/partner/index.ts:21-37 @b95c935160`
  - `infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts:29-54 @b95c935160`
  - `auth.ts:202-216 @b95c935160`
  - `jwt.ts:179-185 @b95c935160`
- **The user row carries no advisor field.** `getUser()` maps none from `opal-users-v2` (`db.ts:138-167 @b95c935160`).
- **No login is bound to `abby_horton` today.** 0 of 11 `opal-partner-49financial` rows carry `advisorKey = abby_horton` (IB-rtf-3, 08:29:50Z).

**So the principal is TWO rows, not one: K1 is the login, K1b is the advisor binding.** The entitlement the halves sign is unchanged: exactly `abby_horton`'s existing grants in 49financial, with no new grant in the ownership map. What changed is the **key list** and therefore the **writers** counted.

**Why not the estate's own provisioning script.** `users/scripts/create_user_v2.py` writes both rows. It is not used, for three reasons:
- It refuses a 49financial e-mail outside `@49financial.com` (`create_user_v2.py:63, 119-129 @b95c935160`), so it cannot mint a reserved `.test` e-mail.
- It writes a third item that nothing on the mint path reads (named below).
- It sends an SES verification e-mail unless `--no-ses` is passed, and bound 2 forbids any send.

The two rows are therefore declared as direct `PutItem` shapes, as the 2026-07-20 precedent did (`org/critical_paths/change_management/20260720T1644Z_portal-authhard-wave1-testuser_deploy_completion.md`).

---

## K1 -- ONE `opal-users-v2` PROFILE item (the login)

Only fields the deployed `getUser()` reads, and only those the act needs.

| attribute | value | the line that reads it | sense |
|---|---|---|---|
| `PK` | `USER#usr_irptrte_<epoch>` | `db.ts:130 @b95c935160` | `getUser` reads the PROFILE item by PK after the e-mail lookup |
| `SK` | `PROFILE` | `db.ts:130 @b95c935160` | the sort key read |
| `email` | `irpt-rte1-test-<epoch>@opal.test`, lower-case | `db.ts:87 @b95c935160` (email-index GSI); `auth.ts:86 @b95c935160` (lower-cased); `jwt.ts:173 @b95c935160` (`sub`) | the login key; the reserved `.test` TLD never receives mail |
| `passwordHash` | bcrypt of a random password generated at run time, **never recorded** | `db.ts:140 @b95c935160`; `auth.ts:95 @b95c935160` | the only credential the login checks |
| `name` | `IRPT test principal (IB-rtf-3)` | `db.ts:141 @b95c935160`; `jwt.ts:174 @b95c935160` | the token's `name` claim |
| `role` | `user` | `db.ts:142 @b95c935160`; `jwt.ts:175 @b95c935160` | `admin` would bypass the edge advisor check (`auth-validator-edge/index.mjs:201 @b95c935160`), be FIRM_OPERATIONS on IRPT (`_scope/resolve.py:186-192 @b95c935160`), and add descendant firms at the API authorizer (`portal-authorizer/index.mjs:145-150 @b95c935160`) |
| `firmId` | `49financial` | `db.ts:143 @b95c935160`; `auth.ts:209 @b95c935160`; `jwt.ts:169 @b95c935160` | selects `opal-partner-49financial`; tier `advisor`, not `internal` (`jwt.ts:168 @b95c935160`) |
| `status` | `active` | `db.ts:145 @b95c935160`; `auth.ts:105 @b95c935160` (login), `:537` (refresh) | any other value refuses both |
| `createdAt` | ISO instant of creation | `db.ts:147 @b95c935160`; `jwt.ts:222 @b95c935160` | the refresh token's row binding |
| `createdBy` | `0.7.0_AE_CloudOps~V IB-rtf-3` | `db.ts:148 @b95c935160` | provenance only; the census marker that finds the row |

**Deliberately ABSENT on K1:**

| attribute | why absent | the line that reads it |
|---|---|---|
| `userType` | `Dev` is superadmin and gets ALL firms at the authorizer (`portal-authorizer/index.mjs:127-130 @b95c935160`). Absent means no claim. | `db.ts:144`, `jwt.ts:178`, `types.ts:44 @b95c935160` |
| `mfaChannel` / `mfaEnabled` | Absent reads `none`/`false`, so the MFA gate is skipped and **nothing is sent** | `db.ts:160-161`, `auth.ts:115 @b95c935160` |
| `phoneNumber` / `phoneVerifiedAt` | no phone on the row | `db.ts:162 @b95c935160` |
| `mustChangePassword` | absent reads `false` | `db.ts:146 @b95c935160` |
| `advisorKey` / `advisorId` | **dropped from the first packet's K1**: `getUser` reads no advisor field, so written here it would never be read | `db.ts:138-167 @b95c935160` |

**NOT NEEDED, named so a half cannot assume it:** the `FIRM#49financial / MEMBER#<userId>` item that `create_user_v2.py` and `createUser()` also write (`db.ts:220-228 @b95c935160`). Nothing on the login, refresh or `/auth/me` path reads it. Without it, the test login does not appear in firm-member listings, which is narrower.

**ROLLBACK -- K1:** `DeleteItem` on `{PK, SK: PROFILE}`, **verified** by a consistent-read `GetItem` on that key returning no `Item` key at all. The e-mail-index GSI is eventually consistent, so the verifying read is the base-table `GetItem`, never the index. `opal-users-v2` has point-in-time recovery on (`shared-infra/dynamo.tf:70 @b95c935160`), so the deleted item survives in PITR backups for the retention window. Named, not a defect.

---

## K1b -- ONE `opal-partner-49financial` item (the advisor binding)

Exactly what the deployed reader needs for the claim to be minted, and nothing else.

| attribute | value | the line that reads it | sense |
|---|---|---|---|
| `email` | the SAME e-mail as K1 | `lib/partner/index.ts:27 @b95c935160` (`GetItem Key {email}`); table HASH key `modules/partner-firm-table/main.tf:24 @b95c935160` | the partner lookup key |
| `advisorKey` | `abby_horton` | `lib/partner/index.ts:31 @b95c935160`; `db.ts:49 @b95c935160`; `jwt.ts:180, 183 @b95c935160` | becomes the token's `advisorKey` AND `advisorId`, then `X-Advisor-Id`, then FIRM_ADVISOR (`_scope/resolve.py:193-194 @b95c935160`) |

**Deliberately ABSENT on K1b:**

| attribute | why absent | the line that reads it |
|---|---|---|
| `firmRole` | Absent means no `firmRole` claim (`db.ts:47`). `admin` would bypass the edge advisor check (`auth-validator-edge/index.mjs:206 @b95c935160`) and the backend tier and L1 scope (`opal-partners-data/lambda_function.py:163-170, 1675-1694 @b95c935160`). | `lib/partner/index.ts:30`, `db.ts:47 @b95c935160` |
| `advisorRole` | Absent reads `''`, so the principal is FIRM_ADVISOR on IRPT and never FIRM_OPERATIONS (`_scope/resolve.py:186 @b95c935160`). On the advisor-intelligence routes it is level 0, so L0 only (`tier_policy.mjs:55-67 @b95c935160`). It also stays out of the sparse `ByAdvisorRole` index (`modules/partner-firm-table/main.tf:36-40 @b95c935160`), which has 0 code readers. | `db.ts:51 @b95c935160` |
| `advisorName` | display only; absent reads `''` | `db.ts:50 @b95c935160` |
| `createdAt` / `createdBy` / `updatedAt` | nothing on the mint path reads them; a field nothing reads is not a key | (the reader reads only `firmRole` and `advisorKey`, `lib/partner/index.ts:30-31 @b95c935160`) |

**ROLLBACK -- K1b:** `DeleteItem` on `{email}`, **verified** by a consistent-read `GetItem` returning no `Item`. The table's `deletion_protection_enabled` guards the TABLE, never an item (`modules/partner-firm-table/main.tf:62 @b95c935160`). PITR is on (`:58-60`), so the item survives in backups for the retention window. Named.

---

## K2 -- the session (ephemeral; never persisted, logged or committed)

- **The access token** is minted by a normal login through the real portal route (`auth.ts:216 @b95c935160`, RS256, the private key read by NAME). Its TTL is **15 minutes** (`jwt.ts:17 @b95c935160`). It carries `sub, name, role=user, tier=advisor, firmId=49financial, advisorKey=advisorId=abby_horton` and no `userType`, `firmRole` or `advisorRole`.
- **The refresh token** has a TTL of 7 days (`jwt.ts:18 @b95c935160`). Its `sub` is bound to K1's `PK + createdAt` (`jwt.ts:220-224 @b95c935160`). A refresh re-reads the row (`auth.ts:483-537 @b95c935160`), so **it dies with K1**. `/auth/me` also re-reads the row (`auth.ts:558-566 @b95c935160`).
- **Side effects of the login**, all inside the radius:
  - `updateLastLogin` writes `lastLogin`/`updatedAt` on K1 (`db.ts:239-247 @b95c935160`), deleted with K1.
  - A SUCCESSFUL login issues `DeleteItem` on the throttle counter keyed by the e-mail's hash (`throttle.ts:170-173 @b95c935160`), which creates nothing.
  - A FAILED login would create one counter item with a TTL (`throttle.ts:132-137 @b95c935160`). If one is created, it is named in the ledger.
- **What must never be recorded:** the token, the `Authorization` header, the password, any `get-secret-value` output (bound 6). The `exp` of each access token IS recorded, because the interval closes on it.

---

## The census of `opal-partner-49financial` -- the property the first packet never counted

**WRITERS, identity plane.** Every IAM role and user was simulated for `PutItem/UpdateItem/DeleteItem/BatchWriteItem` on the table ARN, one resource ARN per call (battery `battery_ib_rtf_9.py`, first run 2026-09-19T09:05Z):

- **Resource plane:** no resource-based policy on the table.
- **Population:** 263 principals simulated (256 roles, 7 users), 0 unsimulated, **0 UNKNOWN**. 112 were settled by reading their statements.
- **Controls:** the positive control (user `Andrew_Berman`, administrator) is a writer, and the negative control (`opalinvest-auth-lambda-role`, GetItem-only grants at `portal-auth/iam.tf:136-143` and `shared-infra/main.tf:262-282 @b95c935160`) is not.

CENSUS-WRITERS: 4 of 263

| principal | kind | actions | note |
|---|---|---|---|
| `Andrew_Berman` | user | all four | the operator identity this seat holds |
| `Andrew_Berman_Console` | user | all four | human |
| `Opal_Terminal` | user | all four | terminal |
| `opal-news-lambda-role` | role | all four | a NEWS Lambda's role that can write a partner identity table. It sits outside this act, and the first packet noted the same role on `opal-users-v2`. **An IAM finding for the IAM owner, not absorbed here.** |

**Code writers:** `users/scripts/create_user_v2.py` (`_write_partner_table`, `:202-228 @b95c935160`), reached from three operator wrappers: `users/scripts/partners/provision_49financial.py`, `provision_cottonwood.py` and `provision_inflection.py`, via `partner_contracts.py`. All are operator scripts, run by whoever holds the IAM writes above.

**Blind spot, carried from the first packet:** a signup or admin surface inside the auth-handler is not IAM. The census re-checked it at the code level: the auth role holds GetItem only on `opal-partner-*`, and 0 of the 5 direct code readers write.

**READERS, code.** An UNSCOPED `git grep` over all 38,500 tracked files at `b95c935160`, plus the portal repo at `be8cf21874`, for the table pattern `opal-partner-|partnerTableName|getPartnerProfile|getPartnerIdentity|partner_table|firm_49financial|partner-firm-table`:

- 322 files hit; 23 are production code.
- Those 23 split as: 5 direct readers, 1 code writer, 2 IAM grants, 6 table definitions, 1 edge consumer, and **8 FALSE MATCHES**. The false matches are all the SNS topic `opal-partner-etl-ops-alerts`, and every hit line in them was verified to be the topic.

CENSUS-READERS-DIRECT: 5 of 23

| reader | sense |
|---|---|
| `infra/aws/lambda/lib/partner/index.ts` (+ `tableName.ts`, its name builder) | **identity claim**: `GetItem Key {email}` gives `advisorKey`/`firmRole` |
| `infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts` | **identity claim**: `getPartnerIdentity` feeds the JWT advisor claims |
| `infra/aws/opalinvest_dev/lambda/auth-handler/src/auth.ts` | **identity claim**, at login (`:209`), refresh (`:543-545`) and `/auth/me` (`:577-579`) |
| `users/scripts/partners/partner_contracts.py` | an operator read-back verifying `advisorKey` after provisioning |

**The SENSE the row sets downstream (claim consumers).** The claim pattern `advisorRole|firmRole|advisorId|X-Advisor-Id|X-Advisor-Role` hits 544 files; 42 are production code. Every one is classified (0 unclassified). **12 are enforcement points:**

CENSUS-CLAIM-ENFORCERS: 12 of 42

| enforcement point | what it grants on `advisorId` / `advisorRole` / `firmRole` |
|---|---|
| edge `auth-validator-edge/index.mjs` | advisor allow-list `[advisorId]`; `role`/`firmRole` `admin` bypass (`:200-208`); injects `X-Advisor-Id`/`X-Advisor-Role` |
| edge `auth-validator-edge/tier_policy.mjs`, `aggregate_gate.mjs`; `shared-advisor-router/index.mjs`, `tier_policy.mjs` | ADVI tier by `advisorRole` (L0 = any authenticated firm user, `tier_policy.mjs:9`); advisor S3 routing by `advisorId` |
| API authorizer `users/lambda/portal-authorizer/index.mjs` | `allowedFirmIds`: `Dev` or tier `internal` gives ALL; otherwise own firm, plus descendants only for `role=admin` (`:125-154`) |
| backend `opal-partners-data/lambda_function.py` | L1/L2 tier and L1 path scope by `advisorId`; admin bypass on `role`/`firmRole`/`opal-capital`/`Dev` (`:163-170, 1673-1694`) |
| IRPT `_scope/resolve.py`, `_scope/global.py`, `_authz/enforce.py`, `holdings/resolve.py`, `holdings/enforce.py` | `X-Advisor-Id` gives FIRM_ADVISOR; `advisorRole` `admin` gives FIRM_OPERATIONS |

The other 30 production files are the claim's producer (`jwt.ts`, `types.ts`), direct readers, operator scripts, 9 tests, 7 route-path or comment texts, one table definition, one archive, and 2 library modules (`infra/aws/auth/validator.*`) whose deployed consumers were not censused.

**The portal** (a client-side SPA, its tests and docs) consumes the claims for display and routing and is not an enforcement point. Two of its tracked auth fixtures carry plaintext credentials (row IRPT_BCKEND-S87, routed to `1.0.0_SA_CTO`).

---

## The blast radius, both branches, per key

**BRANCH -- K1b PRESENT (with K1), the exercise state.** A login on the test e-mail mints `firmId=49financial, role=user, tier=advisor, advisorId=abby_horton`, with no `userType`, `firmRole` or `advisorRole`.

- **IRPT scoped routes:** FIRM_ADVISOR for `abby_horton`, which is **exactly `abby_horton`'s existing 49financial grants**. Those are 33 accounts and 18 relationships at 08:29Z (ownership map VersionId `nR.FkCE1frsI9R5zRp2wJWB7vyMZ04NK`), served as the disclosed partial (`k` permitted, the remainder counted). No new grant.
- **Edge:** the advisor allow-list is `[abby_horton]`.
- **API authorizer:** `allowedFirmIds = 49financial` only.
- **Advisor-intelligence routes:** level 0, so **L0 firm aggregates only**. They are admitted to any authenticated 49financial login (`tier_policy.mjs:9`; `opal-partners-data:1673-1680`). That is the pre-existing firm-membership exposure `1.0.0_SA_CTO` holds, **named here as inside the radius, not widened, narrowed or fixed**. L1 and L2 are refused at the edge tier and the backend, and every admin bypass is unreachable.

**BRANCH -- K1b ABSENT (K1 only).** This state exists only mid-create or mid-rollback. A login mints the same token WITHOUT `advisorKey`/`advisorId`. It is UNKNOWN on IRPT and refused on advisor-scoped paths (`_scope/resolve.py:195-196`; edge `index.mjs:207`). On advisor-intelligence L0 it is admitted by firm, which is the same pre-existing exposure and not this act's.

**BRANCH -- neither row (after ROLLBACK).** A new login fails because no row exists, a refresh fails (`auth.ts:508-537`), and `/auth/me` fails. **An access token already issued lives until its own `exp` (at most 15 minutes) with its claims baked in.** The IRPT resolver re-checks the ownership GRANT on every request, not the partner row, so a live token still resolves FIRM_ADVISOR for `abby_horton` until `exp`. **So the principal's interval closes at `max(K1 delete verified, K1b delete verified, last access-token exp)`, not at the delete.**

**Every branch the first packet stated is re-derived here, not copied.** The first packet's radius sentence ("exactly `abby_horton`'s existing entitlement, no new grant minted") is TRUE of K1+K1b and was FALSE of its K1 alone (row S86).

---

## THE EXERCISE PLAN -- for the re-handed IB-rtf-3, on the two keys

Unchanged in substance from IB-rtf-3's face; restated so the re-handed order reads ONE packet.

1. **Ledger.** Open the change-management entry and commit its OPEN sentinel before any write.
2. **Guard (CTO half s.2).** Immediately before any write, re-read 49financial's live ownership map and confirm `abby_horton` is PRESENT with a grant set; ABSENT is a STOP. Record the counts and the VersionId. A materially different number is a ROW, not a blocker.
3. **Create.** First K1, then K1b immediately before the login, so the binding exists for the shortest time. Read each back by a consistent `GetItem`, hash the item with `passwordHash` excluded from the printed digest input, and record it. Prove the firm binding by the enforcer's own read.
4. **Login.** One normal login through the real portal auth route mints K2. Record its `exp`, never the token.
5. **Negative controls BEFORE the outcome arms (COO half).** The firm swapped to inflection or cottonwood is refused `FIRM_BINDING` without echo, `m of m`. A route outside `api/scoped/` is refused. The terminated client's entitlement gap is enforced. **A failed negative control is a STOP and a same-turn rollback.**
6. **Outcome arms.** FWD-1 (search, select, relationship + permitted accounts + as-of, recording `k` and `count` against the grant count at the event), FWD-2 (every tab and the export within the permitted set, `k of k` swaps refused), FWD-5 (custody holdings + model percentages for a permitted account). Each is a real signed request with its artifact hash, and vendor calls stay `0`. FWD-11 is not reachable by a FIRM_ADVISOR principal and is recorded as such.
7. **DELETE ORDER: K1b FIRST, then K1.** Each is `DeleteItem` verified by a failing consistent read, `2 of 2`. The binding goes before the login.
8. **Close K2.** After the last access token's `exp`, one request with it is refused (401), `n of n`. The interval is recorded as `[K1 create, max(deletes verified, last exp)]`, and the ledger is closed and committed before the grading reads.
9. **A STOP under any arm** performs step 7 (and step 8's wait) the same turn.

---

## What this packet does NOT cover -- named so nothing is read into the silence

1. **The firm-membership exposure on the older routes.** A 49financial login with no book sees L0 firm aggregates. It is `1.0.0_SA_CTO`'s, named in-radius and not widened. **CORRECTION (row IRPT_BCKEND-S88):** row S86 and the IB-rtf-9 face cite `lib/partner/index.ts:39-47` (`canAccessFirm`) as the mechanism, but that function has **0 callers** in production code. The mechanism is the L0 tier (`tier_policy.mjs:9`) and `opal-partners-data`'s tier check on L1/L2 only (`:1673-1680`).
2. **FWD-11's roster parameter** `/opal/irpt/opal-principal-roster`: a separate act with its own sign-off.
3. **Any second principal**, any ownership-map or directory write, any change to the auth-handler, the authorizer, the edge or the JWT key.
4. **The served bytes of the edge validator and the API authorizer.** Their rules are cited at source `@b95c935160`. Only the auth-handler's served bytes were compared this run, and the IRPT functions' served bytes were compared by IB-rtf-2 (7 of 7 `CodeSha256`).
5. **`opal-news-lambda-role`'s write access** to partner identity tables: the IAM owner's.
6. **The portal's tracked credential fixtures** (row S87).
