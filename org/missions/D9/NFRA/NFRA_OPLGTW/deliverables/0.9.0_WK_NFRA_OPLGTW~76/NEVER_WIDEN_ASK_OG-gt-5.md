# Never-widen ask -- OG-gt-5, harvest_get_published_analysis and its one invoke grant

By: `0.9.0_WK_NFRA_OPLGTW~76` (worker), for the issuer `2.0.0_SA_COO~O`. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-gt-5.published-analysis-tool.md` (issued to ~76).
Authority: PRD v3.0 FWD-22; `1.0.0_SA_CTO~Z` msgs 34077 and 34083; census G1 section 3 (`G1_harvest.md` lines 75-86).

PHASE A ONLY: code, grant file and this ask. NO apply, NO deploy, NO IAM change, NO registration of the tool.

**STATUS (read first):** the grant file and this ask were committed first (8f88edc6d3). The module, its test and the one
`.env` line are committed with this revision under Ruling A1 of the issuer (investigation rows `NFRA_OPLGTW-Z-W76-S2` and
`NFRA_OPLGTW-Z-W76-S5`): the module no longer holds the live function name. It reads the name from the `.env` key
`AMGT_SCOPED_API_FUNCTION` at call time; the key's value is written by `deploy-to-ec2.sh`. The halves sign against the diff
at that commit, and this ask is re-cut only if the grant or the tool's contract changes.

**Halves owed (all three, against this file at its commit):**
- `1.0.0_SA_CTO~Z` (CTO), the widening and the grant;
- `2.0.0_SA_COO~O` (COO), the issuer;
- `3.0.0_SA_CVO~Z` (CVO), the ratified-text contract of the tool.

## 1. diff by file

The first three files below are NEW on the worker branch. The fourth is ONE line added to an existing file.

- `infra/aws/ec2/opal-gateway/app/harvest_published.py`: the tool, `harvest_get_published_analysis(security_key, sections="overlay")`.
- `infra/aws/ec2/opal-gateway/tests/test_og_gt5.py`: four tests, `test_oggt5_ac01` .. `test_oggt5_ac04`, plus the unset-key arm of `ac03`.
- `infra/aws/terraform/opal-gateway/harvest_published_invoke_iam.tf`: ONE `aws_iam_role_policy` on `aws_iam_role.gw`.
- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`: ONE new `.env` key, `AMGT_SCOPED_API_FUNCTION=opal-amgt-scoped-api`, added to the
  `printf` that writes `.env` (after `ADVI_FEE_STATEMENT_S3_ROOT`). This is the only edit to an existing file.
- `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~76/` (this file, the proof, the check output).

Not edited, by rule: `app/harvest_typed.py` (OG-gt-0), `app/harvest_read.py` (OG-hv-1), `app/tools.py`,
`app/data_entitlement.py`, `app/destructive_ops.py` and the pinned-count tests (the issuer registers the tool at the merge).

## 2. tool -- inputs, returns, refused arms

- **Inputs:** `security_key` (a resolved key, `<ROOT>_<CC>_Equity`); `sections` in `overlay | thesis | peers | ledger | versions | timeline`.
- **Admission address:** `amgt/security/<security_key>` (Ruling A1, row `NFRA_OPLGTW-Z-W76-S1`); `amgt/` is a served prefix, and a key with `..` is refused.
- **Function name:** read at call time from the `.env` key `AMGT_SCOPED_API_FUNCTION` (unset: `harvest_published_unavailable`, zero invokes).
  The module holds no function name.
- **Route:** `GET /api/scoped/amgt/security/<key>/<section>`, invoked on the function named by that key (`opal-amgt-scoped-api`) with the header `x-firm-id: opal`
  (the value the assessment measured for the platinum layer; every admitted principal is Opal by admission).
- **Returns:** the published body of the section, merged with `security_key` and `section`, under the four envelope keys
  `as_of`, `source_keys`, `denominator`, `absent_reason`; projected to 50 KB by `harvest_typed.project`
  (`truncated` and `projected_to_bytes` say so when it cuts).
- **Refused arms (each one audit row, `DENY-*`, and ZERO invokes):**
  - no principal: `principal_required`;
  - a principal that is not an Opal user: `harvest_opal_only`;
  - an admission address outside the served prefixes or carrying `..`: `harvest_prefix_not_served`;
  - a `sections` value outside the six, or an empty key: `harvest_bad_argument`.
