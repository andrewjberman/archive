<to_id>NFRA_DEBTSCAN.TO-D3</to_id>
<project>NFRA_DEBTSCAN</project>
<title>TO-D3 -- canon-motif scorer + motif-outlier census (4 pattern-classes) over the marker-CURRENT estate graph, suppression-gated + twin-shadow-discriminated</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<consult>0.4.0_DE_ClientPlatform (SERVED_LINEAGE frontend-graph motifs if they reach the portal layer); 1.0.0_SA_CTO (canon-patterns author -- spec + AC4); 3.0.0_SA_CVO (adjudicates the outlier candidates -> the >=1 true deviation AC4 needs)</consult>
<issued_by>2.0.0_SA_COO (NFRA_DEBTSCAN PRD section 2c + AC4; canon-patterns.yaml v0.1 ef6110129 CTO-RATIFIED 2026-06-18 = the gate-clear)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_DEBTSCAN is complete; this TO was last touched 2026-06-25, predating the project close 2026-07-09. Closed as a record act, not a work verdict. Prior status: graph-native SHIPPED 2026-06-25 (AC4 pending CVO) + source-integration legs DEFERRED (scoped follow-on, COO-beat 180230Z). SHIPPED: the canon-motif scorer infra/aws/globgrph/debtscan_canon_scorer.py (7 commits 21792a412..3342e6a0a) -- per-class MULTI-SOURCE architecture CTO-RATIFIED (174018Z); freshness-gate (kuzu _canonical.ensure_fresh + HEAD-current-assert/abort-on-stale, 0-mutation read_only); canon-patterns + suppression_v1 loaders (twin_shadow + suppression kept SEPARATE); per-class SOURCE PROVENANCE (CTO auditability rider); EMIT (infra/aws/globgrph/debtscan_scorecard_latest.json); comp-manifest-check CLEAN (canonically-homed exempt path). GRAPH-NATIVE classes scored: AUTH_CANON shape-census (API_ROUTE-ROUTES_TO->LAMBDA 77 + ServedURL-SERVED_FROM->BUCKET_POLICY 29, 0 shape-outliers); SERVED_LINEAGE_CANON (29 resolved + 16 dangling_served -> 3-bucket: 5 known-dispositioned + 7 action-by-design + 4 NEW data-serving candidates). AC4 = 4 NEW dangling_served candidates ROUTED TO CVO (/returns/etf-periods, /aum/summary, /api/private/portfolio/funds, /api/scoped/security-scanner/factors) -- CVO verdict = the AC4 close-gate. DEFERRED (scoped follow-on, NOT dropped -- COO-logged, CTO comp-tool-backlog): DEPLOY_CANON(b) prefix-grain (source-map + comp-pipescript-deployed), AUTH_CANON auth-edge/rewrite deviations (comp-routes), PIPELINE_CANON interior (comp-pipescript) -- ALL BLOCKED on the comp-*-bash-subprocess-on-Windows ENVIRONMENTAL limit (banked; 3rd comp-tool runtime gap today w/ aws_freshness + comp-pipescript-io). Un-defer when the structured-source-ingest runtime path exists. RAVC2 COO+CVO on the ship.</status>
<!-- GO 2026-06-18 (COO /drive cycle-1): gate CLEARED -- AE RAVC2'd D8-AE Part B CORE (B1 ledger + B2-Layer1 scan + B5 hooks) COMPLETE, live-verified (82e27199c). TO-D3's real dep = the live scan+ledger surface + marker-current graph, all confirmed. The D8 residual (B4 real-time leg + AC8(d) demos + blocking-flip ramp) does NOT gate TO-D3. staged->pending. RAVC2 to COO (CC CTO+CVO). -->

<priority>QUEUED behind NFRA_GRAPHS.D8-AE Part B RAVC2 (shared AE 0.7 slot; D8-AE takes priority). Both CONTENT gates now CLEARED -- canon gate (ef6110129 delivered) + P1-precision gate (NFRA_TSGRAPH P1 complete) -> AUTHORABLE. Only AE-capacity sequencing remains (the D8-AE-Part-B priority).</priority>

<gate>NFRA_GRAPHS.D8-AE Part B RAVC2 (frees the shared AE 0.7 slot). COO GOes after that RAVC2.</gate>

<context>
canon-patterns.yaml v0.1 (CTO-ratified ef6110129) defines the estate's 4 CANONICAL path-motifs (PIPELINE_CANON / AUTH_CANON / DEPLOY_CANON / SERVED_LINEAGE_CANON) -- each with the graph-queryable motif, dominant-vs-outlier semantics, incident-anchored deviation-classes, and a TWIN_SHADOW_GUARD (bd/cot/inf parallels are DESIGNED twins, not deviations). This TO builds the scorer + motif-outlier census that consumes it. PRD 2c + AC4.
</context>

