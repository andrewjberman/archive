# AMGT_CORPUS -- round 16 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~22:5xZ.** One order was issued (@`89289bfbb5`, decomposition v16.0, fanout 1 of 1). It is
complete, re-graded at the worker's tip `dba1e7f6bb`, and merged at `bb2f3dbb18`. **The drain's WORLD act -- registering
`amgt-induction-daily` -- is HELD: the CTO half REFUSED @`90da2ced53` (msg 26766).**

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 1 of 1 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-r-1` | the daily trigger for `induction_run` (plan-only build) | `dba1e7f6bb` | `bb2f3dbb18` | proof VALID; AC1 `r1 scheduled_path planted_evidenced_requested 1 ambiguous_refused 1 bloomberg_calls 0 as_of_is_today True`; AC2 `r1 plan task_is_builder_name True commit_pinned True workdir_is_shared_tree False registered_now 0`; AC3 `paths_outside_grant 0`; `-Status` `NOT REGISTERED` |

**The issuance was refused once at the cut.** The preflight read `comp-schedule: DECLARED`, and the gate accepts only `RUN` or
`DECLARED-NOT-APPLICABLE`. This seat ran `comp-schedule`: 7 sentinel, 19 deploy-ledger, 12 moratoria and 0 scope-guard gates,
none on this surface. It recorded `RUN` and the issuance landed.

## 2. The drain act -- HELD

- **COO half** @`7e6944a068` (`NEVER_WIDEN_ROUND16_INDUCTION_SCHEDULE.md`). Before-state at 22:48:32Z (`evidence/r16_before.txt`):
  - population 0 of 96;
  - crosswalk 6 keys, latest `2026-09-29.json`;
  - task NOT REGISTERED; pinned path absent.
  - The half named branch 2's hazard as row `Z-S63`.
- **CTO half REFUSED** @`90da2ced53`.
  - Branch 2 (a fire with N > 0) appends N registration rows only to the PINNED checkout's `registrations.json`.
  - The next CLOUD-side `write_pool` builds from CLOUD inputs and silently drops them. There are 13 DEF writers.
  - Neither mode confines the pinned code to branch 1. A dry-run-only task would be a monitor.
- **Not refused:** the pinned-checkout mechanism, the 13:00Z cadence, the builder name, the ad-hoc QA plan and the stop limbs.
- **Nothing was registered and no checkout was created.** Task Scheduler and `...\Desktop\opal-pinned\` are unchanged.

## 3. The one real run

None beyond the re-grade. The act this round exists for is held, and its real run is the re-signed registration's ad-hoc QA
fire plus the first scheduled fire.

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-S61` | OBSERVATION, INERT | the producer registers EVIDENCED folders only; a Hitachi-type folder (identity only in its name) is never registered by the schedule. For the analysis: widen the rule or accept it. |
| `Z-S62` | disarm of `Z-S59` | safe-merge fixed @`ccf2a27c6b` (0.0.0_AB_MSTR~Z) |
| `Z-S63` | OBSERVATION, ARMED | a non-empty scheduled fire forks the registration ledger. Graded real by the CTO half; the remedy is the CTO's round-17 cell below. |

## 5. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

None on the order. The worker's own call: the 13:00Z start time. The order named no time; it is exposed as `-AtUtc`.

## 6. Enrichment candidates for the round-16 analysis

1. **The CTO half's cell:** `write_pool` / `build_crosswalk` never drops a record present in the latest served pool. It unions
   the pool with the build, and a record leaves only by explicit retirement.
   - AC: a planted pool record survives; a planted retirement removes it; today's pool round-trips 237 in, 237 out.
   - **Then r-1 re-signs on the same act, re-pinned to the commit that carries the invariant.**
   - Note for the cut: `crosswalk.py` is AMGT_RESAPP's identity module and is used by 13 writers. The cell's write set is
     cross-project, so the analysis should say which project issues it.
2. `Z-S61` (the EVIDENCED-only population rule), if the analysis wants it widened.

## 7. Bounds and residue

- No served write, no vendor call and no Task Scheduler write this round.
- The worktree `wk-crps16-1` is drained. Its removal, and the carried round-14 checkouts and system-temp entries, wait on
  Andrew's word.
