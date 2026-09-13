# AMGT-rd-5 -- THE CHATTER AXIS WRITER: window record

`0.9.0_WK_AMGT_RESAPP~2`, round 5/v5, cell AMGT-rd-5 (row S16, FWD-15). Deliverable (c):
the window, the normalization, and TOP_N implemented -- each cited, not chosen here.

## The axis, as given

| parameter | value | declared in | cited to |
|---|---|---|---|
| window | 30 days | `lib/research/metrics/chatter_gate.py:WINDOW_DAYS` | PRD v0.3 s.3b (`AMGT_RESAPP_PRD.md:525`) + Andrew-direct 2026-09-11 ~07:2xZ, verbatim "30 day for both trending and breakout (means we have to backfill)" (`org/tier1_exec/4.0.0_SA_CRO/deliverables/CHATTER_VOLUME_DAILY_REFRESH_MECHANISM_20260911.md` s.4a) |
| normalization | 0-100, min-max relative to the current constituent set | `chatter_gate.py:SCORE_MIN`/`SCORE_MAX` | Same PRD line: "0-100 normalized". Andrew, same turn: "chatter can be 0-100 normalized relatively among the constituents"; CRO doc s.4a point 2: "take every tracked ticker's raw `chatter_count`, min-max (or percentile) normalize across that day's ~89-name universe into 0-100" |
| TOP_N | 10 | `chatter_gate.py:TOP_N` | Same PRD line: "TOP_N=10" |

`lib/research/metrics/chatter_gate.py` is the ONE place these three numbers are declared
(`CITATION` constant in that module carries both citations verbatim). Every other module
that needs them -- `chatter_axis.py` (the producer), `tests/test_chatter_axis.py` (AC1),
the Lambda handler (`infra/aws/terraform/amgt-resapp/lambda_src/lambda_function.py`, via
the packaged `chatter_axis.py`/`chatter_gate.py`) -- imports these names. None re-declares
a literal `30`, `0`/`100`, or `10` as its own threshold (mechanically checked:
`test_chatter_axis_imports_the_gate_not_a_local_redeclaration` reads `chatter_axis.py`'s
own source text and asserts it carries no `WINDOW_DAYS =`/`SCORE_MIN =`/`SCORE_MAX =`/
`TOP_N =` assignment of its own).

Nothing here widens, narrows or re-tunes the window, and no new qualification threshold
is invented anywhere in this cell's chatter path (task-order BLOCK).

## The window's exact definition

`window_bounds(as_of_date, window_days=30)` returns `[as_of_date - 29 days, as_of_date]`
inclusive of both ends -- 30 calendar days total, including the as-of date itself. Example
(2026-09-11): `2026-08-13 .. 2026-09-11`.

## Where the raw signal comes from, and the state it is in today

