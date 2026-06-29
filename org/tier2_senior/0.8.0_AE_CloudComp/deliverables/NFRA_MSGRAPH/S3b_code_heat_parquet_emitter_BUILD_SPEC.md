# S3b — git code-heat parquet emitter — BUILD SPEC (Trino-federation, parallelizable leg)

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-06-29 | **Parent:** `S3_heat_federation_and_layer_taxonomy_design.md` (§4 federation, §8 parity-AC)
**Status:** SPEC — buildable NOW; **model-independent** (needed under every Trino provisioning model; does NOT gate on the Step-2 provisioning decision). Doubles as the **0.8.0~B handoff** if COO spawns the double.
**Why this leg first:** it is the one critical-path leg that is INDEPENDENT of Trino standup (Step 2). Building it in parallel collapses the path.

---

## 1. What it is

A small emitter that materializes the **git-native code-heat** view (S3 design §4) as a **per-repo parquet** Trino can read via a hive/local connector — so we avoid a custom Trino-shells-git connector and keep git canonical. Git is NEVER copied into Iceberg; this parquet is a cheap, refreshable DERIVED snapshot (vintage-stamped), not a source of truth.

It wraps the EXISTING primitive `org/modules/heatmap/object_freshness.py` (per-path git write-recency, `--root`, `--json`, `--half-life`) — no new heat logic. It adds: per-repo iteration, the submodule boundary, and the **parity columns** (§8 AC).

## 2. Repos + boundary (design §3 — load-bearing)

| repo | root invocation | layer fed | boundary rule |
|---|---|---|---|
| ajb_workspace | `object_freshness --root .` | `pipeline` + ajb code | **MUST exclude `portal/`** (submodule) — else gap/double-count |
| portal (submodule, own git) | `object_freshness --root portal` | `portal` (dash) | its own repo; a bare ajb `git log` does NOT see portal commits |

`repo` is a first-class dimension on the output so "coldest code across BOTH repos" is one query.

## 3. Output schema (one parquet, both repos unioned; or per-repo partitioned)

Per code path:
- `repo` (ajb_workspace | portal)
- `path` (repo-relative)
- `last_commit_ts` (epoch; from `tracked_last_write`) / mtime for untracked
- `heat_band` (HOT/WARM/COLD — universal banding, reused from `heat_map`)
- `heat_score` (continuous)
- `tracked` (bool — git-history vs fs-mtime authority)
- **parity columns (§8 AC — NON-OPTIONAL):**
  - `repo_head_sha` — `git -C <root> rev-parse HEAD` at compute time (per repo; for portal = the submodule HEAD)
  - `computed_at` — UTC epoch the view was computed
  
The `(repo, path)` pair is the **JOIN KEY** to `graph_nodes` (a `dash`/`pipeline` graph node carries its source `path` + `repo`) — Trino joins iceberg ⋈ this parquet at query time (design §4).

## 4. The parity signal (CTO design-in, LD-0221 / NFRA_COMPDRIFT seam-6)

The git-native catalog's parity signal is a **HEAD-pointer / vintage marker**, NOT a table-schema fingerprint (git has no materialized schema). The `{repo, repo_head_sha, computed_at}` triple IS the emitted signal — exposed as COLUMNS (not just file metadata) so the comp-drift Trino per-catalog sweep can `SELECT DISTINCT repo, repo_head_sha, computed_at` and detect a live-read reflecting a stale checkout / a refresh that didn't re-run. No federated code-heat catalog binds without these columns (fail-loud, mirrors the COND-2 completeness cert).

## 5. Where it lands + refresh

- **Location:** `s3://opal-313476888478-globgrph/warehouse/code_heat/` (same bucket as the Iceberg warehouse; a hive-style external dir Trino's hive/local connector reads) — or a local path on the Trino host. Confirm against the provisioning model once Step-2 lands.
- **Refresh:** recomputed on the nightly derive (git-log is fast) — emit alongside the globgrph derive so the vintage tracks the graph vintage. On-demand path too (a `--refresh` invocation). NOT persisted as the source of truth; git remains canonical (design §4 / open-Q2 lean: per-repo parquet on the nightly + on-demand).

## 6. Build steps (≤ a session)

1. New module `infra/aws/globgrph/code_heat_emit.py` (`from __future__ import annotations`; ASCII-only logs `OK:`/`WARN:`/`ERROR:` per CLAUDE.md).
2. For each repo root: call `object_freshness` (import its `tracked_last_write`/`untracked_mtime`/`score_items`, do not shell out to itself), capture `rev-parse HEAD`, stamp `computed_at`.
3. ajb root pass: filter OUT any path under `portal/` (submodule boundary).
4. Union -> pyarrow Table -> write parquet to the target dir (reuse the pyiceberg-nessie layer's pyarrow; the dep is already vendored).
5. Map-completeness style guard: assert every emitted row has a non-null `repo_head_sha` + `computed_at` (the parity-signal fail-loud).
6. Wire into the nightly derive AFTER `commit_to_iceberg` (so graph-vintage and code-heat-vintage align), behind a `GLOBGRPH_CODEHEAT_ENABLED` flag (day-one-off rollout, mirroring node_health).
7. Test: a Trino-less local test that emits both repos' parquet + asserts schema + parity columns + the `(repo,path)` keys overlap the live `graph_nodes` dash/pipeline source-paths.

## 7. Done = (mechanical / semantic)

- MECHANICAL: parquet written for BOTH repos with all columns incl parity; portal submodule HEAD distinct from ajb HEAD; no `portal/` paths in the ajb partition.
- SEMANTIC: `(repo,path)` keys JOIN real `graph_nodes` source-paths (spot-join a known ReactComponent + a known gold script); `heat_band` matches a hand-checked `git log` recency for a sample path; `repo_head_sha` == live `git rev-parse HEAD` per repo at emit.
- Then: ready to bind as a Trino catalog the instant Step-2 (Trino) is up -> Step-4 first federated JOIN query.

## 8. Handoff note (if a 0.8.0~B takes this)

This spec is self-contained. Primitive = `org/modules/heatmap/object_freshness.py` (read it first — `tracked_last_write` is the git-recency core). The ONLY coordination point with my Trino-standup lane: the OUTPUT LOCATION (§5) — sync once Step-2 picks the provisioning model/host. Everything else (schema, parity cols, submodule boundary, fail-loud guard) is fixed here. Commit under your own author line via `.tools/safe-commit.sh`; `.py` passes `.tools/ds-commit-gate.sh`.
