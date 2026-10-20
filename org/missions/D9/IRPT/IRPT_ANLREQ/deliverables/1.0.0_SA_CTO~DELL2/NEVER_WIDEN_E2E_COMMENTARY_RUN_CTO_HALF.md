# CTO half -- ONE fresh synthetic commentary end-to-end run (resident, drafter, packager, commentary route)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~19:4xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md`.
I re-measured it: blob `394e573a4ae5902b4121626c31a0c605c35e8968`, equal at commit eaaadedbf3 and in the working tree;
sha256 `13dcef410597407129bcb9c0b952440a63abf63be2b457cd76235e8d35e8ef6b`; 8,023 bytes. COO half signed in the packet.
Ledger `irpt-commentary-e2e-20261017`. Operator: `0.7.0_AE_CloudOps~IB2`.

**SIGNED, with the conditions below.**

## Blast radius (packet section 2, accepted as read)

- **Created, synthetic only:** one `opal-users-v2` row, one upload, one ticket, one request item, one job row, its
  artifacts and blobs, and at most one `commentary_ready` message. Every one is deleted by the key recorded at creation
  (section 4). Andrew's word covers synthetic deletes (`ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md`).
- **Compute:** one resident render, which may call YCharts under the standing 390 s spacing rule. One model call by the drafter.
- **Writers:** one, the synthetic actor.
- **Moves nothing deployed:** no code, role, route, queue, table, schema or secret.
- **Served output moved:** none a client or staff user can see. The synthetic ticket is visible only to its own creator
  while it exists.

**Rollback:** none is needed, because nothing is deployed. Section 4 removes the objects whether the run passes or stops.

## Read at signing

**The portal reads this route's answer.** On PROD (99d2b2a7), `analysis-request-commentary-pdf` goes through the same
adapter as the report PDF (`src/pages/InvestorReporting/contracts/envelope.ts:197` and `:201`, both
`adaptAnalysisRequestPdf`). So the `signedUrl` type against the `download_route.url` contract (rows W293-S1 and S2)
is adapted in one place, the same place that serves the report link. This run still reads the route directly, as the
packet says. The portal-side read is graded once in the portal flag's own DEV smoke.

## Conditions (in addition to section 3)

1. **The API base.** R0 states which deployed API the run calls, by its config source (the `vite.config` proxy target
   name, or the Terraform output name), never as a URL in the receipt. It is the deployed API that the PROD portal
   calls. A local dev server is used only as a proxy to that same API, never as a different backend. Any doubt STOPS
   before step A.
2. **Notifications.** Beyond `TICKET_DL_MAP` reading `{}`, R0 states whether ticket creation posts to Teams or any channel.
   Any recipient outside a synthetic or `@opalinvest.com` address STOPS before step T.
3. **The door.** A refusal at step U is an expected first stop (window 4). The receipt names its closed code, and the
   deletes then run for what exists. No second upload is tried in this pair.
4. **The poll budget** is 30 minutes in total with a 20 s step. Exceeding it is a STOP at the hop it reached, with the
   hop named.
5. **The receipt** carries the packager's own `IRPT_RESIDENT_PACKAGE` line for this run's message (outcome, or
   `retained_for_retry class= code=`), its UTC time, and the dead-letter depth before and after.
6. **On pass,** the receipt prints the PDF's size and content type, and `~Y2` reports to this seat. The portal flag
   `cand/dell2/anlreq-commentary-always-requested` then goes to DEV by its own approval row. Its PROD promote waits on
   Andrew's word (Ticket Center is client-facing).
7. **Timing:** outside the weekday 11:30Z to 14:15Z band. Today is Saturday, so it may run now. It never runs alongside
   another IB2 apply.

---

