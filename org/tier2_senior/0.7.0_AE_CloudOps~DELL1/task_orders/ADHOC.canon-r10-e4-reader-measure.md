# pipeline-override: MDPF_CANON round 10 -- the round-10 issuance is closed to new order files (ONE ISSUER PER ROUND), so the E4 one-day measurement rides one CloudOps ADHOC order, on ADHOC.canon-r9-trend-publish-tonight and the MDPF_CANON round-2, 4, 6, 7 precedents.
# TO MDPF_CANON CN-r-3: one day of S3 request metrics on opal-data-assets (E4, a measurement record, not an alarm) -- enable, read, name the hour/prefix/bytes, remove (DELL1 CloudOps)
<task_order id="ADHOC.canon-r10-e4-reader-measure">
<to_id>ADHOC.canon-r10-e4-reader-measure</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-15</date>
<status>complete</status>
<risk>WORLD</risk>
<proof_genre>MEASURE</proof_genre>
<priority>P3 (a measurement record; BEHIND the CTO's written word on the filter set and cost, and the issuer's GO -- see PRECONDITIONS)</priority>

<title>MDPF_CANON CN-r-3 / E4: enable S3 request metrics on opal-data-assets with ONE EntireBucket filter and a short named prefix list for ONE day, read BytesDownloaded and request counts by hour and prefix, write the measurement record, then remove exactly the configuration ids this order created; nothing is left running, no alarm, no dashboard, no standing metric</title>
<context>
The 53 GB: `opal-data-assets` shipped 53.1 GB of DataTransfer-Out over 2026-10-11..10-14 (the hourly CUR; `E4_MEASURE.md`, section 2) and 240.7 GB since 10-01, and NO instrument names the reader: no request-metrics configuration, no access logging, no CloudTrail data events on the bucket (`E4_MEASURE.md`, section 3). Placement: laptop CTO `RULING_20261015_063xZ_S3_EGRESS_ANOMALY_PLACEMENT.md` @06ffa2a6e8 and dell1 CTO `CTO_RULING_DELL1_S3_EGRESS_E3_E4_PLACEMENT_20261015.md` @e65d1fed56: "ONE day of S3 request metrics on the bucket (a measurement record, not an alarm), read and then decided".
What this order can and cannot name: request metrics give BytesDownloaded, request counts and latency by HOUR and by PREFIX; they do NOT name the principal. The dell1 CloudOps agent user is simulated ALLOWED `s3:PutMetricsConfiguration`/`s3:GetMetricsConfiguration` and simulated explicitly DENIED `cloudtrail:PutEventSelectors` (the audit trail is not yours to change; do not work around it). If the day names a prefix but the principal is still wanted, the closing report hands the prefix and hours to the CTO, who routes the trail or access-log step to its owner.
The rail and the moratorium (CLAUDE.md section 5): this is a one-time instrument that is removed again. Create NO CloudWatch alarm, NO dashboard, NO SNS topic, NO scheduled reader. The box rule of the dell1 CTO (a read expected to pull more than about 1 GB out of AWS states why in your log first) is met: every read below is a CloudWatch statistic or a CUR parquet of about 6 MB.
</context>

<scope>
1. Open a deploy ledger (NEVER-2) BEFORE the first act, slug `mdpf-canon-r10-e4-reader-measure`: legs L0 (preconditions), L1 (before print), L2 (enable), L3 (read), L4 (remove), L5 (record). Name in it the bucket, the configuration ids, the start and stop times and the rollback route. Open and COMMIT the sentinel `org/critical_paths/.open_deploys/mdpf-canon-r10-e4-reader-measure.json` with it.
2. **PRECONDITIONS, read first; any false means do nothing and report which:**
   a. The issuer's GO is a broker message from `2.0.0_SA_COO~D1` citing this order's path. The CTO's written word is IN HAND: (i) the filter set is the `EntireBucket` filter plus the ten prefix filters named in L2, eleven ids, ruled (b) by `1.0.0_SA_CTO~DELL1` msg 6053 ("the EntireBucket filter plus the ten prefix filters, for 24 h, all eleven removed after with the removal read back"); (ii) the cost, about $1.8, is accepted in the same message; (iii) removing the configurations at the end is part of the measurement (msg 6051: "removed after, with the removal read back; a measurement record only, not an alarm"). Without the GO this order is `staged` and WAITS; on the GO, flip the status to pending.
   b. `s3api list-bucket-metrics-configurations --bucket opal-data-assets` reads `{"IsTruncated": false}` (no configuration exists; the issuer read it so on 2026-10-15). Any existing configuration is somebody's: STOP and report it, change nothing.
   c. No open deploy sentinel names `opal-data-assets` other than this order's own (read `org/critical_paths/.open_deploys/` in every live worktree: `git worktree list --porcelain`, then `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`; union them; print the per-tree denominator).
   d. The identity you run as can do it: `aws iam simulate-principal-policy` for `s3:PutMetricsConfiguration` on the bucket reads allowed (it did on 2026-10-15); a deny is a STOP.
