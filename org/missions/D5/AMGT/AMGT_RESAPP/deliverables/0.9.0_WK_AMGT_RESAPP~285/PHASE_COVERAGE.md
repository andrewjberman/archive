# AMGT-ba-19 -- chatter phase-coverage read (worker 0.9.0_WK_AMGT_RESAPP~285, round 77)

Function `opal-amgt-scoped-api`, CodeSha256 `OVpDhfwDG3BzKE++wDxMlFA6JrwpTnH3FiHC+NrzsrE=` (OVpDhfwD), 1769 MB, x86_64, python3.11.
Route `/api/scoped/amgt/lead-panel/timeseries/collected/chatter`. Burst: `leadpanel_cold_warm.py --label ba19`, run ONCE at 2026-10-07T01:55:42Z
(`burst_output.txt`): 6 cold chatter invokes (all `?days=30`), 81 invokes in the window, 6 log streams. Raw events: `cloudwatch_events_raw.json`;
join code: `build_coverage.py` (a request is the lines between START and REPORT of one log stream, in timestamp order).

## 1. The emit map (HEAD, `AMGT_PHASE route=chatter`)

| label | file:line |
|---|---|
| generation read | lib/research/api/monthly_chatter.py:304 |
| mentions decode | lib/research/api/monthly_chatter.py:306 |
| compute (first) | lib/research/api/monthly_chatter.py:333 |
| names | lib/research/api/monthly_chatter.py:335 |
| classification | lib/research/api/monthly_chatter.py:339 |
| compute (second) | lib/research/api/monthly_chatter.py:372 |
| serialize | lib/research/api/scoped_amgt.py:6782 |

Six labels, seven sites. A chatter request ALSO prints four `route=rankings/TRENDING/PRICE` lines (scoped_amgt.py:1440 classification, :1444 names,
:1506 generation read, :1517 compute): `_places_moved_index` (monthly_chatter.py:147) calls `read_rankings("TRENDING","PRICE")` on a worker thread
started at :342. They fall INSIDE the second compute span and are not added to any sum (they are in the JSON as nested). The label_set in the JSON holds
all ten labels.

Spans of the handler that emit NO line: (a) `lambda_handler` wrapper -> `scoped_amgt.handler` entry, routing, authorisation (`_scheduled_action_response`,
`_path`, `_firm_id`, `_route_template`, `_query`); (b) the request-time `from lib.research.api import monthly_chatter, rolling_windows` at
scoped_amgt.py:6773 (chain reaches pyarrow and numpy), and `parse_days`; (c) the first lines of `read_monthly_chatter` up to :289 (its `from ... import
rolling_windows, scoped_amgt` is cached); (d) serialize line to handler return and the runtime response hand-off. The S3 client creation, the `names_read`
import and the gold-read starts (:290-303) sit INSIDE the first phase (generation read).

## 2. Attribution of every cold millisecond (6 cold invokes; ms)

| invoke (stream tail) | Init ms | Duration ms | generation read | mentions decode | compute (1st, :333) | names | classification | compute (2nd, :372) | serialize | outside | outside before 1st phase / after serialize (log ts) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3883a18b9d41 | 628.27 | 2855.97 | 768 | 0 | 1040 | 0 | 7 | 253 | 2 | 785.97 | 782 / 3 |
| 3262d0adc7d2 | 531.31 | 3776.75 | 966 | 25 | 1475 | 0 | 6 | 299 | 2 | 1003.75 | 1000 / 3 |
| 3e8310b6fadd | 619.42 | 2811.16 | 684 | 151 | 962 | 0 | 6 | 248 | 2 | 758.16 | 734 / 3 |
| 1eedd4017efc | 678.21 | 2913.50 | 698 | 102 | 1086 | 0 | 9 | 218 | 2 | 798.50 | 792 / 3 |
| 55501c0e5faf | 663.37 | 2941.48 | 711 | 49 | 1128 | 1 | 12 | 228 | 2 | 810.48 | 790 / 4 |
| fd04f6ccf0e0 | 670.08 | 2931.16 | 660 | 96 | 1121 | 0 | 7 | 264 | 2 | 781.16 | 776 / 3 |

