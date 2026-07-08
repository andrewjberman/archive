# Task Order: NFRA_GLOBGRPH NODEGAP -- triage the 7 real graph_nodes coverage-gap endpoints (CVO-adjudicated, non-blocking)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-globgrph-nodegap</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps (globgrph node materialization) + 0.4.0_DT_ClientPlatform (bd-client-detail stale-edge decision, coordinate base COO)</issued_to>
    <date>2026-07-08</date>
    <status>staged -- LOW-PRIORITY (after FRESHGUARD/MOTIF-P0/GUARD-REFILE/S3); NON-BLOCKING (CSE-P2 stays closed, upstream node-coverage)</status>
    <prd_ref>docs/architecture/NFRA_GLOBGRPH_PRD.md</prd_ref>
    <dispatch_state>STAGED low-pri. CVO-characterized finding (routed to COO~B for dispatch). CSE-P2 is CLOSED + correct (materialized graph + loader correct); this is an UPSTREAM graph_nodes coverage gap only.</dispatch_state>
    <gate_note>CVO adjudicated the CSE-P2 dangling-edge chain: 27-edge radar -> 377 loader skipped_missing_endpoint -> ARN-vs-node_id join-key artifact -> ARN-aware anti-join = 13 distinct dangling endpoints -> 6 synthetic wildcards CLOSED-by-design + 7 REAL. Exact ARNs in CVO<->0.5.0_AE exchange.</gate_note>
  </metadata>

  <objective>Triage the 7 real dangling endpoints (edges reference them; graph_nodes doesn't materialize them) -- per endpoint: materialize-the-node, prune-the-stale-edge, or confirm-deliberate-out-of-scope. Close the graph_nodes coverage gap honestly.</objective>

  <requirements>
    <requirement id="1">MATERIALIZE the node for the 2 should-materialize resources: opal-drift-producer (CodeBuild) + dc2-test1-offpeak-orchestrator (custom SSM) -- add to the graph_nodes producer coverage.</requirement>
    <requirement id="2">PRUNE-OR-KEEP the stale-edge-suspect: bd-client-detail (decommissioned dead-route lambda -- likely a stale edge to prune, not a missing node). 0.4.0_DT / the edge-producer decides (coordinate base COO -- bd is a firm pipeline).</requirement>
    <requirement id="3">CONFIRM-OUT-OF-SCOPE (or materialize if wrong) the 4 likely-out-of-scope: 2 AWS-managed SSM (AWS-StartEC2Instance, AWS-RunPowerShellScript) + 2 EC2 subnets. Deliberate exclusion = document it (honest coverage, not a silent gap).</requirement>
  </requirements>

  <cross_domain_coordination>
    - CVO (3.0.0_SA_CVO) + 0.5.0_AE hold the exact 13/7 ARN set + evidence.
    - bd-client-detail touches the bd firm pipeline (base COO lane) -- coordinate, don't unilaterally prune a firm-pipeline edge.
    - comp-aws (NFRA_COMPAWS, deprioritized) is the AWS-resource-node recognizer domain -- reuse, don't rebuild.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Each of the 7 endpoints dispositioned: materialized / stale-edge-pruned / out-of-scope-documented. No silent gap remains (LAW-2 honest coverage).
    2. Re-run the ARN-aware anti-join -> the 7 real dangling either resolve (node exists / edge pruned) or are documented deliberate-out-of-scope. Ground on live graph state (Rule 22). RAVC COO~B + CVO.
  </acceptance_criteria>
</task_order>
```
