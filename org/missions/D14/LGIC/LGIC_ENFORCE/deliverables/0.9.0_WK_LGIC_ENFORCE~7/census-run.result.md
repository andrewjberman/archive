# census-run.result -- LGIC_ENFORCE.TO-EN-s-1 (EN-s-1), 0.9.0_WK_LGIC_ENFORCE~7

Branch `wk-lgic-enforce-1-7-s1`, base CLOUD @`32855486f0`. The module, the report and the rows were committed at
`f64b6f35cb` (LOCAL). **The order stays OPEN: S1-AC1 and S1-AC2 FAIL by output.**

## What landed

- `lib/opal_naming.py`: census mode, as new functions plus the CLI verb
  `census [--names FILE] [--live] [--repo] [--report PATH] [--budget N]`. With no plane flag it reads both planes. It
  exits 0 when every item is judged, 3 on the first RAISE (printing `CENSUS RAISE <plane> <type> [<where>] <string> --
  <step message>`), and 2 when a plane cannot be read.
  - live: `comp-find --corpus aws --name .` over the 33 node types of NAMING_SCHEMA.json, `--all`. The pull must say
    WITHIN BUDGET with 0 deferred, and the parsed node count must equal its DENOMINATOR, or there is no measurement.
    The NOT GRADED types, and the names the schema's aws_fixed puts outside the domain, are counted and not judged.
  - repo: the name attribute of each Terraform resource of 28 graded types when it is one literal. In every config.py,
    and in the Lambda sources under `infra/aws/lambda/`, each string literal `_census_classify` places as a name.
    Vendored and test files are excluded.
- `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md`: the run's report, **STOPPED on the first
  RAISE**.
- Rows LGIC_ENFORCE-W7-S1 (BLOCKING), -W7-S2 and -W7-S3 (OBSERVATION), all INERT.

## The run

- Vintage `Built from the estate as of 2026-09-15 00:57:50 UTC. Stitch source: stitch-codebuild built
  2026-09-14T03:01:18Z. manifest: e8a06d444ae8`; registry@50e4fabd1cb6a150.
- live 2148 nodes, minus 327 of NOT GRADED types, minus 16 aws_fixed names, gives live_nameable 1805.
  repo: 1869 names.
- The run stopped on the 4th live name: `live API_GW sentiment-query-api -- R1.f: 'sentiment' is in no vocabulary; no
  registry row resolves it`. Before the stop it judged 3 names: 2 CONFORMANT and 1 OUT-OF-PATTERN.
- A diagnostic sized the RAISE population. It is not the census: it is a scratch script outside the worktree that keeps
  going past a RAISE. Live: 504 of 1805 raise, across 115 distinct tokens (globgrph 67, news 46, find 34, trade 24,
  estate 24, astn 19, ...). Repo: 623 of 1869 raise. So on this registry the census cannot judge every nameable live
  name. That is row W7-S1.

## Criteria (each run twice on the final bytes, identical)

| id | verdict | deciding line |
|---|---|---|
| S1-AC1 | FAIL | `PLANES: ['live']` ... `VERDICT: FAIL-PLANES` (rc 1) |
| S1-AC2 | FAIL | `LIVE NAMEABLE: 1805  JUDGED: 3  LIVE ROWS: 3` / `VERDICT: FAIL-NOT-ALL-JUDGED` (rc 1) |
| S1-AC3 | PASS | `ROWS: 3  MALFORMED: 0` / `VERDICT: PASS-ROW-SHAPE` (rc 0) |
| S1-AC4 | PASS | `CENSUS RAISE names LAMBDA ... zzqx-inf-foo-lambda ...` / `VERDICT: PASS-RAISE-STOPS` (rc 0) |

## Controls

- The stop is caused by the RAISE, not a constant exit code. The same CLI on three placeable names (CONFORMANT, ALIAS
  and NOT-GRADED) printed `CENSUS: COMPLETE 3 judged`, rc 0.
- Determinism: the four criteria ran twice and cmp read them IDENTICAL, 17 lines each. Three live pulls read the same
  2148 nodes at the same vintage.

## Not claimed

- No comparison against the hand gradings (that is EN-s-2's).
- No verdict on the repo plane: the run never reached it.
- No registry change: `infra/logic/registry/` is outside this order's `<paths>`.
- The repo placement rule is this worker's own (row W7-S3), not a ratified one.
