# Never-widen sign-off packet -- r34: the resident r32 -> r34 at pin bc9f2d0c44 (the swap pass, the dated pool snapshot, the yfinance checker at the door and the hop_failure writers)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~G2`, 2026-10-16. **Applier:** a CloudOps seat named by the CTO.
**Authority:** CTO msgs 8907 and 8971 (C-HOP-FAILURE: the resident writers of `hop_failure`, folded into this release), CTO msg 8968 (the door's yfinance checker, folded into this release; ruling on `~Y2` msg 8965, row `IRPT_ANLREQ-D2-W165-S2`), CTO msgs 8693, 8711, 8714, 8723 (the swap: an UNRESOLVED holding is replaced in the Opal producer by a class-matched, Yahoo-priced security from a
dated pool), msg 8863 ("r34 is next"), PRD v0.19 (C-SWAP steps 1 and 2; step 3, the classifier, is its own cell after run 3). **Ledger:** `irpt-resident-r34b-20261016`.
**One move:** D1, the install of one new root on the resident host. No IAM, Lambda, queue, table or schema moves. **Two new Yahoo call paths:** the door's checker asks Yahoo for one month of history per symbol YCharts omits (section 2c), and the swap pass asks Yahoo
(through the `yfinance` library, whose presence on the host V2 reads) for monthly history of pool candidates; section 2b states the calls per holding and their bound. `opal_pricing` stays OFF.

## 1. What ships

Package pin `bc9f2d0c44ab320f43a62951bc77d438790dd5a5`; base pin `0485393f3ad0a7e564f4867f5e70003e2e62195b`; built by `r34_build.py` over the tools at that pin, BUILD ONLY. **314 members**: 300 identical to r32, **10 changed**
(including `SHA256SUMS` and the bindings), **4 added**, 0 removed. Two builds under one fixed clock are identical 314 of 314, and the tarball equals
the issuer's own earlier build of the same pin. The verifier `ar_g107_checks.py verify` (independent of the builder) recomputed every number below and passed.

| member | vs r32 | in the resident's runtime (static import walk) |
|---|---|---|
| `intake/portfolio.py` | changed | LIVE |
| `intake/uploads.py` | changed | LIVE |
| `ops/status.py` | changed | not reachable |
| `reports/resident_bindings.json` | changed | not reachable |
| `reports/resident_installed.py` | changed | LIVE |
| `ycharts/generate/durable_job.py` | changed | LIVE |
| `ycharts/generate/resident_worker.py` | changed | LIVE |
| `ycharts/research/opal_producer.py` | changed | LIVE |
| `ycharts/session/resident_session.py` | changed | LIVE |
| `intake/yfinance_check.py` | ADDED | LIVE |
| `ycharts/research/swap_pass.py` | ADDED | LIVE |
| `ycharts/research/swap_pool.json` | ADDED | not reachable |
| `ycharts/research/yahoo_history_days.py` | ADDED | LIVE |

Reachable modules: 78 in r34, 74 in r32. Compiled: 130 of 130 Python members.

**The bindings** gain ONE key, `opal_swap_pool` = `{path: ../ycharts/research/swap_pool.json, sha256: bf047533f63e083f969fb776bcea375b878970554f43f92565734953d6818ccb}`, pinned by content and verified by the installer's own loader
at every job; the provenance block changes; every other key is unchanged (pricing still OFF).

**The pool snapshot** `swap_pool.json`: schema `irpt-swap-pool.v1`, claim `held`, as of 2026-10-16, 4419 rows in 37 classes (largest 1229). It is the
committed output of the AQ2 read of the `etf-classifications` table (`dcdc6cb3d1`), shipped inside the package, not read from AWS at run time.

