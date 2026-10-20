# TCKT_VNEXT D2-S46: who holds `lambda:InvokeFunction` on the functions behind the portal authorizer (READ cell; `2.0.0_SA_COO~V2`, 2026-10-20 ~06:0xZ)

Asked by the CTO (msg 11222): count the principals by name; read IAM only; the CTO rules the fix on that count. Nothing was written, granted or invoked.

## Scope read
- **The functions:** the 20 Lambdas integrated (AWS_PROXY) on routes of the portal API `7k3ed8px20` whose `AuthorizationType` is `CUSTOM` (authorizer `portal-jwt-authorizer` -> `opal-portal-authorizer`): 123 of the API's 126 routes. List: `S46_FUNCTIONS_BEHIND_AUTHORIZER.json`. The 3 `NONE` routes reach only `opalinvest-auth-handler` (not counted). Not read: any other API or authorizer (the portfolio-management REST authorizer).
- **The IAM denominator (account 313476888478), `aws iam get-account-authorization-details`, one call, read 2026-10-20:** 7 users, 3 groups, 335 roles, 79 managed policies (local and AWS-managed). Matched with the script `s46_census.py` (an Allow statement whose Action covers `lambda:InvokeFunction`, by `lambda:InvokeFunction`, `lambda:*`, `lambda:Invoke*` or `*`, and whose Resource covers a function ARN or `*`). Raw result: `S46_CENSUS_RESULT.json`.

## The count, by name
**Identity principals that can invoke these functions: 4 users, 4 roles (8 in all).**

| principal | kind | functions | through | note |
|---|---|---|---|---|
| `Andrew_Berman` | IAM user | all 20 | group `AdministratorAccessOpalCapital` (`AdministratorAccess`) | |
| `Andrew_Berman_Console` | IAM user | all 20 | the same group | |
| `cloudops-dell1-agent-user` | IAM user | all 20 | the same group, and group `cloudops-dell-agents-group` (`cloudops-dell-agent-deploy-policy`) | an agent identity |
| `cloudops-dell2-agent-user` | IAM user | all 20 | the same two groups | an agent identity; the one this box uses |
| `trade-submission-lambda-role` | role | `trade-dashboard-api`, `trade-identifier-cache`, `trade-submission-handler`, `trade-workflow-handler` | inline `trade-submission-policy` | trust: the Lambda service |
| `irpt-export-render-role` | role | `irpt-export-render` | inline `irpt-export-render-submit-policy` | trust: the Lambda service |
| `amgt-global-freshness-snapshot-scheduler-role` | role | `opal-amgt-scoped-api` | inline `amgt-global-freshness-snapshot-scheduler-policy` | trust: `scheduler.amazonaws.com` |
| `gateway-global-internal-reader-role` | role | `opal-amgt-scoped-api` | inline `gateway-global-harvest-published-invoke-policy` | trust: `role/opal-gateway-role` |

- **Three more roles matched only a `Deny NotAction` statement** (`gateway-blackdiamond-read-role`, `gateway-schwab-catalog-read-role`, `gateway-schwab-read-role`: each carries a `Deny` with `NotAction` of the three S3 read actions, so it is S3-read-only and denies Lambda): they hold no invoke grant and are not counted.
- **No explicit Deny of `lambda:InvokeFunction`** on any counted principal; none carries a permissions boundary.
- **Resource policies (all 20 read):** `apigateway.amazonaws.com` on every function (the portal API), plus `events.amazonaws.com` on `irpt-directory-search` (the keep-warm rule). No other principal.

## What it means for the row
The two Administrator users and the two cloudops agent users hold every function through `AdministratorAccess`; the direct-invoke bypass is therefore open to exactly those four named users on all 20 functions, and no narrower grant exists for them to lose. The four roles hold one to four functions each, none of them the ticket service. **`opal-ticket-api` is invokable through IAM by the four users only** (plus API Gateway). Narrowing would mean taking `AdministratorAccess` from the agent users or adding an explicit Deny of `lambda:InvokeFunction` on the function for them; that is the CTO's ruling.

## Not read (limits)
SCPs and the organisation's policies; session policies; cross-account roles that could assume one of the four roles; trust policies' deeper chains (who can assume `gateway-global-internal-reader-role` beyond its named trust); any identity not in this account; the portfolio-management authorizer's functions; whether any of the four users' keys are in use. The matcher reads Allow statements by pattern; a `Condition` on a counted statement would have been flagged (none was).
