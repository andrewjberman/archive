# NEVER-WIDEN SIGN-OFF -- COO HALF -- IB-pr-373 IAM leg (row D2-W181-S1): irpt-export-render may persist a Performance client statement

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~22:5xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-373_IAM_LEG.md`, **blob
f98f340b38f3ad0013725454103c92b14843c9a0** (@77440a907b on box/dell2).

**Blast radius signed:** exactly one new resource, `aws_iam_role_policy.export_render_custody_persist`, in the root
`infra/aws/terraform/investor-reporting/export`. It holds five statements on `aws_iam_role.export_render` and nothing else. The plan is
`1/0/0`; the rollback is the same resource removed (`0/0/1`).

**Measured by this seat:**
- The persist's DynamoDB writes are `put_item` only (`repository.py:437`, `retention.py:296`; no update or transact), so UpdateItem is
  withheld.
- Every prefix is derived from `reporting_policies.json` and `scopes.json` exactly as `b1_submit.tf:42-45` derives the PERFORMANCE
  prefixes. The registry rows were read: CUSTODY_REPORT is platinum/custody_reports; REQUEST_COMPOSITION is state/request_compositions;
  the firms are 49financial, cottonwood and inflection.
- The KMS actions on writes (S2, S5) are inferred from AWS SSE-KMS behaviour, with after-read 2 as the measure. A refusal there is a STOP
  and a row, never a widening.

**Branch A** grants nothing reachable until the route order applies, and the only caller remains the guarded Entry. **Branch B** is
today's fail-closed state.

**Verdict: GIVEN**, for exactly this resource and these five statements at this blob.

-- 2.0.0_SA_COO~P2
