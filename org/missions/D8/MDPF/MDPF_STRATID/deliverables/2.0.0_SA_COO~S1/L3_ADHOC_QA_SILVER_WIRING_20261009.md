# MDPF_STRATID W2 -- ad-hoc QA ahead of ledger `mdpf-stratid-w2-wiring-silver` L3 (2026-10-09 ~15:5xZ)

Run by `2.0.0_SA_COO~S1`. This is a test ahead of the scheduled run. The scheduled run stays the acceptance: L3 stays OPEN until the
runner's next dispatch executes the deployed code.
- **Next dispatch:** `mdpf-feeder-backstop-daily`, `cron(52 12 * * ? *)` UTC, to `mdpf-feeder-trigger`, then the runner's
  `mdpf-daily-dispatch.sh` step 6d.
- **Not a dispatch:** `mdpf-accrual-bridge-daily` (13:40Z) does not run the Cottonwood slice.

## The run (in memory, DRY-RUN, nothing written)

- **Code:** the DEPLOYED silver bytes, downloaded from `s3://opal-data-mdpf/code/scripts/silver/`:
  - `rebalancer_schemas.py`, 15,970 B;
  - `opal_strategy_matcher.py`, 4,296 B.

  Both were first on `sys.path` (`rebalancer_schemas from <tmp>/silver`). The gold slice `build_cottonwood_mdpf_slice.py` came from
  the repo.
- **Instrument:** `build_composed(s3)` against live S3, compared with the served slice
  `s3://opal-data-assets/gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json`:
  - VersionId `ti203WCyH5lJ3BKMOKBZM_uSn8aPY.fr`;
  - LastModified 2026-10-09T13:31:12Z.

## Read

| Check | Result |
|---|---|
| Slice gates | `GATES PASS` (absent-is-not-zero, strict-Opal filter, conservation, W-2b identity) |
| `STRATEGY_CONFIG_SOURCE` | `s3://opal-data-etfs/config/etf_universe.json` (the S3 list, not a fallback) |
| `by_model` keys | QA 16, served 16; only-QA [], only-served [] |
| Last date | QA 2026-10-08, served 2026-10-08 |
| `model_value` differences on 2026-10-08 | 0 |
| PFDE | 410,420.98 (= the Global PFDE node, `FWD1_SEAT_WALK_GLOBAL_VIEW_20261009.md`) |
| Verdict | `L3-QA PASS` |

The deployed wiring reads the S3 list and serves the same strategy members and figures as the pre-wiring code's 13:31Z run.

Driver: session scratch `l3qa_run.py`, not committed; this page records the instrument.
