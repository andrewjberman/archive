# L8 drain end -- ADVI_COTBKF round 20

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~19:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB20t2-AC3)

Round 20 was cut as one issuance (@3ff22173a1, `fanout: 1 of 1 chains, cap 8`, a chain of two cells) on `1.0.0_SA_CTO~DELL2`'s
round-19 analysis @c015b6de3d (msg 1355). 2 of 2 orders terminal; the chain drained once at its end @16f0103204 (18 of 18 paths,
0 dropped); proofs VALID; 0 unmerged worker branches; 0 linked worktrees for this project. Risk LOCAL: nothing applied.

| order | item | worker | criteria |
|---|---|---|---|
| CB-t-1 | E1: class the 163 MATCH -> DIFF months; persist month grades | ~41 @101fb91b59 | AC1 9 passed; AC2 sum_ok=True |
| CB-t-2 | E2: sweeps-v2 with rule (b); re-grade v1 -> v2; control | ~41 @9e42830fa1, repair @900b146dd9 | AC1 13 passed; AC2 control_same=True; AC3 JUDGMENT, yours |

**Amendment:** @c6e1cae6d3 widened CB-t-2's grant by one path (`tests/test_commonwealth_mover_classes.py`), so the worker could fix a
CB-t-1 test that pinned the v1 arm to the CURRENT list version (row W41-S2). The criteria were unchanged. to-pipeline-gate graded the
modification (no limb fires on a modified order with `<placeholders>NONE`).

## The real runs, shared tree, after the drain

```
SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=8 fixed=0 months_before=2057/1522/79014 months_after=2057/1522/79014 control_same=True
MOVER-CLASSES movers=163 core=16 other_mmf=0 neither=147 sum_ok=True
pytest data/assets/scripts/silver/tests: 514 passed, 11 skipped
```

Both lines are identical to the worker's.

## What the chain found

- **E1, the 163 movers** (`deliverables/0.9.0_WK_ADVI_COTBKF~41/mover_classes.md`):
  - core (holds 316067107): 16;
  - other money-market fund: 0;
  - neither: 147.
  - The month grades of both round-19 arms are now persisted (`month_grades_before.parquet` / `month_grades_after.parquet`, one row per
    account and month). The re-run of the round-19 arms reproduces round 19's line exactly.
  - The movers are mostly NOT core-fund accounts, so rule (b) could explain at most 16 of the 163.
- **E2, sweeps-v2: the (b) entry did NOT land (row W41-S1).**
  - No custodian document or field naming 316067107 the core position is readable from the repo or the chain's data. `Position_Type`
    reads CASH for every security, and `Asset_Type` "Cash Equivalent" covers every money-market fund. The only claims of "core" in the
    repo are behavior-based (the round-19 CTO and CVO documents).
  - Per the ruling ("no source = no entry"), v2 has the same two members as v1 (both rule (a)). The entry is recorded as a candidate
    with `designation_source = None` and the places searched.
  - So v1 -> v2 is identical, and all 163 stay DIFF.
  - The MMF behavior census (accounts, rows, first date, same-day paired share, dividend months) for 316067107 and every other rejected
    MMF is printed, as a list only, in `deliverables/0.9.0_WK_ADVI_COTBKF~41/v2/sweep_regrade.md`. No MMF was added by census.
- **AC3 asks you:** whether the off-list decision is right, i.e. whether any source cited there or elsewhere is a custodian designation.

**Rows this round:** W41-S1 (no citable designation), W41-S2 (the CB-t-1 test pin, fixed @900b146dd9), W41-S3 (records S2's fix; the
row gate refuses an in-place edit, so S2's closure is yours in REMEDIATION). OBSERVATION / INERT. ARMED: 0.

**Round-close check:** `round-close-check.py --project ADVI_COTBKF --round 20` -> REFUSED on one cause only: CB20t2-AC3 UNGRADED
(judgment, yours at L9). Orders 2/2 complete.

**Enrichment candidates for the round-20 analysis** (the CTO's to list):
1. **The 147 `neither` movers.** In the worker's named table their v1 return sits a fraction of a point off a reported return near 0, a
   few in 2019 by 2 or more points. They are not core-fund accounts and need their own classing.
2. **A designation source for 316067107.** The candidate places are a custodian document or statement outside the repo, e.g. the
   laptop's restricted statements. If one is obtained, the change is one list entry and a re-run.
3. Carried: the `ZERO_BASE` prose in `commonwealth_flow_timing.py:188`.

**Still external:** MDPF_SECHIST's price load (FWD-3 coverage), the laptop's restricted-statements apply, and Andrew's CRM landing.
