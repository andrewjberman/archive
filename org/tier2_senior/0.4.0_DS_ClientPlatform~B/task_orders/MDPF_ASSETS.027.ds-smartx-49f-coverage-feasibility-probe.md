<task_order>
  <metadata>
    <id>MDPF_ASSETS.027</id>
    <slug>ds-smartx-49f-coverage-feasibility-probe</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20 (authored on Andrew Mandate Change 3 via CTO~B)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- GATING. Andrew changed the 49F basis a 3rd time (Mandate Change 3, 2026-05-20): Cohort 1 (49F) = ONLY what SmartX covers (~$1.65B), superseding the v0.7 full-Black-Diamond-book basis (~$1.81B certified_aua). This probe is the gating feasibility question -- its outcome determines whether the re-scope uses a SmartX-direct mechanism (Andrew's preference) or a Schwab-based fallback, and CTO~B's PRD v0.9 amendment + the .024/.025/.016/.026 re-scope TOs all wait on the findings brief.</priority>
    <sla>~2-4h DS wall -- a non-mutating feasibility investigation, not a build.</sla>
    <deadline>Prompt -- it gates the PRD v0.9 amendment + the MDPF 49F re-scope. Not a forced timeline, but it is the critical-path item.</deadline>
  </metadata>

  <references>
    <origin>Andrew Mandate Change 3, 2026-05-20, relayed via 1.0.0_SA_CTO~B. New 49F mandate: Cohort 1 (49F) = ONLY what SmartX covers. SmartX-covered 1a+1b+1c ~= $1.65B (~= the Schwab 49F figure). Cohort 0 still excluded; Cohort 2 = 2a (Eclipse Inflection model) only. Headline = 49F SmartX-covered (~$1.65B) + 2a (~$93.6M) ~= $1.75B. This SUPERSEDES the v0.7/v0.8 full-BD-book basis.</origin>
    <basis_history>49F basis has now changed 3 times: (1) original Schwab-only ~$1.655B; (2) Ruling 2 / PRD v0.7 = full Black Diamond book certified_aua ~$1.81B; (3) Mandate Change 3 = SmartX-covered ~$1.65B. The .024 (aggregator) / .025 (WS-E) / .016 (backfill) builds + the .026 legacy-emit TO were all built on basis (2) -- they will need rework to basis (3); CTO~B holds that rework pending this probe + PRD v0.9.</basis_history>
    <wsb_feeder>data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py -- the WS-B feeder already pulls 1a (model) + 1c (SMA) from the SmartX enterprises/allocations endpoint. 1b (non-model) is the unknown this probe must resolve.</wsb_feeder>
  </references>

  <context>
    Under Mandate Change 3 the 49F headline source becomes "what SmartX covers" rather than the full Black Diamond book. The WS-B feeder already extracts 1a (49F model AUA) and 1c (SMA) from SmartX. The open question is 1b (49F NON-model AUA): does SmartX expose non-model assets WITHIN its covered 49F book, and can a CLEAN 1b be derived directly from SmartX -- or must 1b still come from a Schwab residual? The answer determines both the mechanism and the arithmetic of the re-scoped headline.
  </context>

  <scope>
    <step>Phase 0 -- NON-MUTATING PROBE. No code ships, no artifact is written, no S3 deploy. Investigate the SmartX API surface (and the existing WS-B feeder's use of it) to answer:
      Q1 -- Can SmartX directly yield 49F's 1a + 1b + 1c summing to ~$1.65B? Specifically: does SmartX expose 49F NON-model (1b) assets within its covered book, and can a clean 1b be read directly?
      Q2 -- Does SmartX expose 1a / 1b / 1c as DISJOINT buckets (-> the headline arithmetic is additive 1a + 1b + 1c) OR is 1b still a residual (-> 1c is a subset of 1b, the v0.8 nesting where 1b is SMA-inclusive)? This determines the re-scoped headline formula.
      Q3 -- Empirically: what does SmartX-covered 1a + 1b + 1c actually sum to on a recent date? Does it land at ~$1.65B (the mandate's expectation)?
      Q4 -- If SmartX cannot yield a clean 1b: characterize the Schwab-based fallback (mechanism = the existing partner_custody_total / WS-E residual path against the Schwab book).</step>
    <step>Phase 0 deliverable -- a findings brief at docs/briefs/ recording Q1-Q4 with empirical figures, and a clear OUTCOME recommendation: (a) SmartX-direct mechanism (Andrew's stated preference) or (b) Schwab-based fallback. Route the brief to 1.0.0_SA_CTO~B (CC 2.0.0_SA_COO~B). CTO~B uses it to author the PRD v0.9 amendment + the re-scoped .024/.025/.016/.026 TOs.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Q1-Q4 answered with empirical figures (not inferred) -- a real SmartX read on a recent date.</ac>
    <ac id="AC2">The disjoint-vs-residual question (Q2) resolved definitively -- it determines the re-scoped headline arithmetic.</ac>
    <ac id="AC3">A clear OUTCOME: (a) SmartX-direct or (b) Schwab fallback, with the mechanism characterized either way.</ac>
    <ac id="AC4">Findings brief at docs/briefs/, routed to CTO~B (CC COO~B). Non-mutating -- no code, no artifact, no deploy.</ac>
  </acceptance_criteria>

  <out_of_scope>
    Re-scoping / re-writing .024 / .025 / .016 / .026 -- HELD pending this probe + CTO~B's PRD v0.9 amendment + re-scoped TOs. Do NOT reopen those scripts. This TO is the feasibility probe ONLY. The pipeline is parameterized (the 49F-total SOURCE is the variable) so the eventual rework is a code change, not a rebuild -- but it waits on the probe.
  </out_of_scope>

  <deliverables>
    - Findings brief (docs/briefs/) answering Q1-Q4 + the (a)/(b) outcome recommendation, routed to CTO~B CC COO~B.
  </deliverables>
</task_order>
