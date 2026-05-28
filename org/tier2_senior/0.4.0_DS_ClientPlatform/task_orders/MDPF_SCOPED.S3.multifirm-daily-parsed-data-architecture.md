# MDPF_SCOPED.S3 — Multi-firm daily-parsed data architecture (CORE BACKEND / SPINE, investigation-first) (DS~B + AE)

**Project:** [MDPF_SCOPED](../../../projects/MDPF_SCOPED.json)
**PRD:** `docs/architecture/MDPF_SCOPED.md` v0.1 §3 S3 + §4 + §8 Q4 (commit 486da0470)
**Pod:** 0.4.0_DS_ClientPlatform~B (lead) + 0.7.0_AE_CloudOps (bucket/Lambda/TF if infra needed)
**Lane:** DS_ClientPlatform ~B (MDPF on tilde-lane; ADVI_INFMVP holds DS-CP base — parallel, no contention)
**Issued to:** 0.4.0_DS_ClientPlatform~B
**Author:** 2.0.0_SA_COO 2026-05-28T~20:00Z (/drive — CTO MDPF_SCOPED NOVEL_PRD_READY 19:54Z)
**Sizing:** Phase-0 locate ~60-90min; design + emit sized after Phase-0
**Authority anchor:** CTO PRD v0.1 486da0470 + Andrew direct 2026-05-28

<status>complete</status>

## Objective — the backend spine

Model Portfolios is a **single global aggregate** of split-out cohorts today; it won't scale as partners onboard. Replace it with a **per-firm daily-parsed data architecture**: a Global method (cohort-based, preserves today's behavior) + per-firm scoped artifacts (49 Financial, Inflection) under a firm-subfolder structure that extends to Cottonwood/others **without central-logic edits**. **S3 is the spine** — S1's 3 dropdown modes and S2's Inflection 5/18 split both read S3's per-firm artifacts.

## Phase 0 — locate (investigation-first, do not redesign blind)

1. Trace where Model Portfolios data is held today: consumer fetches `portal/src/api/endpoints/aum.ts` (getAUMMetrics / getAUMTimeSeries / getAccountDistribution) + `portal/src/api/portal-proxy.ts` (getModelPortfolioBenchmarks / getNonModelAssets) → back to the S3 artifacts / API and the producing script(s).
2. Document how cohorts are split today (the single aggregate) — which script, which keys, where the cohort logic lives.

## Design (shared per-firm structure)

3. Global method that **uses cohorts** (preserves current Global behavior).
4. Subfolders for **49 Financial + Inflection**, structure extensible to future partners. Q4: bucket/prefix convention (e.g. `model-portfolios/{global|49financial|inflection}/{date}.json`) — align with inf-pipeline canonical prefix scheme; surface to COO if ambiguous.
5. **Shared parsing** so onboarding = "add subfolder + register firm", NOT "edit central cohort-splitting logic" (the maintainability driver; aggregate-of-cohorts explicitly rejected).

## Acceptance criteria

- **AC3.** Per-firm daily parse: Global artifact (cohort-based, current behavior preserved) + per-firm scoped artifacts (49F, Inflection) under an extensible firm-subfolder structure; the 3 S1 modes read their respective artifacts; onboarding a new partner = add subfolder + firm registration, documented. Rule 17: silver passthrough discipline; per-firm scoping that is business-logic (which cohorts = which firm) belongs in gold.
- **AC3-deploy.** Any Lambda/bucket changes via Terraform only (Rules 1-6); source-map update (Rule 4); `from __future__ import annotations` + ds-commit-gate (Rules 14/15) on any `data/*/scripts/{gold,silver,bronze}/*.py`.

## Dependencies

- **None upstream to start Phase-0.** S1 (selector) scaffolds in parallel against the Global artifact; S2 (Inflection 5/18) depends on S3's Inflection artifact carrying rolling-365d daily Non-Model AUA + the model-split.
- **ADVI_INFMVP coordination:** none direct (different page); shared firm-id namespace only (see Notes).

## Sequencing

1. ~30min: trace aum.ts + portal-proxy.ts fetches → S3/script producers; document current cohort-split
2. ~30min: design per-firm structure + prefix convention (Q4) + shared-parsing approach
3. **interim COO-surface:** Phase-0 findings + design sketch + Q4 prefix proposal before heavy emit build
4. emit Global + per-firm artifacts; deploy (TF) → RAVC2

## RAVC2 deliverable

`[RAVC2-Request] MDPF_SCOPED.S3 — multi-firm data architecture` to ws COO. CC ws CTO. Phase-0: interim findings MCP (current data location + cohort-split + prefix proposal). Build: per-firm artifact emit + extensibility doc + (if infra) TF 0-diff + tag.

## Compiler tools mandate

- `comp-pipescript io <script>` before edit (COLUMN GAPS + PORTAL CONSUMERS — Model Portfolios is a platinum consumer).
- `comp-iam service <lambda>` if new S3 prefixes/perms; Terraform-only deploy.
- `.tools/ds-commit-gate.sh` on any python edit (Rule 14).

## Cross-domain coordination

`<scoped/>` — Model Portfolios per-firm artifacts + portal consumers (aum.ts / portal-proxy.ts). Coordinate firm-subfolder prefix with AE. **Shared firm-id namespace with ADVI_INFMVP** — use the canonical `firmAccess.ts` L1 firm-id namespace AI already uses (Global/49financial/inflection); do not invent a parallel namespace.

## Notes

- MDPF runs on tilde-lanes (~B) so ADVI_INFMVP keeps the DS-CP base lane (Andrew priority) — the two projects parallelize.
- Investigation-first mandatory (Andrew + CTO): locate before redesign.

— ws COO /drive 2026-05-28T~20:00Z