3. **ORDER OF ACTS (the order is the safety):**
   a. **L1 Before print.** The metrics-configuration list (expect empty), `get-bucket-logging` (expect none, unchanged by this order), the bucket's CloudWatch series list (expect only `NumberOfObjects` and `BucketSizeBytes`), and the CUR hourly series for the bucket for the previous 72 hours (the issuer's query, `E4_MEASURE.md` section 2) printed as the baseline.
   b. **L2 Enable.** `put-bucket-metrics-configuration` with these ids and no other: `e4-entire` (no filter: the whole bucket) and one filter per prefix of this list, each id `e4-pfx-<prefix without the slash>`: `blackdiamond/`, `orion/`, `schwab/`, `eclipse/`, `bloomberg/`, `gateway/`, `gold/`, `mdpf/`, `smartx/`, `portal/`. (The ten are the vendor and served prefixes among the bucket's 19; the CTO may shorten or extend the list in the GO. Do NOT add a filter the GO does not name.) Record the start time, read each configuration back, and print the ids.
   c. **L3 Read (after 24 hours, then once more at 26 hours).** For each id: `cloudwatch get-metric-statistics` for `BytesDownloaded` (Sum), `AllRequests` and `GetRequests` (Sum), period 3600, over the 24 hours since the start, with the dimensions `BucketName=opal-data-assets` and `FilterId=<id>`. Print one table: hour, `e4-entire` bytes, and each prefix's bytes; the totals; the denominators (24 hours, 11 ids). Also read the CUR for the same day (it lags by about 12 hours): the day's DataTransfer-Out GB for the bucket, as the cross-check that the measured day carried the kind of burst the CRO saw. **Decision rule printed before reading:** if the CUR's day for the bucket reads under 2 GB, the day was quiet and proved nothing: extend the SAME configurations a second 24 hours (report that you did) and read again; never extend past 48 hours without a new GO.
   d. **L4 Remove.** After the last read: `delete-bucket-metrics-configuration` for EXACTLY the ids L2 created (the list from L1/L2; a delete of a configuration, never of an object), then `list-bucket-metrics-configurations` reads empty again. A configuration this order did not create is never touched. The ledger lists every id removed.
   e. **L5 The record.** Write `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/canon_r10_e4/E4_READER_MEASURE.md`: the table of L3, the cross-check, and a plain statement of what was named. If one prefix carries most of the bytes in the burst hours, say which prefix and which hours (the bytes, the share, the denominator). **The principal is NOT named by this order**: say so, and hand the prefix, the hours and the share to the issuer, who gives them to the CTO to route (the trail change `cloudtrail:PutEventSelectors` is explicitly denied to your identity; an access-log or trail step belongs to the owner of that surface). Then report to `2.0.0_SA_COO~D1`, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
4. **Rollback and stop conditions:** the only changes are the configurations this order created, and the rollback of each is its delete. If L2 fails midway, delete any id already created and report. If a read at L3 returns no datapoint for an id after 30 minutes of the configuration existing, say so; do not retry by changing the filter. There is no S3 object write or delete anywhere in this order.
5. **Cost (an estimate; the issuer's INFERENCE, not a measurement):** CloudWatch bills request metrics at the custom-metric rate, about 16 metrics per filter at $0.30 per metric-month. At hour-prorated billing the one-day cost is about $0.16 for `e4-entire` plus about $0.16 per prefix filter, so about $1.8 for the eleven ids; if billing were a full month per metric the ceiling is about $53. The cost to be read from the next Cost Explorer day and recorded in L5.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the L1 before print (metrics-configuration list, logging, CloudWatch series list, the 72-hour CUR baseline), then put-bucket-metrics-configuration for the eleven ids and the read-back of each</invocation>
  <expect>the list was empty before; after L2 exactly the eleven ids named in the GO exist and no other; get-bucket-logging and the bucket policy are unchanged</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>cloudwatch get-metric-statistics BytesDownloaded, AllRequests and GetRequests per FilterId at period 3600 over the 24 hours, and the CUR day read for the same bucket</invocation>
  <expect>one table with 24 hours and 11 ids and its totals; the day's CUR GB printed beside it; if the CUR day was under 2 GB the second day was run and read</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>delete-bucket-metrics-configuration for the ids created, then list-bucket-metrics-configurations, then python .tools/deploy_ledger.py check</invocation>
  <expect>the list reads empty; E4_READER_MEASURE.md written naming the prefix, hours, bytes and share (or stating none dominated) and stating the principal was not named; the ledger CLOSED with every leg proven and the sentinel committed and closed</expect>
</criterion>
</proof_of_spec>
</task_order>
