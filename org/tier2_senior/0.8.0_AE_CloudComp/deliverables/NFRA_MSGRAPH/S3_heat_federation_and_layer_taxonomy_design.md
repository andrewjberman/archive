# NFRA_GLOBGRPH S3 — heat-analytics FEDERATION + canonical layer taxonomy (design for the CTO/CVO arch-gate)

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26 | **Andrew-direct** (the federation + both-repos scope is his call)
**Gate:** CTO arch-gate (schema/lens decision — node classification + the COND-A baseline + the analytics surface). RAVC → [1.0.0_SA_CTO]; CVO [3.0.0_SA_CVO] owns the layer-taxonomy at sign-off; CC [2.0.0_SA_COO] + [0.7.0_AE_CloudOps] (clusters/portal lane).
**Scope:** DESIGN ONLY (design→gate→build, the GATE-0 pattern). No build until arch-gated. Two coupled decisions: (A) the canonical `node_type → layer` taxonomy; (B) the heat layer is a CROSS-SOURCE FEDERATION (Iceberg assets + git code-heat), with **git NOT materialized into Iceberg**.

---

## 0. The core principle (Andrew, 2026-06-26)

> Heat/cold clustering is a **domain-agnostic analytic** — it shouldn't only sit on top of *physical/served assets* (AWS resources, MS files, portal components in Iceberg). It must also cover **code** (git). And **git does NOT belong in Iceberg** — git already has great versioning (commit DAG, timestamps, authorship, blame, rename tracking); materializing it would be redundant + lossy. Query git directly; materialize nothing.

So the heat layer is **Trino-federated**: Iceberg (the materialized graph) ⋈ git (queried live). Trino was chosen precisely because it is a *federator* — this is its sweet spot, not a single-source query over Iceberg.

## 1. Decision A — canonical `node_type → layer` taxonomy

Today every node without an explicit `layer` defaults to `'aws'` (`derive_runner.py:324`), so portal-code + clusters get mislabeled `aws` (the exact thing that made COND-A read alarming). The fix is an explicit, canonical partition:

| layer | node_types | source-of-truth | drifts? |
|---|---|---|---|
| **aws** | S3_BUCKET, LAMBDA, IAM_ROLE/POLICY, DYNAMODB_TABLE, EC2_INSTANCE, EVENT_RULE/SOURCE, SECRET, CW_ALARM, LOG_GROUP, SECURITY_GROUP, SERVICE_PRINCIPAL, INSTANCE_PROFILE | live AWS (comp-aws) | no — **frozen COND-A baseline** |
| **dash** (portal) | ReactComponent, JSXElement, JSXRender, Field, TypeDecl, Module, Prop, Hook, Component, DataFetch, ReactQueryKey, PanelCluster, Page, ServedURL, Endpoint | the **portal repo** | yes — tracks live portal |
| **pipeline** | GOLD_SCRIPT, S3_DATA_KEY | the **ajb_workspace repo** (gold/silver/bronze) | per deploy |
| **ms** | MS_SITE, MS_LIBRARY, MS_FOLDER, MS_FILE, MS_DRIVE_ONEDRIVE, MS_USER, MS_GROUP | M365 (the gateway) | additive (the new estate) |

Implementation: a single centralized `NODE_TYPE_LAYER` map + a post-fold relabel pass (so `ingest_ts_semantic_producer` + the cluster producer stop defaulting to `aws`). Folds 0.7.0's `db4d40246` (clusters→portal). **Naming:** the portal/dashboard layer is canonically **`dash`** (Andrew's term); `extract_portal_stitch`'s existing `'portal'` value is aliased/migrated to `dash` so there is ONE name. Result: `aws` = pure resources (the frozen baseline COND-A actually wants), and every summary view groups by `(layer, node_type)` — the natural analytics shape.

## 2. Decision B — heat is a FEDERATION; the recency SOURCE is per-layer

`node_health.heat_band` is **universal** (HOT/WARM/COLD, the reused `heat_map` banding). But the *recency signal* feeding it comes from the layer-appropriate source:

| layer | heat recency source | how |
|---|---|---|
| **aws** | the resource's own `last_modified` / CloudTrail-ish activity | props `last_modified_dt` (Iceberg) |
| **ms** | the file/folder `lastModifiedDateTime` | props `last_modified_dt` (Iceberg) |
| **dash** (portal code) | **git — the portal repo** | `git log` per source-path last-commit → band (the existing `org/modules/heatmap/object_freshness.py` primitive) |
| **pipeline** (ajb code) | **git — the ajb_workspace repo** | same primitive, ajb_workspace root |

So a `ReactComponent` node gets hot/cold from the **portal repo's** git history; a `GOLD_SCRIPT` from **ajb_workspace's**; an `MS_FILE` from its modified-time. Same `heat_band` field, source-appropriate signal. **Git is never copied into Iceberg** — the code-heat is a derived view computed at query/refresh time (git-log is fast).

