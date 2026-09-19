# IB-rtf-3 result: STOP at arm (a), no principal created, R60-AC1 FAIL

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-3.the-test-principal-exercised-on-the-disclosed-partial-path-and-deleted.md` @4ee8426c72
**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1`
**Signed act:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/NEVER_WIDEN_SIGNOFF_PACKET_IB-rte-1.md`, blob `3d9f57335b9893753973132ba5c4958b2622e24f`. The COO half is @a0f05dda0c and the CTO half @482b2c627e.

## What happened

1. **Precondition: holds.** 2 of 2 halves are at HEAD, each names the packet blob and each names K1 and K2. The packet re-hashes equal at HEAD and in the worktree.
2. **The premise does not hold, so I stopped before any write.** Both halves sign a session shape: *"a token minted against K1 carries exactly `abby_horton`'s already-live entitlement in 49financial ... because no new grant is minted anywhere"* (CTO half s.1). K1 and K2 cannot produce that session.
   - **Served bytes.** I downloaded the deployed `opalinvest-auth-handler` zip and hashed it: sha256(b64) `h1tnQVRpRA52eWyfAia6CfBsJmn6xKwHa8IUC0zBSsQ=`, equal to the live `CodeSha256`.
   - **Where the advisor claim comes from.** In those bytes the advisor claim comes from `opal-partner-<firm>` read with `GetItem Key {email}` (source: `infra/aws/lambda/lib/partner/index.ts:21-37 @4ee8426c72`, `infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts:29-54 @4ee8426c72`). `mintSession` passes it to `generateAccessToken` (`auth.ts:202-216 @4ee8426c72`, `jwt.ts:179-185 @4ee8426c72`).
   - **The user row is never read for it.** `getUser()` maps no advisor field off the `opal-users-v2` row (`db.ts:138-167 @6275297f0e`), so the packet's `advisorKey/advisorId = abby_horton` on K1 would be written and never read.
   - **No login is bound to `abby_horton`.** `opal-partner-49financial` is keyed `HASH=email`, and a COUNT scan finds **0 of 11** rows with `advisorKey = abby_horton`. No login anywhere binds `abby_horton` today.
   - **What K1 and K2 would actually mint.** A new `.test` e-mail would get a `firmId=49financial` session with **no** advisor claim. On the IRPT scoped routes that principal classifies `UNKNOWN`, not `FIRM_ADVISOR` (`_scope/resolve.py:193-196 @4ee8426c72`). On the older portal routes `canAccessFirm` admits it by `firmId` alone (`lib/partner/index.ts:39-47 @4ee8426c72`). Neither half signed that entitlement.
   - **What the signed shape would need.** A partner-table row binding the test e-mail to `advisorKey=abby_horton`. The packet does not name that key. It would be the first login binding for `abby_horton` anywhere, which is an authorization write, where the halves sign "an authentication row; it adds no authorization".
   - **The rule that applies.** CTO half s.1: a key the act discovers it needs is *"a STOP and a new packet, not a widening of this one."*
3. **Nothing was written.** 0 of 2 keys were applied, no ledger entry was opened (there was no act), no session was minted, and there were 0 vendor calls. The principal's interval is **EMPTY**: it never existed, so there is nothing to delete.
4. **Informational, not the guard (no K1 exists).** The live ownership map (`s3://opal-data-bd/platinum/49financial/ownership_map.json`, VersionId `nR.FkCE1frsI9R5zRp2wJWB7vyMZ04NK`, ETag `ff85ad011af1636ecdb9dc7ae6ee1398`) carries `abby_horton` with **33 accounts / 18 relationships**. The packet measured 43 / 18; the move is already row W1-S30.

## R60-AC1: FAIL by output

Battery `battery_ib_rtf_3.py`, run 2026-09-19T08:29:50Z at HEAD 6275297f0e (the run in the committed `IB-rtf-3_R60-AC1_battery_output.txt`), printed:

- *"STOP at arm (a): the signed keys K1 + K2 cannot produce the session shape both halves sign ..."*
- *"RESULT: R60-AC1 FAIL -- STOP at arm (a); 0 of 4 outcomes exercised; principal never created"*

