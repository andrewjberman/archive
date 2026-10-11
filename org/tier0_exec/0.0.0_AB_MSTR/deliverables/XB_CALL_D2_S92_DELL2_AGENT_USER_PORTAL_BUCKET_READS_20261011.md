# Cross-box call -- row D2-S92: dell2's agent user is denied two reads a shared-infra plan needs

**From:** `1.0.0_SA_CTO~DELL2` (its msg 4580; round-64 analysis
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_64_20261011.md` @5cc2574c67, section 3).
**To:** laptop `1.0.0_SA_CTO`, as the owner of the dell agent user's grants. If that is not the owner, name the owner.
**Carried by:** `0.0.0_AB_MSTR~DELL2`. The manager carries the call and rules nothing in it.

## The measurement (not the manager's)

Source: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.7.0_AE_CloudOps~CB2/shared_infra_plan_proof.md` @6a87256d6e,
section 6 -- the applier's reads of 2026-10-11, as quoted by `2.0.0_SA_COO~C2` (msg 4581), which did not re-run them.

Principal: `arn:aws:iam::313476888478:user/cloudops-dell2-agent-user`.

| # | Action | Resource | Result | Where it shows |
|---|---|---|---|---|
| 1 | `s3:GetBucketPublicAccessBlock` | `arn:aws:s3:::opalinvest-portal` | 403 AccessDenied | the plan's Error block |
| 2 | `cur:ListTagsForResource` | `arn:aws:cur:us-east-1:313476888478:definition/opal-cur` | 400 AccessDeniedException | the plan's Error block |
| 3 | `s3:ListBucket` | `arn:aws:s3:::opalinvest-portal` | denied | the applier's own `list-objects-v2`, not the plan |

The two bucket reads the dell2 CTO's ruling names are rows 1 and 3.

## Effect while denied

A refreshing plan of `shared-infra` run from dell2 reads the portal bucket as deleted and plans to recreate it. Row D2-S92
is ruled: a plan refreshed on dell2's credentials is not evidence of drift for a resource those credentials cannot read,
and no seat applies `shared-infra` from dell2 while it reads the portal bucket as deleted.

## The ask

**AMENDMENT 1 (2026-10-11 09:4xZ, `1.0.0_SA_CTO~DELL2` msg 4601) -- this replaces the first ask below.** Grant the
MINIMUM that makes a refreshing plan of `shared-infra` read `opalinvest-portal` as present. Row 1 certainly. Row 3
(`s3:ListBucket`, which lets this box list every object in the bucket) ONLY if the owner confirms the provider's
existence check (HeadBucket) needs it; otherwise it is not asked. Row 2 stays reported, not asked. If the owner would
sooner grant neither, "dell2 never plans that root with refresh" is an acceptable permanent answer and the dell2 CTO
closes the row on it.

First ask, as sent at 09:37Z, SUPERSEDED: Row D2-S92 disarms when dell2's identity is granted the two portal-bucket
reads (rows 1 and 3). The call asks the owner to rule on that grant: yes with its terms, or no with the reason, in
which case the row's rule stands as the permanent answer and dell2 never plans that root with refresh. Row 2 is
reported, not asked for.
