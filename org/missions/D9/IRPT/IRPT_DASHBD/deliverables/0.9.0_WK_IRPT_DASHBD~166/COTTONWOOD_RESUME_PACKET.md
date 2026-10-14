# COTTONWOOD RESUME PACKET -- account_return_daily (never-widen)

**TO:** IRPT_DASHBD.TO-DB-b-201 | **Worker:** 0.9.0_WK_IRPT_DASHBD~166 | **Issuer:** 2.0.0_SA_COO~D2 | **Round:** 104, workstream B
**Status:** PACKET ONLY. Nothing is written, deployed, pushed or scheduled by this cell. The resume is BLOCKED (section 7).
**Reference end:** 2026-10-12 (a Monday and a trading day; `prev_trading_day(2026-10-13)` returns 2026-10-12).
**Never-widen:** the act moves only the keys in section 2. Each key is named, counted and rolled back in section 6.

---

## 1. The act

Two linked acts, both proposed here and neither authorised by this packet:

- **Backfill** of `account_return_daily` (bucket `opal-data-cottonwood`, prefix `irpt/cottonwood/gold/account_return_daily/`) for the trading days from **2026-06-23** through **2026-10-12**, inclusive. The range is **78 trading days**, counted by `lib/trading_calendar.py` `trading_days_between` (source `NYSE/hardcoded-fallback-2010-2027`; see section 7, condition 4). The backfill runs through the adapter's own apply path (`data/assets/scripts/silver/commonwealth_account_return_daily.py`, which calls the producer's `emit_day`).
- **Schedule** the producer moves onto: an EventBridge Scheduler schedule, rule name `irpt-cot-reporting-gold-daily`, cron `cron(41 7 ? * MON-FRI *)`, timezone `America/New_York` (section 3).

The backfill's start, 2026-06-23, is the one date the Commonwealth silver input holds (section 2). The backfill's end, 2026-10-12, is the reference end. The input does not reach the end (section 7, condition 3).

---

## 2. What moves

- **Partitions written:** 78, one per trading day in 2026-06-23 .. 2026-10-12 (inclusive). The table then holds 3,325 + 78 = 3,403 day partitions.
- **Objects per partition:** 2 (`data.parquet`, `manifest.json`). Total objects written by the backfill: 156.
- **Current state of the target (read 2026-10-14):** 3,325 partitions, 2013-04-03 .. 2026-06-22, 6,650 objects. All were minted on 2026-10-11 by the TO-CB-al-2 apply (section 4b).
- **Keys outside `keys_written`:** the apply path also lands the blank-reasons sidecar (`irpt/cottonwood/gold/account_return_daily_blank_reasons/source_date=2026-06-23/`) and the method row (`irpt/cottonwood/gold/dim_return_method/method_version=3/`, two objects) on a stamped run. Section 7, condition 5, requires the resume to exclude them or to prove them byte-identical.
- **Pages that read this table:** none established. The CB-al-2 ledger records the table as APPLIED, UNREAD, and ADVI_COTBKF ADDENDUM 11.1 records that no reader exists. `comp-pipescript postdeps` refused the producer's script id in all four trees (bd, inf, cot, mdpf), so the tool did not establish the reader set. A repo search for the table path returns writers, checkers and records of reads, and no served page. Consequence: no page's figures change from this act. A reader built later must be named before any resume.

---

## 3. When and where

**Schedule (EventBridge Scheduler, kind EVENTBRIDGE):**

