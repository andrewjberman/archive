# Never-widen ask -- OG-bf-1, the 13-month completion-record backfill, both masters

By: `0.9.0_WK_NFRA_OPLGTW~41` (PHASE A, no write of any kind), measured 2026-10-08T22:45Z to 2026-10-09T00:12Z, on
behalf of the issuer `2.0.0_SA_COO~O`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-bf-1.closure-marker-backfill-13m.md`.
Input: `closure_census_record.json` (OG-cc-1, drained @d02b443889). Form follows
`deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_ASK_OG-gw-2_20261003.md`.

**Halves owed:** `1.0.0_SA_CTO~O` and `2.0.0_SA_COO~O`, each against THIS file at its commit.

**THE DECISION THIS ASK TURNS ON (read section 3 first).** The 08242234 write set has no downstream consumer and can be
signed as written. The 08335338 write set fires the 49F gold dispatcher once per record, and the dispatcher does NOT
use the record's date: each qualified historical record runs the gold chain for today's T-1. Section 5 names three
ways to sign 08335338, and which of them needs a separate leg by `0.7.0_AE_CloudOps~Z`.

All files below are in `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/` (call it `W`).

## 1. What Phase A measured (steps 1-3)

**Missing dates (OG-cc-1).** 256 per master, window 2025-09-07 to 2026-10-07, of 273 silver dates; the same 256 dates
on both masters. 10 per master carry a LEGACY record today; the other 246 have no record at all.

**Source proof, per date (step 2).** For each of the 512 (master, date) pairs `bf1_dry_run.py` ran the producer's own
`convert_object` over every bronze key the date holds, through a read-only S3 wrapper (any verb but `get_object`,
`head_object`, `list_objects_v2` is recorded and refused before it reaches S3). It then composed the closure the replay
would write (`day_inventory` + `build_closure`) and graded it twice: with the producer's `validate_closure`, and with
the gateway's record-level rule on the would-be marker body (`catalog.membership_findings` + `catalog.validate_closure`,
as OG-cc-1 did). A date is a CANDIDATE only if all of these hold: zero convert errors, zero write attempts, zero
missing projection dims or facts, exactly one marker date equal to the date, and both validators say qualified.

| master | missing | CANDIDATE | UNAVAILABLE | write attempts | convert actions seen | bronze keys over candidates |
|---|---|---|---|---|---|---|
| 08242234 | 256 | 256 | 0 | 0 of 256 | `skipped-hole`, `skipped-idempotent` only | 2900 |
| 08335338 | 256 | 256 | 0 | 0 of 256 | `skipped-hole`, `skipped-idempotent` only | 3341 |

Output: `dry_run_all.json` (one row per pair, all fields), `backfill_plan.json` (the write set below). Elapsed
2328 s, 4 workers.

**Controls on the instrument** (run 2026-10-09 ~00:00Z, not part of the 512):
- a date with no bronze (2025-09-06) and a future date (2026-12-25) both read `UNAVAILABLE` with
  `NO_BRONZE_SOURCE` and `incomplete:UNEXPLAINED_EMPTY_DAY`, so the grade can say no;
- an already-qualified date (2026-09-15) reads CANDIDATE / QUALIFIED, matching the live record;
- a `put_object` through the wrapper is recorded and refused (`write refused`), so a zero write count is not a blind zero.

**What "proven-complete" means here, and does not.** The producer's closure derives its expected set from the bronze
objects that exist for the date when it is composed (its own `expected_source_basis`: "the vendor publishes no day-level
manifest, so a type that lands AFTER composition is not expected by this record"). So a candidate is proven to be
internally consistent -- every expected silver table present, VersionId-bound and row-counted, nothing failed, no
unexplained empty -- against the bronze as landed. It is NOT proven that the vendor sent every file. No date was
refused for that reason, because the producer has no instrument to refuse on. This is the same standard OG-c-2
replayed one date on, and the standard the daily producer applies now.

## 2. The exact write set

Per master, per candidate date, the replay invokes `opal-assets-silver-schwab` once with that date's bronze keys as a
synthetic S3 event (the OG-c-2 form: `Records[].s3.object.key`, RequestResponse, one attempt, no retry). Each
invocation writes exactly TWO objects, as OG-c-2's `replay.json` records:

| per master | count | key | write type |
|---|---|---|---|
| completion record | 256 | `schwab/<master>/meta/complete/date=<D>.json` | S3 conditional PUT: `If-None-Match: *`, else read ETag then `If-Match` |
| run manifest | 256 | `schwab/<master>/meta/conversions/<run_id>.json` | plain PUT, a new key per run |

Total 1024 objects: 512 per master. 10 of the 256 completion-record writes per master replace a LEGACY version (the
bucket is versioned, so the legacy version stays as the previous version); 246 are first versions. The dates, newest
first, and each overwritten record's current VersionId are in `backfill_plan.json`. The 17 dates already QUALIFIED are
not in the set: the producer's `_already_qualified` check would write nothing for them anyway.

**Nothing else is written.** No bronze or silver object (the dry run's zero write attempts, and `convert_object` reached
only the idempotent branch on all 512). No `backfill-status.json`: the sweep path writes it, the event path "NEVER
touches it" (`schwab_runtime.py` header). No bucket setting, notification, policy or grant.

**The writing identity.** The Lambda's role `opal-assets-silver-schwab-role`, read live: attached policy
`opal-assets-silver-write-schwab` allows `s3:PutObject`, `GetObject`, `AbortMultipartUpload`,
`ListMultipartUploadParts` on `schwab/08242234/{silver,meta}/*` and `schwab/08335338/{silver,meta}/*`, and `ListBucket`.
It has no delete. The operator identity that invokes (`Andrew_Berman`, `iam simulate-principal-policy`) is allowed
`lambda:InvokeFunction`, `s3:DeleteObjectVersion`, `s3:GetObjectVersion`, `s3:ListBucketVersions` on these keys. Deployed
code: `CodeSha256 v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`, `OPAL_BUILD_COMMIT 1f03a3f209`, last modified
2026-09-16T18:49:30Z, equal to OG-c-2's deployed build. Memory 3008 MB, timeout 600 s.

**Order and rate.**
- 08242234 first, in full; then 08335338 (only once section 5 is settled for it).
- Within a master, newest date first (2026-09-14 down to 2025-09-08), so an interruption at any point leaves a contiguous
  qualified suffix and no gap inside the served range.
- One invocation in flight at a time. The function has reserved concurrency 2, so one slot stays free for the daily
  bronze events. Measured per-invocation time in OG-c-2 was 10.7 to 12.5 s for 11 bronze keys; expected here about 12
  to 15 s, so about 55 to 65 minutes per master.
- Outside the windows OG-c-2 used (09:30-10:30Z, 12:40-13:00Z, 21:30-22:30Z), plus the sweep at 12:15Z, which the
  same function runs.
- After each invocation, GET the record and apply the OG-cc-1 qualification rule. Stop on the first record that is not
  QUALIFIED, on any Lambda `FunctionError`, throttle or timeout, and report; do not retry blind.

**Writers of `meta/complete/` -- N, and the rule read for each.** N = 2 call sites of ONE function, in ONE Lambda:
1. `schwab_runtime.run_event` -> `conversion_manifest.write_complete_marker_verified`. Rule: a lane emits its marker only
   if none of ITS results failed; one marker per date in the results' `silver_keys`; the closure is composed from a fresh
   read of the whole day and written by conditional PUT; if the object already holds a qualified closure with the same
   `closure_id` it writes nothing (`ALREADY_QUALIFIED`). The replay uses this path.
2. `schwab_runtime._sweep_lane` (12:15Z, EventBridge `{"mode":"sweep"}`) -> the same function, same rule, for the dates
   the sweep itself converted. The sweep converts nothing for these dates (all are idempotent), so it writes no record
   for them.

The function has three `put_object` sites: `conversion_manifest.py:274` (the v1 write, reached only with no `compose`;
both callers pass one), `:897` (the conditional write; deployed `write_guard: conditional`, as OG-c-2 read back) and
`:907` (the fallback when botocore predates conditional writes; it writes `write_guard: unconditional`, which never
qualifies). No other code in the repo writes this prefix (the gateway code and `schwab_reader_iam.tf` only read it).
IAM can also let the operator identity write anywhere; this order uses no such path.

## 3. Every ObjectCreated consumer of these keys, and what ONE historical record causes

Read live 2026-10-08, `s3api get-bucket-notification-configuration` on `opal-data-assets` (`evidence_bucket_notification_config.json`):
11 Lambda configurations, 0 queue, 0 topic, no EventBridge configuration. Filtered to `schwab/*/meta/`:

| key prefix | consumers | what one record causes |
|---|---|---|
| `schwab/08242234/meta/complete/`, `meta/conversions/` | **none** (0 of 11 configurations match; no rule targets any consumer by `list-rule-names-by-target`) | nothing downstream |
| `schwab/08335338/meta/conversions/` | **none** | nothing downstream |
| `schwab/08335338/meta/complete/` `*.json` | **1**: `advi-49f-silver-complete-accelerator` -> `advi-49f-gold-dispatch` | below |

The silver Lambda's own bronze rules filter `schwab/<m>/bronze/*.zip`, which a `meta/` write does not match. The
dispatcher has no reserved concurrency, no event-invoke config, no event-source mapping.

**What the dispatcher does with ONE record on 08335338** (deployed code equals `infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py`,
byte for byte after LF normalisation, `CodeSha256 TjIWGFWkbUswLkA+mUac9NS+LRZ1q7o6lR1iQLb0kI4=`, modified 2026-09-29T03:12:40Z;
`evidence_dispatcher_function.json`). Branches, from `lambda_handler`:

- **Branch ACTS (the record's exact version reads `closure.status == "qualified"`; lines 229-244 gate on nothing else).**
  The dispatcher ensures the host `i-01003b035d2988dfb` is running (starting it if stopped), then `send_command`s the SSM
  document `advi-49f-chain-dispatch` with ONE parameter, `StartedByDispatcher` (lines 259-265). **It passes no `Date`.**
  The document's empty-`Date` path runs `chain_49f_entrypoint.py --production`, which derives the date from the trading
  calendar as T-1 at run time. So a record for 2025-09-08 runs the chain for today's T-1 (2026-10-08 if sent at the
  time of writing), not 2025-09-08. Both statements are read from code, not from the net result:
  `advi_49f_floor.tf` document body, `data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py` (the repo copy; the
  S3 `_code` the host syncs is in the 49financial bucket, which this order does not read).
  Measured effect of ONE such dispatch (OG-c-2, 2026-09-16, `producer-deploy-replay.result.md` section 3): the host went
  stopped -> started; `CHAIN START date=2026-09-15 ... CHAIN OK wall=144.6s`; **30 of 31** `gold/.../date=2026-09-15`
  keys were re-PUT as new VersionIds; the dispatcher logged `ERROR ... signature=UNKNOWN` (row W4-S12); the host stopped
  again about 13 minutes later. That is a served-output move per record, on a date that was already served.
- **Branch SKIPS (the version reads anything else, `incomplete` or an unreadable body).** The dispatcher prints `SKIP`,
  returns `dispatched: false`, and makes no EC2 or SSM call. Nothing downstream. For this backfill that branch occurs
  only if a record is composed `incomplete` at write time (for example, a bronze file lands during the invocation); a
  record the dry run graded qualified is expected to take the ACTS branch.

**Cumulative effect of 256 records on 08335338 at the planned rate, INFERRED not measured.** About 256 dispatcher
invocations, one per record. The chain holds a host-level mutex (`CHAIN REFUSED rc=3`, never stolen), and one chain run
takes about 145 s against about 13 s between records, so about 23 chain runs would complete (each re-PUTting ~30 gold keys
for the same T-1) and about 230 dispatches would end `REFUSED`. One further hazard is read from the document text and
has never been exercised: a dispatcher that finds the host not running passes `StartedByDispatcher=true`, and the
document ends with `sudo shutdown -h +2` for such a command even when the chain refused. Several dispatchers arriving
during the host's start-up could each schedule a halt, and a halt two minutes after a refused sibling could land inside
the 145 s run of the live chain. Treat this as a possible half-written gold fire.

**08242234 has no consumer.** Its 256 records and 256 manifests move nothing outside the Gateway's own reads. The Gateway
begins serving the newly qualified dates; that is the intended effect of C3 and is not a never-widen item (the
Gateway's grants are unchanged).

## 4. Rollback per key

- **Completion record, first version (246 per master):** `delete-object --version-id <the new VersionId>` leaves no
  version; the key is absent, which is its state today. The new VersionId is recorded by the replay, per record.
- **Completion record replacing a LEGACY version (10 per master):** the same delete of the new VersionId makes the legacy
  version the current one again. The legacy VersionIds are in `backfill_plan.json` (`prior_marker_latest_version_by_date`)
  and `marker_versions_before.json`.
- **Run manifest (256 per master):** a new key each; `delete-object` of its version (or the key) returns the state to
  absent.
- Identity for rollback: the operator (allowed), never the Lambda role (no delete). Each delete is per version, and
  none touches silver or bronze.
- **What a rollback does NOT undo (08335338 only):** a dispatched chain run. The gold `date=<T-1>` keys it re-PUT keep their
  new VersionIds; their previous VersionIds are recoverable per key from the bucket's version list. Phase B would take a
  before and after snapshot of those keys (the OG-c-2 form), which needs read access to
  `s3://opal-data-49financial/gold/advi/_logs/` and the `date=<T-1>` keys. The order's bounds do not admit that bucket
  (OG-c-2's exception, ruling R-OG-4, was for that order). **The signed halves must admit that read, or say that no
  such snapshot is wanted.**

## 5. How 08335338 can be signed -- the issuer picks one; I recommend none and take the signed choice as written

- **Option X, accept the effect.** Sign the cumulative paragraph of section 3 as written: up to 256 dispatches, about 23
  gold re-PUTs of T-1, a possible mid-run halt. No other leg. Prior art: OG-c-2 signed one dispatch.
- **Option Y, make a historical record inert first (a separate leg).** `0.7.0_AE_CloudOps~Z` deploys a change to
  `advi-49f-gold-dispatch` so that it SKIPs a marker whose date is not the date its own `--production` would run. This
  changes the Lambda's code through Terraform (`module.advi_49f_gold_dispatch`, the only deploy path for a Lambda per
  CLAUDE.md); its rollback is the previous zip (the live `CodeSha256` above). It leaves the accelerator live for the daily 09:46Z markers, which are for T-1 and
  would still dispatch. The gate's rule is for the leg's owner to design; the date the document derives needs the
  trading calendar, which the Lambda does not carry today. After the leg, the 256 records cause no dispatch (the SKIP
  branch). Cost: a code change to the production dispatcher.
- **Option Z, suspend the accelerator for the write window (a separate leg).** `0.7.0_AE_CloudOps~Z` removes the one
  `advi-49f-silver-complete-accelerator` block from the singleton `aws_s3_bucket_notification` by Terraform, then
  restores it, and reads the notification configuration back equal to `evidence_bucket_notification_config.json`
  (11 of 11). The floor `cron(45 12 * * ? *)` stays the production trigger throughout (the block's own comment: the
  accelerator is "an accelerator only"). Cost: the apply rewrites the notification set of a bucket whose other 10
  configurations drive every silver conversion; a slip drops bronze triggers.
- **Option W, write 08242234 only now.** Sign the 08242234 write set (256 records, 256 manifests, no consumer) and hold
  08335338 until X, Y or Z is chosen.

If any leg is chosen, I would not write 08335338 until the leg's own ledger entry is closed and its read-back is
committed; I would name that commit in the continuation I act on.

## 6. The 08403355 extension

Not in this write set. The producer declares `DECLARED_SCHWAB_MASTERS = ("08242234", "08335338")`
(`silver_registry.py:56`), so the deployed Lambda cannot write a record for 08403355 until `OG-tm-1`'s change to that
list is deployed and its own silver exists. The extension is the same procedure re-run for that master (census, dry run,
write set, rollback, consumer scan) and needs its own signed ask; it does not ride this one. Its consumer scan can
reuse the table in section 3: 0 of 11 notification configurations match `schwab/08403355/meta/`.

## 7. Phase B, if signed (for the continuation to confirm)

1. Open `nfra-oplgtw-og-bf-1-marker-backfill` with `.tools/deploy_ledger.py`, commit it and its sentinel.
2. Write `W/backfill_record.json` with `started_utc` before the first write; invoke per section 2, in order and rate.
3. After each invocation: read the record back, apply the qualification rule, stop on the first failure.
4. Close the ledger and commit before AC1 and AC2. AC2's difference control needs no snapshot: every silver object a
   record names has a `LastModified` older than `started_utc`.
5. AC3 is read from the consumers' logs: the dispatcher's CloudWatch log group and, if admitted, the 49F chain logs.

## 8. Halves

**COO -- owed:** `2.0.0_SA_COO~O`. **CTO -- owed:** `1.0.0_SA_CTO~O`.
Each half should name: the option chosen in section 5; whether the 49financial read in section 4 is admitted; and
whether the order stands (newest first, one in flight, outside the named windows).

## 9. Files

`NEVER_WIDEN_ASK_OG-bf-1.md` (this), `backfill_plan.json`, `dry_run_all.json`, `bf1_dry_run.py`,
`marker_versions_before.json`, `evidence_bucket_notification_config.json`, `evidence_dispatcher_function.json`,
`closure_census_record.json` (OG-cc-1).
