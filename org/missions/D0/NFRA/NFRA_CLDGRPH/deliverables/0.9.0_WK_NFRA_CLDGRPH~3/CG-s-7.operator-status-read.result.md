# CG-s-7 -- the operator status read: `comp-graph status` repointed at the projection pointer's manifest

**TO:** `NFRA_CLDGRPH.TO-CG-D-4` · **Cell:** `CG-s-7` · **Worker:** `0.9.0_WK_NFRA_CLDGRPH~3` · **Date:** 2026-09-04

## 1. BEFORE -- the wrong artifacts (measured at the cut)

`bash .tools/comp-graph status` (pre-repoint HEAD @5644fee152) reported a `CLOUD / CROSS-LAYER
(infra/aws/globgrph/)` group stating two LOCAL files under `infra/aws/globgrph/` -- `kuzu_db` and
`stitch_graph` -- neither of which is the served cloud projection (brief F6). Measured live today:

```
CLOUD / CROSS-LAYER (infra/aws/globgrph/)
  kuzu_db              MISSING      absent             no-TTL    comp-kuzu Cypher DB (AWS + stitch layers)  (build: kuzu_nessie_load.py --force (nightly 02:00 + intraday))
  stitch_graph         MISSING      absent             no-TTL    P2-STITCH unified cross-layer graph (build artifact)  (build: derive_stitch.py)
```

Both read `MISSING` because no such local files exist on this laptop -- the row was never reading
the served cloud artifact at all, so it could never distinguish a fresh publish from a stale one
or a night that ran from a night that did not.

The pointer + manifest read directly (before any code change), quoted:

**Pointer** `s3://opal-313476888478-globgrph/projection/current.json`:
```json
{"artifact_prefix":"projection/2026-09-04T05:53:37.689093+00:00/","manifest_key":"projection/2026-09-04T05:53:37.689093+00:00/_build_manifest.json","manifest_sha256":"44388b219db76b43203c490d0c45d539ca767faaa299a46c8d496c250a4b9087","schema_version":1,"vintage":"2026-09-04T05:53:37.689093+00:00"}
```

**Current manifest** (`projection/2026-09-04T05:53:37.689093+00:00/_build_manifest.json`, sha256
verified against the pointer's `manifest_sha256` -- match):
```json
{"age_line":"Built from the estate as of 2026-09-04 05:53:37 UTC.","artifact":{"files":[{"name":"kuzu_nessie_db","sha256":"577184c6f7100f00c4decccfe030483c39693a4aff2a9e16dbf75655275107bc","size_bytes":34832384}],"format":"kuzu-raw-v0.11","total_size_bytes":34832384},"built_at":"2026-09-04T05:54:06.928866+00:00","committed_at":"2026-09-04T05:53:37.689093+00:00","edge_count":58622,"edges_skipped_missing_endpoint":418,"edges_snapshot_id":6541343322795706185,"nessie_commit_hash":"7bd11ec84758a8bac997d7ba79f5c3fe06e2207c55ebdd584cf5cc2f5bc860bd","node_count":27244,"nodes_snapshot_id":92487625797322719,"producer":{"engine":"kuzu","engine_version":"0.11.3","mode":"incremental","source_commit":"649164d75bc96b7c9f3001a9342108a5852ad0a2"},"schema_version":1,"vintage":"2026-09-04T05:53:37.689093+00:00","writer_id":"incremental_updater"}
```

(This manifest omits `artifact.expected_publish_set_size_band_bytes`; the repoint reports that as
`NO-BAND` -- never a silent pass -- rather than inventing a band.)

**The last nightly full**, found by listing `projection/` (17 versioned prefixes, one bounded
`--delimiter /` call, 2026-09-03T13:23:54 .. 2026-09-04T05:53:37) and reading the manifest inside
today's `[02:00Z, 08:00Z)` window: `projection/2026-09-04T02:09:19.993324+00:00/_build_manifest.json`,
`writer_id: derive_runner`, `producer.mode: full`, `built_at: 2026-09-04T02:22:43.290435+00:00`,
`node_count: 27246`, `edge_count: 58646` -- matching the issuer's cut-time measurement exactly.

## 2. THE REPOINT

`org/modules/graph/graph_status_cli.py`'s cloud group no longer stats `infra/aws/globgrph/kuzu_db`
or `infra/aws/globgrph/stitch_graph.json`. It now:

1. Resolves `COMP_GRAPH_POINTER_URI` (default the live pointer; a bare path or `file://` is a
   local fixture) into an S3 `(bucket, key)` or a local `(directory, name)` base.
2. Reads via **boto3** if importable (measured importable here: `boto3 1.42.54` under both
   `python` and `python3`), else falls back to `.tools/aws s3 cp ... -` via subprocess -- the
   method actually used is recorded on the row as `read_method`.
3. Applies the reader straddle rule verbatim (`PROJECTION_CONTRACT.md` s.6): GET pointer P1, GET
   + SHA-256-verify its manifest, GET pointer again as P2, repeat from P2 if P1 != P2 (bounded to
   4 repeats).
4. Emits two rows in the `CLOUD / CROSS-LAYER` group:
   - `projection.current` -- verdict `PRESENT` or `UNVERIFIABLE (reason)`; reports `vintage`,
     `age_line`, `built_at`, `nessie_commit_hash`, both snapshot ids, `writer_id`,
     `producer.mode`, `producer.source_commit`, `node_count`, `edge_count`,
     `edges_skipped_missing_endpoint`, `artifact_bytes`, and `band_status`
     (`IN-BAND`/`OUT-OF-BAND`/`NO-BAND`).
   - `projection.last_night` -- `REFRESHED LAST NIGHT: YES at <built_at>` or
     `REFRESHED LAST NIGHT: NO (last full: <built_at>)`, computed per s.3 below.
   - Both rows: `query` = `comp-kuzu`, `rebuild` = `none -- the estate refreshes itself (FWD-2)`.
   - `--json` carries the identical fields flat on each `graphs[]` entry, plus
     `refreshed_last_night` (`True`/`False`/`None`) on `projection.last_night`.
5. A pointer/manifest that cannot be read (bad bucket, missing local plant, SHA-256 mismatch,
   JSON parse failure, straddle non-convergence) prints `UNVERIFIABLE (reason)` on both rows --
   never a pass, never a default.

Nothing else in the file changed: the local trace-layer group (`_collect`'s `graph`/`baseline`/
`platinum.*` rows), the FRESHNESS CONTRACT / POPULATION print block, and `cmd_clear` are byte-for-
byte the same logic as before the repoint (only the now-dead `_GLOBGRPH_DIR` constant, which
existed solely to build the two wrong paths, was removed).

## 3. "LAST NIGHT" -- the definition, written down

"Last night" is the most recent `02:00Z` boundary before now (the nightly schedule is
`cron(0 2 * * ? *)`, `infra/aws/terraform/globgrph/item2a.tf:439`). The night **RAN** if a
`producer.mode == "full"` manifest with `writer_id == "derive_runner"` exists whose `vintage`
falls inside `[boundary, boundary + 6h)`. Finding it means one bounded `list_objects_v2` /
`s3api list-objects-v2 --delimiter /` call over `projection/`, then reading at most 12 manifests
whose vintage falls in that window. A night that did **NOT** run reports the newest full
manifest's `built_at` **before** the boundary (also bounded, at most 12 further GETs) --
`NO (last full: <that built_at>)`, never a silent default.

## 4. THE EXERCISE -- both readings, post-commit

**Live** (`bash .tools/comp-graph status`):
```
  projection.last_night YES          present            no-TTL    REFRESHED LAST NIGHT: YES at 2026-09-04T02:22:43.290435+00:00
                       evaluated: boundary 2026-09-04T02:00:00+00:00 (+6h window); checked 1 manifest(s)
```
The pointer's own current vintage is an *incremental* stamp (`writer_id: incremental_updater`,
05:53:37Z), but the last-night check correctly finds the *full* derive-runner manifest at
`02:09:19.993324+00:00` inside the window and reports its `built_at` -- one manifest GET, bounded.

