# OG-bh-1 plan -- history of the Tax SMA master 08403355 through the path 08335338 already uses (Phase A, no write)

By `0.9.0_WK_NFRA_OPLGTW~46`, 2026-10-09 ~07:50Z. Order `NFRA_OPLGTW.TO-OG-bh-1`. `W` = this folder. Nothing was written to S3.

## 1. What the census says (step 1-2)

`bh1_census_record.json`: SSM `fd109a83-6c02-4f4f-a3a9-b16a5d46a17d`, started 2026-10-09T07:41:04.561Z, `-LookbackDays 2000`
(search window 2021-04-18..2026-10-09), exit 0, no vendor refusal.

| | value |
|---|---|
| files enumerated | 6002 |
| served business dates | 758 (2023-10-03 .. 2026-10-08) |
| earliest_served | 2023-10-03 (the window opened 2021-04-18, so this is the source's start, not the window's edge) |
| types | 16: acc 509, rld 758, rlu 12, rly 36, rps 510, rtu 12, rty 36, sec 510, tcf 722, tcfx 245, tnn 102, trn 510, uln 510, ult 510, upn 510, upt 510 |

Two earlier runs (same copy, same one edit) sat at their window's edge and were widened, as the order asks:
`06102931-7d52-4e8d-a574-772874c7c655` (400 d; earliest 2025-09-04 = the window's first day, 276 dates / 3060 files) and
`b06d7458-a301-466a-9712-a160e90e12d6` (800 d; earliest 2024-07-31 = the window's first day; its output hit SSM's 24,000-character cap
and lost its tail, row Z-W46-S2). Each date's count in those two equals the 2000-day run's count for the same date (0 differences over
all dates the three share), so the search did not lose boundary dates between window sizes.

The history is not under a year. It is three years, in three shapes (file counts per date, from the DATE lines; type start dates
from the run's per-type lines):

| era | dates | files | what a date holds |
|---|---|---|---|
| A: 2023-10-03 .. 2024-09-26 | 248 | 526 | 2 files (rld, tcf) on 233 dates; 4 on 15 dates (the periodic rly, rty, rlu, rtu add files; the per-type split of those 15 dates is not in the run's output) |
| B: 2024-09-27 .. 2025-10-16 | 265 | 2735 | 10 to 13: acc, rld, rps, sec, trn, uln, ult, upn, upt, tcf, tnn and the periodic rly, rty, rlu, rtu |
| C: 2025-10-17 .. 2026-10-08 | 245 | 2741 | era B plus tcfx |

`tcf`, `tcfx` and `tnn` are the converter's NAMED_HOLES (`conversion_manifest.py:57`): 1069 of the 6002 files convert to nothing.
Three types (rlu, rtu, tcf) did not appear in the 30-day run of OG-en-1 (13 types) because they are not published inside that window.

## 2. The path 08335338 uses today (step 3), read live

1. **Bronze.** The SI2 puller (`sdd-daily-pull.ps1`, `-Target monolith`, default) lands the vendor zip untouched at
   `schwab/<master>/bronze/<type>/<YYYYMMDD>/<vendor name>.zip` and nothing else (it does not unzip; the extractor was removed). Live:
   `schwab/08335338/bronze/rps/20261007/` holds the one key `08335338.CRS20261007.RPS.zip`; `rld/20230712/` holds one zip. The partition
   date is the API AsOfDATE, cross-checked against the date in the vendor filename. The box role writes with `--sse AES256`.
2. **Silver.** The bucket notification `silver-schwab-<master>` (`schwab/<master>/bronze/`, suffix `.zip`, ObjectCreated) invokes
   `opal-assets-silver-schwab` ASYNC once per landed object. Live: reserved concurrency 2, memory 3008, timeout 600 s, MaximumRetryAttempts 2,
   on-failure destination `opal-assets-silver-dlq` (depth 0 now), CodeSha256 `AzrzJS+91y57ylRdqGccFPGqWaqAGLFn/jhItkAQCzE=`, modified
   2026-10-09T02:33:06Z. Each event converts that object to `schwab/<master>/silver/<table>/date=<D>/data.parquet` (rps also feeds
   fact_rps_s2, dim_position and dim_balance; sec feeds dim_asset; trn feeds dim_transaction), writes one run manifest
   `meta/conversions/<run_id>.json`, then composes the day's closure.
3. **Completion record.** The same invocation calls `write_complete_marker_verified` (`schwab_runtime.py:235`), which composes the closure from a fresh
   read of the whole day and writes `meta/complete/date=<D>.json` by conditional PUT. It writes nothing when the key already holds a qualified closure with
   the same `closure_id`. A second path, the 12:15Z EventBridge sweep (`{"mode":"sweep"}`, `schwab_runtime.py:338`), converts every bronze object whose silver is
   missing across all lanes (08403355 is the third lane since 02:33Z today), drains the DLQ (cap 100), and writes `meta/backfill-status.json`.
4. **History of 08335338, as it reads in the bucket** (measured; the 2026-07 act itself is not in a record I opened, so the order of events
   is INFERRED from these four reads): bronze reaches back to 2023-07-12 (rld, 815 date prefixes), silver to the same date (fact_rld 815
   partitions); completion records exist only for 2025-09-08..2026-10-07 (273, written by the OG-bf-1 13-month replay); the first
   `meta/conversions` manifest is 2026-07-14T21:46:02Z and one `trigger: sweep` manifest, `20260715T181504Z-64a7e1f5`, reads `shortfall_pre 344,
   bronze_keys 6959, silver_keys 8452, shortfall_post 0`, i.e. the sweep converted the 344 dates the event path had not. The puller
   header and `SCHWAB_AUTO_PULL_DESIGN.md` section 4.3 say the bronze came from a 2023-to-now wide search (6,933 rows) on the box into the staging
   bucket `opal-data-schwab` and was remapped to the monolith by the one-time remap role. **That staging step does not apply to 08403355**: its
   puller default target is the monolith, its box grants (`quartz-si2-monolith-write`: MonolithSchwabWrite, OpsWrite, MetaPullsWrite, plus the
   ListBucket condition) already name `schwab/08403355/`, and the remap role is not extended to it.

## 3. The backfill uses that SAME path, with no new code

- **Bronze:** the installed, unedited puller (S3 code object ETag `e49aea76a8c634c9d49e6a7cccc51bdf`, the one the schedule runs) with `-Master 08403355
  -Mode download -Target monolith -LookbackDays <L>` and no `-SnsTopicArn`, run as Administrator through the same register-start-wait-unregister SSM wrapper
  as `monolith-daily-schedule.tf`. Its single wide search plus skip-if-landed makes each run resume where the last stopped.
  The puller has no date-range parameter, so a batch is a window `[today - L, today]`; newest-first batches are successive larger L. `-MaxFiles` is NOT used:
  a run that stops at MaxFiles hits the denominator guard (`ENUMERATED != dl+skip+fail`, `Die 5`) and exits non-zero.
- **Silver and completion records:** the existing ObjectCreated rule `silver-schwab-08403355` and the existing 12:15Z sweep. No invoke by hand, no replay script.
- **No deploy, no Terraform apply, no new Lambda, no new layout.** Every grant it needs is live (section 4 of the ask). No separate leg for
  `0.7.0_AE_CloudOps~Z`.
- **Read-back:** a date is `backfilled` when its `meta/complete/date=<D>.json` reads `closure.status == "qualified"` under the gateway's record rule
  (`catalog.membership_findings` + `catalog.validate_closure`, as OG-cc-1 and OG-bf-1 grade); a served date whose record is absent or not qualified after the 12:15Z sweep
  following its batch is `unavailable` with the closure's own `findings` text, never guessed.

## 4. Questions the plan cannot answer yet (stated, not closed)

- **Era A dates** (rld and tcf only) have no precedent: 08335338 carries sparse early silver (fact_rld alone on 2023-07-12; no dim_* there) but no completion record
  before 2025-09-08. The producer composes the expected table set from the bronze that landed, so such a day expects fact_rld only (tcf is a named hole)
  and may qualify; whether the gateway's rule accepts it is only readable after the bronze lands. They are 248 of 758 dates. The ask lets the halves
  decide whether era A is in scope (section 6, item 1).
- **Time per batch** is unmeasured: no 08403355 download has run. Batch 1 is the measurement; the ask gates batch 2 on it.
