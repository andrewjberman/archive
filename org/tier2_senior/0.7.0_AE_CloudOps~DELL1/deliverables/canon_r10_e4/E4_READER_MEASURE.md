# E4 reader measure: S3 request metrics on opal-data-assets, 26 hours (0.7.0_AE_CloudOps~DELL1, 2026-10-16)

Order `ADHOC.canon-r10-e4-reader-measure`. Instrument: eleven request-metrics configurations (`e4-entire` plus ten prefix filters), live 2026-10-15T15:59:00Z to 2026-10-16T18:05:58Z, then removed. Every number below carries its source: CloudWatch `AWS/S3` `BytesDownloaded`, `AllRequests`, `GetRequests` (Sum, period 3600, dimensions `BucketName=opal-data-assets`, `FilterId=<id>`), MEASURED; the CUR figures are MEASURED from `s3://opal-cur-313476888478/cur/opal-cur/opal-cur/year=2026/month=10/opal-cur-00001.snappy.parquet`. Raw JSON: `L3_raw_24h/`, `L3_raw_26h/`. Tables: `L3_24h_table.txt` (read 16:03Z), `L3_26h_table.txt` (read 18:04Z).

## 1. What was named

**The prefix is `orion/`, the hours are 2026-10-16 06Z to 16Z, and the principal is NOT named.**

| scope | bytes downloaded | share of `e4-entire` | denominator |
|---|---|---|---|
| `e4-entire` (whole bucket), 26 hourly buckets 2026-10-15 16Z .. 10-16 17Z | 145.98 GB | 100% | 26 hours x 11 ids |
| `orion/` | 122.10 GB | 83.6% | |
| `schwab/` | 11.53 GB | 7.9% | |
| `blackdiamond/` | 4.78 GB | 3.3% | |
| `smartx/` | 0.43 GB | 0.3% | |
| `portal/`, `eclipse/`, `gold/`, `gateway/`, `bloomberg/`, `mdpf/` | 0.07, 0.05, 0.02, 0.0002, 0, 0 GB | under 0.1% each | |
| bytes in the nine prefixes the ten filters do not cover | 7.00 GB | 4.8% | 19 top-level prefixes, 10 filtered |

At 24 hours (window 10-15 15:59Z to 10-16 15:59Z) the figures were 134.2 GB total and 111.5 GB `orion/` (83.1%); the two extra hours (16Z, 17Z) added 10.6 GB of `orion/` in the 16Z hour and almost nothing in 17Z.

**The burst.** 99.4% of the `orion/` bytes fall in the hours 10-16 06Z .. 16Z (11 hourly buckets; 07Z is nearly empty, 0.03 GB). The largest hours (GB, `orion/`): 12Z 29.3, 09Z 24.7, 06Z 14.7, 10Z 10.7, 16Z 10.6, 08Z 9.8; 11Z 5.5, 13Z 7.8, 14Z 5.0, 15Z 3.1. Before 06Z the whole bucket moved under 2.3 GB an hour in every hour. In the ten active hours (every hour of 06Z .. 16Z except 07Z) `orion/` is 62% to 95% of the bucket's bytes in that hour (lowest 14Z at 62%, highest 06Z at 95%). Request counts over the same prefix are small (`orion/`: 7,170 requests, 6,776 GETs in 26 hours; 122 GB over about 6,800 GETs is about 18 MB a GET), so the reader pulls few, large objects. The pattern is a few GB to 30 GB an hour for eleven hours, still running at 16Z when the window ended.

## 2. Cross-check against the CUR (the decision rule)

Rule printed in the order: a CUR day under 2 GB means a second day. The measured day was not quiet. CUR `DataTransfer-Out-Bytes` for `opal-data-assets` (file LastModified 2026-10-16T17:32:30Z, usage through 13Z, 1,179 bucket rows): day 2026-10-16 up to 13Z = 100.86 GB; the window hours present (22 of 26, to 13Z) = 104.57 GB. Hour by hour the CUR and the metrics agree in shape and size (06Z CUR 14.35 vs 14.69 `orion/`; 09Z 24.24 vs 24.70; 12Z 27.50 vs 29.33). `BytesDownloaded` counts all downloads and the CUR only bytes billed as leaving AWS, so the metric is the larger figure. No second day was run.

## 3. What the data says and does not say

- NAMED (MEASURED): the prefix `orion/`, the hours, the bytes, the share and the object-size scale above.
- INFERRED: the egress is billed Data Transfer Out, so the reader is outside AWS (a box or a vendor-side puller); the CUR bills no in-region read as egress, yet the CloudWatch bytes and the CUR bytes match hour by hour.
- **NOT NAMED: the principal.** Request metrics carry no requester. The trail change that would (`cloudtrail:PutEventSelectors`) is explicitly denied to this identity and is not worked around. Access logging to a log bucket needs a policy edit on a security bucket owned elsewhere.
- NOT excluded, UNVERIFIED: the co-seated AE lanes on this box share the IAM user `cloudops-dell1-agent-user`. This seat's own requests in the window are listed in `SELF_TRAFFIC_NOTE.md` and none touched `orion/`; the other lanes' requests cannot be subtracted. A local process listing at 16:3xZ showed no process naming `orion` or the bucket. The E3 pulls of `opal-data-bd` were by this user, so this user is a candidate, not a finding.
- The seat's own acts inside the window moved the `gold/`, `portal/` and `gateway/` hours slightly (the gold dry runs and the before and after prints); they are 0.02% of the bytes and cannot change the reading.

## 4. Hand-off

To `2.0.0_SA_COO~D1`, for the CTO to route: prefix `orion/`, hours 2026-10-16 06Z to 16Z (11 hours, 122.1 GB, 83.6% of the bucket's 146.0 GB in the 26 hours), the burst may still be running. To name the principal the CTO routes a trail (`ReadOnly` data events for `opal-data-assets`, `PutEventSelectors`) or an access-log step to its owner; this seat cannot do either.

## 5. Removal and cost

L4: all eleven ids deleted at 2026-10-16T18:05:58Z by `delete-bucket-metrics-configuration`, each rc=0; `list-bucket-metrics-configurations` reads `{"IsTruncated": false}` (`L4_remove.txt`). `get-bucket-logging` still empty; bucket policy sha256 `fc779219ebda5268` unchanged from before the order. Nothing else was created: no alarm, dashboard, SNS topic or schedule. Cost: the order's estimate (about $1.8 for one day, INFERRED) is not yet a measurement; the Cost Explorer day for 2026-10-16 appears after the next billing refresh and will be recorded by a note appended here.
