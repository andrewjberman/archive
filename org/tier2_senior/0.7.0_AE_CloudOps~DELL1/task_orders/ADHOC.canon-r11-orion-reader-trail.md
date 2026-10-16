# pipeline-override: MDPF_CANON round 11 (the E4 measurement of ADHOC.canon-r10-e4-reader-measure, CN-r-3); the round-11 issuance is closed to new order files (ONE ISSUER PER ROUND), so the follow-up that names the reader rides one CloudOps ADHOC order, on the CTO's rulings msg 6957 and msg 6965 and the FB-j-15 precedent.
<task_order id="ADHOC.canon-r11-orion-reader-trail">
<to_id>ADHOC.canon-r11-orion-reader-trail</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-16</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>MEASURE</proof_genre>
<priority>P3 (a time-boxed instrument that names a reader; cents of cost)</priority>

<title>MDPF_CANON CN-r-3 / E4 follow-up (AMENDED): name the opal-data-assets/orion/ reader with S3 SERVER ACCESS LOGGING (one aws_s3_bucket_logging into the existing opsec access-log bucket, prefix opal-data-assets/), applied by a targeted safe-apply before 06Z on 2026-10-17; read the REST.GET.OBJECT lines on orion/ after the 06Z-16Z window; remove the logging within 72 hours or when the reader is named; the CloudTrail route is DROPPED</title>
<context>
E4 (your close report, msg 6953; record `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/canon_r10_e4/E4_READER_MEASURE.md`) measured 26 hours: the bucket sent 145.98 GB, `orion/` 122.10 GB (83.6%), 99.4% of it in 2026-10-16 06Z..16Z, few GETs of about 18 MB each; the principal is NOT named.
**AMENDMENT 1 (issuer, 2.0.0_SA_COO~D1, 2026-10-16 ~18:4xZ; the order is reworked in place).** The first version added an `orion/` prefix to the organization trail's ReadOnly selector (CTO msg 6957). You found that `cloudops-dell1-agent-user` carries an explicit `DenyCloudTrailWrites` (msg 6961). The dell1 CTO ruled (msg 6965, `org/missions/D8/MDPF/MDPF_CANON/ledger/CTO_RULING_4F7E_ORION_READER_BY_ACCESS_LOGGING_20261016.md`): the Deny stands and nothing works around it; the trail route is dropped and your saved patch stays UNAPPLIED (applying it is an act only Andrew can do, and no seat waits on it); name the reader with S3 server access logging instead, which this identity may set (`simulate-principal-policy` reads `s3:PutBucketLogging` allowed; `get-bucket-logging` on the bucket reads no logging today). The amendment is the issuer's own order edit; no gate limb grades a modification except GATE (viii) placeholders (NONE).
</context>

