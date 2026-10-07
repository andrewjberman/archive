# TRADING_CALENDAR_IMPORTERS -- census for TO NFRA_CTLPLN.TO-CT-k-1 (worker 0.9.0_WK_NFRA_CTLPLN~12, 2026-10-07)

Method: every git-tracked file (`git ls-files`, worktree `wk-NFRA_CTLPLN-12` at the build commit) containing the text `trading_calendar` or `_trading_day_calendar`, read by a scratch script (not committed): a file is an IMPORTER when it carries an import statement for the module (`import trading_calendar`, `from trading_calendar`, `from lib.trading_calendar`, `import lib.trading_calendar`, `_trading_day_calendar`), a VENDORED COPY when it is a file named `trading_calendar.py`, PACKAGING when it names the module in a build or deploy list, and a MENTION otherwise (comments, docs, records). `workflows/` and `archive/` were not scanned (run records). Call sites were read for every public-function call line per file; a file whose date source is an event, request or argument is UNKNOWN for the date question.

## Denominators

- Files naming the module at all (excluding `workflows/`, `archive/`): 1133. Import-statement importers: **129** (the Dells reported 103). Of those, 57 sit under `org/` (deliverable and run-once scripts, DOC-OR-OTHER, summarised in section 4) and 72 are the code/test importers tabled in section 2 (the table also carries the 1 import-by-name test and shared-lib rows it classifies).
- Vendored byte-copies of the module: 3 in code (`infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm`, `infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily`, `infra/aws/lambda/opal-assets-absence-check`) plus one test fixture under `org/` (`...pre_act_deployed_coverage/trading_calendar.pyfixture`).
- Packaging lists naming the module: 12 files (section 3).
- Mention-only files (comments, docs, logs, records; no import statement): 1004, not tabled; the code-adjacent ones were read and are comments only (`.tools/safe_deploy_core.py`, `.tools/tool_index.py`, `D_03.composition_artifacts.py`, `publish_page.py`, `pull_eclipse_portfolios.py`, `dim_mdpf_*.py`, `calendar_tieout.py`, opal-gateway `tools.py`/`ssavail_contract.py`, `refresh.py`, `ops/manifests.py`, `ticketing/intake/sweep.py`).
- Class counts of the 73 tabled rows: DOC-OR-OTHER=1, EC2-OR-CONTAINER=13, LAMBDA=35, LOCAL-TOOL=12, TEST=12.
- UNKNOWN cells: pmc-in-runtime UNKNOWN on 23 of 73 rows; passes-outside-range UNKNOWN on 30 of 73 rows (UNKNOWN is a value, never a guess).

Claim levels: 'NO per manifests' = no `pandas_market_calendars` in any requirements file, layer manifest or packaging list read in the repo; the deployed layer bytes themselves were NOT read (no AWS call). 'HAS' = the repo's own install line or layer pin names it.

## 1. Deployed units (the function/host level)

