# NFRA_CLDGRPH CG-s-2/CG-s-3 worker revision 3 result

`NFRA_CLDGRPH.TO-CG-C-2` is complete at the implementation and live-exercise layers. The conditional publisher, verified forward-only pointer writer, incremental compaction, exact integrity checks, and measured deadline default are deployed in task-definition revision 3. One authentic producer event advanced the live pointer through S3 -> SQS -> Pipe -> ECS; both same-vintage arms and both deadline caller arms were then exercised without altering the valid current artifact.

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-C-2",
  "assignee": "0.7.0_AE_CloudOps~S",
  "source_commit": "a38c0437eb1c6207040c99361f302d7676085321",
  "image": {
    "repository": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner",
    "tag": "latest",
    "digest": "sha256:68bd8b932689a331928c1c3a6cc00fe124d24e04e7a9b64ba008f1a2d3de10e8",
    "build_id": "globgrph-derive-build:efc258e6-713c-47ae-ba79-fa2e691e0d0e",
    "build_source_head": "649164d75bc96b7c9f3001a9342108a5852ad0a2"
  },
  "applied": {
    "task_definition": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:3",
    "pipe": "arn:aws:pipes:us-east-1:313476888478:pipe/opal-globgrph-projection-worker",
    "pipe_state": "RUNNING",
    "pipe_target_revision": 3,
    "cpu": 2048,
    "memory_mib": 16384,
    "projection_worker_revision": "3"
  },
  "deadline": {
    "default_seconds": 3600,
    "slowest_accepted_cloud_full_seconds": 835,
    "budget_to_observed_ratio": 4.31,
    "spare_seconds": 2765,
    "deployed_override_seconds": 3600,
    "inheriting_observation": "KUZU_REBUILD_DEADLINE_S=3600 source=measured-default",
    "explicit_task_id": "bd842c7582a840f0aa0fe10541149784",
    "explicit_observation": "KUZU_REBUILD_DEADLINE_S=3600 source=environment"
  },
  "terraform": {
    "targeted_plan": "1 add, 2 change, 1 destroy",
    "targeted_apply": "1 added, 2 changed, 1 destroyed",
    "targets": [
      "aws_ecs_task_definition.projection_worker",
      "aws_iam_role_policy.projection_pipe",
      "aws_pipes_pipe.projection_worker"
    ],
    "unscoped_post_apply_addresses": [
      "aws_glue_partition.tool_activity[\"rolling_log\"]",
      "aws_glue_partition.tool_activity[\"rolling_log_summary\"]",
      "aws_glue_partition.tool_activity[\"routing\"]",
      "aws_sns_topic_subscription.critical_surface_alerts_email"
    ],
    "owned_addresses_in_unscoped_post_apply": 0,
    "deployment_ledger": "CLOSED 7/7"
  },
  "authentic_advance": {
    "cloudtrail_event_id": "675113f0-3085-4734-b459-43654615c6ce",
    "lambda_request_id": "ce77d595-65da-5b36-a749-b686a038ff26",
    "pipe_execution_id": "358ac19b-d1f7-4d0c-9c92-489e358e3e1c",
    "task_id": "f8b288ad95ec42dab2d17ef5a33cbd29",
    "task_exit_code": 0,
    "before_vintage": "2026-09-03T17:01:08.128628+00:00",
    "after_vintage": "2026-09-03T19:02:18.412096+00:00",
    "before_manifest_sha256": "28ed81e28144fa3db6dc880adf55ff1076c1b376d36b4b8b1d8597d1cc4a8f1c",
    "after_manifest_sha256": "751b870534c474298e0e968390f143e325b4741a4a4fc471c3bf341cd39c0b58",
    "pointer_log_order": ["POINTER_VERIFY_OK", "POINTER_PUT_OK"]
  },
  "incremental_integrity": {
    "prefix": "projection/2026-09-03T19:02:18.412096+00:00/",
    "mode": "incremental",
    "exact_object_count": 2,
    "manifest_bytes": 1540,
    "manifest_sha256": "751b870534c474298e0e968390f143e325b4741a4a4fc471c3bf341cd39c0b58",
    "artifact_bytes": 34824192,
    "artifact_sha256": "29a3ded43743baa46a3ed8c399dc1d672eb385ab286c1cf2cca5d8c35f551116",
    "full_artifact_bytes_for_record": 47964160,
    "checkpointed_bytes": 83615744,
    "reclaimed_bytes": 48791552,
    "direct_node_count": 27225,
    "direct_edge_count": 58606,
    "declared_node_count": 27225,
    "declared_edge_count": 58606,
    "cross_mode_band_present": false
  },
  "same_vintage": {
    "byte_identical_task_id": "842093d9e6874ebca80f4ad8b495be1a",
    "byte_identical_exit_code": 0,
    "byte_identical_result": "POINTER_NOOP status=already_current; pointer_written=false",
    "non_identical_task_id": "fd3d9ea9afdc46749ab7b84fcf77d16f",
    "non_identical_exit_code": 0,
    "non_identical_result": "IMMUTABLE_REFUSED then EXPECTED_COLLISION_REFUSAL",
    "refusal_seam": "The deployed image called the production conditional-create helper with different bytes against the existing manifest key. If-None-Match:* made an overwrite impossible; the helper read the existing object, detected the difference, and raised the expected refusal.",
    "manifest_preserved_etag": "d66b9b358248d49352149a264e2ae610",
    "pointer_preserved_etag": "7b16c2239928aaa255808d6080ff19b2"
  },
  "push_state_at_report": {
    "origin_cloud": "351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee",
    "source_commit_is_origin_cloud_ancestor": false,
    "head_is_origin_cloud_ancestor": false,
    "push_performed": false
  }
}
```

## Code and control evidence

The implementation is one five-file commit, `a38c0437eb1c6207040c99361f302d7676085321`, authored by this exact seat. `projection_worker.py:163-224` conditionally creates both versioned objects and accepts only exact-byte identity. `projection_worker.py:246-407` validates the exact two-object set, declared byte size and SHA-256, canonical prefix/vintage, and direct Kuzu counts. `projection_worker.py:413-448` performs remote verification before the forward-only pointer decision and PUT. `projection_worker.py:552` records compaction. No cross-mode byte-band constant or manifest field remains.

`kuzu_nessie_load.py:460-474` derives the default from the measured maximum 835-second accepted cloud full load: 3600 / 835 = 4.31x, leaving 2,765 seconds. `projection.tf:237-239` stamps worker revision 3 and preserves both explicit 3600-second task overrides. The focused worker/deadline suite passed 12/12; the combined worker/server/incremental/deadline suite passed 19/19; Terraform validation passed.

The authentic trigger was one re-PUT of the bucket's already-existing ordered six-tag set. CloudTrail recorded `PutBucketTagging` event `675113f0-3085-4734-b459-43654615c6ce` at 18:59:54Z. The incremental Lambda wrote one real node and stamped the 19:02:18 marker; the Pipe launched revision-3 task `f8b288ad95ec42dab2d17ef5a33cbd29`. That task completed the incremental refresh in 4.002 seconds and the entire worker in 6.999 seconds, compacted the DB, verified the S3 readback, and advanced the pointer. C1 was immediately routed both vintages and task identity and independently observed the new pointer through its owned service surface.

The exact prefix contains only `_build_manifest.json` (1,540 bytes) and `kuzu_nessie_db` (34,824,192 bytes). Independent streamed hashes matched the manifest and pointer. The worker's readback opened the actual downloaded Kuzu file and directly counted 27,225 `CloudNode` nodes and 58,606 `CloudEdge` relationships before `POINTER_PUT_OK`. For comparison, the prior full artifact was 47,964,160 bytes; size is diagnostic context, not an acceptance band.

## Exact contract text for relay to `0.7.0_AE_CloudOps~T`

The contract owner should replace §2 and §5 with the following exact wording. This text deliberately removes the old cross-mode band; it does not edit the owner's file.

> ## 2. Artifact layout
>
> One publish contains exactly these two objects:
>
>     projection/<vintage>/kuzu_nessie_db
>     projection/<vintage>/_build_manifest.json
>
> `kuzu_nessie_db` is the raw, uncompressed Kuzu 0.11.x database file emitted by the engine. It is not ZIPped, tarred, multipart-concatenated, or renamed inside an archive. The local sibling `<db>._build_manifest.json` is normalized to the S3 object name `_build_manifest.json`. If a later Kuzu version emits a directory or multiple database files, that is a contract-version change; the producer must not silently archive or flatten it under this contract version.
>
> Completeness is an integrity property, not a cross-mode size band. The producer must read back exactly the two objects above; the database object's observed byte count and SHA-256 must equal the manifest's declared `size_bytes`, `sha256`, and `total_size_bytes`; the manifest's canonical bytes must hash to the pointer's `manifest_sha256`; and the manifest's `node_count` and `edge_count` must equal direct `COUNT(*)` queries on the read-back database. The manifest, prefix, and pointer must name one identical canonical vintage. Full and compacted-incremental databases may have different valid byte sizes, so no fixed publish-set band accepts or refuses a publication and no `expected_publish_set_size_band_bytes` field is written. Observed sizes may be recorded as non-binding operational diagnostics only.
>
> ## 5. Publish algorithm and mechanical completeness property
>
> 1. Read one branch-head marker and retain its exact vintage, Nessie hash, snapshot ids, and writer id.
> 2. Build a local candidate for `projection/<vintage>/` without touching `projection/current.json`. On the incremental path, compact the completed candidate before conformance and publication.
> 3. Close the database, compute the raw file's exact byte count and SHA-256, run post-load `CloudNode` and `CloudEdge` `COUNT(*)` queries, compute `edges_skipped_missing_endpoint`, and serialize canonical `_build_manifest.json` bytes.
> 4. Create each versioned object with `If-None-Match: *`. If the key already exists, read it back: exact byte equality is an idempotent no-op and any difference is a refused same-vintage collision. Never overwrite a versioned object.
> 5. List and read the candidate prefix back. Require exactly `kuzu_nessie_db` and `_build_manifest.json`, the declared exact byte count and SHA-256, canonical manifest bytes, prefix/vintage equality, source pins, and direct database counts equal to the manifest's `node_count` and `edge_count`. Hash the exact manifest bytes. No cross-mode byte band participates in this integrity decision.
> 6. Re-read `projection/current.json` and apply the strictly-forward rule. An equal vintage is a no-op only when prefix, manifest key, and manifest SHA-256 all match; a differing equal vintage or a backward vintage is refused.
> 7. PUT the canonical pointer body once. No later artifact or manifest write is permitted for that vintage.
>
> Therefore a pointer can name only a complete, read-back-verified artifact. A hand-written pointer object is a plant and never a publish.

Conforming collateral edits in the owner's v0.2 document are mechanical: delete `expected_publish_set_size_band_bytes` from §3's field list and JSON example; replace “out-of-band” reader/operator language in §§8-9 with the exact integrity result above. Those edits do not change the two-object layout, manifest count semantics, pointer grammar, or reader-straddle obligation.

## Boundaries and measured push state

The serving service, gateway, client, deriver, marker, and foreign Terraform addresses were not edited. No artifact or pointer was deleted or manually planted. `git ls-remote origin refs/heads/CLOUD` returned `351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee`; both the C2 source commit and current local HEAD returned ancestry rc 1 against that remote head. No push was performed.

