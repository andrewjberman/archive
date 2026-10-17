# Never-widen sign-off packet -- r34j: the resident r34h -> r34j at pin 33f40e903a (the YCharts price tier on the estate client's working form; the door's checker reads the last finite close at the T-1 frontier)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-17. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34, CTO msg 9561).
**Authority:** CTO msgs 10040 (r34j re-adds the tier by CALLING the estate builder), 10079 (option C accepted with two pinning tests: the SPY path byte-equal to IB2's HTTP 200 request; a signature pin on fund_data and _request; `ycharts_client.py` enters the package at its pinned blob, the pin printed here), 10112 and 10122 (the door's checker is the defect behind r34i's V2 failure; fix it in r34j with tests for a null newest row, a Saturday and a holiday; the pricing `as_of` alignment is a separate pair). The reads: `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34h/PRICE_FORM_READ.txt` (IB2 msg 10066: SPY, the estate form, HTTP 200, 1,256 points) and `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34i/A_AFTER_R34I.txt` (r34i rolled back, V2S FAIL SPY LAST_CLOSE_NOT_FINITE). Cells 52f16d8e45,590fad681e. The CRO's research: `org/tier1_exec/4.0.0_SA_CRO/deliverables/RESEARCH_20261016_YCHARTS_SINGLE_TICKER_PRICE_SERIES_FORM.md` @c9f3005376.
**One move:** D1, the install of one new root on the resident host. Two code members change, two are added and the bindings' provenance changes; the tiers (`estate, yfinance, ycharts`) and the budget (6 calls, 390 s) are r34h's. No IAM, Lambda, queue, table or schema moves; no new vendor call path before the first price call a job makes.

## 1. What ships

Package pin `33f40e903a27709915d1c369fa7ce222dcfe8b5d`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34j_build.py` over the tools at that pin, BUILD ONLY, over the RUNNING r34h root (tarball sha256 `60cc8d1d68627c993121df7eca946a40046f1d7f63ddfd2968f83e27077b93c0`). **317 members**: 311 identical to r34h, **4 changed**, **2 added**, 0 removed.

| member | vs r34h | what changes |
|---|---|---|
| `intake/yfinance_check.py` | changed (LIVE in the resident's runtime, static import walk) | the door's checker judges a symbol by its last FINITE close at or before the T-1 trading-day frontier of lib/trading_calendar.py (`now=` injectable): a null newest row, a Saturday's Friday row and the run's own day are no longer the answer (cell AR-g-157) |
| `ycharts/research/price_adapter_ycharts.py` | changed (LIVE in the resident's runtime, static import walk) | the YCharts price reader asks for the path price_form_ycharts builds and sends it with no params (cell AR-g-155) |
| `ycharts/research/price_form_ycharts.py` | ADDED (LIVE in the resident's runtime, static import walk) | NEW: calls the estate client's own fund_data(symbol, calc) on a subclass that reads no secret and sends nothing, and returns the path and query (calc price; level for a ^ index) (cell AR-g-155) |
| `ycharts/research/ycharts_client.py` | ADDED (LIVE in the resident's runtime, static import walk) | NEW: the estate client infra/aws/lambda/ycharts-market-data-pull/ycharts_client.py at its pinned blob, unedited; only its fund_data builder is called, never its sending (CTO msg 10079) |
| `reports/resident_bindings.json` | changed | `provenance.package_pin`, and the files-from list's count and sha256 (it grew by one line, `price_form_ycharts.py`); the verifier proves no other key moved |
| `SHA256SUMS` | changed | the package sums, replaced |

**The estate client's pin.** `infra/aws/lambda/ycharts-market-data-pull/ycharts_client.py` enters the package as `ycharts/research/ycharts_client.py` from the pin: git blob `95f3f2009eb1afb9134e50e5dd24d1fe725dd7d2`, sha256 `da9f7c7b7f8caa1c1a7d04e5f37f4f645e006d7164e00a7adad2dce0a2fedba0`. It is not edited. The module calls only `YChartsClient.fund_data`; the client's own sending (its credentials secret, cookie header, `urllib`) is never reached, because the subclass skips `__init__` and replaces `_request`. A test pins the signatures of `fund_data` and `_request`: a change to either fails the suite.

**Artifacts** (staged outside the repository; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34j.tar.gz`: sha256 `36e19ce7be385d511f85fd216d6018fddc930792f9d3c2ba89cc65d34b258bda`, 1,130,999 bytes, 317 members.
- Package sums `irpt-resident-0485393f3a-r34j.package.SHA256SUMS`: sha256 `db9ccf39ea1f7ab25ff74ea64cebb526b073a65f179f877107cf2a6d1759d6f3`.
- Host install script `resident_host_install_0485393f3a-r34j.sh`: sha256 `bd84c5d78cdfeb17eaea5d8ce81649d8505120e151bcce3a9ac00f924c7e8471`; `install_r34.sh` `191d34cd26716e9ec18383764f11834e207a274807e37d52e7b4058cd199a559`; `pre_read_r34.sh` `65a7f234305ba958aab6050fe65d72cdeefba39c8e8bc885fa779e0fdd48c308`; `rollback_r34.sh` `19fd322ad2bc0e231ac8e4641c2d3d6c837a444a019d042a340a830a41b8d1f5`.
- V2 script `v2_service_env_r34j.sh` (in the repository at `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`): sha256 `f2ac6e5b35e750f4130f7c8063695e67581279c5b72ec366fef849b4a608c280`; its offline test printed 27 cases OK.
- The lease, the budget, the resolve hop, the price transport, the door's resolver and every other member are unchanged.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34h) | AFTER (r34j) |
|---|---|---|
| the door's check of a held symbol (`intake/yfinance_check.py`) | the NEWEST Yahoo row decides: a null close reads NOT_KEPT (r34i's V2 hit it at 00:50Z on a Saturday), and a row dated after T-1 is read as the answer | the last FINITE close dated at or before `prev_trading_day(expected_last_trading_day(now))`; rows after that day are ignored; an only-non-finite history is still NOT_KEPT `LAST_CLOSE_NOT_FINITE`, a last finite close of zero or less NOT_POSITIVE, rows only after the frontier NOT_KEPT `NO_ROWS`; a calendar error is CHECK_FAILED, never NOT_KEPT |
| the YCharts price tier's request | `/charts/fund_data.json?securities=id:SPY,include:true,&zoom=max`, refused HTTP 400 (IB2 PRICE_PROBE), so each price call that reached the tier spent one call of the window budget for nothing | the estate client's own 41-parameter quote-page request, calc price (level for a `^` index): 760 characters for SPY, byte-equal to the request that answered HTTP 200 (IB2 PRICE_FORM_READ); still one symbol per call under the same lease and budget |
| a symbol YCharts prices | -- | the served levels are PRICE levels, so the chained series is a price return, not a total return |
| the host's call budget, the lease row, the count row, the resolve hop, the tiers list | 6 calls per 390 s | unchanged |

