<task_order>
  <metadata>
    <id>POSN_CUSTOM.002-RD</id>
    <slug>holdingstab-csm-custom-holdings-view</slug>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.2.1_RD_Positioning</issued_to>
    <date>2026-07-10</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project POSN_CUSTOM is complete; this TO was last touched 2026-07-10, predating the project close 2026-07-10. Closed as a record act, not a work verdict. Prior status: staged</status>
    <project_code>POSN_CUSTOM</project_code>
    <priority>P1 -- Andrew-prioritized 2026-07-10. STAGED behind POSN_CUSTOM.001: activates (GO) once .001's lifted custom-blend state lands. Do NOT begin until COO~C fires the GO on .001 completion.</priority>
  </metadata>

  <references>
    <prd>docs/architecture/POSN_CUSTOM.md -- PRD v0.1 (1.0.0_SA_CTO~C, @ e010d37b3). READ IT -- esp. sec.2 (HoldingsTab AGG aggregation :567-613, the exact machinery CSM reuses), sec.4.3, sec.6 TO-2 (this TO's authority).</prd>
    <arch_gate>1.0.0_SA_CTO~C arch-gates your build diff. RAVC back to CTO~C (via COO~C). Do NOT self-close.</arch_gate>
    <depends_on>POSN_CUSTOM.001 (same lane) -- reads the shared custom-blend state (weights) that .001 lifts to Positioning.tsx. .001 MUST land first.</depends_on>
  </references>

  <context>
    When the advisor picks the CSM ("Custom") holdings view, show the combined holdings of the custom blend
    (weighted by the advisor's custom MODEL weights, not AUM) + a column exposing those weights -- "similar
    to AGG, with the additional column" (Yang, call 09:26). The key reuse: HoldingsTab ALREADY aggregates
    all 5 portfolios' holdings AUM-weighted for the AGG view (HoldingsTab.tsx:567-613 / 696-777). CSM is that
    SAME aggregation with the AUM weight vector swapped for the custom weights, plus a weights column. This is
    a reuse, NOT a new aggregation engine.
  </context>

  <scope>
    File: portal/src/pages/Positioning/tabs/HoldingsTab.tsx.
    - PORTFOLIOS (line 22) += { id:'CSM', name:'Custom' } (AGG + 5 models retained).
    - Generalize the selectedPortfolio === 'AGG' aggregation branch (:567-613) to accept a WEIGHT VECTOR:
      AUM weights for AGG (unchanged), the shared custom weights for CSM. Read the custom weights from the
      Positioning-scoped state that POSN_CUSTOM.001 lifted.
    - Render the model-weights column ONLY in the CSM view.
    - Treemap + holdings table are already parameterized by selectedPortfolio -- reuse; do not duplicate.
    - Guard: CSM selected while the blend is invalid (Sum weights != 100) -> render the guardrail/empty state,
      NOT a partial aggregate.
  </scope>

  <compiler_tools_mandate>
    <phase_1_before_write>comp-transform schema-check HoldingsTab; read the AGG aggregation branch (HoldingsTab.tsx:567-613) to confirm the weight-vector generalization point before editing.</phase_1_before_write>
    <phase_2_before_commit>comp-cache collisions (no new key); comp-transform schema-check HoldingsTab (stay clean); bun run typecheck + bun run lint -- both exit 0, transcript in session log.</phase_2_before_commit>
    <phase_3_after_commit>DEV smoke -- CSM aggregates the same tickers as a hand-weighted blend; the weights column matches the POSN_CUSTOM.001 inputs; AGG output byte-identical to pre-change.</phase_3_after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>  <!-- Same-project dependency on POSN_CUSTOM.001 (reads its lifted state). Only file touched is HoldingsTab.tsx under portal/src/pages/Positioning/, owned by POSN_CUSTOM. comp-cache clean; no new query key. No cross-project shared files/S3 keys. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">CSM option present in the HoldingsTab portfolio selector.</ac>
    <ac id="AC2">CSM holdings = the custom-weighted merge of the 5 models' holdings (hand-verified on at least one ticker: Sum w_i * holding_weight_i).</ac>
    <ac id="AC3">The weights column shows the active custom weights (matching the POSN_CUSTOM.001 summary inputs).</ac>
    <ac id="AC4">AGG output is byte-identical to pre-change (the generalization must not regress the AUM path).</ac>
    <ac id="AC5">CSM while blend invalid (Sum != 100) renders the guardrail/empty state, not a partial aggregate. bun run typecheck + bun run lint both exit 0.</ac>
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change or regress the AGG AUM-weighted aggregation -- generalize it additively; AGG output must be byte-identical.</rule>
    <rule>Do NOT build a new aggregation algorithm -- reuse the existing AGG merge with a swapped weight vector.</rule>
    <rule>Do NOT begin before COO~C fires the GO (this TO is STAGED behind POSN_CUSTOM.001's lifted state).</rule>
    <rule>Do NOT commit or push to PROD. Build on portal DEV; hand to 0.2.0_DE_PortfolioAnalytics for compiler mandate + review + commit; 0.2.0_DT owns the DEV->PROD promote.</rule>
    <rule>No emojis / non-ASCII in code or the session log.</rule>
  </do_not>

  <deliverables>
    - HoldingsTab CSM view + weights column on the portal DEV working tree.
    - bun run typecheck + bun run lint both exit 0; transcript in your session log.
    - Session log under org/tier3_junior/0.2.1_RD_Positioning/logs/2026-07-10/ (Compiler Tools section mandatory).
    - MCP 0.2.0_DE_PortfolioAnalytics when ready for DE review + compiler mandate + commit.
  </deliverables>

  <handback>
    When done: MCP 0.2.0_DE_PortfolioAnalytics "POSN_CUSTOM.002 RD implementation ready" + files changed + typecheck/lint result. DE runs the 3-phase compiler mandate, reviews vs all 5 ACs, commits; the build diff routes to 1.0.0_SA_CTO~C for arch-gate; RAVC to COO~C. Do NOT flip this TO to complete yourself.
  </handback>
</task_order>
