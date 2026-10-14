# CN-m-1 -- reader census of the staged global aggregate

Key: s3://opal-data-assets/gold/mdpf_revamp/global/aggregate_aua_timeseries.json
Census at 2026-10-14T14:47:12Z by 0.9.0_WK_MDPF_CANON~20. Record: CN-m-1_READER_CENSUS.json beside this file.
Head (read-only head-object): 512,084 bytes, ETag 1113c3c080c4acb0c38d800610ade827, LastModified 2026-10-14T13:31:35Z, as_of_last 2026-10-13.

## Verdict

READERS-FOUND. Total readers 14 (code 5, scheduled 5, iam_static 4). Partner-facing candidate: one reader, the accrual bridge
(build_portal_gold_accrual.py, fired by schedule mdpf-accrual-bridge-daily). The staged bytes have NOT been shown to land under
portal/; the one observed dated portal object for the same as-of is a different object (see Landing evidence).

## Class 1 -- code (denominator: 8,812 files scanned under data/, infra/, lib/, .tools/)

The repo scan (check universe mode) names 28 files that contain both gold/mdpf_revamp and aggregate_aua_timeseries. Four read the
staged key. Five readers in all: a fifth, .tools/comp-freshness, reads the key through its config (served_freshness_config.yaml:115)
and has no literal key, so the scan cannot see it.

| Reader | Reads the key at | Writes its bytes to | Surface |
|---|---|---|---|
| build_portal_gold_accrual.py | :227 (source key built from SOURCE_PREFIX :88, scope global, type aggregate_aua_timeseries, declared :60-61 for every scope) | portal/gold/mdpf/global/aggregate-aua-timeseries/<as_of>.json (:244, put :290) | PARTNER-FACING-CANDIDATE |
| dim_mdpf_aum_metrics.py | :116 (AGG_GLOBAL_KEY :54, load_aggregate, called for --firm global/all) | gold/mdpf_revamp/global/aum_metrics.json and portfolios/aum-metrics.json | INTERNAL |
| dim_mdpf_non_model_assets.py | :102 default global URI, read via _read_json_uri at :244 | gold/mdpf_revamp/global/non_model_assets.json | INTERNAL |
| verify_mdpf_revamp_conditions.py | :54 (KEYS "g" :34) | log only | NONE |
| .tools/comp-freshness | :1097 (s3 cp in content mode, config :115 has as_of_field) | stdout only | NONE |

Excluded from the 28 (24 files): 12 DECLARATIVE-ONLY (config, changelog, manifests, IAM grants), 7 OTHER-KEY (the cottonwood key,
_aggregate_aua prefix, parquet partitions), 3 PRODUCER-WRITE-ONLY (mdpf_gold_consolidator.py, stage_mdpf_revamp_trio.py, and the dispatch
script mdpf-daily-dispatch.sh, whose :563-565 copies the global key; it is the trigger of two readers, counted under scheduled),
1 COMMENT-ONLY (build_dim_model_portfolio.py:37), 1 TEST. Full list in the JSON.

## Class 2 -- scheduled (denominator: 189 triggers: 34 scheduler schedules in the default group plus 155 event rules, read live)

| Trigger | State (live) | Expression | Runs |
|---|---|---|---|
| mdpf-accrual-bridge-daily (scheduler) -> mdpf-accrual-trigger Lambda -> SSM on the runner | ENABLED | cron(40 13 * * ? *) | build_portal_gold_accrual.py |
| mdpf-feeder-backstop-daily (scheduler) -> mdpf-feeder-trigger -> mdpf-daily-dispatch.sh stages 6c and 6e | ENABLED | cron(52 12 * * ? *) | dim_mdpf_non_model_assets.py, dim_mdpf_aum_metrics.py |
| mdpf-feeder-accelerator (event rule, S3 Object Created on opal-data-inf gold/meta/pipeline-complete.json) -> mdpf-feeder-trigger | ENABLED | event, no clock | the same two readers |

Not counted: opal-assets-mdpf-portal-publisher-daily (cron 13:50Z) runs a Lambda whose code reads portal/gold/mdpf/ only, not the
staged key. mdpf-daily-trigger has no live schedule. verify_mdpf_revamp_conditions.py and comp-freshness have no clock trigger in infra/.

## Class 3 -- iam_static (denominator: 574 .tf files under infra/aws/terraform, all searched for the key and for wildcard Resources)

