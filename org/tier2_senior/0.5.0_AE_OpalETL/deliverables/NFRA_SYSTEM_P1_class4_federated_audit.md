# NFRA_SYSTEM P1 -- SCOPE CLASS 4 (FEDERATED LAYER) audit

**Owner:** 0.5.0_AE_OpalETL (executor-audits-what-it-built, PRD SS7) | **TO:** NFRA_SYSTEM.P1 req-4 | **RAVC:** 2.0.0_SA_COO~B
**Grounding discipline:** Rule 22 -- current_state is GROUNDED (live-exercised THIS pass) or CERT-CITED (prior cert/commit), never
aspirational. `built-proven` = exercised live; `built-unproven` = built + self-tested but the LIVE/in-VPC path not yet exercised.
**Scope (req-4):** FEDOBS (cross-producer correlation over the CSE log via in-VPC Trino), the heat map (comp-heat + object-freshness),
analytics, the observe->measure axis (co-evolution, effectiveness). Boundary: the CSE store/schema itself is Class-1 (0.4.0_DS~B); the
CSE PRODUCERS (the "observe" half) + all FEDOBS correlation/measure surfaces are here.

## A. FEDOBS -- the horizontal correlation plane (federate-not-build over C0+C1)

| Component | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| FEDOBS view library (obs_findings_enriched, cross_observer_hotspots, directive_effectiveness) | infra/aws/globgrph/fedobs/fedobs_views.sql | built-proven | globgrph Trino (standing ECS svc), graph_nodes/edges (C1), code_heat.obs_findings | fedobs/README.md; docs/briefs/nfra-fedobs-p1-core-design-20260707.md | AC1 PROVEN live 2026-07-07: cross_observer_hotspots returned 3 C1 nodes flagged by 2 distinct observers (README §AC1); 2414 findings/4 observers emitted |
| fedobs_emit.py (observer-findings emitter, adapters) | infra/aws/globgrph/fedobs/fedobs_emit.py | built-proven | S3 warehouse (fedobs_obs_findings hive parquet), the 4 wired observers (D8/DEBTSCAN/COMPDRIFT/PIPESCRIPT) | fedobs/README.md | 2414 findings across 4 observers -> hive parquet (README "Proven live 2026-07-07") |
| fedobs_observe.py (FEDOBS-P3 reflective-surface producer, in-VPC fedobs read-only role) | infra/aws/globgrph/fedobs/fedobs_observe.py | built-proven | in-VPC Trino, the fedobs read-only role (Nessie HEAD via REST) | my log 2026-07-08 nfra_cse_p3_ac5_four_producers_live.md | CVO-certed dfc00300/d3c6106c7; whole FEDOBS plane closed 947ea237a |
| fedobs_trino_probe.py (in-VPC measure exerciser / P3 reflective-surface engine) | infra/aws/globgrph/fedobs/fedobs_trino_probe.py | built-proven | in-VPC Trino REST (trino.opal-globgrph.local:8080), iceberg.globgrph.cse | (docstring) | RE-EXERCISED THIS PASS 2026-07-08: ran coevolution/coverage/direff/provenance queries via ecs run-task on globgrph-derive-runner -> ERR:NONE |
| comp-fedobs (reader / reflective questions surface) | .tools/comp-fedobs + org/tier2_senior/0.5.0_AE_OpalETL/deliverables/comp-fedobs | built-proven (SoD-land = COO) | fedobs_observe served artifact (fedobs_observations.json), CTO arch-gate | my log nfra_cse_p3_ac5_four_producers_live.md | CTO arch-gate PASS; the 3 measure signals as provenance-linked reflective questions + served-vintage header (honest-thinness ruling) |
| fedobs-trino read-only role (AC2 boundary: read-only on truth catalogs, Deny on Put/commit) | infra/aws/terraform/... (fedobs role) | built-proven | Trino task role, IAM Deny-overrides-Allow | fedobs/README.md §Boundary | deploy-ledger 20260708T0145Z_fedobs-p2-readonly-role_deploy_completion.md (CLOSED); CVO AC2 exercise-cert |

## B. The CSE C0 log producers -- the "observe" half of observe->measure (the substrate = Class-1/DS~B)

