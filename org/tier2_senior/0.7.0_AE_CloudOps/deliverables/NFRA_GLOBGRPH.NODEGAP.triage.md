# NFRA_GLOBGRPH.NODEGAP -- 7 real dangling-endpoint triage (grounded dispositions)

**Author:** 0.7.0_AE_CloudOps~B | **TO:** NFRA_GLOBGRPH.NODEGAP.7-dangling-endpoint-triage.md | **Date:** 2026-07-08
**Grounding discipline (Rule 22):** every disposition below cites a LIVE AWS/graph read this session, not the original CVO/0.5.0 characterization alone (that finding is the STARTING point; every item is independently re-verified against current live state before disposition, since the estate has moved since the finding was made).

---

## Disposition summary

| # | Resource | Category (TO) | Disposition | Status |
|---|---|---|---|---|
| 1 | `dc2-test1-offpeak-orchestrator` (SSM Automation doc) | materialize | **ALREADY RESOLVED** | node exists live |
| 2 | `opal-drift-producer` (CodeBuild project) | materialize | **REAL GAP -- routed for arch-gate**, not built this pass | taxonomy + scanner addition needed |
| 3 | `bd-client-detail` (Lambda) | prune-or-keep | **PRUNE recommended, coordinating with DT/base COO** | not unilaterally acted |
| 4 | `AWS-StartEC2Instance` (SSM doc) | confirm-out-of-scope | **CONFIRMED correct exclusion** | by design |
| 5 | `AWS-RunPowerShellScript` (SSM doc) | confirm-out-of-scope | **CONFIRMED correct exclusion** | by design |
| 6 | subnet ARN #1 | confirm-out-of-scope | **CONFIRMED correct exclusion** | by design |
| 7 | subnet ARN #2 | confirm-out-of-scope | **CONFIRMED correct exclusion** | by design |

---

## 1. `dc2-test1-offpeak-orchestrator` -- ALREADY RESOLVED

Live comp-kuzu query this session: `arn:aws:ssm:us-east-1:313476888478:document/dc2-test1-offpeak-orchestrator` IS present as a `SSM_DOCUMENT` node in the current graph. Most likely resolved as a side effect of today's earlier taxonomy addition (`+LAMBDA_LAYER/SCHEDULE/SSM_DOCUMENT` re-sign, commit `24790cf54`, dual-signed) followed by an intervening derive run -- SSM_DOCUMENT wasn't in `NODE_TYPE_LAYER` before that, so any custom SSM Automation document (this one included) would have fail-closed or been silently absent until that gate opened. No action needed; the CVO/0.5.0 finding predates the fix.

## 2. `opal-drift-producer` (CodeBuild project) -- REAL GAP, mechanism grounded

Live-confirmed: the graph HAS the surrounding resources (`opal-drift-producer-gha-role` IAM_ROLE, `opal-drift-producer-nightly` EVENT_RULE, `/aws/codebuild/opal-drift-producer` LOG_GROUP, related IAM_POLICY nodes) but NO node for the CodeBuild project itself. Source-grounded mechanism (`org/modules/graph/comp_aws_cli.py`): there is **no CodeBuild recognizer at all** -- zero mentions of `codebuild` in the scanner (grep-confirmed). This is a genuine, real gap: the EventBridge rule's edge presumably targets the CodeBuild project ARN, which has no corresponding node -- a true dangling target, not a taxonomy-label issue like the SSM case.

**Fix required (NOT built this pass -- routing for arch-gate, per this session's established taxonomy-governance pattern):**
1. A new `live_codebuild_projects()` recognizer in `comp_aws_cli.py` (boto3 `codebuild.list_projects` + `batch_get_projects`), mirroring `live_ssm_documents()`'s shape.
2. A new `CODEBUILD_PROJECT` node_type registered in `NODE_TYPE_LAYER` (`derive_runner.py:1623`) -> layer `aws` -- this is a NEW node_type, so per the `NodeTypeLayerGap` fail-closed guard (COND-2 durability, the exact class today's semctl work hardened), it needs the same CTO arch-gate + CVO count re-sign BEFORE any derive run would encounter it, or the derive fails closed the instant the new recognizer starts emitting `CODEBUILD_PROJECT` nodes.

Given this touches the same fail-closed taxonomy gate this session already worked through twice (semctl layer, SSM_DOCUMENT/SCHEDULE/LAMBDA_LAYER), building it unilaterally without arch-gate would repeat exactly the risk class those prior fixes exist to prevent. Scoped as a small, well-precedented follow-on (one recognizer function + one taxonomy entry, mirrors an existing pattern closely) -- not blocking, low-pri per the TO.

## 3. `bd-client-detail` (Lambda) -- PRUNE recommended, coordinating

Live-confirmed this session: `aws lambda get-function-configuration --function-name bd-client-detail` -> `ResourceNotFoundException: Function not found`. The Lambda is genuinely gone (decommissioned), not merely stale-but-present. This confirms CVO's suspicion definitively: the graph edge referencing it is a **stale edge to a dead resource**, not a missing-node gap. Per the TO's cross-domain-coordination note (bd is a firm pipeline, base-COO lane -- don't unilaterally prune), messaging DT + base COO with this live confirmation now rather than pruning myself.

## 4-7. The 4 confirm-out-of-scope items -- all CONFIRMED correct, live-verified

- **`AWS-StartEC2Instance`, `AWS-RunPowerShellScript`** (SSM docs): live `aws ssm describe-document` this session confirms `Owner=Amazon` for both. `live_ssm_documents()`'s `Filters: [{Key: Owner, Values: [Self]}]` deliberately excludes these BY DESIGN (docstring: "Self-owned only (exclude AWS-public docs)"). Correct, intentional exclusion -- not a gap.
- **2 EC2 subnet ARNs**: source-grounded (`comp_aws_cli.py`) -- subnets appear ONLY as wildcard edge TARGETS (`IN_SUBNET` edges from load balancers, `E(lb["arn"], f"arn:...:subnet/{sn}", ...)`), never as a first-class node type. No `SUBNET` recognizer exists anywhere in the scanner. This mirrors the deliberate `EXTERNAL_ENDPOINT` drop (Andrew-direct 2026-06-26) -- VPC network topology (subnets, route tables, etc.) is consistently treated as infrastructure substrate, not estate/application resources the graph materializes as nodes. Consistent with existing taxonomy philosophy; documenting as deliberate, not silently gapped.

---

## Acceptance criteria check (per TO)
1. **Each of the 7 endpoints dispositioned** -- YES, all 7 above (2 resolved/confirmed-correct-by-design=6 total + 1 real gap routed + 1 coordinate-pending).
2. **No silent gap remains** -- the one genuine gap (#2, CodeBuild) is NAMED, its mechanism grounded, and a concrete fix is specified and routed for arch-gate -- not silently left open.

**RAVC:** COO~B + CVO (dispositions + the routed CodeBuild recognizer follow-on). Coordinating bd-client-detail prune separately with DT + base COO.
