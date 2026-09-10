# NFRA_IAMROLES202609 -- IAM-s-5: DECLARED-vs-LIVE RECONCILER (member identity)

Cell: `IAM-s-5`. Serves outcome `FWD-4`. THIS ROW RECONCILES ONLY -- it does not dispose. Governance
disposition (removal, Terraform adoption, exemption, over-grant assessment) is `IAM-s-6`'s remedy,
never this one's (bound `C-TWO-REMEDIES`, D6).

## INSTRUMENT AND VINTAGE

Invocation: `comp-find '.' --corpus aws IAM_ROLE --all`

```
VINTAGE: Built from the estate as of 2026-09-10 05:57:16 UTC. Stitch source: stitch-codebuild
         built 2026-09-10T03:01:17Z.  manifest: 8ea66ca427c1
DENOMINATOR: 219 hit(s) across 219 aws node(s) scanned [corpus=aws types=IAM_ROLE]
```

This is a re-measurement of the LIVE AWS plane (`--corpus aws`, the served graph) AT THIS CELL'S OWN
VINTAGE (2026-09-10 05:57:16 UTC), not inherited from the L5 lane's vintage (2026-09-10 03:31:02
UTC) or from either brief-stage vintage. `measured`, not `inferred`.

**This is one plane only.** `comp-iam` (a separate instrument, parsing Terraform SOURCE, not the
live graph) reports 195 roles from that source plane. 195-vs-203 or 195-vs-219 is NOT a
DECLARED-vs-LIVE delta about this cell's question -- it is `comp-iam`'s own parser reach on a
different plane (its own run emits two NOTEs about mis-linked `orchestrator`/`scheduler` labels
pre-fix) and is not presented here as evidence about the undeclared set.

## DECLARED-vs-LIVE, THIS VINTAGE

```
DRIFT (scanned): DECLARED=203 LIVE-no-DECLARED=16
203 + 16 = 219  -- reconciles exactly against the denominator above
```

## THE UNDECLARED SET

The 16 `LIVE-no-DECLARED` members at this vintage, by name:

- bd-merge-daily-lambda-role
- bd-pipeline-task-role
- codebuild-semantic-clustering-role
- ecsTaskExecutionRole
- finbert-ec2-backfill-role
- lambda-ec2-runtime-monitor-role
- lambda-test-role
- opal-data-refresh-lambda-role
- opal-smartx-lambda-role
- portal-auth-lambda-role
- portfolio-management-lambda-role
- rds-monitoring-role
- seeking-alpha-scraper-role
- sentiment_query_api-role
- vpc-flow-logs-role
- workspace-sync-lambda-role

Count: 16 (measured, this vintage), matching the DRIFT line above.

## MEMBER IDENTITY

The L5 lane established the COUNT held at 16 across three vintages (population 208 -> 216 -> 219)
but explicitly did not measure whether the MEMBERS were the same 16, or a different 16 of equal
size. This section closes that gap by comparing this vintage's set, name for name, against the L5
lane's own enumerated list (2026-09-10 03:31:02 UTC).

| # | role name | L5 lane (03:31:02 UTC) | this vintage (05:57:16 UTC) | class |
|---|---|---|---|---|
| 1 | bd-merge-daily-lambda-role | present | present | SAME |
| 2 | bd-pipeline-task-role | present | present | SAME |
| 3 | codebuild-semantic-clustering-role | present | present | SAME |
| 4 | ecsTaskExecutionRole | present | present | SAME |
| 5 | finbert-ec2-backfill-role | present | present | SAME |
| 6 | lambda-ec2-runtime-monitor-role | present | present | SAME |
| 7 | lambda-test-role | present | present | SAME |
| 8 | opal-data-refresh-lambda-role | present | present | SAME |
| 9 | opal-smartx-lambda-role | present | present | SAME |
| 10 | portal-auth-lambda-role | present | present | SAME |
| 11 | portfolio-management-lambda-role | present | present | SAME |
| 12 | rds-monitoring-role | present | present | SAME |
| 13 | seeking-alpha-scraper-role | present | present | SAME |
| 14 | sentiment_query_api-role | present | present | SAME |
| 15 | vpc-flow-logs-role | present | present | SAME |
| 16 | workspace-sync-lambda-role | present | present | SAME |

`diff` between the L5 lane's sorted 16-name list and this vintage's sorted 16-name list is EMPTY
(exit 0). No member ARRIVED, no member LEFT. All 16 class SAME.

**THE FINDING:** the stable count of 16 (this cell's fourth vintage measured) is not merely
consistent with "the same 16" -- it now IS the same 16, name for name, across a ~2.5 hour gap
within the same day. Member identity is established at this vintage, not merely count stability.
This does not extend backward to the two brief-stage vintages (208- and 216-population), which
were never enumerated by name and cannot be re-diffed after the fact; the claim above is scoped to
the L5-lane-vintage-to-this-vintage comparison only.

## CHARACTER NOTES (carried for IAM-s-6; not a disposition)

These notes describe what each member IS, for the governance cell that disposes of them. They are
observations about role character, not a recommendation about any of them:

- `ecsTaskExecutionRole`, `rds-monitoring-role`, `vpc-flow-logs-role` -- AWS SERVICE-DEFAULT roles,
  the kind a console action or managed service mints on its own.
- `portal-auth-lambda-role`, `opal-data-refresh-lambda-role` -- attached to functions on the
  production serving path.
- `lambda-test-role` -- name suggests a test/scratch role rather than a serving-path role.
- The remaining 11 members are lambda/task/codebuild-style roles with no service-default or
  serving-path marker recorded here.

## SCOPE HELD

This deliverable reconciles. It does not state that any role belongs in Terraform, does not state
that any role should be dropped, and does not carry an over-grant or exemption judgment about any
member -- those are `IAM-s-6`'s remedy on this output, and `IAM-s-1`'s remedy on permission scope,
per bound `C-TWO-REMEDIES`.
