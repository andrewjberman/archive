# FB-l-2 -- The move plan for Cottonwood (FWD-9(a), read-only)

Record: `PLAN_COTTONWOOD.json` (same folder). Read at 2026-10-14T12:31Z. Worktree HEAD 7ee8e70830. Nothing was changed in AWS, in any product file, or in the registry. Writing this plan starts no move.

## 1. Canonical home

Recommended canonical bucket: **opal-data-cottonwood**. Legacy bucket to move and decommission: **opal-data-cot**.

Evidence for the canonical name: the registry cottonwood scope names opal-data-cottonwood as its bucket (bucket_provisioned true, managed by s3-lgic-firm-buckets.tf), and grades opal-data-cot as a routed alias of it (`infra/logic/registry/scopes.json` lines 164-206). The PRD firm-bucket row names the same bucket. The IRPT Cottonwood holdings writer (irpt-cot-holdings-role) already writes `irpt/cottonwood/` there (irpt/cottonwood/platinum 493 objects, gold 6,898).

Still legacy today: the edge router firm map, the IRPT directory map (eight live functions), the portal bucketSuffix map, and the served data itself (platinum 1,153 objects, gold entities/views/artifacts 2,158). The registry settles the name; the routing flip is move M13. Ratification by the CTO is open question Q1.

## 2. Ordered moves (30 rows, see the JSON for rollback and proof text)

