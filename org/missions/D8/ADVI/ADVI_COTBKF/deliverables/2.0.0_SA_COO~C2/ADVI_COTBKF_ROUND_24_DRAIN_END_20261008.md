# L8 drain end -- ADVI_COTBKF round 24

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~00:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB24x1-AC4)

Round 24 was cut as one issuance (@ed6fe05d5e, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-23 analysis
@19a4a6e00b (msg 1740), basis msg 1710 and the CRO's `RESEARCH_20261008_COMMONWEALTH_TWR_METHOD.md` @35c8aa0d75. The spawn was held
~22:1xZ-22:2xZ on the worker-definition YAML fix (MSTR msgs 1729, 1769). 1 of 1 order complete; drained @d9484f20fa (15 of 15 paths, 0
dropped); proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project. Risk LOCAL: nothing applied.

| order | item | worker | criteria |
|---|---|---|---|
| CB-x-1 | E1: rebuild the after arm on Commonwealth's stated method (`method` cash leg, now the default) | ~46 @b9f31e686c, @797dc26899 | AC1 31 passed; AC2 + AC3 `year_chain_same=True` (103/103); AC4 JUDGMENT, yours |

**Amendment 1** @a34db91fd0 (CTO msg 1944): AC2's no-sweep control replaced by the year-chain control. An account-wide method moves
no-sweep months by design (464 of 465 MATCH->MATCH moved a median 0.002 pts), so that control was the issuer's wrong choice. The
default switch to `method` was conditioned on a named cause for each of the 98 regressions; met.

## The real run, shared tree, after the drain (own `--data-dir`)

```
SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=8 fixed=8 months_before=2058/1525/79010 months_after=3059/925/78609 control_same=False regressions=98 movers_back=138 year_chain_same=True r22_named=25/25
pytest data/assets/scripts/silver/tests: 595 passed, 11 skipped
```

Identical to the worker's line. `control_same=False` is information only, per the amendment.

## What the round found

- **Whole grade:** MATCH 2,058 -> 3,059; DIFF 1,525 -> 925; UNGRADABLE 79,010 -> 78,609. This is the largest single move in the
  project.
- **Round 22's 25 months:** 25 of 25 MATCH. Round 22's 23 regressions are also all MATCH.
- **The 163 round-19 movers:** 138 MATCH, 25 DIFF.
- **Year-chain control:** 103 of 103 account-years agree (4,050 of 4,054 of Commonwealth's year rows chain their months; Opal computed
  all 12 months in 103 of them). The worst deviation is 3.98e-13 pts.
- **Cash ledger check:** the method's cash equals the 2026-06-23 snapshot's sweep + CFNCASH positions to the cent on 40 of 40 accounts.
- **The 98 MATCH -> DIFF months, each named** (`deliverables/0.9.0_WK_ADVI_COTBKF~46/sweep_regrade.md`; 0 unexplained):

  | cause | months |
  |---|---|
  | unlisted type: `ftax` 29, `ftax+stax` 1, `cbf` 3, `fco` 1, `stp` 1 | 35 |
  | dividend posted at pay date (`dv` 21, `dv+dvlt` 1) | 22 |
  | carried level: before the first valued day 16, `ManAltF` 14, trade cash 3, `csltfee` 2, other 4 | 39 |
  | `man` fee debit | 2 |

- **Dividend dating: NOT GRADED (row W46-S2).** No store the chain reads holds an ex-date; every dividend row carries the pay date
  only. The `--dividend-date pay|ex` option and `--ex-dates` input are built and tested; neither date is adopted.
- **Treatments not in the CRO's table (row W46-S3):** ASF, bcf, cbf, fco, stp, term, ftax, stax, frntax are kept at the default
  (internal). `ci` was applied as a flow per the CRO's list (no graded month contains one). `ManCheck` was read like `ManAltT`, untested.

**Rows this round:** W46-S1 (the ill-posed control, ruled), W46-S2 (no ex-date source), W46-S3 (unlisted types). OBSERVATION / INERT.
ARMED: 0.

**Round-close check:** REFUSED on one cause only: CB24x1-AC4 UNGRADED (judgment, yours at L9).

**Enrichment candidates for the round-24 analysis** (the CTO's to list; CTO msg 1944 names the first two):
1. **The unlisted types, `ftax` first.** Is a withholding that rides a withdrawal a flow? 35 months.
2. **Dividend ex-dates through the dell1 data-queue project** (Yahoo carries ex-dates); then grade pay vs ex with the swing. 22 months.
3. **The 16 levels present before the first valued day** (opening-state cash), and the 14 `ManAltF` carried levels.

**Parked, owner `~C2`:** the ranked price-need list, un-parked by the dell1 data-queue project's L2. **Still external:** that project,
MDPF_SECHIST's Bloomberg leg, the laptop's restricted-statements apply, Andrew's CRM landing; 316067107 PARKED with `1.0.0_SA_CTO~DELL2`.
