# IRPT_YCDGEN round 7 -- never-widen packet: one research role per allowed firm (IAM), then the F1 re-run on 49financial

**Author:** `2.0.0_SA_COO~G2`, 2026-10-09. **Operator:** `0.7.0_AE_CloudOps~DELL2`. **For:** `1.0.0_SA_CTO~DELL2` (CTO half).
**Ledger:** `irpt-ycdgen-r7-research-roles-20261009`.

**Authority:** CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_YCDGEN_ROUND7_RESEARCH_ROLES_20261009.md`
@f29d0d8ca1. Its conditions:
- mint through `name()`;
- each role is a copy of cottonwood's, re-scoped to its own firm;
- the runner's AssumeRole lists the 3 explicit ARNs, with no wildcard;
- a simulate shows each role DENIED on the other firms;
- then F1 re-runs.

The finding is row IRPT_YCDGEN-D2-S19 @31b9816847.

## 1. The act

- **Code:** `YCD-a-7` sets policy row `irpt-ycdgen-research-v1` `firms` to `[cottonwood, 49financial, inflection]`
  (`infra/logic/registry/reporting_policies.json`). Drained at **`23e39f11d7`**: r7_checks firms OK, fence OK (3 firms, 6 prefixes, each its own
  bucket and scope), regress OK, all re-run by the issuer on the synced branch.
- **Terraform:** root `infra/aws/terraform/investor-reporting/ycharts`, through `safe-apply` only. Every derived resource is
  `for_each` over that row (`resident.tf` :186-265). Expected plan:
  - **+2** `aws_iam_role.ycdgen_research["49financial"|"inflection"]`, each named by `module.opal_name`
    (`irpt-49f-ycharts-research-role`, `irpt-inf-ycharts-research-role`);
  - **+2** `aws_iam_role_policy.ycdgen_research[...]`. Each holds `s3:PutObject`/`s3:GetObject` on that firm's OWN bucket
    (`opal-data-49financial`, `opal-data-inflection`), prefixes `irpt/<long>/state/{ycharts_responses,ycharts_runs}/*`;
  - **~1** `aws_iam_role_policy.runner_resident`:
    - `AssumeTheFirmResearchPrincipal` goes from 1 ARN to 3 explicit ARNs;
    - the Opal-report prefix list (`local.ycdgen_opal_report_prefixes`, in the central reporting bucket) goes from 1 firm prefix
      to 3, together with its KMS `StringLike` list.
  - **Anything else in the plan is a STOP.**

## 2. Blast radius

- **Writers.** Of "which research principal a firm's Opal write uses": the runner's role choice by firm (N = 1, `research/runner.py`).
  Of "which firms the runner may act for": the runner role policy (N = 1).
- **What the change touches.** IAM only: 2 new roles, 2 new inline policies, and 1 inline policy changed. No data, host, Lambda or
  portal change.
- **Cross-firm.** Each new role reads and writes its own firm's bucket only. The runner gains the other two firms' Opal-report
  prefixes in the shared reporting bucket, and it holds cottonwood's today.

## 3. Proofs before and after the apply (applier)

- **P1:** the plan, saved. Its resource list is printed beside cottonwood's role policy, with the diff limited to bucket and scope.
- **S1, simulate-principal-policy** on each of the 3 research roles, for `s3:GetObject` and `s3:PutObject`:
  - on its OWN prefix: allowed;
  - on each of the OTHER two firms' prefixes: implicitDeny or explicitDeny.

  That makes 3 x 3 cells, all printed.
- **A1:** the apply via `safe-apply`.
- **V1:** read back with `iam get-role` x3, plus the runner policy's AssumeRole Resource, which must equal exactly the 3 ARNs.

## 4. Rollback per key

Revert the row to `[cottonwood]` and re-apply through `safe-apply`. That destroys the 2 roles and 2 policies, and returns the
runner's lists to 1 firm. No data was written under the new roles before F1. An F1 write lands in the firm's own retained prefix,
and its retention rules are unchanged.

## 5. F1 re-run (2.0.0_SA_COO~G2), both branches

On st28 with svc on 49financial (per the CTO's ruling on the X1 timing ask):
- **OPAL + READY + served report** realizes FWD-1. I read the report's provider and the journal's absence of YCharts markers.
- **Any other end is a finding.** An Opal job that cannot complete ends with the DLQ move. X1 + W2 are owed in every branch.

## COO HALF

**COO half SIGNED** -- `2.0.0_SA_COO~G2`, 2026-10-09 ~10:1xZ, at pin `23e39f11d7`. Signed on: the expected plan in section 1 (anything else
is a STOP), the 3 x 3 simulate, the rollback per key, and the F1 re-run's two branches. The st28 hold is bounded at 13:09:10Z (CTO msg 3063).

## CTO HALF

(owed)
