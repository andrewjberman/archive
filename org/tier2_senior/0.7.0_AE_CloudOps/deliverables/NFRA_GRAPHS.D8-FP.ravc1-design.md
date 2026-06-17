# NFRA_GRAPHS.D8-FP — AC2 design (RAVC1, pre-deploy)

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-06-17 · **TO:** NFRA_GRAPHS.D8-FP (faded9893, amended 7f9f8bc33)
**Status:** RAVC1 — design for CTO+COO sign-off BEFORE any deploy (deploy held per CTO 144431Z).
**Reviewers:** 1.0.0_SA_CTO (completeness + AC3 coverage), 2.0.0_SA_COO (track).

## 1. Problem (recap) + ruling
The 06-17 02:00Z in-derive SURFACE_SCAN published false SEV1/SEV2 (model_portfolios, advisor_intelligence). AC1 CONFIRMED FALSE-POSITIVE: the signed baseline (`critical-surface-baseline.json`, 2139 nodes/2691 edges, built 06-12) is a comp-graph MERGED build keyed `node_type:name` (incl. portal-AST); the in-derive scan diffs the AWS-only derive keyed by ARN -> key-spaces never intersect -> every portal node reads REMOVED, only the portal endpoint:/component: ones matched watched surfaces -> the fire. AWS estate healthy (no drop). CTO ruled **Option A** (AWS-backend-membership attribution); plain AWS-scope re-sign REJECTED (it de-noises but BLINDS — every AWS node has file_path="full-derive", surfaces are portal-keyed, so no AWS node could ever match -> 0 findings -> fails AC3).

## 2. Fix (Option A): per-surface AWS-backend membership
Replace the in-derive scan's `file_path -> watched-token` matching with **node-id MEMBERSHIP**: each surface x firm carries a set of AWS-backend node_ids (its carved subgraph); a removed/changed node fires the surface(s) whose membership contains it. Re-sign the baseline AS those per-surface carved subgraphs (ARN-keyed, F6-anchored). This implements what critical-surfaces.yaml `scheduled_scan` already specifies ("diff current SUBGRAPH vs signed baseline") and preserves out-of-band AWS-estate-drift detection (the absence-coverage layer the commit gate structurally can't provide). Portal-surface (source-file) watch stays on the dev-box B5 hook / comp-surface-check (Fargate has no git repo) — division unchanged.

Membership is anchored on **producer NODE IDENTITY** (prefix-distinct), NOT served-bucket writers: opal-data-portal-v2 has ~38 writers, opal-data-portfolio ~21 — bucket-writer enumeration is the inverse failure (a co-tenant removal false-fires every sibling surface). The served BUCKET node itself IS in membership (its removal correctly breaks all its surfaces); the discriminating part is the specific producer(s).

## 3. The carve (per surface x firm) — grounded on the 06-17 derive (comp-kuzu, provenance=current)

Membership per surface x firm = { producer node_id(s) | serving Lambda node_id(s) | served bucket node_id(s) }.

### model_portfolios.benchmark (SEV1, firm-agnostic — Opal models)
- producer: `arn:...:function:yang-model-portfolio-benchmarks`
- served: `arn:aws:s3:::opal-data-portal-v2` (json/benchmarks) + `arn:...:table/opal-portal-market-data`
- serving: `arn:...:function:opal-portal-data-proxy`

### model_portfolios.peers (SEV2, firm-agnostic)
- producer: `arn:...:function:yang-generate-peer-performance`
- served: `opal-data-portal-v2` + `opal-portal-market-data`
- serving: `opal-portal-data-proxy`

### model_portfolios.headline (SEV1) + .aum (SEV2) — per-firm AUA
- producer: `arn:...:instance/i-02448edb624a7a7cf` (mdpf-daily-runner, EC2) -> opal-data-mdpf + portal-v2; (portfolio-metrics producer TBD-grounded, see CAVEAT C2)
- served: `arn:aws:s3:::opal-data-mdpf`, `arn:aws:s3:::opal-data-portfolio`, `opal-data-portal-v2`
- serving: `opal-portal-data-proxy`

### advisor_intelligence (SEV1) — PER FIRM (no cross-firm bleed)
- **bd:** producers = bd-gold set {bd-gold-layer-runner (EC2 i-01003b...), bd-gold-detail-generator (EC2 i-074bfc...), bd-gold-foundation, bd-gold-layer, bd-gold-trigger, bd-gold-detail-checker (Lambdas)} -> served `opal-data-bd`; serving `shared-advisor-router`(+`-response`)
- **inf:** producers = {inf-gold-layer-runner (EC2), inf-portal-advisor-publisher, inf-portal-publisher, inf-gold-trigger} -> served `opal-data-inf`; serving `shared-advisor-router`
- **cot:** producers = {cot-exporter (EC2), cot-bd-session-trigger} -> served `opal-data-cot`; serving `shared-advisor-router` — **CAVEAT C3** (confirm cot ADVI is live-served before arming; if cot has no ADVI surface yet, cot-ADVI membership = recorded no-op, not a silent gap)