| unit | kind | how it gets the module | pmc in runtime | passes dates outside 2010-2027 / before 2024? |
|---|---|---|---|---|
| mdpf-gold-lambda | LAMBDA | build_package.py flat member | HAS (layer mdpf-gold-calendar-deps, pmc 4.6.1) | UNKNOWN (window arguments) |
| inf-etf-ownership-daily | LAMBDA | VENDORED OLD copy | LACKS | UNKNOWN (event `day`) |
| bd-served-vintage-alarm | LAMBDA | VENDORED OLD copy | LACKS | NO (current) |
| opal-assets-absence-check | LAMBDA | VENDORED OLD copy | LACKS | NO (current) |
| bd-49f-etf-ownership-daily | LAMBDA | layer opal-trading-calendar-layer (built from lib/ at layer-build time) | LACKS per manifests | NO (catch-up window) |
| cot-etf-ownership-daily | LAMBDA | layer opal-trading-calendar-layer | LACKS per manifests | NO (catch-up window) |
| etf-positioning-producer | LAMBDA | layer opal-trading-calendar-layer | LACKS per manifests | UNKNOWN (history partitions) |
| cot-satellites-characteristics-producer | LAMBDA | build_package.py member lib/trading_calendar.py | LACKS per manifests | NO (current) for build_satellites_characteristics; UNKNOWN for the bundled etf_positioning_gold |
| cot-satellites-registry-producer | LAMBDA | build_package.py member | LACKS per manifests | NO (current) |
| irpt-directory-refresh | LAMBDA | source map, staged at build | LACKS (layers = []) | NO (current) |
| irpt-performance-adapter | LAMBDA | source map files list | UNKNOWN (performance_native layer unread) | UNKNOWN (holdings history) |
| irpt-holdings-performance-lambda | LAMBDA | source map files list | UNKNOWN (native layer unread) | UNKNOWN (backfill events) |
| irpt-inf-holdings-performance-lambda | LAMBDA | source map files list | UNKNOWN (native layer unread) | UNKNOWN (backfill events) |
| irpt-49f-reporting-gold-lambda | LAMBDA | source map files list | UNKNOWN (native layer unread) | UNKNOWN (backfill args) |
| etfs-rivalfunds-daily-lambda | LAMBDA | rivalfunds_package.py STAGED | LACKS per manifests | UNKNOWN (event start/end) |
| etfs-rivalfunds-fetch-holdings-lambda | LAMBDA | rivalfunds_package.py STAGED | LACKS per manifests | UNKNOWN (event start/end) |
| rivalfunds-build-canonical-shape-lambda | LAMBDA | rivalfunds_package.py STAGED | LACKS per manifests | UNKNOWN |
| rivalfunds-build-silver-lambda | LAMBDA | rivalfunds_package.py STAGED | LACKS per manifests | UNKNOWN |
| rivalfunds-publish-page-lambda | LAMBDA | rivalfunds_package.py STAGED | LACKS per manifests | UNKNOWN |
| opal-amgt-scoped-api | LAMBDA | build-and-upload-scoped-amgt.sh closure | LACKS per manifests | UNKNOWN (request `asked` date) |
| mdpf-daily-runner EC2 | EC2-OR-CONTAINER | repo checkout / s3 hash-tied copy | HAS (pmc<5, user-data.sh) | UNKNOWN |
| ADVI 49F chain host (advi_49f_floor.tf SSM) | EC2-OR-CONTAINER | repo checkout | UNKNOWN (host not read) | NO for --production; UNKNOWN for --date backfills |
| COT / INF chain hosts, black_diamond gold_dispatch host | EC2-OR-CONTAINER | repo checkout | UNKNOWN (host not read) | UNKNOWN |
| both Dells and the laptop (LOCAL-TOOL rows) | LOCAL-TOOL | repo checkout | laptop HAS 5.4.0; Dells LACK | per tool, section 2 |

## 2. Per-file table (code and test importers)