| Component | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| iceberg.globgrph.cse (the live C0 log FEDOBS correlates over) | Iceberg/Nessie globgrph namespace (cse_store.py writer) | built-proven | Nessie REST, S3 warehouse, the marker-HEAD oracle | (cse_store.py docstring); NFRA_CSE_algebra_schema_v0.1.md | LIVE THIS PASS: total_cse=341 rows across git/graph_head/deploy/agent + frontend-coevolution partitions (probe read-back) |
| cse producers: git(seed) / graph_head / deploy / agent | infra/aws/globgrph/cse_emit_{graphhead,deploy,agent}.py | built-proven | cse_store (--ingest), cse_schema @0.4, derive task-def | my log nfra_cse_p3_ac5_four_producers_live.md | 4 producer partitions live (84 rows pre-this-pass); AC5 grounded read-back |
| cse_emit_frontend_coevolution.py (5th producer -- frontend co-evolution) | infra/aws/globgrph/cse_emit_frontend_coevolution.py | built-proven | DS~B's git co-change analysis (e6f5b00e2), cse_store, portal git | commit 84d9793b0; my log this session | PERSISTED THIS PASS: 257 CSEs -> globgrph.cse; cse_coevolution baseline 0 -> 54 live sparse frontend pairs; CVO-certed c13a73cdd/61ae8c3f1 |
| cse_emit_promote.py (6th producer -- PROMOTE directive-effectiveness feed, R4) | infra/aws/globgrph/cse_emit_promote.py | built-unproven (in-VPC ingest pending) | comp_promote_materializer._build_promote_cse (a0528032d), ProducerKind.PROMOTE @0.4, promote_recognizer_manifest.json | commit de804f615; ~D's R4 contract NFRA_PROMOTE_P2_GOVB_R4_promote_emission_contract.py | self-test 9/9 + reuse-fidelity == the reference builder; the LIVE in-VPC emit awaits 0.7.0's coupled @0.4 atomic pass (NOT yet in the store) |

## C. The heat + freshness observers (object-state correlation)

| Component | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| code_heat_emit.py (code-heat observer-findings binding -> obs_findings hive parquet) | infra/aws/globgrph/code_heat_emit.py | built-proven (source+precedent) | S3 warehouse (code_heat namespace), the Trino code_heat binding | fedobs_views.sql (the code_heat.globgrph.obs_findings ref) | fedobs_views.sql joins code_heat.globgrph.obs_findings live (the obs_findings_enriched base join) -- the binding is exercised by FEDOBS; NOT re-run standalone THIS pass |
| code_heat_parity.py | infra/aws/globgrph/code_heat_parity.py | built (source-present) | code_heat_emit | -- | source-cited; current-state NOT re-exercised this pass -- flag for the deeper live-exercise pass |
| comp-heat (heat-map reader) | .tools/comp-heat | built (source-present) | code_heat / object-freshness | graph-call-manifest.yaml | source-present + in the tools catalog; NOT re-exercised THIS pass -- flag for the deeper pass (honest: not a live cite) |
| comp-freshness (object-freshness / gold+platinum vintage) | .tools/comp-freshness | built-proven (prior) | S3 served artifacts, the marker oracle | CLAUDE.md comp-tool table; graph-call-manifest.yaml | the canonical freshness tool (s3 ls .../gold|platinum -> comp-freshness, CLAUDE.md); NOT re-exercised THIS pass -- prior-use cite only |

## D. The observe->measure axis (the FEDOBS-P2 measure signals + the promotion measure loop)

