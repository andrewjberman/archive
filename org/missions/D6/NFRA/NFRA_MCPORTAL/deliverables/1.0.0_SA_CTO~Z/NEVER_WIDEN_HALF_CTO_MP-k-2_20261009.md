# Never-widen half (CTO) -- NFRA_MCPORTAL MP-k-2: the gateway role's one write, close requests only

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~09:3xZ (re-pointed from the retired `1.0.0_SA_CTO~O` by AMENDMENT 3 @2724889425, merged @a7ff380da2).
**Ask:** `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-k-2.md` @77184244cf, read whole
(applier branch `wk-mcportal-cp2-k2`). **COO half:** SIGNED at the same merge, per `2.0.0_SA_COO~MP` msg 32620.
**Ruling it implements:** `1.0.0_SA_CTO~O` msg 32404 on Q3, which is now this seat's to stand behind.

## VERDICT: SIGNED -- one `aws_iam_role_policy`, `gateway-mcportal-close-request-write-policy`, one statement: `Allow s3:PutObject` on `arn:aws:s3:::opal-313476888478-globgrph/fabric/open-calls/v1/box=*/requests/*`, no condition, added to `opal-gateway-role` in its own file. Plan `1 to add, 0 to change, 0 to destroy` and nothing else.

## What this seat read at signing (live, 09:3xZ)

| read | result |
|---|---|
| `iam list-role-policies --role-name opal-gateway-role` | 20 inline policies, none named `gateway-mcportal-close-request-write-policy`; 1 managed (`AmazonSSMManagedInstanceCore`) |
| `simulate-principal-policy`, `s3:PutObject` on `.../box=sitez/requests/x.json` | `implicitDeny` today. So the write is new, and the ask's AC2 `allowed` arm will show the grant's own effect |

## The width, and why it stops here

- **`box=*` is the ruling's scope:** the MC portal serves every box's open calls, so Andrew's close request may be addressed to any box.
- **The grant is the ceiling, not the authority.** Who may ASK to close a call is decided in the gateway's request handler. This IAM
  grant only lets the gateway process write the object. A request closes nothing by itself: each box's own scan applies it through that
  box's writer and writes the result (`open-calls-scan.py:407`, `:453`, `:400-402`). The list, the results, the activity store and every
  delete stay out of reach (ask section 3).
- **One production writer of `requests/` after the act** (the ask's census of all 11 write verbs in the scan; its only `requests/`
  put is inside the self-test).

## Accepted as stated, not re-read here

The builder-output policy name; the comment-only diff of `graph-read.tf`; the `comp-iam gaps` figures and their stated limits; the
NEVER-2 ledger `nfra-mcportal-cp2-close-request-grant`; rollback by `delete-role-policy` or a targeted destroy, touching no other grant.

## Conditions

- The apply goes through `safe-apply` with the saved plan. Any plan line other than this one addition is a STOP.
- AC2's 6 arms read 6 of 6, with the GetObject positive control `allowed`. An all-`implicitDeny` sheet is read as an instrument fault, not a pass.

-- 1.0.0_SA_CTO~Z
