# MDPF_CANON round 3 enrichment item 1 -- the value leg's clock (issuer read, 2.0.0_SA_COO~D1, 2026-10-11 ~02:5xZ)

Round-2 analysis @71e85b7191 section 3 item 1, first half: name the `aum_daily` producer and its delivery schedule, read whether its
2026-10-09 rows have landed, and state whether the value leg structurally lands a day behind the count leg on a weekend fire.
Read-only: S3 lists and parquet gets. Nothing was put. The held acts are untouched (CTO ruling msg 3317 scope).

## The producer

The gold consolidator's `aum_daily` is `s3://opal-data-assets/smartx/platform/silver/fact_model_aum_daily/date=<run_date>/data.parquet`
(`channel_sources.py:58`, `SMARTX_AUM`). The silver table is built by `infra/aws/lambda/opal-assets/opal-assets-silver-smartx/silver.py`
(`fact_model_aum_daily`, from `model/{rmid}/bronze/model_aum`, `:27`, `:151`). The owner of that Lambda and of the SmartX bronze feed was
NOT read here.

## Delivery schedule, measured

One partition per calendar day, written at about 13:25Z (2026-10-10: `LastModified` 13:25:52Z, five minutes before the 13:30Z gold
fire). The listing holds 89 objects under the prefix (denominator printed). The partition for run_date R carries a `day` axis that
ends at max(`day`):

| run_date | weekday | max `day` | n |
|---|---|---|---|
| 2026-09-19 / 09-20 | Sat / Sun | 2026-09-17 (Thu) | both |
| 2026-09-21 | Mon | 2026-09-18 (Fri) | |
| 2026-09-26 / 09-27 | Sat / Sun | 2026-09-24 (Thu) | both |
| 2026-09-28 | Mon | 2026-09-25 (Fri) | |
| 2026-10-03 / 10-04 | Sat / Sun | 2026-10-01 (Thu) | both |
| 2026-10-05 | Mon | 2026-10-02 (Fri) | |
| 2026-10-06 .. 10-09 | Tue .. Fri | the prior trading day | each |
| 2026-10-10 | Sat | 2026-10-08 (Thu) | |

## Reading

- **The 2026-10-09 (Friday) value rows have not landed as of this read.** The newest partition is run_date 2026-10-10 and ends at
  2026-10-08. By the pattern above the first partition to carry Friday 2026-10-09 is run_date 2026-10-12 (Monday), written about
  13:25Z, five minutes before the 13:30Z fire.
- **Structural, not a one-off.** Every Saturday and Sunday run in the four weekends read (09-19/20, 09-26/27, 10-03/04, 10-10) ends
  at Thursday; every Monday run ends at Friday. Four weekends of four, 7 of 7 weekend runs in the listing window read. The silver
  table's `day` axis therefore sits one trading day behind the T-1 frontier (`lib/trading_calendar.prev_trading_day`) on every
  weekend run, while the count leg reaches Friday on the same day.
- Mechanism: INFERRED, not read. The pattern fits a SmartX source that publishes a day's performance on the next business-day
  morning only; the bronze landing times were not read.
- Consequence at the gold fire: on a weekend fire, global's cross-axis gate (v) refuses on the models whose count carries Friday
  against a missing value, and the value-bearing types for 49financial and inflection carry as-of Thursday. The gate's refusal is
  correct and is not loosened (round-2 analysis section 2). A Monday fire reads both legs at Friday.

## Falsifiers on the clock

- Sunday 2026-10-11 13:30Z fire: this reading predicts global refuses again and the value-bearing series stay at as-of 2026-10-08.
- Monday 2026-10-12 13:30Z fire: this reading predicts run_date 2026-10-12 ends at 2026-10-09 and the amended `r2_daily.py` reads
  arms 1 and 4 at the frontier 2026-10-09. A refusal with both legs at Friday would put the defect in the producer.
