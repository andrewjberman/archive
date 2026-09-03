# NFRA_CLDGRPH projection artifact, manifest, and pointer contract

**Contract version:** 0.1 (Phase A, 2026-09-03)

**Owner:** `NFRA_CLDGRPH.TO-CG-B-3`, cell `CG-s-3`

**Canonical path:** this file. The intended `docs/architecture/` path is lane `ANY_CTO` and refused this seat, so the task-order fallback under the project tree is authoritative until the L4 owner lifts it into PRD v0.5.

**Scope:** `s3://opal-313476888478-globgrph/projection/` only. Bucket versioning remains OFF. This contract never writes `warehouse/_branch_head.main.json`.

This document is the binding producer/reader contract for the cloud Kuzu projection. A publish is artifact-first and pointer-last. The pointer is the only mutable object and is never deleted. Every object below the versioned artifact prefix is immutable after it is first written.

## 1. Vintage and prefix grammar

`<vintage>` is the exact `committed_at_iso` value in the consumed `warehouse/_branch_head.main.json` marker. It must be a fixed-width UTC ISO-8601 token matching `YYYY-MM-DDTHH:MM:SS.ffffff+00:00`. Under that grammar, lexical order is chronological order.

The versioned prefix is:

```text
projection/<vintage>/
```

The manifest's `vintage` and `committed_at` fields must both equal `<vintage>`, byte for byte. A producer refuses a marker whose timestamp is not canonical UTC. It never invents a wall-clock vintage and never substitutes `built_at` for the source vintage.

## 2. Artifact layout

One publish contains exactly these two objects:

```text
projection/<vintage>/kuzu_nessie_db
projection/<vintage>/_build_manifest.json
```

`kuzu_nessie_db` is the raw, uncompressed Kuzu 0.11.x database file emitted by the engine. It is not ZIPped, tarred, multipart-concatenated, or renamed inside an archive. The local sibling `<db>._build_manifest.json` is normalized to the S3 object name `_build_manifest.json`. If a later Kuzu version emits a directory or multiple database files, that is a contract-version change; the producer must not silently archive or flatten it under version 0.1.

CG-s-10 measured the raw database at `46,993,408 B` and the database plus its then-current manifest at `46,994,310 B`, identically in two full builds. Version 0.1 therefore admits a diagnostic publish-set band of `42,294,879..51,693,741 B` (the measured combined baseline +/-10%). The exact file size and SHA-256 in the manifest are the completeness proof; the band is an independent sanity gate. An out-of-band publish is refused before the pointer PUT and surfaced as a surprise rather than silently widening the contract.

## 3. `_build_manifest.json`

The object is canonical UTF-8 JSON. Keys are sorted and the serialized bytes are the bytes hashed into the pointer. These fields are required; their meaning is defined here once for both producer modes.

| Field | Producer semantics |
|---|---|
| `schema_version` | Integer `1` for this contract. |
| `vintage` | Exact consumed marker `committed_at_iso`; also the artifact-prefix token. |
| `committed_at` | Exact consumed marker `committed_at_iso`; must equal `vintage`. |
| `age_line` | Plain words derived from `committed_at`: `Built from the estate as of <YYYY-MM-DD HH:MM:SS UTC>.` A reader may display this sentence without knowing build internals. |
| `nessie_commit_hash` | Exact hash from the consumed branch-head marker. |
| `nodes_snapshot_id` | `graph_nodes.snapshot_id` from that marker. |
| `edges_snapshot_id` | `graph_edges.snapshot_id` from that marker. |
| `writer_id` | Source-marker writer identity from the consumed marker, such as `derive_runner` or `incremental_updater`; this is not the projection worker identity. |
| `built_at` | UTC ISO-8601 time after the artifact is closed and before verification begins. It describes the projection build, not estate vintage. |
| `producer` | Object with `mode` (`full` or `incremental`), `engine` (`kuzu`), `engine_version`, and `source_commit` for the exact worker bytes. |
| `node_count` | Post-load `MATCH (n:CloudNode) RETURN count(*)` against the completed artifact, for both full and incremental producers. It is never an input-row or MERGE-attempt count. |
| `edge_count` | Post-load `MATCH ()-[e:CloudEdge]->() RETURN count(*)` against the completed artifact, for both full and incremental producers. It is never an input-row or MERGE-attempt count. |
| `edges_skipped_missing_endpoint` | Count of consumed `graph_edges` source rows excluded because either normalized endpoint is absent from the canonical node-key set. It remains its own field and is never folded into `edge_count`, `node_count`, or an error total. Both producer modes compute it over the exact consumed snapshots. |
| `artifact` | Object with `format: "kuzu-raw-v0.11"`, `files`, `total_size_bytes`, and `expected_publish_set_size_band_bytes`. `files` contains exactly one entry for `kuzu_nessie_db` with `size_bytes` and lowercase hex `sha256`. |

Required shape:

```json
{
  "schema_version": 1,
  "vintage": "2026-09-03T13:23:55.222893+00:00",
  "committed_at": "2026-09-03T13:23:55.222893+00:00",
  "age_line": "Built from the estate as of 2026-09-03 13:23:55 UTC.",
  "nessie_commit_hash": "<64 lowercase hex>",
  "nodes_snapshot_id": 7140819680255399272,
  "edges_snapshot_id": 1026441646305052092,
  "writer_id": "incremental_updater",
  "built_at": "<UTC ISO-8601>",
  "producer": {
    "mode": "full|incremental",
    "engine": "kuzu",
    "engine_version": "0.11.3",
    "source_commit": "<40 lowercase hex>"
  },
  "node_count": 27134,
  "edge_count": 58432,
  "edges_skipped_missing_endpoint": 383,
  "artifact": {
    "format": "kuzu-raw-v0.11",
    "files": [
      {
        "name": "kuzu_nessie_db",
        "size_bytes": 46993408,
        "sha256": "<64 lowercase hex>"
      }
    ],
    "total_size_bytes": 46993408,
    "expected_publish_set_size_band_bytes": {
      "baseline": 46994310,
      "minimum": 42294879,
      "maximum": 51693741
    }
  }
}
```

