# FB-h-6 -- exec-summary trigger diagnosis (read-only, 2026-10-13)

Worker 0.9.0_WK_ADVI_FIRMBKTS~65. Record: `EXEC_SUMMARY_DIAGNOSIS.json` in this folder. Verdict: **INDETERMINATE**.

## What the reads show

**The put-events error text: none exists.** CloudTrail `LookupEvents` for `EventName=PutEvents`, window
2026-07-15T00:00:00Z to 2026-10-13T23:59:59Z (90 days), returns **0 events in all 17 enabled regions**
(us-east-1 first, then the 16 others). There is no PutEvents record from any principal, so no `errorCode`,
no `errorMessage` and no `FailedEntryCount` response exists to quote. Exact error text: **none (CloudTrail holds no PutEvents call)**.

**Positive control.** The same lookup method, unfiltered by PutEvents, returns events in us-east-1 for
`EventSource=events.amazonaws.com` (DescribeRule, ListTargetsByRule, DescribeEventBus, ListTagsForResource,
including reads by this worker's identity). So the lookup works; it does not prove PutEvents itself would be recorded.
An unbounded pagination of the control call timed out (rc=124 at 300 s) and was not retried.

**The bus.** `default` exists in us-east-1. Its describe output carries no resource policy.

**The rule.** `exec-summary-trigger` is ENABLED, with EventPattern
`{"detail-type":["chain-complete"],"source":["bd-pipeline.gold-chain"]}` and one target,
`exec-summary-generator`. The pattern matches the script's emitted `Source` `bd-pipeline.gold-chain` and
`DetailType` `chain-complete` exactly. The target Lambda's resource policy grants `lambda:InvokeFunction` to
`events.amazonaws.com` with `AWS:SourceArn` equal to this rule's ARN. So an event that reached the bus would match and invoke.

**The dispatcher role.** The script's comment names `bd-exporter-ec2-role`. The instance profile
`bd-exporter-profile` holds only that role. Two runners carry the profile: `bd-gold-layer-runner`
(i-01003b035d2988dfb, stopped, launched 2026-10-13T04:00:47Z) and `bd-gold-qa-runner` (i-0090b823a4a0997e3,
stopped, launched 2026-05-04T19:52:50Z). The role's `RoleLastUsed` is 2026-10-13T06:18:15Z. The inline policy
`events-emit`, statement `EmitChainCompleteEvents`, allows `events:PutEvents` on
`arn:aws:events:us-east-1:313476888478:event-bus/default` with no condition. No permissions boundary is set.
No Deny in the 16 inline policies or in the attached `bd-securities-access` v1 touches events. The only explicit
Deny is `cross-firm-bucket-deny` (s3:*, opal-data-cot). The AWS-managed `AmazonSSMManagedInstanceCore` v2 has no events
action. The Organizations SCP read was **denied** (AccessDeniedException), so SCP effect is absent.

**The script's test.** `gold_dispatch.sh:850` is `aws events put-events --entries file://... 2>&1 | grep -q
'"FailedEntryCount": 0'`. On the CLI's default JSON output a successful call prints that line, so it would pass.
The grep cannot match a non-zero count, CLI error text, text or yaml output, or a missing binary; each prints WARN
(`gold_dispatch.sh:853`). It cannot tell a call that never reached the events API from a rejected one. The
runner's configured output format, CLI version and default region are not readable by this order: **absent**
(claim inferred for the test's behaviour, absent for the runner).

## Why INDETERMINATE

- `EMITTED_NOT_MATCHED` needs a recorded emit. There is none.
- `DENIED` needs a recorded AccessDenied on PutEvents. There is none.
- `BUS_OR_RULE_ABSENT` is contradicted: both exist and match.
- `NOT_EMITTED_SCRIPT_TEST` would blame the grep. A successful call would pass the grep, so the
  WARN is not explained by the test alone, and the zero CloudTrail count says no call reached the API.

The defect therefore sits upstream of EventBridge: in the runner's `aws` invocation, its default region,
its credential identity, or in whether the chain closes with the emit gate open. The WARN itself
(`gold_dispatch.sh:853`) is cited from the order's cell text, held and not re-read; no run log was read.

## Fix owner (proposal)

The emit call and the runner's CLI configuration belong to the gold-chain pipeline lane
(`data/black_diamond/scripts/gold/gold_dispatch.sh`, `bd-gold-layer-runner`), not this read-only order. The rule,
bus, Lambda resource policy and role grant need no change. The next read is the runner-side one the order excludes
(CLI identity, default region and output, and the chain's WARN lines). The issuer 2.0.0_SA_COO~B1 routes it as a later cell.

## Surprise rows filed (ADVI_FIRMBKTS-D1-W65-S1 .. S3)

S1: the world has no CloudTrail PutEvents at all, across 17 regions, against the order's implied premise
that a failing put reaches the API. S2: the order's us-east-1-only read was extended to 17 regions, because the
runner's region is unreadable. S3: the Organizations SCP read is denied.

No product file was touched, nothing was emitted and no AWS write was made.
