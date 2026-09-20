# IB-rtf-3 result (THIRD HAND): the route serves, the DISCLOSED PARTIAL is exercised and exact (k+count=44=denominator=map), the principal deleted and verified. R60-AC1 FAIL 10 of 12 -- the two remaining arms are pre-existing world defects with carriers, and one of my own controls was found VACUOUS

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-3.the-test-principal-exercised-on-the-disclosed-partial-path-and-deleted.md`. GO msg 98485.

**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`. Base: CLOUD merged, carrying rtf-13's apply drain `0d45a81053`.

**Graded run:** `timeout 1800 py -3.12 .../battery_ib_rtf_3.py` @`5d2f3a942f`, **2026-09-20T11:43:00-11:58:24Z, rc 1**.

---

## R60-AC1: FAIL, by output -- 10 of 12 arms hold (was 9 of 12 on the second hand)

| arm | verdict | note |
|---|---|---|
| (a) halves at HEAD | **PASS** | 2 of 2 naming the packet blob |
| (b) guard | **PASS** | live ownership map read immediately before any write |
| (b) keys + login | **PASS** | 2 of 2 created and read back; claims as the packet declares |
| (d) negative controls | **PASS** | 4 of 4 refused -- **but see s.3: NC3 is VACUOUS this run** |
| (c) FWD-1 | **PASS** (was FAIL) | the disclosed partial, exact |
| (c) FWD-2 | **FAIL** | within-set tabs served 0 of 2 -- `W2-S27`, `W1-S18` |
| (c) FWD-5 | **FAIL** | permitted account refused `FIRM_BINDING` -- `S100` |
| (c) vendor calls 0 | **PASS** | |
| (e) deletes / refresh / expired token / residue | **PASS** x4 | lifecycle closed |

`FWD-11` remains NOT-REACHABLE by this principal (a `FIRM_ADVISOR` token carries one `firmId`; `OPAL_GLOBAL` is the SSM roster plus an opal-capital login, a separate act) -- recorded, no request made, per re-hand condition (v).

---

## 1. WHAT THE THIRD HAND SETTLED: the disclosed-partial path is EXERCISED and EXACT

The second hand failed FWD-1/2/5 for one reason: `irpt-directory-search` raised on its missing contract and the boundary answered `UNEXPECTED`, so there were no entries, no permitted account and nothing to exercise. rtf-13's apply fixed that route. This run:

- **search SERVED**: `HTTP 200`, `operation directory-search`, `state PARTIAL`, `reason OBJECT_NOT_COVERED`, **7 entries**, `sha256 5bba231c…`;
- **the disclosed partial is EXACT**: `unprojected_grant count=23`, `denominator=44`, `kinds {UNPROJECTED-ID: 23}`, whole entries `k=21` -> **k + count = 44 = denominator = the ownership map's 44 accounts at the event**;
- **resolve SERVED**: `scope_kind=RELATIONSHIP`, `account_count=1`, `ok=True`, `sha256 7a048b15…`;
- **firm binding by the enforcer's own read**: envelope `firm_id fir_c9fc04650e2134d6ea033da2` == the directory's `firm_id_opaque`;
- **as-of** present (`business_date 2026-09-17`);
- **`q` is honoured**: a no-match query returned **0** entries against **7** for `q=a` -- the control that separates "search works" from "search returns everything".

**The grant moved under the packet and the battery re-derived rather than inheriting:** the live map reads **44 accounts / 19 relationships** where the packet recorded **33 / 18**. Every count above is the live one at the event, which is why `k+count` reconciles at 44 and not at 33.

---

## 2. THE TWO REMAINING FAILURES ARE PRE-EXISTING WORLD DEFECTS, EACH WITH A CARRIER

