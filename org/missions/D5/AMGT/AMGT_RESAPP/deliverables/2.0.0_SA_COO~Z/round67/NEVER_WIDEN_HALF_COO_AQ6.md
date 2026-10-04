# AMGT_RESAPP round 67 -- `AMGT-aq-6` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-04 ~22:4xZ

**The act (ONE):** add the prefix `amgt/harvest/gold/chatter_window/` to `local.scoped_amgt_pool_prefixes` in
`infra/aws/terraform/harvest/scoped-amgt-api.tf`, then ONE `safe-apply` targeted at `aws_iam_role_policy.scoped_amgt_api_grants`.
There is NO code change.
- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-aq-5.the-code-redeploy.md`, AMENDMENT 2 (leg 3; it owns cell `AMGT-aq-6`).
- Ruling: the CTO's AMENDMENT 1 to the aq-5 half @14aa3c9200 (msg 29280), on row Z-S346.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `aoQ+WrefJ+JjQcymqyrt2c7MEIlTPmvjJEv8sqZ6M98=` (aq-5's code leg, LastModified 2026-10-04T21:41:09Z), OR the build AMGT_CORPUS al-5 lands at `288de3d95d` (entry `amgt-corpus-r36-al5`; it carries round 67, since `d8bafe6896` is its ancestor). Leg 3 runs after that entry closes and does not move the code |
| function MemorySize | 1769 |
| role policy `opal-amgt-scoped-api-grants` | the aq-5 grant leg @f61711ef2b: the pool prefixes WITHOUT `chatter_window/`, plus the scanner object |
| simulate GetObject `opal-data-harvest/amgt/harvest/gold/chatter_window/date=2026-10-01/part-0.json` | implicitDeny |
| simulate ListBucket `opal-data-harvest`, `s3:prefix=amgt/harvest/gold/chatter_window/` | implicitDeny |
| controls, the same two calls on `chatter_daily/` | allowed, allowed |

## WHAT THE ACT MAY TOUCH

| act | what it MAY touch | rollback |
|---|---|---|
| targeted `safe-apply` | `opal-amgt-scoped-api-grants` only. GetObject gains `arn:aws:s3:::opal-data-harvest/amgt/harvest/gold/chatter_window/*`, and the ListBucket `s3:prefix` condition gains `amgt/harvest/gold/chatter_window/*` | a targeted `safe-apply` with the entry removed |

**Scope:**
- The bucket is one the role already reads, under 11 sibling pool prefixes; `chatter_daily/` and `chatter_event/` already hold both actions.
- The grant is read only: no Put, no Delete and no other bucket.
- The producer of `chatter_window` (aq-2's table) writes there; this role reads it only.

## EXPECTED OUTCOME -- both branches

| check | base (deployed `aoQ+WrefJ`, ~22:3xZ) | after (local control at the same hour) |
|---|---|---|
| `r67_grant_aq6.sh` | C1 FAIL, C2 FAIL (implicitDeny), controls PASS: NO | C1, C2, controls PASS: YES |
| r67 c24 C2 | FAIL: unreadable 95 of 95 per window | PASS: unreadable 0 per window |
| r67 c24 C1 | mismatches 74, old-reason 0, no-table-row 21 | mismatches 0, old-reason 0, no-table-row 21 (row Z-W220-S1, the producer's 212-name set) |
| r67 c23 / c25 / c26 | YES | YES (a policy-only act) |

**Failure branch:**
- **ROLLBACK** of the policy: a regression against the base, meaning mismatches above 74, a non-200 on any covered route, or c23,
  c25 or c26 not YES.
- **STOP, reported with the simulate output:** C2 still FAIL after AC1 reads YES. The grant did not take on the served path.

## WHAT THIS HALF DOES NOT COVER

Any of the following in the plan is a STOP:
- a code change, or a moved CodeSha256;
- a memory change;
- another prefix, bucket or action;
- a store write or an S3 delete;
- a vendor call;
- a route or gateway change.
