# LGIC_NAMING N5 -- cross-bucket reader, score (cell LN-l-3)

Scorer: `0.9.0_WK_LGIC_NAMING~5`, branch `wk-lgic-naming-1-5`, run 2026-09-14 ~16:5xZ.
Task order: `org/missions/D14/LGIC/LGIC_NAMING/task-orders/LGIC_NAMING.TO-LN-l-3.cross-bucket-scoring.md`.

What was scored:
- the answers: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n5-reader.tsv` @15c38055ca (LN-l-2, `0.9.0_WK_LGIC_NAMING~4`)
- the key: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N5_KEY.json` @777770e6aa
- the addresses: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N5_ADDRESSES.json` @777770e6aa
- the checker: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py` @777770e6aa (`l3_correct` :411-420, `l3_control` :423-430)

## Checker output, verbatim

`L3-AC1`: `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py l3-correct`

```
WRONG: a3  labeled=DOES-NOT-FIT  expected=bucket,source,scope,tier,table,partition
CONFORMING ADDRESSES: 6  CORRECT: 5  WRONG: 1
VERDICT: FAIL-MISREAD
rc=0
```

`L3-AC2`: `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py l3-control`

```
NEGATIVE CONTROLS: 1  MARKED DOES-NOT-FIT: 1
VERDICT: PASS-CONTROL-FLAGGED
rc=0
```

## Every WRONG line

There is one:

```
WRONG: a3  labeled=DOES-NOT-FIT  expected=bucket,source,scope,tier,table,partition
```

## All seven, answer against key

| id | address | reader's answer | key | result |
|---|---|---|---|---|
| a1 | `s3://opal-data-49financial/advi/49financial/gold/advisor_positions/date=2026-09-12/data.parquet` | bucket,source,scope,tier,table,partition,object | bucket,source,scope,tier,table,partition,object | correct |
| a2 | `s3://opal-data-49financial/advi/49financial/platinum/advisors/advisor_id=A123/book.json` | bucket,source,scope,tier,table,partition,object | bucket,source,scope,tier,table,partition,object | correct (v1.3 entity partition) |
| a3 | `s3://opal-data-mdpf/mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | DOES-NOT-FIT | bucket,source,scope,tier,table,partition | **WRONG** (v1.3 code tier) |
| a4 | `s3://opal-data-mdpf/mdpf/cottonwood/platinum/model_portfolio/date=2026-09-12/model-portfolio.json` | bucket,source,scope,tier,table,partition,object | bucket,source,scope,tier,table,partition,object | correct |
| a5 | `s3://opal-data-mdpf/mdpf/global/gold/portfolio_weights/date=2026-09-12/data.parquet` | bucket,source,scope,tier,table,partition,object | bucket,source,scope,tier,table,partition,object | correct |
| a6 | `s3://opal-data-49financial/advi/49financial/state/run_cursor/latest/cursor.json` | bucket,source,scope,tier,table,partition,object | bucket,source,scope,tier,table,partition,object | correct |
| a7 | `s3://opal-data-49financial/gold/advi/canonical/accrual_materiality/date=2024-07-08/data.parquet` | DOES-NOT-FIT | DOES-NOT-FIT | control flagged (live legacy tier-first key) |

Denominators: 5 of 6 conforming addresses labeled as the key reads them; 1 of 1 negative control marked DOES-NOT-FIT.

## Recorded beside the miss (facts, not a grade)

- The key's own note on a3 (`N5_KEY.json:4`): "a3 is the v1.3 code tier (the table slot carries the built tier and the file is the named leaf in the partition slot, with no object)."
- The briefing the reader was given (`N5_ADDRESSES.json:6`) states one layout of seven segments ending in `{object}`, and its partition role (`:13`) is "a date=YYYY-MM-DD, or a named leaf, or an entity=id". It does not say that an address may end at the partition with no object, or that a tier word may sit in the table slot.
- The reader's stated reason for a3 (`deliverables/0.9.0_WK_LGIC_NAMING~4/cross-bucket-reader.result.md:18` @15c38055ca): "6 segments. After `code` in the tier slot, the table slot holds a second tier word (`gold`), and there is no partition".

Surprise row filed for the failing criterion: `LGIC_NAMING-W5-S1` in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
