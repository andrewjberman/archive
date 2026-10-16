# Never-widen CTO half -- IRPT_ANLREQ FWD-1 run, ADDENDUM 3 (the third window: the step-0 probe, W7, and run 3 on r34)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~05:2xZ. **COO half:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_THIRD_WINDOW_COO_HALF.md`
at commit `db78445db3`, blob `64884b3338965c79a962c3f40cdb5cde44ad5811`, sha256 `d69d8441e80fc35a11cfac256f66ee632d427b50fffc9028909cf076d0a43dfd`
(both re-measured by this seat). It amends the first pair and ADDENDUM 2, whose CTO halves stand.

## Verdict

**SIGNED** on that blob, covering section 6 with section 8 (a) to (c). One signature covers the probe and the run, as ruled on call c116
(msg 9083).

## What this half covers

- **(a) W7:** after the Submit click, the driver presses only the planned decision buttons (Yes / Replace / No), each re-posting the same
  upload. It is bounded at six re-posts and adds no new principal or route.
- **(b) W8, step 0, the probe:**
  - one transient internal-viewer identity: a 20-minute token, never written or logged, the row removed and read ABSENT;
  - at most five probes of the upload route, at least 15 s apart, with the fixed candidates `ALPPL, APPL, BREIT, SREIT, ZQXWVK` in that order;
  - only the status, finding code, suggestion-present flag and actions are recorded;
  - the deterministic selection rule for U1 to U3, and the run inputs it fixes, with their sha256 printed before the run row is minted.
  - Any vendor touched is reached through the door's existing calls only: the door's suggestion step and r34's yfinance checker. There is
    no new vendor leg.
- **(c) Evidence kept:** the persisted ticket, input and request, and any object the probe or the window writes, stay as evidence. A
  delete of any of them is a later call for Andrew.

## Conditions (each is a STOP)

1. **R0e is the gate of the whole window:** the re-applied R34B reads V1 green AND V2 SPY KEPT. Anything else stops before step 0, with
   nothing minted.
2. **The intake prefix is listed before and after the probe** (versions, markers, counts). A new object is a finding, listed by key and
   VersionId. The window continues, but that object is never deleted in the window.
3. **The swap pass's Yahoo calls are counted in the resident journal** against R34B's per-holding bound. Any call beyond it is a STOP.
4. **A row the probe cannot fill is UNEXERCISED, never improvised.** No candidate is added in the window. A new candidate list is a new
   addendum.
5. The DLQ message of window 2 stays untouched. The run drives portal DEV at or after `f7eb6b14` from a private worktree on port 5174.

-- `1.0.0_SA_CTO~DELL2`

## AMENDMENT 1 (the re-pin), SIGNED 2026-10-16 ~06:5xZ

**COO half:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_AMENDMENT1_REPIN_COO_HALF.md`,
blob `7a4e8735155f871b8f8573d0d4d0f3cc63704bec`, sha256 `52430487da67ad423e456dae6cd61fde1f077fa53458ee0a34fd742d89b11f55` (re-measured).

**SIGNED.** It replaces ONLY R0d and R0e:
- **R0d:** `irpt-ycharts-generate` stays at r33 `kxOEgpbs...`; `irpt-status` moves to r35L `+TcZDWmw...` (live, AQ2 msg 9129).
- **R0e:** the resident root `0485393f3a-r34c` from the R34D tar `272d5c54...2ff8` (packet blob `6feb7b728c`, signed @b249e74f7a), with the hard
  gate: the closure pair installed first, V2 SPY KEPT, V3 UpdateItem allowed.

W7, W8 and every other term and condition of ADDENDUM 3 and of this half stand unchanged. The earlier blob b778d4072e was never signed.

## AMENDMENT 2 (the probe re-post), SIGNED 2026-10-16 ~07:3xZ

**COO half:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_AMENDMENT2_PROBE_REPOST_COO_HALF.md`,
blob `e9347582e07326f15f4dc0c099add09f198f78e9`, sha256 `5e0d8a9e1726758027d960288aebcd4be3b40a509c4698f176bb587c3cd51204` (re-measured).

**SIGNED.** It replaces only W8's "each ONCE". AQ2's R33 trace shows a fresh upload token answers RESOLVING first, so a single post records
nothing. The rule now:
- Post once.
- **If and only if** the answer is RESOLVING, wait at least 15 s and re-post the SAME upload (same token, same file) once, keeping the second
  answer.
- At most two posts per candidate, ten in all.
- A second RESOLVING is recorded as such. There is no third post, and the U-row stays UNEXERCISED if no candidate qualifies. No candidate is
  improvised.

Same identity, same route, no new reach. The before/after listing of the intake prefix and the no-delete-in-window condition stand
unchanged.


## AMENDMENT 3 -- second probe set, the stored-object claim corrected, R0e re-pinned to r34d (2026-10-16 ~12:1xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_AMENDMENT3_SECOND_PROBE_R34D_COO_HALF.md`
(msg 9332), blob `0975453cd1e992d8244ba9abccda90bb3e0f308b`, sha256 `6dbc6c5f32da09d6cfc403a6fefdcd68159caf67855f6fc3ec0b33ee7b5ca972`,
7,812 bytes (re-measured). R0e's r34d binding equals the blob I signed for r34d (`60cf9b70bc`, section "SIGN on r34d" of my R34 half).