**Artifacts** (staged outside the repository; nothing uploaded):
- Tar `irpt-resident-0485393f3a-r34c.tar.gz`: sha256 `272d5c543bc7731217f57157afd9817db9ed8906b148977852c9b9b1714d2ff8`, 1,119,932 bytes, 314 members.
- Package sums `irpt-resident-0485393f3a-r34c.package.SHA256SUMS`: sha256 `55d48fb64c5305007d40ba8fa55130c720a55e1c1b8fb20da6d06dfdf5246a1f`.
- Host install script `resident_host_install_0485393f3a-r34c.sh`: sha256 `c7d165d84795da5e079584c557b14dea253b389446b6bc43840942656ed4ad27`; `install_r34.sh` `c50dc2018e64ebea304df0f07a75aa83fd83cf784fc18b6babf35c2f683d8af9`; `pre_read_r34.sh` `3fa249488c04de335dc7eada0c787a862e5f063485164eb57b446164b01dc1a7`; `rollback_r34.sh` `beee07c483d576523b10aee5610a36f44378fff045e99ba731cbff1867c16380`.
- The capture library and wrapper are unchanged.

## 2. Blast radius, by branch (read from the code at the pin)

| what | BEFORE (r32) | AFTER (r34) |
|---|---|---|
| an Opal job whose holdings carry no UNRESOLVED row | runs | the same (the swap stage is skipped; the pool is still read and checked at the start of every Opal job) |
| an Opal job with an UNRESOLVED holding | the read refuses (an unresolved row is not admitted) | each UNRESOLVED row is replaced by the pool candidate of its class with the longest Yahoo monthly history (ties: the alphabetically first), the amount KEPT; a replacement already held is MERGED into that row |
| the SAME job, a ticker the pool does not hold in exactly one class | -- | NOT swapped and left out; the disclosure reads "SYM is not analysed; Opal Staff will manage the replacement." |
| a job whose every holding is left out | -- | refused `NO_ANALYSABLE_HOLDINGS` |
| a swap | -- | one `SWAP` disclosure per row, ahead of every other disclosure; `run_doc.swaps` names the pool vintage and holds NO amount; `settings.swap` carries pool date, claim, stale flag, swapped and left-out counts |
| a pool older than 30 days at the run date | -- | the swap still runs; each disclosure says the pool is older than 30 days (this pool turns stale after 2026-11-15) |
| a damaged, absent or altered pool file | -- | EVERY Opal job refuses (`PINNED_FILE_ABSENT` / `PINNED_FILE_DIFFERS` / a `POOL_*` code); the file is pinned by sha256 in the bindings and in the package sums |
| the door tree (`intake/portfolio.py`, `intake/uploads.py`, `ops/status.py`) | r32 bytes | the bytes the Lambdas carry (`portfolio.py` and `uploads.py` at the r33 pin, `status.py` at the r35L pin: the same blobs, checked by the generator); the resident's static walk reaches `portfolio.py` and `uploads.py`, not `status.py` |
| a symbol YCharts omits and the registry does not resolve (the door, every upload) | filed TICKER_NOT_FOUND with Replace and No offered | sent to the yfinance checker in ONE batch: KEPT when yfinance returns rows with a finite positive last close (no Replace or No; priced from yfinance), NOT_KEPT stays NOT_FOUND, a failed or pushed-back check reads UNAVAILABLE `YFINANCE_CHECK_FAILED`, never absence; a missing `yfinance` library reads as a failed check |
| a ready-signal send that fails (the commentary step is not told the analysis is ready) | a journal line only; the job stays READY | the same line, plus ONE write on that job's row: `hop_failure` = `{hop READY_SIGNAL, code READY_SIGNAL_SEND_FAILED, at}` (set-once: a second failure is a no-op) |
| a commentary-ready message the packager refuses or fails on | refusal logged and message deleted, or the error raised and the message retried | the same, plus ONE set-once write `hop_failure` = `{hop PACKAGER, code PACKAGER_REFUSED or PACKAGER_FAILED, at}`; the packager's own error is re-raised unchanged and a failing write is swallowed and journalled |
| the job row's state, receipt and `i3_sent_at` | -- | untouched by either write (the write names only the `hop_failure` attribute, conditional on it not existing) |
| pricing, the producer list, the map selection, the capture library | -- | unchanged |

