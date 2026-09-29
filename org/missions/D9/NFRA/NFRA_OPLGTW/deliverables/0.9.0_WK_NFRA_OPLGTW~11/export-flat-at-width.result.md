# OG-x-4 result -- the R-4 remedy: export memory flat at full width (0.9.0_WK_NFRA_OPLGTW~11)

Release `63264dfb22cf6e6b6acdab30d7086736686e1be9` (branch rel-nfra-oplgtw-export-flat, LOCAL) = the live release `4248b70b39` + only
OG-x-4's gateway files (`schwab/engine.py`, `tests/test_schwab_engine.py`, `tests/test_schwab_export_stream.py`; `onhost_bench.py`
is not on the live tree and is not shipped in the artifact, so it is left out). `deploy-to-ec2.sh` unchanged (its
`ENABLED_INTEGRATIONS` line = the host's). Deployed to `i-07dccb1615503ac99` by `safe-ec2-deploy.sh`, ssm
`ef0a8f2c-f268-4536-91f2-3dae19d6c4ce`, restart 2026-09-29 08:43:42 UTC. Override use: 1
(`GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~11`, the release commit only).

## The four causes of memory that followed rows (measured in PHASE A, local; see ANNOUNCE_OG-x-4.md)
1. **The input was resident whole (H1).** `_plan_job` read every source object into Arrow and registered the result as `src`;
   about 57 MiB of resident input at 250,000 rows x 11 columns (33.5 MiB of Arrow tables cost 92 MiB of RSS).
2. **The maximal query held the same whole input (H3).** Old engine 271,347,712 bytes (101.1 percent of the cap, refused); the 500-row page
   result was never the cost.
3. **A DuckDB working set sized for a query, not an export** (64 / 128 MiB): the sort held all rows in memory instead of spilling.
4. **(H4, found in PHASE A, not in the order) the export statement's `LIMIT cap+1` is a non-spillable top-N heap.** Over `ORDER BY`
   DuckDB plans a top-N whose heap holds up to 250,001 rows in memory; it caused DuckDB's out-of-memory at 250,000 x 11 columns,
   and made any small working set impossible.
Refuted: H2 (a second copy in `_read_source`): `pa.concat_tables` is zero-copy (RSS 186 MiB before and after).
The fix: DuckDB scans the job's Parquet objects itself (`allowed_paths` = the source list, external access off, configuration locked,
policy a semi-join inside the `src` view); the export drops its LIMIT (the count-before-fetch refusal guarantees rows <= cap); rows-mode
exports take a 16 MiB working set (aggregate exports 64 MiB, measured necessary).

## Release checks (bound 4)
- **Census:** 110 worktrees (48 distinct sentinel blobs at HEAD, plus a working-directory scan of every tree): no gateway sentinel open except the
  superseded `nfra-oplgtw-og-r-1-first-release` slug. Two trees appeared during the run (`ae-og-g1c`, `wk-hvst-r15-41`); neither carries one.
- **Live base by content:** host 76 of 76 files = `4248b70b39`'s tree (CLOUD manifest `deployed_commit` 4248b70b39; service unrestarted since
  05:22:10Z); `.env` 27 keys; `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index`; 51 tools.
- **Tests on the release tree:** engine 14, export 27, query 26, export_stream 3 (incl. `test_ogx4_ac03`): 70 passed, 0 failed.
- **Rollback proven before the act:** `/c/tmp/og-x4-rb` at `4248b70b39`, mcportal `a3bff71ffa`; rebuild 79 files vs the live artifact
  `opal-gateway-4248b70b39.tar.gz` (406,162 bytes): `diff -rq` empty, 79 of 79 identical.
- **Ledger** `nfra-oplgtw-export-flat-release`: opened and committed with its sentinel BEFORE the act (`ae9d32396b`), closed
  (`46c5e45f8e`), 4 of 4 legs proven.
- **Verify:** read-only SSM 08:45:17Z to 08:45:40Z: `/health` 200; `engine.py` md5 `42445b377079d741f78c7dd1fb3fc41e` = the release's bytes; 76-file
  host manifest = the release tree 76 of 76 (only `schwab/engine.py` changed); tools AFTER = BEFORE (51, sorted diff empty);
  `ENABLED_INTEGRATIONS` unchanged and without `schwab`; 27 `.env` keys. **The read began 95 s after the restart, five seconds outside the
  order's 90 s** (the wrapper's own install steps ran first); nothing failed, so no rollback.
- **Manifest:** the wrapper's own record was refused at the naming limb (LGIC_ENFORCE) and left a whole-file CRLF rewrite unstaged in the release
  tree, which is not used; recorded by hand on an LF copy (`a13797a324`, 5 lines): `deployed_commit` 63264dfb22, `previous_deployed_commit`
  `4248b70b39` (the committed release the live tree equalled).

## The on-host re-measure (`CAPACITY_X4.json`; onhost_bench.py --scale full, 2026-09-29T08:50:54Z..08:51:30Z, 36.0 s, served release 63264dfb22)
Served code confirmed by md5 in the same SSM command: `engine.py` 42445b37... = 63264dfb22; `integration.py` f436630c..., `export.py` c9943e78... = 4248b70b39.
| job | outcome | peak child RSS (bytes) | ratio to the 25k peak |
|---|---|---|---|
| export 25,000 x 11 columns | ok, csv 3,748,900 B, 2.5 s | 161,800,192 | 1.0000 |
| export 125,000 x 11 columns | ok, csv 18,743,499 B, 8.1 s | 177,328,128 | 1.0960 |
| export 250,000 x 11 columns | ok, csv 37,488,002 B, 15.2 s total (engine job 2.0 s), files gone | 175,976,448 | 1.0876 |
| maximal query | ok | 151,691,264 (56.5 percent of the cap; bar 214,748,364) | |
| concurrent pair | ok | 144,924,672 / 144,822,272 | |
Verdict SUFFICIENT: no job exceeds the cap (max peak 177,328,128 vs 268,435,456), deadlines respected, the contract-scale export completes in 15.2 s
(bar 30 s), admission gap 0 (nothing overshoots). OG-r-3 measured on the same host: 172 / 225 / refused at 272.7 MB, maximal 286.7 MB.
**Thin margin, stated:** the 125,000-row peak is 1.0960 of the 25,000-row peak against a bound of 1.10. A second full run on the same host and
code read tenth / half / full 166,936,576 / 175,747,072 / 177,737,728 (ratios 1.0528 / 1.0647), maximal 151,580,672, all ok, SUFFICIENT.
Not tuned; nothing was changed between the runs. Host scratch removed; service active and unrestarted since 08:43:42Z through both runs.

## Criteria (run as written from the worktree root; details in the proof instance)
AC1 PASS (`export sizes graded 3 of 3`, bound 177,980,211); AC2 PASS (151,691,264 <= 214,748,364); AC3 PASS (`test_ogx4_ac03`, PHASE A: child
1.092, parent 0.966).
## Not measured / carried
`dim_asset` (three free-text columns) was not exported on the host; text-heavy rows-mode exports complete up to the 50 MiB byte cap locally
(144,000 rows x 9 columns x 215-char text) and are refused on memory beyond it. Rows Z-W11-S10 and S11 (OG-r-3) are answered by this measurement:
S10 (capacity INSUFFICIENT at width) now measures SUFFICIENT; S11's admission gap is 0 because no job overshoots the cap.