- **rule_name:** `irpt-cot-reporting-gold-daily`
- **name_source:** `lib/opal_naming.py` `name("irpt", "cottonwood", "reporting-gold", "daily")`, which returns `irpt-cot-reporting-gold-daily`. This is the same builder call and cadence kind as the 49 Financial schedule (`infra/aws/terraform/investor-reporting/reporting-gold/schedule.tf`, module `irpt_reporting_gold_schedule_name`, which yields `irpt-49f-reporting-gold-daily`). No registry row is needed: the builder returned without refusal.
- **owner:** the AE CloudOps class `0.7.0_AE_CloudOps`. The instance is for the CTO to assign. The seat that minted the table is `0.7.0_AE_CloudOps~CB2`.
- **cron:** `cron(41 7 ? * MON-FRI *)`, timezone `America/New_York`. This is the 49 Financial model, read live this session (state ENABLED). It is a model value and was not measured against any Commonwealth landing time, because none exists after 2026-06-23.
- **Trading-day rule:** MON-FRI, with the handler resolving T-1 from the trading calendar, as the 49 Financial schedule does.
- **Target:** NOT ESTABLISHED. The 49 Financial schedule targets `irpt-49f-reporting-gold-lambda`, whose declared sources resolve to one firm (`infra/aws/terraform/investor-reporting/reporting-gold/locals.tf`, `irpt_rg_firm`). A Cottonwood schedule needs its own target or a declared source. That is a build item and is not decided here.
- **Existence now (read this session):** `irpt-cot-reporting-gold-daily` does not exist (GetSchedule: ResourceNotFoundException). `irpt-49f-reporting-gold-daily` exists, ENABLED, target a reporting-gold Lambda.
- **Where it would be built:** a Terraform root beside `infra/aws/terraform/investor-reporting/reporting-gold/`. Nothing is written in this cell.

---

## 4b. Writers

Counted writers of `irpt/cottonwood/gold/account_return_daily/` for the window 2026-10-10 00:00Z to 2026-10-12:

