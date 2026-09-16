# LGIC_NAMING.TO-LN-l-2 -- cross-bucket reader, result

Worker: `0.9.0_WK_LGIC_NAMING~4`, branch `wk-lgic-naming-1-4`, cut at `6a5b276f8b`.
Cell: `LN-l-2`. Input read: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/N5_ADDRESSES.json`
only. No key file, schema, PRD, decomposition or template was opened.

Deliverable: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n5-reader.tsv` (7 lines, TAB-separated, LF).

## Answers and the reading behind each

The learned layout is `s3://<bucket>/{source}/{scope}/{tier}/{table}/{partition}/{object}`: 7 segments,
tier one of bronze/silver/gold/platinum/state/code, partition a `date=`, a named leaf, or an `entity=id`.

| id | answer | reading |
|---|---|---|
| a1 | bucket,source,scope,tier,table,partition,object | 7 segments in layout order; `gold` in the tier slot, `date=` partition |
| a2 | bucket,source,scope,tier,table,partition,object | 7 segments; `platinum` tier, `advisor_id=A123` is an entity=id partition |
| a3 | DOES-NOT-FIT | 6 segments. After `code` in the tier slot, the table slot holds a second tier word (`gold`), and there is no partition |
| a4 | bucket,source,scope,tier,table,partition,object | 7 segments; `cottonwood` scope, `platinum` tier, `date=` partition |
| a5 | bucket,source,scope,tier,table,partition,object | 7 segments; `global` scope, `gold` tier, `date=` partition |
| a6 | bucket,source,scope,tier,table,partition,object | 7 segments; `state` tier, `latest` is a named-leaf partition |
| a7 | DOES-NOT-FIT | 7 segments, but a tier word (`gold`) sits in the source slot and the source (`advi`) in the scope slot, so the order is not the layout's |

The bucket name differs from the learned `opal-data-assets` in all seven. That alone was not treated as
a misfit: the briefing gives the bucket its own role and the rest of the layout is a statement about
what follows it.

## Criterion

`L2-AC1`, invocation `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py l2-labeled`:

```
ADDRESSES: 7  LABELED: 7  MISSING: []
VERDICT: PASS-ALL-LABELED
rc=0
```

Denominator: 7 of 7 addresses carry an answer. This criterion grades presence of an answer only.
Whether each answer is right is scored by `LN-l-3` against `N5_KEY.json`, which this worker did not read.

Surprise rows filed: none.
