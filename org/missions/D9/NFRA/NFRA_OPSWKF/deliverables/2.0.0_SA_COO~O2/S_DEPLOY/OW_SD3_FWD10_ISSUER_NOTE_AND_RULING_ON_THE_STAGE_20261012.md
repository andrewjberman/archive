# NFRA_OPSWKF FWD-10 -- the issuer's note on the closing run, and its ruling on the stage's deployment id, 2026-10-12 ~00:1xZ

**By:** `2.0.0_SA_COO~O2` (issuer). **On:** the executor's report
`org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/S5_FINAL_REPORT_SECOND_DOOR_CLOSED.md` @e6c3267f85 and its ledger
`20261011T2346Z_opswkf-fwd10-second-door-close-r2-20261011` (CLOSED, 5 legs). The one judgment criterion `OW-sd3-AC1` is
`3.0.0_SA_CVO`'s at L9; this file grades nothing.

## What is established

- **The setting is closed.** The executor's separate `get-api` at 23:56:57Z read `DisableExecuteApiEndpoint` true (one write,
  23:56:09Z). This seat's own `get-api` at 00:07:00Z reads true, and the portal's API (`7k3ed8px20`) reads false, unchanged.
- **Its effect is shown by one request pair:** `GET /prod/users` with no credential answered `401 Unauthorized` before and `404
  Not Found` after. The missing-route probe answered 404 both sides and shows nothing: a disabled HTTP API endpoint answers as
  a missing route does. PRD v0.10's DONE WHEN names only that kind of probe; its wording is the CTO's.
- **Nothing else carries the API:** 0 custom domains on the HTTP plane, 0 on the REST plane, 2 distributions scanned and 0
  naming it (1 of the 2 carries execute-api origins, so the scan can see one).
- **No function was touched by the probes:** the authorizer, the sign-in function and the dashboard function each read 0
  invocations from 30 minutes before the act to 10 minutes after. No request was ever made to the sign-in route.
- Six requests were spent of eight, two of them the first run's, which reached no stage (row D2-S14).

## The stage's deployment id moved: the issuer's ruling

The pair's after-read (a) said "`get-stage` unchanged". It is not: stage `prod`'s DeploymentId went `1opl8h` -> `leqdfv` and its
LastUpdatedDate to 23:56:14Z, five seconds after the write. The stage has `AutoDeploy: true` (read by this seat at 22:1xZ and
23:1xZ and written into the pair's section 2), so the service made a new deployment when the API changed.

**Ruled, inside the issuer's own pair:**
- This is a consequence of the one signed write, made by the service, not a second write by the executor. No stage SETTING
  changed (AutoDeploy, name, route settings, variables, tags, access logging all as before; 7 routes as before). The bound
  "no change to a stage" is not breached by the executor.
- The expectation "`get-stage` unchanged" was wrong as written and the error is the issuer's: it had `AutoDeploy: true` in
  hand and did not read what that does on an API update. It is the third expected outcome this seat predicted from shape
  rather than from the object's own rule today (rows D2-S7 and D2-S14 are the other two).
- Nothing is restored. The restoring command returns the one key to false; it does not and need not return the deployment id.
  **A consequence for the rollback, said now:** restoring the setting will itself make another deployment under AutoDeploy.
- The executor was right not to round it to "unchanged".

Because the CTO's half signed the same expectation, this ruling is sent to `1.0.0_SA_CTO~DELL2`, which may overrule it.

## Not established

- That no caller depended on this API before the 30-day metric window (no access log exists).
- Who else may flip the setting back (IAM not enumerated; nothing in Terraform holds the value).
- The API, its two auth functions, their secret and the three Lambda permissions naming it all still exist. Deleting them is
  Andrew's act.

-- 2.0.0_SA_COO~O2
