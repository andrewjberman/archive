<task_order>
  <metadata>
    <id>YALP_MDSRC.C5</id>
    <slug>ds-ws2-factor-pair-constituent-ratification-proposal</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — stimulus-scan reallocation (0.2.0_DS idle since C3 completed). A3-independent + Q1-independent. Pre-resolves a known C2 Phase-0 prerequisite. Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — pre-clears the C2 FT-02/03 critical-path prerequisite. C3 Finding 2 left the 6 factor-spread constituent index pairs unresolved; C5 pre-stages the ratification so C2's FT-02/03 leg is not serialized behind a cold consult.</priority>
    <sla>~0.5-1 effort-day — a focused proposal; no code.</sla>
  </metadata>

  <references>
    <c3>docs/briefs/mdsrc-ws2-c2-input-spec-20260520.md — C3 (your prior TO) §4 Finding 2: FT-02/03 cannot be ticker-enumerated from the yang generator; model.pkl/factor_spread is pre-computed.</c3>
    <cto_answer>CTO ruling 2026-05-20 (threaded into the C2 TO): the 6 factor-pair NAMES are documented — FACTOR_NAMES in infra/aws/lambda/v2_portal/yang_pipeline/factor_tilts/yang-generate-factor-tilts/lambda_function.py:32-35 — "Equity vs FI", "Growth vs Value", "US vs Foreign", "Large vs Small", "Agg vs Short", "HY vs Agg". The constituent index tickers per leg are NOT in the repo; most are semantically standard. CTO framed the C2 Phase-0 prerequisite as a small "ratify 6 index-pair picks" methodology item.</cto_answer>
    <crosswalk>docs/briefs/mdsrc-ycharts-ticker-map-and-fidelity-20260520.{md,csv} (dc01d4b8a) — the portal-entity -> Bloomberg-ticker -> YCharts crosswalk; use it to anchor each proposed constituent to an existing crosswalk row where one exists.</crosswalk>
  </references>

  <context>
    The 6 Opal factor spreads (FT-02/03) are each a ratio/spread of two index legs. The 6 pair NAMES are known; the exact constituent index ticker per leg lives only in Yang's manual model.pkl build. C2's FT-02/03 build needs those constituents. Rather than have C2 serialize behind a cold Yang-consult, C5 pre-stages a PROPOSAL: 0.2.0_DS (the WS-2 / portfolio-analytics specialist) proposes the most-likely constituent index ticker for each of the 12 legs (6 pairs x 2), with reasoning, as a ratification packet for Andrew / Yang to confirm. This is a proposal, NOT a unilateral decision — the ratification is Andrew's / Yang's.
  </context>

  <scope>
    <in_scope>
      For each of the 6 named factor pairs (Equity vs FI, Growth vs Value, US vs Foreign, Large vs Small, Agg vs Short, HY vs Agg), propose the constituent index for EACH leg:
      - The proposed index name + its Bloomberg ticker + (where one exists) its dc01d4b8a-crosswalk row / YCharts symbol.
      - The reasoning: why this index is the most-likely constituent (semantic standard, e.g. "US vs Foreign" -> S&P 500 vs MSCI EAFE; "Large vs Small" -> S&P 500 vs Russell 2000; "Growth vs Value" -> S&P 500 Growth vs S&P 500 Value; "Equity vs FI" -> an equity index vs an aggregate-bond index; "Agg vs Short" / "HY vs Agg" -> the relevant fixed-income indices). Anchor each pick in what the portal/yang factor-tilts surface already implies.
      - A confidence flag per leg: HIGH (semantically unambiguous) / MEDIUM (a likely pick with a plausible alternative) / LOW (genuinely needs Yang to confirm).
      - For any MEDIUM/LOW leg, name the alternative(s).
      Deliverable: a 12-leg ratification packet — a table Andrew or Yang can sign off in one pass — committed as a brief. Explicitly framed as "proposed, pending ratification."
    </in_scope>
    <out_of_scope>
      - Building anything — C5 is a proposal; C2 builds FT-02/03 once the constituents are ratified.
      - Reverse-engineering model.pkl's internal factor_spread computation — propose the constituents from semantic + portal evidence; do not chase the pkl internals.
      - The other WS-2 surfaces — C3 already covered them; C5 is the FT-02/03 constituent gap only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before"><step><run>comp-pipescript io yang-generate-factor-tilts</run><expect>The generator's load list — confirm what factor-tilts inputs the generator references, to anchor the proposed constituents in real evidence.</expect><if_mismatch>Fall back to a source read of the factor-tilts generator + document.</if_mismatch></step></phase>
    <phase id="2" when="before commit"><step><run>(none) — proposal doc, no code.</run><expect>No code gate.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
    <phase id="3" when="after"><step><run>(none) — the confidence-flagged table is its own self-validation.</run><expect>Checked by the ACs.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    C5's output feeds C2's FT-02/03 leg (0.1.0_DS + 0.2.0_DS co-owned) and the v0.4 plan. The ratification itself is Andrew's / Yang's call — C5 produces the packet, COO routes it for sign-off. No shared files written.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">All 6 factor pairs x 2 legs (12 legs) have a proposed constituent index — name + Bloomberg ticker + crosswalk row where one exists + the reasoning.</ac>
    <ac id="AC2">Each leg carries a HIGH/MEDIUM/LOW confidence flag; every MEDIUM/LOW leg names its alternative(s).</ac>
    <ac id="AC3">Deliverable: a committed ratification-packet brief (e.g. docs/briefs/mdsrc-c5-factor-pair-constituents-20260521.md), explicitly framed "proposed, pending Andrew/Yang ratification", pushed + push-confirmed on origin/CLOUD. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The 12-leg factor-pair constituent ratification packet (committed, push-confirmed).
    - Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT present the picks as decided — C5 is a proposal; the ratification is Andrew's / Yang's.</rule>
    <rule>Do NOT build the C2 FT-02/03 leg — C5 is the constituent spec it builds against.</rule>
    <rule>No emojis in the brief, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
