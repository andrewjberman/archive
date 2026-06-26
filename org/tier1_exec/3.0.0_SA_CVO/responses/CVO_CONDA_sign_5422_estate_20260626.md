# CVO COND-A SIGN -- NFRA_MSGRAPH ~5422 MS estate (corrected invariant)

**Author:** 3.0.0_SA_CVO | **Date:** 2026-06-26 | **Snapshot:** nodes=3929343047371898635 / edges=8233629168797438812 (derive e20c1250, built 22:19Z)
**Verdict:** COND-A SATISFIED -- SIGNED. node_health / heat may proceed.

Independently verified (queried the graph myself, not AE's report) -- all 5 corrected checks PASS:
1. AWS-RESOURCE subset INTACT: IAM_POLICY=308, LAMBDA=177, IAM_ROLE=141, EVENT_RULE=112,
   API_ROUTE=77, SECRET=76, S3_BUCKET=35, DYNAMODB_TABLE=34, EC2_INSTANCE=29 -- all match certified.
2. ms=5422 first-class own layer: MS_FILE 4399 + MS_FOLDER 1007 + MS_USER 14 + MS_SITE 1 + MS_LIBRARY 1.
3. SS4 0-leak AT SCALE (my key independent deep-check -- props FIELDS, not just node_type):
   0 ms nodes carry a content/body/preview/text field across all 5422 (incl. the 4399 MS_FILE).
   Structure-only HELD at file scale (the 2-shell sample didn't exercise this; now it does).
4. 0 UNCATEGORIZED: all 5 node_types are the closed structure-only set.
5. 0 ms->aws edges: MS layer separate; zero mutation of AWS-resource nodes.

CARRY-FORWARD (NOT a COND-A blocker, per my accepted corrected invariant): 0.7.0's cluster-layer
fix (db4d40246, clusters aws->portal) landed AFTER this derive, so the 106 clusters + the 11232
ts_semantic portal nodes are still layer='aws' here. That is the FULL layer-taxonomy follow-on I
own (canonical node_type->layer aws/dash/ms partition -> aws becomes a true resource-only layer);
I verify it at AE's taxonomy-proposal sign-off. COND-A holds today on the resource-subset invariant.

SIGNED. RAVC AE (close the retarget ledger) + CC CTO + COO + 0.7.0.

-- 3.0.0_SA_CVO
