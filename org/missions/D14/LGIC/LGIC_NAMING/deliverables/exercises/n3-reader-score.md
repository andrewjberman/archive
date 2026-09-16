# LGIC_NAMING N3 -- the blind reader's score (cell LN-e-5)

Scorer: `0.9.0_WK_LGIC_NAMING~5`, branch `wk-lgic-naming-1-5`, worktree HEAD at run `23beb7751c`, 2026-09-14.
Task order: `org/missions/D14/LGIC/LGIC_NAMING/task-orders/LGIC_NAMING.TO-LN-e-5.reader-scoring.md`.

What was scored (none was edited):
- the names: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-namer-a.tsv` @254a310135 (LN-e-1)
- the marks: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-reader.tsv` @3c2910ac09 (LN-e-4, `0.9.0_WK_LGIC_NAMING~6`)
- the items: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa
- the key: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_KEY.json` @777770e6aa
- the checker: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py` @777770e6aa (`e5_correct` :287-302, `e5_consistent` :305-317)

## Checker output, verbatim

`E5-AC1`: `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py e5-correct`

```
WRONG: i07  name=mdpf-gold-read-policy  marked=mdpf  expected=none
WRONG: i08  name=etfs-price-refresh-dlq  marked=etfs  expected=none
WRONG: i14  name=mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz  marked=mdpf  expected=global
WRONG: i17  name=etfs-pipeline-alerts  marked=etfs  expected=none
ITEMS: 18  CORRECT: 14  WRONG: 4
VERDICT: FAIL-MISREAD
rc=0
```

`E5-AC2`: `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py e5-consistent`

```
NAMES: 18  TOKENS MARKED AS A FIRM OR PRODUCT: 9  A MARKED TOKEN READ OTHERWISE ELSEWHERE: 5 [('mdpf-cot-exporter-sg', 'mdpf', 'cot'), ('mdpf-cot-publisher-lambda', 'mdpf', 'cot'), ('mdpf-demo-publish-failure-alarm', 'mdpf', 'demo'), ('mdpf-inf-delivery-status-table', 'mdpf', 'inf'), ('mdpf/49financial/platinum/advisor_books/advisor_id=A123', 'mdpf', '49financial')]
VERDICT: FAIL-TWO-REFERENTS
rc=0
```

The E5-AC2 line prints at most 5 clashes (`clash[:5]`, `check_ln.py:317`); its count is 5, so all 5 are shown.

## Every WRONG line (E5-AC1)

There are four:

| item | name | reader's mark | expected token (N3_KEY.json) |
|---|---|---|---|
| i07 | `mdpf-gold-read-policy` | `mdpf` | `none` |
| i08 | `etfs-price-refresh-dlq` | `etfs` | `none` |
| i14 | `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | `mdpf` | `global` |
| i17 | `etfs-pipeline-alerts` | `etfs` | `none` |

## All eighteen, mark against key

| item | name | reader's mark | key | result |
|---|---|---|---|---|
| i01 | `mdpf-cot-publisher-lambda` | cot | cot | correct |
| i02 | `blackdiamond-49f-session-fetch-role` | 49f | 49f | correct |
| i03 | `orion-inf-ingest-daily` | inf | inf | correct |
| i04 | `schwab/49f/api-credentials` | 49f | 49f | correct |
| i05 | `opal-data-cottonwood` | cottonwood | cottonwood | correct |
| i06 | `eclipse/inflection/silver/account_holdings/date=2026-09-14` | inflection | inflection | correct |
| i07 | `mdpf-gold-read-policy` | mdpf | none | **WRONG** |
| i08 | `etfs-price-refresh-dlq` | etfs | none | **WRONG** |
| i09 | `mdpf-demo-publish-failure-alarm` | demo | demo | correct |
| i10 | `smartx-49f-platform-export-weekly` | 49f | 49f | correct |
| i11 | `pathfinder-etfs-ingest-task` | etfs | etfs | correct |
| i12 | `blackdiamond-cot-download-document` | cot | cot | correct |
| i13 | `mdpf/49financial/platinum/advisor_books/advisor_id=A123` | 49financial | 49financial | correct |
| i14 | `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | mdpf | global | **WRONG** |
| i15 | `orion-inf-gold-build-profile` | inf | inf | correct |
| i16 | `mdpf-cot-exporter-sg` | cot | cot | correct |
| i17 | `etfs-pipeline-alerts` | etfs | none | **WRONG** |
| i18 | `mdpf-inf-delivery-status-table` | inf | inf | correct |

Denominators: 14 of 18 names marked with the key's token. For E5-AC2, 9 distinct tokens were marked as a firm or product
across 18 names, and 5 names carry a marked token (all five `mdpf`) that the reader read as something else.

## Recorded beside the misses (facts, not a grade)

- The key's rule (`N3_KEY.json:4`): "'global' for the shared product scope of a key, and 'none' for a shared resource that
  carries no scope (S5)". All four WRONG lines are on the shared rows. Three are `none` in the key, where the reader
  marked the product token in the name's first slot (`mdpf` on i07, `etfs` on i08 and i17). The fourth is i14, `global`
  in the key, where the reader marked `mdpf`.
- The reader's stated rule (`LGIC_NAMING-W6-S2`, channel `INVESTIGATION_v1.md`): "marked the firm token whenever one
  was present and the product token otherwise". The reader saw no firm token in i07, i08, i14 or i17, so it marked the
  product token, where the key has `none` or `global`.
- All 5 E5-AC2 clashes are the token `mdpf`. The reader marked `mdpf` on i07 and i14 (both WRONG above) and read it as
  the product prefix, not the mark, on i01, i09, i13, i16 and i18.
- Read, not run: `N3_KEY.json:8` has `etfs` for i11 and `none` for i08 and i17, and both i08 and i17 carry the token
  `etfs`. Under `check_ln.py:308-314`, a reader who marked exactly the key's 18 tokens would print 2 E5-AC2 clashes
  (i08 and i17, token `etfs`). So E5-AC1 PASS and E5-AC2 PASS cannot both hold on these 18 names and this key.
  Recorded for 3.0.0_SA_CVO; this cell does not judge what it means.

A wrong mark is the outcome's evidence, not a defect to fix: no mark, name or key is changed here.

Surprise rows filed, one per failing criterion: `LGIC_NAMING-W5-S3` (E5-AC1) and `LGIC_NAMING-W5-S4` (E5-AC2), in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
