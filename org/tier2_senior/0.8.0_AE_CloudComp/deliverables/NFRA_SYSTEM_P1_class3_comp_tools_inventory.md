# NFRA_SYSTEM P1 class-3 inventory + NFRA_TOOLCHECK P1 verification matrix: COMP-TOOLS + COMP-WHICH + COMPRAIL

**Author:** 0.8.0_AE_CloudComp~D | **Date:** 2026-07-08 | **TOs:** NFRA_SYSTEM.P1.audit-investigation.md (req 3) + NFRA_TOOLCHECK.P1.functional-verification.md (req 1-5)
**Dual-purpose (COO SYNERGY, CTO flag):** the ONE shared comp-tool artifact both projects read -- Sections 1-9 = the SYSTEM class-3 MAP (what the tools ARE + interact); Section 10 = the TOOLCHECK HEALTH overlay (do they WORK -- WORKS/BROKEN/friction/gate-firing/retire, real-invocation + log-grounded). SYSTEM-P4 maturity consumes both.
**Discipline:** Rule-22 grounded, honest current-state. `built-proven` requires exercise/usage evidence; `built-unproven` = exists but no exercise evidence found; `forming` = partial/stub; `designed-only` = design/PRD, no working code. Consolidate-don't-duplicate: this is the synthesis + gap-list, the cited docs are the deep source.

## 0. Scope + authoritative counts (grounded)

The class-3 surface is the comp-tool CATALOG + the comp-which ROUTER + the COMPRAIL rail + the ~37 query tools + the meta/enforcement tools.

- **37** tools in `org/modules/graph/graph-call-manifest.yaml` `tools_index` (the per-tool instructional catalog).
- **56** tools in the SOURCE-OF-TRUTH ledger `org/modules/graph/comp-coverage-map.yaml` (union of `tools` + `meta_tools`).
- Grounding: `python org/modules/graph/comp_coverage_view.py --verify` -> `OK: all 37 manifest tools_index entries present in the ledger union (56 tools); regeneration is non-breaking` (exit 0, exercised 2026-07-08). The 37 (manifest) < 56 (ledger) delta = the meta/enforcement/harness tools + newer tools not yet projected into the manifest tools_index (see GAP list).

## 1. The catalog + router + rail (core class-3 spine -- grounded by live exercise)

