# pipeline-override: Andrew-direct ~16:5xZ 2026-10-08, the graph-coherence build runs WITHOUT project registration (4.0.0_SA_CRO leads; CTO half @1d61e96831 names this seat COO co-signer and 0.7.0_AE_CloudOps the applier)
<task_order>
  <metadata>
    <id>GRAPH_OVERLAY.TO-APPLY-1.fabric-overlay-projection-worker-deploy-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NONE (Andrew-direct fast build, no project registration: 4.0.0_SA_CRO leads, ~16:5xZ)</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>

  <objective>
    Land the fabric overlay in the served graph: commit the patch, build and push the projection image, and move ONLY the
    projection worker task family to the new digest. The next projection then carries three new Kuzu tables (`FabricNode`,
    `FabricEdge`, `FabricLink`) and two manifest counts; the estate tables are not written.
  </objective>

  <context>
    Patch: `org/tier1_exec/4.0.0_SA_CRO/deliverables/FABRIC_OVERLAY_20261008.patch` (4 files under `infra/aws/globgrph/`;
    `git apply --check` clean on laptop CLOUD at ~18:3xZ). `infra/aws/` is the CLOUD_OPS_OR_ETL lane: you commit it.
    The image tag is shared by FOUR task families (derive runner, projection worker, projection server, cse producer).
    Halves, both SIGNED; read both in full and carry every condition:
    - request (blast radius): `org/tier1_exec/4.0.0_SA_CRO/deliverables/FABRIC_OVERLAY_SIGNOFF_REQUEST_20261008.md` @b337c560da
    - CTO: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_FABRIC_OVERLAY_SERVED_GRAPH_20261008.md` @1d61e96831
    - COO: `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_FABRIC_OVERLAY_SERVED_GRAPH_20261008.md` @0b0180e42a
  </context>

  <the_act>
    1. Load /cloud-ops. Run `python -m pytest infra/aws/globgrph/tests/test_kuzu_fabric_overlay.py` and the worker's existing
       tests after `git apply` in your working tree; any failure is a STOP before commit.
    2. BEFORE (record each): the current image DIGEST of all four task families (one `describe-task-definition` sweep of every
       family that pulls the tag); `projection/current.json` bytes digest and LastModified (UTC, `s3api`); the worker task's
       memory and any timeout, against the last full builds (849-985 s) plus 4 min -- a limit that would be crossed is a STOP.
    3. Open ONE NEVER-2 ledger entry in `org/critical_paths/change_management/` naming all four families, the saved digests,
       the pointer, the three halves and the rollback (`GLOBGRPH_FABRIC_OVERLAY=0` on the worker task definition; or the
       worker family back to its saved digest; or repoint `projection/current.json` to the saved bytes).
    4. PIN the derive runner, projection server and cse producer families to their CURRENT digest (new task-definition
       revisions referencing the digest, services/schedules moved to them) BEFORE the tag moves. A family that cannot be
       pinned is a STOP (CTO half).
    5. Commit the patch (`.tools/safe-commit.sh`, your lane), build, push the image, and move ONLY the projection worker
       family to the new digest.
    6. PROOF, on the next projection publish (fire the worker's own next trigger if one is due within the hour; otherwise
       report the time it will run): the manifest carries `fabric_node_count` > 0 and `node_count` in the 29,5xx class;
       `comp-kuzu "MATCH (n:FabricNode) RETURN n.node_type, count(*)"` answers with a VINTAGE line newer than the deploy; the
       three pinned families still run their saved digests. On the failure branch (worker log `WARN: FABRIC_OVERLAY rc=`), the
       estate published unchanged: report it, set `GLOBGRPH_FABRIC_OVERLAY=0`, and report.
    7. Close the entry.
  </the_act>

  <bounds>
    - The four task families' definitions and the one image only. No Terraform apply unless the families are declared in
      Terraform: then the change goes through `.tools/safe-apply.sh` and you say which root.
    - No delete of any projection vintage. No push of a shared branch.
  </bounds>

  <paths>
    infra/aws/globgrph/Dockerfile
    infra/aws/globgrph/kuzu_fabric_overlay.py
    infra/aws/globgrph/projection_worker.py
    infra/aws/globgrph/tests/test_kuzu_fabric_overlay.py
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: RUN by the applier at step 6 (the worker's next trigger).
comp-iam: DECLARED-NOT-APPLICABLE no identity change (the worker role's read of the graph bucket is DESIRED in projection.tf; a live refusal fails the overlay, which WARNs and publishes the estate).
comp-adversary: RUN -- the shared tag moving three other families (pinned by digest first, step 4; checked again at step 6); a broken publish (estate failure branch; pointer saved; quick-off flag); a time or memory overrun (step 2 headroom check); BLIND: ad hoc unlabelled MATCH (n) counts will include fabric nodes (COO half item 4).
lane: the <paths> block names the four patch files, the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="F-OVERLAY"><invocation>comp-kuzu "MATCH (n:FabricNode) RETURN n.node_type, count(*)"</invocation><expect>VINTAGE:</expect></criterion>
</proof_of_spec>
  AC1's row states the VINTAGE time (after the deploy), the per-type counts, the manifest's `fabric_node_count` and
  `node_count`, and the three pinned families' digests read after.

  <report>
    Report ONCE to 2.0.0_SA_COO~C (copy 4.0.0_SA_CRO) when the entry closes, or at a STOP (name the step): test results; the
    four saved digests and the three pinned revisions; the new worker digest; the deploy time in UTC in the subject line; the
    first publish's manifest counts and VINTAGE; the failure-branch evidence if any; the ledger path and close; the proof
    instance (named with this order's full id) and its check; commit hashes and the measured push state.
  </report>
</task_order>
