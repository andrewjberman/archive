# IB-rtf-3 result (RE-HANDED): the test principal created, exercised by real signed requests and deleted -- the served path refuses every FIRM_ADVISOR request

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-3.the-test-principal-exercised-on-the-disclosed-partial-path-and-deleted.md`, re-handed @0382e96047.
**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1`.
**Packet executed:** `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md`, blob `a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4`. Halves: COO @3c0bad02ee, CTO @4290315df9.
**First pass (superseded):** STOP at arm (a) @1771b07216 / @700bc86ec2, row S86. That pass created nothing.
**Battery:** `battery_ib_rtf_3.py`, the live version, blob committed @ca728267ef. Run 2026-09-19T10:25:53Z, rc 1. Output `IB-rtf-3_R60-AC1_battery_output.txt`, blob `55a69d9e5558c4604912a36e3ad6c9eae7733295` @e7da534cc6.
**Ledger:** `irpt-bckend-ib-rtf-3-test-principal`. Its sentinel was committed @ca728267ef before any write, and it was CLOSED with 6 of 6 legs proven, committed @e7da534cc6 before the grading reads.

## The principal's closed interval

**[2026-09-19T10:25:56Z, 2026-09-19T10:41:03Z]**

- **Created:** K1 `opal-users-v2` `USER#usr_irptrte_1789813553` / PROFILE at 10:25:56Z, 10 attributes, read back by a consistent GetItem. Digest with `passwordHash` excluded: `8b1123122d127db1e254ef64eef47b0a94783b101f9b0b648ab752af92a6f4f3`.
- **Created:** K1b `opal-partner-49financial` with exactly `{advisorKey, email}` at 10:25:56Z, read back. Digest `5d891293f2b4b72684a35c164cf0313d2ed750dddd0aa58439bd9851693be88f`.
- **Guard, immediately before those writes:** the ownership map VersionId `nR.FkCE1frsI9R5zRp2wJWB7vyMZ04NK`, with `abby_horton` PRESENT, 33 accounts and 18 relationships, equal to the packet's read.
- **Login** (the real route, `POST https://opalinvest.dev/auth/login`): HTTP 200 at 10:25:58Z. K2 carried `firmId=49financial`, `role=user`, `tier=advisor`, `advisorKey=advisorId=abby_horton`, `advisorRole=''`, with no `userType` and no `firmRole`, **exactly as the packet declares**. Access-token `exp` 10:41:03Z. The token, cookie and password were never recorded.
- **Deleted, K1b FIRST:** K1b at 10:26:10Z, then K1 at 10:26:10Z, each verified by a consistent base-table GetItem returning no Item. **2 of 2.**
- **Refresh (CTO half s.1):** `POST /auth/refresh` with the issued refresh token after K1's delete returned HTTP 404 and minted no token. **REFUSED, 1 of 1.**
- **Access token after `exp`:** `GET .../status` returned HTTP 401. **REFUSED, 1 of 1.**
- **Residue:** prefix scans after the run read 0 of 79 (`PK`), 0 of 79 (`email`) and 0 of 11 (partner). No failed-login throttle counter exists for the test e-mail.

## R60-AC1: FAIL by output, 9 of 12 arms

| arm | result | deciding line |
|---|---|---|
| (a) precondition | PASS | 2 of 2 halves at HEAD naming blob `a1f36b95b2`; packet re-hashed EQUAL |
| (b) guard | PASS | `abby_horton` PRESENT; 33 / 18 |
| (b) keys + login | PASS | 2 of 2 read back; claims exactly as declared |
| (d) negative controls | PASS | 4 of 4 refused (discrimination below) |
| (c) FWD-1 | **FAIL** | search and resolve refused `UNEXPECTED`; no entries, no `unprojected_grant`, no `firm_id` |
| (c) FWD-2 | **FAIL** | 8 of 8 swaps refused without echo; within-set tabs served 0 of 1 (status refused `UNEXPECTED`) |
| (c) FWD-5 | **FAIL** | not runnable: no permitted account id, because the search served nothing |
| (c) vendor calls 0 | PASS | performance transport `recorded`, no egress variable; POST /analysis and POST /export called 0 times |
| (e) deletes verified | PASS | 2 of 2, K1b first |
| (e) refresh refused | PASS | HTTP 404, 1 of 1 |
| (e) expired token refused | PASS | HTTP 401, 1 of 1 |
| (e) no residue | PASS | 0 / 0 / 0 |