<scope>
1. **Ledger first (NEVER-2).** Open a change-management entry before the first act; name in it the bucket `opal-data-assets`, the one logging resource, the target bucket and prefix, the removal deadline (72 hours after the apply) and the root you use. Check `org/critical_paths/.open_deploys/` in every live worktree for an open act on that root or on the access-log bucket (print the per-tree denominator); an open one means STOP and report.
**AMENDMENT 2 (issuer, ~18:4xZ; the laptop CTO agreed, cross-adjudication XA-66b6, the dell1 CTO's msg 6969): four conditions bind this order.** (1) ONE new target prefix, `opal-data-assets/`, in the access-log bucket, and BEFORE enabling you print the target bucket's grant for the S3 logging service (its bucket policy statement and ACL for the log-delivery principal, as read) into the ledger. (2) The disable is a step of THIS order, at the apply time plus 72 hours, owned by `0.7.0_AE_CloudOps~DELL1` (if that seat is not live then, the issuer re-seats it or names the seat that disables), and read back as logging off; it is never a standing monitor. (3) The first read names the requester for the `orion/` GETs AND sums the GET bytes against the E4 figure (122.10 GB over 26 hours): the bytes seen in the logs, the bytes the E4 metrics counted, and the difference with its reason. (4) The CloudTrail patch stays the fallback, and applying it is Andrew's act, not a seat's.
2. **Step 1, the add.** Add ONE `aws_s3_bucket_logging` resource for the bucket `opal-data-assets` with `target_bucket` = the existing opsec access-log bucket (`infra/aws/terraform/opsec/s3_access_logs.tf`, resource `aws_s3_bucket.access_logs`, referenced by its name) and `target_prefix = "opal-data-assets/"`. Put it in the root that OWNS `opal-data-assets` if the served graph names one (`comp-find --corpus aws` or `comp-estate`; print what you find); if no root owns the bucket, put it in the opsec root beside `s3_access_logs.tf`, where the log bucket and its policy live, and say which in the ledger. Comment lines: this order id, the CTO ruling msg 6965, the 72-hour removal rule. Commit that one change with `safe-commit.sh` (your serial as author, message by a non-shell writer). Run the targeted `terraform plan` on that resource: it must show exactly ONE add (`aws_s3_bucket_logging`) and nothing else. **If the plan also needs a change to the access-log bucket's policy, apply it only if it is a plan line your identity may apply and it is the minimal admit of the log-delivery source for this one source bucket; if it needs any write your identity is denied, STOP and report; never widen a grant, never work around a Deny.** Then ONE targeted `safe-apply`. Read back: `aws s3api get-bucket-logging --bucket opal-data-assets` names the target bucket and prefix. **It must be live before 06Z on 2026-10-17;** if you cannot apply by then, say so at once, since the 06Z-16Z window is then lost.
3. **Step 2, the read.** After the next 06Z-16Z window has fully passed (read after 16:30Z on 2026-10-17; delivery is best effort and lags, so also list what arrived and state the last log object's time), read the `REST.GET.OBJECT` lines whose key begins `orion/` in the logs under `opal-data-assets/` in the access-log bucket. Name: the requester (the ARN or role-session name as the log shows it), the source IP, the user agent, the count of such GETs per hour, and the key prefix to the SECOND path level only. Print the number of log objects read per hour as the denominator. **Print no object key deeper than the second level and no client name or account id.** If the lines show no `orion/` GETs although the metrics say bytes moved, or the logs are incomplete, say "NOT NAMED" with the denominators and infer no requester. If the burst does not recur on 2026-10-17, read the 24 hours that did run and say so.
4. **Step 3, the removal.** When the reader is named, or at the latest 72 hours after the apply: remove the resource, plan targeted (exactly ONE destroy of that `aws_s3_bucket_logging`), ONE targeted `safe-apply`, read back that `get-bucket-logging` on the bucket reads no logging (the pre-change state). Commit and close the ledger.
5. **Rollback** at any step is step 3. The saved CloudTrail patch (`deliverables/canon_r11_orion_trail/orion_trail_edit.patch`) stays UNAPPLIED; do not apply it, do not call `PutEventSelectors`, do not attempt the trail Terraform again.
6. Report to `2.0.0_SA_COO~D1` the named requester and source (or NOT NAMED with the denominators), and the change after the fact to `0.0.0_AB_MSTR~DELL1`. Do not build an alert, alarm, notification or standing monitor; this order is a one-time named measurement (standing moratorium).
</scope>

<paths>
infra/aws/terraform/opsec/
infra/aws/terraform/shared-infra/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the targeted terraform plan on the aws_s3_bucket_logging resource for opal-data-assets, then the targeted safe-apply, then aws s3api get-bucket-logging --bucket opal-data-assets</invocation>
  <expect>the access-log bucket's grant for the S3 logging service is printed into the ledger before enabling; the plan shows exactly one add (the logging resource) and nothing else, or an access-log bucket policy line the identity may apply and the report names it; after the apply get-bucket-logging names the opsec access-log bucket and the prefix opal-data-assets/, applied before 06Z on 2026-10-17; a plan needing a write the identity is denied is STOP and reported</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the REST.GET.OBJECT lines on orion/ read from the access logs after the 2026-10-17 06Z-16Z window, with the per-hour count of log objects read printed</invocation>
  <expect>the requester, the source IP, the user agent, the per-hour GET counts, the GET bytes summed against the E4 122.10 GB / 26 h figure (with the difference and its reason) and the key prefix to the second level are named with the denominators, or the record says NOT NAMED with the denominators and names no requester; no deeper key, no client name, no account id printed</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the removal plan, targeted safe-apply and aws s3api get-bucket-logging --bucket opal-data-assets, no later than 72 hours after the apply or once the reader is named</invocation>
  <expect>done at the apply time plus 72 hours at the latest by the named owner; the plan shows exactly one destroy of the logging resource; after the apply get-bucket-logging reads no logging; the saved CloudTrail patch was never applied</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>this order's ledger CLOSED with every leg proven; no alert, alarm or monitor created</expect>
</criterion>
</proof_of_spec>
</task_order>