1. **0.7.0_AE_CloudOps~CB2**, the TO-CB-al-2 mint, `--apply` step 6, 07:01:01Z to 07:17:06Z on 2026-10-11. It wrote 3,325 partitions and 6,650 objects. Evidence: deploy-completion ledger `20261011T065618Z` (opened 06:56:18Z, closed 07:23:05Z; leg L1 read zero versions and zero delete markers under the prefix before the write; leg L5 landed 3,325 days); the seat's session log for the day; the two manifests' LastModified instants (07:03:46Z and 07:17:06Z, the second equal to the apply's last-line time). Each key holds one version and no delete marker, which fits a first creation and not an overwrite.
2. **The reporting-gold Lambda** (`irpt-49f-reporting-gold-lambda`): zero log events on 2026-10-10 and 2026-10-11. The positive control on the same group over the last 30 days returned events on 2026-10-02, 10-03, 10-05 through 10-09, 10-12 and 10-13, so the query could read events. The function's configuration was last modified 2026-10-13.
3. **Unexplained writer from the round-103 read:** none remains for these two keys. The "rewrite" of round 103 was the mint's first creation (row `IRPT_DASHBD-D2-W166-S1`).

**Instrument limit:** no CloudTrail trail records S3 data events for `opal-data-cottonwood`. The organisation trail's write-only selectors name `opal-data-cot`, `opal-data-bd` and `opal-data-inf`. The served-key trail names `platinum/firm/` prefixes only. Management events on the bucket in the window returned zero. The attribution therefore rests on the ledger and the S3 instants, not on a read of the caller.

---

## 5. Both branches

- **The backfill lands (78 partitions, 156 objects):** the series reaches 2026-10-12 and the table holds 3,403 partitions. No served page reads the table (section 2), so no figure changes. The partitions are APPLIED, UNREAD, as the mint's keys are.
- **The backfill fails part-way:** the apply writes day by day, each put with its own ETag. A partial range leaves partitions from 2026-06-23 up to the failing day. A day can be half-landed: `data.parquet` present and `manifest.json` absent, which the verify step reports as `manifests=N/M` short. The mint's ledger rule applies: a partial mint is RESUMED under an amendment and is not deleted in place. The packet does not recommend resuming a partial range except by amendment. Detection: the `ARD-COTTONWOOD-VERIFY` line (`match` below `days`) and an independent `list-objects-v2` of the prefix.

---

## 6. Rollback

Per key, in bucket `opal-data-cottonwood`, whose versioning state is **Enabled** (read live 2026-10-14). No lifecycle configuration exists.

- **Previous version of each key:** none. Every key the mint created holds one version and no delete marker, and the mint's leg L1 read zero versions before the write. So there is no previous version to restore for any key this resume would create.
- **Rollback of a created key is its deletion, and that act belongs to Andrew.** The CB-al-2 ledger (CLOSE DISPOSITION, AMENDMENT 4 kept by AMENDMENT 5) states that rollback is not a delete and that a delete is Andrew's act. This packet names the deletion as the only rollback and does not perform it.
- **Scope of any deletion:** only the keys under `irpt/cottonwood/gold/account_return_daily/date=<D>/` for D in the 78 trading days of section 1: each partition's `data.parquet` and `manifest.json` (156 keys). Under versioning a plain delete leaves a delete marker; a version-specific delete is permanent. Both forms are named so that the choice is Andrew's.
- **Schedule rollback:** delete or disable `irpt-cot-reporting-gold-daily`. It does not exist yet.
- **No other key moves.** The rollback touches the 156 keys above and the schedule, and nothing else.

---

## 7. Conditions

1. **Ledger first.** The writer's record is ledger `20261011T065618Z`. The CTO reads it before any resume.
2. **The unexplained writer.** Established as 0.7.0_AE_CloudOps~CB2 (section 4b). The CTO confirms or rules.
3. **The input must cover the backfill. NOT MET.** `input_available_through` is **2026-06-23**. The three Commonwealth Cottonwood silver tables (`daily_returns`, `account_day_value`, `month_grades`) each hold one partition, `date=2026-06-23`, and the adapter reads only that partition. **gap_in_words:** no Commonwealth Cottonwood silver partition exists after 2026-06-23, so the 77 trading days 2026-06-24 .. 2026-10-12 have no input. **resume_blocked_on:** a Commonwealth delivery that covers 2026-06-24 onward; or a decision to change the pinned input date, which is an amendment to the adapter's input contract; or a decision to resume through 2026-06-23 only, which is a one-day act and not this packet.
4. **Trading calendar.** `pandas_market_calendars` is absent on this box, so `lib/trading_calendar.py` answers from its generated NYSE fallback (2010-2027). For the range 2026-06-23 .. 2026-10-12 the fallback is acceptable on the following reading: the range lies inside the covered years, the count of 78 is the fallback's answer, and the fallback must be regenerated before 2028. The equality test against the package (`lib/tests/test_nyse_fallback_equals_package.py`) was not run in this cell. The CTO accepts or requires the package before the resume.
5. **Other keys.** The apply path also lands the sidecar and the method row on a stamped run (ledger leg L5). The resume must exclude those two prefixes, or prove them byte-identical, so that `no_other_key_moves` holds for the resume and not only for this packet.
6. **Schedule.** The owner instance is assigned, the target is named (section 3), and the cron is checked against an input landing time. None exists after 2026-06-23.
7. **Questions for the CTO's half:** (a) Accept the 2026-06-23 input boundary, or require a delivery first? (b) Which target does the schedule call? (c) Which AE instance owns it? (d) Is deletion of the minted keys Andrew's word, as the ledger reads? (e) Accept the fallback calendar for this range (condition 4)?
8. **Not in this cell:** no S3 write, no DynamoDB write, no Lambda, EventBridge, Terraform or IAM act, no invoke, no producer run, no vendor call, no secret read, no deploy, no push.

---

## 8. Not established

- The caller of the 2026-10-11 PutObject calls. No CloudTrail data events cover the bucket. The attribution rests on the ledger and the S3 instants.
- Whether a backfill run writes the sidecar and the method row (condition 5 requires it be settled).
- The set of pages that read the table. `comp-pipescript` refused the producer's id in all four trees, and the ledger's "no reader" is recorded but not independently graded here.
- Whether the cron fits any Commonwealth landing time (no input exists after 2026-06-23).
- The target function for a Cottonwood schedule.
- Whether the fallback calendar equals the package's answer for this range (the equality test was not run here).
- Byte-level stability of the 6,650 minted objects (not re-read here beyond the two manifests).
