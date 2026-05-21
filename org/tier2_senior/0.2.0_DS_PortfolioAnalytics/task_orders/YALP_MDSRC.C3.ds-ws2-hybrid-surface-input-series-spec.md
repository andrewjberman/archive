<task_order>
  <metadata>
    <id>YALP_MDSRC.C3</id>
    <slug>ds-ws2-hybrid-surface-input-series-spec</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — CTO stimulus-scan recommendation, COO-issued. A3-INDEPENDENT and Q1-INDEPENDENT — this enumerates what the yang generators ALREADY consume, no YCharts dependency. 0.2.0_DS is idle and owns the WS-2 domain (it ran YALP_MDSRC.002). Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — parallelizes the C2 (YCharts market-data pull) critical path. When A3's internal-API mapping lands, C2's build needs the WS-2 hybrid-surface input requirements already enumerated; this pre-stages them so C2 is not serialized behind a fresh enumeration.</priority>
    <sla>~1-2 effort-days — a focused source-read + comp-pipescript enumeration; no code authored.</sla>
  </metadata>

  <references>
    <ws2_audit>docs/briefs/mdsrc-ws2-portfolio-analytics-audit-20260520.md + the WS-2 matrix slice — the YALP_MDSRC.002 WS-2 audit (your prior TO). C3 sharpens it from surface verdicts to the exact input-series requirements.</ws2_audit>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3.2 §5.2 WS-2 hybrid surfaces: correlation, factor spreads (FT-02/03), the Model Portfolios benchmark legs (MP-01/02/03).</prd>
    <c2>YALP_MDSRC.C2 (the YCharts market-data pull) — C3's output is a C2 build-input. Hand the finalized requirements list to C2 when it dispatches.</c2>
  </references>

  <context>
    The WS-2 hybrid surfaces are "yang generator + a market-data input" — the input leg will move to the YCharts internal API (C2). When A3's internal-API mapping lands, C2's build must know EXACTLY which index/security input series each WS-2 hybrid surface needs. C3 pre-stages that: it enumerates, per WS-2 hybrid surface, the exact input series the yang generator currently consumes — so C2's YCharts-pull build starts from a finished requirements list rather than serializing a fresh enumeration behind A3. Audit only; no code change.
  </context>

  <scope>
    <in_scope>
      For each WS-2 hybrid surface — correlation, factor spreads (FT-02 / FT-03), and the Model Portfolios benchmark legs (MP-01 / MP-02 / MP-03) — enumerate the EXACT index/security input series the yang generator consumes:
      - Run comp-pipescript io on yang-generate-correlation, yang-generate-factor-tilts, yang-model-portfolio-benchmarks (the load list + COLUMN GAPS + portal consumers).
      - Source-read each generator to confirm the precise input series — every index ticker / security symbol the generator reads, what it feeds, the cadence + units.
      - Cross-reference each input series to the YCharts crosswalk (the dc01d4b8a ticker map) where a YCharts mapping is already known, and flag the ones still needing an A3 internal-API lookup.
      Deliverable: a per-WS-2-hybrid-surface input-series requirements list — per surface: the input series (ticker/symbol), what it feeds, cadence/units, current source, the known-or-pending YCharts mapping. Machine-readable table form.
    </in_scope>
    <out_of_scope>
      - Building the C2 pull — C3 is the input spec C2 builds against.
      - The YCharts internal-API endpoint discovery — that is A3; C3 enumerates the REQUIREMENT (what input is needed), A3 supplies the ENDPOINT (where it comes from). Where they meet is C2.
      - WS-1 / WS-3 surfaces, SmartX, FRED — C3 is WS-2 hybrid only.
      - Any code / portal change.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before">
      <step>
        <run>comp-pipescript io yang-generate-correlation + comp-pipescript io yang-generate-factor-tilts + comp-pipescript io yang-model-portfolio-benchmarks</run>
        <expect>The load list + COLUMN GAPS + portal consumers for each WS-2 hybrid generator — anchor the input enumeration to compiler-confirmed fact rather than reading the scripts blind.</expect>
        <if_mismatch>If a generator is not a comp-graph node, fall back to a direct source read + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit"><step><run>(none) — spec doc, no code.</run><expect>No code gate applies.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
    <phase id="3" when="after commit"><step><run>(none) — the per-surface requirements table is the deliverable's self-validation.</run><expect>Checked by the ACs.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    C3's output feeds C2 (YCharts market-data pull; 0.1.0_DS + 0.2.0_DS co-owned) and dovetails with A3 (the YCharts internal-API mapping) — C3 = the requirement side, A3 = the endpoint side. Coordinate with 0.1.0_DS (A3) so the requirements list uses the same surface IDs A3's mapping uses. No shared files written (audit-only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Every WS-2 hybrid surface (correlation, FT-02, FT-03, MP-01, MP-02, MP-03) has its exact input-series requirements enumerated — per input: ticker/symbol, what it feeds, cadence + units, current source.</ac>
    <ac id="AC2">Each input series cross-referenced to the YCharts crosswalk where a mapping is known; the ones still needing an A3 internal-API lookup flagged explicitly.</ac>
    <ac id="AC3">Deliverable: a committed, machine-readable per-WS-2-hybrid-surface input-series requirements list (e.g. docs/briefs/mdsrc-ws2-c2-input-spec-20260520.md + table), pushed + push-confirmed on origin/CLOUD. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The per-WS-2-hybrid-surface input-series requirements list (committed, push-confirmed).
    - Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT build the C2 pull — C3 is the input spec.</rule>
    <rule>Do NOT duplicate A3's endpoint discovery — C3 is the requirement side; flag pending YCharts mappings, do not chase them.</rule>
    <rule>No emojis in the spec, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
