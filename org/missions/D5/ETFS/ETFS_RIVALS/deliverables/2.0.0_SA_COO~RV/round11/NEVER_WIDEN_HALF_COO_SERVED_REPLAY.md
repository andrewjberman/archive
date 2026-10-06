# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 11 item 2 -- the SERVED replay of the four G5 code classes (1,316 rows), G3-pinned

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-06 ~02:1xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).
**Rulings carried:**
- the round-10 analysis @134485f75b item 2 and ruling 1 (C-S42 + the review's s.5);
- round-9 addendum 2 @36310d88f1 (the replay comes after the `_g5_target` fix, before ok-1);
- round-9 ruling 3 (the RIV-e-2 and data-arrival classes keep their vintage).

## VERDICT: SIGNED

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** `etfs-rivalfunds-served-replay` and commit its sentinel at open.
2. **`serve`** (`C:/tmp/rv-served-signoff/served_replay.py`, sha256 `f766eacdb90de3a2...`, device-local; run with the replay tree
   `C:/tmp/rv-replay` @`59805c595c` = gt-1's branch, which is `0997603f5d` + gt-1, WITHOUT ok-1).
   - **Drift check first.** Re-list G1, G3, G5 and G6 on S3 and compare with the measure snapshot (1,359 / 4 / 1,357 / 1,033
     keys). **STOP** on any difference, or if any target key exists.
   - **Then write.** PUT exactly the 364 measured objects -- 182 G5 + 182 G6, one each per planned date, all `-v02` -- and read
     each back, bytes equal by sha256.
3. **No Lambda deploy and no page republish in this act.** The 07:00 ET marker publish and the 09:00 ET sweep read the new objects
   organically (every reader picks `revision.newest`). The ok-1 deploy (item 3) follows under its own pair.

## EXPECTED OUTCOME -- MEASURED

Measured 01:3x-02:0xZ by `served_replay.py measure`, read-only. The S3 listings were identical at its start and end.
Evidence: `served_replay_manifest.json` (656,912 B, sha256 `63879286d2952d16...`) and `served_replay_plan.json` beside this file.

- **Rows moved:** 1,316 over 182 dates (2026-01-02 .. 2026-09-29), 419 planned (date, fund) pairs.
  - By class: key_resolution_out_of_confidence 1,040, full_exit_priced 266, implausible_window_refused 10, own_prior_pairing 7.
  - These equal RIV-gd-1 and the rp-2 dry run.
- **Outside the classes:** rows moved 0; G3 label columns moved 0.
- **Labels and fills (C-S42):** 4,950 rows / 9,892 cells of G1 revision labels relabelled; 5,287 additive cells filled.
- **G6:** 0 (date, fund) pairs outside the plan differ. Planned funds' G6 rows change on INEQ 12, SCHY 63, ETFT 12, GQGU 61,
  CGIC 53, TXUE 10, BIDD 18, PCLG 12, BASG 3, TSEL 3, WCMG 2.
- **Names:** 182 G5 and 182 G6 objects, each `trades-<rev>-v02` / `reconciliation-<rev>-v02`. Every one is ABSENT on S3, so
  nothing is overwritten. They are stamped `producer_version` `gold_trade_schedule/2`.

### PER FUND (C-S42: rows moved, relabels, fills)

| fund | rows moved | G1-relabelled rows | relabelled cells | filled cells |
|---|---|---|---|---|
| BASG | 6 | 37 | 74 | 38 |
| BIDD | 19 | 95 | 190 | 114 |
| CGIC | 73 | 1,818 | 3,636 | 1,891 |
| ETFT | 21 | 54 | 106 | 70 |
| GQGU | 836 | 1,022 | 2,044 | 1,092 |
| INEQ | 62 | 331 | 660 | 393 |
| PCLG | 24 | 37 | 74 | 54 |
| SCHY | 251 | 1,462 | 2,920 | 1,522 |
| TSEL | 5 | 42 | 84 | 47 |
| TXUE | 13 | 50 | 100 | 63 |
| WCMG | 6 | 2 | 4 | 3 |
| **total** | **1,316** | **4,950** | **9,892** | **5,287** |

IDVZ and PFOE are not planned: their G5 was built from Bloomberg at D12 Step B with today's code.

## WRITERS AND READERS (one rule read each)

- **Writers of the touched prefixes:** the G5 stage (`gold_trade_schedule`) and this act. The live Lambda runs the pre-gt-1
  `_g5_target`. On a same-revision rerun it reuses the newest object when the held funds are equal, which after this act is the
  `-v02` -- so it writes nothing new. A new G1 revision builds a fresh object, as today.
- **Readers:** every reader picks `revision.newest` (capture time, then `-v<NN>`): `publish_page._by_date`,
  `gold_buying_trend._newest_by_date`, and `ai_accounts` (ai_accounts.py:555, :639). The publish guardrail compares
  `_base_revision` (publish_page.py:678), so `-v02` reads as the canonical revision and does not fail it.
- **W6-S2's first-window precondition:** G1 is staged from 2025-12-01 (`g5_drift.STAGE_FROM`), so each fund's first replayed
  window still finds its own prior report.

## BLAST RADIUS, PER KEY

| key | before | after | rollback (no delete) |
|---|---|---|---|
| `gold/trade_schedule/date=D/` for the 182 planned D | newest = the live object | newest = `-v02` (+1 object) | put the prior newest bytes as `-v03` |
| `gold/flow_reconciliation/date=D/` for the same 182 D | newest = the live object | newest = `-v02` (+1 object) | same |
| the page, buying trend and AI accounts from the next run | the live G5 | the replayed G5 | the rollback above, then republish |

## BOTH BRANCHES

- **Serve lands:** 364 objects, each read back sha-equal. A post-census of the served newest G5 per planned date against the
  measured bytes reads 364 of 364 equal. Ledger closed.
- **Serve STOPs or fails part-way:** nothing lands (STOP comes before the first PUT), or the objects already written stay and are
  listed. On the rollback branch, the prior bytes go back as `-v03` per key and the ledger stays OPEN and escalated.
