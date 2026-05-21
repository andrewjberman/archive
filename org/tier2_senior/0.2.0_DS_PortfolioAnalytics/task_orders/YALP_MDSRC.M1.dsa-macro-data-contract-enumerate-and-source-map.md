<task_order>
  <metadata>
    <id>YALP_MDSRC.M1</id>
    <slug>dsa-macro-data-contract-enumerate-and-source-map</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics~A</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — WS-C of YALP_MDSRC PRD v0.4 (6543894ce). PRD §6 "TO-M1". COO capacity call: owner 0.2.0_DS_PortfolioAnalytics~A — it authored F1 (the Bloomberg->FRED macro-sourcing audit/mapping), so it holds the exact macro-sourcing context M1 extends. Authors in parallel with V1/SA1/SA2/SA3. M1 hands its contract to M2 for independent verification — M1 does NOT self-certify source claims (R5).</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — WS-C. The enumerated macro data contract; Andrew's "cannot forget one" requirement.</priority>
    <sla>~1-2 effort-days — a contract row for each of ~91 indicators.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md (v0.4, 6543894ce) §6 TO-M1, §7 (the 12-group / ~91-indicator MACRO_GROUPS enumeration table — the starting frame).</prd>
    <f1>The F1 Bloomberg->FRED macro-sourcing audit (docs/briefs/mdsrc-fred-macro-sourcing-audit-20260520.md) — 0.2.0_DS~A's own prior work; M1 extends it from the FRED-only mapping to the full multi-source contract.</f1>
    <source_lambda>yang-generate-macro — the MACRO_GROUPS enumeration (12 groups, ~91 indicators, each with its Bloomberg ticker) IS the M1 starting enumeration; build on it, not a from-scratch discovery.</source_lambda>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md.</standard>
  </references>

  <context>
    The Macroeconomics page renders MACRO_GROUPS from yang-generate-macro — 12 groups, ~91 indicators, all Bloomberg-sourced today. M1 authors the enumerated macro data contract: for EVERY indicator, a contract row mapping it to its authoritative non-Bloomberg source.

    R5 — the contract must be EXHAUSTIVE ("cannot forget one" — every indicator enumerated, none dropped) and M1 does NOT self-certify (verifier != author; M2 independently validates every source claim). Andrew's premise is correct and expected: a material fraction (~25-30 of 91 — ISM, S&P PMI, NFIB, ADP, AAII, Conference Board, UMich, NAHB, Case-Shiller, MOVE, DXY, Bloomberg FCI) are proprietary releases with NO free government source — those resolve to YCharts-if-carried or stays-Bloomberg-proprietary. That split is the real WS-C output; stays-Bloomberg-proprietary is a valid honest verdict, not a failure.
  </context>

  <scope>
    <in_scope>
      - Start from the yang-generate-macro MACRO_GROUPS enumeration (PRD §7 — 12 groups, ~91 indicators, each with its Bloomberg ticker).
      - For EVERY indicator, produce a contract row: name | group | Bloomberg ticker | what it is | frequency | candidate authoritative source(s) | sourcing verdict.
      - Sources to evaluate per indicator: FRED, BLS, BEA, U.S. Census, BIS, U.S. Treasury, the originating body (ISM, Conference Board, AAII, NFIB, U. Michigan), YCharts.
      - Verdict space per indicator: FRED-replaceable | BLS | BEA | Census | Treasury | originating-body-direct | YCharts | stays-Bloomberg-proprietary.
      - Deliverable: the committed enumerated macro data contract (all ~91 rows). Hand it to M2 for independent verify-channel validation. RAVC2 to COO + CC CTO + the M1->M2 handoff.
    </in_scope>
    <out_of_scope>
      - Self-certifying source claims — M1 maps candidate sources + a verdict; M2 independently verifies (R5, verifier != author). M1 must not mark a row "confirmed."
      - Implementing any macro re-sourcing — M1 is the contract; migration is downstream.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
  Phase 1: confirm the enumeration is complete against yang-generate-macro MACRO_GROUPS — every indicator present, none dropped ("cannot forget").
  Phase 2: comp-platinum reverse on json/macro/** -> confirm which Macroeconomics components consume which indicator groups.
  Phase 3: hand the contract to TO-M2 for independent verification — TO-M1 does NOT self-certify source claims.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - M1 -> M2 handoff: the M1 contract is M2's input. M2 is owned by a DIFFERENT agent (0.1.0_DS_MarketIntelligence) per R5 verifier != author. RAVC2 the contract to COO + CC CTO + signal M2's owner.
    - No code/silver/bronze/gold/S3 changes — M1 is a contract document. Auto-rule 4 N/A.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — every indicator in yang-generate-macro MACRO_GROUPS present in the contract; Phase-1 completeness check confirms none dropped (~91 rows).
    - AC2 — per indicator: name, group, Bloomberg ticker, description, frequency, candidate authoritative source(s), sourcing verdict — all cells populated.
    - AC3 — the proprietary-vs-replaceable split explicit: every indicator with no free government source resolves to YCharts-if-carried or stays-Bloomberg-proprietary, called out.
    - AC4 — no row self-certified "confirmed" — M1 verdicts are candidate-source claims for M2 to verify.
    - AC5 — committed macro data contract; session log Compiler Tools section; RAVC2 to COO + CC CTO; contract handed to M2.
  </acceptance_criteria>
</task_order>