| order | id | what moves | depends on | class |
|---|---|---|---|---|
| 1 | M1 | cot-etf-ownership-daily: SRC_BUCKET env and two stale legacy grants removed (first move, exercisable alone) | -- | lambda |
| 2 | M2 | router_iam.tf comment: the destroyed rule is named as absent | -- | comment |
| 3 | M3 | satellites characteristics header: "zero writers" corrected | -- | comment |
| 4 | M4 | org trail data-event selector adds opal-data-cottonwood (FWD-6 instrument) | -- | trail |
| 5 | M5 | registry: cottonwood platinum destination rows (none today) | -- | registry |
| 6 | M6 | served tier copied to advi/cottonwood/platinum/ (firm, clients, advisors, entities, views, artifacts, ownership map) | M5 | copy |
| 7 | M7 | directory and refresh state copied to irpt/cottonwood/ canonical forms | M5 | copy |
| 8 | M8 | satellites JSON copied (same keys) | M5 | copy |
| 9 | M9 | ingest raw forwardfill_v2/ and code/bronze/templates/ copied | M5 | copy |
| 10 | M10 | serving grant for the advisor OAI on advi/cottonwood/platinum/* and satellites; IRPT directory read grants | M6, M7, M8 | role |
| 11 | M11 | bucket-policy admit list for the Cottonwood writer roles (fence stays) | M10 | role |
| 12 | M12 | EventBridge enabled on opal-data-cottonwood (singleton, empty today) | M4 | notification |
| 13 | M13 | CUTOVER: routed alias flip and regeneration of every generated map | M4-M11 | registry |
| 14 | M14 | redeploy shared-advisor-router and auth-validator-edge | M13 | edge |
| 15 | M15 | IRPT readers: IRPT_DIRECTORY_BUCKET_MAP cottonwood entry and directory prefix (8 functions) | M13 | lambda |
| 16 | M16 | portal bucketSuffix 'cottonwood' moves to the new bucket (cand branch; PROD waits on Andrew) | M13 | portal |
| 17 | M17 | rules cot-bronze-complete and cot-silver-complete repointed | M9, M12 | rule |
| 18 | M18 | served-header guard rule and Lambda repointed | M6, M10, M12 | rule and lambda |
| 19 | M19 | value-parity Lambda and rule repointed (anchor fork Q5) | M6, M9, M10 | lambda |
| 20 | M20 | satellites registry producer writes to the new bucket | M8, M11, M13 | lambda |
| 21 | M21 | satellites characteristics producer reads and writes the new bucket | M20, M11, M13 | lambda |
| 22 | M22 | session trigger: COT_DATA_BUCKET and mode marker to the canonical state key | M13, M17 | lambda |
| 23 | M23 | ingest mirror cot row reads the new source | M9, M13 | lambda |
| 24 | M24 | SSM run documents and repository scripts write the new bucket | M13, M22 | script |
| 25 | M25 | residual bronze, silver, gold, logs copied or decided (Q9) | M24 | copy |
| 26 | M26 | registry legacy address rows repointed | M13, M25 | registry |
| 27 | M27 | decommission A: legacy grants and EventBridge removed on opal-data-cot (after the window) | M14-M26 and 45 days | policy |
| 28 | M28 | decommission B: CloudFront origin S3-opal-data-cot removed (after M27) | M27 | edge |
| 29 | M29 | decommission C: objects, versions and the bucket (each act is Andrew's word) | M28 | delete |
| 30 | M30 | crosswalk input and its 7 consumers and 11 importers: verification re-read only, no object changes | M13 | reader |

First move: M1. It touches one Terraform file, changes no served data, and its proof is the next 10:30 UTC run's output.

## 3. Decommission of opal-data-cot

- Window: 45 consecutive days, read or write, on opal-data-cot, other than an excluded probe.
- Instrument: opal-organization-trail. Its ReadOnly and WriteOnly data-event selectors cover opal-data-cot/ today (measured). The served-key trail is narrower and is not the basis.
- Start: no earlier than the trail's observed-live stamp (its configuration date is not read: Q8), and only after the cutover. Cutover means M13 through M26 have landed. Any event restarts the count.
- Readers that must reach zero first: the CloudFront origin and its OAI grant, the router rewrite, the IRPT directory readers, the portal readers, the event chain and producers, the ingest mirror, the mode marker.
- Not decommissioned: opal-data-cottonwood is the canonical home.
- Every removal and every per-version delete needs Andrew's word, act by act. The bucket is versioned, so "delete" means "hide".

## 4. Legacy operations to retire

| id | operation | consumers | decision |
|---|---|---|---|
| R1 | bd-cot-freshness-probe repository source (stack torn down, CHANGELOG line 218) | 0 | retire the source in one commit |
| R2 | graph node cot-satellites-registry-producer-daily (absent live) | 0 | retire the node name; the live trigger is the stamp-gated rule |
| R3 | cot-etf-ownership-daily legacy read path | 0 code readers | retired by M1 |
| R4 | investor-reporting directory copy read through IRPT_DIRECTORY_BUCKET_MAP | 9 before M15, 0 after | retired by M7 and M15; the copy stays until M27 |
| R5 | legacy mode marker key | 1 writer, readers not read | replaced by M22; retire after Q3 |
| R6 | firmsep-cot-bucket-recovery-role (can rewrite the canonical bucket policy) | not read | not retired here; Andrew with the CTO (never-widen) |

FIRMSEP-s3-direct-access-bypass is not a Cottonwood operation (its pattern names bd and inf only). It is open question Q12, not a retirement in this plan.

## 5. Crosswalk input and consumers

The crosswalk input is outside every legacy home: `opal-data-assets/commonwealth/cottonwood/silver/crosswalk/` (2 objects, 860,081 bytes, measured). The builder and the seven consumers read it through `opal_naming.address()`. None of the seven named consumer files carries the string opal-data-cot. They are recorded as unaffected (JSON key `unaffected`, XW-1 to XW-3), with the eleven module importers on the inventory's measured claim.

## 6. Live IAM and environment column

Recorded per function in the JSON key `iam_env_column`: 15 Cottonwood and IRPT functions, 2 edge functions, and 2 absent functions. Only variable names are recorded, plus bucket and queue values. Key findings are in M1, M11, M13 and M14. The Lambda@Edge role grants GetObject on opal-data-bd only (open question Q13).

## 7. Open questions

Q1 canonical ratification (CTO). Q2 served key layout for satellites. Q3 readers of the mode marker. Q4 writer of forwardfill_v2 (not in any inventory). Q5 value-parity anchor shape. Q6 fence amendment (never-widen, CTO and COO). Q7 mdpf/cottonwood prefix on the canonical bucket. Q8 instrument stamp for the window. Q9 residual gold and logs. Q10 EC2 exporter crontab. Q11 IRPT reporting-read map. Q12 FIRMSEP rule disposition (FB-l-1 and FB-k-5 owner). Q13 Lambda@Edge ownership-map grant. Q14 directory key owner (IRPT_BCKEND).

## 8. Not read

Full list in the JSON key `not_read` (18 entries). Principal items: EC2 exporter contents, ECS and Step Functions definitions, object bodies, readers of the mode marker, the forwardfill writer, SNS subscriptions and alarms, CloudFront access logs, Terraform state, the deployed bytes of the edge and Lambda code.

## 9. Denominators

Lambda functions listed: 237 (five pages). Cot, cottonwood or irpt name matches: 25. Lambda configurations read: 28 (plus 2 edge, 2 absent). IAM roles read: 18. Inline policy documents read: 44. S3 objects: opal-data-cot 7,929 in 9 top-level prefixes; opal-data-cottonwood 7,633 in 2. EventBridge rules: 12 by prefix, 13 targets. Scheduler: 2. SSM documents: 4. CloudFront: 7 origins, 29 behaviours, none to the cot origin. IAM simulations: 7. Graph nodes scanned: 2,929.