Arms (b), (c), (d) and (e) did not run. The order stays open.

**Correction to row IRPT_BCKEND-S86's grounding, recorded here because the channel is append-only.** The row cites the output file as "run 2026-09-19T08:28:40Z". The committed file is the **08:29:50Z** run. The 08:28:40Z run read the same values: zip sha256 = CodeSha256, the partner lookup by e-mail, 0 of 11, and the STOP. It differed only in printing the `getUser` range as `db.ts:138-201`, which ran on into `createUser`'s item literal. The battery was corrected to end at `} as User;` (`db.ts:138-167`) before the committed run.

## R60-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**Is each outcome now EXERCISED as its DONE WHEN reads? None of them is, this round.** No session was minted, so no arm made a request.

| outcome | what the arm did | what it did not reach |
|---|---|---|
| FWD-1 (search, select, relationship + permitted accounts + as-of) | nothing | The disclosed-partial path IB-rtf-2 deployed is untested by a live session. IB-rtf-2's own in-process arm read `k = 21` permitted with `unprojected_grant.count = 12` of denominator 33 for `abby_horton` at its run (row W1-S30). For the DONE WHEN, a partial means "permitted accounts" is `k` of the grant set, with the rest disclosed by count. Whether that satisfies FWD-1 is the L4 ruling's three conditions @61627f39f9, graded at L9, not here. |
| FWD-2 (every tab and the export within the permitted set, `k of k` swaps refused) | nothing | unreached |
| FWD-5 (custody holdings + model percentages for a permitted account) | nothing | unreached |
| FWD-11 (the global viewer across every firm) | nothing | Unreachable by this principal even with a working mint path. A `FIRM_ADVISOR` token is not `OPAL_GLOBAL`, and the roster parameter `/opal/irpt/opal-principal-roster` is a separate act that neither half authorizes. |

**What the attempt revealed about the served routes and the mint path (row IRPT_BCKEND-S86, BLOCKING, ARMED, disarm owner 2.0.0_SA_COO~B):**

- The finding is on the **mint path**, not the served routes. The token's advisor identity is a partner-table binding keyed by e-mail, and the user row plays no part in it.
- Since 0 of 11 partner rows bind `abby_horton`, no real person's login reaches the IRPT scoped routes as `abby_horton` either. The only principal that could exercise FWD-1/2/5 "as `abby_horton`" is one whose partner row is written for the purpose.
- A second observation, **not measured here and not graded**: a 49financial principal with no partner row is a "firm member with no book". The IRPT scoped routes refuse it; the older portal routes admit it by `firmId`. Whether any such login exists today was not censused. This is named for the CTO as an exposure question, not claimed as an incident.

**Can a future round repeat this without a standing account? Yes, but with two keys, not one.**

- The create-exercise-delete lifecycle still works inside one ledger interval, as long as the packet names **both** rows: the `opal-users-v2` item (authentication) and an `opal-partner-49financial` item keyed by the test e-mail carrying `advisorKey=abby_horton` (the advisor binding).
- Each needs its own rollback: `DeleteItem`, then a consistent-read `GetItem` returning no `Item`.
- The partner row also needs its own writer census and reader census, because it is the key that carries the entitlement.
- After deletion, the refresh token dies with the row (the refresh `sub` binds to PK + createdAt, `jwt.ts:220-224 @4ee8426c72`). An already-issued access token lives at most 15 minutes (`jwt.ts:17 @4ee8426c72`, `ACCESS_TOKEN_EXPIRY = '15m'`). That is the bound on the CTO half's s.5 item 3 exposure for a re-cut.
- Neither row may outlive the interval, so no standing account is needed.

## Rows filed

- `IRPT_BCKEND-S86`: BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~B`. The signed keys cannot produce the signed session; STOP before any write; a re-cut packet is needed.
- The face mints `IRPT_BCKEND-A-S<k>` here too. That grammar defect is already row `IRPT_BCKEND-S83` (seat form used), so it is not re-filed.
