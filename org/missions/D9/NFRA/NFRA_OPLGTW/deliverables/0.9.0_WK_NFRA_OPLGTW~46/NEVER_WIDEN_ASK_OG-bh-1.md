# Never-widen ask -- OG-bh-1, the full history of the Tax SMA master 08403355 through bronze, silver and the completion record

By `0.9.0_WK_NFRA_OPLGTW~46` (PHASE A, no write of any kind), measured 2026-10-09T07:33Z to ~07:55Z, for the issuer `2.0.0_SA_COO~O`.
Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-bh-1.taxsma-history-backfill.md`. Form follows
`deliverables/0.9.0_WK_NFRA_OPLGTW~41/NEVER_WIDEN_ASK_OG-bf-1.md`. Census: `bh1_census_record.json`; path and eras: `bh1_plan.md`.
All files are in `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~46/` (call it `W`).

**Halves owed:** `1.0.0_SA_CTO~O` and `2.0.0_SA_COO~O`, each against THIS file at its commit.

**What this ask turns on (section 6 first).** No consumer is wired to `schwab/08403355/` except the silver converter itself, so unlike 08335338
there is no served-output move beyond the Gateway starting to serve more 08403355 dates. The size is the issue, not a consumer: the source starts 2023-10-03, not
April 2026 -- 758 business dates, 6002 vendor files, about 5,800 silver-converter invocations on a function with reserved concurrency 2.

## 1. What Phase A measured

| | |
|---|---|
| census run | SSM `fd109a83-6c02-4f4f-a3a9-b16a5d46a17d`, 07:41Z (outside both windows), `-LookbackDays 2000`, window 2021-04-18..2026-10-09, exit 0, no refusal |
| served | 758 dates, 2023-10-03 .. 2026-10-08, 6002 files, 16 types |
| prefix today | `schwab/08403355/` holds no key at all (`list-objects-v2` with `/` delimiter returned no prefix) |
| first scheduled pull | 10:45Z today lands the 30-day window (22 dates, 226 files, per OG-en-1); this ask's set INCLUDES those 226 keys only if they are not yet landed when a batch runs |

## 2. The exact write set (all under `schwab/08403355/`; nothing under 08242234 or 08335338; no other bucket)

Counts are for the whole 6002-file set; subtract what the scheduled pulls have already landed when a batch starts (skip-if-landed writes nothing).

| prefix | what | count | write type |
|---|---|---|---|
| `bronze/<type>/<YYYYMMDD>/` | `08403355.CRS<YYYYMMDD>.<TYPE>.zip`, the vendor bytes, no extract | 6002: acc 509, rld 758, rlu 12, rly 36, rps 510, rtu 12, rty 36, sec 510, tcf 722, tcfx 245, tnn 102, trn 510, uln 510, ult 510, upn 510, upt 510 | `aws s3 cp --sse AES256`, new key |
| `silver/<table>/date=<D>/data.parquet` | converter output | about 7,483 (INFERRED: files x tables per type -- acc 1, rld 1, rps 4, sec 2, trn 2, uln/ult/upn/upt 1, rlu/rtu/rly/rty 1, tcf/tcfx/tnn 0 -- the table set read from 08335338's live closure of 2026-10-07, 15 expected tables) | PutObject, new key; an idempotent re-event writes nothing |
| `meta/complete/date=<D>.json` | the completion record | 758 keys; between 758 and about 6,000 PUTs, because the closure is recomposed as sibling files land and a changed `closure_id` rewrites the key (new VersionId each time; the last one stands) | conditional PUT (`If-None-Match: *`, else read ETag then `If-Match`) |
| `meta/conversions/<run_id>.json` | run manifest | about one per event invocation, so up to about 6,000, plus one per daily sweep | plain PUT, new key |
| `meta/backfill-status.json` | sweep status | 1 key, rewritten by every 12:15Z sweep (it is written whether or not this backfill runs) | PutObject, new version |
| `_ops/daily_pull/last_run.json`, `_ops/daily_pull/runs/<RUNID>.json`, `meta/pulls/<RUNID>.json` | the puller's run record | per puller run: 1 rewritten key + 2 new keys; 10 runs planned (section 4) = 20 new keys + 10 versions | `aws s3 cp --sse AES256` |

Nothing else: no delete, no bucket setting, notification, policy or grant, no Lambda or Terraform change, no write to the staging bucket
`opal-data-schwab`, no gold key.

**Dates and what each is expected to become.** Era A, 2023-10-03..2024-09-26 (248 dates, 526 files, rld and tcf only): expected table set is
fact_rld; qualification is UNMEASURED (no precedent, `bh1_plan.md` section 4). Era B, 2024-09-27..2025-10-16 (265 dates, 2735 files) and era C,
2025-10-17..2026-10-08 (245 dates, 2741 files): the shapes the producer qualifies today for 08335338 (OG-bf-1: 256 of 256 candidates).

## 3. Every writer of each prefix -- N printed, the rule read for each

| prefix | N principals | N code sites | rule read |
|---|---|---|---|
| `bronze/`, `_ops/`, `meta/pulls/` | 1: the SI2 box role `quartz-si2-spike-role`, inline `quartz-si2-monolith-write`: `MonolithSchwabWrite` PutObject `schwab/08403355/bronze/*`, `MonolithSchwabOpsWrite` `_ops/*`, `MonolithSchwabMetaPullsWrite` `meta/pulls/*`, `MonolithSchwabList` ListBucket with the `bronze/*` prefix condition (live read 2026-10-09). No GetObject, no delete | 1 puller (`sdd-daily-pull.ps1`, 4 `aws s3 cp` sites: landing, 2 `_ops`, 1 `meta/pulls`) | master from the filename prefix, date from AsOfDATE cross-checked to the filename; a mismatch quarantines the file; the zip is written before anything else; run record WARNs, never dies |
| `silver/`, `meta/conversions/`, `meta/complete/`, `meta/backfill-status.json` | 1: `opal-assets-silver-schwab-role`, policy `opal-assets-silver-write-schwab` (PutObject/GetObject/multipart on `schwab/08403355/silver/*` and `meta/*`, ListBucket; live read 2026-10-09, three masters). No delete | silver `schwab_conversion.py:267` and `stream_parquet.py:136`; manifest `conversion_manifest.py:138`; completion record `conversion_manifest.py:283` (v1, not reached: both callers pass `compose`), `:912` (conditional, `write_guard: conditional`), `:922` (fallback when botocore predates conditional writes; writes `write_guard: unconditional`, which never qualifies); status `backfill_status.py:246` | `meta/complete/` is written from two call sites of one function, `schwab_runtime.py:235` (event) and `:338` (sweep): a lane emits a marker only if none of ITS results failed; one marker per date in its `silver_keys`; the closure is composed from a fresh read of the whole day; nothing is written if the key already holds a qualified closure with the same `closure_id` |

Not writers: `opal-assets-write-schwab` (attachment count 0 per OG-tm-1), the remap role (not extended to 08403355), `bd49f_convert` (writes
`schwab/08335338/silver/fact_acc/*` only). The operator identity (`Andrew_Berman`) can write anywhere by IAM; this order uses no such path.

## 4. Run order, batch size, quiet windows

- **Order:** newest first, in batches by window. The puller has no date-range argument, so a batch is the window `[today - L, today]` with `L = (run day - oldest date of the batch)` in days, and
  skip-if-landed makes it write only what the previous batch did not. Nine batches (oldest date, newest date, dates, files in the range):
  B1 2026-06-09..2026-09-08 (63, 697; B1 also writes the 226 files of the last 30 days if the 10:45Z/22:45Z pulls have not), B2 2026-03-12..2026-06-08 (61, 697),
  B3 2025-12-11..2026-03-11 (61, 694), B4 2025-09-11..2025-12-10 (64, 694), B5 2025-06-04..2025-09-10 (68, 699), B6 2025-02-27..2025-06-03 (67, 697),
  B7 2024-11-19..2025-02-26 (67, 693), B8 2024-02-23..2024-11-18 (187, 699), B9 2023-10-03..2024-02-22 (98, 206). A tenth closing run uses `-LookbackDays 2000`: every file is then
  already landed, and its `enumerated = downloaded + skipped + failed` and landing-guard line are the whole-history denominator.
- **One puller in flight.** No `-MaxFiles` (it ends the run at `Die 5`), no `-SnsTopicArn`. The batch gate: batch N+1 does not start until, for every date of batch N, the completion record has been read, the DLQ
  `opal-assets-silver-dlq` reads depth 0, and the function's Throttles and Errors for the interval are named. Batch 1 is the measurement of puller minutes per batch and of silver drain time; the continuation reports both before batch 2.
- **Quiet windows.** A batch starts only outside, and finishes before, `[09:15,11:35)Z` and `[21:15,23:35)Z` (the three scheduled pulls with their deadlines), and outside `[12:00,12:50)Z` (the 12:15Z sweep, which shares the function's 2 slots). The SSM wrapper
  stops the Scheduled Task at 09:00Z or 21:00Z if it is still running (the lock file is then stale and the next run reclaims it).
- **The box-wide SDD session lock.** `C:\schwab-sdd\.sdd-session.lock`, CreateNew, one holder. A live holder makes a second puller `Die 7` rather than wait, so the batches avoid the scheduled pulls by time, as above, and avoid each other by being strictly one at a time. A crashed holder is reclaimed
  after its pid is dead or 120 minutes. The Phase A enumerate runs left a stale lock three times and each next run reclaimed it (logged `SDD session lock is STALE ... reclaiming`; rows Z-W39-S1/S3).
- **Silver load.** One bronze event per file, reserved concurrency 2, async with Lambda's own retry: batches of about 700 files are sized so the queue clears well inside the 6 h async event age. If a throttled event ages out it goes to the DLQ and the 12:15Z sweep converts the miss; the sweep's timeout is 600 s and its longest recorded Duration was 159 s with two lanes (a sweep that must convert a large miss is the case the batch gate exists to avoid).

## 5. Rollback per key (bucket versioning Enabled, read 2026-10-09)

The prefix is empty today, so every key this order writes is a FIRST version and its prior state is absence. Rollback is `delete-object --version-id <the version Phase B recorded>` for each key in the backfill record, in this order: completion records, manifests, silver, bronze, run records.
Identity: the operator (simulated 2026-10-09: `s3:DeleteObjectVersion`, `GetObjectVersion`, `ListBucketVersions` allowed on `schwab/08403355/` bronze, silver, `meta/complete` and `meta/conversions` keys), never the box role or the converter role (no delete). Deleting
a bronze object raises no event (the rules are ObjectCreated only). Keys written by the scheduled pulls (run ids not in the backfill record) are not in the set. What a rollback does NOT undo: a Gateway reader that read a record in the interval (nothing is cached in the data path I read; not measured).

## 6. Every ObjectCreated consumer of these keys, and what ONE historical date causes

Read live 2026-10-09, `s3api get-bucket-notification-configuration` on `opal-data-assets` (`W/evidence_bucket_notification_config.json`): 12 Lambda configurations, 0 queue, 0 topic, no EventBridge configuration key.
Filtered to `schwab/08403355/`:

| prefix | consumers | what one historical date causes |
|---|---|---|
| `schwab/08403355/bronze/` `*.zip` | **1**: `silver-schwab-08403355` -> `opal-assets-silver-schwab` | BOTH BRANCHES. Converts: ~10-13 invocations per date, each writing its silver tables, a manifest, and a closure recompute. Skips: a hole type (tcf, tcfx, tnn: 1069 files) writes a manifest and no silver; an already-landed key is never re-uploaded, so no event |
| `schwab/08403355/meta/complete/`, `meta/conversions/`, `silver/`, `_ops/`, `meta/pulls/` | **none** (0 of 12 configurations match) | nothing downstream |
| `schwab/08335338/meta/complete/` | 1: `advi-49f-silver-complete-accelerator` -> `advi-49f-gold-dispatch` | **does not match 08403355**. No 49F accelerator and no gold dispatch is wired to `schwab/08403355/` (OG-tm-1 wired none; this read confirms). The 49F question stays open with Andrew and is not in this ask |

The Gateway's reader roles (OG-tm-1) already read `schwab/08403355/silver/dim_*` and `meta/complete/`; after the backfill the Gateway begins serving the newly qualified 08403355 dates. That is the intended effect and no grant changes.

## 7. What the halves decide

1. **Scope of era A (248 dates, 526 files, rld and tcf only).** Include them (Andrew: "full backfill, no cap"), accepting that some may end `unavailable`; or write eras B and C first and decide A after reading them. Bronze for A is 526 small files either way.
2. **Pace and the 700-file batch**, the nine batches and the closing run, the gate between batches, the quiet windows of section 4.
3. **Stop rule** (my proposal): stop on the first batch where a landed date's record reads not qualified for a reason other than missing sibling files, on any `Die` other than 7, on a DLQ depth above 0, or on a puller that did not start (Administrator console logged off). Report; do not retry blind.
4. Nothing else needs a leg: no deploy, no Terraform apply, no `0.7.0_AE_CloudOps~Z` step.

## 8. Phase B, if signed (for the continuation to confirm)

Open ledger `nfra-oplgtw-og-bh-1-taxsma-history`; write `W/bh1_backfill_record.json` with `started_utc` before batch 1; for each batch: UTC check, SSM wrapper, wait, read back, gate, record keys and VersionIds; the closing run; then the 12:15Z sweep
read (records for any date the sweep healed). Close the ledger and commit before AC2.

## 9. Files

`NEVER_WIDEN_ASK_OG-bh-1.md` (this), `bh1_plan.md`, `bh1_census_record.json`, `ssm_invocation_census_400.json`, `ssm_invocation_census_800.json`, `ssm_invocation_census_2000.json`, `evidence_bucket_notification_config.json`.