**The class of the missing ticker.** The resident wires NO classifier store: the swap knows a ticker's class only when the pool holds that ticker in exactly one class. An
UNRESOLVED ticker the pool does not hold is left out. That is the C-SWAP step 3 gap (the model classifier is its own cell and pair after run 3). Run 3's candidates carry no
class in the pool, so this release alone does not swap them; it makes the swap real for every UNRESOLVED ticker the pool holds, and it is the release the classifier lands on.

**Writers counted.** The pool file: ONE writer (the builder, for this release). The bindings: ONE (the builder). Swap records: ONE (the producer).

## 2b. Yahoo calls per swapped holding, and their bound

Source: `swap_pass.py` and `yahoo_history_days.py` at the pin (REQUEST_CHUNK = DEFAULT_CHUNK = 50). `[measured from the code and the shipped pool]`

- The swap asks Yahoo for the monthly Close history (`period` max, `interval` 1mo) of EVERY pool candidate in the missing ticker's class, in `yf.download` calls of at most 50 tickers
  (the prefetch). **Calls per swapped holding: at most ceil(class size / 50) download calls** = 25 for the largest class (1229 tickers); 107 if every one of the 37 classes were
  asked once. The history is CACHED for the job: a second holding of the same class asks nothing; a different class asks its own batches.
- `[inferred, library behaviour not read here]` `yfinance` fans one `download` out to one HTTP fetch per ticker, so the number of fetches Yahoo sees per swapped class is the class size
  (up to 1229), not 25. The bound that matters for Yahoo's rate limit is therefore the CLASS SIZE per distinct class per job.
- **Failure branch.** A batch that raises is skipped; its tickers are then asked ONE AT A TIME by the chooser, and a single ticker that raises is dropped as `HISTORY_ERROR` and is NOT
  cached, so a second holding of that class asks it again. With Yahoo fully down this is up to the class size of single calls per holding (1229 for the largest class) before the pick ends
  `NONE_PRICED` and the holding is left out with the not-analysed disclosure. A failed request never reads as "unpriced" in a way that picks a wrong replacement.
- The job's other work (the BBG/estate history, the existing yfinance price adapter) is unchanged and unreachable while pricing is off.
- The host check at V2 makes ONE `yf.download` call for ONE ticker and ONE checker call (`YfinanceChecker().check` of one ticker), to read that the host can reach Yahoo through the installed library at all.

## 2c. Yahoo calls by the door's checker, and their bound

Source: `intake/yfinance_check.py` and `security_resolution.py` at the pin. `[measured from the code]`

- Per upload: at most `cap` = 10 symbols are checked, each ONE `yf.Ticker(symbol).history(period="1mo")` call, paced `pace_seconds` = 1.0 apart, so at most 10 calls and about 10 seconds added to that upload's resolve. A symbol beyond the cap reads NOT_CHECKED `BEYOND_CAP` (UNAVAILABLE, never absent).
- A 401, 403 or 429 stops the rest of that batch (`STEP_STOPPED`); the stopped symbols read UNAVAILABLE.
- Only symbols the provider answered NOT_FOUND and the registry did not resolve are checked: a found symbol never reaches Yahoo. The result is cached KEPT for a day only when the resolver has a cache; the resident builds none, so a repeated upload re-asks.
- A missing library raises `CheckerUnavailable`; the resolver reads that as CHECK_FAILED for every symbol of the batch (a configuration fault, not a verdict).

## 2d. The hop_failure writers (C-HOP-FAILURE), and what they need

Source: `durable_job.py` (`mark_hop_failure`, `mark_hop_failure_keyed`, `HOP_FAILURE_CODES`), `resident_worker.py` `send_ready`, `resident_installed.py` `make_packager` at the pin. `[measured from the code]`

