# Never-widen sign-off packet -- r34d: the resident r34c -> r34d at pin 11e0751415 (the door checker reads a symbol Yahoo has no data for as NOT_KEPT, not CHECK_FAILED)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-16. **Applier:** `0.7.0_AE_CloudOps~AQ2`.
**Authority:** CTO msg 9283 (hold run 3; diagnose the served checker) and msg 9291 (diagnosis accepted; cut r34d under its own pair, own names; ONLY `YFTickerMissingError` and its subclasses map to no rows; proof is a V2 run in the service's own environment). Diagnosis: AQ2's read-only record `CHECKFAIL_READ.txt` (commit 51686af530) refuted the environment hypotheses; the cause was read from the yfinance 1.2.0 wheel (`scrapers/history.py` lines 98-99, 273-274). **Ledger:** `irpt-resident-r34d-20261016`.
**One move:** D1, the install of one new root on the resident host. One member changes: `intake/yfinance_check.py`. No IAM, Lambda, queue, table or schema moves; no new Yahoo call path (the checker already calls Yahoo for each symbol YCharts omits, bounded as r34c's packet states); `opal_pricing` stays OFF.

## 1. What ships

Package pin `11e0751415c1e811bffd0381d24a7c890ad1f33d`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34d_build.py` over the tools at that pin, BUILD ONLY, over the RUNNING r34c root (tarball sha256 `272d5c543bc7731217f57157afd9817db9ed8906b148977852c9b9b1714d2ff8`). **314 members**: 311 identical to r34c, **3 changed**, 0 added, 0 removed. Two builds under one fixed clock are identical 314 of 314, and the tarball equals the issuer's own earlier build of the same pin. The verifier `ar_g122_checks.py verify` (independent of the builder) recomputed every number below and passed.

| member | vs r34c | what changes |
|---|---|---|
| `intake/yfinance_check.py` | changed (LIVE in the resident's runtime, static import walk) | `default_history` returns no rows when yfinance raises a ticker-missing exception (merged cell AR-g-121, `b535f41cb8`); every other exception is re-raised unchanged |
| `reports/resident_bindings.json` | changed | only `provenance.package_pin` (the verifier proves no other key moved) |
| `SHA256SUMS` | changed | the package sums, replaced |

**Artifacts** (staged outside the repository; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34d.tar.gz`: sha256 `9a088a5cfdeecd84173ee85b82d93ecf2b6fdfa311d3aec982e7db7134cf78ab`, 1,120,240 bytes, 314 members.
- Package sums `irpt-resident-0485393f3a-r34d.package.SHA256SUMS`: sha256 `9220275ac25a6fe252b7cbc5e8d00171242e4b13d5a35f686322edd8cee688a8`.
- Host install script `resident_host_install_0485393f3a-r34d.sh`: sha256 `1a9e6c44ef32efaee3b95633f2d54cdc03d9817aba32bde17eed9f68b942cf49`; `install_r34.sh` `6644430f68b18fb400467d347a4e279323f91f2ea2fc8462a95f98fe48e5054f`; `pre_read_r34.sh` `7769f3733e82b3f711569f2b7625094bd137cce5f4d2bb82256f7204f1699e56`; `rollback_r34.sh` `56a484adf173a17b1be5e698c12f1bcfe63783a947b29c35116a75a5e13424f6`.
- V2 script `v2_service_env_r34d.sh` (in the repository at `org/tier1_exec/2.0.0_SA_COO~G2/deliverables/r34/`): sha256 `90802b18a174414353387c0595fc8beae414399d82042ec9ab973df699ab7940`.
- The capture library, wrapper and every other member are unchanged.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r34c) | AFTER (r34d) |
|---|---|---|
| a symbol the provider omits and yfinance has no data for (the door, every upload) | CHECK_FAILED: "could not be checked just now", `REPLACE_FILE` only (the cause of the run-3 hold) | NOT_KEPT: stays NOT_FOUND, so the filer's Replace and No branches are offered (PRD v0.19) |
| a symbol yfinance knows | KEPT | KEPT (unchanged) |
| a rate limit (HTTP 401, 403, 429; `YFRateLimitError`), a connection error, a timeout, any other exception | CHECK_FAILED | CHECK_FAILED (unchanged; the verifier's guard arms and the unit tests assert it: an outage never reads as "ticker does not exist") |
| a class merely NAMED like the yfinance one | -- | not matched: the rule is the exact class name `YFTickerMissingError` anywhere in the exception's MRO |
| the swap pass, the pool, the hop_failure writers, pricing, the producer list, the map selection | -- | unchanged (the other 311 members are byte-identical to r34c) |

**Known limit (named, not a stop; the CTO accepts the class as the line, msg 9291).** A transient Yahoo "no price data" for a real symbol raises the same class and now reads NOT_KEPT instead of CHECK_FAILED; the symbol is then offered Replace or No rather than "try again". The hidden-error-frame path (no raise) is untouched and stays CHECK_FAILED.

**Writers counted.** `intake/yfinance_check.py`: ONE writer (the builder, for this release). The package sums: ONE (the builder).

## 3. Apply protocol, in this order

1. Both halves at HEAD naming this file's blob. The ledger `irpt-resident-r34d-20261016` is opened first; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the resident host, the unit or its root is a STOP).
2. **Send every host script AS ROOT** (the r34c first install was sent as the operator's shell user and failed on ownership; `systemd-run` also needs root). Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r34c`, exit 40; the r34d root absent; the library and wrapper unmoved; `intake/yfinance_check.py` at its r34c value; the queue 0/0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM` (exits 31 and 33; dry-run: unchanged copy rc 0, one byte changed rc 31 and 33); it then runs the host script, which stages the tar, checks 3 members, keeps the r34c root and the library, installs, polls, and ROLLS BACK ITSELF to r34c on a failed start.
4. V1: running root `0485393f3a-r34d`; the 3 members at their built value; the package sums 313 of 313 OK; the imports; queue 0/0; no sign-in in the journal.
5. **V2, INSIDE the service's own environment** (CTO msg 9291): `v2_service_env_r34d.sh`, sha256 `90802b18a174414353387c0595fc8beae414399d82042ec9ab973df699ab7940` (verify before sending). It reads the unit's User, WorkingDirectory, Environment and interpreter, runs the root's own `intake/yfinance_check.py` with the default history port in a transient unit with those properties, and prints `V2S OK SPY KEPT and ZQXWVK NOT_KEPT` only when SPY reads KEPT (HISTORY_ROWS) and ZQXWVK reads NOT_KEPT (NO_ROWS). Two Yahoo calls, no write, no job, no queue message. Offline test of the script: 8 cases pass, including the pre-fix checker reading CHECK_FAILED (V2S FAIL).
6. **Gate:** anything but `V2S OK` (or an install that did not print its success line): send `rollback_r34.sh` AS ROOT the same session, read the running root back as `0485393f3a-r34c`, close the ledger ROLLED-BACK, report. No retry.
7. The ledger closes at V2.

**Live proof is a separate act** (FWD-1 run 3 under `~Y2`, once this ledger reads CLOSED and the CTO releases the hold).

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r34c`, which stays on the host.
- **The receipt:** the r34c receipt is kept by the install and copied back.
- **The library:** unchanged bytes before and after.
- **Queued messages:** none are touched; a job picked up after a rollback is served by r34c (whose door reads an unknown symbol as CHECK_FAILED, the state run 3 is held on).

## 5. Not claimed

- That Yahoo raises `YFTickerMissingError` for every symbol it lacks, or that a transient "no price data" cannot raise it for a real symbol (V2 reads SPY and one nonsense symbol).
- That the service process itself (not a transient unit with its properties) has run the fixed checker: run 3 does.
- The live host, S3 objects, running root and receipt were NOT read (this is a build record).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-16, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34d`); the receipt and its r34c copy; the unit's ExecStart; the kept library copy; one transient systemd unit for V2. The blast radius is section 2; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO

(not signed)
