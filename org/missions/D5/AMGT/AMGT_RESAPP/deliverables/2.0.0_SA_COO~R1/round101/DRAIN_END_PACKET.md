# AMGT_RESAPP round 101 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-13 ~14:0xZ. Four orders, all complete: `AMGT-bh-1` (a build: the freshness snapshot is current by the trading calendar), `AMGT-bh-2` (its apply: `opal-amgt-scoped-api`
`42z0tn68..` -> `j+j1k5r7IY1ZCh9NijT8GSLaqEL3FhamwT8V3tYofCk=`, no served byte moved), `AMGT-bh-3` (a read: the cold first overlay on the live function with a current snapshot) and `AMGT-bh-4`
(a read: the first full weekday after the S3-client build).** Round 101 implements the CTO~DELL1 round-100 analysis `ledger/ROUND_ANALYSIS.round100.md` ADDENDA 1 and 2 (msgs 4292, 4347);
decomposition s.109; issuance @78d59f3ae4. One amendment (the issuer's own order, no gate limb graded it: it is a modification): `bh-3` AMENDMENT 1 @92c9b10d50.
`round-close-check.py --round 101`: orders 4, proof_ok 4 of 4, judgment 2 (`bh-3` AC2, `bh-4` AC2), graded 0, **verdict REFUSED until you grade both**.

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-bh-1` | the reader counts a stored snapshot current when written at or after the latest trading day's 12:30Z write (24-hour rule kept where the calendar cannot answer) | complete, merged @7da642c1ff | worker ~398; `snapshot.py` `f8df11bd6cce` -> `64fa354a1e1c` (+40 -1); 24 tests pass, rule check 11 of 11 |
| `AMGT-bh-2` | the apply of `bh-1` from merged pin `7da642c1ff`; ONE member differs | complete, SERVED: applied 2026-10-13T13:16:29Z (LastModified 13:17:52Z) by `0.7.0_AE_CloudOps~RA1`, commit d56643b4bb (on origin `box/dell1`, ls-remote read), ledger CLOSED, proof VALID | pair `ledger/NEVER_WIDEN_ROUND101_SNAPSHOT_RULE_REDEPLOY_{COO,CTO}_HALF.md` (COO @6d7a29efb8, CTO msg 4356) |
| `AMGT-bh-3` | read: cold first overlay, live function, snapshot current | complete, worker ~399 merged @92d43f8f91; closed @614de1ff58 | AC1 YES after AMENDMENT 1; AC2 yours |
| `AMGT-bh-4` | read: the first full weekday of the S3-client build | complete, worker ~400 merged @cc84bfa858; closed @1a7dec2185 | AC1 YES (9 of 9), proof VALID; AC2 yours |

## 2. The issuer's ONE REAL RUN at close

- **bh-2 (SERVED, WORLD): re-run by the issuer on the live function, after RA1's reads, alone** (RA1 released the hold at 13:32Z; my readers ran from 13:36Z). Deployed censuses
  `r97_sector_serve_census.py` (6 of 6), `r95_classification_census.py` (6 of 6), `r94_name_census.py` all YES; `r101_snapshot_equal.py` YES (302 rows against 302, differing 0, the packaged list
  files' deployed path allowed for and printed); `r89_deployed_close.sh --want amgt-corpus-dossier/15` YES. `r98_thesis_fullbody_compare.py --after local` from a detached worktree at the pin
  (the live function against the pin's own handler, 95 names, all 200): **0 paths under `team_sheet`, 5 generation clocks, 18 `float_repr` (the measuring checkout's python 3.14; the same 18
  as rounds 98 to 101), 0 other**: `R98 THESIS FULLBODY: YES`. `ay4_compare.py` re-run on RA1's pre and post captures: 95/95, 95/95, growth 0 for every name, build 1/1.
  RA1's compare: replay 527 requests, status moved 0, 36 clock paths, 0 over 20 s (max 2.87 s). RA1's first overlay requests after the apply (a cold pair): `ASML_NA` 25.26 s, `ADBE_US` 21.67 s,
  200, identical bodies: **the cold tail did not move, as the pair said it would not.** `r101_cold_live.py` read NOT QUIET (925 invocations in the prior 15 minutes were RA1's own captures), which
  the order names as an allowed reading; warm ASML 0.74 s, ADBE 0.67 s.
- **bh-1 (LOCAL): re-run on the merged tree.** `pytest` of the two freshness modules 24 passed; `r101_snapshot_rule_check.py` 11 of 11 (weekend and holiday clocks serve, a weekday past the
  write recomputes, bytes equal to the recompute).
- **bh-3 and bh-4 (reads): AC1 re-run by the issuer on each worker's tree** (bh-3 YES after AMENDMENT 1; bh-4 9 of 9 shape arms); the independent instrument for bh-4 is below.

## 3. What the readings say, and what they do not

1. **bh-3: with a CURRENT snapshot the cold first overlay on the live function reads 20.05 s** (cold container, init 687 ms); before Monday's write the same function read 22.39 s. The snapshot
   buys about 2.3 s of 22 s on Lambda. The order's own note said "if it still reads 20 s or more, the snapshot is not the lever on Lambda and `AMGT-bh-2` does not go"; the CTO, shown that reading,
   ruled in ADDENDUM 2 (msg 4347) that `bh-2` applies for the WEEKEND STEADY STATE (a warm request after the 60 s hold, 4.3 to 4.5 s recomputed against 1.27 s served locally) and not for the cold
   tail. The apply was made under that ruling, not under the order's note, which the ruling superseded.
2. **bh-4: the first full weekday had no organic traffic.** 625 invocations, 1 over 20 s, 0 pool-full. Lambda's own `Invocations` metric by UTC hour (not the log group) reads 308 at 12Z and 317 at
   13Z on 2026-10-12, 1 at 12Z on 2026-10-13 and no datapoint in any other hour: the function was silent and the logs lost nothing. The one over-20 s request is `bh-3`'s own cold probe
   (request d6d9ce24, 20049.86 ms, init 686.71 ms, 12:41:31Z); the other 623 are my sequential route measurement for the `bh-2` pair. The weekend's 45,646 invocations were seats' sweeps.
   **The CTO's day-after criterion (msg 4262: over-20 s and pool-full counted over a full day "against 53 and 49") is not gradable by waiting**: a quiet weekday has no concurrency to exhaust a
   pool, so 0 pool-full in 623 sequential reads is consistent with the build and is not a test of it. A deliberate concurrent replay would be; that call is the CTO's.
3. **What neither reading shows:** where the remaining ~20 s of the cold request goes on Lambda. That is round 102's first cell (below).

## 4. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **`bh-3` AC1's instrument read NO on a true YES.** It compared the Lambda-written snapshot with a checkout recompute and did not allow for the packaged list files' deployed path
   (`/var/task/...`), the only difference. **Cost: a BLOCKING row from the worker (`AMGT_RESAPP-D1-W399-S1`), AMENDMENT 1, one re-run and a worker proof that read INVALID until its
   PENDING-THIS-COMMIT artifact rows were re-pinned.** The control I now keep: an equality criterion's invocation is dry-run against the artifact the live function will actually produce, not a
   local twin of it, and a difference-class that is an environment fact is named in the order before the cut.
2. **I carried the weekend's raw counts forward as a baseline.** The `bh-2` status line recorded 45,646 invocations, p95 1,524 ms and 80 over 20 s (Saturday 12:30Z to Monday 12:30Z) as the
   weekend close's comparison, and `bh-4` was staged as a rate comparison against round 99's 53 of 32,528. **Neither asked what produced that traffic**; the metric by hour (bh-4's own attribution)
   shows seats' sweeps. Nothing was acted on the wrong baseline; the cost is a worker (~12 minutes), a reading that cannot grade its criterion, and a baseline line that had to be superseded
   (here). The control: before staging a "day-after rate" or "weekend count" criterion, read the reference window's SOURCE of traffic (the metric by hour against the seats' sweep times).
3. **The value of `bh-2` was first stated from local timings.** The local figures (a recompute 3.5 times faster than Lambda's) led the round-100 argument; bh-3's live reading came before the
   apply and cut the claim to ~2.3 s per recomputed request. The pair states the cold tail is not claimed and the weekend close is graded Lambda against Lambda. **Cost: an apply (a WORLD act,
   about 45 minutes of RA1's window) whose benefit is shown on Lambda only on Saturday.** (The same class as round 100's `bg-3`.)

## 5. JUDGMENT for L9

`bh-3` AC2 and `bh-4` AC2: that each reading states only what its numbers show. For your own re-run, read-only: `r101_cold_live.py` (announce it to the function's other readers: it invokes the
live function), the Logs Insights queries of `BH4_FIRST_WEEKDAY_READING_20261013.md`, and the `Invocations` metric by hour.

## 6. Rows filed this round

Worker ~399: `AMGT_RESAPP-D1-W399-S1` (BLOCKING, dismissed by the issuer: its cause is the issuer's instrument, AMENDMENT 1) and `S2` (resolved by the same amendment). Worker ~400:
`AMGT_RESAPP-D1-W400-S1` and `S2` (OBSERVATION, INERT, dismissed with no action). RA1: none. Issuer: none. **Disarmed by this round:** none open.

## 7. For the next round (the CTO's rulings; the ENRICHMENT LIST's inputs)

1. **Round 102's first cell (CTO msg 4347): per-phase `_phase_log` lines in the overlay handler**, log lines only, served bytes byte-equal, under its own pair; "no remedy before a day of real
   cold requests names the phase". **Open point for the CTO:** bh-4 shows there are no organic cold requests to wait for, so the attribution needs DELIBERATE cold probes (one per container
   lifetime, spaced past the idle recycle); the cell's close should name that, with the request count printed.
2. **The weekend close of `bh-2`** (the issuer's read): Saturday 2026-10-17 from 12:35Z, three DELIBERATE warm overlay requests more than 60 s apart, Lambda against Lambda, denominator printed;
   a fall from the 4.3 to 4.5 s the recompute costs locally scaled by the live figure. Raw weekend counts are not a comparison.
3. **The day-after criterion of `bg-3`** (section 3.2): the CTO's call: a deliberate concurrent replay, or retire it.
4. **Carried:** the portal PROD promote call `dell1-20261011T033643Z-e7f2` (Andrew), FWD-16, the model API key (Andrew), the CSL AU sector vintage (CTO call), `ss-7` and `pp-4` on the DEMQUE
   answer, `D1-W381-S1` (`0.0.0_AB_MSTR~DELL1`), and the carried EXPIRED-rule criterion for the first cell that reads `packs/<key>/status.json`
   (`ledger/CARRIED_CRITERION_EXPIRED_RULE_FOR_THE_FIRST_PULL_STATUS_READER.md`, none exists yet).
