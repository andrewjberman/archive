<to_id>NFRA_TSGRAPH.P3-1</to_id>
<project>NFRA_TSGRAPH</project>
<title>P3-1 -- log-mined bug/logic-class catalog (PARTITIONED frontend-detectable vs cross-domain) from 2745 logs + 203 LDs</title>
<assigned_to>3.0.0_SA_CVO</assigned_to>
<consult>NFRA_DEBTSCAN owner (2.0.0_SA_COO) -- the cross-domain partition is a CONSUMED input to the estate scanner; CC at P3-1 close</consult>
<issued_by>2.0.0_SA_COO (CTO PRD section-9 handoff 151724Z; PRD docs/architecture/NFRA_TSGRAPH_PRD.md @ 2b61ac87e, Andrew-steered 2026-06-18)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>staged</status>
<priority>HIGH -- Andrew-steered P3 substrate. INDEPENDENT lead (mines the log corpus; does NOT need the graph or a DE lane) -> the live-startable P3 lead. P3-2 + P3-3 gate on this catalog.</priority>

<context>
Andrew steered P3 to a LOG-MINED substrate: the structured log-scan IS the source (replaces the PRD section-4(3) theoretical bug list). Corpus: 2745 session logs + 203 LD entries + postmortems; signal density 756 root-cause / 524 silent-* / 459 P0-incident / 71 named-"X class" files. This TO produces the catalog that P3-2 (DE) turns into frontend detectors and that NFRA_DEBTSCAN consumes for the cross-domain classes.
</context>

<scope>
Mine the corpus (org/**/logs/**, org/tier0 LD records, docs/architecture/POSTMORTEM*, briefs) for named bug/logic classes -- "the X class", root-cause patterns, the silent-* family, P0/incident anchors -- and produce a STRUCTURED catalog, one row per class:
  {class, signature, exemplar-incidents (cited log/LD/commit), frequency, domain}
HARD REQUIREMENT -- PARTITION every class into:
  (a) FRONTEND/TS-detectable -> feeds P3-2 (DE graph detectors on the NFRA_TSGRAPH graph): OFC cohort/ternary forks, cross-firm conditional asymmetry, silent-display-fork, `any`-erosion, dead-code, prop-drill-depth, hook-dep-mismatch, render-guard-vs-nullability.
  (b) CROSS-DOMAIN (pipeline/data/infra) -> routes to NFRA_DEBTSCAN (the estate-wide scanner). NOT built here.
The catalog is a SHARED deliverable. Every class MUST cite at least one real log-anchored exemplar (the empirical anchor P3-2's validation gate depends on -- a class with no exemplar incident is not catalogued).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>structured corpus scan: count root-cause / silent-* / P0-incident / named-class signal files (baseline the density before mining)</run>
      <expect>~756 root-cause / 524 silent-* / 459 P0-incident / 71 named-class files (PRD section-9 census) -- confirm the corpus is intact before mining.</expect>
      <if_mismatch>If counts diverge materially from the section-9 census, note it -- the corpus may have grown/moved; mine what is present, do not assume the census.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-which "is there a bug-class / debt catalog already in NFRA_DEBTSCAN" + read org/projects/NFRA_DEBTSCAN.json + org/modules/graph/debtscan/</run>
      <expect>DEBTSCAN is a reachability/composition/cost scanner -- NO existing bug-class catalog (verified by COO at decomposition). Confirm your catalog is the shared UPSTREAM, not a duplicate of an existing DEBTSCAN artifact.</expect>
      <if_mismatch>If DEBTSCAN already has a bug-class artifact, STOP + surface to COO -- reconcile to one shared catalog, do not double-build (the exact CTO double-build flag).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>partition audit: every catalog row tagged frontend|cross-domain + every row has >=1 cited exemplar incident</run>
      <expect>0 untagged rows; 0 rows without an exemplar. The frontend partition is the P3-2 input; the cross-domain partition is the DEBTSCAN hand-off.</expect>
      <if_mismatch>An untagged or exemplar-less row fails acceptance -- P3-2's empirical-validation gate cannot anchor on a class with no real instance.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The catalog is a SHARED deliverable across NFRA_TSGRAPH P3 and NFRA_DEBTSCAN (project, COO-owned, the estate-wide scanner). DEBTSCAN is verified (COO, 2026-06-18) to be a reachability/composition/cost scanner -- NOT a bug-class miner today -- so this catalog is a clean shared UPSTREAM (no double-build). At P3-1 CLOSE: CC the NFRA_DEBTSCAN owner (2.0.0_SA_COO) with the cross-domain partition as a consumed input. Andrew-LOCKED BOUNDARY: P3 (this project) builds detectors ONLY for the frontend partition; the cross-domain classes are HANDED to DEBTSCAN, NOT built here -- no NFRA_TSGRAPH scope-creep into a general estate bug-miner.
</cross_domain_coordination>

<acceptance_criteria>
1. Catalog extracted from the corpus, one structured row per class: {class, signature, exemplar-incidents (cited), frequency, domain}.
2. EVERY class PARTITIONED frontend-detectable vs cross-domain (0 untagged).
3. EVERY class cites >=1 real log/LD/commit-anchored exemplar incident (the empirical anchor for P3-2 -- not theoretical).
4. Cross-domain partition handed to NFRA_DEBTSCAN (CC owner at close); frontend partition handed to P3-2.
5. Session-log Compiler Tools section reproduces every <run> above with observed output + pass/fail vs <expect>. Missing rows = REWORK.
RAVC2 to COO (CC CTO + NFRA_DEBTSCAN owner).
</acceptance_criteria>

<dependencies>
  <dependency artifact="log corpus (org/**/logs, org/tier0 LDs, postmortems)" status="available"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/NFRA_TSGRAPH_PRD.md section 9 (Andrew-steered P3 log-mined substrate, 2b61ac87e)</ref>
  <ref type="project">org/projects/NFRA_DEBTSCAN.json (the cross-domain consumer)</ref>
</references>

<lane_note>
P3-1 is the INDEPENDENT live-startable P3 lead -- mines the log corpus, needs no DE lane or graph. Assigned 3.0.0_SA_CVO (CVO-class structured analysis; CTO section-9 named "CVO or dedicated"). INDEPENDENCE NOTE: the catalog is a FACTUAL mining artifact (data, not a verification verdict), so CVO authoring it does not compromise CVO's later independence to verify P3 deliverables -- but if CVO is saturated past GCONTR.TO-3, COO may reassign to a dedicated mining spawn (allocation call). GATE for GO: COO confirms CVO capacity (or spawns dedicated) before GO. RAVC2 to COO (CC CTO + DEBTSCAN owner).
</lane_note>