| component | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| **graph-call-manifest.yaml** (the use-case -> canonical-call catalog) | `org/modules/graph/graph-call-manifest.yaml` (892 lines) | built-proven | comp_coverage_view.py (projection/drift gate); each tool's canonical call | `docs/architecture/NFRA_GRAPHS.md`; header STATUS v0.1 SCAFFOLD (CTO 2026-06-11) | file present, 37 tools_index entries; header line 8-10 status; comp-which reads it (comp-which:31) |
| **comp-coverage-map.yaml** (the SOURCE-OF-TRUTH ledger) | `org/modules/graph/comp-coverage-map.yaml` | built-proven | comp_coverage_view.py; comp-coverage-check gate | NFRA_COMPUNIFY (S1 CTO ruling #1: ledger is SoT, manifest tools_index is a PROJECTION) | `comp_coverage_view.py --verify` green; ledger union = 56 tools (exercised) |
| **comp-tools.yaml** (per-tool prose reference: when/cost/output-history) | `org/modules/graph/comp-tools.yaml` | built-proven | cross-links from the manifest tools_index | referenced in graph-call-manifest header line 842 | file present; per-tool blocks (comp-build/heat/drift/xray/parity/aws/kuzu/... enumerated) |
| **comp-which** (the NL -> canonical-call router; the catalog made queryable) | `.tools/comp-which` (932 lines) + engine `org/modules/graph/comp_route.py`, `comp_capability_provider.py`, `comp_which_signals.py`, `comp_potion_relevance.py`, `comp_route_affinity.py` | built-proven | graph-call-manifest.yaml + the ledger; comp-grep/glob (never-dead-end); OPAL_AGENT_SERIAL (role-passing) | `org/projects/NFRA_TOOLHUD.json`, `docs/architecture/NFRA_COMPRAIL_PRD.md` | EXERCISED: `comp-which "what produces canonical_prices.parquet"` -> routed a near-tie (comp-pipescript io / pipescript) via the COMPROUTE posterior; DR2 default-router flip live (CVO~B cert 4c1d93be5); Charter-1 POTION semantic-relevance E1 PASS (CVO~B 0fd19f02c) |
| **COMPROUTE router engine** (the posterior behind comp-which) | `org/modules/graph/comp_route.py` + `comp_capability_provider.py` + `comp_which_signals.py` + `comp_potion_relevance.py` | built-proven (default posterior + POTION semantic relevance are LIVE) | the capability ledger; POTION embeddings | NFRA_COMPROUTE (in NFRA_COMPRAIL family) | comp-which:692 `_default_router` DR2 flip; :659 `_shape_b_relevance_route` Charter-1 (POTION + Shape-B preserve, fail-safe -> lexical) |
| **COMPROUTE learned-affinity (w_h) term** | `org/modules/graph/comp_route_affinity.py` (`CachedAffinityProvider`) | **built-unproven-in-production** (WIRED but OFF by default; shadow/eval-only until the DRV affinity flip) | comp_route; the flywheel training queue | NFRA_COMPROUTE charter-2 | comp-which:573-593: `_LIVE_AFFINITY` default OFF; `--live-affinity`/`COMP_WHICH_LIVE_AFFINITY=1` enables; "LIVE comp-which decision stays affinity-COLD until the DRV FLIP" -- HONEST built-but-not-live-enabled |
| **COMPRAIL enforcement hook** (PreToolUse HUD nudge + gated raw-grep/aws deny) | `.tools/hooks/comp-tool-hud.sh` | built-proven | jq; the per-session freeform marker; comp-which patterns | `docs/architecture/NFRA_COMPRAIL_PRD.md`, `NFRA_COMPRAIL_HARDENING_BATCH.md`; TOs TO-2/3/4/5/6 | hook FIRING this session (HUD nudges observed on Glob/Bash); fail-safe exit-0; /freeform escape (line 42-52) |
| **COMPRAIL telemetry** (the rail log) | `org/mcp/comp-which-rail.log` | built-proven | comp-which `_log_rail` | NFRA_COMPRAIL.TO-5 (post-enforce telemetry) | 3,992 lines accumulating (exercised: `wc -l`); routes/RUN-GREP/ROUTE-SURFACE decisions logged |
| **comp-grep / comp-glob** (on-rails search primitives -- the never-dead-end) | `.tools/comp-grep`, `.tools/comp-glob` | built-proven | .gitignore + submodule awareness; the dependency-context overlay | NFRA_COMPRAIL_PRD (never-dead-end); CLAUDE.md Rule 21 | comp-which `_run_primitive` invokes them (comp-which:511); the sanctioned fallback when no rich tool fits |
| **comp-coverage-check** (the COMPUNIFY non-redundancy gate) | `.tools/comp-coverage-check` + `org/modules/graph/comp_coverage_view.py` | built-proven | the ledger; the manifest tools_index | NFRA_COMPUNIFY S2 | `comp_coverage_view.py --verify` green (exercised); asserts one-home + declared-overlap + tools_index projection current |
| **comp-manifest-check** (D6 graph-manifest enforcement gate) | `.tools/comp-manifest-check` | built-proven | graph-call-manifest.yaml; comp-diff | NFRA_GRAPHS D6 | CLAUDE.md Rule 20 gate; auto in safe-commit (excluded_not_graph_use_cases -- enforcement, not a query) |
| **comp-surface-check** (D8 critical-surface commit gate) | `.tools/comp-surface-check` + `org/modules/graph/surface_check_cli.py` | built-proven | critical-surfaces.yaml; comp-diff; comp_log_auto.py | NFRA_GRAPHS D8 / NFRA_GRAPHS.md §10 | EXERCISED this session (WARN on the promote_seam surface, R3); auto in safe-commit |
| **comp-to** (per-session TO_ID context setter for the auto-logger) | `.tools/comp-to` | built-proven | org/mcp/sessions/; comp_log_auto.py | CLAUDE.md compiler-tools-log convention | a startup/context primitive (excluded_not_graph_use_cases); writes the race-free per-session TO_ID |
| **comp auto-logger** (every comp call -> compiler-tools-log.md) | `org/modules/graph/comp_log_auto.py` | built-proven | comp-to (session TO_ID); org/compiler-tools-log.md | CLAUDE.md Rule 14 log convention | invoked by every comp wrapper tail (e.g. comp-surface-check:18) |
| **comp test/telemetry harness** (comp-learns-run/status, comp-perf, comp-v5-composite-test.sh) | `.tools/comp-learns-*`, `.tools/comp-perf`, `.tools/comp-v5-composite-test.sh` | built-unproven (harness; no in-session exercise -- flagged for the family agents / follow-up) | the comp-tool set | -- (excluded_not_graph_use_cases, line 28-33) | catalog explicitly excludes them as non-graph-query (self-learning/telemetry/regression harness); current-state not exercised this pass |

## 2. TRACE + PORTAL-FRONTEND family (comp-trace/blast/build/diff/xref/transform/cache/cluster/pii/types/adapter-audit/tooltip)

All 12 wrappers + engines present, all `status: canonical`, all with real usage rows in compiler-tools-log.md.

| tool | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| comp-trace | `.tools/comp-trace` -> `org/modules/graph/cli.py` (`trace`) over trace_graph.py + graph_cache.py; reads `.comp-graph/graph.json` | built-proven | trace-graph cache (built by comp-build), cli.py/trace_graph.py/graph_cache.py | NFRA_GRAPHS.md + ADHC_COMPIL.md | manifest `trace.walk.dependency_chain` canonical; 205 log rows |
| comp-blast | `.tools/comp-blast` -> `cli.py` (`blast`) | built-proven | trace-graph cache (fn-level caller/callee edges) | NFRA_GRAPHS.md, ADHC_COMPIL.md, COMPILER_BLAST_SCRIPT_ARTIFACT_EDGES.md | `trace.blast.what_breaks` canonical; 539 log rows (heaviest of family) |
| comp-build | `.tools/comp-build` -> `cli.py` (`build`) | built-proven | WRITE-PATH producer of graph.json; trace_graph.py extractors | NFRA_GRAPHS.md, ADHC_COMPIL.md | `trace.rebuild.refresh` canonical write_path; 132 log rows |
| comp-diff | `.tools/comp-diff` -> `cli.py` (`diff`) | built-proven | trace-graph rebuild + git (uncommitted/staged/--ref) | NFRA_GRAPHS.md, ADHC_COMPIL.md | `trace.diff.staged_blast` canonical; 9 log rows (thinnest exercise) |
| comp-xref | `.tools/comp-xref` -> `cli.py` (`xref`) | built-proven | trace-graph cache (symbol) / rebuild + saved baseline (drift) | NFRA_GRAPHS.md, ADHC_COMPIL.md (V4.014 dual-mode) | `trace.xref.symbol`+`trace.xref.graph_drift` canonical; 84 log rows |
| comp-transform | `.tools/comp-transform` -> `org/modules/graph/transform_cli.py` (+ extract_transforms.py) | built-proven | portal/src tsx + types.ts (live parse, no graph.json) | NFRA_GRAPHS.md, ADHC_COMPIL.md | `trace.transform.component_fields` canonical; 373 log rows |
| comp-cache | `.tools/comp-cache` -> `org/modules/graph/cache_cli.py` | built-proven | portal/src React-Query useQuery keys + response types (live parse) | NFRA_GRAPHS.md, ADHC_COMPIL.md | `trace.cache.key_collisions` canonical; 83 log rows |
| comp-cluster | `.tools/comp-cluster` -> **`infra/aws/globgrph/comp_cluster_cli.py`** (off-tree) | built-proven | LIVE canonical Kuzu graph + materialized cluster layer (NFRA_TSGRAPH P2); comp-kuzu | NFRA_TSGRAPH_PRD.md | `cloud.cluster.page_panel_drilldown` canonical; engine main() L224; 51 log rows |
| comp-pii | `.tools/comp-pii` -> `org/modules/graph/pii_cli.py` | built-proven | pseudonymizer.py target-field list, auth-edge role matrix, comp-transform, portal/src | NFRA_GRAPHS.md, ADHC_COMPIL.md | `trace.pii.exposure` canonical; 33 log rows |
| comp-types | `.tools/comp-types` -> `org/modules/graph/types_cli.py` | built-proven | portal/src regex grep + emitted types-index/<Type>.yaml | ADHC_COMPIL_V4.md, NFRA_GRAPHS.md | `trace.types.type_consumers` canonical; 63 log rows |
| comp-adapter-audit | `.tools/comp-adapter-audit` -> `org/modules/graph/adapter_audit_cli.py` | built-proven | **LIVE S3 fetch** (~60s) + portal adapter fns (served-envelope->component thread) | ADHC_COMPIL_V4.md, ADHC_VALGATE.md, NFRA_GRAPHS.md | `trace.adapter.field_threading` canonical; 26 log rows |
| comp-tooltip | `.tools/comp-tooltip` -> `org/modules/graph/tooltip_cli.py` | built-proven (narrow/likely-dormant) | portal/src tooltip-pattern scan vs <DataTooltip> | ADHC_COMPIL.md / V4.md | `meta.tooltip.migration`; comp-tools.yaml "one-off audit tool"; 13 log rows (lowest) |

**Notes/gaps (this family):**
- **NO in-module self-test in any of the 12 engines** (only `__main__`); built-proven rests on `status:canonical` + heavy log usage, NOT self-verification. Family regression lives out-of-module (comp-v5-composite-test.sh, comp-tool-health).
- **comp-cluster home outlier:** engine at infra/aws/globgrph/ (queries the Kuzu graph), off the org/modules/graph/ tree where every other trace engine lives.
- **comp-tooltip** self-described "one-off audit tool ... migration sprints only" + lowest usage (13) -> keep-dormant review candidate. **comp-diff** thinnest exercise (9 rows).
- **Directive lag:** comp-tools.yaml does NOT list comp-cluster (only manifest + coverage-map); comp-trace/blast/build/diff/xref carry no lifecycle-status field there -> the manifest is the status SSoT, the directive file lags.
- **Stale duplicate:** `worktrees/comp-learns-_stub/org/modules/graph/comp-tools.yaml` is a 2nd copy of the directive (drift/orphan).
- **Dependency asymmetry:** only comp-trace/blast/build/diff/xref share graph.json (build=producer); comp-transform/cache/pii/types/adapter-audit are LIVE rebuilds (adapter-audit hits live S3); comp-cluster reads live Kuzu -> a stale graph.json doesn't affect the latter six.

## 3. CLOUD / KUZU / IAM / ROUTES family (comp-kuzu/aws/iam/routes/lambdamap/secrets/dups)

| tool | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| comp-kuzu | `.tools/comp-kuzu` -> `infra/aws/globgrph/kuzu_cli.py` (loader `kuzu_load.py`) | built-proven | Kuzu local DB from Nessie/Iceberg (default `kuzu_nessie_db`); `kuzu` pkg; `_branch_head.main.json` HEAD-oracle marker | NFRA_GLOBGRPH_PRD.md, NFRA_GRAPHS.md | kuzu_cli.py `__main__` L110; manifest `cloud.lookup.*` canonical; 1551 comp-kuzu log rows |
| comp-aws | `.tools/comp-aws` -> `org/modules/graph/comp_aws_cli.py` (2655 L) | built-proven | live AWS boto3 + TF state reconcile; writes .comp-graph + snapshot tarballs to Nessie | NFRA_COMPAWS_SCHEMA.md; comp-aws-agent-usage.yaml | `__main__` L2654; `cloud.derive.refresh` canonical; 171 log rows |
| comp-iam | `.tools/comp-iam` -> `org/modules/graph/iam_cli.py` (416 L) | built-proven | live TF state + boto3-action code scan (no Kuzu) | COMPILER_IAM_LAMBDA_PARSER.md | `__main__` L415; `cloud.iam.permission_gaps` canonical; 452 log rows |
| comp-routes | `.tools/comp-routes` -> `org/modules/graph/routes_cli.py` (426 L) | built-proven | static parse of cloudfront/api-gw .tf + router .mjs + portal/src (no live AWS) | NFRA_COMPROUTE_PRD.md | `__main__` L425; `trace.routes.serving_path` canonical; 284 log rows |
| comp-lambdamap | `.tools/comp-lambdamap` -> `org/modules/graph/lambdamap_cli.py` (648 L) | built-proven | live Lambda CodeSha256 + S3 artifact meta + TF/dir (3-leg deploy parity) | COMPILER_IAM_LAMBDA_PARSER.md, ADHC_LAMBDADOC.md | `__main__` L647; `cloud.lambdamap.parity` canonical; 108 log rows |
| comp-secrets | self-contained `.tools/comp-secrets` (346 L, no separate module) | built-proven (CVO-owned) | live Secrets Manager boto3; Windows cert-store SSL fallback; git-grep consumer map | NO standalone PRD -- only manifest `cloud.secrets.inspect` + coverage-map + docstring | git cc2db4ef4 "live-tested: 76 secrets"; provisional->canonical 114921117 |
| comp-dups | `.tools/comp-dups` (runpy shim) -> `org/modules/graph/debtscan/dup_scan.py` (601 L) | built-proven (CVO-owned) | TF + first-party python bodies (BM25) + git; reads derived graph (never rebuilds); read-only | NFRA_DEBTSCAN_PRD.md | `__main__` L600, `--validate-dead` self-test L576; nightly ledger dups_latest.json (595KB, 2026-06-26); git 6af49d71c |

**Notes/gaps (this family):**
- **Auto-log ≠ exercise signal for the 2 CVO tools:** comp-secrets (standalone) + comp-dups (runpy shim) do NOT call comp_log_auto.py, so 0 log-rows is EXPECTED, not non-use -- grounded instead on the committed live-test (secrets, 76 secrets) + on-disk nightly ledger (dups). Both built-proven.
- Only comp-dups has a built-in fixture self-test (`--validate-dead`); comp-kuzu/aws/iam/routes/lambdamap rest built-proven on heavy documented log usage + canonical status (only `__main__`, no `--self-test`).
- Live-AWS tools NOT executed this pass (comp-aws/iam/lambdamap/secrets hit live AWS; comp-kuzu would trigger a Nessie-HEAD auto-refresh) -- grounded by file-presence + manifest status + log-counts.
- **comp-secrets doc thinness:** the one tool documented only via catalog + docstring (no numbered NFRA PRD) -- doc-coverage gap, not a defect.
- **comp-dups ledger staleness (minor):** dups_latest.json dated 2026-06-26 (~12d old as of 2026-07-08); engine/wrapper proven but the persisted ledger freshness lags if the nightly cadence is expected current.
- Engines split by design: comp-kuzu under infra/aws/globgrph/, the rest under org/modules/graph/ (comp-dups nested in debtscan/); all wrapper->engine links verified present, no dangling wrappers.

## 4. PIPELINE / PIPESCRIPT / VALIDATE family (comp-pipescript/pipescript/platinum/validate/freshness/chainrun/constants/incrparity/parity)

All nine built-proven (live engine + `__main__` + real exercise evidence: production log rows and/or a passing offline self-test).

| tool | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| comp-pipescript | `.tools/comp-pipescript` -> `org/modules/graph/pipeline_cli.py` (L3213) | built-proven | lib/s3_layout.py (AST) + gold_dispatch.sh chain/catalog + imports; safe_deploy_core.PIPELINE_MAP + live S3 (deployed); git | ADHC_COMPIL.md (+V4/V5), NFRA_GRAPHS.md | `trace.pipeline.gold_dag` canonical; **2,523** log rows (most-used comp-tool) |
| pipescript (AE-lane, DISTINCT) | `.tools/pipescript` -> `org/modules/graph/pipescript_cli.py` (L741) | built-proven | prebuilt estate-coverage-resolver.json (gen-estate-resolver.py); NO AWS | NFRA_PIPESCRIPT_PRD.md | EXERCISED: `pipescript_cli.py --validate` -> PASS exit 0 (offline); 492 log rows |
| comp-platinum | `.tools/comp-platinum` -> `org/modules/graph/platinum_cli.py` (L1031) + graph_cache.py | built-proven | chains comp-transform+routes+pipescript; per-firm .comp-graph/platinum.* cache; portal/src, CF/API-GW tf, gold DAG | NFRA_GRAPHS.md (D2 caching, LANDED) | `trace.fullstack.component_to_gold` canonical; 307 log rows |
| comp-validate | `.tools/comp-validate` -> `org/modules/graph/validate_cli.py` (L829) | built-proven | gold_validate_config.yaml (bd/inf/cot); local gold JSON/parquet (pyarrow) | COMP_VALIDATE_PROTOCOL.md | `pipeline.validate.artifact` canonical; 216 log rows (mandatory pre-S3 gate) |
| comp-freshness | **self-contained** `.tools/comp-freshness` (59.7KB python, NOT a graph-module wrapper) + freshness_manifest_gen.py | built-proven (NOT re-run -- live AWS) | live S3 + DynamoDB; gold_freshness_config.yaml + ddb_freshness_config.yaml; PyYAML; AWS creds | ADHC_COMPIL.md (Theme G) + V4 (DDB) | AC1-AC13 acceptance PASS (log:2067-2079; live 32-artifact BD chain 27.8s; caught RPS+aum staleness) |
| comp-chainrun | `.tools/comp-chainrun` -> `org/modules/graph/chainrun_cli.py` (`_selfcheck` L544) | built-proven | INF gold S3 (CHAIN_MANIFEST); live S3 for snapshot; `--from-dir`/`selfcheck` offline | ADHC_VALGATE.md §4.B | EXERCISED: `chainrun_cli.py selfcheck` -> ALL PASS exit 0 (12 checks incl synthetic DROPPED/COLUMNS-LOST) |
| comp-constants | `.tools/comp-constants` -> `org/modules/graph/comp_constants_cli.py` (L427) + seed yamls | built-proven | live code AST vs canonical seeds; `--lane bd/inf/cot/multifirm`; git | ADHC_COMPIL_V4.md (V4.003) | `pipeline.constants.drift` canonical; 22 log rows incl real drift finds (V4.021 ship) |
| comp-incrparity | `.tools/comp-incrparity` -> `org/modules/graph/incrparity_cli.py` (L155) + incrparity_core.py | built-proven | live S3 _parity (windowed cache vs oracle full-recompute); incremental promotion configs | INCREMENTAL_RUNS_DESIGN.md §5, INCREMENTAL_PARITY_STANDARD.md | `pipeline.incrparity.bd` canonical; 12 log rows (ALL/C_06/D_00 PASS) |
| comp-parity (DATA/served, DISTINCT from comp-lambdamap DEPLOY parity) | `.tools/comp-parity` -> `org/modules/graph/comp_parity_cli.py` (L312) | built-proven | firm parity-config 49f_parity_config.yaml; live S3 (canonical vs BD-served) | DATA_SSOTMG_PRD.md (TO-4) | `--help` exit 0 + logged live `49f\|PASS` streak (log:9562/10822/11086) |

**Notes/gaps (this family):**
- Strongest self-verified this pass: `comp-chainrun selfcheck` ALL PASS + `pipescript --validate` PASS (both offline, run live). comp-parity's data run evidenced by the logged multi-day `49f|PASS` streak (the DATA_SSOTMG cutover gate).
- **comp-freshness source outlier:** `.tools/comp-freshness` IS the full 59.7KB engine (self-contained, not a wrapper->graph-module). Built-proven on the logged AC1-AC13 live acceptance + 2 incidents it caught; not re-run (live AWS).
- **Name-collision confirmed (documented):** comp-pipescript (medallion gold-DAG, pipeline_cli.py, 2523 uses) vs pipescript (estate named-thread superset, pipescript_cli.py, 492 uses) are DISTINCT engines; comp-pipescript is one of pipescript's 134 sub-resolvers. pipescript owner = AE/cloud-ops (Andrew-direct 2026-06-23, manifest L348).
- Known in-registry caveats (real, not row-defects): `comp-pipescript chain --pipeline inf-gold` returns the BD chain (documented bug, comp-tools.yaml:253); comp-constants `--lane` was catalog-drift 2026-05-08 then shipped V4.021.

## 5. FRESHNESS / HEAT / DRIFT / XRAY / META family (comp-heat/xray/drift/graph/shell/registry/coverage)

All seven built-proven (backing engine on disk + logged runtime exercise).

| tool | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| comp-heat | `.tools/comp-heat` -> `org/modules/heatmap/heat_map.py` + object_freshness.py; `federated` -> `.tools/_trino_fed.py` | built-proven | git write-history (derived-on-demand, no persisted store); heatmap engine; `federated` adds LIVE Trino; READ-ONLY | NFRA_EXPAND_PRD.md (HEATMAP_OBJECT strand-C), NFRA_HEATMAP_SCOPING.md; brief 20260625 | log:8524/8526 "comp-heat BUILT+verified end-to-end" |
| comp-xray | `.tools/comp-xray` -> `infra/aws/compdiff/cli.py` over {engine,axes_s3,axes_git,axes_schema,freeze_monitor}.py | built-proven | S3 list_object_versions+get_object (VINTAGE-primary); git log; parquet footer; SNS (freeze-monitor --publish); READ-ONLY | NFRA_COMPDIFF_PRD.md | log:9634-9642 help/code/config/frozen/schema/freeze-monitor PASS+synthetic-FAIL (2026-06-30); pytest test_engine.py |
| comp-drift | `.tools/comp-drift` -> orchestrator `org/modules/graph/drift_cli.py` walking `drift-topology.yaml` | built-proven (orchestrator, does NOT re-implement) | drift-topology.yaml SSoT + SUBPROCESSES the seam engines (comp-heat/pipescript/lambdamap/iam/kuzu/freshness + globgrph iceberg/code/trino/tool parity); READ-ONLY | NFRA_COMPDRIFT_PRD.md + brief 20260629 | log:10152 coverage PASS; :10154 sweep FAIL (real findings); drift_cli.py:5-8 + subprocess dispatch L42-48 (calls, never re-implements) |
| comp-graph | `.tools/comp-graph` -> `org/modules/graph/graph_status_cli.py`; substrate graph_cache.py (D2) | built-proven | trace graph.json + per-firm platinum/trace caches + cloud kuzu status; status/clear | NFRA_GRAPHS.md (D3) | log:4615-4624 status/status --json/clear platinum/clear all PASS (2026-06-11) |
| comp-shell | `.tools/comp-shell` -> `org/modules/graph/shell_cli.py` | built-proven | reads .sh source only; Rule-16 forbidden-util list; wired into pre-commit gate on staged .sh | ADHC_BASHFIX.md (Rule-16 / Git Bash 3.6.7) | log:2144-2157 scan/list-forbidden AC1-AC10 PASS |
| comp-registry | `.tools/comp-registry` -> `org/modules/graph/registry_cli.py` | built-proven | REGISTRY narrative vs org/projects/*.json vs PRD Status: + git citations; `--apply` writes | manifest `meta.registry.drift`; NFRA_COMPDRIFT (no dedicated PRD) | log:4199 sync --project PASS; :4482 sync + --apply PASS |
| comp-coverage | `.tools/comp-coverage` -> `org/modules/graph/coverage_cli.py` | built-proven | compiler-tools-log.md (TO logging) vs done TOs; report [--by-agent/--gated-only/--pipeline]; writes REPORT.md | ADHC_COMPIL_V4.md (TO-coverage program) | log:3594-3595 report --by-agent + --gated-only PASS |

**Notes/gaps (this family):**
- **comp-drift orchestrator CONFIRMED** (not could-not-verify): drift_cli.py:5-8 + subprocess dispatch L42-48 shell out to the real seam engines; walks drift-topology.yaml as pure data; live `sweep` exit-1 = real cross-seam findings (topology coverage PARTIAL on seam-3/7, SELF-HEAL seam-4).
- **comp-heat exercise is build-time verify, not a runtime PASS row:** its 43 log hits are mostly comp-surface-check scans OF the file + 2 [IMPLEMENT] build-verify narratives -- no `|comp-heat|freshness|PASS|` invocation row like the other six. Built-proven via cited landing, noted.
- **Hint correction:** comp-graph -> graph_status_cli.py (NOT graph_cache.py, which is the D2 cache substrate it reports over).
- **Doc thinness:** comp-registry (only manifest entry + NFRA_COMPDRIFT mentions) + comp-coverage (only within ADHC_COMPIL_V4.md) have no standalone NFRA_* PRD -- gap vs comp-heat/xray/drift/graph/shell.
- **Trino-federation deps cost-guarded/HELD:** comp-heat `federated` + comp-drift seam-6 legs depend on the LIVE Trino surface (_trino_fed.py, in-VPC run-task; persistent endpoint SCTY-gated/HELD) -- those live subcommands NOT exercised offline; grounded on code + drift-topology `seam-6 COVERED`, not a fresh live run.

## 6. HONESTY / FEDOBS reflective-observation family (comp-honesty/fedobs)

| tool | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| comp-honesty | `.tools/comp-honesty` (runpy delegate) -> `org/modules/graph/comp_honesty.py` (453 L; GOV-A I1 honest-missing / I2 measure-per-case / I3 fires-when-exercised; STATIC-AST + EVIDENCE modes) | built-proven (strongest in family; no caveat) | fully LOCAL (Python stdlib ast/json; no cloud); doctrine dep NFRA_SEMCTL_HONESTY_INVARIANTS.md; GOV-A ratify b9f58b442 / CVO co-ratify 7aad2f834 | NFRA_SEMCTL_HONESTY_INVARIANTS.md (SS2/SS4.2); NFRA_COMPRAIL_GROUNDING_DOCTRINE.md | EXERCISED: `comp-honesty --self-test` -> **9/9 PASS** (GOV-A worked corpus incl D_02 silent-crash, A_00 aggregate-hide, dead-guard + counter-fixtures + dogfood N-A); self-test comp_honesty.py:319-416; canonical `meta.honesty.invariant_gate` |
| comp-fedobs | reader `.tools/comp-fedobs` (130 L, self-contained SS3 read-model); backing in-VPC producer (DISTINCT) `infra/aws/globgrph/fedobs/fedobs_observe.py` | built-proven (as a READER) -- THIN-signal caveat | reader: boto3 GetObject on `s3://.../warehouse/fedobs_signals/observations/fedobs_observations.json`; producer: in-VPC Trino iceberg.globgrph.cse (the C0 CSE log) + Nessie marker_head + cse_schema.py + fedobs_views.sql | NFRA_FEDOBS_PRD.md; TOs NFRA_FEDOBS.P1/P2/P3; fedobs_views.sql | EXERCISED: `python .tools/comp-fedobs` -> served artifact EXISTS+fresh, header "SERVED vintage (NOT live) as-of 2026-07-08T02:15:09Z marker_head=dfc00300271c source=iceberg.globgrph.cse **cse_log_total=6**"; canonical meta.fedobs.co_evolution/coverage_gaps/directive_effectiveness |

**Notes/gaps (this family):**
- **observe->measure axis is SEED-STAGE / thin-signal (material).** comp-fedobs the READER is proven (read the live served artifact, returned vintage-headed rows), BUT the observation surface is backed by only `cse_log_total=6` CSEs -- all from ONE seed session `nfra-cse-p2-seed-20260707`, every co-evolution pair `co_sessions=1`, single `['git']` producer. The measure arm functions but is a GENESIS SEED, not a mature production stream. The tool reports this thinness LOUD by design (reader THIN/EMPTY branch comp-fedobs:66-75). **CROSS-LINK:** this is the axis my class-5 GOV-B PROMOTE producer feeds -- the R4 in-VPC PROMOTE live-emit leg (0.5.0/0.7.0 deploy, pending) is a FUTURE producer into this thin log; directive-effectiveness (coverage-map L600) only binds at Wave-4 once PROMOTE materializes real directives. So the observe->measure loop is WIRED end-to-end but THINLY FED today.
- **Reader vs producer correctly separated (could-not-verify on the producer cadence):** comp-fedobs only READS (no recompute); fedobs_observe.py computes in-VPC against Trino. The fresh artifact (computed_at 2026-07-08T02:15Z) PROVES the producer ran >=1x, but its in-VPC scheduled cadence / role-bound live run is NOT directly observable from this host (Trino cluster-internal) -- inferred, not verified.
- **comp-honesty** = the one fully-local, deterministically-self-verifying, no-staleness-risk tool in the whole class-3 set (dogfoods I1 on itself -> un-checkable becomes LOUD N-A, never a silent PASS).
- **Registration drift (minor):** comp-fedobs commit 588cbe75a describes it as `not_homed` + manifest-excluded, yet comp-coverage-map.yaml carries it as 3 CANONICAL meta.fedobs.* entries -- the class label drifted from commit-message to canonical (both surfaces register it on-rail).

## 7. Class-3 GAP LIST (honest -- built-but-unproven / stale / contradictory / undocumented)

- **G1 (catalog projection lag):** `comp-dispatch` + `comp-symbols` (NFRA_COMPROUTE S1 tools, live in comp-which's curated RULES at comp-which:73/107) are NOT in the graph-call-manifest.yaml `tools_index` (37). They are routed + in the ledger but the manifest tools_index has not been re-projected to include them -> the "37" undercounts the routable set. `comp_coverage_view --verify` passes because it checks manifest-subset-of-ledger, not ledger-subset-of-manifest. HONEST: the manifest tools_index trails the ledger for the two newest routed tools.
- **G2 (affinity honest-state):** the COMPROUTE learned-affinity (w_h) term is WIRED but OFF by default (shadow-only). Any "comp-which learns from usage" claim is aspirational for the LIVE decision until the DRV affinity flip -- must be labeled built-but-not-live-enabled (GOV-A).
- **G3 (harness current-state unexercised):** comp-learns-*/comp-perf/comp-v5-composite-test current-state not exercised this pass (excluded_not_graph_use_cases) -- labeled built-unproven pending a follow-up exercise, not asserted working.
- **G4 (catalog status vs reality):** graph-call-manifest.yaml self-labels `v0.1 SCAFFOLD` (header) yet carries 37 fully-populated canonical entries + is the live comp-which source -- the status label is stale vs the built reality (a doc-vs-territory drift to reconcile: it is well past scaffold).
- **G5 (self-verification is the exception, not the rule):** across ~37 query tools, only a handful carry an in-module offline self-test (comp-chainrun `selfcheck`, pipescript `--validate`, comp-dups `--validate-dead`, comp-xray pytest, comp-honesty `--self-test`). The MAJORITY are `built-proven` on `status:canonical` + heavy compiler-tools-log usage, NOT self-verification -- family regression lives OUT-of-module (comp-v5-composite-test.sh, comp-tool-health). HONEST: "built-proven" here = exercised/used-in-production, not self-checking. A per-tool self-test coverage push is a real hardening gap.
- **G6 (doc-thinness cluster):** comp-secrets, comp-registry, comp-coverage (+ comp-cluster documented only in NFRA_TSGRAPH) have NO dedicated NFRA_* PRD -- documented only via the catalog/coverage-map entries + docstrings. A consolidation-index gap.
- **G7 (engine-home is non-uniform):** most engines are `.tools/comp-X -> org/modules/graph/X_cli.py`, BUT: comp-kuzu + comp-cluster live under `infra/aws/globgrph/`; comp-freshness + comp-secrets are SELF-CONTAINED (`.tools/comp-X` IS the engine, no separate module); comp-heat under `org/modules/heatmap/`; comp-xray under `infra/aws/compdiff/`; comp-dups nested in `org/modules/graph/debtscan/`. Feeds the Q1 comp-system-home decision -- there is no single engine home today.
- **G8 (directive file lags the SSoT):** comp-tools.yaml (the CLAUDE.md-facing directive) is missing comp-cluster + carries no lifecycle-status for the trace tools; the manifest tools_index is the status SSoT. + a STALE DUPLICATE `worktrees/comp-learns-_stub/org/modules/graph/comp-tools.yaml` (orphan copy).
- **G9 (persisted-ledger + live-path freshness):** comp-dups `dups_latest.json` is ~12d old (2026-06-26); the live-AWS tools (comp-freshness/aws/iam/lambdamap/secrets) + the cost-guarded Trino legs (comp-heat federated, comp-drift seam-6, SCTY-HELD) were NOT exercised this pass -- grounded on logged acceptance/code + drift-topology declarations, an honest could-not-freshly-verify on those specific paths.
- **G10 (observe->measure axis is THIN -- material, cross-class):** the FEDOBS observation surface comp-fedobs reads is a genesis seed (`cse_log_total=6`, single seed session, all `co_sessions=1`, single git producer). The reflective-observation LOOP is wired end-to-end (producers -> CSE log -> comp-fedobs reader -> MOTIF/PROMOTE consumers) but THINLY FED; directive-effectiveness binds only at Wave-4. This is the axis my class-5 GOV-B PROMOTE producer feeds -- the pending R4 in-VPC PROMOTE emit leg (0.5.0/0.7.0) will add real producer diversity. Any FEDOBS-derived "organizational signal" today must honor the LOUD thin-signal header (not a settled measure).
- **G11 (comp-fedobs producer cadence could-not-verify):** the in-VPC fedobs_observe.py scheduled cadence / role-bound live run is not observable from this host (Trino cluster-internal); proven ran >=1x (fresh artifact) but the standing cadence is inferred, not verified -- a genuine could-not-verify finding.
- **G12 (registration/class-label drift):** comp-fedobs commit 588cbe75a labels it `not_homed`/manifest-excluded, but comp-coverage-map.yaml carries it CANONICAL (3 meta.fedobs.* entries); comp-secrets/comp-dups skip the auto-logger by design (0 log-rows expected). Minor label-vs-reality drifts to reconcile at the SoT.

## 7a. Class-3-internal interaction summary (the spine; full cross-layer map = class 6/COO)

The class-3 surface is not 40 loose tools -- it is a **routed catalog over a shared substrate**:
- **Registry spine:** comp-coverage-map.yaml (SoT ledger, 56 tools) -> projects to -> graph-call-manifest.yaml tools_index (37) -> queried by -> comp-which (router) -> falls through to -> comp-grep/comp-glob (never-dead-end). `comp_coverage_view --verify` + comp-coverage-check gate the projection lockstep; the comp-tool-hud.sh PreToolUse hook + comp-which-rail.log are the enforcement + telemetry arm (COMPRAIL). This spine is my core domain and is built-proven end-to-end (exercised this pass).
- **Data-substrate clusters:** (a) the TRACE graph.json cache -- comp-trace/blast/build(producer)/diff/xref share it; (b) the KUZU/Nessie canonical graph -- comp-kuzu/comp-cluster/comp-aws(write-path) + comp-drift's kuzu seam; (c) LIVE portal/src parses -- comp-transform/cache/pii/types/tooltip/adapter-audit(+live S3); (d) LIVE AWS -- comp-iam/lambdamap/secrets/freshness/aws; (e) the CSE log -- comp-fedobs(reader) <- fedobs_observe(producer) <- the 5 CSE producers (incl my PROMOTE). comp-drift is the ORCHESTRATOR that walks these seams (calls, never re-implements).
- **Gate tools thread every hop:** comp-honesty (GOV-A claim honesty), comp-validate (pre-S3 artifact), comp-surface-check/manifest-check (commit-time), comp-parity/incrparity/lambdamap (parity) -- the freshness + honesty gates the TO's req names.

## 8. Open-decision touchpoints (PRD SS9) my grounding surfaces

- **Q1 (comp-system home):** the class-3 spine already has a de-facto home split -- the LEDGER (comp-coverage-map.yaml) is SoT, the manifest tools_index is a projection (NFRA_COMPUNIFY ruling #1). A comp-system home decision should ratify the ledger as the canonical registry.
- **Q2 (static-vs-dynamic boundary):** comp-which's affinity term is the live static/dynamic boundary question (curated-rules + surface-first = static/vetted; the learned-affinity flywheel = dynamic, currently OFF). The boundary is presently pinned STATIC-live / DYNAMIC-shadow.
- **Q3 (maturity taxonomy):** this inventory's built-proven/unproven/forming/designed-only labels ARE a maturity taxonomy instance -- feeds the Q3 decision.
- **Q4 (refresh cadence):** comp_coverage_view --verify is the drift gate; the catalog/ledger refresh cadence (when the manifest tools_index re-projects from the ledger) is the Q4 cadence question G1 exposes.

## 9. RAVC
RAVC 2.0.0_SA_COO~B (assembles the 6-class synthesis + routes CTO arch-gate / CVO grounded-not-recalled cert). Class-3 grounded against live source + exercised tools; built-but-unproven labeled as such.

---

# 10. NFRA_TOOLCHECK P1 -- functional-verification overlay (the HEALTH layer on the class-3 MAP)

**Method (non-negotiable):** real-invocation + usage-log-grounded (`org/compiler-tools-log.md`, 14,356 rows), NEVER `--help`. The false-green lesson cuts BOTH ways: a `--help` pass can HIDE a break AND a raw log-fail-count can OVERCOUNT honest-nonzero exits as breaks. Verdicts: **WORKS / BROKEN / GATE-FIRING-CORRECTLY / HONEST-UNVERIFIABLE / DISCOVERABILITY-FRICTION / RETIRE-CANDIDATE.**

## 10.0 PREREQUISITE (req#1) -- DONE + LIVE + COMMITTED

The telemetry-substrate jq starvation is FIXED (`org/mcp/hooks/post-tool-telemetry.sh`, SoD-committed 417004b7d). GROUNDED root cause (Rule 22, CORRECTED the hypothesis): NOT "no fallback" -- the fallback + `.tools/jq.exe` existed + installed==canonical; the real mechanism = `SCRIPT_DIR=$(cd $(dirname $0))` resolves to `.` INTERMITTENTLY when `$CLAUDE_PROJECT_DIR` is empty in the PostToolUse shell -> `${SCRIPT_DIR}/../jq.exe` missed + PATH missed -> starve (proof: NO_JQ log lines carry `script_dir=.` AND telemetry lands SOME calls -- intermittent, not total). FIX: a jq-resolution ladder independent of SCRIPT_DIR + a pure-bash guarded fallback that still emits telemetry. EXERCISED: NO_JQ frozen at 252 (zero new post-fix), telemetry landing every call, comp-shell r16-clean. **The USED-axis is un-starved -> RETIRE verdicts are now trustworthy** (do NOT retire on pre-fix starved data).

## 10.1 The per-tool verdict overlay (real-invocation + log-grounded)

**WORKS (log-grounded majority):** the bulk of the ~55 tools -- every class-3 built-proven tool (Sections 1-6) with heavy PASS rows in the 14,356-row log AND Part-0's log-mining confirming no break: comp-kuzu / aws / iam / routes / lambdamap / secrets / dups / trace / blast / build / diff / xref / transform / cache / cluster / pii / types / adapter-audit / pipescript / comp-pipescript / platinum / freshness / chainrun / incrparity / parity / heat / xray / graph / shell / registry / coverage / honesty / fedobs(reader) / comp-which / comp-grep / comp-glob. Grounded on real use, NOT --help.

**BROKEN (confirmed on REAL invocation this pass):**
| tool | real-invocation | verdict | grounding |
|---|---|---|---|
| comp-learns-run | `comp-learns-run` -> `No module named comp.framework.run` rc=1 | BROKEN (hard, every invocation) | packaging: the comp.framework.run module is absent. P2 fix #2. CONFIRMED real (Part-0 + my run) |
| comp-tooltip | `comp-tooltip --help` -> `comp-tooltip <U+FFFD> Portal tooltip...` | BROKEN (mojibake, r16/ASCII violation) + 46% scan-fail (Part-0) | a non-ASCII char in --help output (CLAUDE.md Code Quality). CONFIRMED. P2 fix #4 (-> ASCII). Also a RETIRE-CANDIDATE (one-off, 13 log rows) |

**Part-0 CORRECTIONS (my real-invocation grounding reclassifies 2 of the 4 pre-populated "breaks"):**
| tool | Part-0 said | my real-invocation finding | corrected verdict |
|---|---|---|---|
| comp-drift | "REAL BREAK 50% (41/82 FAIL, all forms), TOP break" | `coverage` rc=0 WORKS; `sweep` rc=2 = "EXIT: 2 (unverifiable)" -- the HONEST tri-state on the Trino seams (SCTY-held from this host), COVERAGE LEDGER COVERED=4/PARTIAL=2/SELF-HEAL=1 | **HONEST-UNVERIFIABLE, largely NOT a break** -- the exit-2 is never-silent-MATCH working as designed. A P2 fix must target only GENUINE crashes, NOT the honest-unverifiable Trino legs. (Some forms may still crash -- I ran coverage+sweep, not <path>/--deep; flag for the P2 pass to separate crash-legs from unverifiable-legs before "fixing" the 50%.) |
| comp-constants | "52% FAIL" | `comp-constants` -> detected real drift (GUARD_B_AUA_UPPER 400M vs canonical 300M); `check --lane bd` -> "OK: no drift across 34 constants" rc=0 | **GATE-FIRING-CORRECTLY** (nonzero on real drift = working, like comp-validate) + unmarked synthetic fixtures -- NOT a hard break |

**GATE-FIRING-CORRECTLY (nonzero exit = the gate working, NOT a break):** comp-validate (exit nonzero on NO_CONFIG/violation), comp-manifest-check (exit nonzero on a manifest violation), comp-surface-check (WARN/exit on a real critical-surface touch -- exercised this session on the promote_seam), comp-constants (above).

**DISCOVERABILITY-FRICTION (high fail-count from SURFACE, not a break):** comp-pipescript (21% -- canonical script/resource token-resolution: agents can't guess the token); comp-kuzu (12% -- Cypher-dialect: agents write typed relationships vs the CloudNode/CloudEdge-with-properties schema). Self-inflicted-by-surface -> P2 optimization (alias/`--list-resources`; schema-surface-at-prompt), NOT a fix.

**RETIRE-CANDIDATE (re-confirm on the NOW-un-starved telemetry -- do NOT retire on pre-fix data):** comp-tooltip (one-off migration tool, 13 log rows, mojibake), + Part-0's comp-dups/secrets/dispatch named low-usage -- BUT my class-3 grounded comp-secrets/dups built-proven + CVO-owned + skip the auto-logger (0 log-rows EXPECTED, not non-use). So their retire-candidacy is a FALSE SIGNAL from the starved+no-auto-log substrate; re-confirm usage post-telemetry-fix before any retire (P2 principle: fix-substrate-first).

## 10.2 Coverage-gap list (66 no-rich-tool rail escapes) -- ROUTE-vs-BUILD flagged (resolve in P3 before building)

| gap cluster | ROUTE-vs-BUILD | note |
|---|---|---|
| symbol/file-outline ("list functions/classes in a file") | **ROUTE** (comp-symbols EXISTS -- in comp-which RULES:107 but NOT in the manifest tools_index) | G1 from Section 7: comp-symbols is exist-but-under-projected. P3 routing fix, not a new build |
| type-def lookup ("show me the TenantLayoutConfig type") | **ROUTE** (comp-types EXISTS, comp-which routes `trace.types.type_consumers`) | verify the routing reaches it for a "show me the TYPE" phrasing vs "who consumes"; likely a phrasing-route gap |
| source-of-record "where is X" (LARGEST cluster) | **BUILD-or-ROUTE (P3 decide)** | named .tf/secret/script/function locate that pipescript/blast/kuzu didn't satisfy -> currently falls to comp-grep (the never-dead-end). May be the legit grep-primitive floor OR a missing locate-tool |
| live-AWS verify (SNS-delivers / SG-ingress / secret-read / s3-prefix-age) | **off-graph by design (likely)** | partly covered (comp-secrets read, comp-freshness artifact); the verify-live-behavior class is arguably operational, not a comp-tool gap |
| live-progress / staged-vs-served key-diff / mtime-localize | **BUILD-candidate (P3)** | a repeated `# rail-checked` override theme -> a real recurring intent with no rich tool |

## 10.3 The SYNTHETIC-MARKER problem (req#5)

The `(SYNTHETIC TEST FIXTURE)` marker is effectively UNUSED (1/1,302 FAILs marked) -> synthetic test-fixture invocations are INDISTINGUISHABLE from real failures in the usage log. This structurally BLOCKS a clean automated works/broken filter (a fail-count includes deliberate synthetic-FAIL fixtures, e.g. comp-honesty's D_02/A_00 red-fixtures, comp-chainrun's synthetic DROPPED/COLUMNS-LOST). FIX (P2): a commit/emit-time gate or lint that REQUIRES the marker on a synthetic-fixture invocation, so the log's real-fail signal is clean. This is exactly why the comp-drift/comp-constants "fail %" over-counted -- gate-firing + synthetic fixtures inflate the raw FAIL rate.

## 10.4 Break list (for P2), grounded on real use

1. **comp-learns-run** -- HARD BREAK (No module comp.framework.run) -- packaging fix. CONFIRMED.
2. **comp-tooltip** -- mojibake (r16/ASCII) + 46% scan-fail. CONFIRMED. (also retire-candidate.)
3. **comp-drift** -- NOT the flat 50% break Part-0 read; the exit-2 is largely HONEST-UNVERIFIABLE (Trino seams). P2: run <path>/--deep to isolate any GENUINE crash-legs from the honest-unverifiable before "fixing."
4. **comp-constants** -- NOT a break (gate-firing + synthetic fixtures). No fix needed; feeds the synthetic-marker fix.
5. **telemetry substrate** -- FIXED (417004b7d).
6. **synthetic-marker gate** -- P2 lint (unblocks automated works/broken).

## 10.5 Coordination + status

- **DS~B pull sent** (org/modules/graph engines -- comp-pipescript/validate/platinum/chainrun/incrparity/transform/cache/pii/types/constants/freshness): DS~B real-invokes + returns verdicts -> folded here. (My comp-constants correction shared.)
- Verdicts for the live-AWS tools (comp-aws/iam/lambdamap/secrets/freshness) rest on the 14,356-row log PASS evidence + class-3 built-proven grounding (not re-run this pass -- live AWS), per the log-ground-truth method.
- RAVC COO~B -> CTO arch-gate (verification-completeness) + CVO real-use-grounding cert -> P2 (fixes-first).