## ADDENDUM 1 -- SIGNED (2026-10-17 ~20:4xZ): name a synthetic advisor on the upload

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM1_ADVISOR_COO_HALF_20261017.md`.
I re-measured it: blob `02149564860419fbcb11e3add00de8617282af32`, equal at 5f19ba81e7 and in the working tree; sha256
`491648a2bad52856b7db7ff200b4b7b1557dc8701f225d4c2ed48c0495fabade`; 4,454 bytes. COO half signed. Ledger
`irpt-commentary-e2e-2-20261017`.

**Read at signing:** `infra/aws/lambda/investor-reporting/_authz/served.py:1089-1091` raises
`ProspectOwnershipRefused("an on-behalf upload must name the firm advisor")` when the upload names no `advisor_email`
and the tenant is in the actor's `allowedFirmIds`. That is the first run's stop. Neither the door nor the mint is wrong;
the run's steps lacked the advisor.

**Blast radius delta, accepted:** two more synthetic rows at 49financial, written and removed by the existing
`fwd1_advisor.py`. They are one `opal-users-v2` row (no credential, cannot sign in) and one `opal-partner-49financial`
row, and they exist only for the run. Nothing deployed moves.

**Conditions:** all seven of my conditions above stand, and these are added:
1. A2's pre-state refusal reads both rows ABSENT before any write. Monday's window-5 advisor (`...-20261019`) must not
   exist yet or be touched.
2. A closed authorization refusal at R (the route re-authorizes the owner placement, `ops/owned_report.py:347-349`) is a
   STOP at R with its code. It is an informative result, not a failure of this pair.
3. D removes the advisor rows by the tool's own `remove`, read back ABSENT, in the same receipt as the other deletes.

---

## ADDENDUM 2 -- SIGNED (2026-10-17 ~20:5xZ): re-post the identical upload while the door answers RESOLVING

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM2_RESOLVING_COO_HALF_20261017.md`.
I re-measured it: blob `5bddf32c3b213142e35f4d882fe6114de3c55fc3`, equal at d09a236b6c and in the working tree; sha256
`523d0f8380f1bc1ce05096a53711981a06f1aef20e2b2c88bc0822acccccd777`; 4,562 bytes. COO half signed. Ledger
`irpt-commentary-e2e-3-20261017`.

**Read at signing:** `infra/aws/lambda/investor-reporting/intake/uploads.py:522-533`. A retained `RESOLVING` row is
resumed. It is re-dispatched only after `REDRIVE_SECONDS` under a conditional replace, and it answers `RESOLVING` again.
A re-post of the same token creates no second object. The blast radius is unchanged.

**Accepted:** at most 5 identical posts, 3 s apart, the portal's own rule. A fifth `RESOLVING` is a STOP at U, with the
elapsed time and the resident journal's `RESOLVE` line count (window and total printed).

**Note:** if five tries at 3 s all answer `RESOLVING`, the portal's limit may be shorter than the resident's resolve
time. A real filing would then hit the same wall. That stop is a product finding for the next step, not a failure of
this pair.

My seven conditions and ADDENDUM 1's three stand. My condition 3 reads "no second upload": the re-post is the same
upload, not a second one.

---

## ADDENDUM 3 -- SIGNED (2026-10-19 ~15:3xZ): a fresh upload token and distinct bytes for run 4

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM3_FRESH_TOKEN_COO_HALF_20261019.md`.
I re-measured it: blob `f2baabd809e756324538352641b8ce1530c124da` (commit 4f2c13f0db), sha256
`493c7524e30a85fa98cbba2d0d17a9c02639ba6256d717cfd1f592063b2ccf24`, 4,935 bytes. COO half signed.

**Accepted as written:**
- R0 compares the token and the bytes' sha256 with every earlier run's, and any equality is a STOP before a write.
- A new staff address is used, and a new advisor dated 20261018. Both that advisor and Monday's 20261019 advisor are read
  ABSENT first.
- The token is fresh at the first post and never written down. The SPY row reads 101.
- K must read `no`.
- IB2's order: the r34l release first.

The blast radius is unchanged in kind: one more synthetic user, advisor and upload. One more standing 118-byte blob is
filed as a surprise row with its key; there is no deleter (D2-S211). All earlier conditions stand.

---

## ADDENDUM 4 -- SIGNED (2026-10-19 ~17:2xZ): backoff up to 4 minutes; no delete before the last read

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM4_BACKOFF_NO_EARLY_DELETE_COO_HALF_20261019.md`, blob `6c7c3bbaafc5149c3c95405bcc8091e20a151fbb` (commit 6649c9b54d), sha256 `ce1afb97ce23e1135cef60a3c956646ea54512d7e8c1d0a42941a22d7020202c`. COO half signed.

**Accepted:**
- U re-posts on the portal fix's backoff (3, 3, 6, 6, 12, 12, 24, 24, then 30 s; at most 240 s).
- Nothing is deleted before the run's last read and the resident's resolve of its own upload, or 5 minutes.
- D prints the first-delete and last-read times.

This verifies already-built code on PROD, so it is allowed under Andrew's pause (@444090ce10). It runs after r34l is live,
never alongside another IB2 act.

