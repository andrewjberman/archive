# GRAPH_OVERLAY first-publish verification complete

Original worker deployment:2026-10-08T20:56:38.290Z task7 registration,Pipe7 modified20:56:53Z. safeapply1/2/1 and targetedreplan0 were recorded in activation-readback.json/overlay-retry-apply.txt. Predeploy tests12 passed as recorded for retry; no new source change or deployment in this verification. Build/pin evidence and before-pointer remain in this directory.

CRO107540 identified the real first publish. Independently read current.json, verified manifestbytesSHA256 equals pointer manifest_sha256, then queried served graph with mandated comp-kuzu invocation. Vintage2026-10-09T00:49:09.369447+00:00 (newer than deploy),incremental. Manifestdc305b5abee7;node_count29586,edge_count63213,fabric_node_count4819,fabric_edge_count16864. FabricNode types:BOX4,SEAT361,SURFACE504,COMMIT3922,PROJECT28 (sum4819). first-publish-manifest.json and first-publish-readback.json hold full manifest/hash/pointer.

Re-read all7 taskfamilies and7 existing consumerbindings; all unchanged from activation. Worker digestd3037f32;other6saved digest17ccc9b01855. Exact reads:
- globgrph-comp-learns-producer:4 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:17ccc9b01855138e2abd0c36938c62a21ffd0730bf7886b9758a5317b4d24d04
- globgrph-cse-producer:4 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:17ccc9b01855138e2abd0c36938c62a21ffd0730bf7886b9758a5317b4d24d04
- globgrph-derive-runner:9 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:17ccc9b01855138e2abd0c36938c62a21ffd0730bf7886b9758a5317b4d24d04
- globgrph-fedobs-producer:4 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:17ccc9b01855138e2abd0c36938c62a21ffd0730bf7886b9758a5317b4d24d04
- globgrph-projection-worker:7 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:d3037f32c0143855a283f5e997fa83d8f09fc23755608c190896ab0adfd3f3b1
- globgrph-resource-summaries-producer:4 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:17ccc9b01855138e2abd0c36938c62a21ffd0730bf7886b9758a5317b4d24d04
- globgrph-serving:4 313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:17ccc9b01855138e2abd0c36938c62a21ffd0730bf7886b9758a5317b4d24d04

Worker logs from2026-10-09T00:45Z:21lines,2positive FABRIC_OVERLAY INFO entries,0 WARN: FABRIC_OVERLAY rc=. Each positive reports4819nodes,15958edges and906links (sum16864). No failure-branch rollback indicated. No trigger fabricated, no apply, no vintage deletion.

Released external hold and closed V1 on org/critical_paths/change_management/20261008T2054Z_graph-overlay-worker-retry-laptop-20261008_deploy_completion.md; ledger CLOSED alllegs,sentinel removed. Existing activation evidence1b5da75554; final closurecommit supplied in issuer report. Full-id proof updated to PASS for firstpublish and corrected obsolete pending-state prose. LOCAL,no push;ls-remote origin/CLOUD e6de770dd328ee5522ff393ee917c24ee6f44eda;origin/box/laptop af564065fb89cc2208eb222e75c179888c085e5d. Issuer owns task status flip.
