# Never-widen sign-off packet -- IRPT_YCDGEN close: the resident runner role keeps YCharts research answers and run records in Cottonwood's own bucket (two tables, Put/Get)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y`, 2026-10-04 ~02:3xZ.

**Authority:** the IRPT_YCDGEN PRD v0.1 @8b364d6d94 (RATIFIED): C-STORE (research outputs at builder addresses in the client
firm's bucket, state tier), C-SESSION (calls inside the served lease) and C-VENDOR (only `~Y` and its agents call YCharts).
Round 1 is merged and drained (@c1d672f636). The close's one real run of FWD-1 runs the runner ON the resident host, because
the session cookie and its WAF token are bound to that host (decomposition ruling 4).

**Ledger:** `irpt-ycdgen-grant-20261004` (D1, V1 open). **One move.** No code, route, table, queue, schema or Lambda moves.

## 1. What changes, measured

**Before (simulate-principal-policy, read only, 02:2xZ):**
- `irpt-ycharts-runner-role`: `s3:PutObject` and `s3:GetObject` on
  `opal-data-cottonwood/irpt/cottonwood/state/ycharts_responses/x.json` are `implicitDeny`.
- Control: the same actions on `opal-data-irpt/irpt/cottonwood/state/vendor_documents/x.pdf` are `allowed`.

**The change:** `abdac9bf16`, merged `1597d9939d`, in `infra/aws/terraform/investor-reporting/ycharts/resident.tf` (this seat's
lane):
- `locals`: `ycdgen_policy` is the registry row `irpt-ycdgen-research-v1` (landed by YCD-k-1); `ycdgen_host_families` is
  `YCHARTS_RESPONSE` and `YCHARTS_RUN`; `ycdgen_host_prefixes` is derived from the row's `firms` and `families` and each
  scope's own `bucket` (`scopes.json`). No address is typed.
- ONE statement `KeepYChartsResearchAnswersAndRunRecords`, with `s3:PutObject` and `s3:GetObject` on those prefixes.

**The targeted plan** (`close/plan_grant_ycdgen.txt`): `aws_iam_role_policy.runner_resident` updated in place, 0 to add, 1
to change, 0 to destroy. The one added statement's resources are exactly:
- `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/state/ycharts_responses/*`
- `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/state/ycharts_runs/*`

## 2. Blast radius

| principal / object | after |
|---|---|
| the runner role on the two research tables in `opal-data-cottonwood` | Put and Get (was implicitDeny) |
| the runner role on any other key in `opal-data-cottonwood` (holdings, served, other tables) | unchanged, implicitDeny |
| the runner role on another firm's bucket | unchanged: the policy row names Cottonwood only |
| `YCHARTS_OPAL_REPORT` (the Opal report) | not granted: the layout writes it from the laptop |
| KMS | none: the bucket's default encryption is SSE-S3 (AES256), read at the cut |
| every existing statement | byte-identical |

There is no list, no delete and no wildcard over the bucket. A cross-firm write is impossible by construction: the prefix
carries the firm's own bucket and long name.

## 3. Rollback

Revert `abdac9bf16` and ONE targeted safe-apply of `aws_iam_role_policy.runner_resident`. Read back: the statement is
absent and the simulation returns implicitDeny.

## 4. Apply protocol

1. Both halves at HEAD naming this file's blob.
2. **Before-read, STOP on any difference:** the live policy has no `KeepYChartsResearchAnswersAndRunRecords`, and the
   simulation is implicitDeny (above).
3. **D1:** a fresh targeted plan (1 to change, one added statement); ONE `HALT_ACK=1 safe-apply`; the policy read back.
   Simulate:
   - allowed on both research prefixes;
   - implicitDeny on `opal-data-cottonwood/irpt/cottonwood/state/ycharts_opal_reports/x.pdf` (not granted);
   - implicitDeny on another firm's bucket (`opal-data-49financial`, the same path shape).
4. **V1:** the close run's kept answers and `run.json` read back from the store; then the ledger closes.
