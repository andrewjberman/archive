<task_order>
  <metadata>
    <id>YALP_MDSRC.S1</id>
    <slug>ds-smartx-coverage-deep-dive-positioning-attribution-factortilts</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <co_owner>0.4.0_DS_ClientPlatform — owns Part A (the SmartX REST probe); rides alongside YALP_MDSRC.B1 since 0.4.0 is already in the SmartX REST API. 0.2.0_DS_PortfolioAnalytics owns Part B (the surface mapping) + the deliverable.</co_owner>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO NOW — Andrew-direct (idle agents are not acceptable; 0.2.0_DS is idle, this is its real work). Q1-INDEPENDENT — SmartX, not YCharts. Part B (0.2.0) starts immediately — surface enumeration + the Brinson question do not wait on Part A. Part A (0.4.0) rides alongside B1.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct. The model-dimension extension of WS-3 (which scoped only model-portfolio *performance*); answers what SmartX can secure for the Positioning / Attribution / Factor-Tilts surfaces. Feeds the v0.4 amendment.</priority>
    <sla>~2-4 effort-days. Part B can begin now; Part A rides B1.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. §5.2 surfaces: WS2-FT-01 (factor tilt snapshot — "proprietary"), WS2-FT-02/03 (factor-spread series — "hybrid"), WS2-POS-01 (model holdings — "Bloomberg-pkl-only"), WS2-POS-02 (allocation summary — "proprietary"), WS2-POS-03 (Brinson holdings attribution — "proprietary"), the Model Portfolios benchmark/peer surfaces. This TO re-tests those verdicts against the SmartX REST API's model-dimension endpoints.</prd>
    <ws3_brief>docs/briefs/mdsrc-ws3-client-facing-data-audit-20260520.md (f963b8727) — the WS-3 audit; the SmartX REST API characterization (model-portfolio performance). S1 extends it to holdings / attribution / factor inputs.</ws3_brief>
    <b1>YALP_MDSRC.B1 (0.4.0_DS_ClientPlatform) — the SmartX-REST model-performance pull; reuses the SXPL_RESTIN ROPC-JWT auth. Part A of S1 rides the same auth path.</b1>
    <index>docs/briefs/mdsrc-INDEX.md (281cf0b2a) — the YALP_MDSRC consolidation / start-here nav doc.</index>
  </references>

  <context>
    Andrew-direct: a definitive read on what SmartX can secure for the portfolio-analytics surfaces that WS-3 left as "proprietary"/"Bloomberg-pkl-only" (WS-3 only scoped model-portfolio *performance*). The SmartX REST API (`api.smartxadvisory.com/api/3.1`) exposes more than the performance endpoints B1 uses — model holdings, statistics, peer/category data. If SmartX model holdings + returns can drive an automated Positioning view and a Brinson attribution, several "permanently manual" verdicts (the manual `attribution_excel`, `model_pkl` positioning) may downgrade to SmartX-securable. v0.2 authorizes NO code/Terraform/portal change — this is an audit.
  </context>

  <scope>
    <in_scope>
      PART A — SmartX REST probe (0.4.0_DS_ClientPlatform; rides B1's auth). Empirically probe the SmartX REST API beyond B1's performance endpoints — confirm with REAL responses:
      - `reportedmodels/{rmid}/holdings` — holdings GRANULARITY: per-symbol only, or asset-class-tagged? Does classifying them need a security master? (this decides Positioning coverage.)
      - `performance.smartxadvisory.com/models/performance` — does it carry PEER / category-relative data? (decides the Model Portfolios peer-tab coverage — currently uncertain.)
      - `models/{id}/statistics` / `historicalperformance` — risk/return statistic depth (feeds the Factor-Tilts model-return input).
      Reuse the SXPL_RESTIN ROPC-JWT auth (already in 0.4.0's hand from B1) — no parallel pull.

      PART B — surface mapping (0.2.0_DS_PortfolioAnalytics; the deliverable owner). Map the Part-A-confirmed SmartX data onto the WS-2 surfaces — Positioning, Attribution, Factor-Tilts. Per surface: what is directly SmartX-securable, what is hybrid (SmartX input + Opal computation), what is a genuine gap. SPECIFICALLY RESOLVE: can SmartX model holdings + returns feed an AUTOMATED Brinson attribution — replacing the manual `attribution_excel` — with only the policy benchmark + the Brinson math staying Opal? 0.2.0 may begin Part B's surface enumeration + the Brinson framing immediately; integrate Part A's probe results as they land.

      SUB-ITEM — TrueShares ETF-holdings look-through (0.2.0 owns it). SmartX gives top-level model holdings; ETF look-through (what is inside a held ETF) is NOT in SmartX. Scope: does TrueShares (Opal's own ETF issuer) expose constituent holdings, and does third-party ETF look-through need a vendor? Andrew flagged this explicitly.
    </in_scope>
    <out_of_scope>
      - Correlation + Macroeconomics surfaces — SmartX is a managed-accounts platform, not a market-data vendor; it has nothing for those (they stay YCharts / FRED). Do NOT chase SmartX for market data.
      - The YCharts side — TO-C2.
      - Model-portfolio performance — WS-3 / B1 already own that.
      - Any code/Terraform/portal change — audit only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the audit">
      <step>
        <run>comp-pipescript io &lt;each data/smartx gold-tier script the audit touches&gt;</run>
        <expect>Load list + COLUMN GAPS + portal consumers for the SmartX gold-tier scripts — characterize the existing SmartX I/O accurately rather than reading blind.</expect>
        <if_mismatch>If a script is not a comp-pipescript node, fall back to a source read of `data/smartx/` + document.</if_mismatch>
      </step>
      <step>
        <run>comp-routes behaviors  (for the Positioning / Attribution / Factor-Tilts serving paths)</run>
        <expect>The serving paths for the WS-2 surfaces in scope confirmed.</expect>
        <if_mismatch>Document any serving-path delta as an audit finding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>(none) — audit deliverable is a committed brief; no code authored.</run>
        <expect>No code gate applies.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>(none) — the coverage matrix is the deliverable's self-validation.</run>
        <expect>Checked by the acceptance criteria.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Part A (0.4.0_DS_ClientPlatform) reuses the SXPL_RESTIN ROPC-JWT auth — coordinate with the B1 work (same agent, same API); do not stand up a parallel SmartX auth/pull. 0.2.0 (Part B) integrates Part A's probe results — MCP-coordinate the hand-off. SXPL_RESTIN (active, base-lane, COO-owned) is the SmartX REST integration project — consume its knowledge. MDPF_ASSETS (~B-lane): SmartX is a shared source but performance/holdings (this TO) and AUA (MDPF) are orthogonal — no conflict. No shared files written (audit-only).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Part A: `reportedmodels/{rmid}/holdings`, `performance.smartxadvisory.com/models/performance`, `models/{id}/statistics` / `historicalperformance` all probed with REAL responses — holdings granularity, peer/category-relative availability, and statistic depth characterized empirically.</ac>
    <ac id="AC2">Part B: a per-surface coverage map for Positioning / Attribution / Factor-Tilts — each surface classified directly-SmartX-securable / hybrid / genuine-gap, with evidence. The WS-3-era "proprietary"/"Bloomberg-pkl-only" verdicts re-tested against the Part-A findings.</ac>
    <ac id="AC3">The Brinson question answered explicitly: can SmartX model holdings + returns feed an automated Brinson attribution replacing the manual `attribution_excel` (with only the policy benchmark + the Brinson math staying Opal)? Yes/no/hybrid, with the evidence.</ac>
    <ac id="AC4">The TrueShares ETF-holdings look-through sub-item scoped: does TrueShares expose constituent holdings; does third-party ETF look-through need a vendor; named alternative if so.</ac>
    <ac id="AC5">Deliverable: a committed SmartX coverage deep-dive brief, pushed + push-confirmed on origin/CLOUD. Session log with a Compiler Tools section. RAVC2 to 1.0.0_SA_CTO (feeds the v0.4 amendment).</ac>
  </acceptance_criteria>

  <deliverables>
    - The SmartX coverage deep-dive brief (Part A probe results + Part B surface map + the Brinson verdict + the TrueShares look-through scoping).
    - Session log with Compiler Tools section. RAVC2 to 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT chase SmartX for Correlation / Macro market data — SmartX is a managed-accounts platform; those surfaces stay YCharts/FRED.</rule>
    <rule>Do NOT stand up a parallel SmartX auth/pull — Part A reuses the SXPL_RESTIN ROPC-JWT path.</rule>
    <rule>Do NOT author code / Terraform / portal changes — audit only.</rule>
    <rule>No emojis in the brief, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
