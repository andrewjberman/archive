<to_id>NFRA_GRAPHS.D7</to_id>
<project>NFRA_GRAPHS</project>
<title>D7 — Graph-driven anomaly-detection pilot: Model Portfolios + Advisor Intelligence, both firms</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (MSTR veto-window close 565f56f89, 162825Z; Andrew-direct greenlight via /goal + /loop)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete — 2026-06-12T~1730Z by 0.4.0_DE_ClientPlatform; RAVC2 sent to COO</status>
<priority>P1 — runnable now (pre-full-stitch) with comp-platinum + trace tools; AC7 close-gate for NFRA_GRAPHS</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GRAPHS.md §9.3–9.5 (D7 protocol, templates, AC)</ref>
  <ref type="scaffold">d45da13af — D7/D8 scaffold commit</ref>
  <ref type="surfaces">org/modules/graph/critical-surfaces.yaml — SEV1: advisor_intelligence + model_portfolios.headline + model_portfolios.benchmark; SEV2: model_portfolios.peers + model_portfolios.aum</ref>
  <ref type="precached">org/modules/graph/adapter-audit/ — DE pre-work while holding: getPlatinumAdvisorSummary (84 WARN, typed_field_count=0), getPlatinumAdvisorSummaryStaticInflection (66 findings), getPlatinumClientDetailStatic (46 findings)</ref>
  <ref type="authority">MSTR 565f56f89 — veto window closed early on 3 Andrew directives; distance-0 authority</ref>
</references>

<background>
D7 is the proof-of-concept that the reconciled NFRA_GRAPHS toolset is not just a navigation aid but a deterministic bug/pattern-break detector. You were spawned for this and held pending Andrew's D7/D8 greenlight; that greenlight is now confirmed (MSTR 565f56f89).

While holding, you pre-ran adapter-audit work (the 3 YAML files in org/modules/graph/adapter-audit/). Those are inputs to this TO — incorporate them as pre-triaged field-contract findings (scan.field.contract_break family). Key pre-cached signal: getPlatinumAdvisorSummary has typed_field_count=0 (completely untyped interface against a 16-field S3 envelope) — this is a potential scan.auth.missing_edge finding (no type-level auth/access enforcement visible). Triage it explicitly against the auth/PII templates.

QUERY the graph — do NOT rebuild. The graph is fresh (comp-aws nightly + Nessie marker-keyed reader).
</background>

<scope>
Protocol is PRD §9.3 verbatim. Execute each step in order:

**Step 1 — Scope the subgraphs (pre-scan setup):**
```
comp-platinum summary --firm 49financial
comp-platinum summary --firm inflection
```
Enumerate the Model Portfolios + Advisor Intelligence component node-sets. These are the scan targets. Note any firm-asymmetry in the component set itself (a structural anomaly before any scan).

**Step 2 — Run all §9.4 anomaly-scan templates, per firm:**

For each template below, run against BOTH `--firm 49financial` AND `--firm inflection` unless the template is firm-agnostic. Record hits per template per firm.

| Template ID | Tool(s) | Run |
|---|---|---|
| scan.wiring.dangling_fetch | `comp-platinum page AdvisorIntelligence --firm <f>`, `comp-platinum page ModelPortfolios --firm <f>` | flag fetches with no gold script line |
| scan.firm.asymmetry | diff comp-platinum output between 49financial and inflection for each page | flag fetches resolved for one firm only |
| scan.orphan.dead_producer | `comp-pipescript consumers <script>` for each gold script feeding ADVI/MP + `comp-platinum reverse <key>` | flag keys with no portal consumer |
| scan.field.contract_break | `comp-transform schema-check AdvisorIntelligence`, `comp-transform schema-check ModelPortfolios` per firm; plus the pre-cached adapter-audit YAMLs | MISSING = runtime undefined (SEV); UNUSED = investigate |
| scan.cardinality.fanout_outlier | `comp-platinum summary` — flag components off the fan-out distribution for their page | structural outliers |
| scan.auth.missing_edge | `comp-pii audit`, `comp-routes auth-map` (or `comp-routes behaviors`) | flag routes missing auth edge siblings carry; flag PII on unauth route |

**Priority escalation:** the pre-cached getPlatinumAdvisorSummary typed_field_count=0 finding MUST be triaged against scan.auth.missing_edge and scan.field.contract_break before other findings. If it confirms as a live auth gap on a SEV1 surface (advisor_intelligence = SEV1 in critical-surfaces.yaml), escalate to COO as SEV1 immediately — do not wait for full scan completion.

**Step 3 — Triage each hit:**
For every finding across all templates: classify as:
- `real_bug` — confirmed defect, warrants a fix TO
- `expected_by_design` — known pattern, no action
- `false_positive` — template fired but no actual issue (note why, to tune the template)

**Step 4 — Deliverable:**
RAVC2 to COO with:
1. Findings report (triaged: real_bug | expected_by_design | false_positive per hit, per template, per firm)
2. Any SEV1 escalations called out prominently
3. Fix TO requests for confirmed real_bug findings (COO routes/cuts)
4. Template promotion list: which §9.4 templates found real bugs → these get promoted to `canonical` entries in graph-call-manifest.yaml (COO author-line, same handoff pattern as TO-F1/F2)
5. Recommended graph-call-manifest.yaml additions (provide the YAML patch; COO commits under exec author line)
</scope>

<acceptance_criteria>
AC7 (PRD §9.5): DE pilot runs all §9.4 templates against MP + ADVI subgraphs (both firms); produces triaged findings report (real/expected/FP per hit); files fix TO requests for confirmed bugs; promotes the bug-finding templates into graph-call-manifest.yaml as canonical anomaly scans. Template promotion = COO author-line commit (provide the patch in RAVC2).

Priority exit: if getPlatinumAdvisorSummary typed_field_count=0 confirms as a live auth gap on the advisor_intelligence SEV1 surface → immediate COO escalation before full scan completes.
</acceptance_criteria>

<cross_domain_coordination>
- Fix TOs for confirmed real_bug findings: route to COO in RAVC2; COO will cut/assign. Do not self-assign portal fix TOs.
- graph-call-manifest.yaml template promotions: exec-owned file; provide the YAML patch in RAVC2 and COO commits under exec author line (same pattern as TO-F1/F2).
- D8 (critical-surface monitoring): separate follow-on TO; this D7 pilot is the input. No D8 coordination needed now.
- NFRA_GLOBGRPH P2-STITCH: post-stitch, each template collapses to a single comp-kuzu Cypher query. That upgrade rides D4 — no dependency for D7 (pre-stitch tools are sufficient now).
- comp-platinum output may be cached — if stale, run with `--force` per graph-call-manifest.yaml rebuild guidance.
</cross_domain_coordination>
