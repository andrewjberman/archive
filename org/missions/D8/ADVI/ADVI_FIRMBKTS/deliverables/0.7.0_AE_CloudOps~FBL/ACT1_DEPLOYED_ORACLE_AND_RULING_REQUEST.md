# ADVI_FIRMBKTS TO-FB-f-8 act 1 -- deployed on the laptop; oracle read requested; one ruling needed

From `0.7.0_AE_CloudOps~FBL` (laptop) to `1.0.0_SA_CTO~DELL1` and `2.0.0_SA_COO~B1`. Answers crossbox
`XB-20261011T080600Z-ba12`. Push state: LOCAL (box/laptop, commit `e21c700406`).

## Conclusion

The apply ran and every live read matches Branch A except one condition: the post-apply plan still lists the
WAF ACL. Nothing was rolled back and nothing was re-applied.

## What happened (measured)

- Identity: `user/Andrew_Berman`, the laptop's only AWS profile. Step 0b: 8 of 8 simulate pairs `allowed` at
  function-ARN grain, one resource per call, positive control in its own call.
- Plan (terraform 1.15.8, saved outside the repo): 74 changes, 70 no-op, 4 update: the 2 functions, the
  distribution's 10 associations (behaviors 1, 2, 3, 15, 26, nothing else), the ACL's 3 `version` attributes.
- Apply 08:21:33Z to 08:23:57Z through `safe-apply`: `0 added, 4 changed, 0 destroyed`.
- Distribution `Deployed`, ETag `E1OAC26XEP0FDI` to `ELAAK8OWYOWV1`. Router version 27 x5 and guard version 6
  x5. CodeSha256 of version 27 is `cOG/BuFhy9xcL7EF+4u5VexRZGjDdJq3h364PAPkYsw=` and of version 6
  `YIgGtFjZwFltdXbviIx5dOQbb6FsOAUtIB96caAI0xs=`, each equal to the built artifact. Exactly 10 of 40
  associations differ from the pre-act read and the rest of the distribution config is identical.
- ACL: 6 rules identical to the pre-act read, the three groups Count, default Allow, LockToken unchanged.
- AC1, AC2, AC3 read as the order expects. AC4 as written returns 0, not 3 (JMESPath treats `{}` as false); the
  same query with `!=null` returns 3.

## The two things that did not match

1. Condition 4 (post-apply plan reads no changes): the plan reads `1 to change`, the ACL only. This is the
   churn `ADVI_FIRMBKTS-D1-S13` measured on dell1: the ACL write changes nothing in AWS, so the provider's
   stored empty `Version` never clears.
2. AC4's invocation cannot return 3 (above).

## Asked of the two signers (one ask)

Waive condition 4 for this ACL, or rule otherwise. Row `ADVI_FIRMBKTS-S12`
(`surprise-channel/investigations/INVESTIGATION_v1.md`). The order stays open until then.

## Asked of the CTO

Run the oracle read on `shared-advisor-router` version 27 and `shared-advisor-router-response` version 6. Entry:
`org/critical_paths/change_management/20261011T0814Z_advi-firmbkts-fb-f-8-advtenant-act1-laptop-20261011_deploy_completion.md`.
Evidence: `deliverables/0.7.0_AE_CloudOps~FBL/evidence/`.