**Planted** (`COMP_GRAPH_POINTER_URI=.../deliverables/0.9.0_WK_NFRA_CLDGRPH~3/plant/current.json bash .tools/comp-graph status`):
```
  projection.last_night NO           present            no-TTL    REFRESHED LAST NIGHT: NO (last full: 2026-09-02T20:15:00.000000+00:00)
                       evaluated: boundary 2026-09-04T02:00:00+00:00 (+6h window); checked 1 manifest(s)
```
The plant is a local fixture (`plant/current.json` + `plant/2026-09-02T20_00_00.000000+00_00/_build_manifest.json`
-- Windows forbids `:` in a path component, so the local-fixture layout escapes `:` -> `_` in the
vintage directory name only; this never touches an S3 key, which allows `:` natively) whose only
published vintage is a `full`/`derive_runner` manifest at `2026-09-02T20:00:00`, ~35h before the
current boundary and outside every future boundary's window too (the plant date only recedes
further into the past as wall-clock time advances). The two readings differ exactly on the
`last_night` line, as R4 requires.

The wrong artifacts are gone (`kuzu_db`/`stitch_graph` no longer appear anywhere in the cloud
group; measured `grep -c` = 0).

## 5. THE BATTERY

`.tools/tests/test_cg7_status_read_battery.py`, direct AND pytest grain, denominator 7:

```
[PASS] ARM-I-LIVE-SHAPED-YES
[PASS] ARM-II-PLANT-NO
[PASS] ARM-II-RED-MUTANT-EMPTY-WINDOW-YES
[PASS] ARM-III-UNREADABLE-POINTER-UNVERIFIABLE
[PASS] ARM-III-RED-MUTANT-SILENT-NO
[PASS] ARM-IV-JSON-REFRESHED-LAST-NIGHT-AND-VINTAGE
[PASS] ARM-V-R4-CENSUS-NO-ALARM-SNS-SCHEDULE (0/707 source line(s) scanned)
CG7-STATUS-READ BATTERY: 7/7 PASS (denominator 7)
```

`python -m pytest .tools/tests/test_cg7_status_read_battery.py -q`: `1 passed`.

Two RED mutants (arms ii and iii) each prove the discriminator: (ii) forcing every listed vintage
into the nightly window makes the plant's empty-window truth wrongly read `YES` -- exactly the
class of bug the TO names ("a reader that prints YES when the window is empty"); (iii) breaking
the unreachable-pointer message so it silently claims `NO` instead of `UNVERIFIABLE` -- proving
the "never a default" invariant is load-bearing, not decorative.

## 6. BOUNDS HELD

Pull-read only: no S3 write, no engine call, no rebuild, no cache file created. No alarm, SNS,
CloudWatch metric, EventBridge or schedule call anywhere in the engine (arm v census, 0/707 lines).
`bash .tools/commit-gate.sh` clean on both touched `.py` files.