`outside` = Duration - sum of the seven route=chatter phase values (integers as logged), so each row sums to the Duration by construction. The last
column splits `outside` by CloudWatch event timestamps (1 ms resolution): before = (first phase line time - START time) - generation-read ms; after =
REPORT time - serialize line time. Before + after is within 1-21 ms of `outside` (log-timestamp noise; the 21 ms row is invoke 3e8310b6fadd).
Init Duration is outside Duration and is listed for reference only.

Reading: Duration 2,811-3,777 ms (mean 3,038; one slow container at 3,777). In-phase 2,070 / 2,773 / 2,053 / 2,115 / 2,131 / 2,150 ms.
Outside 758-1,004 ms (mean 823), of which 734-1,000 ms (mean 812) sits BEFORE the first phase line and 3-4 ms after serialize. So the unlabelled
time is the span from handler entry to the start of `read_monthly_chatter`'s first phase, i.e. routing plus the request-time import chain.
Two big labelled items are cold-only: the first `compute` (962-1,475 ms cold, mean 1,135; warm mean 321 ms over 21 warm invokes) and the first `generation
read` (660-966 ms cold, mean 748; warm mean 62 ms). Warm Duration over the same window: mean 522 ms (451-636).

## 3. The outside time, profiled locally (inference, not a measurement of the deployed function)

`profile_chatter.py`, fresh process, `time.perf_counter` around the handler's own calls, nothing under lib/ edited (run 3 times, then once with `--full`):

| unlabelled span | local ms (runs) |
|---|---|
| S1 routing + authorisation (all helper calls) | 0.012-0.018 |
| S2 request-time import of monthly_chatter + rolling_windows (113 new modules; numpy and pyarrow load here) | 97, 115, 223 (`--full` run 109); `-X importtime`: 116 cumulative, pyarrow 94 of it, numpy 59 of that |
| S3 parse_days | 0.003-0.004 |
| S4 `_response` on a 1,500-row stub (the real one is the labelled serialize, 2 ms deployed) | 0.9-1.2 |
| S0 import of scoped_amgt (Init, not Duration; reference) | 525-862 (deployed Init 531-678) |

Locally the outside time is the import chain and nothing else: S2 is 97-223 ms against 734-1,000 ms deployed before the first phase, so deployed it is about 4-8 times
the local figure (cold package read, Lambda CPU share and the layer are the likely causes; none of that is measured here). THE LOCAL SPLIT IS AN INFERENCE ABOUT THE
DEPLOYED ONE: it says which span CAN hold the time (the only one with non-trivial cost), and the deployed timestamps say the time sits before the first phase; it
does not measure the deployed import.

## 4. Free cuts (no spend; each is an estimate, none validated on the deployed function, no deploy was made)

| cut | where | est ms | note |
|---|---|---|---|
| Import the chatter chain (pyarrow, numpy, coverage) at module scope, so it runs in Init | scoped_amgt.py:6770-6773 (AMGT-ag-0 comment) | 812 | measured outside-before mean; MOVES to Init, so Init+Duration is unchanged unless Init has more CPU (unmeasured); the isolated-runtime arm named in the comment must be re-read |
| Pre-warm the pyarrow kernels/decode path the first compute uses, at Init | monthly_chatter.py:308-333 | 814 | cold mean 1,135 less warm mean 321; inference that the gap is first-use cost; MOVES to Init |
| Make the S3 client and first TLS connection at Init | monthly_chatter.py:294-297 | 686 | cold generation-read mean 748 less warm 62; the client/TLS share cannot be split from log lines; upper bound; MOVES to Init |

The three estimates overlap (they are gaps between cold and warm, not independent). All three relocate cold cost from Duration to Init; none removes cold
wall time on its own. The floor if every cold-only cost left the request is the warm Duration, 522 ms (JSON `residual_ms`). Not exhausted.

## 5. Inputs for the card (numbers only)

1 provisioned instance, 1769 MB (read from `get_function_configuration`), 730 hours a month. Price per GB-second 0.0000041667, provisioned-concurrency
allocation, x86, us-east-1, read at `docs/briefs/fe-driven-lambda-keep-warm-feasibility-20260603.md:89`; the public AWS price page was not read here
(UNVERIFIED-HERE). Arithmetic: 1769/1024 x 0.0000041667 x 3600 x 730 x 1 = 18.9167 USD a month (allocation only; the brief gives on-demand 0.0000166667 per
GB-s; a provisioned request's own duration rate is not in this repository and is UNVERIFIED-HERE).