## 3. BOTH repos are first-class (Andrew-direct)

The git-code-heat federation spans **two distinct git repos**, each its own heat profile:

| repo | what lives there | git-heat root | layer it feeds |
|---|---|---|---|
| **ajb_workspace** | infra/aws, data pipelines (gold/silver/bronze), org/, comp-tools, the globgrph derive itself | repo root (`.`), **excluding the `portal/` submodule** | `pipeline` + ajb code |
| **portal** (a SUBMODULE — its own git repo, DEV/PROD) | the React/TS frontend (the `dash`-layer components) | `git -C portal` (inside the submodule) | `dash` |

**Submodule subtlety (load-bearing):** `portal/` is its own repo (CLAUDE.md — a bare `git log` at the ajb root does NOT see portal commits, and inside `portal/` only sees portal's). So the heat pass runs **per-repo**: `object_freshness --root .` for ajb_workspace (which must exclude the `portal/` submodule path to avoid a gap/double-count), and `object_freshness --root portal` for portal. **`repo` is a dimension** on the code-heat view (`{repo: ajb_workspace|portal, path, last_commit, heat_band, author_churn}`) so "coldest code across BOTH repos" is one federated query.

## 4. The federated shape (Trino)

```
          ┌─ Iceberg catalog (Nessie) ── graph_nodes ⋈ node_health   ← aws + ms + dash + pipeline ASSETS (materialized)
Trino ────┤
          ├─ git code-heat view: ajb_workspace   ── object_freshness(root=., excl portal/)   ← NOT materialized
          └─ git code-heat view: portal          ── object_freshness(root=portal)            ← NOT materialized
                         │
            unified heat lens (comp-heat / Trino SQL): hot/cold/DEAD across physical assets AND code,
            each node from its native source. graph code-nodes JOIN their git-heat by source-path;
            non-graph files surface in the standalone per-repo code-heat view ("dead code" = a query, not a crawl).
```

- **Join key:** a `dash`/`pipeline` graph node carries its source `path` (+ repo); the code-heat view keys on `(repo, path)`. Trino joins them at query time — no materialization of git.
- **Standalone code-heat:** the per-repo view stands alone too, so cold/dead code that ISN'T a graph node (a util never imported, a stale script) is still surfaced — across both repos.
- **Refresh:** the code-heat view is recomputed cheaply on demand (git-log is fast); optionally snapshotted per derive into `graph_metrics` for the burn-down time-series (a derived snapshot, NOT the source of truth — git remains canonical).

## 5. Beyond recency — code-specific risk signals (phase-2, flagged)

Git carries signals an asset's mtime can't. The code-heat view can extend past pure recency (Andrew's prompt):
- **author-churn / blame-concentration** — a file many authors thrash, or one only its original author understands (bus-factor 1), is a risk hotspot independent of recency. From `git log --format` + `git blame` aggregates.
- **hot-but-fragile** — high write-frequency on a node feeding many SEV1 surfaces (cross with the graph's betweenness) = concentration risk.
These are dimensions on the same code-heat view; recency (heat_band) ships first, churn/blame as a fast follow-on. Still git-native, still not in Iceberg.

## 6. COND-A / additive-safety implications (CVO)

- The taxonomy makes `aws` = **pure AWS resources** = the genuinely-frozen COND-A baseline (no more portal-drift / cluster-accounting muddying the count — the issue CVO adjudicated tonight). COND-A becomes a clean per-class AWS-resource subset check, permanently.
- The git federation is **read-only + materialization-free** — it cannot mutate the certified graph (git is queried, never written to Iceberg). Additive-safety is structural: the code-heat is a query-time JOIN, not a derive write.

## 7. Open questions for the arch-gate

1. **`dash` vs `portal` naming** — adopt `dash` canonically (Andrew's term) and migrate `extract_portal_stitch`'s `'portal'`? (My lean: yes, one name.)
2. **Code-heat compute locus** — a Trino table-function/UDF shelling git, vs a lightweight per-repo parquet the heatmap emits (queried via Trino hive/local connector), vs an on-demand view. (My lean: a cheap per-repo parquet refreshed on the nightly + an on-demand path — avoids a custom Trino connector, keeps git canonical.)
3. **ajb_workspace ⟂ portal-submodule boundary** — confirm the ajb root pass excludes `portal/` (no double-count) and portal is its own pass.
4. **Where node_health stores code-heat** — code-layer nodes get `heat_band`/`cold_since` like asset nodes (same record), just sourced from git; confirm the record stays one shape across all four layers.

**Net:** the heat/analytics layer becomes a Trino federation — Iceberg-materialized assets (aws/ms/dash/pipeline) ⋈ git-native code-heat (ajb_workspace + portal, never materialized) — under one universal `heat_band` whose recency source is layer-appropriate. Git keeps its own versioning; Iceberg keeps the assets; Trino joins them. RAVC → CTO arch-gate; CVO owns the taxonomy sign-off.
