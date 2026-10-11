# MDPF_DEMQUE round 9 -- the standing T-1 extension, first run: receipt (2.0.0_SA_COO~Q1)

Run 2026-10-11 17:18:24Z to 17:48:56Z on dell1: `bash data/mdpf/scripts/demque/run_daily_draw.sh` once, under the t-31 pair (COO half
`NEVER_WIDEN_HALF_REQUEST_DEMQUE_R9_T31_EXTENSION_20261011.md` @b3baaeb04c; CTO half SIGNED `ledger/NEVER_WIDEN_ROUND9_T31_EXTENSION_CTO_HALF.md`,
msg 4028, one condition). Code at box/dell1 `89007f31a2` (t-30/31 `1961d4ee7a`, t-36 `df9aaa34cc`, t-37 `8e63ec0a23`, t-38 `1bb7035580`,
t-39 `89007f31a2`). Exit 0; the day's ledger uploaded
(`s3://opal-data-assets/yahoo/global/bronze/demand_ledger/dt=2026-10-11/ledger.jsonl`).

## Before

Snapshot taken first: `R9_PRE_EXTENSION_MANIFEST.json` (566 objects, 10,685,426 bytes, every one with a VersionId, bucket versioning Enabled);
bodies at `~/.opal/demque/snapshots/r9_pre_extension_20261011T171807Z/` (device-local), with `pacer.json.before`. The plan: frontier 2026-10-09
(a Sunday gives the prior Friday), request `STANDING-T1-EXTEND-2026-10-09`, 141 symbols, 141 pacer entries reset.

## After: the section 6 denominators of the COO half

| quantity | read |
|---|---|
| names in the run (`stored`) | 141 |
| LOCKED and written (branches A and B) | **127** |
| REJECTED, untouched (branch C) | **14** (`REJECTED:LOW_TRADE_AGREEMENT`, the held names of D1-S9) |
| pull not OK (branch D) | 0 |
| names held because the pull ADDED a split row (CTO condition) | **0** |
| `prices.parquet` objects that changed against the snapshot | 127 of 141 (the other 14 byte-identical) |
| files with FEWER rows than the snapshot | **0** |
| cells of the old range that differ (`close_served`, `as_traded_close`, `total_return`, `cash`) | **0** of the 127 files |
| `max(date)` after | 2026-10-09 on **127**; 2026-06-23 on 14 (untouched three-column files) |
| lock rows | 127 `LOCKED` / `held` / `trades_through` stated; 14 `LOCKED` / `held` (the hold records, no `trades_through`) |
| Yahoo pacer | no pushback; 166 requests by 17:38Z, run ended 17:48Z |

## What is true now

- **C-PRICES: 127 of 141 price files are seven-column AND at the T-1 frontier (2026-10-09).** The 14 are three-column, end 2026-06-23, and serve
  with claim `held` and the stated reason (D1-S9, D1-S13). 141 of 141 is NOT met.
- No split row was added in the 76-trading-day tail for any name, so the CTO's split condition held nothing back.
- Consumers named in the half: `commonwealth_daily_valuation.py` reads `splits.parquet` (rewritten byte-equal in content for the 127, no row added);
  `commonwealth_price_need.py` reads `index/index.parquet`, rewritten by the run.

## Not yet read (named, open)

- Condition 4 of the half: the schedule read as DESIRED and APPLIED after the first SCHEDULED run (the task's 22:30 local fire of 2026-10-11),
  and the `comp-freshness` entry carrying `freshness_basis: trading-day-frontier`. The deliberate run above is not the scheduled one.
- The second scheduled run's day-2 id (`STANDING-T1-EXTEND-<next frontier>`) drawing: the live negative arm of row D1-W24-S1.
- ADVI_COTBKF's reader of `prices.parquet` (dell2), a residual the CTO accepted as named.
