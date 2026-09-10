# NFRA_REPORT -- SECTION_MAPPING (cell RP-s-22, round 4, `0.9.0_WK_NFRA_REPORT~2`)

**What this is:** the 13-way partition of `lambda_handler`'s `report["sections"]` keys
(`infra/aws/lambda/infrastructure_monitor/lambda_function.py:185-293` at HEAD,
`@2b45cd42273c8bd73f7493f5bb859894e714ccf9`), as implemented by
`infra/aws/lambda/infrastructure_monitor/edition_rows.py`'s `rows_from_report()`. Every
section lands in exactly one of three buckets; the denominator is 13 and it is counted
below rather than asserted.

## THE DENOMINATOR

```
MAPPED                 : 10 of 13 (always) + ai_analysis conditionally (see CONDITIONAL below)
OMITTED-WITH-REASON    :  2 of 13 (always)
CONDITIONAL-BY-DESIGN  :  1 of 13 (ai_analysis -- realized as either a MAPPED row or an
                          OMITTED-WITH-REASON omission each run, never neither)
-----------------------------------------------------------------------------------------
TOTAL                  : 13 of 13
```

Measured this run (worktree `C:/tmp/wk-report-4-2`, the AC2/AC3 fixture from the task
order's own `<proof_of_spec>`, `ai_analysis` forced `None`): `SECTIONS=13 COVERED=13
MISSING=[] ROWS=10 OMISSIONS=3` (10 MAPPED rows + 2 always-omitted + 1 conditional-omitted
== 3 omissions this run, since `ai_analysis` was `None`).

## BUCKET 1 -- MAPPED (10 of 13, always; 11 of 13 when ai_analysis fires)

Each becomes exactly one row in the specimen's `ROW_FACTS` shape (`property`,
`attribution`, `family="axis"`, `prev`, `curr`, `citation`, `evidence`), plus an additive
`section` key naming which of the 13 collector keys produced it. `curr.axis1` is always
`CHECKED` (the section ran -- it is present in `report["sections"]`). `curr.axis2` is one
of `OK` / `DEGRADED` / `BREACH` / `UNASSERTED`, read from the section's own REAL field
name (never a generic literal), defaulting to `UNASSERTED` -- never `OK` -- when that
field is absent (`ROW_STRUCTURE.md`'s own "not defaulted to OK" rule, already used
elsewhere in `compose_edition.py`'s `ROW_FACTS` for `inf-otp-alert` /
`opal-critical-surface-alerts`). `prev` is built the SAME way from `prior_report`'s
corresponding section when one is supplied, else `{"axis1": "UNCHECKED", "axis2": None}`
(no baseline yet -- never asserted).

| # | section | real axis2 field | citation |
|---|---|---|---|
| 1 | `lambda_health` | `functions_with_errors` (int) | `lambda_function.py:300-361` |
| 2 | `smartx_pipeline` | `status` (ok/watch/stale/unknown) | `lambda_function.py:391-462` |
| 3 | `data_freshness` | `overall_status` (ok/watch/red) | `lambda_function.py:571-755` |
| 4 | `deploy_drift` | `overall_status` (ok/watch/red) | `lambda_function.py:805-908` |
| 5 | `producer_drift` | `overall_status` (ok/watch/red) | `lambda_function.py:950-1042` |
| 6 | `sns_egress` | `overall_status` (ok/watch/red) | `lambda_function.py:1064-1119` |
| 7 | `graph_head` | `overall_status` (ok/watch/red) | `lambda_function.py:1735-1814` |
| 8 | `contract_integrity` | `overall_status` (ok/watch/red) | `lambda_function.py:1821-1911` |
| 9 | `cost_depth` | `status` (ok/watch) | `lambda_function.py:1230-1330` |
| 10 | `security_sweep` | `critical_issues`/`high_issues`/`medium_issues`/`low_issues` + `status` | `lambda_function.py:1424-1502` |
| 11 (conditional) | `ai_analysis` | n/a -- see CONDITIONAL-BY-DESIGN below | `lambda_function.py:255,:259-260,:1652-1724` |

`graph_head` and `contract_integrity` render `attribution=Graph` (both are about the
same globgrph/Nessie substrate that `compose_edition.py`'s own "ECS cluster
opal-globgrph" row already grounds to `Graph`, PRD sec.6 v0.7 closure block). Every
other MAPPED section renders the mandatory `UNGROUPED` -- none of them names one
v0.7-ratified member the way `opal-gateway`/`opal-globgrph` do (same precedent as the
specimen's own `comp`, SNS-topic and `Cost segment` rows, all `UNGROUPED`).

## BUCKET 2 -- OMITTED-WITH-REASON (2 of 13, always)

Neither section carries an OK/DEGRADED/BREACH signal in its own real return shape
without this cell inventing a threshold the collector itself does not assert
(`C-NO-FROZEN-FACTS`: never rendered from a literal).

- **`aws_costs`** (`lambda_function.py:1137-1192`, `get_aws_costs()`): returns a raw
  MTD total, `daily_avg` and top-10 `by_service` breakdown. No status/severity field of
  any kind. The account's per-pipeline cost trend IS collected with a real computed
  `status` field and is MAPPED instead (bucket 1, row 9, `cost_depth`).
- **`openai_cost`** (`infra/aws/lambda/infrastructure_monitor/openai_cost_tracker.py:158-229`,
  `get_openai_cost_section()`): returns per-function token/dollar accounting
  (`by_function`, `grand_total`, `no_usage_lines`). No status/severity field. Grading it
  OK/DEGRADED/BREACH would require this cell to invent a spend threshold the collector
  itself does not assert.

## BUCKET 3 -- CONDITIONAL-BY-DESIGN (1 of 13)

- **`ai_analysis`** (`lambda_function.py:254-260`): `lambda_handler` sets this key to the
  Claude-generated error briefing ONLY when `lambda_health.functions_with_errors > 0`;
  otherwise it is explicitly set to `None`. **`None` is CORRECT behaviour here, not a
  regression and not a collection gap** -- this cell's own module docstring and
  `_handle_ai_analysis()` say so explicitly rather than leaving a reader to infer it.
  Realized as:
  - an **omission**, reason `"CONDITIONAL-BY-DESIGN: ai_analysis is None because
    lambda_health.functions_with_errors == 0 ..."`, whenever the report's
    `ai_analysis` value is `None` this run;
  - a **MAPPED row** (`axis2="UNASSERTED"` -- free-text advisory content, not itself
    graded OK/DEGRADED/BREACH, since parsing severity out of Claude's prose would be
    exactly the kind of fabricated literal this cell exists to avoid) whenever the
    value is a non-empty string this run.

  Either way the section is always accounted for. In every fixture this task order's
  own `<proof_of_spec>` supplies, `ai_analysis` is forced `None`, so it always realizes
  as the omission above (`OMISSIONS=3` measured = the 2 always-omitted sections + this
  one, every run).

## A GENUINE FIXTURE-VS-REAL-SHAPE FINDING, FILED AND GROUNDED

The `AC2`/`AC3`/`AC4` fixture supplies a UNIFORM synthetic shape
(`{"status": ..., "probe": ..., "functions_with_errors": ...}`) for all 13 sections,
which the task order itself declares is not a claim about the live shape. Measured
against that fixture: only 3 of the 10 MAPPED sections (`lambda_health`,
`smartx_pipeline`, `cost_depth`) actually discriminate between an all-`"OK"` and an
all-`"BREACH"` synthetic report (their real field names happen to be `status` /
`functions_with_errors`, which the fixture also uses); the other 7 read
`axis2=UNASSERTED` in BOTH synthetic reports, because their real field name
(`overall_status`, or the `security_sweep` issue-count fields) is never populated by
the fixture. `AC2`/`AC3` (coverage + reason) and `AC4` (the aggregate row-SET differs)
all still PASS -- this is not a failure against the cell's own criteria, it is the
declared instrument limit the task order asked to be surfaced. Filed as
`NFRA_REPORT-Z-W2-S7` in
`org/missions/D12/NFRA/NFRA_REPORT/surprise-channel/investigations/INVESTIGATION_v1.md`,
class `OBSERVATION`, `hazard_standing: INERT` (the real collector always supplies the
real field names; only the synthetic fixture cannot exercise all 10).
