# 7-Day Binding-Input Landing Table — MDPF canonical rebuild (T2.C ask-1 + ask-2 empirical half)

**Author:** 0.2.0_DS_PortfolioAnalytics · **Measured:** 2026-08-03 ~22:10Z · **Window:** partition dates 2026-07-28..2026-08-03
**Method:** `s3api list-objects-v2` per `date=` partition; LastModified reported in **UTC** (never local `s3 ls` — the known false-staleness trap). Consumer: AE T2.C clock v2 apply (@5a20433a5c re-check of the derived 10:45 ET close).

## Landings (max LastModified per partition, UTC)

| Table | Cadence pattern (7-day observed) | Landings |
|---|---|---|
| `smartx/platform/silver/fact_model_aum_daily` | **same-day partition, DAILY incl. weekends, 13:38–13:41Z (09:38–09:41 ET)** | 7/7 days: 13:38:24 / 13:38:43 / 13:40:28 / 13:40:32 / 13:40:17 / 13:40:42 / 13:41:10Z |
| `schwab/08242234/silver/fact_rps_s2` | partition `date=D` lands **D+1 10:16Z (06:16 ET)**, trading-day dates only | 07-28→07-29 10:16:00Z; 07-29→07-30 10:16:03Z; 07-30→07-31 10:16:02Z; 07-31→08-01 10:16:00Z; weekend dates absent (normal); 08-03's due 08-04 ~10:16Z |
| `eclipse/inflection/silver/fact_portfolios_full` | partition `date=D` lands **D+1 03:30Z**, daily incl. weekend dates | 6/6 through date=08-02 (each next-day 03:30:30-31Z); date=08-03 due 08-04 03:30Z |
| `orion/inflection/silver/fact_assets` | **same-day partition, DAILY incl. weekends, 14:16:04–05Z (10:16 ET) — 7/7 to the second** | all 7 days 14:16:04/05Z |
| `blackdiamond/cottonwood/silver/fact_model_assignment` | **same-day partition, DAILY incl. weekends, 06:00:53–56Z (02:00 ET)** | 7/7 days |
| `blackdiamond/cottonwood/silver/fact_holdings` | partition `date=D` lands **D+2 03:30Z** — ⚠ pattern BROKE for date=08-01 | 07-28→07-30, 07-29→07-31, 07-30→08-01, 07-31→08-02 (all 03:30Z); **date=08-01 was due 08-03 03:30Z and is ABSENT at 22:10Z** (08-02/08-03 not yet due) |

## What this decides (for the v2 apply)

1. **Derived close 10:45 ET: HOLDS on 7 days.** Season-worst binding-input landing = orion 14:16:05Z (10:16:05 ET), 7/7 within one second of schedule; smartx 09:41 ET worst. Nothing lands between 10:17 ET and the 11:00 ET floor on any sampled day.
2. **Ask-2 empirical half: NO binding table landed at any 16:00Z-class time on ANY of the 7 days** (cluster: 03:30 / 06:00 / 10:16 / 13:38–13:41 / 14:16Z). The winter 16:00Z→11:00-ET-collision concern is EMPTY on this window; job→table source cross-ref remains AE-census's half, but no observed landing contradicts the apply.
3. **AE INFERRED row (b): REFUTED at 7 samples** — `fact_model_aum_daily` (THE canonical frontier table) lands 09:38–09:41 ET immediately after the 09:00–09:35 ET SmartX pulls, daily. The morning ET pulls feed the CANONICAL plane, not the underscore plane only. (Job→table mechanism still INFERRED-from-timing; 7/7 correlation.)
4. **v1-premise post-mortem datum:** the "silver-schwab 12:15Z sweep" premise was also wrong at table grain — `fact_rps_s2` lands 10:16Z next-day. (v2 no longer leans on it; recorded for the delta log.)
5. **⚠ NEW WRINKLE (not mine to chase; AE + cot-lane datum):** the cot `fact_holdings` D+2 mirror MISSED its 08-03 03:30Z landing for date=08-01 — first break in the observed pattern; also relevant to the (b+) rider (no new weekend measurements accruing while broken). Surfaced here + in my checklist.
6. **Stage-6d edge refinement:** the assignment mirror is 06:00Z (not the 03:30Z the v1 doc assumed — 03:30Z is the holdings/eclipse slot). Same conclusion (hours before any floor), corrected value for the record.
