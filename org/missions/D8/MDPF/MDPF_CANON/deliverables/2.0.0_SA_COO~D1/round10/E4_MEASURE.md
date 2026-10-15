# E4 -- the `opal-data-assets` reader (53 GB): what already exists, whether it names the reader, and the cheapest one-day measurement (fork of 2.0.0_SA_COO~D1, 2026-10-15 ~15:3xZ)

DRAFT, read-only. Every number below carries its source query; claims are labelled MEASURED (a read run in this session), INFERRED (derived from a measured number or a document) or UNVERIFIED. Nothing was enabled, written or committed. All AWS calls ran as `arn:aws:iam::313476888478:user/cloudops-dell1-agent-user` through `.tools/aws` (read-only `get`/`list`/`describe`/`simulate`; the CUR parquet read is 6.1 MB, under the box rule's 1 GB line).

## 1. What E4 is (the rulings)

- Laptop CTO placement `org/tier1_exec/1.0.0_SA_CTO/deliverables/RULING_20261015_063xZ_S3_EGRESS_ANOMALY_PLACEMENT.md` @06ffa2a6e8: "E4 `opal-data-assets` reader unknown: one day of request metrics on the bucket names the reader. Then decide." Owner dell1 (MDPF_CANON). No alarm, monitor or cost alert (standing moratorium).
- dell1 CTO `CTO_RULING_DELL1_S3_EGRESS_E3_E4_PLACEMENT_20261015.md` @e65d1fed56: E4 is MDPF_CANON's round-10 enrichment, "ONE day of S3 request metrics on the bucket (a measurement record, not an alarm), read and then decided. If the reader is outside MDPF, it goes to that project's owner."
- The 53 GB is `DataTransfer-Out-Bytes` of `opal-data-assets` over 10-11..10-14 (CRO findings `S3_EGRESS_ANOMALY_20261011_14_FINDINGS_20261015.md` @b05fee1182).

## 2. The number, re-measured (MEASURED)

Source: the hourly Cost and Usage Report, `s3://opal-cur-313476888478/cur/opal-cur/opal-cur/year=2026/month=10/opal-cur-00001.snappy.parquet` (6,109,130 B, LastModified 2026-10-15T09:57:14Z, `head-object`; 287,461 rows; usage through 2026-10-15 04:00Z). Filter `line_item_resource_id = opal-data-assets` and `line_item_usage_type` containing `DataTransfer-Out-Bytes` (1,070 rows).

| day | GB out | day | GB out |
|---|---|---|---|
| 10-01 | 29.77 | 10-09 | 40.66 |
| 10-02 | 4.43 | 10-10 | 0.06 |
| 10-03 | 2.43 | 10-11 | 29.59 |
| 10-04 | 0.15 | 10-12 | 0.81 |
| 10-05 | 2.52 | 10-13 | 9.56 |
| 10-06 | 0.71 | 10-14 | 13.15 |
| 10-07 | 54.50 | 10-15 (to 04Z) | 0.64 |
| 10-08 | 51.69 | total 10-01..10-15 | 240.7 |

10-11..10-14 sums to **53.1 GB** (equals the CRO's 53); 10-05..10-14 sums to 203 GB (the CRO's "200 GB since 10-05"). Denominator: 15 days, 1,070 rows. The bytes are GetObject (the CRO read the by-operation split: GetObject dominates; ListBucket is 1.4-3.5 GB a day across ALL buckets).

Hours with more than 0.5 GB (same query, by `line_item_usage_start_date` hour): 10-11 02Z 2.9, 03Z 3.7, 04Z 3.7, 17Z 2.7, 18Z 5.9; 10-13 15Z 1.9, 16Z 4.2; 10-14 12Z 1.3, 13Z 1.8, 15Z 2.3, 16Z 2.9, 17Z 2.3; 10-15 01-02Z 0.2-0.4. The biggest hours of the series are 10-08 23Z (22.2 GB) and 10-09 00Z (10.7 GB). So: bursts of a few GB an hour, US-daytime on 10-13/10-14, nights and afternoon on 10-11, ending by 10-15 04Z.

Request counts (same CUR, `Requests-Tier1` / `Requests-Tier2`, per day): 10-11 55,302 / 130,063; 10-12 21,349 / 53,399; 10-13 43,145 / 124,718; 10-14 33,248 / 166,828; 10-09 (the peak) 442,868 / 349,110.

## 3. What instruments already cover `opal-data-assets` (MEASURED, all read today)

| instrument | query | result |
|---|---|---|
| S3 request metrics | `s3api list-bucket-metrics-configurations --bucket opal-data-assets` | `{"IsTruncated": false}`: NO configuration |
| CloudWatch bucket metrics | `cloudwatch list-metrics --namespace AWS/S3 --dimensions BucketName=opal-data-assets` | only `NumberOfObjects` and `BucketSizeBytes` (storage); no request or `BytesDownloaded` series |
| server access logging | `s3api get-bucket-logging --bucket opal-data-assets` | empty: OFF |
| CloudTrail data events | `cloudtrail get-event-selectors --trail-name opal-organization-trail` | ReadOnly data events for `opal-data-49financial`, `opal-data-bd`, `opal-data-cot`, `opal-data-inf` only; WriteOnly for bd, cot, inf; `AdvancedEventSelectors` null |
| the second trail | `get-event-selectors --trail-name opal-served-key-write-trail` | advanced selector: writes only (`readOnly = false`) under `opal-data-inf/`, `opal-data-bd/`, `opal-data-cot/` `platinum/firm/`; logging true, last delivery 2026-10-15 09:00Z |
| Storage Lens | `s3control list-storage-lens-configurations` | only `default-account-dashboard` (free tier, no activity metrics; the CRO's read) |
| bucket facts | `get-bucket-versioning`; `cloudwatch get-metric-statistics BucketSizeBytes` | versioning Enabled; 352.8 GB (10-12), 353.2 GB (10-13); 19 top-level prefixes (`list-objects-v2 --delimiter /`): `_probe/ blackdiamond/ bloomberg/ code/ commonwealth/ config/ eclipse/ gateway/ gold/ json/ mdpf/ orion/ pathfinder/ portal/ schwab/ smartx/ sprint/ trueshares/ yahoo/` |

**Conclusion (MEASURED): no existing instrument records who read `opal-data-assets`. The CUR names the bucket, the hour and the bytes; it never names a principal.**

## 4. Can the reader be named now? NO. What the data does narrow (INFERRED, labelled)

1. **Not the round-9 MDPF tooling (INFERRED, from sizes MEASURED by `head-object`):** the SMArtX partitions the producer reads are 85,664 B (`fact_model_aum_daily/date=2026-10-14`) and 598,033 B (`fact_model_allocation_roster`); the gold timeseries object the readbacks read is 661,224 B. A readback or fixture run reads of the order of 6-10 MB. Even 1,000 such runs would be about 10 GB, and the 10-07..10-09 peaks (54, 52, 41 GB a day) PRE-DATE round 9. The CTO's note that "the round-9 publish added readers there" holds for requests, but the BYTES are not from this tooling.
2. **Egress means a reader outside AWS (INFERRED):** `DataTransfer-Out-Bytes` is billed only for bytes leaving AWS, so the reader is a box or a vendor-side puller, not a Lambda or an in-VPC task (in-region reads are not billed as Data Transfer Out; the CRO states the same for CloudFront).
3. **Likely a large-object reader (INFERRED, weakly):** the bucket is 353 GB across vendor prefixes (`blackdiamond/`, `orion/`, `schwab/`, `eclipse/`, `bloomberg/`, ...) and the bursts are a few GB an hour, against MB-sized MDPF gold objects. The daily request counts include in-region readers whose bytes are not billed as egress, so no bytes-per-request figure can be derived from them (not claimed).
4. **The dell1 agent identity is a candidate, not a finding (UNVERIFIED):** the E3 pulls of `opal-data-bd` (143 GB) were by this same user; CloudTrail has data events for `opal-data-bd` but not for `opal-data-assets`, so the same user's reads here would be invisible.

## 5. What it would take (and what each path can name)

| path | names | who may do it (simulated, `iam simulate-principal-policy`; SIMULATED, not exercised) | cost |
|---|---|---|---|
| A. S3 request metrics on the bucket (`PutBucketMetricsConfiguration`): the CTO's literal ruling | hour, bytes (`BytesDownloaded`), request counts; with prefix filters, the PREFIX. **NOT the principal.** | dell1 agent user: `s3:PutMetricsConfiguration` allowed, `s3:GetMetricsConfiguration` allowed | CloudWatch custom-metric rate: about 16 metrics per filter at $0.30 per metric-month. One day, one `EntireBucket` filter about $0.16; plus 19 top-level prefix filters about $3.0 (INFERRED: hour-prorated billing; if each metric were billed a full month the 20 filters would be about $96 -- UNVERIFIED, so the order starts with ONE filter plus a SMALL set) |
| B. CloudTrail ReadOnly data events for `opal-data-assets` on the organization trail (`PutEventSelectors`) | **principal ARN, source IP, user agent, key, `bytesTransferredOut` per request** | dell1 agent user: `cloudtrail:PutEventSelectors` **explicitDeny** (a guardrail on the audit trail; do not work around it). Needs the trail's owner (laptop / NFRA security) | $0.10 per 100,000 data events: the day's 200,000 reads (10-14) about $0.20; the 800,000 of the 10-09 peak about $0.80; log storage cents |
| C. Server access logging to a log bucket (`PutBucketLogging`) | requester ARN, remote IP, key, bytes sent | logging allowed on the source (simulated); the only existing target `opal-data-security-access-logs` admits only two source buckets (`opal-data-security`, `opal-security-evidence`: policy statement `AllowS3ServerAccessLogDelivery`), so a policy edit on a SECURITY bucket is needed | no per-event cost; log storage cents |

**The decision for the CTO (UNRESOLVED here):** the ruling's "request metrics" (A) names the hour, the bytes and (with filters) the vendor prefix, which is enough to place the reader's project from the prefix but not to name the principal. To name the principal and bytes (the task's goal), B or C is needed and each needs a seat other than the dell1 CloudOps agent (B: the trail owner; C: the security bucket's owner). The staged order below is path A, scoped to what the ruling authorises and what the dell1 seat may do; its last leg hands the prefix and hours to whoever runs B or C if the principal is still wanted.

## 6. What I could not verify

- Whether a metrics configuration bills hour-prorated (the S3 pricing statement is INFERRED); the order measures nothing about cost and keeps the filter set small.
- `PutBucketMetricsConfiguration` is allowed only by SIMULATION; it has not been exercised.
- The per-prefix size split of the 353 GB (listing 353 GB of objects is exactly the heavy enumeration to avoid).
- Whether a day will carry a burst (10-10: 0.06 GB, 10-12: 0.8 GB, 10-15 so far 0.64 GB); the order's decision rule extends to a second day when the CUR for the measured day reads under 2 GB.
- Whether the reader is a box (the egress bill says "outside AWS"); the principal stays unnamed on path A.
