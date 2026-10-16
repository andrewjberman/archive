# Never-widen sign-off packet -- r34e: the resident r34c -> r34e at pin f9f851d215 (the door checker reads Yahoo's 404 for an unknown symbol as NOT_KEPT, not CHECK_FAILED)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-16. **Applier:** `0.7.0_AE_CloudOps~AQ2`.
**Authority:** CTO msgs 9283, 9291, 9345 and 9354 (run 3 on hold; the r34d fix rolled back at V2 in the service; read the real exception class first; the r34e rule APPROVED with one tightening: no rows ONLY for `YFTickerMissingError` by name, or a curl_cffi `HTTPError` whose `exc.response.status_code` is 404 and whose response URL is Yahoo's quoteSummary endpoint naming THIS symbol, URL-decoded, exact segment match). Diagnosis: AQ2's read-only records `CHECKFAIL_READ.txt` (commit 51686af530) and `EXCCLASS_READ.txt` (commit 6395c4000d): in the service's own environment ZQXWVK raises `curl_cffi.requests.exceptions.HTTPError` "HTTP Error 404: " from yfinance's info fetch (`quote.py:612 _fetch_info`, `data.py:463 get_raw_json`, `models.py:167 raise_for_status`), which the r34d match on yfinance's own classes never saw. **r34d** was applied and ROLLED BACK at V2 the same session (ledger `irpt-resident-r34d-20261016` ROLLED-BACK, AQ2 msg 9343); its root and three S3 objects are kept, so THIS release has its own names (root `0485393f3a-r34e`, keys `...-r34e.*`). **Ledger:** `irpt-resident-r34e-20261016`.
**One move:** D1, the install of one new root on the resident host. One member changes: `intake/yfinance_check.py`. No IAM, Lambda, queue, table or schema moves; no new Yahoo call path (the checker already calls Yahoo for each symbol YCharts omits, bounded as r34c's packet states); `opal_pricing` stays OFF.

## 1. What ships

Package pin `f9f851d215b1bcbb83ebe9c7a110e66d700d2191`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34e_build.py` over the tools at that pin, BUILD ONLY, over the RUNNING r34c root (tarball sha256 `272d5c543bc7731217f57157afd9817db9ed8906b148977852c9b9b1714d2ff8`). **314 members**: 311 identical to r34c, **3 changed**, 0 added, 0 removed. Two builds under one fixed clock are identical 314 of 314, and the tarball equals the issuer's own earlier build of the same pin. The verifier `ar_g126_checks.py verify` (independent of the builder) recomputed every number below and passed.

| member | vs r34c | what changes |
|---|---|---|
| `intake/yfinance_check.py` | changed (LIVE in the resident's runtime, static import walk) | `default_history` returns no rows when yfinance raises a ticker-missing class (r34d, merged `b535f41cb8`) OR a curl_cffi HTTPError with status 404 on THIS symbol's quoteSummary URL (merged cell AR-g-125, `5e7fe11fc8`); every other exception is re-raised unchanged |
| `reports/resident_bindings.json` | changed | only `provenance.package_pin` (the verifier proves no other key moved) |
| `SHA256SUMS` | changed | the package sums, replaced |

**Artifacts** (staged outside the repository; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34e.tar.gz`: sha256 `a96fbfb74db2caf6ad55d93ab35c3b7dd419cf54f4a4dba444bb3268e68e9227`, 1,121,099 bytes, 314 members.
- Package sums `irpt-resident-0485393f3a-r34e.package.SHA256SUMS`: sha256 `faa98a0a872f7b85cff533dfe2a2f4a8cd2a5277c2a724a3fb77fc97fa8d9df1`.
- Host install script `resident_host_install_0485393f3a-r34e.sh`: sha256 `5b73c2fa57c5fd20d2a422435c0bf75ae67c835b20ef1650a5df2f02022c8a23`; `install_r34.sh` `7d2886e3ab43d3eaf9f98dbcc5f3d911b221e0926caa549c28a2558171856ad0`; `pre_read_r34.sh` `a21079c9b4c727a1b19a55f7e701f2a13043793166e90d69b3f8444730dc08e6`; `rollback_r34.sh` `3f7cc764ef170dabec84fb755cb2311073ec44138d5c521efb0853b28c8d53be`.
- V2 script `v2_service_env_r34e.sh` (in the repository at `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`): sha256 `32d52a15e6c12198f6d328a3a9b859bd68a55c8b28368902e90ece61534d5ea6`.
- The capture library, wrapper and every other member are unchanged.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34c) | AFTER (r34e) |
|---|---|---|
| a symbol the provider omits and Yahoo answers 404 on its quoteSummary URL (the door, every upload; ZQXWVK in the probe) | CHECK_FAILED: "could not be checked just now", `REPLACE_FILE` only (the cause of the run-3 hold) | NOT_KEPT: stays NOT_FOUND, so the filer's Replace and No branches are offered (PRD v0.19) |
| a symbol yfinance knows | KEPT | KEPT (unchanged) |
| a rate limit (HTTP 401, 403, 429; `YFRateLimitError`), any other HTTP status (500, 503), a connection or DNS error, a timeout, any other exception | CHECK_FAILED | CHECK_FAILED (unchanged; the verifier's guard arms and the unit tests assert it with curl_cffi 0.13.0's real classes: an outage never reads as "ticker does not exist") |
| a 404 on another symbol's quoteSummary URL, on the chart endpoint, on another host, with no URL or no response object, or a lookalike `HTTPError` from another module | CHECK_FAILED | CHECK_FAILED (unchanged: the rule is an `HTTPError` whose module starts with `curl_cffi`, status 404, a `*.finance.yahoo.com` host and a path ending `quoteSummary/<THIS SYMBOL>`) |
| the swap pass, the pool, the hop_failure writers, pricing, the producer list, the map selection | -- | unchanged (the other 311 members are byte-identical to r34c) |

**Known limit (named, not a stop; the CTO accepts the Yahoo-wide-404 risk as named, msg 9354).** If Yahoo answered 404 on the quoteSummary URL for every symbol (an endpoint change), every unknown-to-the-provider symbol would read NOT_KEPT instead of CHECK_FAILED and be offered Replace or No rather than "try again"; V2's SPY control would catch it at install. A transient 404 for a real symbol reads the same way. The hidden-error-frame path (no raise) is untouched and stays CHECK_FAILED.

**Writers counted.** `intake/yfinance_check.py`: ONE writer (the builder, for this release). The package sums: ONE (the builder).

## 3. Apply protocol, in this order

1. Both halves at HEAD naming this file's blob. The ledger `irpt-resident-r34e-20261016` is opened first; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT** (the r34c first install was sent as the operator's shell user and failed on ownership; `systemd-run` also needs root). Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34c`, exit 40; the r34e root absent; the library and wrapper unmoved; `intake/yfinance_check.py` at its r34c value; the queue 0/0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM` (exits 31 and 33; dry-run: unchanged copy rc 0, one byte changed rc 31 and 33); it then runs the host script, which stages the tar, checks 3 members, keeps the r34c root and the library, installs, polls, and ROLLS BACK ITSELF to r34c on a failed start.
4. V1: running root `0485393f3a-r34e`; the 3 members at their built value; the package sums 313 of 313 OK; the imports; queue 0/0; no sign-in in the journal.
5. **V2, INSIDE the service's own environment** (CTO msgs 9291 and 9354): `v2_service_env_r34e.sh`, sha256 `32d52a15e6c12198f6d328a3a9b859bd68a55c8b28368902e90ece61534d5ea6` (verify before sending). It reads the unit's User, WorkingDirectory, Environment and interpreter, runs the root's own `intake/yfinance_check.py` with the default history port in a transient unit with those properties, and prints `V2S OK SPY KEPT and ZQXWVK NOT_KEPT` only when SPY reads KEPT (HISTORY_ROWS), ZQXWVK reads NOT_KEPT (NO_ROWS) AND four in-service controls pass (`V2S CONTROLS OK 4 of 4`; no Yahoo call: the real `default_history` path with `Ticker.history` replaced by a function that raises the host's REAL curl_cffi HTTPError, built as `raise_for_status` builds it): a 404 on its own symbol's quoteSummary URL must read NOT_KEPT, and a 429 on that URL (PUSHBACK), a 404 on another symbol's quoteSummary URL and a 404 on the chart endpoint must STAY CHECK_FAILED (EXCEPTION), so the in-service proof shows both sides (`~Y2` msg 9365). Two Yahoo calls (plus one per symbol that reads CHECK_FAILED, to print the class), no write, no job, no queue message. On any CHECK_FAILED it prints the exception's module, name, MRO, HTTP status and the response URL without its query. Offline test of the script against the real curl_cffi classes: 14 cases pass, including the checker without the 404 rule reading CHECK_FAILED (V2S FAIL, with the class named).
6. **Gate:** anything but `V2S OK` (or an install that did not print its success line): send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34c`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2.

**Live proof is a separate act** (FWD-1 run 3 under `~Y2`, once this ledger reads CLOSED and the CTO releases the hold).

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34c`, which stays on the host.
- **The receipt:** the r34c receipt is kept by the install and copied back.
- **The library:** unchanged bytes before and after.
- **Queued messages:** none are touched; a job picked up after a rollback is served by r34c (whose door reads an unknown symbol as CHECK_FAILED, the state run 3 is held on).

## 5. Not claimed

- That Yahoo answers 404 on quoteSummary for every symbol it lacks, or that a transient 404 cannot happen for a real symbol (V2 reads SPY and one nonsense symbol; the probe read one).
- That the service process itself (not a transient unit with its properties) has run the fixed checker: run 3 does.
- The live host, S3 objects, running root and receipt were NOT read (this is a build record).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-16, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34e`); the receipt and its r34c copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO

(not signed)