| file | class | where it runs / function | pmc in runtime | passes dates outside 2010-2027 / before 2024? |
|---|---|---|---|---|
| .claude/skills/mdpf-refresh/mdpf_refresh.py | LOCAL-TOOL | a skill CLI run on a box | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | NO: current-date / T-1 frontier only |
| .tools/comp-freshness | LOCAL-TOOL | CLI on a box | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | NO: current-date / T-1 frontier only (freshness of current partitions) |
| .tools/tests/test_comp_freshness_weekly.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| data/assets/scripts/analysis/commonwealth_price_census.py | LOCAL-TOOL | analysis script on a box | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | YES: ranges start at each CUSIP's first Trade_Date (ADVI_COTBKF measured 2015, 2019, 2022 windows through this module) |
| data/assets/scripts/analysis/commonwealth_price_need.py | LOCAL-TOOL | analysis script on a box | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | YES: same census, first_day..last_day per CUSIP |
| data/assets/scripts/gold/build_satellites_characteristics.py | LAMBDA | cot-satellites-characteristics-producer (members listed in its build_package.py) | NO per manifests: layer pandas-pyarrow-requests-layer has no pmc | NO: current-date / T-1 frontier only |
| data/assets/scripts/gold/investor_reporting/directory_runner.py | LAMBDA | irpt-directory-refresh path (directory_runner is the runner the lambda wraps; trading_calendar staged at build) | NO: irpt-directory-refresh layers = [] (schedule.tf) | NO: current-date / T-1 frontier only |
| data/assets/scripts/gold/investor_reporting/holdings_snapshot.py | LAMBDA | investor-reporting holdings snapshot (packaged by an irpt function; packaging member not confirmed) | UNKNOWN | NO: expected_last_trading_day(now) |
| data/assets/scripts/gold/irpt_holdings_performance/holdings_comparison.py | LOCAL-TOOL | comparison script on a box | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | NO: from 2024-01-01 to today |
| data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py | LAMBDA | irpt-holdings-performance-lambda and irpt-inf-holdings-performance-lambda (source map) | UNKNOWN: layer irpt-performance-native-layer zip is not in the repo (pandas/pyarrow native); no pmc in any manifest read | UNKNOWN: `day` of each run; catch-up/backfill events pass dates |
| data/assets/scripts/gold/irpt_reporting/account_return_daily.py | LAMBDA | irpt-49f-reporting-gold-lambda (source map) | UNKNOWN: layer irpt-performance-native-layer unread | UNKNOWN: args.start/args.end for a backfill |
| data/assets/scripts/gold/runners_49f/a00_dim_account.py | EC2-OR-CONTAINER | 49F chain stage | UNKNOWN (SSM/EC2 host for the ADVI 49F chain; no pandas_market_calendars install in advi_49f_floor.tf read) | NO: absence-age over recent partitions |
| data/assets/scripts/gold/runners_49f/a04_dim_calendar.py | EC2-OR-CONTAINER | 49F chain stage | UNKNOWN (SSM/EC2 host for the ADVI 49F chain; no pandas_market_calendars install in advi_49f_floor.tf read) | UNKNOWN: span = min..max observed dim_balance partitions (earliest partition not read) |
| data/assets/scripts/gold/runners_49f/b04_account_model_membership.py | EC2-OR-CONTAINER | 49F chain stage | UNKNOWN (SSM/EC2 host for the ADVI 49F chain; no pandas_market_calendars install in advi_49f_floor.tf read) | NO: current-date / T-1 frontier only |
| data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py | EC2-OR-CONTAINER | ADVI 49F chain on an EC2 host via SSM (advi_49f_floor.tf) | UNKNOWN (SSM/EC2 host for the ADVI 49F chain; no pandas_market_calendars install in advi_49f_floor.tf read) | NO: --production = prev_trading_day(now); --date D backfills are an argument (UNKNOWN for D) |
| data/assets/scripts/gold/runners_49f/parity_period_returns.py | LAMBDA | irpt-performance-adapter (source map) | UNKNOWN: layers irpt-common (read: no pmc) + performance_native (unread) | UNKNOWN: candidate period ends |
| data/assets/scripts/gold/runners_49f/perfrp_emit_core.py | EC2-OR-CONTAINER | 49F chain stage | UNKNOWN (SSM/EC2 host for the ADVI 49F chain; no pandas_market_calendars install in advi_49f_floor.tf read) | UNKNOWN: start..end of the emitted window |
| data/assets/scripts/gold/satellites_weights.py | LAMBDA | cot-satellites-registry-producer (build_package.py) | NO per manifests (no pmc layer in satellites-registry-producer.tf) | NO: expected frontier of now vs partition_date |
| data/assets/scripts/silver/commonwealth_account_links.py | EC2-OR-CONTAINER | assets silver script (host not read) | UNKNOWN (host not read) | UNKNOWN: lo-45d..hi+45d around data dates |
| data/black_diamond/scripts/gold/gold_dispatch.sh | EC2-OR-CONTAINER | gold dispatcher shell, one inline python call | UNKNOWN (host not read) | NO: current-date / T-1 frontier only |
| data/cot/scripts/gold/runners_cot/a04_dim_calendar.py | EC2-OR-CONTAINER | COT chain stage (host not read) | UNKNOWN (host not read) | UNKNOWN: span of observed partitions |
| data/cot/scripts/gold/runners_cot/c02_twr_engine.py | EC2-OR-CONTAINER | COT chain stage (host not read) | UNKNOWN (host not read) | UNKNOWN: --start/--end arguments |
| data/etfs/scripts/coverage/classifier.py | LOCAL-TOOL | coverage classifier (box script) | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | UNKNOWN: classifies caller-supplied dates |
| data/etfs/scripts/gold/etf_positioning_gold.py | LAMBDA | etf-positioning-producer (layer opal-trading-calendar-layer) and bundled into cot-satellites-characteristics-producer | NO per manifests: the layer holds only lib/trading_calendar.py; pandas-pyarrow-requests-layer has no pmc | UNKNOWN: classifies history partitions at_or_before the as-of; earliest partition not read |
| data/etfs/scripts/presentation/tests/test_coverage_gate.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| data/etfs/scripts/presentation/tests/test_coverage_line.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| data/etfs/scripts/rivalfunds/ai_accounts.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/collector_bloomberg.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/collector_issuer.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/enrichment_bloomberg.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | NO: current-date / T-1 frontier only |
| data/etfs/scripts/rivalfunds/gold_buying_trend.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/gold_canonical_shape.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/gold_holding_contribution.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/gold_holdings_coverage.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/gold_trade_schedule.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/guardrails.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | NO: current-date / T-1 frontier only |
| data/etfs/scripts/rivalfunds/market_context.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/render.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/sweep.py | LAMBDA | the five rivalfunds lambdas, staged by rivalfunds_package.py (STAGED lists lib/trading_calendar.py) | NO per manifests: layer pandas-pyarrow-requests-layer:1 (etfs-rivalfunds/main.tf), no pmc | UNKNOWN: event start/end and windows (earliest_start) are arguments; the rivalfunds product dates in tests are 2026 |
| data/etfs/scripts/rivalfunds/tests/test_g21_holdings_coverage.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| data/etfs/scripts/rivalfunds/tests/test_r8bt1_periods.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| data/etfs/scripts/rivalfunds/tests/test_r8hc1_r30_trading_days.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| data/inf/scripts/gold/runners_inf/a04_dim_calendar.py | EC2-OR-CONTAINER | INF chain stage (host not read) | UNKNOWN (host not read) | UNKNOWN: span of observed partitions |
| data/inf/scripts/gold/runners_inf/c02_twr_engine.py | EC2-OR-CONTAINER | INF chain stage (host not read) | UNKNOWN (host not read) | UNKNOWN: --start/--end arguments |
| data/mdpf/scripts/backfill/eclipse_vintage_reconstruction.py | LOCAL-TOOL | backfill script on a box | per box: laptop HAS 5.4.0; both Dells LACK (CTO ruling B) | UNKNOWN: walks prev_trading_day over silver partition dates; the earliest partition was not read |
| data/mdpf/scripts/gold/build_mdpf_etf_ownership_timeseries.py | EC2-OR-CONTAINER | MDPF gold; runs on mdpf-daily-runner EC2 (and packaged in mdpf-gold-lambda) | HAS: pandas_market_calendars<5 (mdpf-daily-runner user-data.sh line 49 and mdpf-daily-dispatch.sh preflight; mdpf-gold-calendar-deps layer pins 4.6.1) | UNKNOWN: window_start..window_end arguments |
| data/mdpf/scripts/gold/mdpf_calendar_binding.py | EC2-OR-CONTAINER | MDPF binding; refuses a non-pmc backend (assert_pmc_backend compares to PMC_SOURCE, not the fallback string) | HAS: mdpf runner and mdpf-gold-lambda carry pmc<5 | n/a: a re-export; callers' dates apply |
| infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/lambda_function.py | LAMBDA | bd-49f-etf-ownership-daily: layer opal-trading-calendar-layer + pandas layer (bd-49f-etf-ownership-daily.tf) | NO per manifests | NO: catch-up window prior_month_first..yesterday |
| infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/test_catchup_window.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/served_vintage.py | LAMBDA | bd-served-vintage-alarm: VENDORED copy trading_calendar.py (OLD) + vendored served_vintage.py | NO: stdlib-only vendored package | NO: current-date / T-1 frontier only |
| infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/lambda_function.py | LAMBDA | cot-etf-ownership-daily: layer opal-trading-calendar-layer + pandas layer (cot-etf-ownership-daily.tf) | NO per manifests | NO: catch-up window prior_month_first..yesterday |
| infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/test_catchup_window.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py | LAMBDA | inf-etf-ownership-daily: VENDORED copy infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py (163 lines, the OLD module); layer pandas-pyarrow-requests | NO per manifests | UNKNOWN: `day` comes from the event |
| infra/aws/lambda/investor-reporting/directory/expiry.py | LAMBDA | irpt-directory-refresh: staged at build from lib/ (source map staged_from); layers = [] | NO: no layers, stdlib | NO: current-date / T-1 frontier only |
| infra/aws/lambda/investor-reporting/holdings-performance/handler.py | LAMBDA | irpt-holdings-performance-lambda, irpt-inf-holdings-performance-lambda: source map files list lib/trading_calendar.py; layer irpt-performance-native-layer | UNKNOWN: native layer zip not in the repo | NO: gap from last landed day+1 to prev_trading_day(frontier); empty gold -> single target day |
| infra/aws/lambda/investor-reporting/holdings-performance/tests/test_catch_up.py | TEST | test file (loads the real lib/trading_calendar.py by name) | local | NO: fixture dates 2026 |
| infra/aws/lambda/investor-reporting/performance/holdings_gold.py | LAMBDA | irpt-performance-adapter: source map files list lib/trading_calendar.py; layers irpt-common + performance_native | UNKNOWN: performance_native unread; irpt-common requirements read, no pmc | UNKNOWN: trading_days_between(lo, hi) over holdings history |
| infra/aws/lambda/investor-reporting/performance/tests/test_holdings_gold_calendar_gap.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| infra/aws/lambda/investor-reporting/reporting-gold/handler.py | LAMBDA | irpt-49f-reporting-gold-lambda: source map files list lib/trading_calendar.py; layer irpt-performance-native-layer | UNKNOWN: native layer zip not in the repo | NO: newest landed+1 .. T-1 |
| infra/aws/lambda/mdpf-pipeline/_shared/mdpf_roster.py | LAMBDA | mdpf-gold-lambda (shared module; also read by mdpf-daily-trigger): mdpf-gold-lambda packages trading_calendar.py flat (build_package.py line 170) | HAS: mdpf-gold-calendar-deps layer, pandas_market_calendars==4.6.1 | NO: current-date / T-1 frontier only |
| infra/aws/lambda/opal-assets-absence-check/lambda_function.py | LAMBDA | opal-assets-absence-check: VENDORED copy trading_calendar.py (OLD) | NO: stdlib-only vendored package | NO: current-date / T-1 frontier only |
| integrations/bloomberg/pipeline/backfill_extra_securities_history.py | LOCAL-TOOL | Bloomberg box script | UNKNOWN (Bloomberg box environment not in repo) | UNKNOWN: end = prev_trading_day(today); start is an argument |
| integrations/bloomberg/pipeline/etf_constituents_pull.py | LOCAL-TOOL | Bloomberg box script | UNKNOWN (Bloomberg box environment not in repo) | NO: current-date / T-1 frontier only |
| integrations/bloomberg/pipeline/freshness_check.py | LOCAL-TOOL | Bloomberg box script | UNKNOWN (Bloomberg box environment not in repo) | NO: current-date / T-1 frontier only |
| integrations/bloomberg/research/price_axis_pull.py | LOCAL-TOOL | Bloomberg box script | UNKNOWN (Bloomberg box environment not in repo) | NO: current-date / T-1 frontier only |
| integrations/bloomberg/research/price_history_pull.py | LOCAL-TOOL | Bloomberg box script | UNKNOWN (Bloomberg box environment not in repo) | NO: 400 calendar days ending prev_trading_day(today) |
| lib/research/api/rolling_windows.py | LAMBDA | opal-amgt-scoped-api (closure root lib.trading_calendar, build-and-upload-scoped-amgt.sh) | NO per manifests (build-and-upload-scoped-amgt.sh closure; no pmc in it) | NO: current-date / T-1 frontier only |
| lib/research/api/scoped_amgt.py | LAMBDA | opal-amgt-scoped-api | NO per manifests (build-and-upload-scoped-amgt.sh closure; no pmc in it) | UNKNOWN: `asked` date is a request input (line 3312) |
| lib/research/freshness/stale_rule.py | LAMBDA | opal-amgt-scoped-api closure (lib.research) | NO per manifests (build-and-upload-scoped-amgt.sh closure; no pmc in it) | NO: served date .. today |
| lib/research/freshness/tests/test_stale_rule.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| lib/research/harvest/test_ak2_window_tone.py | TEST | test file | local: test runs on the box it is run on | NO: fixture dates 2026 |
| lib/research/harvest/window_tone.py | LAMBDA | lib.research closure of opal-amgt-scoped-api (membership of this module not confirmed) | NO per manifests (build-and-upload-scoped-amgt.sh closure; no pmc in it) | UNKNOWN: as_of_date is an input |
| lib/served_vintage.py | DOC-OR-OTHER | (shared source of the vendored bd-served-vintage-alarm copy): source file in lib/; not itself packaged here | n/a | NO: current-date / T-1 frontier only |

