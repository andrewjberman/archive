# EN-h-1 (round 19) -- the HAND side of FWD-5 clause 3, re-measured across all three surfaces

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1`. **Task order:** `LGIC_ENFORCE.TO-EN-h-1-r19`.
**Branch:** `wk-lgic-enforce-19-1`, base `3ed034c144`.
**Record:** `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/HAND_REMEASURE_R19.json`.
**Builder:** `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/build_hand_remeasure_r19.py`.

## THE RESULT

| surface | compared | agree | disagree | round 9 was |
|---|---|---|---|---|
| `grading_rule_worked_cases` | 45 | 45 | 0 | 45 / 43 / 2 |
| `n6_grader_rows` | 88 | 86 | 2 | 88 / 61 / 27 |
| `tension_ranking_surfaces` | 10 | 9 | 1 | 10 / 5 / 5 |
| **TOTALS** | **143** | **140** | **3** | 143 / 109 / 34 |

Thirty-one of round 9's thirty-four disagreements close when the hand side is re-measured
at the census vintage. **Three survive, and all three are cases a hand-side re-measure is
structurally incapable of closing.** They are named in full below.

## THE DENOMINATORS, RE-DERIVED AT THIS CELL'S WRITE TIME

Not inherited. Each was re-read from its ORIGINAL carrier by the instrument round 9 named:

| surface | value | instrument |
|---|---|---|
| `grading_rule_worked_cases` | **45** | `len(worked_cases)` of the ONE json fence between `## 9. WORKED CASES` and `## 10.` in `GRADING_RULE.md` |
| `n6_grader_rows` | **88** | non-empty lines of `n6-grader-a.tsv` after the `# base` header, split on TAB (89 non-empty = 1 header + 88 rows) |
| `tension_ranking_surfaces` | **10** | count of `{"rank": N` rows in the json fence of `TENSION_RANKING.md` |

**45, not 43.** The figure was re-derived here rather than taken from either carrier at HEAD
that still says 43 (this project's `project.json` round-9 text and
`LGIC_ENFORCE_ROUND8_ANALYSIS.md:151`). The re-read confirms the two names the v1.9 re-cut
`@fd6ce8c330` added are present: `mdpf-lambda-lambda` and `orion-orion-lambda-lambda`.

## THE VINTAGE -- BOTH SIDES AT THE SAME ONE

Every revised hand figure was measured at the vintage the MACHINE side already used:
`NAMING_CENSUS_REPORT.r8.md` @`54659987c0`, *"the estate as of 2026-09-18 12:17:28 UTC"*.
Each of the three `revisions[]` entries in the record states that vintage and its commit.
A hand figure re-measured against a different vintage from the machine figure it is compared
with would re-create this defect one layer down.

## WHAT "RE-MEASURING THE HAND SIDE" MEANT, MECHANICALLY

The hand products are not a list of opinions; they are a WRITTEN RULE applied against a
registry. `GRADING_RULE.md` R1 reads the V1/V2/V3 verdicts from REGISTRY rows
(`DATA.rows_owner`), and the hand applied that rule against a 2026-09-13/14 registry. So the
re-measure **re-applies the hand's own rule against the registry at the census vintage**, and
the deciding fact is READ, per case, out of the census-vintage bytes:

- `infra/logic/registry/systems.json` @`54659987c0` -- the token's vocabulary class
- `infra/logic/registry/resources.json` @`54659987c0` -- the resource-to-system row that fills `{system}` (R1.d)
- `org/standards/NAMING_SCHEMA.json` @`54659987c0` -- `aws_fixed`, which puts a name outside the grade's domain

**The machine side was never re-graded.** `grade_at_census` is read from round 9's record
byte-for-byte; the builder contains no call to `grade()`. Re-running `grade()` so it agrees
with a stale hand side is the refused reading, and so is its mirror -- copying `grade()`'s
output into the hand column, which would be the same defect wearing the other hat. **A case
whose deciding fact could not be verified in the census-vintage bytes is NOT resolved**; it
keeps its disagreement and says so. That branch fired zero times, which is a measured result
and not an assumption:

| basis | cases | of 133 per-name cases |
|---|---|---|
| `UNCHANGED-AGREEING` | 104 | agreed at round 9; the re-measure does not move them |
| `REVISED-TOKEN-CLASS` | 22 | the deciding token's vocabulary row verified in `systems.json` at the census vintage |
| `REVISED-REGISTRY-ROW` | 4 | a `(name, type) -> system` row verified in `resources.json`, filling `{system}` per R1.d |
| `REVISED-AWS-FIXED` | 1 | `aws_fixed.by_name.LOG_GROUP` carries `prefix: aws-waf-logs-`, so the name is outside the grade's domain |
| `UNREVISED-MACHINE-SIDE` | 2 | round 9 found the machine side departing from the written rule |
| `UNREVISED-UNVERIFIED` | **0** | -- |

For `tension_ranking_surfaces` the hand's own instrument is *"quote the naming census"* -- the
file states **"Nothing was measured again for this file"** and quotes `09_NAMING_CENSUS.md` of
2026-09-13. Re-measuring that hand side means RE-RUNNING THAT INSTRUMENT at the r8 census
vintage: 32 of its 38 figures were re-quoted, 6 were not (rank 5, below).

## THE POSITIVE CONTROL

Before any revised figure was believed, the comparator was run over the **UNREVISED** hand
side and had to reproduce round 9's triple exactly. It did:

```
CONTROL (hand side unrevised, must reproduce round 9): {"compared": 143, "agree": 109, "disagree": 34}
CONTROL round 9 as recorded:                           {"compared": 143, "agree": 109, "disagree": 34}
OK: comparator reproduces round 9 exactly -- 143/109/34.
```

The builder refuses to write if that control fails. A comparator that cannot reproduce the
number it is replacing has not been shown to measure anything, and its new number would be
unexplained. Re-runnable as
`python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/build_hand_remeasure_r19.py --control`.

## THE THREE DISAGREEMENTS THAT SURVIVE

### 1. `n6_grader_rows` -- `CW_ALARM::ExecIncrParityFailure`

- hand, re-measured: `OUT-OF-PATTERN`, `{system}-exec-incr-parity-failure-alarm`
- `grade()` at the census vintage (untouched): `OUT-OF-PATTERN`, `{system}-exec-incrparity-failure-alarm`

The verdicts agree; the canonical forms differ. Round 9 found **the MACHINE side departs from
the written rule and the hand follows it**: `GRADING_RULE.md` N2 (line 106) splits before each
capital and states no re-join, while `grade()`'s token step re-joins the pieces of one original
segment. A hand-side re-measure cannot close a machine-side departure, and re-grading the
machine side is refused on this cell. **Survives, correctly, and it is not the hand's defect.**

### 2. `n6_grader_rows` -- `SSM_DOCUMENT::opal-cot-bd-session-fetch`

- hand, re-measured: `OUT-OF-PATTERN`, `opal-cot-blackdiamond-session-fetch-document`
- `grade()` at the census vintage (untouched): `OUT-OF-PATTERN`, `opal-cot-bd-session-fetch-document`

Again verdicts agree, forms differ. Round 9: **`grade()` is WRONG against the written rule and
the hand is right** -- `GRADING_RULE.md` R3 (line 204) says `bd` next to a V4 firm token is the
vendor and *"Either way it is an alias, and the canonical form spells blackdiamond"*, so
`grade()`'s canonical form carries a refused token. Same class as (1). **Survives, correctly.**

### 3. `tension_ranking_surfaces` -- rank 5, *"339 LIVE-no-DECLARED nodes"*

All six of its figures stay outside tolerance, and **this row was deliberately NOT re-quoted**:

| figure | hand | census r8 | within |
|---|---|---|---|
| live names with no same (name,type) on the repo plane | 339 | 669 | no |
| LAMBDA | 15 | 158 | no |
| IAM_ROLE | 16 | 56 | no |
| EVENT_RULE | 10 | 26 | no |
| LOG_GROUP | 68 | 199 | no |
| IAM_POLICY | 36 | 93 | no |

