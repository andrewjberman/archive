# LGIC_NAMING round 3 -- N3 reader score (cell LN-e-5)

Scored by `0.9.0_WK_LGIC_NAMING~6` on `LGIC_NAMING.TO-LN-e-5-r3`, branch `wk-lgic-naming-3-6e5`, worktree HEAD
at scoring `d47aac6c8b`. This cell scores. It does not read or name, and no mark, name or key was changed.

**Inputs (read-only):**
- namer A's names: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/n3-namer-a.tsv` @4dffe3105b
- reader's marks: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/n3-reader.tsv` @b6a992b84d
- items: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa
- key (round 2's, unchanged in round 3): `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/N3_KEY_R2.json` @b9ea6f3686
- checker: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_ln_r3.py` @60350c4a04

## E5T-AC1 -- the reader marked the expected firm, or none, on every item

Invocation: `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-3-6e5 && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_ln_r3.py e5-correct`

Checker output, verbatim (exit code 0):

```
ITEMS: 18  CORRECT: 18  WRONG: 0 (key: r2/N3_KEY_R2.json, unchanged, firm or none)
VERDICT: PASS-ALL-CORRECT
```

**WRONG lines: none.** The checker printed no `WRONG:` line. 0 of 18 items are wrong.

## E5T-AC2 -- no token the reader marked as a firm is read as another referent in another name

Invocation: `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-3-6e5 && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_ln_r3.py e5-consistent`

Checker output, verbatim (exit code 0):

```
NAMES: 18  TOKENS MARKED AS A FIRM: 7  A MARKED TOKEN READ AS ANOTHER REFERENT ELSEWHERE: 0 []
VERDICT: PASS-ONE-REFERENT-EACH
```

The checker counts only one token read as two referents (RULING R), never two roles. The 7 tokens marked as a firm:
`49f`, `49financial`, `cot`, `cottonwood`, `demo`, `inf`, `inflection`.

## The 18 marks against the key

This table is a transcription of the four input files above, for the reader of this record. The checker output
above is the verdict.

| item | name (namer A) | reader's mark | key |
|---|---|---|---|
| i01 | `mdpf-cot-publish-lambda` | cot | cot |
| i02 | `blackdiamond-49f-fetch-role` | 49f | 49f |
| i03 | `orion-inf-ingest-daily` | inf | inf |
| i04 | `schwab/49f/api-credentials` | 49f | 49f |
| i05 | `opal-data-cottonwood` | cottonwood | cottonwood |
| i06 | `eclipse/inflection/silver/account_holdings/date=2026-09-14` | inflection | inflection |
| i07 | `mdpf-read-gold-policy` | none | none |
| i08 | `etfs-price-refresh-dlq` | none | none |
| i09 | `mdpf-demo-publish-failure-alarm` | demo | demo |
| i10 | `smartx-49f-platform-export-weekly` | 49f | 49f |
| i11 | `pathfinder-etfs-ingest-task` | none | none |
| i12 | `blackdiamond-cot-download-document` | cot | cot |
| i13 | `mdpf/49financial/platinum/advisor_books/advisor_id=A123` | 49financial | 49financial |
| i14 | `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | none | none |
| i15 | `orion-inf-build-gold-profile` | inf | inf |
| i16 | `mdpf-cot-export-sg` | cot | cot |
| i17 | `etfs-pipeline-alerts` | none | none |
| i18 | `mdpf-inf-delivery-status-table` | inf | inf |

Round 2 had two misses, i09 and i11 (row `LGIC_NAMING-W6-S4`). In round 3 i09 is marked `demo` and i11 is marked
`none`, and both match the key.