The numbers above illustrate the measured 2026-09-03 graph and size baseline. Each real publish stamps its own observed values. `node_count` and `edge_count` must agree with direct counts on the artifact regardless of producer mode.

## 4. Pointer object

There is exactly one pointer:

```text
projection/current.json
```

Its entire body is canonical UTF-8 JSON:

```json
{
  "schema_version": 1,
  "vintage": "2026-09-03T13:23:55.222893+00:00",
  "artifact_prefix": "projection/2026-09-03T13:23:55.222893+00:00/",
  "manifest_key": "projection/2026-09-03T13:23:55.222893+00:00/_build_manifest.json",
  "manifest_sha256": "<64 lowercase hex>"
}
```

The pointer is written with one ordinary, non-multipart S3 `PutObject` after verification. It is never deleted. Before PUT, the writer reads the current pointer if one exists and refuses any candidate whose parsed UTC vintage is not strictly later. An equal vintage is idempotent only when prefix, manifest key, and manifest SHA-256 all match; otherwise it is refused. A backward-vintage attempt is refused and surfaced as a surprise.

## 5. Publish algorithm and mechanical completeness property

1. Read one branch-head marker and retain its exact vintage, Nessie hash, snapshot ids, and writer id.
2. Build into `projection/<vintage>/` without touching `projection/current.json`.
3. Close the database, compute the raw file's byte count and SHA-256, run the post-load node and edge `COUNT(*)` queries, compute `edges_skipped_missing_endpoint`, and write `_build_manifest.json`.
4. Read every declared artifact object back. Require the exact file set, byte counts, and SHA-256 values; require the manifest's prefix/vintage equality, source pins, count semantics, and size band. Hash the exact manifest bytes.
5. Re-read `projection/current.json` and apply the strictly-forward rule.
6. PUT the pointer body once. No later artifact or manifest write is permitted for that vintage.

Therefore a pointer can name only a complete, verified artifact. A hand-written pointer object is a plant and never a publish.

## 6. Reader straddle obligation

A reader must not treat one pointer GET as a transaction over later object GETs:

1. GET pointer P1.
2. GET P1's manifest; verify its SHA-256, vintage, committed-at value, and artifact prefix against P1.
3. GET and verify every manifest-declared artifact file.
4. GET the pointer again as P2.
5. If P2 and P1 carry the same vintage and manifest SHA-256, use the artifact. If they differ, discard the first read and repeat from P2, taking the newer pointer's artifact. A reader never combines a manifest or artifact from two vintages.

This rule closes the only per-object atomicity gap: an S3 pointer overwrite is atomic and read-after-write consistent, but a reader can straddle the overwrite between its own GETs.

## 7. Recovery property under S14

The Pipe acknowledges on task invocation, so a task that dies during its run is not SQS-redriven. Artifact-first/pointer-last is the retry safety:

- A publish that dies before the pointer PUT is invisible to readers because the previous pointer remains intact.
- The next real marker stamp builds a new immutable vintage and advances the pointer only after that new artifact verifies; this heals service without depending on redrive.
- An incomplete abandoned prefix is never selected, never repaired in place, and never made current by hand.
- A publish that completes the pointer PUT can only name the already-verified artifact from steps 1-5.

The nightly 02:00Z derive guarantees a later stamp even if no intraday stamp arrives.

## 8. Binding handoffs

**CG-s-4 serving service:** read only `projection/current.json`; enforce the two-pointer straddle algorithm; verify `manifest_sha256`; fetch the raw `kuzu_nessie_db`; reject incomplete, mismatched, backward, or out-of-band publications. A failed publish remains invisible and the previous pointer remains serviceable.

**CG-s-6 thin client:** display the manifest's `age_line` verbatim. Its source is `committed_at`, not `built_at`, local file mtime, or wall-clock inference. The client never chooses full versus incremental and never compiles a graph.

**CG-s-7 operator status:** begin at `projection/current.json`, apply the same straddle rule, and report `vintage`, `age_line`, `built_at`, `nessie_commit_hash`, both snapshot ids, source `writer_id`, `producer.mode`, `producer.source_commit`, `node_count`, `edge_count`, `edges_skipped_missing_endpoint`, exact artifact bytes, and expected size-band status. A pre-pointer crash reports the previous healthy vintage, not a half-publish.

## 9. Grounding

- MERGE identity and count semantics: `infra/aws/globgrph/kuzu_nessie_load.py:210-240` @`117e539280d678e946f5c74a1f2593e07d41e01a`.
- Existing manifest stamp: `infra/aws/globgrph/kuzu_nessie_load.py:251-268` at the same commit; Phase B conforms it to this field set after TO-CG-B-2 completes.
- Measured artifact size: `CG-s-10.full-fallback-duration.result.md:91-155` @`a9aea6f3ce`.
- S14 recovery premise: `INVESTIGATION_v1.md` row `NFRA_CLDGRPH-S14` @`6c0297289b`.