**Read.** The correction is the one I asked for in msg 9288: "stores nothing" becomes MEASURED false, and every probe object is listed by key
and VersionId. The second set repeats step 0 once with the same five candidates under a new viewer name, at most ten posts.

**Conditions** (each a STOP):
- **The order leaves HOLD only after ledger `irpt-resident-r34d-20261016` reads CLOSED with `V2S OK` from inside the service.**
- **All five reading CHECK_FAILED again stops the window before the run user is minted.** No B-only run, and a third probe set needs a new
  amendment.
- **ZQXWVK must read NOT_FOUND.** If it does not, the fix did not reach the door: stop and report, whatever the other four read.
- **Every SET 2 object goes into row dc59's source record the same session.** The delete stays Andrew's act, after run 3 is graded.

## AMENDMENT 4 -- R0e re-pinned from r34d (rolled back) to r34e (2026-10-16 ~13:3xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_AMENDMENT4_REPIN_R34E_COO_HALF.md`
(COO half @0d7d051f08), blob `a560bc08075380f7b0137015e3fb2ef9e935dcb8`, sha256 `43feb386e4d3bc3945a024fe9f5c5bfc6c5ba30a6d390a5a52969f15d496be93`,
5,312 bytes (re-measured). Only R0e's pins change. Its r34e binding (packet blob `fd4c17188b`, tar `a96fbfb7...9227`) equals the r34e
signature in my R34 half (@5699c80f35). AMENDMENT 3's terms and my conditions on it stand.

**Condition:** HOLD lifts only after ledger `irpt-resident-r34e-20261016` reads CLOSED with both `V2S OK SPY KEPT and ZQXWVK NOT_KEPT` and
`V2S CONTROLS OK 4 of 4` from inside the service. SET 2's ZQXWVK must read NOT_FOUND at the door, or the window stops.

## AMENDMENT 6 -- one SET 3 (ZQXWVK first, one in flight, 90 s re-post wait) (2026-10-16 ~14:1xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_AMENDMENT6_SET3_COO_HALF.md`
(COO half @73e3ccb390), blob `53decf2ba991ee9e258650ca62968bf2040d6b88`, sha256 `8d1f46e75eb440b66b850099df952fd03460fbda010d86b2416c720d9963c0fd`,
5,384 bytes (re-measured). Only the probe set changes; it is my msg 9446 as written.

**The residual risk (its section 4) is ACCEPTED, with one condition:** the run continues after SET 3 only if SET 3's window shows ZERO
`WAF_CHALLENGE` journal lines. The run's own uploads are posted the way SET 3 is, one in flight at a time. A WAF line in SET 3 ends the
window unspent, and the run then waits for the bounded backoff change (`~G2`, its own pair).

## AMENDMENT 7 -- R0e re-pinned to r34f; the run goes on SET 3's selection, no further probe (2026-10-16 ~16:0xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_AMENDMENT7_REPIN_R34F_COO_HALF.md`
(COO half @1a907fdddf), blob `1355fd0c6d2c6203436a9923b595ff66e76b6c4d`, sha256 `06f71646069bf8db88b4247b89b4ddfb295d51b9aeb487b91c783726d9284c77`,
5,276 bytes (re-measured). Its r34f binding (packet blob `e9ede8d67f`, tar `0d223e50...4a3f`) equals my r34f signature (@57f0938a30).

**Section 3 RULED as proposed: no SET 4.** SET 3 met my stop: ZQXWVK read NOT_FOUND at the door. Its selection stands (U1 ALPPL, U2 APPL,
U3 ZQXWVK). A further probe would spend the lookup budget the run needs. SET 3's WAF line ended that window under my AMENDMENT 6 condition;
r34f is the backoff that condition waited for.

**Conditions:** HOLD lifts only on ledger `irpt-resident-r34f-20261016` CLOSED with `V2S OK`, `V2S CONTROLS OK 4 of 4` and `V2S BACKOFF`
from inside the service. The run's uploads go one in flight at a time. A row ending RESOLVE_RETRY_EXHAUSTED during the run stops the run and
is reported, never retried in the window.

## ADDENDUM 4 -- WINDOW 4 on r34g, deterministic branches only (2026-10-16 ~19:0xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM4_WINDOW4_COO_HALF.md`
(COO half @21e1a1f85d), blob `85115a4f0397c7665b5d2d52fcf5cd8c035838eb`, sha256 `73a73670688f84b4ffd7c7cdf48d8581ec6772ce4cbc725698a830687f261b1d`,
10,181 bytes (re-measured). R0e = r34g (my signature @d5c047fa37). The branches are fixed, as I ruled in msg 9684: ZQXWVK Replace VNQ; APPL
No, then UNRESOLVED, then C-SWAP; ALPPL Yes only if offered, else No. No probe and no selection rule. **Section 2.2, REUSING
`fwd1-staff-r41b@opal.invalid`: ACCEPTED** (removed and read ABSENT at 17:04:02Z, already on the producer list). `allowedFirmIds
["49financial"]`, staff only, zero entitlement rows. Applier IB2.

**Conditions:** the YCharts budget (6 calls per 390 s, counted per securities_info call); the run's evidence is recorded before AR-v-34
drives any failure on its job row; a RESOLVE_RETRY_EXHAUSTED row stops the run without a retry in the window. The window does not use
localhost:5174, which is Andrew's smoke server.
