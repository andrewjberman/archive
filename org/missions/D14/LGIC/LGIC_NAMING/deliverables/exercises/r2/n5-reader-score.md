# LGIC_NAMING round 2 -- N5 cross-bucket reader, scored (LN-l-3, round 2)

**Scorer:** `0.9.0_WK_LGIC_NAMING~6` on `LGIC_NAMING.TO-LN-l-3-r2` | **Worktree base:** `CLOUD` @8de38d4a93 | **This cell scores; it does not read.**

**Inputs (read-only, as found at 8de38d4a93):**
- the answer: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n5-reader.tsv`, written by the clean-context seat of LN-l-2 round 2 (commit 3fecf3a37f; header `# base 619dec559fe82915c6a2c325a0f9f718270b08d0`, `# seat 07de665f-d708-416a-9f2c-7710b2e3380e`)
- the addresses: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N5_ADDRESSES.json`
- the key: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N5_KEY.json` (round 1's, unchanged: RULING K changed the briefing, not the layout)
- the checker: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py` (`l3_key()` reads `N5_KEY.json` above)

## Checker output, verbatim

`L3R-AC1`: `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-6b && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py l3-correct`

```
CONFORMING ADDRESSES: 6  CORRECT: 6  WRONG: 0
VERDICT: PASS-ALL-READ-RIGHT
RC=0
```

`L3R-AC2`: `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-6b && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py l3-control`

```
NEGATIVE CONTROLS: 1  MARKED DOES-NOT-FIT: 1
VERDICT: PASS-CONTROL-FLAGGED
RC=0
```

## WRONG lines

**None.** The `l3-correct` run printed no `WRONG:` line: 0 of 6 conforming addresses were mislabeled. The negative control (1 of 1) was marked `DOES-NOT-FIT`.

## Every address, its labels and its expected roles (all 7 of 7)

| id | address (N5_ADDRESSES.json) | labeled (n5-reader.tsv) | expected (N5_KEY.json) | match |
|---|---|---|---|---|
| a1 | `s3://opal-data-49financial/advi/49financial/gold/advisor_positions/date=2026-09-12/data.parquet` | `bucket,source,scope,tier,table,partition,object` | `bucket,source,scope,tier,table,partition,object` | yes |
| a2 | `s3://opal-data-49financial/advi/49financial/platinum/advisors/advisor_id=A123/book.json` | `bucket,source,scope,tier,table,partition,object` | `bucket,source,scope,tier,table,partition,object` | yes |
| a3 | `s3://opal-data-mdpf/mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | `bucket,source,scope,tier,table,partition` | `bucket,source,scope,tier,table,partition` | yes |
| a4 | `s3://opal-data-mdpf/mdpf/cottonwood/platinum/model_portfolio/date=2026-09-12/model-portfolio.json` | `bucket,source,scope,tier,table,partition,object` | `bucket,source,scope,tier,table,partition,object` | yes |
| a5 | `s3://opal-data-mdpf/mdpf/global/gold/portfolio_weights/date=2026-09-12/data.parquet` | `bucket,source,scope,tier,table,partition,object` | `bucket,source,scope,tier,table,partition,object` | yes |
| a6 | `s3://opal-data-49financial/advi/49financial/state/run_cursor/latest/cursor.json` | `bucket,source,scope,tier,table,partition,object` | `bucket,source,scope,tier,table,partition,object` | yes |
| a7 (negative control) | `s3://opal-data-49financial/gold/advi/canonical/accrual_materiality/date=2024-07-08/data.parquet` | `DOES-NOT-FIT` | `DOES-NOT-FIT` | yes |

Denominators: conforming addresses 6 of 6 correct; negative controls 1 of 1 flagged; all addresses 7 of 7 labeled as the key reads them.
The table is a transcription of the three input files for the reader; the verdict is the checker's output above, not this table.
