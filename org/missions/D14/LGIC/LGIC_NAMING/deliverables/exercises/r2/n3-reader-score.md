# LGIC_NAMING round 2 -- N3 reader scoring (LN-e-5, round 2)

Scorer: `0.9.0_WK_LGIC_NAMING~6`, task order `LGIC_NAMING.TO-LN-e-5-r2`, worktree `wk-lgic-naming-2-6c`, HEAD at
scoring `5fb93bb734`. This cell scores. It does not read or name, and no input was edited.

**Inputs (read-only):**
- namer A's names: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n3-namer-a.tsv` @eaafb46486
- the reader's marks: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n3-reader.tsv` @9096ea3c49
- the items: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa
- the key: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/N3_KEY_R2.json` @b9ea6f3686. It
  holds the firm or none, under RULING Q. `changed_from_round_1` gives i11 as etfs -> none and i14 as global -> none.
- the checker: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py` @b9ea6f3686

## E5R-AC1 -- `check_ln_r2.py e5-correct`

Invocation: `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-6c && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py e5-correct`

Output, verbatim (exit code 0):

```
WRONG: i09  name=mdpf-demo-publish-failure-alarm  marked=none  expected=demo
WRONG: i11  name=pathfinder-etfs-ingest-task  marked=pathfinder  expected=none
ITEMS: 18  CORRECT: 16  WRONG: 2 (key: N3_KEY_R2.json, firm or none)
VERDICT: FAIL-MISREAD
```

Expected `VERDICT: PASS-ALL-CORRECT`. **Printed `VERDICT: FAIL-MISREAD`: 16 of 18 correct.**

### Every WRONG line

| item | name (namer A) | the reader's mark | expected token (N3_KEY_R2.json) |
|---|---|---|---|
| i09 | `mdpf-demo-publish-failure-alarm` | `none` | `demo` |
| i11 | `pathfinder-etfs-ingest-task` | `pathfinder` | `none` |

## E5R-AC2 -- `check_ln_r2.py e5-consistent`

Invocation: `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-2-6c && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py e5-consistent`

Output, verbatim (exit code 0):

```
NAMES: 18  TOKENS MARKED AS A FIRM: 7  A MARKED TOKEN READ AS ANOTHER REFERENT ELSEWHERE: 0 []
VERDICT: PASS-ONE-REFERENT-EACH
```

Expected `VERDICT: PASS-ONE-REFERENT-EACH`. **Printed `VERDICT: PASS-ONE-REFERENT-EACH`: 0 clashes across 18 names.**
7 distinct tokens were marked as a firm. Under RULING R, a clash is a token that is marked as the firm in one name and
read as another referent in a different name that carries it. Two roles for one token do not count as a clash.

## All 18 marks against the key

| item | name (namer A) | mark | key | |
|---|---|---|---|---|
| i01 | `mdpf-cot-publish-lambda` | cot | cot | OK |
| i02 | `blackdiamond-49f-fetch-role` | 49f | 49f | OK |
| i03 | `orion-inf-ingest-daily` | inf | inf | OK |
| i04 | `schwab/49f/api-credentials` | 49f | 49f | OK |
| i05 | `opal-data-cottonwood` | cottonwood | cottonwood | OK |
| i06 | `eclipse/inflection/silver/account_holdings/date=2026-09-14` | inflection | inflection | OK |
| i07 | `mdpf-read-gold-policy` | none | none | OK |
| i08 | `etfs-price-refresh-dlq` | none | none | OK |
| i09 | `mdpf-demo-publish-failure-alarm` | none | demo | WRONG |
| i10 | `smartx-49f-platform-export-weekly` | 49f | 49f | OK |
| i11 | `pathfinder-etfs-ingest-task` | pathfinder | none | WRONG |
| i12 | `blackdiamond-cot-download-document` | cot | cot | OK |
| i13 | `mdpf/49financial/platinum/advisor_books/advisor_id=A123` | 49financial | 49financial | OK |
| i14 | `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | none | none | OK |
| i15 | `orion-inf-build-gold-profile` | inf | inf | OK |
| i16 | `mdpf-cot-export-sg` | cot | cot | OK |
| i17 | `etfs-pipeline-alerts` | none | none | OK |
| i18 | `mdpf-inf-delivery-status-table` | inf | inf | OK |

## State

E5R-AC1 is FAIL by output and E5R-AC2 is PASS by output. The task order says a wrong mark is the outcome's evidence,
not a defect to fix, so nothing in the reader's file, namer A's file or the key is changed here. The E5R-AC1 miss is
filed as row `LGIC_NAMING-W6-S4` in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
