# Readers of the returns manifest (TO-DB-b-119) -- condition 1 of the CTO half on the R45 apply

Object: `manifest.json` beside each `date=` partition of gold `account_return_daily`. R45 adds `valuation_source`, `fee_treatment`, `price_basis`.
Record: `RETURNS_MANIFEST_READERS.json` (same folder). No account number or client figure appears here.

**reader_count = 10. verdict = NO_STRICT_READER.** Nine of the ten are not on a deploy path; the one production reader reads one named key.

| # | file:line | what it is | unknown key | evidence |
|---|---|---|---|---|
| 1 | data/assets/scripts/gold/irpt_custody/client_report_figures.py:676 | production: client-report figures builder | ACCEPTS | `(manifest or {}).get("first_data_date")` |
| 2 | same file :1304 | its own self-test fixture | ACCEPTS | sets one account key, writes the dict back |
| 3 | data/assets/scripts/gold/irpt_custody/tests/test_si_anchor.py:67 | test, fixture manifest | ACCEPTS | `manifest["first_data_date"].update(first)` |
| 4 | data/assets/scripts/silver/commonwealth_account_return_daily.py:425 | adapter read-back of local day manifests | ACCEPTS | `back.get(...)` named keys |
| 5 | same file :427 | sample day, dict passed through | ACCEPTS | `"sample_day_manifest": sample` |
| 6 | same file :437 | version count | ACCEPTS | `back.get("method_version") == 3` |
| 7 | .../2.0.0_SA_COO~P/p2_window/p2_backfill_driver.py:61 | one-time operator driver, reads the served object | ACCEPTS | `m.get("method_version") != 2 or m.get("rows") ...` |
| 8 | .../0.9.0_WK_IRPT_DASHBD~88/manifest_probe.py:45 | measurement script | ACCEPTS | `m.get(f, "<key not in the manifest>")` |
| 9 | .../0.9.0_WK_IRPT_DASHBD~92/manifest_probe.py:45 | same code | ACCEPTS | `f in m` |
| 10 | .../0.9.0_WK_IRPT_DASHBD~92/manifest_compare.py:70 | the packet's Manifest comparison | ACCEPTS | an extra key grades ADDED, not a refusal |

STRICT: none. NOT_ESTABLISHED: none. Gates at deploy: none of the ten is a deploy gate that I read; the test row (3) is a fixture reader and I did not read what CI runs, so that one is stated "not established".

## Scopes and denominators

| scope | files scanned | positive control |
|---|---|---|
| repo, comp-find corpus all, `account_return_daily` | 68,664 | hits the producer and both investor-reporting handlers |
| repo, `manifest` over gold, silver, investor-reporting lambdas, tieout, K2 folder | 1,006 | hits `build_manifest` |
| repo, `manifest\.json` over data, infra/aws/lambda, .tools, lib | 8,752 | hits the writer and reader #1 |
| repo, project scripts and org/standards | 626 | hits readers #7 and #10 |
| portal checkout (`C:/dev/ajb_workspace/portal` @dbeb6764; the worktree copy is empty) | 2,069 | `account_return_daily` 2 files (comments), `manifest.json` 36 files, none the gold object |
| opal_ai checkout (`C:/dev/ajb_workspace/opal_ai` @de5ce25; the worktree copy is empty) | 36 | `manifest.json` 3 files; `account_return_daily` 0 |
| mcportal | ABSENT | an empty directory in both trees; not a zero |

## Not counted, and why

The platinum per-account manifest (`reporting-publish`, read by the portal's `seriesContract.ts`) is a different object built from the series; the publish handler reads the gold parquet, never this manifest. Writer-side tests index the dict `build_manifest` returns and pin values, not a closed key set. `a_reads.py` reads the activity and class tables' manifests.

## What this does not see

A reader outside these scopes (a notebook, a script outside the repo, a cache). No reader validates against a closed key set; `org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json` does not describe the manifest.
