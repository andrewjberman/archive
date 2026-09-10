# BLAST_RADIUS.md — NFRA_IAMROLES202609, cell IAM-s-8 (TO-IAM-s-8)

Serial: `0.9.0_WK_NFRA_IAMROLES202609~2`. Written at 2026-09-10, worktree `C:/tmp/wk-iamroles-2`,
branch `wk-NFRA_IAMROLES202609-2`.

## What FWD-5 asks, and what this cell is (and is not)

FWD-5, verbatim: "An engineer can narrow a permission and know beforehand what it would break."
DONE WHEN **EXERCISED** — a real narrowing has been **checked** in advance and the check was
**believed**. The task order is explicit, and this deliverable follows it to the letter: the bar
is on the CHECK, not on an apply. **This exercise never applied anything to the world.** No
mutating IAM call (attach/detach/put/delete on any role policy) and no infrastructure-as-code
application of any kind occurred at any point in this run. The instrument that moves a claim from
DESIRED to EXERCISED is a single, well-known, read-only AWS API: **`simulate-principal-policy`**
(`aws iam simulate-principal-policy` / boto3 `simulate_principal_policy`), reached here through
IAM-s-1's `.tools/comp-iam-usage reach-check` wrapper. That call is the "simulate battery" the PRD's
D3 named as never yet run for this project. It has now been run, against a real candidate
narrowing, and every result below is EXERCISED evidence, not a read of policy text alone.

## The executable

`preflight-blast-radius.py`, same directory as this file. `--role <name> --remove <action>`.
Composes, rather than re-derives:
- IAM-s-1's `.tools/comp-iam-usage reach-check` (the simulate wrapper, Rule-22a disciplined) and
  `.tools/comp-iam-usage permission-cold` (IAM Access Advisor ACTION_LEVEL historical-usage plane).
- IAM-s-4's `condition-axis-reader.py`, shelled out to directly (never re-implemented) against
  every local `.tf` file this script can resolve a matching statement to.
- `comp-blast` (the code/infra dependency graph), run against every Lambda function this script
  finds assuming the target role, per the L5 battery's own naming of this cell as the one that
  makes `comp-blast` applicable.
- `comp-iam` (the DESIRED-plane Terraform-vs-source cross-reference), queried specifically to
  **name where it is blind**, because a silent DESIRED-plane gap would read as "nothing breaks"
  and that is the exact false-clean the project's C-NO-ACCESSDENIED bound forbids.

## The exercised run (AC1's exact invocation)

```
python org/missions/D12/NFRA/NFRA_IAMROLES202609/deliverables/0.9.0_WK_NFRA_IAMROLES202609~2/preflight-blast-radius.py \
    --role opal-data-refresh-lambda-role --remove s3:PutObject
```

rc=0. Full transcript (verbatim, one run, 2026-09-10T09:35:58Z):

### [1] Live policy enumeration (plane: DESIRED — policy text, read LIVE via `iam:List*`/`iam:Get*`)

The role's live policies are NOT fully visible in this repo's Terraform. Two of the three sources
that grant `s3:PutObject` are local (`infra/aws/terraform/data-refresh/main.tf` and
`infra/aws/terraform/data-refresh/qa-scratch-instance.tf`), but the **third — the managed policy
`opal-data-refresh-lambda-policy`, which is the ONLY source granting `s3:PutObject` on
`data-refresh/*`, `uploads/*` and `json/*` — has no `aws_iam_role_policy`/`aws_iam_policy`
Terraform resource checked into this repo at all.** `main.tf`'s own comment calls it
"pre-existing." This script found it only by reading the LIVE role directly
(`iam:ListAttachedRolePolicies` + `iam:GetPolicy` + `iam:GetPolicyVersion`), which is exactly why
C-DESIRED-UNTIL-EXERCISED insists a repo read is never enough for this cell.

Statements examined (inline + managed, live): **11**. Allow statements naming `s3:PutObject`: 3.
Distinct resource patterns those 3 statements grant it on (**DENOMINATOR of resources
examined**): **6**:

| resource pattern | granted by | condition (plane: DESIRED, policy text) |
|---|---|---|
| `arn:aws:s3:::opal-313476888478-yang-qa-scratch/*` | inline `data-refresh-qa-scratch-access-20260803` (Sid `DrQaScratchReadWrite20260803`) | REQUIRES-NOTHING |
| `arn:aws:s3:::opal-data-portal-v2/security_scanner/*` | inline `data-refresh-sscn-s3-access` (Sid `SSCNUploadPresign`) | REQUIRES-NOTHING |
| `arn:aws:s3:::opal-data-portal-v2` | managed `opal-data-refresh-lambda-policy` v10 (Sid `S3Access`) | REQUIRES-NOTHING |
| `arn:aws:s3:::opal-data-portal-v2/data-refresh/*` | managed `opal-data-refresh-lambda-policy` v10 (Sid `S3Access`) | REQUIRES-NOTHING |
| `arn:aws:s3:::opal-data-portal-v2/uploads/*` | managed `opal-data-refresh-lambda-policy` v10 (Sid `S3Access`) | REQUIRES-NOTHING |
| `arn:aws:s3:::opal-data-portal-v2/json/*` | managed `opal-data-refresh-lambda-policy` v10 (Sid `S3Access`) | REQUIRES-NOTHING |

### [1a] Condition axis — composing IAM-s-4's `condition-axis-reader.py`

Run, verbatim, against both LOCAL `.tf` files (`main.tf`, `qa-scratch-instance.tf`): every
statement it can read prints the literal token `REQUIRES-NOTHING`. **For the managed policy's
Sid `S3Access`, `condition-axis-reader.py` has no local file to read at all** (there is no local
custody of that document) — its Condition-key presence was read directly off the live
`GetPolicyVersion` document instead, a manual read explicitly labelled as bypassing IAM-s-4's
reader, and it also reads REQUIRES-NOTHING. Per IAM-s-4's own CONDITION_AXIS.md finding, "a
statement that requires nothing of its caller is not thereby safe to narrow" — REQUIRES-NOTHING
here means no MFA/source/tag gate stands between a caller and this permission, which if anything
widens the population that could reach it, not narrows the risk.

### [2] EXERCISE — one `simulate-principal-policy` call per resource (Rule-22a limit (b): no batching)

All 6 resource patterns were probed one call at a time (a synthetic leaf key substituted for a
trailing `*`, so the exact prefix the policy scopes is what gets simulated — Rule-22a limit (a)).
**All 6 currently evaluate `allowed`, `condition_handling=no-condition`, `missing_context=none`.**
These are the CURRENT reach-checked callers: since the action is presently granted, every one of
these six live paths would flip to denied if `s3:PutObject` were removed from this role.

### [2a] Controls (separate calls, per Rule-22a limit (b))

- POSITIVE control (`cloudfront:GetDistributionConfig` on the role's known CloudFront distribution
  ARN): `allowed`. Confirms the instrument is not stuck reporting deny.
- NEGATIVE control (`iam:CreateUser` on a nonexistent user ARN): `implicitDeny`. Confirms the
  instrument discriminates — it is not stuck reporting allow either. The six `allowed` verdicts in
  [2] are not an artifact of a broken always-allow probe.

### [3] Historical-usage plane (composed from IAM-s-1's `permission-cold`)

`s3:PutObject` reads `status=unobservable` — **"service 's3' has no action-level tracking in IAM
Access Advisor."** The historical-usage plane is BLIND on this exact action. This is named, not
smoothed over: the CloudTrail/Access-Advisor lifecycle signal cannot corroborate or contradict the
simulate-based prediction above for S3 actions at all. The live reach-check in [2] and the
code-level evidence below are what this prediction actually rests on.

### [4] Compute identities sharing the role + `comp-blast` (code/infra dependency graph)

Per the committed `infra/aws/lambda/ci/lambda-source-map.json`, **two** Lambda functions assume
this role: `opal-data-refresh-api` and `portal-time-machine`. The role is SHARED — a statement
removed for one function's use case is removed for both, since IAM permissions attach to the role,
not to whichever function's developer originally requested them. Direct code inspection of
`infra/aws/lambda/data_refresh/lambda_function.py` (read for grounding, not part of the generic
tool) confirms two real `s3:PutObject` call sites for `opal-data-refresh-api`: a
`generate_presigned_url('put_object', ...)` at line 373 writing under
`data-refresh/pending/{upload_id}/{filename}`, and a direct `s3_client.put_object(...)` at line
528 writing `{pending_prefix}manifest.json` — both under the `data-refresh/*` prefix that only the
undeclared managed policy grants.

`comp-blast` was run against both compute identities, downstream direction:

- `arn:aws:lambda:us-east-1:313476888478:function:opal-data-refresh-api`: **1015** downstream
  graph nodes (a LOWER BOUND per the tool's own caveat — "dynamic/FUNC-key consumers the
  extractors don't edge are NOT counted"). Its `IAM_POLICY` band (40 entries) independently names
  `opal-data-refresh-lambda-policy`, `data-refresh-sscn-s3-access` and
  `data-refresh-qa-scratch-access-20260803` — a SECOND instrument, built off the served cloud graph
  rather than a live `iam:Get*` call, corroborating the same three granting policies [1] found by
  reading AWS directly.
- `arn:aws:lambda:us-east-1:313476888478:function:portal-time-machine`: **1044** downstream graph
  nodes, same three policies corroborated in its own `IAM_POLICY` band (46 entries).

Total compute identities examined: 2. Total downstream graph nodes across both: **2059** (a lower
bound; this is the WHOLE-lambda blast radius from the code graph, a much wider surface than the
single permission under study here — it is corroborating context for "is this role's grant set
real and wired to production," not a per-permission verdict).

### [5] Naming where the DESIRED-plane cross-reference (`comp-iam`) is blind

`comp-iam role opal-data-refresh-lambda-role` returns no match at all: comp-iam's Terraform-vs-code
cross-reference has **no entry for this role whatsoever**. `comp-iam service opal-data-refresh-api`
shows all 55 tracked call-site operations reading `note: role not mapped` — its verdict space for
every one of this Lambda's operations, including both real `s3:PutObject` call sites above, is
`[UNKNOWN]`, not a clean bill; `comp-iam service portal-time-machine` shows the same for its one
tracked operation. This is named explicitly because a reviewer who only consulted `comp-iam` (the
tool this cell is NOT supposed to re-derive, only to check the coverage of) would see silence and
could easily read that silence as "no gap" — it is not. `comp-iam stats` (live) additionally
reports **304 permission gaps** estate-wide and one live-confirmed unmodeled service
(`opal-ipset-reconciler: wafv2:UNMODELED`) — a floor on the DESIRED plane generally, separate from
and not overridden by this role's own complete absence from that plane.

## PREDICTION (EXERCISED)

**Removing `s3:PutObject` from `opal-data-refresh-lambda-role` would break all 6 live-verified
caller paths**, i.e. every one of: the SSCN security-scanner upload-url presigned-PUT endpoint
(`security_scanner/*`); the primary data-refresh file-upload flow and its generated manifest
(`data-refresh/*`, the code-confirmed real caller); the `uploads/*` and `json/*` prefixes the
managed policy also grants (present in the live document; no corresponding code call site was
independently confirmed in this exercise — reported as reach-checked ALLOWED, not confirmed by a
second, code-level instrument, and that distinction is kept rather than collapsed); and the
QA-scratch bucket write path used by the `opal-data-refresh-api-qa-scratch` exercise instance.
Because the role is shared, `portal-time-machine` also currently reaches all six paths even though
none of its own inline statements request `s3:PutObject` — a narrowing scoped to
`opal-data-refresh-api`'s use case cannot be made on the role alone without silently touching
`portal-time-machine` too.

**DENOMINATOR:** 11 live statements examined; 6 distinct resource patterns examined (6 of 6
probed via `simulate-principal-policy`, 0 unprobed/blind for this action); 2 compute identities
examined via `comp-blast`, totaling 2059 downstream graph nodes (a lower bound). The
historical-usage plane (IAM Access Advisor) is named BLIND on this action rather than reported as
"never used"; the DESIRED-plane cross-reference (`comp-iam`) is named COMPLETELY BLIND to this role
rather than read as "no gap."

**Nothing in this exercise was applied to the world.** Every AWS call made was read-only
(`iam:Get*`, `iam:List*`, and the `simulate-principal-policy` read-only evaluation call). No
role-policy mutation of any kind — attaching, detaching, writing, or removing a policy on this or
any role — was issued by this run, and none is issued by the script that produced it. The
`org/critical_paths/change_management/` and `org/critical_paths/.open_deploys/` write surfaces
granted to this task order were not used: no world-changing act became necessary to answer FWD-5
at the bar this cell was given, so NEVER-2's open/act/close sequence was never entered.

## AC5 (judgment)

FWD-5's ACCEPT asks whether the check would actually have been BELIEVED before a real change, and
whether reading EXERCISED as "the check ran and was validated" rather than "a narrowing was
applied to production" is the right reading of this cell. That is not this seat's call to grade.
Recorded UNVERIFIABLE-BY-INSTRUMENT; graded by `3.0.0_SA_CVO~Z` at L9.
