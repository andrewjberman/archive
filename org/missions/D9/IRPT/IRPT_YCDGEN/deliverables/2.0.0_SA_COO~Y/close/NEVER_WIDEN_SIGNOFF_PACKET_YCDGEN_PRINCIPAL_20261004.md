# Never-widen sign-off packet -- IRPT_YCDGEN close: a Cottonwood research principal, assumed by the resident runner, holds the research Put/Get (replaces the inert host-role grant)

**For:** `1.0.0_SA_CTO` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y`, 2026-10-04 ~18:5xZ.

**Why:** row `IRPT_YCDGEN-S1` (@8daaf100b2). The close run `YCD-R1-20261004T1842Z` stopped at its first write
(AccessDenied). The grant applied under batch 237 (`KeepYChartsResearchAnswersAndRunRecords` on the host's
`irpt-ycharts-runner-role`) is inert. Cottonwood's bucket policy `DenyForeignFirmPrincipals` denies `s3:*` to every
principal outside `role/*-cot-*` and four named exceptions. That packet's after-read was an identity simulation, which
cannot see a bucket policy.

**Authority:**
- IRPT_YCDGEN PRD v0.1 @8b364d6d94, C-STORE and C-SESSION (unchanged).
- The estate's settled pattern for a firm fence: `infra/aws/terraform/investor-reporting/directory/holdings_refresh.tf:6-10`.
  It reads "one principal per firm"; widening the host role is the forbidden cross-firm act, so the host ASSUMES the
  firm's principal.

**Ledger:** `irpt-ycdgen-principal-20261004`, opened before the apply. It has D1 (the apply) and V1 (the close run's writes
read back). The earlier ledger `irpt-ycdgen-grant-20261004` V1 closes SUPERSEDED, pointing to this ledger's V1.

## 1. What changes, measured

**Change:** `9a01678592` (this seat's lane; `ycharts/resident.tf` plus the research runner).

- **New role** `irpt-cot-ycharts-research-role`, from `module.opal_name` (system irpt, scope cottonwood, function
  ycharts-research, kind role). Trust: `sts:AssumeRole` by `arn:aws:iam::313476888478:role/irpt-ycharts-runner-role`
  only. Max session 3600 s.
- **Its inline policy** `irpt-cot-ycharts-research-policy`: `s3:PutObject` and `s3:GetObject` on exactly:
  - `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/state/ycharts_responses/*`
  - `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/state/ycharts_runs/*`

  These are derived from the registry row `irpt-ycdgen-research-v1` and `scopes.json`, the same two prefixes the CTO
  signed in batch 237.
- **The host role** (`runner_resident`, one statement changed):
  - `KeepYChartsResearchAnswersAndRunRecords` (Put/Get on those prefixes, inert) becomes `AssumeTheFirmResearchPrincipal`.
  - That statement is `sts:AssumeRole` on that one role ARN.
  - Every other statement is byte-identical.
- **The runner** (`research/runner.py`): `research_s3()` assumes the builder-named role for 900 s before the lease is
  taken, so a refused assume costs no vendor call. Keeps and `run.json` are written with that client. The session's own
  reads stay on the host role.

**The targeted plan** (`close/plan_principal_ycdgen.txt`, drafted from the commit's worktree): 2 to add, 1 to change,
0 to destroy.

**Before-read** (`close/BEFORE_READ_PRINCIPAL_20261004.txt`):
- the bucket policy as quoted;
- the runner role's PutObject, simulated WITH the bucket policy, is `explicitDeny`;
- `irpt-cot-ycharts-research-role` is `NoSuchEntity`.

## 2. Blast radius

| principal / object | after |
|---|---|
| `irpt-cot-ycharts-research-role` on the two research tables | Put and Get (admitted by the fence by its name) |
| that role on any other key, in any bucket | nothing granted (no list, no delete, no wildcard) |
| who can become that role | the runner role only (trust policy) |
| `irpt-ycharts-runner-role` on `opal-data-cottonwood` | unchanged in effect: it was denied by the fence and stays denied (the inert Put/Get is removed) |
| `irpt-ycharts-runner-role`, new | `sts:AssumeRole` on that one role ARN |
| `opal-data-cottonwood`'s bucket policy | not touched: byte-identical |
| another firm | nothing: the policy row names Cottonwood only, and the role is Cottonwood-slotted |
| KMS | none: the bucket's default encryption is SSE-S3 |

The fence admits by NAME. The new principal carries `-cot-` because it holds Cottonwood's prefixes and nothing else, so
the fence's intent (only Cottonwood-scoped principals touch Cottonwood's data) holds. **Writers of the property** (who can
put into those two prefixes after the act): one, this role. **The manual path:** the runner's CLI writes only under the
`--firm` it is given. For a non-Cottonwood firm the assume names a role that does not exist and refuses before the lease.

## 3. Rollback (per key)

Revert the `resident.tf` half of `9a01678592`, then ONE targeted safe-apply of the same three addresses:
- the role and its policy are destroyed;
- the host statement returns to the inert Put/Get.

**Partial apply** (role created, policy or statement not): the same rollback destroys what was created. Read back: get-role
returns NoSuchEntity, and the host statement matches its live text before the act.

## 4. Apply protocol

1. Both halves at HEAD naming this file's blob. Ledger opened.
2. **Before-read, STOP on any difference** from section 1: the role is absent, the host statement is the inert Put/Get,
   and the bucket policy is as quoted.
3. **D1:** a fresh targeted plan (2 to add, 1 to change); ONE `HALT_ACK=1 safe-apply`. **After-read:**
   - get-role (trust names only the runner role); get-role-policy (the two prefixes).
   - simulate-principal-policy on the new role WITH the bucket policy and `aws:PrincipalArn`:
     - allowed on both research prefixes;
     - denied on `ycharts_opal_reports/x.pdf` and on `opal-data-49financial` (the same path shape).
   - simulate the runner role's `sts:AssumeRole` on the role: allowed.
4. **V1:** the close run's kept answers and `run.json` read back from the store (the research bundle is rebuilt from
   `9a01678592`'s runner); then both ledgers close.
