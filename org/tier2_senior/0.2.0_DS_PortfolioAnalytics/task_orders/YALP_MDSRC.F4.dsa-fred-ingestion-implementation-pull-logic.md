<task_order>
  <metadata>
    <id>YALP_MDSRC.F4</id>
    <slug>dsa-fred-ingestion-implementation-pull-logic</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics~A</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — CTO stimulus-scan recommendation, COO-issued. The FRED implementation is Q1-INDEPENDENT (FRED is its own official API, unrelated to the YCharts Q1) and F1 delivered the full Bloomberg->FRED mapping spec — the authoring work is fully unblocked. 0.2.0_DS~A is idle and owns the FRED specialization (it ran F1). Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — the first true Phase-2 IMPLEMENTATION segment that can start now. FRED is Q1-independent; B1/SmartX is mid-deploy; YCharts C1/C2 wait on A3. FRED is the segment to bootstrap immediately.</priority>
    <sla>~2-3 effort-days for the pull-logic authoring + verification. The AE commit+deploy is a sibling TO (see cross_domain_coordination) gated on the F2 IaC ruling.</sla>
  </metadata>

  <references>
    <f1_brief>docs/briefs/mdsrc-fred-macro-sourcing-audit-20260520.md + the mapping TSV (328e3b271) — the F1 FRED macro-sourcing audit. §3.3 is the requirement->FRED-series-ID mapping; §3.4 the empirical fidelity check vs Bloomberg-pkl. This is the build spec — F4 implements it.</f1_brief>
    <pattern>portal/etl/orchestration/green/fred/lambda/fred-data-ingestion/ingest_yield_curve_fred.py — the proven FRED-ingest pattern to extend. NOTE the F2 P0 finding: that fred Lambda family has NO IaC and fred-data-ingestion stores the FRED API key as a PLAINTEXT env var — F4's new pull must do it RIGHT (Secrets Manager), not copy the hygiene gap.</pattern>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED, 73e4da697) — FRED is a documented-API source: characterize it EMPIRICALLY, not docs-blind (§3 step 1). §3 step 2 — the FRED API key binds to AWS Secrets Manager. §3 step 6 — contract-drift detection (fail loud if a FRED series shape/availability changes).</standard>
    <f2_dependency>YALP_MDSRC.F2 — its CTO IaC mechanism ruling (the fred Lambda family has no IaC) governs how F4's FRED-ingestion Lambda deploys. F4's AUTHORING does not wait on it; the deploy sibling-TO does.</f2_dependency>
  </references>

  <context>
    F1 audited the Macroeconomics page and delivered a complete Bloomberg-ticker -> FRED-series-ID mapping (~50 indicators are FRED-migratable; the rest are the documented non-FRED residue). The FRED migration is the most ready Phase-2 implementation segment: Q1-independent, fully spec'd, and FRED is a free official API. This TO is the FRED-ingestion implementation's AUTHORING half — DS~A authors + verifies the pull logic; an AE sibling-TO commits + deploys the Lambda (infra/aws/lambda + the deploy mechanism are AE lane — same B1/B2 author/deploy split). v0.2 of YALP authorized no implementation; F4 is explicitly the FRED implementation, separately authorized here by CTO recommendation + COO issue.
  </context>

  <scope>
    <in_scope>
      PHASE 0 (empirical FRED characterization): per the Third-Party Data Integration Standard, confirm the FRED API empirically — the series/observations endpoints, the real param semantics (units, frequency, aggregation), rate limits, and that every FRED series ID in the F1 §3.3 mapping resolves to live data. Surface any F1-mapped series that does not resolve.
      PHASE 1 (author the pull logic): author the FRED-ingestion pull for the ~50 FRED-migratable indicators in the F1 mapping, extending the ingest_yield_curve_fred.py pattern. The pull: authenticates via the FRED API key from AWS Secrets Manager (NOT a plaintext env var); pulls each indicator's series; emits the artifact(s) the Macroeconomics page consumes, matched to the existing macro JSON shape. Build in contract-drift detection (fail loud on a missing/shape-changed series — Standard §3 step 6).
      PHASE 2 (verify): verify the pulled FRED values against the F1 §3.4 fidelity check (vs the current Bloomberg-pkl values); ds-commit-gate clean; a dry-run produces the expected artifact for all ~50 indicators. Document any fidelity gap.
      Deliverable: the authored + verified FRED-ingestion pull code (in the working tree, gate-clean) + a short build note (the per-indicator verification + any gap), handed to the AE deploy sibling-TO.
    </in_scope>
    <out_of_scope>
      - The AE commit + deploy of the FRED-ingestion Lambda — that is the AE sibling-TO, gated on the F2 IaC mechanism ruling. F4 authors + verifies; AE commits + deploys (infra/aws/lambda is AE lane).
      - The non-FRED residue indicators (the F1-documented international/licensed series FRED cannot serve) — out of FRED scope.
      - The yield_curve / macro-timeseries staleness fixes (F2 / F3) — separate TOs.
      - Portal-frontend changes — the macro JSON shape is matched; no FE work.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before">
      <step>
        <run>(none for the FRED API itself — external system) + comp-routes behaviors for the macro artifact serving paths the pull feeds</run>
        <expect>Confirm the serving paths for the artifacts F4 produces; the FRED API is characterized by empirical probe per the Standard.</expect>
        <if_mismatch>Document any serving-path delta as a finding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit/handoff">
      <step>
        <run>.tools/ds-commit-gate.sh on the authored pull script(s)</run>
        <expect>All three checks exit 0 (py_compile + ds-precommit-check + ruff py39).</expect>
        <if_mismatch>Fix before handoff.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after"><step><run>the per-indicator fidelity check vs F1 §3.4 is the deliverable's self-validation</run><expect>Checked by AC3.</expect><if_mismatch>Document gaps.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    AE DEPLOY SIBLING-TO: F4's FRED-ingestion Lambda must be committed + deployed by AE (infra/aws/lambda lane). The deploy mechanism is governed by the F2 CTO IaC ruling (the fred Lambda family currently has no IaC). When F4's authoring completes, COO issues the AE deploy sibling-TO referencing F4's build note — same author(DS)/deploy(AE) split as B1/B2. Coordinate the artifact path/shape with whoever owns the macro page artifacts. RAVC2 feeds PRD v0.4.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0: the FRED API characterized empirically; every FRED series ID in the F1 §3.3 mapping confirmed to resolve to live data, or the non-resolving ones surfaced.</ac>
    <ac id="AC2">Phase 1: the FRED-ingestion pull authored for the ~50 FRED-migratable indicators, extending the ingest_yield_curve_fred.py pattern; the FRED API key sourced from AWS Secrets Manager (not plaintext); contract-drift detection built in.</ac>
    <ac id="AC3">Phase 2: the pulled FRED values verified against the F1 §3.4 fidelity check; ds-commit-gate exit 0; a dry-run produces the expected artifact for all ~50 indicators; fidelity gaps documented.</ac>
    <ac id="AC4">Deliverable: the authored + verified pull code (gate-clean, in the working tree) + a build note handed to the AE deploy sibling-TO. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The authored + verified FRED-ingestion pull logic (~50 indicators) + the per-indicator verification build note.
    - Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT copy the plaintext-API-key hygiene gap from fred-data-ingestion — the new pull uses AWS Secrets Manager (Standard §3 step 2).</rule>
    <rule>Do NOT commit/deploy the Lambda — F4 authors + verifies; the AE sibling-TO commits + deploys (infra/aws/lambda is AE lane).</rule>
    <rule>Do NOT block on Q1 — FRED is its own official API, Q1-independent.</rule>
    <rule>Do NOT handle the FRED API key in chat / MCP / git / logs — reference the secret by name only.</rule>
    <rule>Terminology: this is an INTEGRATION against the FRED API — never "scrape" (Third-Party Data Integration Standard).</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