- Two writes only, each ONE `UpdateItem` on the `irpt-jobs` row of the request, `SET hop_failure = :value` with the condition that the attribute does not exist, never returning values. The resident host role's declared policy (`resident.tf`, `JobStateAcceptanceAndRetainedIndexes`) grants `dynamodb:UpdateItem` on `irpt-jobs` with no attribute condition `[declared in source; the live policy is read by the apply order's V3 with the simulator]`.
- Dormant until read: nothing reads `hop_failure` until the `irpt-status` reader release (cell `AR-g-111`, applied first) and the commentary writer exist. `mark_hop_failure_keyed` (the commentary hop's form) is in the package but unused by the resident.

## 3. Apply protocol, in this order

1. Both halves at HEAD naming this file's blob, AND the library delivery closed: `yfinance` 1.2.0 and its Linux cp312 closure installed in the host's `pydeps` under its own pair (the first attempt of this release was installed as root `0485393f3a-r34` and ROLLED BACK at V2 because the library was absent; that root, its receipt copy and its three S3 objects are KEPT on purpose, so THIS release has its own names: root `0485393f3a-r34c` and keys `...-r34c.*`; CTO msgs 9066, 9070, 9075, 9114). Without the library V2 stops the install again.
2. Before-read: `pre_read_r34.sh` (fail-closed: the running root must be `0485393f3a-r32`, exit 40; the r34c root absent (the first attempt's r34 root may exist and is not touched); the library and wrapper unmoved; every changed member at its r32 value, every added member ABSENT; the queue 0/0).
3. D1: upload the tar, the sums file and the host script to the keys the install script names (each key must read 404 first; record the S3 versions); `install_r34.sh` fetches the host script and the sums BY KEY and refuses unless their sha256 equal `WANT` / `WANTSUM` (exits 31 and 33, dry-run: unchanged copy rc 0, one byte changed rc 31 and 33); it then runs the host script, which stages the tar, checks 14 members, keeps the r32 root and library, installs, polls, and ROLLS BACK ITSELF to r32 on a failed start.
4. V1: running root `0485393f3a-r34c`; every changed or added member at its built value; the package sums 313 of 313 OK; the imports (`swap_pass`, `yahoo_history_days`, `opal_producer`); the pool file's sha256 equals the binding; queue 0/0; no sign-in in the journal.
5. V3 (read-only): `simulate-principal-policy` for the resident host's role, action `dynamodb:UpdateItem` on the `irpt-jobs` table ARN: expect allowed (the hop_failure writers need it); print the decision. A denial is a STOP before the ledger closes.
6. V2: ONE `yf.download` call for ONE ticker and ONE `YfinanceChecker().check(["SPY"])` call (expect KEPT) through the resident's interpreter (read-only, no job, no queue message); and `swap_pass.load_pool` on the shipped pool with today's date prints the pool date, claim, row count and stale flag.
7. The ledger closes at V2 and V3.

**Live proof is a separate act** (FWD-1 run 3 under `~Y2`).

## 4. Rollback, per key

- **The root:** `rollback_r34.sh` (or the install's own failure branch) restores `0485393f3a-r32`, which stays on the host; its readers are the r32 values of the changed members and ABSENT for the added ones.
- **The receipt:** `cutover_receipt.0485393f3a-r32.json` is kept by the install and copied back.
- **The library:** unchanged bytes before and after.
- **Queued messages:** none are touched; a job picked up after a rollback is served by r32.

## 5. Not claimed

- That the checker has run against a real upload, or that the host has `yfinance` installed (V2 reads it).
- That the swap has run against a real UNRESOLVED upload, or that Yahoo prices any candidate from this host (V2 reads one ticker, not a class).
- That the pool is current beyond its stated date (a held snapshot of 2026-10-16).
- That run 3's candidates are swapped: they need the classifier (C-SWAP step 3).
- The live host, S3 objects, running root and receipt were NOT read (this is a build record).

## COO half -- 2.0.0_SA_COO~G2

SIGNED, 2026-10-16, on this packet's bytes at the commit that carries it. The write set is: one new root directory on the resident host (`/opt/irpt-resident/0485393f3a-r34c`); the receipt
and its r32 copy; the unit's ExecStart; the kept library copy. The blast radius is section 2 and 2b; the rollback is section 4.

## CTO half -- 1.0.0_SA_CTO

(not signed)