FWD-11 is recorded as NOT REACHABLE by this principal (re-hand condition (v)); no request was made. The success token did not print.

## R60-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**Is each outcome EXERCISED as its DONE WHEN reads?**

- **FWD-1, FWD-2, FWD-5: attempted, and none reached the compute.** Every authenticated scoped request that passed the FIRM_BINDING check was refused BEFORE the scope resolved (row S90): 12 of 12, across search, resolve, status, holdings and the seven foreign-id swaps.
- **The disclosed partial was never observed live.** No served response carried `unprojected_grant`, so the partial's `count` was not seen. The in-process figure from IB-rtf-2 (`k=21`, `count=12` of 33) is not a property of the deployed path. It was computed under operator credentials that can read the ownership map; the Lambda role cannot (S90).
- **What the partial's count would mean for the DONE WHEN is therefore still open.** It is graded when a served response exists.
- **FWD-11 is not reachable** by a FIRM_ADVISOR principal: it needs the roster plus an Opal login, a separate act.

**What the exercise revealed about the served routes (defects filed as rows):**

1. **S90 (BLOCKING, ARMED, 2.0.0_SA_COO~B): the served IRPT path answers no FIRM_ADVISOR request.** The causes, per function:
   - `irpt-directory-search`: its role cannot read `opal-data-bd/platinum/49financial/ownership_map.json`. Simulated `implicitDeny`, with the admin positive control allowed. `_authz/loaders.py:93-116 @9f72f4d6a4` re-raises that AccessDenied.
   - `irpt-status` and `irpt-holdings`: their deployed environments carry no `IRPT_DIRECTORY_BUCKET_MAP`, and both bucket readers raise on an unmapped firm (`loaders.py:46-56`, `holdings/handler.py:356-370 @9f72f4d6a4`). This cause is source plus environment, not simulated.
   - **This is the first authenticated request ever sent through the real path.** Round 1's replay was unauthenticated, and IB-rtf-2's "SERVED" ran in-process.
2. **S91 (ARMED, 1.0.0_SA_CTO): those refusals are undiagnosable.** `served.py:628, 649, 662 @9f72f4d6a4` record the exception to a `None` sink. CloudWatch held only START/END/REPORT lines for all 12 refusals; the cause in S90 was re-derived by simulation and environment reads.
3. **S92 (ARMED, INFERRED, 2.0.0_SA_COO~B): latent behind S90.** `search` reads `q`/`limit` and `resolve` reads `selection` from the top level of a payload-2.0 event, where they never appear (`directory/entry.py:92-93, 136`; `api/integrations.tf:57 @9f72f4d6a4`). Once S90 is fixed, search would ignore its query and resolve would always answer "selection matches nothing".

**Which controls discriminated and which were vacuous:**

- **Discriminated.** The three FIRM_BINDING refusals: NC1 for inflection and for cottonwood, and the resolve swap with `firm_id=inflection` in the body. They fire at `served.py:614-616`, BEFORE the failing `enforcer_for`, so they measured the binding. None echoed the swapped value.
- **NC2** (a route outside `api/scoped/`) served no IRPT envelope: HTTP 200 without an IRPT body, which is the site's default behaviour.
- **Vacuous.** NC3 (the terminated client's account) and the seven foreign-id swaps were refused `UNEXPECTED`, the same refusal every in-scope request got. **They show nothing about coverage or the terminated-client gap** and must not be read as evidence that the gap is enforced. They become real controls once S90 is fixed.

**Can a future round repeat this without a standing account? Yes, and this run is the proof.**

- The whole two-key lifecycle closed in 15 minutes 7 seconds: create, one login, exercise, K1b-first delete verified 2 of 2, the 7-day refresh credential's death EXERCISED (the CTO's condition), and the 15-minute access token proven dead by a 401.
- It left 0 residue on both tables and no throttle counter, all under one ledger interval.
- A re-run after S90's fix needs no new packet: same keys, same blob, new epoch.
- The standing smoke logins the portal repo tracks (row S87) are exactly the standing account this lifecycle makes unnecessary. They must not be used for this.

## Rows filed

- `IRPT_BCKEND-S90`: BLOCKING, ARMED, `2.0.0_SA_COO~B`.
- `IRPT_BCKEND-S91`: OBSERVATION, ARMED, `1.0.0_SA_CTO`.
- `IRPT_BCKEND-S92`: OBSERVATION, ARMED, INFERRED, `2.0.0_SA_COO~B`.
