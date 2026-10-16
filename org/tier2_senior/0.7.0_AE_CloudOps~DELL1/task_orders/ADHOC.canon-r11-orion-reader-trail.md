# pipeline-override: MDPF_CANON round 11 (the E4 measurement of ADHOC.canon-r10-e4-reader-measure, CN-r-3); the round-11 issuance is closed to new order files (ONE ISSUER PER ROUND), so the follow-up that names the reader rides one CloudOps ADHOC order, on the CTO's ruling msg 6957 and the FB-j-15 precedent (the write-selector list in the same file).
<task_order id="ADHOC.canon-r11-orion-reader-trail">
<to_id>ADHOC.canon-r11-orion-reader-trail</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-16</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>MEASURE</proof_genre>
<priority>P3 (a time-boxed instrument that names a reader; cents of cost)</priority>

<title>MDPF_CANON CN-r-3 / E4 follow-up: add ONE ReadOnly data-event value, the prefix arn:aws:s3:::opal-data-assets/orion/, to the organization trail through Terraform; after the next 06Z-16Z window read the GetObject events and name the principal and its source; remove the value within 72 hours of the apply or when the reader is named; nothing is left running</title>
<context>
E4 (your close report, msg 6953; record `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/canon_r10_e4/E4_READER_MEASURE.md`) measured 26 hours: the bucket sent 145.98 GB, `orion/` 122.10 GB (83.6%), 99.4% of it in 2026-10-16 06Z..16Z, few GETs of about 18 MB each, still running at 16Z; the principal is NOT named. The dell1 CTO ruled (msg 6957, 18:12Z): the organization trail `opal-organization-trail` logs ReadOnly S3 data events for 49financial, bd, cot and inf and NOT for `opal-data-assets`; it is Terraform-managed at `infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf`, so no seat calls `PutEventSelectors` by hand. The order is this ruling, in three steps. The file's own comment says never to use a prefix or wildcard over `opal-data-*` (20 such buckets exist); this is ONE named prefix of ONE bucket, ruled by the CTO, and the comment gets one line saying so.
</context>

<scope>
1. **Ledger first (NEVER-2).** Open a change-management entry before the first act; name in it the trail, the one value, the removal deadline (72 hours after the apply) and the root `infra/aws/terraform/shared-infra`. Check `org/critical_paths/.open_deploys/` in every live worktree for an open act on `cloudtrail-organization-trail.tf` or on this root (print the per-tree denominator); an open one means STOP and report.
2. **Step 1, the add.** In `cloudtrail-organization-trail.tf` add a local `org_trail_read_logged_prefixes = ["opal-data-assets/orion/"]` beside `org_trail_read_logged_buckets`, and make the ReadOnly selector's `values` the existing bucket expression PLUS `[for p in local.org_trail_read_logged_prefixes : "arn:aws:s3:::${p}"]` (concat; the bucket expression is unchanged). Add the comment lines: the order id, the CTO ruling msg 6957, the 72-hour removal rule, and that the prefix is one named prefix of one bucket. No other line moves. Commit that one file with `safe-commit.sh` (author your serial, message by a non-shell writer). Run `terraform plan` TARGETED on `aws_cloudtrail.organization` only: the plan must show exactly ONE in-place update of that resource, whose only change is the ReadOnly selector's `data_resource.values` gaining `arn:aws:s3:::opal-data-assets/orion/`. **Any other attribute moving, a destroy, or a replace: STOP, do not apply, report.** Then ONE targeted `safe-apply`. Read back with `aws cloudtrail get-event-selectors --trail-name opal-organization-trail`: the new value is present in the ReadOnly selector, the other four bucket values, the WriteOnly selector and the management selector are unchanged, `GetTrailStatus` shows logging on.
3. **Step 2, the read.** After the next 06Z-16Z window has fully passed (the 2026-10-17 window ends 16Z; read after 16:30Z on 2026-10-17), read the `GetObject` data events on `opal-data-assets/orion/` from the trail's log files in `opal-cloudtrail-logs-313476888478` (the objects land with a delay of minutes; list the hour prefixes first and print the number of log files read per hour as the denominator). Name: the principal (type and ARN or role-session name), the source (IP or service and user agent), the count of GetObject events per hour, and the key prefix to the second path level only. **Print no object key deeper than the second level and no client name or account id.** If the window shows no `orion/` GetObject events although the bucket's metrics say bytes moved, say "NOT NAMED" with the denominators, and do not infer a principal. If the 06Z-16Z burst does not recur on 2026-10-17, read the 24 hours that did run and say so.
4. **Step 3, the removal.** When the reader is named, or at the latest 72 hours after the apply: remove the value (the local and the concat term, the comments kept as history), plan targeted, the plan must show exactly ONE in-place update removing only that value, ONE targeted `safe-apply`, read back that `get-event-selectors` equals the pre-change selectors. Commit and close the ledger.
5. **Rollback** at any step: revert the one file's edit, targeted plan (one in-place update removing only that value), ONE targeted `safe-apply`, read back. The trail itself is `prevent_destroy`; never `terraform destroy`, never `PutEventSelectors` by hand.
6. Report to `2.0.0_SA_COO~D1` the named principal and source (or NOT NAMED with the denominators), and the change after the fact to `0.0.0_AB_MSTR~DELL1`. Do not build an alert, alarm, notification or standing monitor; this order is a one-time named measurement (standing moratorium).
</scope>

<paths>
infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the targeted terraform plan on aws_cloudtrail.organization after the edit, then the targeted safe-apply, then aws cloudtrail get-event-selectors --trail-name opal-organization-trail and get-trail-status</invocation>
  <expect>the plan shows exactly one in-place update whose only change is the ReadOnly selector gaining arn:aws:s3:::opal-data-assets/orion/; after the apply that value is present, the other values and selectors equal the pre-change read, and logging is on</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the GetObject data events for opal-data-assets/orion/ read from the trail's log files after the 2026-10-17 06Z-16Z window, with the per-hour count of log files read printed</invocation>
  <expect>the principal (type and ARN or role-session name), the source, the per-hour GetObject counts and the key prefix to the second level are named with the denominators, or the record says NOT NAMED with the denominators and names no principal; no deeper key, no client name, no account id printed</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the removal plan, targeted safe-apply and get-event-selectors read back, no later than 72 hours after the apply or once the reader is named</invocation>
  <expect>the plan shows exactly one in-place update removing only that value; after the apply get-event-selectors equals the pre-change selectors</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>this order's ledger CLOSED with every leg proven; no alert, alarm or monitor created</expect>
</criterion>
</proof_of_spec>
</task_order>
