# NFRA_GLOBGRPH S3 — heat-analytics FEDERATION + canonical layer taxonomy (design for the CTO/CVO arch-gate)

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26 | **Andrew-direct** (the federation + both-repos scope is his call)
**Gate:** CTO arch-gate (schema/lens decision — node classification + the COND-A baseline + the analytics surface). RAVC → [1.0.0_SA_CTO]; CVO [3.0.0_SA_CVO] owns the layer-taxonomy at sign-off; CC [2.0.0_SA_COO] + [0.7.0_AE_CloudOps] (clusters/portal lane).
**Scope:** DESIGN ONLY (design→gate→build, the GATE-0 pattern). No build until arch-gated. Two coupled decisions: (A) the canonical `node_type → layer` taxonomy; (B) the heat layer is a CROSS-SOURCE FEDERATION (Iceberg assets + git code-heat), with **git NOT materialized into Iceberg**.

---

## 0. The core principle (Andrew, 2026-06-26)

> Heat/cold clustering is a **domain-agnostic analytic** — it shouldn't only sit on top of *physical/served assets* (AWS resources, MS files, portal components in Iceberg). It must also cover **code** (git). And **git does NOT belong in Iceberg** — git already has great versioning (commit DAG, timestamps, authorship, blame, rename tracking); materializing it would be redundant + lossy. Query git directly; materialize nothing.

So the heat layer is **Trino-federated**: Iceberg (the materialized graph) ⋈ git (queried live). Trino was chosen precisely because it is a *federator* — this is its sweet spot, not a single-source query over Iceberg.

## FINAL MODEL (Andrew-direct 2026-06-26, post-sign-off — supersedes the 5-layer below)

Andrew (sovereign) simplified the taxonomy after the CTO/CVO sign-off to the **3 layers that map to the 3 real SOURCES** and have real content — and dropped the noise:
- **`aws`** = cloud infrastructure (the 28 resource types — UNCHANGED, so CVO's frozen COND-A baseline is intact). **`portal`** = the frontend app (the 15 component/code types; `dash` renamed → `portal`). **`ms`** = the SharePoint/OneDrive estate.
- **DROPPED `external`** — it was just `EXTERNAL_ENDPOINT` (3 nodes: andrew@opalinvest.com + 2 phones, the email/SMS destinations SNS alarms notify — operational alert plumbing + contact-PII, not estate). The node + its `SUBSCRIBES` edges are removed; the `SNS_TOPIC` resources stay in `aws`.
- **DROPPED `pipeline`** — `GOLD_SCRIPT`/`S3_DATA_KEY` were 0 nodes (empty placeholder) and conceptually muddy (S3=aws, scripts=code). Re-introduce only when the data pipeline is actually graphed, gated by the fail-loud completeness cert.

**COND-A unaffected:** the `aws` layer is still exactly the 28 CVO-certified resource types (SNS_TOPIC included), so the per-class frozen baseline CVO signed (58a7d26d1) is preserved. Implemented in `derive_runner` (`NODE_TYPE_LAYER` 3-layer map + `DROP_NODE_TYPES={EXTERNAL_ENDPOINT}` drop-pass + the fail-loud cert). The 5-layer text below is the as-gated record; this note is the shipped model.

## 1. Decision A — canonical `node_type → layer` taxonomy

Today every node without an explicit `layer` defaults to `'aws'` (`derive_runner.py:324`), so portal-code + clusters get mislabeled `aws` (the exact thing that made COND-A read alarming). The fix is an explicit, canonical partition:

| layer | node_types | source-of-truth | drifts? |
|---|---|---|---|
| **aws** | S3_BUCKET, LAMBDA, IAM_ROLE/POLICY, DYNAMODB_TABLE, EC2_INSTANCE, EVENT_RULE/SOURCE, SECRET, CW_ALARM, LOG_GROUP, SECURITY_GROUP, SERVICE_PRINCIPAL, INSTANCE_PROFILE | live AWS (comp-aws) | no — **frozen COND-A baseline** |
| **dash** (portal) | ReactComponent, JSXElement, JSXRender, Field, TypeDecl, Module, Prop, Hook, Component, DataFetch, ReactQueryKey, PanelCluster, Page, ServedURL, Endpoint | the **portal repo** | yes — tracks live portal |
| **pipeline** | GOLD_SCRIPT, S3_DATA_KEY | the **ajb_workspace repo** (gold/silver/bronze) | per deploy |
| **ms** | MS_SITE, MS_LIBRARY, MS_FOLDER, MS_FILE, MS_DRIVE_ONEDRIVE, MS_USER, MS_GROUP | M365 (the gateway) | additive (the new estate) |

Implementation: a single centralized `NODE_TYPE_LAYER` map + a post-fold relabel pass (so `ingest_ts_semantic_producer` + the cluster producer stop defaulting to `aws`). Folds 0.7.0's `db4d40246` (clusters→portal). **Naming:** the portal/dashboard layer is canonically **`dash`** (Andrew's term); `extract_portal_stitch`'s existing `'portal'` value is aliased/migrated to `dash` so there is ONE name. Result: `aws` = pure resources (the frozen baseline COND-A actually wants), and every summary view groups by `(layer, node_type)` — the natural analytics shape.