| Role | Grant (Action, Resource) | Evidence |
|---|---|---|
| mdpf-daily-runner-ec2-role | GetObject on gold/mdpf_revamp/* | mdpf-pipeline/iam.tf:428 |
| mdpf-gold-lambda-role | GetObject and PutObject on gold/mdpf_revamp/* | mdpf-pipeline/iam.tf:883 |
| opal-assets-daily-emitter-role | GetObject on opal-data-assets gold/mdpf_revamp/* | opal-assets/emitter.tf:76 |
| opal-assets-mdpf-portal-publisher-role | GetObject on gold/mdpf_revamp/* | opal-assets/mdpf_portal_publisher.tf:90 |

No wildcard grant (opal-data-assets/*, *, s3:*) covers the key on an attached role. The router read policy (router_iam.tf:264-267,
opal-assets-read) is a managed policy with no attachment.

## Class 4 -- iam_live (denominator: 5 roles, comp-iam simulate, --no-control)

| Principal | STATE |
|---|---|
| mdpf-daily-runner-ec2-role | ALLOWED |
| mdpf-gold-lambda-role | ALLOWED |
| opal-assets-daily-emitter-role | ALLOWED |
| opal-assets-mdpf-portal-publisher-role | ALLOWED |
| opal-assets-mdpf-egress-publisher-role | NOT-DECIDABLE (implicitDeny with s3:prefix missing from the context; a conditioned statement, not a deny; not retried) |

Counts: ALLOWED 4, DENIED 0, NOT-DECIDABLE 1 (sum 5). Note: the live publisher Lambda opal-assets-mdpf-portal-publisher runs as
opal-assets-mdpf-egress-publisher-role (get-function-configuration), not as the portal-publisher role; the Terraform for the egress role
grants GetObject on portal/gold/mdpf/* only.

## Class 5 -- trail (denominator: 2 trails)

covered = false. server_access_logging = false. Trails opal-organization-trail (read data events on the -49financial, -bd, -cot, -inf
buckets only) and opal-served-key-write-trail (writes only, served firm headers). get-bucket-logging on opal-data-assets returned rc 0
with empty stdout. No read evidence exists for this bucket; the absence of read events here is NOT a count of zero readers.

## Partner-facing readers and what each writes where

1. build_portal_gold_accrual.py (schedule mdpf-accrual-bridge-daily, cron 13:40Z). Copies the staged body verbatim (:227 read, :245 plan, :290
   put) to portal/gold/mdpf/global/aggregate-aua-timeseries/<as_of>.json, the as_of read from the staged content (as_of_last).
2. What allows the staged bytes to land: an as_of with no existing dated key at 13:40Z (R5 never-overwrite is the only guard, :283-289).
3. What stops them: a dated key already present (head-object exists, skip). The served dated key for each day is written at about
   13:31Z, nine minutes before the accrual fires, so for the day's as_of the accrual skips. The writer of that folded dated key is the
   gold consolidator's portal write path (mdpf_gold_consolidator.py, validate-then-write around :2384-2471), traced only as far as its
   function; the Lambda target of the 13:30Z floor schedule is mdpf-gold-lambda.
4. Residual: if no dated key exists for an as_of at 13:40Z (a failed or late fold), the accrual writes the unfolded staged bytes under
   portal/ for that as_of. Whether this has happened is not measured here.

## Landing evidence (read-only head-object, side by side)

| Object | Bytes | ETag | LastModified |
|---|---|---|---|
| gold/mdpf_revamp/global/aggregate_aua_timeseries.json (staged) | 512084 | 1113c3c080c4acb0c38d800610ade827 | 2026-10-14T13:31:35Z |
| portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-13.json (served dated, as_of of the staged content) | 646107 | 3e0ac2b7dfaa1aa4ce25b499e0d3ea84 | 2026-10-14T13:31:48Z |

The two differ in size and ETag: the staged bytes did not land for as_of 2026-10-13. The served object is written 13 s after the
staged key, before the accrual fires. Surface stays PARTNER-FACING-CANDIDATE, not PARTNER-FACING.

## Instrument calls (exit code and deciding output)

- universe: rc 0, scanned 8812, 28 files naming both strings.
- aws head-object staged key: rc 0, ContentLength 512084.
- aws get-object staged key: rc 0, read only as_of_last (2026-10-13); body not retained in the record.
- aws head-object served 2026-10-13: rc 0, ContentLength 646107.
- aws scheduler get-schedule mdpf-accrual-bridge-daily: rc 0, State ENABLED, cron(40 13 * * ? *).
- aws scheduler get-schedule mdpf-feeder-backstop-daily: rc 0, State ENABLED, cron(52 12 * * ? *).
- aws events describe-rule mdpf-feeder-accelerator: rc 0, State ENABLED.
- aws events describe-rule mdpf-daily-refresh-trigger: rc 254, rule does not exist (no such clock trigger).
- aws lambda get-function-configuration opal-assets-mdpf-portal-publisher: rc 0, Role = opal-assets-mdpf-egress-publisher-role.
- comp-iam simulate, five roles: STATE ALLOWED x4, NOT-DECIDABLE x1.
- aws cloudtrail describe-trails: rc 0, 2 trails. get-event-selectors on each: rc 0 (see trail evidence).
- aws s3api get-bucket-logging opal-data-assets: rc 0, empty stdout; the same call on five other opal-data buckets also returned empty
  stdout. get-bucket-location on opal-data-assets (same shim) returned a document, so the shim is live; an in-estate positive control
  for a LoggingEnabled block was not found. Recorded as the spec requires; see the surprise row.

## Limits

- The worker face file that was handed to this worker carried the issuer's record-face section. It was read, and no value from it is
  cited or used as evidence: every number here came from this worker's own reads.
- IAM is Terraform plus simulation. The simulate for the egress role is NOT-DECIDABLE, not a deny.
- Liveness of the dispatch stages 6c and 6e is not measured here; the census records the trigger, not whether it runs to completion.
- No AWS write was made. No product file, Terraform file or script was changed.
