# NFRA_MSGRAPH RE-SCOPE — estate-wide heat + an analytics layer (Iceberg/Trino) + pseudo-RAG; re-target to /sites/Shared

**Author:** 0.8.0_AE_CloudComp (NFRA_GLOBGRPH owner) | **Date:** 2026-06-26
**Routing (Andrew-direct):** → **3.0.0_SA_CVO review** → **1.0.0_SA_CTO arch-gate**. CC 2.0.0_SA_COO (project owner; this changes the S3/S5 scope they are decomposing).
**Trigger:** Andrew-direct architecture refinement (working session 2026-06-26, post-S2-deploy). Two sovereign moves: (1) the real target is the **Opal collaborative drive**, not Andrew's personal OneDrive; (2) **the heat-map logic must apply to AWS resources too**, so heat + the index belong at a shared analytics layer over the graph, not as an MS side-car.
**Status:** PROPOSAL for review. Grounded against LIVE recon (Rule 22 — citations inline). Supersedes the relevant parts of `NFRA_MSGRAPH_PRD.md` §3.3 (cadence), §4 (heat-map MS-scoping), §5 (comp-tools), §6 (S3/S5 phasing); CTO folds accepted parts into the PRD.

---

## 0. TL;DR of the changes

| # | Change | From (current PRD / S2-deployed) | To (this re-scope) |
|---|---|---|---|
| 1 | **Ingestion target** | `/me/drive` (Andrew's PERSONAL OneDrive) + SP default libraries | **`/sites/Shared` "Shared Documents"** (the team's collaborative library) |
| 2 | **Update cadence** | nightly-full + `/delta` hourly (S5-gated) | **hourly FULL poll over existing `/ms/*`** — `/delta` DROPPED (unneeded at this scale) |
| 3 | **Heat scope** | MS-only heat-map (S3) | **estate-wide, domain-agnostic heat** over `graph_nodes` (AWS resources + MS docs) |
| 4 | **Index/RAG home** | "MS-specific comp-tools" (bolt-on) | **materialized Iceberg tables** (heat_index / clusters / rag_index), Nessie-versioned |
| 5 | **Analytics compute** | (implicit: in the derive) | **staged: pyiceberg (HEATMAP_OBJECT, now) → Trino/Athena SQL layer (interactive + RAG ranking)** |
| 6 | **Query surfaces** | Kuzu only | **Kuzu (traversal) + Trino/SQL (analytics + pseudo-RAG)** over the one Iceberg/Nessie estate |

The catastrophic-floor guardrail is UNCHANGED: structure/metadata/activity only, never content; the pseudo-RAG is metadata/heat retrieval, **not** content-embedding (that would be a separate, explicitly-gated decision — see §6).

---

## 1. Grounded recon — the real target (Rule 22)

The S1/S2 recon was pointed at the wrong drive. `list_onedrive` → `/me/drive` is Andrew's **personal** OneDrive (his Desktop, the `ajb_workspace` repo mirror, Schwab data) — not the collaborative estate. Andrew clarified: **Opal works collectively in a shared "OneDrive-as-SharePoint" space.** Decoded from the URL he provided, that is:

- **Site:** `opalinvest.sharepoint.com/sites/Shared` (siteId `...,9332c03f-2ad0-4b84-97fe-7bcd2c9cb90a,...`; last modified 2026-06-25 — active).
- **Library:** "Shared Documents" — the site's **default** library, so the existing gateway `list_site_files` reaches it directly (no `/sites/{id}/drives` multi-library extension needed for THIS target; that gap remains relevant only if other shared libraries appear later).
- Reachability fix was trivial: it's a site I'd simply never name-searched ("Shared" wasn't a probe term).

**Live enumeration (depth-6 crawl, this session):**
- **~4,560 file-object nodes** — 82 top-level items (69 folders + 13 loose files).
- **Document-dominated:** `.pdf` 1,331 · `.xlsx` 1,015 · `.docx` 519 · `.pptx` 244 (= ~3,100 genuine documents, ~68%). Tail: `.csv`/`.pkl` data (165), images (52), `.mp4` (9), `.exe`/`.zip` (14 — installers/archives in `Software`/`Systematic Equity`).
- **Strong structure** — organized by business function. Natural top-level cluster taxonomy (~8 clusters; counts are recursive node estimates):

| Cluster | Representative folders | ~nodes |
|---|---|---|
| Investment Research | Research(1006), ETF(858), Alternatives(200), Div Research(56), Screens, Fund Comps, Sellside, Macro, Viewpoints, Morningstar | ~2,180 |
| Marketing & Presentations | Presentations(304), Market Update(128), Marketing(82), Website(57), PFDE, Brand, Charts | ~660 |
| Models & Portfolios | OCIO Models(259), SMA Model Weights(56), ETF Models(47), Holdings, Covered Call, Polen, SMArtX | ~430 |
| People & HR | Recruiting(250), Adam(80), Hiring, Firmwide Meeting, Training, One-on-One | ~350 |
| Compliance & Governance | GIPs(197), Investment Committee(30), Opal Due Diligence(30), Compliance Manual(16), DDQ, IMAs | ~290 |
| Asset Management | Asset Management(274) | ~274 |
| Operations · Trading · Tax | TAX(101), Dashboard(59), Billing(33), Trading&Ops, Orion, SmartX-Trading | ~250 |
| Partners & Distribution | Alongside(105), 49F Comm(34), 49F Custom(26), Opportunities(13), GFCA, Ausdal, LPL, Cottonwood, Envestnet | ~250 |
| Non-document bulk (flag, don't index as docs) | Software(16/3GB,.exe), Systematic Equity(3/2.4GB,data), .pkl/.zip | ~20 |

**Implications the real numbers settle:**
- **~4,560 nodes is small** → keep **file-object granularity for everything**; no need to roll cold subtrees up to folder-level. (Size ≠ count: the 3 GB `Marketing` / 2.4 GB `Systematic Equity` folders are *few* nodes.)
- The only cleanup is to **flag (not exclude) non-document bulk** (`is_document=false` on `.exe`/data/`.zip`) so the RAG down-ranks it.

---

## 2. Re-target (change #1) + cadence (change #2)

- **Re-target ingestion** to `/sites/Shared` "Shared Documents": drop the `/me/drive` personal crawl entirely; add the `Shared` site as the primary target (it routes through the existing `list_site_files` path — already supported; only the site selection changes). The 6 near-empty `opal`-named SP sites are keep-or-ignore (trivial).
- **Hourly FULL poll** over the existing read-only `/ms/*` endpoints: at ~4,560 nodes a full re-enumerate is ~a few-hundred folder-list calls, ~1-2 min, free (delegated token, within throttling). **`/delta` is DROPPED** — the only reason for delta is to fetch *only* changed items, which at this scale is more bookkeeping than a full re-pull is worth. (Re-add only if the estate grows 10-100×.) **No Microsoft push / subscriptions / new APIs** (Andrew-direct: not paying MS for pushes). This collapses the old S5 to just `/permissions` (access edges) + optional `/insights` (read-heat) — neither is about updates.

---

## 3. Estate-wide heat (change #3) — the core architectural move

Heat is `f(last_activity_timestamp)` and **every node has one**, so heat must NOT be MS-specific. Generalize it to a **domain-agnostic analytics over `graph_nodes`**, run over BOTH layers:

- **MS:** `lastModifiedDateTime` (write-heat) — already day-one.
- **AWS:** per-class last-activity — Lambda last-invoked (CloudWatch) / last code-update; S3 last-object-write; IAM role last-used (IAM provides this); EC2 launch/last-state-change; DynamoDB last-write. (The activity-timestamp extraction per AWS class is the new work; the heat ENGINE is shared.)

The `HEATMAP_OBJECT` engine (build-complete, domain-parameterized) is pointed at `graph_nodes` and emits a **`heat_index` Iceberg table**: `(node_id, layer, last_activity_ts, heat_score, band[hot|warm|cold], cluster, snapshot_ts)` — for ALL nodes. `comp-heat <layer>` queries it; MS findability and AWS debt are two consumers of the one table.

**AWS payoff (why the generalization earns its keep):** estate-wide heat turns the AWS graph into a debt/cost engine — a cold Lambda (no invoke in 90d) + `LIVE-no-DECLARED` orphan + zero blast-radius = a high-confidence cleanup candidate; a cold S3 bucket = an archive/cost candidate. This is the NFRA_DEBTSCAN / NFRA_COSTAWS surface, powered by the same engine that ranks MS docs. One mechanism, two payoffs.

---

## 4. The analytics layer + query surfaces (changes #4, #5, #6)

One estate (Iceberg/Nessie), three surfaces:

```
   Iceberg graph_nodes/graph_edges  (layer='aws' 12,644 + layer='ms' ~4,560)   ← canonical, Nessie-versioned
        │                                   │
        ▼ (analytics)                       ▼ (traversal)
   ANALYTICS LAYER                     KUZU
   - heat scoring / clustering /       - MATCH paths, blast-radius,
     ranking / aggregation              "what connects to what"
   - materializes Iceberg tables:      - reads heat/cluster cols as
     heat_index · clusters · rag_index   node properties (heat-ranked traversal)
   - compute STAGED:
       (a) pyiceberg / HEATMAP_OBJECT  ── now (reuses built engine; cheapest)
       (b) TRINO / Athena SQL layer    ── interactive cross-domain analytics +
                                           the pseudo-RAG ranking served as SQL
        │
        ▼  comp-heat (any layer) · comp-ms-find (layer='ms' + clusters) · comp-debtscan (layer='aws' cold)
```

- **Store = Iceberg.** heat_index / clusters / rag_index are **materialized Iceberg tables** (canonical, Nessie-versioned, time-travel — "what was hot last quarter"). The index lives *inside* the estate, not a bolt-on RAG store.
- **Compute = staged.** (a) **pyiceberg / HEATMAP_OBJECT now** — proven path (the derive already uses pyiceberg/Nessie); produces the heat + cluster + index tables in batch. (b) **Trino / Athena later** for interactive, set-based analytics + the pseudo-RAG: retrieval is fundamentally a SQL ranking (`WHERE layer='ms' AND cluster=? AND is_document ORDER BY heat, recency`), far more natural in SQL than Cypher.
- **Traversal = Kuzu**, unchanged; reads the heat/cluster columns so path queries can be heat-ranked.

**FEASIBILITY ITEM for CVO/CTO (do not over-claim):** Trino's Iceberg connector supports the Iceberg REST catalog; Nessie exposes an Iceberg REST endpoint (the derive's `RestCatalog` already targets `{nessie}/iceberg/{branch}`), so a Trino layer should read the same tables. **Athena** uses the Glue catalog — Athena-over-Nessie needs either dual Glue registration or Athena's Iceberg-REST support; **confirm before committing to Athena specifically.** The pyiceberg compute path is proven; the Trino/Athena *query* layer is the item to validate.

---

## 5. Pseudo-RAG (the "side-car index, maybe inside Iceberg/Trino")

It is a **side-car index over the graph, materialized as Iceberg tables, queried via SQL (Trino) — not a separate system.** Shape:

- **Clusters** = the ~8 functional groups (§1), derived from the folder taxonomy; refinable with co-access edges (the `/permissions` S-item) + naming. The `CONTAINS` hierarchy IS a locality clustering.
- **Index lenses** (each a column/table the retriever ranks by): **hot/cold** (heat_index) · **cluster/function** · **type** (pdf/xlsx/docx/pptx = documents; data/exe down-weighted) · **recency** · **owner/access** (later).
- **`comp-ms-find`** = NL question → pick cluster + lens(es) → SQL ranking over rag_index → heat-ranked document results. (e.g. *"latest GIPS performance report"* → Compliance cluster → GIPs → type=pdf → hot-first.)

---

## 6. Guardrail confirmation (unchanged — for CVO's lens)

- **Never content.** The pseudo-RAG ranks on filename / folder-path / type / heat / recency / owner — **never document bodies**. The two fail-closed layers (gateway `/ms/*` read-only-by-construction + structure-only output allowlist; derive SS4 emit cert) are unchanged and now also apply to the hourly poll.
- **Content-embedding RAG would be a SEPARATE, explicitly-gated decision** (it crosses the never-content line, needs its own store + Andrew sign-off). NOT in this re-scope.
- **Additive-only** still holds: estate-wide heat reads `graph_nodes`, writes new index tables; it never mutates AWS or MS nodes. AWS-heat is additive analytics over the existing AWS graph.

---

## 7. For CVO review → CTO arch-gate

**CVO — independent verification asks:**
1. Ground-truth the recon: confirm `/sites/Shared` is the right target + the ~4,560-node / 8-cluster / document-dominated characterization (re-run the survey if desired; the script is in `S2_build/`).
2. Guardrail preservation: confirm the re-scope keeps never-content intact (metadata/heat RAG, not content-embedding) across the new hourly-poll + analytics paths.
3. Reuse claims: HEATMAP_OBJECT is build-complete + domain-parameterizable to AWS; pyiceberg compute is the proven path; the Trino/Athena query layer is correctly flagged as a feasibility item, not an assumption.
4. Additive-safety: estate-wide heat + index tables never perturb the certified AWS graph (the strict-superset discipline).

**CTO — arch-gate decisions:**
1. APPROVE the re-target (`/me/drive` → `/sites/Shared`) + hourly-full-poll + drop `/delta`.
2. APPROVE generalizing heat from MS-only (S3) to **estate-wide domain-agnostic analytics** over `graph_nodes` (this is the load-bearing re-scope; reframes S3 + couples to DEBTSCAN/COSTAWS).
3. RULE on the analytics-compute path: pyiceberg-now → Trino/Athena-later (and which — confirm the Nessie-REST-catalog feasibility for the chosen engine).
4. APPROVE the index/RAG as materialized Iceberg tables + the pseudo-RAG as a Trino SQL query (vs. a bolt-on store).
5. Fold the accepted changes into `NFRA_MSGRAPH_PRD.md` + re-issue the S3/S5 TO scope (COO).

**Current-state note:** S2 is deployed but pointed at `/me/drive`; tonight's 02:00 nightly will ingest the personal drive (bounded by the 5,000-node ceiling — harmless, additive) and still proves the L6 pipeline. The re-target lands as the first step after this review. No gateway change tonight (stability hold for the 02:00 proofs).