| Component | source_location | current_state | dependencies | existing_docs | grounding_citation |
|---|---|---|---|---|---|
| cse_coevolution (co-evolution measure -- MOTIF coupling/blast-radius input) | fedobs_views.sql @view cse_coevolution | built-proven | iceberg.globgrph.cse (subject_ref/run_id), the CSE producers | fedobs_views.sql | LIVE THIS PASS: 1319 total co-evo pairs; 54 real sparse frontend pairs after my frontend-coevo persist (baseline 0). The measure the PROMOTE gate reads |
| cse_directive_effectiveness (per-period transformation-pattern rate -- PROMOTE's warrant) | fedobs_views.sql @view cse_directive_effectiveness | built-proven (structured; measures once directives land) | iceberg.globgrph.cse (verb x subject_etype x scope x date) | fedobs_views.sql | live 2026-07-08 real per-period baseline (create/Lambda by firm bd=3/inf=2/cot=1); the PROMOTE CSE feed (cse_emit_promote) thickens the directive before/after |
| cse_compiler_coverage (recognizer-gap / honest-degrade rate per artifact_class) | fedobs_views.sql @view cse_compiler_coverage | built-proven | iceberg.globgrph.cse (subject_etype/confidence) | fedobs_views.sql | live 2026-07-08 lambda_source untyped_low_rate=0.0 (honest measured zero, count DISTINCT event_id) |
| cse_signal_provenance (AC3 decompression THROUGH the analytics) | fedobs_views.sql @view cse_signal_provenance | built-proven | iceberg.globgrph.cse (provenance_json) | fedobs_views.sql | live: every seed CSE resolves signal-row -> source CSE -> file:line evidence |
| PROMOTE-P3 standing monitor (post-promotion measure -> auto-demote feed) | infra/aws/globgrph/fedobs/promote_monitor.py | built-proven | DS~B run_measure (git coupling_ratio), recognizer-materializer demote, the manifest | commit 3cad838f0/713d4aec2; my log this session | self-test 12/12 (flapping guard + sustained auto-demote + recovery->re-propose); live tick silent-display-fork 0.180 SUSTAINED; CVO-certed c13a73cdd/61ae8c3f1 |
| frontend co-evolution measure (the CANDIDATE->MEASURED enabler) | cse_emit_frontend_coevolution.py -> cse_coevolution | built-proven | portal git, DS~B e6f5b00e2, cse_store | commit 84d9793b0 | this pass: baseline 0 -> 54 sparse pairs; anti-Goodhart coupling_ratio gate (>=0.15) bites downstream in PROMOTE-P1 |

## Cross-class dependencies (interaction-map inputs for COO~B's Class-6 synthesis)
- **Class-4 <- Class-1:** FEDOBS + all measures READ the CSE C0 log (iceberg.globgrph.cse) + the algebra (cse_schema @0.4). The producers emit CSEs that Class-1 validates fail-closed (cse_store.validate_batch).
- **Class-4 <- Class-2:** the correlation runs on the globgrph Trino + the marker-HEAD oracle (freshness/provenance header) -- Class-2 (0.7.0) infra; FEDOBS adds ZERO new engine (inherits the standing Trino, GLOBGRPH AC6).
- **Class-4 -> Class-5:** cse_coevolution IS MOTIF's coupling input; cse_directive_effectiveness + the PROMOTE monitor/producer ARE the PROMOTE measure+reverse loop (the observe->measure->promote->monitor->demote closed loop, proven 2026-07-08).
- **The observe->measure->promote flow:** a CSE producer OBSERVES (emits to globgrph.cse) -> cse_coevolution/effectiveness MEASURES -> PROMOTE-P1 gates on the coupling_ratio -> materialize -> the PROMOTE monitor RE-MEASURES on an interval -> SUSTAINED|DEGRADED->auto-demote. Every hop threads the fail-closed validate (honesty gate) + the marker-HEAD (freshness gate).

## Honest GAP LIST (Class-4; GOV-A -- built-but-unproven labeled as such)
1. **cse_emit_promote in-VPC emit UNPROVEN in the store** -- executable-ready (self-test 9/9) but the LIVE PROMOTE CSE is not yet in globgrph.cse; fires on 0.7.0's coupled @0.4 atomic pass. (In-flight, sequenced.)
2. **comp-heat / code_heat_parity current-state NOT re-exercised this pass** -- source-present + FEDOBS exercises the code_heat obs_findings binding, but comp-heat/parity were not run standalone this pass. Flag for the deeper live-exercise pass (Rule-22 honest: source-cited, not live-cited).
3. **comp-freshness prior-use cite only** -- canonical + heavily used, but not re-exercised this pass. A live-exercise cite would upgrade it to built-proven-this-pass.
4. **cse_directive_effectiveness is STRUCTURED-but-not-yet-MEASURING directive effect** -- it has a live per-period baseline, but MEASURES a promoted directive's before/after only once PROMOTE CSEs land (gap #1). The two gaps close together in the @0.4 pass.
5. **cross_observer_hotspots grain-heterogeneity** -- only path-2 (co-occurring-grain observers, D8 x PIPESCRIPT) proven; the grain-bridge (edge-hop for heterogeneous-grain observers) is a designed FEDOBS sub-capability, deferred (README design note). current_state = designed-only for the grain-bridge arm.

## Open-decision surfacings (PRD SS9, for CTO via COO~B)
- Q4 (refresh cadence): the FEDOBS measures + the CSE producers are currently AD-HOC/on-demand (ecs run-task); the standing/scheduled cadence (EventBridge, like the nightly derive) for the co-evolution producer + the PROMOTE monitor is an open durability decision (I flagged it as the NFRA_PROMOTE.P3 scheduling follow-on -- LD-0157: not self-armed).

*First-pass grounded inventory (Rule 22). Live-cited where exercised this pass (FEDOBS probe, cse store, frontend-coevo, PROMOTE monitor); source/cert-cited otherwise. Gaps 2-3 (heat/freshness live-exercise) are the honest deepen-next. RAVC COO~B. -- 0.5.0_AE_OpalETL 2026-07-08*