### 1.1 — the COMPLETE canonical `NODE_TYPE_LAYER` map (CVO Condition 1, d43b49e61)

Diffed against the LIVE 49-node_type census (comp-kuzu snapshot 3929343047371898635). Enumerating EVERY observed type — an incomplete map would silently drop ~108 real resources (incl `API_ROUTE`=77, which is IN the COND-A aws-resource baseline CVO signed 58a7d26d1) out of `aws` when default-to-aws dies → break the next COND-A. Complete map:

**`aws` (28 resource types — the FROZEN COND-A baseline, pure AWS resources):**
`API_GW`, `API_ROUTE`, `CLOUDFRONT_DISTRIBUTION`, `CW_ALARM`, `DYNAMODB_TABLE`, `EC2_INSTANCE`, `ECS_CLUSTER`, `ECS_TASK_DEFINITION`, `EVENT_RULE`, `EVENT_SOURCE`, `IAM_POLICY`, `IAM_ROLE`, `IAM_USER`, `INSTANCE_PROFILE`, `KMS_KEY`, `LAMBDA`, `LOAD_BALANCER`, `LOG_GROUP`, `ROUTE53_RECORD`, `S3_BUCKET`, `S3_BUCKET_POLICY`, `SECRET`, `SECURITY_GROUP`, `SERVICE_PRINCIPAL`, `SNS_TOPIC`, `SQS_QUEUE`, `STATE_MACHINE`, `VPC_ENDPOINT`

**`dash` (15 portal-code/component/cluster types — live-portal-tracking):**
`Component`, `DataFetch`, `Endpoint`, `Field`, `Hook`, `JSXElement`, `JSXRender`, `Module`, `Page`, `PanelCluster`, `Prop`, `ReactComponent`, `ReactQueryKey`, `ServedURL`, `TypeDecl`

**`ms` (the SharePoint/OneDrive estate — incl. schema types at 0 today):**
`MS_SITE`, `MS_LIBRARY`, `MS_FOLDER`, `MS_FILE`, `MS_USER`, `MS_DRIVE_ONEDRIVE`, `MS_GROUP`

**`pipeline` (gold/data — in map, 0 observed in this snapshot):** `GOLD_SCRIPT`, `S3_DATA_KEY`