The two sides come from **different INSTRUMENTS**, not different vintages: the hand figure is
`comp-find`'s `drift_class` `LIVE-no-DECLARED` over the live graph, and the census carries no
drift class at all, so the only census-side reading is live `(name,type)` minus repo
`(name,type)` -- and the repo plane reads only literal Terraform name attributes and source
literals, which inflates the difference. Round 9's own words: *"NEITHER SIDE IS SHOWN WRONG."*
**Re-quoting the census here would have manufactured an agreement by overwriting the hand's
figure with the very number it is being compared against.** That is the one move on this
surface that would have closed the comparison while measuring nothing, so the row is left
unrevised and the disagreement stands. Closing it needs a drift-class instrument on the census
side, which is not this cell's work and is not this round's.

## WHERE ROUND 9'S 34 WENT

Round 9's base states the split: **30 of 34 name the hand side as defective (28 HAND SIDE
STALE, 2 hand weaker/wrong)**, leaving 4 that do not. Measured here against that partition:

- **28 HAND SIDE STALE** -> all 28 close (2 in `grading_rule`, 25 in `n6`, rank 7 in `tension`).
- **2 hand weaker/wrong** -> both close (`tension` ranks 1 and 4).
- **of the remaining 4:** rank 8 closes -- the hand figure was *not wrong at its own date*
  (29 s3-* policies), but the comparison requires both sides at ONE vintage and at the census
  vintage the figure is 33. The other **3 survive** and are the three above.

31 closed + 3 surviving = 34. The arithmetic closes against round 9's own partition, not
against a forward list of what this cell happened to fix.

## THE ADDITIVE SIBLINGS -- AND THE ORIGINALS

Three siblings written, none of them replacing anything:

| surface | sibling | shape |
|---|---|---|
| `grading_rule_worked_cases` | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.REMEASURED_R19.md` | one json fence, 45 worked cases |
| `n6_grader_rows` | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.REMEASURED_R19.tsv` | the original's 4-column TSV, `# base` header + 88 rows |
| `tension_ranking_surfaces` | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.REMEASURED_R19.md` | one json fence, 10 ranked rows |

Each carries, per case, BOTH the round-9 hand value and the re-measured one, plus the `basis`
and the evidence line that decided it -- so the difference the 28 "HAND SIDE STALE" findings
are made of is preserved rather than erased.

**The three originals did not move.** Measured at this cell's own base and at HEAD:

```
GRADING_RULE.md      base=5c98cb76e9ff head=5c98cb76e9ff same=YES
TENSION_RANKING.md   base=e69181e5b436 head=e69181e5b436 same=YES
n6-grader-a.tsv      base=91566d3d7a41 head=91566d3d7a41 same=YES
```

## TWO THINGS WORTH THE NEXT READER'S TIME

**The `n6` key had to be `TYPE::NAME`, not `NAME`.** The 88 rows carry only **87 distinct
names** -- `opalinvest-portal` appears twice, once as `S3_BUCKET` and once as
`S3_BUCKET_POLICY`. A record keyed on the bare name would have presented 87 distinct
`compared_keys` against a denominator of 88 and failed set equality, and the arithmetic would
still have looked closed. Measured, not assumed.

**Rank 5 is the surface where this cell could most cheaply have reported a fully closed
comparison.** Re-quoting its six figures from the census would have produced 143/143/0 with
every printed number traceable to a real file. The reason it is 143/140/3 instead is that
re-quoting a figure whose instrument the census cannot reproduce is not a measurement.

## CRITERIA

- `H1R19-AC1` `PASS-H1-COVERAGE` -- all three surfaces, each with its own write-time denominator, compared_keys equal to round 9's by set equality.
- `H1R19-AC2` `PASS-H1-VINTAGE` -- every revision names its carrier, sibling and census vintage; all three originals byte-identical at this cell's base and at HEAD.
- `H1R19-AC3` `PASS-H1-REDERIVED` -- totals close (143 = 140 + 3) and every surface's triple moved off round 9's.
- `H1R19-AC4` -- JUDGMENT, `3.0.0_SA_CVO`'s at L9. **No verdict from this cell.** Whether each
  hand-side revision is right at the bytes across all three surfaces is not something the
  mechanical arms measure, and this worker does not grade it.
