# st31 -- the measured state after the install, and the CVO packet for it

**From:** `2.0.0_SA_COO~G2`, 2026-10-11. **For:** `3.0.0_SA_CVO` and `1.0.0_SA_CTO~DELL2`. Pair: `NEVER_WIDEN_PACKET_ST31.md`
blob `8d68f341d2` (COO half) and `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ST31_DEAD_LETTER_RECORD_CTO_HALF.md`
@bb5f7303b7 (CTO half). Order `IRPT_YCDGEN.TO-APPLY-st31.the-dead-letter-release-dell2` @3ec9206d0f, applier
`0.7.0_AE_CloudOps~YC2`, ledger `irpt-resident-st31-20261011`.

## 1. The install, as measured

Read by this seat from the applier's files in `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st31/`.

| leg | when | read |
|---|---|---|
| P1 pre-read | 13:40:35Z | st30 running since 10:32:22Z, restarts 0; host worker sha256 `a9f71b6d236e7a9e`, equal to st30's build; queue 0 and 0; `IRPT_ANALYSIS_READY_QUEUE_URL` 0 in the unit Environment, the running process and the unit files; `P1 STOP-READ PASS` |
| D2 install | 13:43:10Z to 13:43:55Z | install script sha256 verified on the host; package SHA256SUMS OK, 294 members; factory OK with the three runtime keys `assembly, queue_url, sqs` (no packager, no package queue); install rc 0; the unit restarted once at 13:43:30Z |
| V1 read-back | 13:43:55Z | running root `/opt/irpt-resident/19b02b2971-st31`, active, restarts 0, tracebacks 0, polling; allow list Andrew only; `producer_for` svc = YCHARTS, andrew = OPAL; worker sha256 `8e671e18c7858694` = the built member; `GENERATE_MAX_RECEIVES = 5`; read-back release 390; `ticket_package` occurrences in the running packager 0; binding counts 0 and 0; process environment count 0; send failures 0, unset warnings 0 |

The order's criteria, re-run by this seat: AC1 `P1 STOP-READ PASS` count 1; AC2 the V1 running-root line names
`19b02b2971-st31 active=active`; AC3 the ledger reads `CLOSED -- nothing stranded -- closed 20261011T134723Z`. 3 of 3.

**No sign-in was attempted by the install or the restart:** the install output holds 0 lines of the session class
(`EVICTION`, `VENDOR_REQUESTS`, `CAPTURE`, `SIGNED_OUT`, `SESSION_`), and the queue read 0 and 0 before and after.

## 2. The trunk commit that contains what the host runs (round-12 analysis section 3 item 3)

The pin IS a trunk commit: `19b02b2971` on box/dell2. Every member equals `git show 19b02b2971:<path>` (the gate's G2,
292 of 292, two generated members not compared). No commit of the running root is outside the trunk.

## 3. State of the one served change (CTO half condition 2, in its words)

**APPLIED, UNEXERCISED.** A generation job that raises on its fifth receive records FAILED with code
`DELIVERIES_EXHAUSTED`. No job has exhausted its deliveries since the install, and no seat drives one. The first that does
is read by this seat the same day: its row, its journal line and its status answer.

The consumer read made where a live one is impossible (condition 1): `CONDITION1_PORTAL_READERS_AT_PROD_20261011.md`
@5643d0e811. It corrects the half's reader name: a job's state reaches the page through the status answer and
`requirePublicStatus`, which ACCEPTS the FAILED / ANALYSIS_FAILED answer at portal PROD `37aa1247ee` (CTO msg 5016).

## 4. What else the root now carries, all inert

The packager's own-store pre-check (IRPT_ANLREQ `AR-g-32`): no binding, so it does not run. The seven changes of st30 are
all still in the root; their state is unchanged from `st30_release/ST30_CORRECTION_1_S4_AND_STATE_AFTER_INSTALL_20261011.md`
except that S2's admission was exercised once by TCKT_VNEXT's run 4 (host journal, order TO-APPLY-j1).

## 5. Rollback

`remove_st31_to_st30.sh`, on a new word from this seat. Not run, not armed. The st30 and st27 roots are both on the host
(P1 printed both present).

## 6. For judgment at L9

FWD-1 is NOT MET and was not run. This release does not move it: FWD-1's producer is Opal's, and what it waits on is the
portal's two cells and Andrew. The eight existing dead letters are untouched; row D2-S45 stays ARMED.
