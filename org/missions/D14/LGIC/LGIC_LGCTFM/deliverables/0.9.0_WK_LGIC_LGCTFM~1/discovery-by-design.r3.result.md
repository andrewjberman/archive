# LGIC_LGCTFM.TO-LT-e-5-r3 -- RESULT (0.9.0_WK_LGIC_LGCTFM~1)

**Branch:** `wk-lgic-lgctfm-3-1` (linked worktree). **Commits, all LOCAL:** `b736ee4fdf` (build),
`75df676669` (three channel rows), `40d7729b47` (vintage correction), plus the commit that carries this
file and the proof instance. **Order status: still `pending`** -- E5R3-AC4 reads FAIL, and a FAIL row
leaves the order open.

## Verdicts

| criterion | verdict | deciding line |
|---|---|---|
| E5R3-AC1 | PASS-by-output | `VERDICT: PASS-E5-COVERAGE-SHAPE` (19 node_types, 4 legs, arithmetic closes) |
| E5R3-AC2 | PASS-by-output | `floor 88 = rowed 79 + excluded 9 + unaccounted 0` / `VERDICT: PASS-E5-FLOOR` |
| E5R3-AC3 | PASS-by-output | 7 NAMED classes, 38 of 38 floor nodes rowed / `VERDICT: PASS-E5-NAMED-ROWED` |
| E5R3-AC4 | **FAIL** | `VERDICT: FAIL-E5-SCHEMA` -- receiving-check cannot CLASSIFY the mandated path |
| E5R3-AC5 | RECORDED (judgment) | graded at L9 by `3.0.0_SA_CVO`; no verdict here |

The checker's own controls were run FIRST: `selftest-arms` -> `PASS-ARMS-DISCRIMINATE`, 27 arms.

## What was built

`lib/opal_lgctfm.py` `discover_involved()`. A live AWS node is INVOLVED when one of four legs reaches it,
minus one exclusion. The definition is written verbatim into `contract.json` `coverage.instrument` and
into `infra/logic/10_LEGACY_TRANSFORM.md` s."Discovery by design".

- **token** -- `comp-find --corpus aws '\b(?:49f|49financial)\b' -i --all` (the floor) plus a pull over
  the seed buckets, plus a live EventPattern naming an identifier. The vendor alias `bd` is refused:
  it names the blackdiamond VENDOR, shared with cottonwood and inflection.
- **iam_grant** -- `comp-iam role ""` (all 210 Terraform roles in one call); a role with an ALLOW whose
  Resources name an identifier, every compute node that ASSUMES it (an EC2 through its profile), and
  every involved compute node's own execution role (that reverse step never fans out again).
- **source_text** -- `lambda-source-map.json` packaged files, identifier in a whitespace-free CODE string
  literal only.
- **trigger_target** -- `comp-kuzu` TRIGGERS/EMITS_TO (the only reader of schedule targets and S3
  notifications) plus `comp-trigger 'arn:' --json` for live rule targets; fixpoint.

**Excluded:** the 9 `/aws/lambda/...` LOG_GROUPs, each with its own reason naming its function.

## The run (`deliverables/0.9.0_WK_LGIC_LGCTFM~1/e5_walk/`)

Floor 88 hits of 2591 aws nodes scanned, vintage `Built from the estate as of 2026-09-18 20:13:24 UTC`.
**381 involved, 381 rowed, 9 excluded, 0 not_covered**, 383 contract rows with the two standing plants.
Per-leg: token only 210, iam_grant only 92, trigger_target only 33, source_text only 7, 39 on two or
three legs. 58 of the 67 involved Lambdas carry no token. At the cut the same classes read LAMBDA 0 of 9,
EC2_INSTANCE 0 of 1, DYNAMODB_TABLE 0 of 1, SCHEDULE 1 of 4, IAM_ROLE 1 of 13 (a plant).

## The blocking finding

`E5R3-AC4` demands `ACCEPT lgctfm-contract` from `.tools/receiving-check.py` on R3_BASE.json's
`e5_walk_output`. receiving-check picks a checker BY PATH; its lgctfm-contract route (`:77`) matches
`workflows/legacy_transform/<subject>/<run>/contract.json` or `*.lgctfm-contract.json`. The mandated
deliverables path matches neither, so receiving-check prints `UNCHECKED  unrecognised` and the arm prints
FAIL. The same bytes read `ACCEPT lgctfm-contract` under `.tools/lgctfm-contract-check.py`, the checker
that route dispatches to, and the frozen 1.0 run still reads ACCEPT through receiving-check after the
schema change. Not worked around: no rename, no copy under `workflows/`, no fixed input edited.
Row `LGIC_LGCTFM-W1-S23`, BLOCKING, ARMED, `disarm_owner: 2.0.0_SA_COO~G`.

Two further rows: `W1-S24` (`comp-trigger --list --json` carries no targets, contrary to the order's
premise) and `W1-S25` (the commit gate's MANIFEST-ADVISORY flags Cypher handed TO comp-kuzu as raw).

## Proof

`LGIC_LGCTFM.TO-LT-e-5-r3.discovery-by-design.proof_of_spec.json` --
`python .tools/proof-of-spec-check.py <instance> E5R3-AC1,E5R3-AC2,E5R3-AC3,E5R3-AC4,E5R3-AC5
--governing-order <order>` -> **VALID (rc=0)**. A VALID instance is not a met order: AC4 is FAIL and the
order stays open.