<scope>
Build the canon-motif scorer + motif-outlier census per the canon-patterns.yaml scorer_contract:
- INPUTS: canon-patterns.yaml (the canon) + the marker-CURRENT canonical + pipescript graphs + suppression_v1.yaml.
- For EACH of the 4 pattern-classes: enumerate concrete instances grouped by motif-shape (the ordered node_type/edge_type sequence). DOMINANT motif = the modal shape (N instances). A shape occurring 1-2x (or <= outlier_frac of the dominant) = UNUSUAL-BY-CONSTRUCTION -> candidate finding.
- BINDING: every outlier candidate is ADVISORY until CVO-adjudicated; the scorer files 0 MUTATIONS (verify-before-act is BINDING, PRD).
- REQUIRED DISCRIMINATION (not optional): a 1-2x shape that is DESIGNED (twin/per-firm/purpose-kept) is NOT a finding -- the per-pattern TWIN_SHADOW_GUARD (a CANON fact) clears it FIRST; SEPARATELY every candidate passes through suppression_v1.yaml (the 20 CVO-adjudicated FP classes) BEFORE filing -- a match = recorded suppressed-with-reason, NEVER filed RED. Keep twin-shadow (a canon fact) and suppression (an adjudicated FP) SEPARATE in the scorecard.
- FRESHNESS-BOUND: score against the marker-CURRENT canonical surface ONLY -- read the provenance header, HEAD MUST be CURRENT; a finding off a stale vintage is INVALID (PRD).
- OUTPUTS: (1) per-pattern-class scorecard (dominant motif + instance enumeration); (2) motif-outlier candidate list (shape, frequency, the dominant it deviates from, twin/suppression-clearance status).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-kuzu (the canonical + pipescript graphs) -- READ THE PROVENANCE HEADER</run>
      <expect>HEAD = current (pin==marker). The scorer is freshness-bound; building it against a BEHIND/UNKNOWN-VINTAGE surface invalidates every finding.</expect>
      <if_mismatch>STOP. If the header is not current, do not score -- a stale-vintage finding is invalid per the PRD. Surface to COO.</if_mismatch>
    </step>
    <step>
      <run>read canon-patterns.yaml + suppression_v1.yaml -- enumerate the 4 motif definitions + the 20 suppression FP classes + the per-pattern twin_shadow_guards</run>
      <expect>4 pattern-classes with their motif-shape + twin_shadow_guard; 20 suppression FP classes. The scorer's discrimination logic binds to these exactly.</expect>
      <if_mismatch>If a motif or guard is ambiguous, ping CTO (canon author) for the architectural beat BEFORE building the scorer logic.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-manifest-check (register the scorer as a canonical graph-call-manifest entry) + run the census against suppression</run>
      <expect>Scorer registered; the census runs CLEAN against suppression (0 double-fire of the 20 known FPs); >= 1 TRUE canon-deviation candidate surfaced for CVO adjudication (AC4).</expect>
      <if_mismatch>If the census double-fires a known FP, the suppression gate is wired wrong; if 0 candidates surface across all 4 classes, the motif-outlier threshold (outlier_frac) needs a CTO beat.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Consumes canon-patterns.yaml (CTO-authored, ef6110129) + suppression_v1.yaml (org/modules/graph/debtscan/) + the marker-CURRENT estate graph. Shares the AE 0.7 slot with NFRA_GRAPHS.D8-AE Part B (the GATE -- D8-AE priority). Motif-outlier candidates route to CVO adjudication (the >=1 CVO-verified true deviation = AC4). NO firm-pipeline cross-reference issue: the twin_shadow_guard EXPLICITLY treats bd/cot/inf parallels as DESIGNED twins (a canon fact), not deviations -- the scorer must not RED-flag a twin.
</cross_domain_coordination>

<acceptance_criteria>
1. Per-pattern-class scorecard produced for ALL 4 classes (PIPELINE/AUTH/DEPLOY/SERVED_LINEAGE): dominant motif + concrete-instance enumeration.
2. Motif-outlier candidate list: shape + frequency + the dominant it deviates from + twin/suppression-clearance status (twin-shadow and suppression kept SEPARATE).
3. AC4 DEMONSTRABLE: >= 1 TRUE canon-deviation finding, CVO-VERIFIED; the census runs CLEAN against suppression (0 double-fire of the 20 FP classes).
4. 0 MUTATIONS (scanner executes 0 deletes/edits). Freshness-bound (HEAD CURRENT at score-time).
5. Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail vs <expect>. Missing rows = REWORK.
RAVC2 to COO (CC CTO -- canon author + 3.0.0_SA_CVO -- adjudicator).
</acceptance_criteria>

<dependencies>
  <dependency artifact="canon-patterns.yaml v0.1 (ef6110129, CTO-ratified)" status="delivered"/>
  <dependency project="NFRA_GRAPHS" task="D8-AE Part B" note="shared AE 0.7 slot -- the GO gate" status="active"/>
  <dependency artifact="marker-CURRENT canonical + pipescript graphs" status="available"/>
</dependencies>

<references>
  <ref type="canon">org/modules/graph/canon-patterns.yaml (v0.1, ef6110129)</ref>
  <ref type="prd">NFRA_DEBTSCAN PRD section 2c + AC4</ref>
  <ref type="suppression">org/modules/graph/debtscan/suppression_v1.yaml (the FP gate)</ref>
</references>

<lane_note>
AE 0.7 primary (estate-graph scorer over canonical+pipescript -- consistent with TO-D1/TO-D4 AE lane); DE consult for SERVED_LINEAGE frontend motifs; CVO adjudicates the outlier candidates (the AC4 true-finding); CTO is the canon author (architectural beat if a motif/guard is ambiguous). STAGED -- GO after NFRA_GRAPHS.D8-AE Part B RAVC2 frees the shared AE slot (do NOT jump it ahead of D8-AE). Note: this adds to AE 0.7's load (already concentrated) -- the D8-AE-Part-B gate sequences it so it doesn't compound the live queue. RAVC2 to COO (CC CTO+CVO).
</lane_note>
