# IB-rtf-9 result: the two-key packet declared on the real mint path, nothing created

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-9.the-two-key-test-principal-packet-on-the-real-mint-path.md` @dd95b034da
**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1` (fast-forwarded to CLOUD `b95c935160` on the issuer's word)
**The packet:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md`, **blob `a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4`**, committed @5811d7201a. The halves sign against this blob.

## What the packet declares

- **K1**: one `opal-users-v2` PROFILE item with 10 attributes set. Each is cited to the line of the deployed `getUser()` or login path that reads it.
  - 5 attributes are deliberately absent, each with why and the line that reads it: `userType`, MFA, phone, `mustChangePassword`, and `advisorKey/advisorId`.
  - The advisor fields are dropped from the first packet's K1 because `getUser` never reads them (`db.ts:138-167 @b95c935160`).
  - The third item `create_user_v2.py` writes (FIRM#/MEMBER#) is named NOT NEEDED.
- **K1b**: one `opal-partner-49financial` item with exactly `email` + `advisorKey = abby_horton`. Those are the only two attributes the deployed reader needs for the claim (`lib/partner/index.ts:27-31 @b95c935160`).
  - `firmRole`, `advisorRole` and `advisorName` are deliberately absent. An `admin` value in either role field would widen the radius at the edge (`index.mjs:201, 206 @b95c935160`), on IRPT (`_scope/resolve.py:186 @b95c935160`) and in the backend (`opal-partners-data:163-170 @b95c935160`).
- **K2**: the session. The access token has a 15-minute TTL (`jwt.ts:17 @b95c935160`). The refresh token is bound to K1's row and dies with it (`jwt.ts:220-224`, `auth.ts:483-537 @b95c935160`).
- **Rollback**: `DeleteItem` per key, each verified by a failing consistent read, **K1b deleted FIRST**. The interval closes at `max(deletes verified, last access-token exp)`: an issued token keeps its baked claims until `exp`, and IRPT re-checks the ownership grant, not the partner row.
- **The census of `opal-partner-49financial`**:
  - resource policy NONE;
  - **writers 4 of 263** principals (0 unsimulated, 0 UNKNOWN, both controls hold). One of them is `opal-news-lambda-role`, an IAM finding named for the IAM owner;
  - **direct code readers 5 of 23** production files touching the table pattern, with 8 SNS-topic false matches verified line by line;
  - **claim enforcers 12 of 42** production files consuming the claims, 0 unclassified.
- **The exercise plan** is restated on the two keys for the re-handed IB-rtf-3.

## R66-AC1: PASS by output

`battery_ib_rtf_9.py`, run 2026-09-19T09:19:18Z at HEAD 5811d7201a, after the packet's commit. rc 0. Output: `IB-rtf-9_R66-AC1_battery_output.txt`.

- **(a)** Attributes cited: 22 of 22. The served auth-handler zip's sha256 equals the live `CodeSha256` `h1tnQVRpRA52eWyfAia6CfBsJmn6xKwHa8IUC0zBSsQ=`. The served bundle references 13 of 13 of the attribute names, including the partner `GetItem Key {email}`.
- **(b)** Resource policy NONE. 263 principals simulated, 0 unsimulated, 0 UNKNOWN. Writers: 4 of 263. Both controls hold. Unclassified production hits: 0.
  - The three census lines the packet prints each equal this run: `4 of 263`, `5 of 23`, `12 of 42`.
- **(c)(d)(e)** The packet blob at HEAD equals the worktree (`a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4`), and 9 of 9 section markers are present.
- **(e)** Zero writes: the test prefixes are absent before and after on both tables. `opal-users-v2` reads 0 of 79 by `PK` and 0 of 79 by `email`; `opal-partner-49financial` reads 0 of 11.
- **All 4 ARM lines read PASS**, followed by *"RESULT: R66-AC1 PASS -- the two-key packet declared on the real mint path; nothing created"* and the success token.

## R66-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**1. The advisor identity living in a partner table keyed by e-mail: intended design, or an accident the IRPT routes now depend on?**

- **The table itself is intended.** The module says it verbatim: *"Per-partner identity bridge between portal users (opal-users-v2) and the partner firm's advisor identity. The auth-handler Lambda reads this table at login time to inject advisor claims into the JWT"* (`infra/aws/terraform/modules/partner-firm-table/main.tf:5-7 @b95c935160`). The edge dates the framework to the "Phase 0 identity overhaul 2026-04-15" (`auth-validator-edge/index.mjs:202-205 @b95c935160`).
- **The IRPT dependence is transitive and was never traced.** IRPT reads `X-Advisor-Id`, which the edge injects from the token's `advisorId` (`_scope/resolve.py:92-96, 174 @b95c935160`). The token gets that claim only from the partner table.
- **The IRPT records mis-located it.** The test-principal record RT2 cited the claims at `jwt.ts:167-187` without tracing where they come from. The first packet then put the advisor on the user row. That is a record inheriting an unexamined source, not a code accident.
- **The structural consequence, named but not measured.** Two independently written spellings of one identity must agree for FIRM_ADVISOR to resolve: the ownership map's advisor key (`abby_horton`), and the partner row's `advisorKey`, which operators write by hand at onboarding (`main.tf:11 @b95c935160`). This census found no validator between them. How many of the 11 partner rows carry an `advisorKey` present in the 174-advisor ownership map was not measured here. It is one read-only join.

**2. The exposure IB-rtf-3 named: a firm login with no book admitted by firm on the older routes.**

- **The mechanism is re-cited (row S88).** It is not `canAccessFirm`, which has 0 callers. It is the L0 tier:
  - "any authenticated 49 Financial user" (`tier_policy.mjs:9 @b95c935160`);
  - the API authorizer's own-firm `allowedFirmIds` (`portal-authorizer/index.mjs:125-154 @b95c935160`);
  - `opal-partners-data` gating only L1/L2 (`:1673-1680 @b95c935160`).
- **What the unscoped census would take (the CTO's).**
  - For every firm with a partner table (`opal-partner-*`: 49financial, inflection, cottonwood, demo), read the firm's PROFILE items from `opal-users-v2` through `firmId-index`.
  - Read the partner table's `email` and `advisorKey` by projection.
  - Count PROFILE e-mails with NO partner row, and partner rows with an EMPTY `advisorKey`, each over the firm's PROFILE count.
  - Separately, count firms with a `firmId` and no partner table at all, which are all no-book by construction.
  - Print counts only, never e-mails. Denominator: every PROFILE item whose `firmId` is not `opal-capital` (79 items in `opal-users-v2` at 09:05Z, PROFILE and non-PROFILE together).
  - The two tracked portal smoke logins (row S87) belong in that population.

**3. Does FWD-11's global viewer need a partner row in EVERY firm's table, or a different mint path?**

- **Neither: it needs the roster.** OPAL_GLOBAL is decided ONLY by the server-side roster parameter `/opal/irpt/opal-principal-roster`, matched on `X-User-Email` (`_scope/global.py:10, 65, 140 @b95c935160`; `_scope/resolve.py:181-183 @b95c935160`). It is never decided by a header or a partner row.
- **An Opal principal skips the partner table entirely.** A `firmId = opal-capital` principal gets no partner lookup (`auth.ts:207 @b95c935160`), carries tier `internal` (`jwt.ts:168 @b95c935160`), and has ALL firms at the API authorizer (`portal-authorizer/index.mjs:133-136 @b95c935160`).
- **A partner row cannot provide it.** A partner row in every firm's table would not make any principal global: a token carries ONE `firmId`, so a partner row yields FIRM_ADVISOR in that one firm.
- **So FWD-11's path is** an Opal login plus the roster parameter, which is a separate infrastructure act with its own sign-off. This packet does not authorize it.

## Rows filed

- `IRPT_BCKEND-S87`: OBSERVATION, ARMED, disarm owner `1.0.0_SA_CTO`. The portal repo tracks two auth fixtures with plaintext login credentials: `.frontend-dev/auth/credentials.json` (three logins, including `internal_admin`) and `login-constitution.json` (one). Both are on `origin/DEV` and `origin/PROD` since portal commit `03d719d4` (2026-06-08). Only key names and lengths were read; whether any password is live was NOT tested.
- `IRPT_BCKEND-S88`: OBSERVATION, INERT. A correction to this seat's row S86 and to the IB-rtf-9 face: `canAccessFirm` has 0 callers, and the firm admission is the L0 tier.

## What I did not do

- Created nothing: 0 items in either table, before and after (the battery's zero-write arm).
- Minted no session and made no vendor call.
- Did not compare the edge validator's or the API authorizer's served bytes. Their rules are cited at source `@b95c935160`, and this is stated in the packet's "does NOT cover" list.
- Did not measure the unscoped no-book-login census or the partner-to-ownership-map join. Both are named above with what they would take.
