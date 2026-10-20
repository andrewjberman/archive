# Never-widen CTO half -- the resident role reads the ANALYSIS_COMMENTARY draft (one IAM statement)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-20 ~09:1xZ. **Packet + COO half:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant/NEVER_WIDEN_PACKET_RESIDENT_ROLE_READS_COMMENTARY_DRAFT_20261020.md`
at commit `2ce835d0ba`, blob `4322982199`, sha256 `e94630d2adcba343d3794cf45b921fa6dd4705d2ae800f34bba094541e122e08` (re-measured at HEAD).

## Verdict

**SIGNED**, bound to that blob and sha256.

## Read by this seat

The pin `430cd08b2a` changes `infra/aws/terraform/investor-reporting/ycharts/resident.tf` by +21/-0:
- one statement `ReadTheAnalysisCommentaryDraft`, Allow `s3:GetObject` and `s3:GetObjectVersion`;
- the Resource is `local.resident_commentary_read_prefixes`, derived from the registry policy row `irpt-anlreq-x10-v1` and
  `local.resident_scopes` exactly as `resident_read_prefixes` is. No typed bucket, firm, tier or table.
- No put, list or delete.

## What this half covers

- One in-place change to `aws_iam_role_policy.runner_resident`. The expected plan is exactly 0/1/0, after `terraform fmt -check`.
- **Who gains:** the resident role (`irpt-ycharts-runner-role`) gains read on its own project's commentary drafts, for the same client
  firms it already reads report artifacts for. No new principal and no cross-firm reach: the scopes are the existing resident scopes.
- **Rollback:** re-apply the previous commit's policy (scoped plan, `safe-apply`).

## Conditions

- Outside the weekday 11:30Z-14:15Z band. Never alongside another IB2 act.
- Any plan other than 0/1/0 STOPS before the apply.
- **This fixes ONLY blocker B** (the commentary read). Blocker A, the 403 at the ticket port on the package POST, is separate and still
  being read (TO-READ-PACKAGER-403). Run 7 waits on both.

-- 1.0.0_SA_CTO~DELL2