**Known limits (named, not stops).** (1) ONE SAMPLE: the estate form was read once, for SPY, signed in (and 67 of 67 in May for the estate client's pull); other symbols, the signed-out call and ETFs other than SPY are unmeasured. (2) PRICE, NOT TOTAL RETURN: whether a report line must carry that basis next to `source: ycharts` is a PRD question (C-PRICES names the source only). (3) THE CALENDAR'S FALLBACK covers 2010 to 2027 (`pandas_market_calendars` is absent on the host): a date outside it raises, which the checker reads as CHECK_FAILED; regenerate with `lib/tests/gen_nyse_closures.py --write` before 2028. (4) THE PRICING `as_of` is still the weekday rule (`resident_installed.py:379-385`: Saturday gives Friday, the calendar gives Thursday); it moves report as-of dates and is its own pair (CTO msg 10122, row IRPT_ANLREQ-D2-S163). (5) The DASHBD calendar hunk `f25618c0b4` is again NOT in this release (the pin is a scratch commit that puts `lib/trading_calendar.py` back to the r34e bytes; `prev_trading_day` and `expected_last_trading_day` exist in those bytes).

**Writers counted.** Each changed or added member: ONE writer (the builder, for this release). The bindings file and the package sums: ONE (the builder).

## 3. Apply protocol, in this order

1. **No YCharts call and no `~Y2` window runs during the install or V2.** The GO says so in terms.
2. Both halves at HEAD naming this file's blob. The ledger `irpt-resident-r34j-20261017` is opened first; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
3. **Send every host script AS ROOT.** Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34h`; the r34j root absent; the library and wrapper unmoved; every changed member at its r34h value and the added members absent; the queue 0 0).
4. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM`.
5. V1: running root `0485393f3a-r34j`; the 6 changed or added members at their built value; the package sums 316 of 316 OK; the imports (including `price_form_ycharts` and `ycharts_client`); queue 0/0; no sign-in in the journal; `opal_pricing` enabled true with the tiers `estate, yfinance, ycharts` and `ycharts_window_budget` (6, 390).
6. **V2, INSIDE the service's own environment:** `v2_service_env_r34j.sh`, sha256 `f2ac6e5b35e750f4130f7c8063695e67581279c5b72ec366fef849b4a608c280` (verify before sending). It keeps r34h's controls, back-off, door, pricing and budget checks, and its TIER check now reads the estate-form SPY path (760 characters, sha256 `96a5d1b9...e383d`, built by the shipped modules from the shipped estate client, no network). The SPY and ZQXWVK reads use the shipped checker, so they follow the T-1 rule. No YCharts call.
7. **Gate:** anything but `V2S OK` (or an install that did not print its success line): send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34h`, close the ledger ROLLED-BACK, report. No retry.
8. The ledger closes at V2.

**Live proof is a separate act:** one priced request that reaches the YCharts tier (a symbol neither the estate nor Yahoo prices), read for its status, its rows and its source field.

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34h`, which stays on the host.
- **The receipt:** the r34h receipt is kept by the install and copied back.
- **The lease row and the count row:** unchanged by r34j (no lease code moves).
- **Queued messages:** none are touched; a message received after a rollback is served by r34h.

## 5. Not claimed

- That the YCharts price tier answers for any symbol but SPY, or without the signed-in session, or that it keeps answering.
- That a price return is what a report should print where a total return is expected.
- That the live host, S3 objects, the lease row, running root and receipt are as the build assumes (this is a build record; they were NOT read).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-17, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34j`); the receipt and its r34h copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO

(not signed)
