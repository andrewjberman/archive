# L8 drain end -- IRPT_CUSTDY round 3 (E1 and E2; E3 gated, not cut)

**Issuer:** `2.0.0_SA_COO~K2` (dell2) | **Date:** 2026-10-07 ~10:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no JUDGMENT criteria)

Round 3 is the round-2 analysis's gated list (`1.0.0_SA_CTO~DELL2` @10e64fe9df): each item issued the tick its gate opened
(`decompositions/IRPT_CUSTDY_DECOMP.round3.md`). Two gates opened, two items issued and drained; the third gate is still closed.

| item | gate | issuance | order | drain | proof | real run on dell2 |
|---|---|---|---|---|---|---|
| E2 hop 3 on real returns | S4 FILE @ef5ea44568 (msg 286) | @0e054dd64e (workstream ~K2) | CU-c-1 hop3_real_run.py, worker ~7 | @1312dbea80 | VALID: AC1 10 passed, AC2 SELFTEST all True | `HOP3-REAL-RUN advisor=matthew_gooch as_of=2026-09-30 households=10 accounts=14 uncovered=4 held_si=0 error=none` (rc 0, ~10:46Z, after the fence on `opal-data-49financial` lifted; laptop relay 346 withdrawn). Graded in row S8 |
| E1 the 482 re-read | IRPT_BCKEND E-P8 = IB-pr-339 drained @b43f82c155 (msg 299) | @9b91ef7a78 (workstream ~K2-E1) | CU-c-2 pick_reread.py, worker ~8 | @f4ccdbf04e | VALID: AC1 9 passed, AC2 `reasons_sum_ok=True` | `PICK-REREAD before_refused=482 after_refused=0 of=7022 uncovered=2189 reasons_sum_ok=True advisor=matthew_gooch advisor_still_eligible=True pick_now=matthew_gooch` (NOT_IN_DIRECTORY 1961, NO_SILVER_AT_AS_OF 228, COVERED 4833) |
| E3 the 49 Financial template | portal kit on dell2 | not cut | -- | -- | -- | `portal/node_modules` absent (row S5) |

**E2 graded from the real run (row S8):** accounts QTD/YTD/1Y OK 14 of 14; households QTD and YTD OK 10 of 10, 1Y OK 7 and NO_DATA 3
(shown in place); every figure names its source rows, 124 of 124; SI is NO_DATA on every account and household because no inception
anchor resolves, so the "SI held before 2024" criterion is vacuous; 4 granted accounts are NOT_IN_DIRECTORY. The real-run file holds a
real advisor's client figures and is NOT committed; the row carries its measured summary.

**Drain checks** on `data/assets/scripts/gold/irpt_custody/` after the last merge: `py_compile` 8 of 8, ruff clean, `pytest` 73 passed,
1 xfailed, 1 failed -- `test_none_source_names_the_seam_line` only, row S7 (IRPT_BCKEND's seam fix removed the refusal that round 2's
tracer test fabricates). 0 linked IRPT_CUSTDY worktrees.

**Process notes:** the L6 gate's one-issuer-per-round limb (no override) admitted E1 only as its own workstream `~K2-E1`, since E2 was
already issued for round 3. HOLD A was lifted for 2010-2027 (msgs 317, 322) mid-round; this lane produced no pre-2024-dated artifact.

**FWD-1 thread: NOT LIVE.** Hops 1-3 run on real data. Hop 4 (descriptions) is built; hop 5 waits on IRPT_BCKEND a1-a4 and on E3;
hop 6 is Andrew's.

## Rows of the round

| row | class | standing | note |
|---|---|---|---|
| S6 | OBSERVATION | INERT | S4's FILE proved presence (6854 accounts at 2026-09-30) but carried no figures; E2 re-cut as a wrapper |
| W7-S1 | OBSERVATION | INERT | the face's "no 8+ digit run" masking test also hits floats, masters and dated filenames; narrowed to account values |
| W7-S2 | OBSERVATION | INERT | on dell2 the deny was at the firm-bucket read only (before ~10:44Z) |
| S7 | OBSERVATION | INERT | drain red: the none_source fixture test after the upstream seam fix |
| S8 | OBSERVATION | INERT | E2's grade on the real run; the SI anchor gap; 4 NOT_IN_DIRECTORY |

**For the round-3 analysis (not rows):** the SI anchor gap (S8) and moving the SI hold floor 2024 -> 2010 (HOLD A lifted); the 1961
NOT_IN_DIRECTORY accounts after the seam fix are an IRPT_BCKEND directory-coverage question; S7's repair (retire or re-point the tracer).

-- 2.0.0_SA_COO~K2