## 3. Packaging lists and vendored copies

| file | role |
|---|---|
| infra/aws/lambda/ci/lambda-source-map.json | packaging list: 10 functions list lib/trading_calendar.py (mdpf-gold-lambda, inf-etf-ownership-daily, etf-positioning-producer, cot-satellites-registry-producer, cot-satellites-characteristics-producer, irpt-performance-adapter, irpt-directory-refresh, irpt-holdings-performance-lambda, irpt-inf-holdings-performance-lambda, irpt-49f-reporting-gold-lambda) |
| infra/aws/lambda/etfs-pipeline/rivalfunds_package.py | STAGED packaging list: lib/trading_calendar.py into the five rivalfunds lambdas |
| infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py | packaging list line 170 (trading_calendar.py at zip root) |
| infra/aws/lambda/cot-pipeline/cot-satellites-characteristics-producer/build_package.py | packaging list (member lib/trading_calendar.py) |
| infra/aws/lambda/cot-pipeline/cot-satellites-registry-producer/build_package.py | packaging builder (member lib/trading_calendar.py) |
| infra/aws/lambda/etfs-pipeline/etf-positioning-producer/build_package.py | REMOVED trading_calendar.py from members; it comes from the layer |
| infra/aws/lambda/layers/opal-trading-calendar-layer/build-layer.sh | builds the layer from lib/ at build time; used by etf-positioning-producer, bd-49f-etf-ownership-daily, cot-etf-ownership-daily |
| infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh | CLOSURE_ROOTS includes lib.trading_calendar (opal-amgt-scoped-api) |
| infra/aws/lambda/investor-reporting/PATH_MANIFEST.json | path manifest lists lib/trading_calendar.py |
| .github/workflows/lib-vendored-copies-parity.yml | parity CI: 4 pairs (3 vendored copies exist; the 4th, schwab-bronze-freshness/trading_calendar.py, does not) |
| infra/aws/ec2/EC2_MANIFEST.json | mdpf runner: trading_calendar.py distributed from s3://opal-data-mdpf/code/scripts/gold/ (hash-tied copy) |
| .owned-paths.yaml | ownership of lib/ shared primitives (no runtime) |
| infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/trading_calendar.py | VENDORED COPY (LAMBDA); already differs from lib/ (163 lines, no weekly_production_day); not changed by this order; it is the OLD 2024-2027 fallback with no fail-closed |
| infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py | VENDORED COPY (LAMBDA); already differs from lib/ (163 lines, no weekly_production_day); not changed by this order; it is the OLD 2024-2027 fallback with no fail-closed |
| infra/aws/lambda/opal-assets-absence-check/trading_calendar.py | VENDORED COPY (LAMBDA); already differs from lib/ (163 lines, no weekly_production_day); not changed by this order; it is the OLD 2024-2027 fallback with no fail-closed |

