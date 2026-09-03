# CG-s-3 -- projection contract result

**Task order:** `NFRA_CLDGRPH.TO-CG-B-3`

**Seat:** `0.7.0_AE_CloudOps~T`

**Phase state:** Complete. Contract, publisher controls, producer agreement, duplicate census, two forward publishes, reader check, and both refusal controls are exercised.

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-B-3",
  "cell": "CG-s-3",
  "phase": "COMPLETE",
  "phase_b_release": {
    "condition": "issuer written release after TO-CG-B-2 reported no further Python edit pending",
    "observed_status": "released by issuer Msg 93769",
    "observed_at": "2026-09-03T16:04:02Z",
    "bounded_paths": [
      "infra/aws/globgrph/**",
      "infra/aws/terraform/globgrph/**"
    ]
  },
  "contract": {
    "path": "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.7.0_AE_CloudOps~T/PROJECTION_CONTRACT.md",
    "version": "0.1",
    "lane": "project-tree fallback; docs/architecture is ANY_CTO and refused this seat",
    "artifact_prefix_grammar": "projection/<vintage>/",
    "artifact_key": "projection/<vintage>/kuzu_nessie_db",
    "manifest_key": "projection/<vintage>/_build_manifest.json",
    "pointer_key": "projection/current.json",
    "pointer_rule": "single PutObject after full verification; strictly forward; never deleted",
    "artifact_format": "raw uncompressed Kuzu 0.11 database file",
    "measured_publish_set_baseline_bytes": 46994310,
    "expected_publish_set_size_band_bytes": [42294879, 51693741],
    "recovery_property": "a publish dying before pointer PUT is invisible to readers; the next real stamp publishes a new vintage and heals while the previous pointer remains intact"
  },
  "duplicate_census": {
    "measured_at": "2026-09-03T13:53Z",
    "edge_snapshot_id": 1026441646305052092,
    "edge_metadata_key": "warehouse/globgrph/graph_edges_6629328d-a582-46d2-80bc-5059de1a77ce/metadata/00000-d146d11e-e12a-4d20-af79-7f5da47ee62d.metadata.json",
    "node_snapshot_id": 7140819680255399272,
    "rows_read": 61071,
    "skipped_missing_endpoint": 383,
    "merge_attempts": 60688,
    "stored_distinct_identities": 58432,
    "duplicate_excess": 2256,
    "duplicate_identity_groups": 1632,
    "multiplicity": {
      "1580 identities occurred 2 times": 1580,
      "52 identities occurred 14 times": 52
    },
    "all_duplicate_rows_identical_on": [
      "src_id",
      "dst_id",
      "edge_type",
      "layer",
      "snapshot_ts",
      "props"
    ],
    "classification": {
      "expected_by_construction": {
        "excess": 13,
        "identity": "bd-exporter-profile ASSUMES bd-exporter-ec2-role",
        "reason": "comp_aws_cli observes the same profile-to-role relation once for each of 14 EC2 instances sharing that profile; the graph relation is intentionally one identity"
      },
      "finding_live_c2_instance_producer": {
        "excess": 2235,
        "edge_type": "CONTAINS",
        "layer": "semctl",
        "rel_tier": "C2i->C1",
        "reason": "c2_individuate deduplicates motif nodes by member set but appends their member edges for every raw match and emits that uncollapsed edge list",
        "source_owner": "3.0.0_SA_CVO -- c2_individuate.py"
      },
      "finding_eventbridge_projection": {
        "excess": 8,
        "edge_type": "TRIGGERS",
        "layer": "aws",
        "reason": "eight rules each have two configured target IDs for the same Lambda; target Id/Input are not carried into comp_aws_cli's edge props, so distinct target configurations collapse to one empty-props identity",
        "source_owner": "0.8.0_AE_CloudComp -- comp_aws_cli.py; live EventBridge target owners retain configuration ownership"
      }
    },
    "answer": "13 of 2256 excess rows are expected repeated observations of one logical edge. The remaining 2243 are findings: 2235 uncollapsed C2-instance emissions and 8 target-config identities made indistinguishable by the AWS graph producer. No fix is adjudicated by this cell; surprise row NFRA_CLDGRPH-S16 carries the owners."
  },
  "handoffs": {
    "CG-s-4": "Read projection/current.json only; verify manifest SHA-256 and use the two-pointer straddle rule; the artifact is raw kuzu_nessie_db; a pre-pointer crash is invisible and leaves the prior artifact current.",
    "CG-s-6": "Display manifest.age_line verbatim, sourced from committed_at; never infer age from built_at, mtime, or a local graph.",
    "CG-s-7": "Read pointer then manifest with the straddle re-read; report source pins, producer mode/commit, post-load counts, missing-endpoint count, exact bytes, and the 42,294,879..51,693,741 B expected publish-set band."
  },
  "phase_b": {
    "release_commit": "Msg 93769; B2 worker a9ef0f6160b6aa786b0321f1893e5089c08e118a and engine 117e539280d678e946f5c74a1f2593e07d41e01a",
    "pointer_writer": "infra/aws/globgrph/projection_worker.py @59aeb265cca69506ec8c02f76d11a2b615dbe195",
    "producer_agreement": {
      "graph_vintage": "2026-09-03T16:27:39.471730+00:00",
      "nodes_snapshot_id": 8525533673192182741,
      "edges_snapshot_id": 2253722689641059303,
      "full_manifest": {"mode": "full", "node_count": 27206, "edge_count": 58550, "edges_skipped_missing_endpoint": 383},
      "incremental_manifest": {"mode": "incremental", "node_count": 27206, "edge_count": 58550, "edges_skipped_missing_endpoint": 383},
      "full_direct_count": {"node_count": 27206, "edge_count": 58550},
      "incremental_direct_count": {"node_count": 27206, "edge_count": 58550},
      "incremental_delta": {"node_upsert": 0, "node_delete": 0, "edge_upsert": 0, "edge_delete": 0},
      "incremental_seconds": 5.450,
      "control": "all four count pairs equal; the pre-S8 merge-attempt value 60,688 is not reported as stored edge_count"
    },
    "publish_keys": [
      {
        "task": "968bf1a3ca4d48d5bc60244228bbfcda",
        "artifact_prefix": "projection/2026-09-03T13:23:55.222893+00:00/",
        "manifest_sha256": "cb26341dd4635d81af907cca21989d31f0cfb4c4d2854ae1337aec1c6dea51ca",
        "artifact_bytes": 47054848,
        "node_count": 27134,
        "edge_count": 58432,
        "pointer_status": "advanced",
        "pointer_written": true,
        "exit_code": 0
      },
      {
        "task": "fa5df7737afc48fdbda6a9106d5676b6",
        "artifact_prefix": "projection/2026-09-03T16:27:39.471730+00:00/",
        "manifest_sha256": "0c2c0052c43ca06ce92bb37fe822a733c4999a0405e2a8b456b015f14d40f101",
        "artifact_bytes": 48046080,
        "node_count": 27206,
        "edge_count": 58550,
        "pointer_status": "advanced",
        "pointer_written": true,
        "exit_code": 0
      }
    ],
    "reader_control": {
      "pointer_1_vintage": "2026-09-03T16:27:39.471730+00:00",
      "manifest_vintage": "2026-09-03T16:27:39.471730+00:00",
      "pointer_2_vintage": "2026-09-03T16:27:39.471730+00:00",
      "pointer_bytes_same": true,
      "manifest_sha256_match": true,
      "artifact_prefix_match": true
    },
    "incomplete_artifact_refusal": {
      "plant_key": "projection/2026-09-03T13:23:54.000000+00:00/kuzu_nessie_db",
      "written_by": "this seat via .tools/aws s3api put-object at 2026-09-03T16:25:44Z",
      "size_bytes": 71,
      "manifest_present": false,
      "size_band_minimum_bytes": 42294879,
      "result": "PublicationRefused: expected the database plus _build_manifest.json, actual set contained only the database; projection/current.json was unchanged and absent"
    },
    "backward_vintage_refusal": {
      "candidate": "2026-09-03T13:23:55.222893+00:00",
      "current": "2026-09-03T16:27:39.471730+00:00",
      "result": "PointerRefused: backward vintage refused: candidate=2026-09-03T13:23:55.222893+00:00 current=2026-09-03T16:27:39.471730+00:00",
      "pointer_sha256_before": "432ec2848835649bfd01c548589dfa4ad04dfba855b0ac13412e303fd25c3359",
      "pointer_sha256_after": "432ec2848835649bfd01c548589dfa4ad04dfba855b0ac13412e303fd25c3359",
      "pointer_etag_before": "3e945885dc5bb2d9e3d2c98811297ac6",
      "pointer_etag_after": "3e945885dc5bb2d9e3d2c98811297ac6",
      "pointer_unchanged": true
    },
    "boundary_disclosures": {
      "S21": "This seat stopped B2 task 6aa88972790949a5bbe9b315381ec895 after 288.286 seconds at 2026-09-03T16:26:35.641Z with reason 'CG-s-3 prevent pre-contract image collision at released vintage'; issuer Msg 93787 ruled the stop outside this order. Exit 137 is not labeled OOM.",
      "S23": "B2 task fa5df7737afc48fdbda6a9106d5676b6 crossed B2's no-pointer bound and advanced projection/current.json. S23 @952fae0cc4 routes disarm to B3-AC2; no undo. The completeness check and If-None-Match:* same-vintage guard @59aeb265cc supersede the bare shared writer, with deployment carried to round 3.",
      "runtime_actions_after_ruling": "No further B2 task-definition launch, stop-task, Pipe mutation, or queue mutation by this seat."
    }
  }
}
```

## Phase A evidence

The MERGE identity is normalized `(src, dst, edge_type, props)` at `infra/aws/globgrph/kuzu_nessie_load.py:210-226` @`117e539280d678e946f5c74a1f2593e07d41e01a`; the post-load stored count is at `:230-240`. A read-only PyIceberg census of the marker-pinned tables reproduced the complete denominator: `61,071 - 383 = 60,688`, and `60,688 - 58,432 = 2,256`.

All 2,256 excess rows were byte-identical across every stored source-table column. The split was then grounded against producer code and live read-only controls:

- `2,235` semctl/C2i excess rows: `c2_individuate.py:427-465,631-633` @`23220a7b20df85b669c6a9711e0ae9d50b3acd1a` deduplicates nodes by deterministic member-set id but appends edges before that collapse and emits the uncollapsed list. Neither static semctl spec contains an internal duplicate, and neither overlaps these duplicate identities.
- `13` AWS `ASSUMES` excess rows: `comp_aws_cli.py:1382-1398` @`59347e4d9ec9603562c6dd7095e13dd1ae630291` emits the profile-to-role relation inside the EC2 loop. A live read found exactly 14 EC2 instances using `bd-exporter-profile`, explaining the 14 identical observations of one logical relation.
- `8` AWS `TRIGGERS` excess rows: `comp_aws_cli.py:1500-1516` at the same commit emits only rule ARN, target ARN, and edge type. Live `events list-targets-by-rule` reads showed two target IDs on each of the eight rules, with target `Input` differing or absent; the graph row preserves neither field and collapses them to one identity.

`infra/aws/globgrph/derive_runner.py:313,357-376` @`ec0408628ac098ddbb0035da1f032964faa8b286` overwrites Iceberg from the concatenated edge list without a dedup pass. This cell answers and records the census; it does not adjudicate or implement a producer fix.

## Phase boundary

Phase A made no edit in either bounded infrastructure tree and did not run `comp-blast`. The issuer released Phase B in Msg 93769 after ~S stated no further Python edit was pending. The publisher/manifests landed at `5bb91c894d`; the issuer-ruled same-vintage conditional-create guard and S22 landed at `59aeb265cc`, deliberately not redeployed because Msg 93803 carries that B2 runtime act to round 3.

The already-running retained-marker task `968bf1a3ca4d48d5bc60244228bbfcda` and authentic Pipe task `fa5df7737afc48fdbda6a9106d5676b6` both finished at exit 0 through digest `sha256:1e1aaa14df31da756001f3a42b1f5b6c671e4d75586aeb72c96586534a50f01c`; their `PROJECTION_RESULT` records show two strictly forward pointer advances. The live reader control matched pointer/manifest/pointer vintages and manifest SHA. The 71-byte incomplete prefix and the older complete vintage were independently refused with the pointer unmoved. S23 records that the B2 task wrote a pointer outside its own bound; B3 disarms that shared-path hazard through the completeness and conditional-create controls without undoing a valid live pointer.