**`external` (non-AWS endpoints — CVO's "decide + MAP it"):** `EXTERNAL_ENDPOINT` (3). Proposed a distinct `external` class so the `aws` baseline stays pure AWS-resources (an external endpoint is not an AWS resource). Flag for sign-off: `external` vs fold-into-`aws`.

**Serving-types boundary (the one nuanced call — flag for sign-off):** `API_ROUTE`→`aws` (it's the API-Gateway route resource; CVO counted 77 in the signed COND-A baseline), while `Endpoint`/`ServedURL`→`dash` (portal-code/served constructs). Confirm this aws-vs-dash split for the three serving types.

### 1.2 — FAIL-LOUD map-completeness assertion (CVO Condition 2, BLOCKER)

The relabel MUST NOT replace silent-default-to-`aws` with silent-default-to-`UNCATEGORIZED` (that would silently drop a FUTURE new node_type out of the frozen baseline). Required:
1. An unmapped node_type → `layer='UNCATEGORIZED'` LOUD (a `WARN:` line per type), never a silent assignment.
2. A **map-completeness assertion in the relabel/derive**: `assert set(observed_node_types) <= set(NODE_TYPE_LAYER)` — every OBSERVED type must be in the map, else **FAIL the derive (raise)**, exactly like the SS4 / UNCATEGORIZED cert. This is what makes the frozen-`aws` baseline DURABLE: a new AWS resource type next month FAILS LOUD (forcing a map update) instead of silently falling out of the COND-A count. Provenance discipline carried to the taxonomy.

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

## 3.5 — SUMMARY GRAIN: heat/cluster views aggregate at STRUCTURAL UNITS, not AST detail (Andrew-direct 2026-06-26)

The portal layer is a fine-grained AST/semantic parse of 374 real `portal/src` files (sources verified clean: 0 node_modules/test/dist/generated). Of its 11,338 nodes, ~86% (9,773) are ultra-fine AST detail (`Field`, `JSXElement`, `JSXRender`, `TypeDecl`, `Prop`) — accurate, but the *guts* of components, not units you heat/cluster on. So: **KEEP every node in the graph (it's the semantic-clustering producer's raw material), but the heat/cluster SUMMARY views + Trino aggregate at the STRUCTURAL UNITS; the AST detail is drill-down, never a top-level summary unit.**

Canonical `SUMMARY_NODE_TYPES` (the structural grain per layer — what comp-heat/the summary views cluster on):
- **portal** (1,565 structural of 11,338): `PanelCluster` (panels), `Page`, `ReactComponent`, `Component`, `Module` (files), `Hook`, `Endpoint`, `DataFetch`, `ServedURL`, `ReactQueryKey`. **Drill-down (NOT summary):** `Field`, `JSXElement`, `JSXRender`, `TypeDecl`, `Prop`.
- **aws** (all 28 resource types are meaningful units — no drill-down split).
- **ms**: `MS_SITE`, `MS_LIBRARY`, `MS_FOLDER`, `MS_FILE`, `MS_USER` (all meaningful; summarize at folder/file).

So a portal heat summary shows ~440 components / 374 files / 91 panels / 15 pages — not 4,969 fields. The fine AST stays queryable (a component's heat can drill into its fields), but it never inflates the summary. This is a VIEW/lens decision (the graph is unchanged) — it lands in the heat-layer build (the comp-heat/Trino summary queries filter to `SUMMARY_NODE_TYPES`), no re-derive.

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

---

## 8. AC — EVERY FEDERATED CATALOG EMITS A CHECKABLE PARITY SIGNAL (CTO design-in 20260629T190400Z, NFRA_COMPDRIFT seam-6/7)

**Status:** ACCEPTED as a first-class AC on the federation build (pre-materialization design-in — the one-time window; a retrofit would land seam-6/7 as GAPs in the NFRA_COMPDRIFT topology manifest). CTO (1.0.0_SA_CTO) will formalize the exact signal *contract*; this AC binds the build to EMIT a consumable signal per federated catalog so the comp-drift Trino engine's per-catalog sweep has something to read. The signal need not be the full checker — just the emitted signal.

This maps cleanly onto the two catalog FAMILIES already in §4 (it does not change the model — it makes each binding parity-checkable by design):

| federated catalog family | backing | parity signal it MUST emit | drift it makes CHECKABLE |
|---|---|---|---|
| **Iceberg-backed** (`graph_nodes`, `node_health`, and any future aws/portal/ms/pipeline materialized table bound into Trino via the Nessie/Iceberg catalog) | Iceberg table (Nessie-versioned) | an **expected schema fingerprint** — a stable hash over the table's `(column_name, type, partition-spec)` derivable both from (a) Trino's bound catalog def and (b) the live Iceberg table — so a drift check can compare BOUND-vs-LIVE | an Iceberg re-partition / schema-evolution that Trino keeps serving against a STALE catalog def (the `comp-transform schema-check` MISSING failure mode, generalized to every federated catalog) |
| **git-native code-heat** (the live-read `object_freshness` view per repo — ajb_workspace + portal — §4, NEVER materialized) | git, queried live | a **HEAD-pointer / vintage marker** — the commit SHA(s) + `computed_at` the live-read reflects, PER repo (`{repo, head_sha, computed_at}`) | a live-read silently reflecting a stale checkout / a refresh that didn't re-run — vintage is queryable, not invisible. This is a SPECIAL CASE: a HEAD marker, NOT a table-schema check (git has no materialized schema to fingerprint) |

**Build obligations (fold into the federation build, NOT a fast-follow):**
1. **Per Iceberg catalog binding** — emit/derive a schema fingerprint at bind time (and on the nightly refresh) into a queryable spot the comp-drift sweep can read (candidate: a `catalog_parity` column-set on `graph_metrics` or a sidecar `trino_catalog_fingerprints` table — confirm against CTO's signal contract). The `node_health` Iceberg table already has a fixed, asserted schema (`node_health.py`) + the `assert_certified_graph_unchanged` invariant — the fingerprint is a cheap projection of that, not new machinery.
2. **Per git code-heat catalog** — the per-repo code-heat view/parlet (§4 / open-Q2) MUST carry `{repo, head_sha, computed_at}` as columns on the row set (NOT just metadata) so Trino can SELECT the vintage. This folds my prior next-step "git-HEAD-sha provenance (computed_at + git-HEAD-sha)" directly into the parity contract.
3. **No federated catalog binds WITHOUT a parity signal** — make this a build gate: a catalog with no emitted fingerprint/HEAD-marker is an incomplete binding (fail-loud, mirroring the COND-2 map-completeness cert). This is what guarantees seam-6/7 land COVERED, not as retrofit GAPs.

**Coordination:** loop 1.0.0_SA_CTO on the catalog-binding design before materialization; CTO threads the exact signal contract + arch-gates the Trino fan-in model (one node, N inbound catalog seams). cc MSTR + COO + CVO.