## 4. `org/` importers (DOC-OR-OTHER, one class)

57 files under `org/` import the module (55 python deliverable and run-once scripts of earlier orders, one `.md` carrying an import snippet, and one `.pyfixture`); by directory: org/missions/D12/NFRA=1; org/missions/D5/AMGT=7; org/missions/D5/ETFS=14; org/missions/D8/ETFS=8; org/missions/D9/IRPT=15; org/modules=1; org/tier1_exec=8; org/tier2_senior=3. None is a deployed runtime; each runs only when someone re-runs that deliverable.

## 5. Conclusions the order asks for

- Deployed LAMBDA importers that LACK the package (behaviour changes at their next rebuild or re-vendor, if they ever see an uncovered year): **15 of 20 lambda units** -- inf-etf-ownership-daily, bd-served-vintage-alarm, opal-assets-absence-check, bd-49f-etf-ownership-daily, cot-etf-ownership-daily, etf-positioning-producer, cot-satellites-characteristics-producer, cot-satellites-registry-producer, irpt-directory-refresh, etfs-rivalfunds-daily-lambda, etfs-rivalfunds-fetch-holdings-lambda, rivalfunds-build-canonical-shape-lambda, rivalfunds-build-silver-lambda, rivalfunds-publish-page-lambda, opal-amgt-scoped-api.
- Lambda units whose pmc status is UNKNOWN (native layer zip not in the repo): 4 -- irpt-performance-adapter, irpt-holdings-performance-lambda, irpt-inf-holdings-performance-lambda, irpt-49f-reporting-gold-lambda.
- Lambda units that HAVE the package: mdpf-gold-lambda (4.6.1). EC2: mdpf-daily-runner (pmc<5). Behaviour unchanged for both.
- IMPORTANT: the three VENDORED copies (inf-etf-ownership-daily, bd-served-vintage-alarm, opal-assets-absence-check) are NOT touched by this change; they stay the OLD module (silent answer for pre-2024) until someone re-vendors them. The three layer-fed functions (etf-positioning-producer, bd-49f-etf-ownership-daily, cot-etf-ownership-daily) change only when `opal-trading-calendar-layer` is rebuilt from lib/ and re-published. The build-staged functions change at their next build.
- Importers that pass dates before 2024 or after 2027 (YES): data/assets/scripts/analysis/commonwealth_price_census.py, data/assets/scripts/analysis/commonwealth_price_need.py. Lambda/EC2 rows with UNKNOWN dates: 27 (listed in section 2; the call sites take an event, request or argument date).
- Readers of the old provenance string `NYSE/hardcoded-fallback-2024-2027` in code: `data/mdpf/scripts/gold/tests/test_canplat_p1_1.py:105` (a mock return value; unaffected), and the three vendored copies (their own old source line 163, not comparisons). Prefix reader `infra/aws/lambda/investor-reporting/performance/holdings_gold.py:360` uses `startswith("NYSE/hardcoded")` (still true). `data/mdpf/scripts/gold/mdpf_calendar_binding.py:84` compares to the pmc string, not the fallback string. No literal comparison of the old string breaks.
