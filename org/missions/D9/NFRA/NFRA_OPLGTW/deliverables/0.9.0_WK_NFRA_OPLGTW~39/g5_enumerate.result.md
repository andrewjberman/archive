# OG-en-1 -- list-only run for the Tax SMA master 08403355, beside its control 08335338

Box: `i-0f3d57a97f14727af` (SI2). Window searched by both runs (one wide search, default 30-day lookback): 2026-09-08..2026-10-08.
Mode `enumerate` only: no download, no S3 write, no `-SnsTopicArn`. Two vendor list requests, one per master, run one after the other.

Box-side copy (never the installed file): `C:\schwab-sdd\og-g5\sdd-enumerate-g5.ps1`, pulled from the S3 code object
(MD5 on the box before edit `0017f9b549ca9f8013704f50c4327bed` = the ETag), two `-replace` edits, each matched once, 569 lines
(original 568), SHA-256 `333a3e09d406fa5e25b95033f33e0c3296d11903fb757660c45f2ed64a441ad1` on both runs:

- (a) `[Parameter(Mandatory=$true)][ValidateSet('08242234','08335338','08403355')][string]$Master,`
- (b) `$plan | ForEach-Object { Log ("  FILE " + $_.phys) }` (inside the enumerate block)

Run task `OpalOgG5Enumerate-<master>` as Administrator /IT /RL HIGHEST (the monolith-daily-schedule.tf pattern); it started, ran,
LastTaskResult 0, and was unregistered (`TASK_UNREGISTERED=True` both runs). After the second run `C:\schwab-sdd\og-g5\` was
deleted (`COPY_DELETED=True`).

| | 08403355 (Tax SMA) | 08335338 (control) |
|---|---|---|
| SSM command id | `22e138b8-907f-4694-87d4-a43ea7610b20` | `5ca67e2b-e63e-43b5-9eb9-e3849b58c963` |
| started (UTC) | 2026-10-08T23:24:12Z | 2026-10-08T23:27:41Z |
| puller exit (LastTaskResult) / SSM status | 0 / Success | 0 / Success |
| ENUMERATED (distinct files) | 226 | 248 |
| types | 13 | 14 |
| outcome | FILES | FILES |

Per type (files over the window):

| type | 08403355 | 08335338 |
|---|---|---|
| acc | 22 | 22 |
| rld | 22 | 22 |
| rly | 1 | 1 |
| rps | 22 | 22 |
| rty | 1 | 1 |
| sec | 22 | 22 |
| slm | -- | 22 |
| tcfx | 22 | 22 |
| tnn | 4 | 4 |
| trn | 22 | 22 |
| uln | 22 | 22 |
| ult | 22 | 22 |
| upn | 22 | 22 |
| upt | 22 | 22 |

Vendor filename grammar (read from the per-file lines of each run's own log; counts per shape):

- 08403355: `{master}.CRS{YYYYMMDD}.{TYPE}.zip` for all 226 files.
- 08335338: `{master}.CRS{YYYYMMDD}.{TYPE}.zip` for 226 files and `{master}.CS{MMDDYY}.{TYPE}.zip` for the 22 `slm` files.

## Verdict on "the same shape"

- The master `08403355` IS returned to the box's login: 226 files over a window with 22 trading days. The "not entitled" outcome
  (`Die 2`, zero files) did not occur, so no Schwab-side fix is indicated by this run.
- Type set: the 13 types of `08403355` are all in the control with identical counts per type (22 each, `rly`/`rty` 1, `tnn` 4).
  The control has one more type, `slm` (22 files), absent from `08403355` over this window: `types_only_in_08403355` = [],
  `types_only_in_08335338` = [`slm`]. This run does not say whether `slm` is never published for the Tax SMA or simply not in the
  last 30 days; it is the only difference.
- Grammar: the shared 13 types use the same `CRS{YYYYMMDD}` grammar in both. The control's second grammar `CS{MMDDYY}` appears
  only on its `slm` files. Strict set equality of grammars is therefore `false` (`grammar_equal`), and the difference is exactly the
  one type that is missing.
- Date range in the per-type lines: `acc, rld, rps, sec, tcfx, trn, uln, ult, upn, upt` 20260908..20261007 on both masters; `tnn`
  20260914..20260925 on both. The `rly`/`rty` lines print `2..0` for their single file (a display defect in the puller's summary,
  row W39-S2); the physical names are in the box log.

## What was left on the box

Nothing scheduled and no copy. The puller itself created `C:\schwab-sdd\daily\08403355\` with its `daily-pull.log` (247 lines), and an
enumerate run exits without releasing the box-wide session lock (the control run logged reclaiming the first run's lock as stale);
see rows W39-S1 and W39-S3. The full per-file list for each run is in that master's `daily-pull.log` on the box.

Evidence saved here: `ssm_invocation_08403355.json`, `ssm_invocation_08335338.json` (the two get-command-invocation reads).