## ADDENDUM 5 -- SIGNED (2026-10-19 ~21:3xZ): run 4 reads the fresh report's sections once, read-only, as r34l's live proof

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM5_SECTIONS_READ_COO_HALF_20261019.md`
at commit `43ff3d7146`, blob `2ba7104f1d`, sha256 `560cb2c5b87221835ed8fd012d5b26e6ba3d05d9ad31f0b98893871312bb30b6` (re-measured by this
seat at HEAD). COO half SIGNED in the addendum.

**SIGNED**, bound to that blob and sha256, as an addition to the packet and ADDENDA 1-4.

**What this half covers:**
- **R0:** the running root must read `0485393f3a-r34l`; any other root STOPS the run before any write.
- **S:** the variant is Multi-Comp, with exactly two comparison keys, derived by the backend from the count.
- **R2:** ONE read-only `GET .../analysis/{REQ id}/sections` by the same synthetic user, one try. The receipt prints closed counts and names
  only, never a value.
- **Delta:** one read and no write. No object or principal is added, and D is unchanged (nothing is deleted before the last read).

**PASS** is per section 2: 0 builder-only sections without a value, 0 not-in-this-version, at least 1 value. A refused R2 is a finding,
not a release failure, and never a rollback trigger for r34l.

-- 1.0.0_SA_CTO~DELL2

## ADDENDUM 6 -- SIGNED (2026-10-20 ~00:1xZ): run 5 keeps ZQXWVK by the Keep re-post, records the finding, proves the swap

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM6_KEEP_REPOST_AND_SWAP_PROOF_COO_HALF_20261020.md`
at commit `3ec6395e39`, blob `161846b1f6`, sha256 `eb0f5929861abbcb5d2890c8920a4cfe797de04f4ec9a6ff5874baedd5d52c1a` (re-measured at HEAD). COO half SIGNED.

**SIGNED**, bound to that blob and sha256, as an addition to the packet and ADDENDA 1-5.

**What this half covers:**
- Exactly ONE Keep re-post of the same upload: the equal pair, sent only after exactly the one expected finding. The door makes no second
  object (`intake/uploads.py`).
- The finding is recorded as closed words.
- One more synthetic advisor date, 20261020.
- A read-only P6 proving the kept row is `UNRESOLVED/KEPT_AS_TYPED` with a swap outcome.
- No new write path.

**PASS** is as section 2.

**What this run does NOT grade:**
- It does not grade v0.24 FWD-1's bar (a staff filer with NOTHING seeded): this run still mints a synthetic advisor under ADDENDUM 1. The
  unseeded staff filing is graded after O1 ships.
- It proves: r34l's sections on a live report (ADDENDUM 5), the Keep path to C-SWAP (this addendum), and the commentary hops.

**Conditions:**
- After 07:00Z Tue and before 11:30Z.
- Not alongside TV2's R20_REL2 or any other IB2 act.

-- 1.0.0_SA_CTO~DELL2

## ADDENDUM 7 -- SIGNED (2026-10-20 ~02:1xZ): run 5B drops the second unknown row APPL; with a one-shot clean fallback

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM7_NO_SECOND_UNKNOWN_ROW_COO_HALF_20261020.md`
at commit `9adea1ea37`, blob `5dfb81ba80`, sha256 `05fec27809f32b6c2803eb0668a5a33b32fe6851abc43882763518fdbe76547a` (re-measured at HEAD).
COO half SIGNED.

**SIGNED**, bound to that blob and sha256, as an addition to the packet and ADDENDA 1-6.

**What this half covers:**
- A four-row synthetic file (SPY, AGG, TIMXX, ZQXWVK).
- The single equal-pair Keep, sent only when the one blocking finding is ZQXWVK and every other finding is a `TICKER_KEPT_BY_HISTORY`
  notice.
- PASS as section 2; no blast radius beyond ADDENDUM 6.

**Added by this half, under Andrew's relayed word (record `ANDREW_DIRECT_20261020_013xZ_R34L_LIVE_BEFORE_9AM_ET_VERIFY_FRESH_REPORT.md`):**
- If run 5B stops at U again, ONE run 5C may follow under its own ledger, with the three-row file SPY, AGG, TIMXX (no unknown row, no Keep;
  the U line reads `keep=not-needed`). Its purpose is that a fresh report's R2 sections read lands before 13:00Z.
- The blast radius is a subset of this addendum's: one fewer row and no Keep post.
- 5C proves r34l's sections only. The Keep-to-C-SWAP proof then moves to the next run.

**Windows:** before 05:45Z, or 07:00Z-11:30Z. Never alongside r37, r34m or any other IB2 act.

-- 1.0.0_SA_CTO~DELL2

