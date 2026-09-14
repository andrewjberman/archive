# LGIC_NAMING N3 -- the two namings compared (cell LN-e-3)

Compared by `0.9.0_WK_LGIC_NAMING~5` on branch `wk-lgic-naming-1-5`, worktree HEAD `33131baf6f` at the start of the run.
This file compares the two namings. It does not name anything and does not pick a winner: a difference is evidence
for the outcome, not a defect to fix.

**Inputs read.** None was edited.
- `deliverables/exercises/n3-namer-a.tsv` @254a310135 (namer A, `0.9.0_WK_LGIC_NAMING~2`, LN-e-1)
- `deliverables/exercises/n3-namer-b.tsv` @beaefc6cf5 (namer B, `0.9.0_WK_LGIC_NAMING~3`, LN-e-2)
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa (18 items)

## E3-AC1 -- identical strings

Invocation: `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py e3-identical`

Output, verbatim (rc=0):

```
DIFFERS: i01  A=mdpf-cot-publisher-lambda  B=mdpf-cot-publish-lambda
DIFFERS: i02  A=blackdiamond-49f-session-fetch-role  B=blackdiamond-49f-fetch-role
DIFFERS: i04  A=schwab/49f/api-credentials  B=schwab/49f/api
DIFFERS: i07  A=mdpf-gold-read-policy  B=mdpf-read-gold-policy
DIFFERS: i09  A=mdpf-demo-publish-failure-alarm  B=mdpf-demo-publish-alarm
DIFFERS: i13  A=mdpf/49financial/platinum/advisor_books/advisor_id=A123  B=RAISE
DIFFERS: i14  A=mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz  B=mdpf/mdpf/code/gold/mdpf-accrual-bridge.tar.gz
DIFFERS: i15  A=orion-inf-gold-build-profile  B=orion-inf-build-gold-profile
DIFFERS: i16  A=mdpf-cot-exporter-sg  B=mdpf-cot-export-sg
ITEMS: 18  IDENTICAL: 9  DIFFERENT: 9
VERDICT: FAIL-DIFFERENT
```

Expected `VERDICT: PASS-IDENTICAL`, so the criterion is **FAIL** on 9 of 18 items identical.

## E3-AC2 -- the namers were blind to each other

Invocation: `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py e3-blind`

Output, verbatim (rc=0):

```
BASE A: 6a5b276f8b382edca90673d1f425320a251ca0e5 (holds B's file: False)  BASE B: 6a5b276f8b382edca90673d1f425320a251ca0e5 (holds A's file: False)
VERDICT: PASS-BLIND
```

Expected `VERDICT: PASS-BLIND`, so the criterion is **PASS**, 2 of 2 bases checked. Both namers recorded the same base commit,
and that commit holds neither answer file.

## Where the namers part -- every differing item (9 of 18)

**How the slot is found.** Each pair is split on its separator: `-` for the resource grammar, `/` for the secret and
key grammars. The strings are then walked from the left to the first token that differs, and that token is mapped to
the slot of the grammar that `org/standards/NAMING_SCHEMA.json` @33131baf6f gives for the item's type:
- resource: `{system}-{scope}-{function}[-{qualifier}]-{last}` (:51)
- secret: `{system}/{scope}/{purpose}` (:105)
- IAM policy: `{system}-{scope}-{purpose}-policy` (:107)
- key: `{source}/{scope}/{tier}/{table}/{partition}` (:26)

The token position is measured. The slot name is this worker's reading of the grammar, and it is marked wherever more
than one reading applies.

| item | type | namer A | namer B | first differing token | slot where they part |
|---|---|---|---|---|---|
| i01 | LAMBDA | `mdpf-cot-publisher-lambda` | `mdpf-cot-publish-lambda` | 3 of 4: `publisher` vs `publish` | function |
| i02 | IAM_ROLE | `blackdiamond-49f-session-fetch-role` | `blackdiamond-49f-fetch-role` | 3: A `session-fetch` (2 tokens) vs B `fetch` (1 token) | function |
| i04 | SECRET | `schwab/49f/api-credentials` | `schwab/49f/api` | 3 of 3: `api-credentials` vs `api` | purpose |
| i07 | IAM_POLICY | `mdpf-gold-read-policy` | `mdpf-read-gold-policy` | 2 of 4: `gold` vs `read` -- the same two tokens in opposite order | purpose. Neither string has a scope token (both read the policy as shared), so position 2 is the purpose slot |
| i09 | CW_ALARM | `mdpf-demo-publish-failure-alarm` | `mdpf-demo-publish-alarm` | 4: A adds `failure` after the shared `publish`, before the kind | function (A's own row LGIC_NAMING-W2-S1 records `publish-failure` as its function token) -- or the optional qualifier. The string alone does not say which |
| i13 | S3Key | `mdpf/49financial/platinum/advisor_books/advisor_id=A123` | `RAISE` | 1: B recorded no string | the whole string, as recorded. Row LGIC_NAMING-W3-S1 records B's unrecorded derivation as `mdpf/49financial/platinum/advisor_books/{advisor \| advisor_id}=A123`, which would part from A only at the partition's left-hand token |
| i14 | S3Key | `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | `mdpf/mdpf/code/gold/mdpf-accrual-bridge.tar.gz` | 2 of 5: `global` vs `mdpf` | scope |
| i15 | INSTANCE_PROFILE | `orion-inf-gold-build-profile` | `orion-inf-build-gold-profile` | 3 of 5: `gold` vs `build` -- the same two tokens in opposite order | function |
| i16 | SECURITY_GROUP | `mdpf-cot-exporter-sg` | `mdpf-cot-export-sg` | 3 of 4: `exporter` vs `export` | function |

**Count by slot (9 differing items):**
- function or purpose: 7 (i01, i02, i04, i07, i09, i15, i16). i09 is function or qualifier, as noted in the table.
- scope: 1 (i14)
- RAISE against a string: 1 (i13)

Seven of these nine were already anticipated by the namers' own rows: LGIC_NAMING-W2-S1 and W3-S2 on the open function
slot, W2-S2 and W3-S1 on i13's partition token, and W2-S3 and W3-S3 on i14's scope. The comparison only records that
those readings produced different strings.

**Identical (9 of 18):** i03 `orion-inf-ingest-daily`, i05 `opal-data-cottonwood`,
i06 `eclipse/inflection/silver/account_holdings/date=2026-09-14`, i08 `etfs-price-refresh-dlq`,
i10 `smartx-49f-platform-export-weekly`, i11 `pathfinder-etfs-ingest-task`, i12 `blackdiamond-cot-download-document`,
i17 `etfs-pipeline-alerts`, i18 `mdpf-inf-delivery-status-table`.
