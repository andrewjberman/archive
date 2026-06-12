<to_id>NFRA_GRAPHS.D8-DE</to_id>
<project>NFRA_GRAPHS</project>
<title>D8 — Critical-surface baseline scans + signed baselines per surface × firm (DE scope)</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_GRAPHS D8 decomposition, ~171200Z 2026-06-12)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>active</status>
<priority>high — last deliverable before NFRA_GRAPHS AC8 close; companion D8-AE TO (alarm infra) and CTO registry authority also in flight</priority>

<background>
critical-surfaces.yaml (org/modules/graph/critical-surfaces.yaml) defines 4 monitored surfaces:
  SEV1: model_portfolios.headline, model_portfolios.benchmark, advisor_intelligence (all firms)
  SEV2: model_portfolios.peers, model_portfolios.aum (all firms)

The file is scaffolded (v0.2, paths verified 2026-06-11) but `signed: false` — no baselines have been generated yet. D8-DE scope: generate the signed baselines + run D7-style anomaly scans against each carved subgraph + record Day-0 findings.

Baseline method (from critical-surfaces.yaml §84-86): `comp-xref --save per surface x firm at carve-time`.
</background>

<scope>
1. BASELINE GENERATION: For each of the 4 surfaces × each firm (49financial/bd, inflection/inf, cottonwood/cot = 12 surface×firm pairs), run:
   `comp-xref --save <surface_id> --firm <firm>` (or equivalent depending on comp-xref CLI)
   Save each baseline artifact. Check with `comp-xref --help` for exact invocation — the carve-root is the frontend_root from critical-surfaces.yaml per surface.

2. ANOMALY SCANS (D7 templates against carved subgraphs): For each surface, run the applicable canonical D7 templates (from graph-call-manifest.yaml anomaly.* entries) against the carved subgraph:
   - scan.wiring.dangling_fetch (comp-platinum)
   - scan.firm.asymmetry (comp-platinum, both firms)
   - scan.field.contract_break (comp-adapter-audit + comp-transform)
   - skip auth/orphan/cardinality if comp-platinum can't carve to the subgraph — note why
   Record all findings per surface × firm.

3. DAY-0 KNOWN FINDING (model_portfolios.aum): getAUMMetrics resolves to `url: (not resolved)` in comp-platinum (double-wrap indirection, known since D7). Document as a Day-0 baseline finding, NOT an alarm trigger (expected_by_design at carve-time).

4. UPDATE critical-surfaces.yaml: flip `signed: false` -> `signed: true` for each surface once its baselines are saved. Add a `baseline_generated` timestamp.

5. CREATE D8-findings.md in org/projects/ or org/modules/graph/: record all Day-0 findings per surface × firm in triage format (template, finding, verdict, baseline-or-alarm). This is the document AE's scheduled alarm wiring will diff against.

Deliverable sequence: baseline scan first (this TO), alarm infrastructure (D8-AE parallel), CTO registry review (in-flight). Your RAVC2 should include the signed: true flip + D8-findings.md path.

Note: CTO registry/severity authority review of critical-surfaces.yaml carve-roots is in-flight — if CTO requests carve adjustments before your baselines are finalized, hold the signed: true flip. Carve is firm enough to start scanning; wait for CTO ACK before calling baselines authoritative.

Acceptance (AC8 DE portion):
- critical-surfaces.yaml `signed: true` per surface (or explicit CTO-pending hold note if carve changes pending)
- D8-findings.md present with Day-0 triage per surface × firm
- comp-xref baseline artifacts saved per the baseline.method
- RAVC2 to COO
</scope>
