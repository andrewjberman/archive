# N6 -- the two gradings compared (LN-h-3)

**Worker:** `0.9.0_WK_LGIC_NAMING~5` | **TO:** `LGIC_NAMING.TO-LN-h-3` | **Branch:** `wk-lgic-naming-1-5`, worktree HEAD at start `c17d7d09c9`
**Cell:** `LN-h-3` (PRD candidate N6). This cell compares the two gradings. It does not grade.

**Inputs read.** None was edited.
- `deliverables/exercises/n6-grader-a.tsv` @388b07f486 (by `0.9.0_WK_LGIC_NAMING~7`)
- `deliverables/exercises/n6-grader-b.tsv` @40f445d92c (by `0.9.0_WK_LGIC_NAMING~8`)
- `deliverables/GRADING_RULE.md` @51b0952d71. Line numbers below are at this commit.
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N6_SAMPLE.json` @777770e6aa
- Read beyond the order's list, to find the raising step: `deliverables/0.9.0_WK_LGIC_NAMING~8/grader-b.result.md` and
  `deliverables/0.9.0_WK_LGIC_NAMING~7/grader-a.result.md`, both @c17d7d09c9. See row `LGIC_NAMING-W5-S5`.

## 1. The checker's output, verbatim

Each command ran from `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-naming-1-5` under `timeout 120`.

**H3-AC1** -- `python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py h3-agree`
```
DISCRIMINATING NAMES: 85  AGREE ON VERDICT AND CANONICAL FORM: 85  DISAGREE: 0
VERDICT: PASS-AGREE
rc=0
```

**H3-AC2** -- `python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py h3-disjoint`
```
DISCRIMINATING SAMPLE: 84  WORKED CASES IN IT: 0 []
VERDICT: PASS-DISJOINT
rc=0
```

**H3-AC3** -- `python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_ln.py h3-blind`
```
BASE A: 3d671ff59cfba948d00af61d2d7145ea254f63b7 (holds B's file: False)  BASE B: 3d671ff59cfba948d00af61d2d7145ea254f63b7 (holds A's file: False)
VERDICT: PASS-BLIND
rc=0
```

**Why AC1 prints 85 and AC2 prints 84.** `h3_agree` (`check_ln.py:450-463` @777770e6aa) counts the 85
discriminating `(type, name)` entries. `h3_disjoint` calls `g1_disjoint` (`check_ln.py:176-181`), which counts a
**set of names**. The name `opalinvest-portal` appears twice in the sample, once as S3_BUCKET (position 37 of 37) and
once as S3_BUCKET_POLICY (position 15 of 15), so the set holds 84 names. Both verdicts stand on their own denominators.

## 2. What was compared

| measure | grader A | grader B |
|---|---|---|
| rows (85 discriminating + 3 overlap) | 88 | 88 |
| rows whose `(type, name)` keys equal the sample's 88 | yes | yes |
| CONFORMANT / ALIAS / OUT-OF-PATTERN / RAISE / NOT-GRADED | 13 / 1 / 37 / 18 / 19 | 13 / 1 / 37 / 18 / 19 |
| recorded base | `3d671ff59c` | `3d671ff59c` |
| sha256 of the answer file | `41c3de9d...ffde945` | `41c3de9d...ffde945` |

The two answer files are byte-identical (`cmp` rc=0). The checker compares only the 85 discriminating names. I also
compared the 3 overlap names with a separate count (`.scratch/h3_tally.py`, run once, not committed): they agree too.
**0 of 88 rows disagree.**

## 3. Every disagreement

None. H3-AC1 prints `DISAGREE: 0` over 85 discriminating names, and the separate count over all 88 prints 0. No
disagreement row is filed.

## 4. Every RAISE, with the line of GRADING_RULE.md it exposes

Each grader gives RAISE to the same 18 names: 17 discriminating and 1 overlap. The rule says a RAISE "is a defect in this
rule, the data file or the registry, and the output names the step that raised" (`GRADING_RULE.md:26-27`). Neither answer
TSV has a column for that step, and the fourth field is empty on all 18 RAISE rows in both files.

The **step** column is taken from grader B's own table (`grader-b.result.md:25-35`). Grader A recorded no step (row
`LGIC_NAMING-W5-S5`). The **line** column is where that step stands in `GRADING_RULE.md` @51b0952d71. The
**registry gap** column names the section-8 row the rule itself files for that step, where it files one.

| # | set | type | name | step (grader B) | GRADING_RULE.md line it exposes | registry gap the rule names |
|---|---|---|---|---|---|---|
| 1 | disc | CODEBUILD_PROJECT | `estate-report-seam-freshness-publisher` | R1.c, t1 `estate` in V2 | `:143` R1.c "If t1 is in V2, RAISE"; `:100` V2 lists `estate` | W1-S2 (`:315`) |
| 2 | disc | CODEBUILD_PROJECT | `semantic-clustering-lambda-build` | R1.c, t1 `semantic` in V2 | `:143`; `:100` V2 lists `semantic` | W1-S2 |
| 3 | disc | EC2_INSTANCE | `estate-report-runner` | R1.c, t1 `estate` in V2 | `:143`; `:100` | W1-S2 |
| 4 | disc | ECS_TASK_DEFINITION | `globgrph-comp-learns-producer` | R1.c, t1 `globgrph` in V2 | `:143`; `:100` V2 lists `globgrph` | W1-S2 |
| 5 | disc | ECS_TASK_DEFINITION | `globgrph-nessie` | R1.c, t1 `globgrph` in V2 | `:143`; `:100` | W1-S2 |
| 6 | disc | ECS_TASK_DEFINITION | `globgrph-trino` | R1.c, t1 `globgrph` in V2 | `:143`; `:100` | W1-S2 |
| 7 | disc | EVENT_RULE | `FIRMSEP-s3-direct-access-bypass` | R1.c, after N2 gives `firmsep` | `:68-70` N2 (its own example `FIRMSEP-auth` -> `firmsep`); `:143`; `:100` V2 lists `firmsep` | W1-S2 |
| 8 | overlap | ECS_CLUSTER | `opal-globgrph` | R2, t2 `globgrph` in V2 | `:157` R2 "If t2 is in V2, RAISE"; `:100` | W1-S2; the same name is worked case `:351` with the same RAISE |
| 9 | disc | LOG_GROUP | `/aws/codebuild/estate-report-seam-freshness-publisher` | L3 -> R1.c (the rest raises) | `:226-227` L3 grades the rest by section R; `:143`; `:100` | W1-S2 |
| 10 | disc | LOG_GROUP | `/aws/lambda/opal-globgrph-freeze-monitor` | L3 -> R2 (the rest raises) | `:226-227`; `:157`; `:100` | W1-S2 |
| 11 | disc | DYNAMODB_TABLE | `user-permissions` | R1.f, t1 `user` in no vocabulary | `:150` R1.f "Any other t1 is in no vocabulary. RAISE: a token no registry row resolves" | none named in section 8 |
| 12 | disc | IAM_POLICY | `yield-curve-artifact-write` | R1.f, t1 `yield` in no vocabulary | `:150` (reached through R8, `:188`) | none named in section 8 |
| 13 | disc | LAMBDA | `access-anomaly-scanner` | R1.f, t1 `access` in no vocabulary | `:150` | none named in section 8 |
| 14 | disc | SQS_QUEUE | `partner-etl-ops-queue` | R1.f, t1 `partner` in no vocabulary | `:150` | none named in section 8 |
| 15 | disc | IAM_POLICY | `AWSDataLifecycleManagerServiceRole` | G2.2, `AWS` prefix | `:55` G2.2 | W1-S4 (`:317`) |
| 16 | disc | LOG_GROUP | `aws-waf-logs-opal-gateway` | G2.3, no leading `/` | `:56-57` G2.3 (its own example `aws-waf-logs-*`) | W1-S4 |
| 17 | disc | S3Key | `%s/date=%s/data.parquet` | K1, segment 1 is a variable segment | `:258-259` K1 "Anything else RAISES ... That covers ... a variable segment" | none named in section 8 |
| 18 | disc | S3Key | `warehouse/_branch_head.main.json` | K1, segment 1 `warehouse` is neither a source nor a tier | `:258` K1 | none named in section 8 |

**By rule line** (18 names): R1.c `:143` with V2 `:100`, 7 names (#1-7), and 1 more reached through L3 (#9); R2
`:157` with V2 `:100`, 1 name (#8), and 1 more through L3 (#10); R1.f `:150`, 4 names (#11-14); G2.2 `:55`, 1 name
(#15); G2.3 `:56-57`, 1 name (#16); K1 `:258-259`, 2 names (#17-18). That is 8 + 2 + 4 + 1 + 1 + 2 = 18.

## 5. Stated for L9, not decided here

- Both graders say in their result files that they had to choose a reading on `SECRET opal/bd/credentials`
  (`GRADING_RULE.md:204` S3 names only V4 tokens as a scope, and `:123` puts `bd` outside the V4 table) and on
  `SSM_DOCUMENT opal-cot-bd-session-fetch` (`:156-163` R2 and R3). They chose the same reading on each, and the verdict and
  canonical form agree, so neither is a disagreement.
- The answer files are byte-identical, and so are their row order and base commit. H3-AC3 shows that neither base
  carries the other's file. Whether identical output from two blind graders says more than that is not this cell's
  question.

3.0.0_SA_CVO grades H3-J1 at L9: is every disagreement and every RAISE traced to the rule line it exposes? This record
gives no verdict on it.