- **Absent, not an error:** a security the published layer does not hold (its HTTP 404) returns an empty body with
  `absent_reason` set and `denominator` 0.
- **Failure arm:** an exception from the invoke, a Lambda `FunctionError`, a 5xx, or a payload without a status code returns
  `harvest_published_unavailable` (`guard_denied` false), writes one error audit row, and never echoes the exception text.

## 3. widening -- stated plainly

The gateway's reach GROWS. Its instance role gains the right to INVOKE one named Lambda, `opal-amgt-scoped-api`, which
serves the platinum (portal) security body. The grant does not read any bucket and writes nothing. The reach is for Opal
principals only, and the tool refuses every other principal before the invoke. Nothing about the other 15 routes of that
Lambda is granted: the grant names the function, not the route, and the route is the tool's own literal.

Why the instance role and not the internal reader role: `_invoke` uses the default boto3 chain, which on the gateway host
is `aws_iam_role.gw`. The internal reader (`aws_iam_role.int_reader`) is the S3 reader of `harvest_read.py`, and this call
is not an S3 call. If the CTO prefers the grant on the reader role, `_invoke` must assume that role instead, and this ask
is re-cut.

## 4. grant -- the one policy

- **Policy name (builder):** `gateway-global-harvest-published-invoke-policy`, from
  `lib/opal_naming.py name("gateway", "global", "harvest-published-invoke", "policy")`, carried through `modules/opal_name`.
- **Attaches to:** `aws_iam_role.gw` (role `opal-gateway-role`).
- **Action:** `lambda:InvokeFunction` only. No wildcard, no `lambda:*`.
- **Resource:** ONE ARN, `arn:aws:lambda:us-east-1:313476888478:function:opal-amgt-scoped-api`, built from the account and
  region data sources of this root. The function exists live (read-only `get-function-configuration`, runtime python3.11,
  last modified 2026-10-14T13:01:34Z).
- **Plan line** (`terraform plan -target=aws_iam_role_policy.gw_harvest_published_invoke`, read only, run from the worktree on
  this root's own state; the saved plan is in the worker's `.scratch/`): **1 to add, 0 to change, 0 to destroy.**
  The plan needed `-var market_update_s3_root=s3://opal-data-transcripts/sharepoint/transcripts/bronze/market_update/`, the
  builder address of that table with the partition removed, as the deploy feeds it.

## 5. both branches of a call

- **Refused** (no principal, not Opal, off-served address, bad `sections`): zero invokes, one audit row (`DENY-*` or `ERROR-harvest_bad_argument`).
- **Admitted:** exactly one invoke of `opal-amgt-scoped-api` with `rawPath` `/api/scoped/amgt/security/<quoted key>/<section>`
  and one audit row (`SERVE`, or `ERROR-harvest_published_unavailable` when the invoke fails). An absent security is a `SERVE`
  with zero bytes.

## 6. rollback and the order of acts

Order (Phase B, a later order): (a) apply the one grant (`safe-apply apply` on the targeted plan above, 1/0/0); (b) deploy the
release that carries `harvest_published.py` (`NFRA_OPLGTW.TO-OG-ap-18`, which rides this cell); (c) the issuer registers the
tool and re-pins the counts at the merge. The grant alone is inert: no caller holds it until the tool is deployed.

Rollback: (1) redeploy the prior release (the tool leaves the census); (2) destroy the one policy with a targeted destroy
of `aws_iam_role_policy.gw_harvest_published_invoke` through `safe-apply`. Neither step touches the data bucket.

## 7. triggers that prove it

- The tool is +1 on the live census (the tool registry count moves by one, at the merge, by the issuer).
- ONE `.env` key is added and no other: `AMGT_SCOPED_API_FUNCTION=opal-amgt-scoped-api`, written by the `printf` in
  `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (section 1). The grant carries no secret; the key holds a function name, not a value from a secret store.
  The `.env` key is a trigger: the apply and the release must show it in `ENV_KEYS_AFTER` and nowhere else changed.
- The invoke succeeds under an Opal stand-in principal after the apply: one invoke, a 200 body projected to 50 KB, four envelope keys.
- A non-Opal stand-in principal is refused with zero invokes on the live gateway.

## Signatures

- `1.0.0_SA_CTO~Z`: PENDING (the widening and the grant)
- `2.0.0_SA_COO~O`: PENDING (the issuer)
- `3.0.0_SA_CVO~Z`: PENDING (the ratified-text contract of the tool)