The raw chatter count per ticker is a COUNT-only DynamoDB `Query` against
`opal-amgt-articles` (AMGT-rd-1's table)'s `ticker_date_index` GSI (`ticker` HASH,
`published_at` RANGE), `published_at BETWEEN start_date AND end_date~` -- never fetching
article bodies; this producer ranks volume, it does not read content.

MEASURED at this cut (2026-09-11, live `describe-table` + `scan --select COUNT`):
`opal-amgt-articles` is ACTIVE but holds 0 items -- AMGT-rd-3/rd-4 (the harvester box and
the four harvesters) have not landed data yet, and this cell is independent of them (its
only dependency is AMGT-rd-2). `normalize_scores`' degenerate branch (every ticker's raw
count equal, including the all-zero case) scores every ticker `SCORE_MIN` (0) rather than
fabricating a spread that does not exist, and `rank_top_n`'s ticker-ascending tie-break
still produces a deterministic TOP_N=10 -- pre-computed rows are written even when the
signal itself is currently flat (bound (d): PRE-COMPUTED ONLY; the axis does not refuse to
rank just because today's underlying volume is zero).

## Which tickers are considered

`read_universe_tickers()` reads the identity layer's landed `universe.json`
(AMGT-s-12/AMGT-r-12, `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/
0.9.0_WK_AMGT_RESAPP~4/universe.json` at this worktree's HEAD -- overridable via
`--universe`), restricted to entries whose `bloomberg_ticker` status is `MEASURED`
(34 of 89 folders at this cut). An `UNRESOLVED` entry carries no identifier to query
`opal-amgt-articles` by -- excluded on that precondition, not as a chatter threshold.

## Exercised, live, ad hoc (QA only -- bound (b))

```
$ python -m lib.research.metrics.chatter_axis --dry-run
OK: chatter axis [DRY-RUN] as_of=2026-09-11 window=2026-08-13..2026-09-11 tickers_considered=34 rows_ranked=10 rows_written=0
  rank=00001 ticker=2317 TT score=0.00 raw_chatter_count=0
  ...

$ python -m lib.research.metrics.chatter_axis
OK: chatter axis [WRITE] as_of=2026-09-11 window=2026-08-13..2026-09-11 tickers_considered=34 rows_ranked=10 rows_written=10
```

Live post-write verification (`aws dynamodb query --index-name axis-rank-index
--key-condition-expression "axis_date = :ad" --expression-attribute-values
'{":ad":{"S":"CHATTER#2026-09-11"}}'`): `Count: 10`, `rank_sort` `00001..00010`, every
`score` `0` (the all-zero-signal case above), tickers alphabetical
(`2317 TT`, `9433 JP`, `992 HK`, `ASML NA`, `BA US`, `BABA US`, `BBSE3 BZ`, `BP/ LN`,
`COST US`, `Enel IM`).

## THE SCHEDULE (deliverable (b)) -- a real clock trigger, deployed and verified live

`infra/aws/terraform/amgt-resapp/chatter-axis-schedule.tf`: Lambda `amgt-resapp-chatter-axis`
(python3.12, least-privilege role: `dynamodb:Query` on `opal-amgt-articles`'s
`ticker_date_index` only, `dynamodb:PutItem`/`BatchWriteItem` on
`opal-amgt-security-metrics` only, and its own CloudWatch Logs stream -- the standard
Lambda execution grant, not a monitor) + `aws_scheduler_schedule`
`amgt-resapp-chatter-axis-daily`, `cron(0 10 * * ? *)` UTC, `state = ENABLED`, targeting
the Lambda via a scoped `lambda:InvokeFunction`-only scheduler role. Deployed via
`safe-apply` (change-management ledger
`org/critical_paths/change_management/20260911T1812Z_amgt-resapp-rd-5-chatter-axis-schedule_deploy_completion.md`,
opened before the act, both legs closed with live proof, CLOSED same session -- nothing
stranded): `Apply complete! Resources: 6 added, 0 changed, 0 destroyed.`

Live verification, post-apply:
```
$ aws lambda get-function --function-name amgt-resapp-chatter-axis --query "Configuration.[FunctionName,State,LastUpdateStatus,Runtime]" --output text
amgt-resapp-chatter-axis  Active  Successful  python3.12

$ aws scheduler get-schedule --name amgt-resapp-chatter-axis-daily --query "[Name,State,ScheduleExpression]" --output text
amgt-resapp-chatter-axis-daily  ENABLED  cron(0 10 * * ? *)

$ aws lambda invoke --function-name amgt-resapp-chatter-axis .out.json
{"StatusCode": 200, "ExecutedVersion": "$LATEST"}
$ cat .out.json
{"as_of_date": "2026-09-11", "tickers_considered": 34, "rows_ranked": 10, "rows_written": 10}
```
CloudWatch Logs confirm a clean `OK:` line and no error on two live invokes
(`2026-09-11T18:14:26Z` and `18:15:02Z`, ~10-16s each, well inside the 60s timeout).

10:00 UTC is an operational cadence choice (after the prior UTC day's press cycle has
largely landed, before the US session opens) -- NOT one of the three given axis numbers,
which stay exactly as `chatter_gate.py` declares them.

## Why the Lambda's source is a static zip, not `archive_file` -- a genuine, measured blocker

The natural Terraform shape (`data "archive_file"`, packaging `lib/research/metrics/`
straight from the repo, as `infra/aws/terraform/estate-report/orchestrator.tf` does for
its own Lambda) needs the `hashicorp/archive` provider declared in a `required_providers`
block. This module directory (`infra/aws/terraform/amgt-resapp/`) already has exactly ONE
such block, in `security-metrics-table.tf` (AMGT-rd-2's own file) -- and this cell's task
order explicitly BLOCKS touching that file's `terraform{}`/`provider{}`/`backend{}`
content (surprise rows `AMGT_RESAPP-Z-S9`/`-S10`: the directory already carries a live
provider/backend collision between AMGT-rd-1's and AMGT-rd-2's own files, routed to
AMGT-rd-3 for reconcile -- not this cell's to touch). MEASURED, not assumed: adding a
second `required_providers` block for `archive` and running `terraform init` against this
directory refused hard --

```
Error: Duplicate required providers configuration
  A module may have only one required providers configuration. The required
  providers were previously configured at chatter-axis-schedule.tf:33,3-21.
```

-- a genuine Terraform limitation, not a style question. Per the coordinator's amendment
(898fef5268): a terraform command failing on "Duplicate provider configuration" against
this module is the known, routed-elsewhere defect and this cell stops on it rather than
fixing it -- which is exactly what happened here, one level removed (the SECOND
declaration was mine, not rd-1's, but the module's one-config ceiling is the same
constraint). Instead: `infra/aws/terraform/amgt-resapp/lambda_src/build_zip.py` builds the
deployment zip OUTSIDE Terraform, reading the exact same three source files
`archive_file` would have (`lambda_function.py`, `lib/research/metrics/chatter_gate.py`,
`chatter_axis.py`) plus a frozen `universe.json` snapshot, and `chatter-axis-schedule.tf`
references the resulting static file via Terraform's BUILT-IN `filebase64sha256()` --
no provider requirement at all. `terraform init` + `terraform validate` + `terraform plan`
all passed cleanly against this directory with that shape (`6 to add, 0 to change, 0 to
destroy` -- zero diff against AMGT-rd-2's already-applied table, confirming this file adds
nothing that touches rd-2's own resource). Re-run `build_zip.py` after any change to the
packaged source files, then re-apply -- documented in both that script's docstring and
this file's terraform comments.
