# CG-s-3 -- projection contract result

**Task order:** `NFRA_CLDGRPH.TO-CG-B-3`

**Seat:** `0.7.0_AE_CloudOps~T`

**Phase state:** Phase A complete; Phase B remains gated on TO-CG-B-2's committed `complete` status.

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-B-3",
  "cell": "CG-s-3",
  "phase": "A_COMPLETE_B_HELD",
  "phase_b_release": {
    "condition": "NFRA_CLDGRPH.TO-CG-B-2 status is complete at a named commit",
    "observed_status": "pending",
    "observed_at": "2026-09-03T13:58:51Z",
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
    "release_commit": null,
    "pointer_writer": null,
    "producer_agreement": null,
    "publish_keys": [],
    "incomplete_artifact_refusal": null,
    "backward_vintage_refusal": null
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

This seat did not edit either bounded infrastructure tree and did not run `comp-blast`; concurrent staged work there belongs to the TO-CG-B-2 seat. Phase B starts only after a committed TO-CG-B-2 `complete` flip is named here. It then adds the pointer writer to the worker's own publish path, conforms both manifest producers, exercises two real publishes, and runs the required refusal controls.