**FWD-5 -- `S100`.** `GET holdings/<permitted account>` (an account this principal's OWN resolve had just granted) returned `HTTP 200`, `public_reason_code FIRM_BINDING`, `state UNAVAILABLE`, `sha256 754aa8b2…`. `S100` (ARMED) already has the mechanism: `holdings/entry.py:70-71,88-89,109-112` reads `IRPT_DIRECTORY_KEY=investor-reporting/directory/latest.json` -- the **POINTER** -- as the directory artifact, so `FirmBinding` raises and the boundary refuses with no `firm_id`. **No new row: the row exists and this is its live confirmation on the permitted path**, which is stronger evidence than the forbidden-path observations that produced it.

**FWD-2 -- within-set tabs served 0 of 2.**
- `performance/<permitted>` -> `DEPENDENCY_UNAVAILABLE` (`business_date 2026-09-17`, `sha256 3f805b4f…`). Carrier: **`W2-S23`/`W2-S27`** -- the adapter's tenant routing is a third id space, and `DEPENDENCY_UNAVAILABLE` is the honest code for "this function has no route for that firm", not an authorization failure.
- `status (summary)` -> `UNSUPPORTED_OPERATION` (`sha256 b43add8d…`), a declared member of the closed `PUBLIC_REASONS` tuple.
- the export within the set **is not exercisable**: no export exists for this firm (**`W1-S18`**) and `POST /export` is excluded from this cell.

**The swap half of FWD-2 is now materially better and is recorded as such:** 8 of 8 foreign-id swaps refused **without echo**, and they now carry SPECIFIC codes (`FIRM_BINDING`, `NOT_AUTHORIZED`, `INVALID_INPUT`, `UNSUPPORTED_OPERATION`) where the second hand saw `UNEXPECTED` on all of them. The two that remain `UNEXPECTED` are both export routes -- **`S104`/`S106`**, the defects this seat measured on IB-rtf-14.

---

## 3. A CONTROL OF MINE THAT COULD NOT FAIL -- found by the arm that can falsify it (row `S110`)

**NC3 passed and proves nothing this run.** It asks whether a TERMINATED client's entitlement gap is enforced, and reads a refusal as proof. It got `FIRM_BINDING`. **FWD-5's PERMITTED account got `FIRM_BINDING` too.** So the control's evidence is identical whether or not any gap is enforced -- it would read PASS against a route with no entitlement checking at all. Under Rule 22's DISCRIMINATION axis it is not evidence, and its PASS above stands as **REPORTED**, not as evidence.

It is not a battery-only problem, which is why it is filed as **`S110`** rather than only fixed here: **while `S100` is armed, ANY negative control on `irpt-holdings` that asserts "refused" is vacuous**, including the rtf-10 and rtf-12 arm-(f) observations that recorded holdings `FIRM_BINDING` as an expected refusal. The remedy is not a better control -- it is `S100`. The battery now prints the vacuity itself whenever the two codes match, so the finding travels with the evidence.

**What `S110` does NOT claim:** that any entitlement gap is UNenforced. It claims the estate holds **no evidence either way** on this route -- weaker, and the honest statement.

---

## 4. THE BATTERY DEFECT THIS PASS FOUND IN ITSELF (fixed @`5d2f3a942f`, before the graded run)

The first third-hand run (11:16:34-11:32:00Z, 9 of 12) failed FWD-1 on **`terminated visible > 0`**. That clause was **mine, not the face's** -- R60-AC1 (c) requires the `k + count` recording and names no terminated condition -- and it grades the ROUTE on a property of the GRANT:

- `directory/handler.py:25-27` and `:126`: **"A TERMINATED CLIENT STAYS VISIBLE (Andrew's fixed constraint)"**, and the visibility filter reads the **permitted account set**, never the termination indicator. So visible <=> entitled.
- **Measured, denominator printed:** the 2026-09-17 directory carries **4,576 entries, 71 TERMINATED**; the live grant is **44 accounts**; TERMINATED entries intersecting that grant: **0 of 71**. With this grant, 0 terminated visible is CORRECT.
- **And my two conditions were jointly unsatisfiable.** NC3 needs a terminated client OUTSIDE the grant (so its account is refused); FWD-1 needed one INSIDE it (so it is visible). Both drew on the same 71 entries. At 0 of 71 entitled, only NC3 is satisfiable.

**Fixed grant-aware rather than deleted:** the route is still graded on terminated visibility whenever the grant entitles at least one terminated client, and is explicitly NOT graded when it entitles none -- with the branch, the counts and the reason printed either way. The check survives for a future principal; it simply cannot be graded by this one. **This is the rtf-12 arm-(a) class repeated by the same seat**, and it is recorded as such.

---

## 5. THE LIFECYCLE, CLOSED AND VERIFIED (arm (e))

- **K1b then K1 deleted**, each verified by a failing consistent BASE-TABLE read: **2 of 2**.
- **REFRESH with the issued refresh token after the delete: HTTP 404, no access token minted -> REFUSED (1 of 1).**
- **The access token after its `exp`: `GET status` -> HTTP 401 -> REFUSED (1 of 1)**, after the battery waited out the full token lifetime.
- **Residue: 0 of 79 / 0 of 79 / 0 of 11** (users by PK prefix, users by e-mail prefix, partner table by e-mail prefix). No failed-login throttle counter exists for the test e-mail.
- **INTERVAL: `[2026-09-20T11:43:03Z, 2026-09-20T11:58:12Z]`.**
- Never printed or written: password, access token, refresh token, Authorization header, or any response body (real client data) -- every response is bound by its `sha256` and summarised by counts and codes only.

---

## 6. R60-AC2: JUDGMENT, recorded for `3.0.0_SA_CVO`, not self-graded

1. **Is each FWD now EXERCISED as its DONE WHEN reads?**
   - **FWD-1: YES, and this is the first pass in which it could be.** Search + resolve served under a real signed request as a real advisor principal, and the partial's `count` is not decorative: `k=21` whole entries + `count=23` unprojected = `denominator=44` = the live map's account total at the event. **What the `count` means for the DONE WHEN:** the route discloses the SIZE of what it withheld and the KIND (`UNPROJECTED-ID`) without disclosing the ids, so an advisor can tell "I am seeing part of my book" from "my book is small" -- which is the disclosure the DONE WHEN asks for. It did NOT reach the terminated-but-entitled case (0 of 71 entitled under this grant).
   - **FWD-2: NO, and it is now precisely bounded.** The refusal half is fully exercised (8 of 8 swaps refused without echo, specific codes, no echo of the refused value). The SERVING half reached 0 of 2 tabs, for two separately-carried reasons (`W2-S27`, `W1-S18`) and neither is an authorization defect.
   - **FWD-5: NO, and the cause is `S100`** -- not an entitlement decision at all. This run supplies what earlier observations could not: the refusal occurs on an account the principal's own resolve GRANTED, so `S100` is now confirmed on the permitted path.
   - **FWD-11: NOT REACHABLE by this principal by construction**, unchanged.
2. **What the exercise revealed about the served routes.** The scope plane and the data plane have diverged: an advisor can be correctly identified, firm-bound, scope-resolved and told exactly how much of the book is withheld -- and then served no data on any tab. Every failure is an honest declared refusal code rather than `UNEXPECTED`, except the two export routes (`S104`/`S106`). **The estate's refusal vocabulary is working; its data paths are not.**
3. **Can a future round repeat this without a standing account?** **Yes, and this pass is the evidence.** The principal was minted, exercised and deleted inside one battery run with the lifecycle verified 4 ways and residue 0/0/0, twice in one morning. **The bound worth stating:** it costs ~15 minutes of wall clock per run, almost all of it waiting out the access token's `exp` to prove the expired-token refusal, and it requires the two DynamoDB writes the packet signs. Nothing about it needs a standing account -- **but it does need the grant re-read at the event, not inherited from the packet** (33/18 -> 44/19 between signing and this run).
4. **A judgment on my own controls, offered because the CVO grades this and I cannot.** Two of the twelve arms in this battery have now been found to grade something other than what they claim -- FWD-1's terminated clause (fixed here) and NC3's discrimination (`S110`). Both were found by an arm INSIDE the same battery, not by re-reading it. **A battery that exercises the positive and negative case on the same instrument in the same run can catch its own vacuous controls; one that only asserts refusals cannot.**

---

## 7. ROWS

- **Filed this pass: `S110`** (a negative control on holdings cannot fail while `S100` is armed) -- OBSERVATION, ARMED, `disarm_owner 2.0.0_SA_COO~B`.
- **Confirmed, not re-filed:** `S100` (FWD-5, now on the permitted path), `W2-S27` (performance), `W1-S18` (no export exists), `S104`/`S106` (the two export swaps still `UNEXPECTED`).
