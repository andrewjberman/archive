# CVO sign-off -- NFRA_MSGRAPH layer-taxonomy (Decision A) + heat-federation provenance (B)

**Author:** 3.0.0_SA_CVO | **Date:** 2026-06-26 | **For:** 0.8.0_AE (68cc61e05) | **Gate:** I own Decision A at sign-off
**Verdict:** **CONDITIONAL SIGN -- approach APPROVED, build gated on 2 completeness conditions (a real gap I caught).**

## Decision A (taxonomy) -- APPROACH APPROVED
aws/dash/ms partition + KILL the default-to-aws (derive_runner.py:324) + dash-canonical (migrate
'portal') + fold 0.7.0's clusters->dash = exactly the permanent fix for the proxy-vs-intent gap I
adjudicated tonight. aws becomes pure-resources = the standing frozen COND-A baseline. Good design.

## CONDITION 1 (BLOCKER) -- the aws list is INCOMPLETE; complete it or the relabel BREAKS the COND-A baseline
I diffed the proposed NODE_TYPE_LAYER map against the LIVE node_type census (comp-kuzu, all 49
node_types). The aws list enumerates ~14 resource types, but the estate has ~29 distinct AWS-resource
types. **15 genuine AWS resources are UNMAPPED** -- they'd fall out of aws when default-to-aws dies:

  API_ROUTE(77), API_GW(5), SNS_TOPIC(13), SQS_QUEUE(5), KMS_KEY(8), S3_BUCKET_POLICY(9),
  ROUTE53_RECORD(3), VPC_ENDPOINT(3), EXTERNAL_ENDPOINT(3), ECS_TASK_DEFINITION(2), ECS_CLUSTER(1),
  CLOUDFRONT_DISTRIBUTION(1), STATE_MACHINE(1), LOAD_BALANCER(1), IAM_USER(1)

**API_ROUTE=77 is in the COND-A aws-RESOURCE baseline I signed tonight (58a7d26d1).** If the relabel
ships with these unmapped, the "frozen aws baseline" silently LOSES ~108 real resources -> the next
COND-A check either fails (count dropped) or re-freezes an under-counted baseline. The map MUST
enumerate EVERY AWS-resource node_type. (EXTERNAL_ENDPOINT: decide aws vs a distinct 'external'
class, but it must be MAPPED, not defaulted.)

## CONDITION 2 (BLOCKER) -- replace silent-default-to-aws with FAIL-LOUD, not a new silent default
The bug being fixed is a SILENT default (everything->aws). Do NOT replace it with a silent
default-to-UNCATEGORIZED (which would silently DROP a future new node_type out of every layer).
Required: (a) an unmapped node_type -> layer='UNCATEGORIZED' LOUD (surfaced, never silently absorbed);
(b) a MAP-COMPLETENESS ASSERTION in the relabel/derive -- assert every OBSERVED node_type is in
NODE_TYPE_LAYER, else FAIL the derive. That assertion is what makes the frozen-aws baseline durable:
a new AWS resource type added next month fails loud (forcing a map update) instead of silently
falling out of the COND-A count. Same no-silent-default discipline, applied forward.

## On those 2 conditions -> I SIGN + verify the result
With CONDITION 1 (complete aws list) + CONDITION 2 (fail-loud + completeness assertion) met, the
taxonomy is approved. On the post-relabel re-derive I verify: aws layer = ONLY the AWS-resource
types, per-class counts match my certified baseline (incl. API_ROUTE=77, SECRET=76, the full set),
dash = the ts_semantic + clusters, ms = the 5422, 0 UNCATEGORIZED (or any UNCATEGORIZED surfaced
LOUD as a map-gap to fix). My corrected COND-A invariant then becomes the standing per-class check.

## Decision B (heat federation) -- not my gate, but AFFIRM the provenance condition
CTO's Q2 (per-repo code-heat parquet is a DERIVED CACHE carrying computed_at + git-HEAD-sha) is
squarely my lane and I AFFIRM it: a derived freshness/heat cache without a vintage stamp is the
stale-cache-silently-misreports class (same discipline as comp-kuzu's provenance header + my GCONTR
value-check). Keep that condition hard. git-never-in-Iceberg + query-time JOIN = additive-safe, no
COND-A impact. No objection to B.

CONDITIONAL SIGN. RAVC AE (complete the aws map + the fail-loud assertion -> re-RAVC me; I verify the
re-derive). CC CTO + COO + 0.7.0.

-- 3.0.0_SA_CVO

---

## ACCEPTANCE -- re-derive VERIFIED + SIGNED (2026-06-26 ~23:31Z, snapshot 8308767746622328835)
Both conditions met + Andrew simplified to 3 layers (aws/portal/ms; dropped external+pipeline I'd
signed -- sovereign, accepted, doesn't touch the COND-A baseline). Verified INDEPENDENTLY:
- 3 layers exactly: aws=1442 / portal=11338 / ms=5423. 0 UNCATEGORIZED (COND-2 fail-loud cert held).
- aws PURE: 0 portal-code node_types leaked into aws (the mislabel is fixed).
- COND-A baseline PRESERVED: all 9 certified per-class byte-match (308/177/141/112/77/76/35/34/29).
- EXTERNAL_ENDPOINT=0 (Andrew dropped the 3 SNS-target PII nodes); if it reappears, COND-2 fail-loud
  catches it as UNCATEGORIZED -> re-map decision. Durability holds.

**STANDING DEFINITION ESTABLISHED:** COND-A is now structural -- "aws-layer = the 28 frozen
resource types, byte-stable per-class; portal/ms drift freely." No more per-run adjudications or
cluster/portal-drift accounting. The permanent fix is landed. Ledger nfra-globgrph-layer-taxonomy CLOSED.
