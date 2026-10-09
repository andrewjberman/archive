# Never-widen half (COO) -- OG-da-1, the data_refresh admission fails closed

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~07:4xZ.
Against: the ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-da-1.md` @d9539cc0b7,
sections 5, 6 and 7. The CTO half (section 0, the recognisers and the composition) is `1.0.0_SA_CTO~Z`'s @93ddbb1288.

## Read at signing (issuer, live)

- **No edit since the ask.** `git diff d9539cc0b7 HEAD -- infra/aws/lambda/data_refresh/ infra/aws/terraform/data-refresh/`
  is empty, so the CTO half's void condition has not fired.
- **The rollback target is the running code.** `opal-data-refresh-api` reads `CodeSha256 E4944Imr7Y4S4//rTR6HN5sbwczbwLw5DcaH4IZ0D0E=`,
  Active, Successful, LastModified 2026-08-03T17:08:27Z. The artifact version `WJQGGIAlTSMp0Vny8avvQ7LxflVuvLf6` reads
  19753 B, ETag `15413b4ac88881c9b0e19dae0eceb215`, metadata `content-sha256` = that same CodeSha256.
- **Writers of the served property (the execution table `opal-data-refresh-executions`), counted by a repo-wide read of
  the table name: N = 2 code writers.** `opal-data-refresh-api` (`lambda_function.py`, `check_triggered_by.py`, one
  function) and the yang pipeline's `varflag-check` (`varflag_check.py`). This act changes only the first. Its rule after
  the act is in the ask's section 2: it refuses before any write where it used to admit, and writes nothing new.

## SIGNED: section 5, the blast radius

One Lambda's code, `opal-data-refresh-api`, through `module.data_refresh_api` only. The role, environment, limits,
runtime, routes, the authorizer, the API, `portal-time-machine` and `varflag-check` are outside the act. The only
behaviour moved is the admission decision.

**Both branches, from the function's own rule.**
- A caller that is `Dev` or Opal-internal (`tier == 'internal'` or `firmId == 'opal-capital'`, exact match) is admitted
  and writes its execution record as today. The ask measured 124 of 124 calls in 14 days on this branch, 6 of 6 roles.
- Any other caller (empty `userType` with no internal signal, the string `"null"` firm, no authorizer context) is refused
  before any write. No record is written, and no stored record changes. Method 3 fired 0 times in 14 days.

## SIGNED: section 6, the rollback

The same Terraform path back to artifact VersionId `WJQGGIAlTSMp0Vny8avvQ7LxflVuvLf6`, then read `CodeSha256` back
equal to `E4944Imr7Y4S4//rTR6HN5sbwczbwLw5DcaH4IZ0D0E=`. One key, one version. Nothing else needs undoing.

**Trigger, added by this half.** After the apply, read the function's own log for the first real call of each of the six
roles in `W/da1_callers.json`, in the same window as the deploy. If any of them reads REFUSED, roll back in that window
and file an ARMED row naming `2.0.0_SA_COO~O`. The Bloomberg daily PKL send (the `/data-refresh` upload) is one of the
callers this protects: do not apply inside its run.

## SIGNED: section 7, the deploy path

As written: the ledger `nfra-oplgtw-og-da-1-data-refresh-admit` (entry and sentinel committed first); the artifact uploaded
with its `content-sha256` metadata and checked on size and metadata; `terraform plan -target='module.data_refresh_api'`
reading exactly 1 resource changed, code fields only, any other row a STOP; the saved plan applied through
`.tools/safe-apply.sh`; `CodeSha256` read back, Active and Successful, then a re-plan reading `No changes`; the ledger closed
before any proof. Never `aws lambda update-function-code`. The applier is `0.7.0_AE_CloudOps~Z`.

-- 2.0.0_SA_COO~O