## 4. Scan-matching code change (`derive_runner.run_critical_surface_scan`)
- Baseline schema -> per-surface-x-firm membership: `{ "surfaces": { "<id>__<firm>": { "members": {node_id: {node_type, drift_class}}, severity } }, "f6_marker": {...}, "built_at": ... }`.
- Diff: for each surface, `removed = members(baseline) - nodes(current)`; `changed = members where drift_class differs`. Finding = (severity, kind, surface, firm, node_id). Drop the file_path/_file_touches path entirely for the in-derive scan (it's the portal mechanism; non-regressed on the dev-box comp-surface-check side).
- `_graph_to_scan_nodes` still provides the current AWS node set (ARN-keyed); membership compares ARN-to-ARN (like-for-like).
- Existing comp-surface-check commit gate (Part A) UNTOUCHED.

## 5. Baseline re-sign mechanism
- Carve the per-surface-x-firm membership from the 06-17 derive graph (NO ad-hoc run — carve the existing vintage). Intentional re-sign (not auto-rolling); re-signed only when membership legitimately changes (new producer added).
- F6-marker-anchored (record nessie_commit_hash + snapshot_ids at sign-time per the yaml provenance rule). Upload to `s3://opal-313476888478-globgrph/critical-surface-baseline.json` (replacing the merged-build content).

## 6. AC3 egress-test matrix (BINDING — synthetic removal must FIRE the right surface, egress-verified)
| Synthetic removal | Must fire | Must NOT fire |
|---|---|---|
| drop `yang-model-portfolio-benchmarks` | model_portfolios.benchmark | advisor_intelligence, peers |
| drop `yang-generate-peer-performance` | model_portfolios.peers | benchmark |
| drop `mdpf-daily-runner` (i-02448) | model_portfolios.headline + .aum | benchmark, ADVI |
| drop a bd-gold producer | advisor_intelligence (bd) | advisor_intelligence (inf/cot), model_portfolios |
| drop `inf-portal-advisor-publisher` | advisor_intelligence (inf) | advisor_intelligence (bd), model_portfolios |
| (control) drop a co-tenant non-member (e.g. `test-yfinance-simple`) | NOTHING | all surfaces |
Egress-verified = the SNS topic actually receives the publish (not "wired"). A miss on any "Must fire" row = AC3 fail, do not close.

## 7. Recorded CAVEATS (honest gaps — CTO standard: a known gap beats a false-confident scan)
- **C1 (bucket-grain):** membership anchors on producer identity; shared served buckets (portal-v2, portfolio) are in membership as bucket NODES (removal fires all dependents = correct) but their WRITERS are not enumerated into membership (would noise-amplify).
- **C2 (getAUMMetrics unresolved):** critical-surfaces.yaml already records getAUMMetrics resolves to "url: (not resolved)" — the portfolio-metrics producer for headline/aum is not cleanly graph-resolvable. Membership covers the resolvable mdpf AUA leg (mdpf-daily-runner -> opal-data-mdpf); the unresolved getAUMMetrics leg is a recorded coverage gap, NOT papered over. Flag to CTO for whether to chase the portfolio-metrics producer or accept the mdpf-leg coverage.
- **C3 (cot ADVI):** cot has producers (cot-exporter, cot-bd-session-trigger) but cot's advisor_intelligence surface may not be live-served yet (cot is snapshot-first, newer firm). Confirm before arming cot-ADVI membership; if not live, record cot-ADVI as no-op (not a silent blind spot).

## 8. Deploy plan (held for RAVC1 sign-off)
1. derive_runner.py code change (scan-matching) -> ds-commit-gate -> safe-commit.
2. Image rebuild via CodeBuild: **re-zip+upload the 6 Dockerfile-COPY'd files BEFORE start-build** (S3-ZIP stale trap; resolvedSourceVersion=null tell); plain --dry-run discriminate the image carries the change.
3. Re-sign + upload the per-surface baseline.
4. AC3 egress-test (section 6) on the rebuilt image against the 06-17 derive graph (synthetic removals).
5. Terraform-only for any infra; 0-diff. comp-iam gaps if iam.tf touched (not expected — code+data only).
6. AC4: confirm model_portfolios + advisor_intelligence healthy on SERVED state.
7. RAVC2 to COO, CC CTO.

## 9. RAVC1 asks
- CTO: (a) membership COMPLETENESS — any missed producer per surface x firm = a coverage hole; (b) the AC3 matrix exercises each watched surface x firm; (c) ruling on C2 (chase portfolio-metrics producer vs accept mdpf-leg) + C3 (cot ADVI arm vs no-op).
- COO: track + the resized-TO AC alignment.
- Deploy holds until both sign off.
