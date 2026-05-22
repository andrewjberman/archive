<task_order>
  <metadata>
    <id>YALP_MDSRC.B1</id>
    <slug>ds-smartx-rest-model-portfolio-performance-pull</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO FIRED 2026-05-20 — PRD v0.3 confirmed on origin/CLOUD (de7facf93 + c3c04bc9d); COO flipped pending + dispatched. Original: STAGED — Phase 2B. Q1-INDEPENDENT (SmartX REST is an official key-authed API, an active Opal integration — not gated on the YCharts Q1 decision; dispatchable on COO decomposition per PRD v0.3 §7/§12). COO flips status->pending + fires the GO once PRD v0.3 (de7facf93) is confirmed on origin/CLOUD. NOTE: Q8 (portal shows realized SmartX returns vs design model.pkl returns) is a product call that gates ONLY the portal-wiring step (Phase 2 of the scope below) — the SmartX pull build + validation (Phase 0/1) proceed without it; surface for Andrew's Q8 ruling before wiring portal columns.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2B. A source UPGRADE (manual weekly model.pkl -> daily SmartX-REST) for the portal's model-portfolio performance surfaces. Runs in parallel with Phase 2A/2C.</priority>
    <sla>~3-5 days (PRD §7).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. This TO = §7 Phase 2B TO-B1. Read §5.2 (surfaces WS3-MP-01 / WS3-MP-02), §5.3 (the WS-2/WS-3 column seam), §6.2 (SmartX REST = Q4 canonical source).</prd>
    <ws3_brief>docs/briefs/mdsrc-ws3-client-facing-data-audit-20260520.md (corrected f963b8727) — the WS-3 audit; the SmartX REST endpoint characterization.</ws3_brief>
    <sxpl_restin>SXPL_RESTIN (active, base-lane, COO-owned) — the SmartX REST ingestion project. SXPL_RESTIN.001 (0.4.0_DS_ClientPlatform — per-model availability assessment) + SXPL_RESTIN.002 (0.5.0_AE_OpalETL — SmartX REST pull flow). TO-B1 REUSES SXPL_RESTIN's SmartX ROPC-JWT auth path — see cross_domain_coordination.</sxpl_restin>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 §6.2 / Q4: the portal's model-portfolio PERFORMANCE surfaces (the `model` / `model_return` columns of `model_portfolio_benchmarks.json` + `model_portfolio_timeseries.json` — surfaces WS3-MP-01/02) should move off the manual weekly yang `model.pkl` to the SmartX REST API — a daily-automatable, machine-API-authed (ROPC JWT) performance feed for the Opal models. `model.pkl` is RETAINED as the Opal-proprietary *design* view. This is a Q1-independent source upgrade. You owned the WS-3 audit — you know the SmartX REST surface.
  </context>

  <scope>
    <scope_split note="COO routing ruling 2026-05-20 — B1 / B2 split (UPDATED)">
      BOTH B1 build artifacts are AE-lane infra/aws/lambda code — DS 0.4.0 authors + verifies, AE commits + deploys (CLAUDE.md Rule 1; the DS commit carve-out Rule 13 is `data/*/scripts/{gold,silver,bronze}/*.py` only). The COO's earlier "yang Lambda = your ClientPlatform lane" framing was WRONG — all of infra/aws/lambda/ is AE lane (CLOUD_OPS_OR_ETL); DS 0.4.0 correctly caught it. Both artifacts split to YALP_MDSRC.B2 (0.5.0_AE_OpalETL):
        - Artifact 1: data/smartx/scripts/pull_smartx_model_monthly_performance.py (SHARED_OPAL_ETL).
        - Artifact 2: infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py (CLOUD_OPS_OR_ETL).
      DS 0.4.0 BUILT + VERIFIED both (gate-clean; pull dry-run + YTD cross-check 0.002pp; yang dual-source override logic tested vs a synthetic sidecar). B1 (this TO, DS 0.4.0) is now honestly scoped to: author + verify the two code artifacts (DONE); write the AE hand-off brief; coordinate the sidecar S3 path/shape with B2; run the end-to-end model_portfolio_benchmarks.json verification once B2 deploys both Lambdas; RAVC2. B1's build work is complete — the remaining active B1 work is the hand-off brief + the post-deploy end-to-end verification.
    </scope_split>
    <in_scope>
      Phase 0 (verify-first): confirm against REAL SmartX REST data — `reportedmodels/{rmid}/historicalperformance` cadence + the `performanceValue` units/semantics, and `models/{id}/statistics` — before building. Surface any data-shape surprise.
      Phase 1 (build) — PATH A, RULED 2026-05-20 (CTO+COO converged on the B1 Phase-0 finding that SmartX model-perf is monthly-cadence; the originally-stated daily pull of historicalperformance/statistics is SUPERSEDED — those endpoints are stale/buggy). HYBRID BY CADENCE:
        - Build a MONTHLY pull of SmartX `performance/models/performance` for the 5 portal models -> feed the 7 monthly+ periods (1M / MTD / QTD / 1Q / YTD / 1Y / SI) of `model_portfolio_benchmarks.json`'s `model` column.
        - model.pkl is RETAINED as the source for the DAILY periods (1D / WTD) + the daily `model_portfolio_timeseries.json` — NOT re-sourced. No cadence downgrade.
        - REUSE the SmartX ROPC-JWT auth as CODE reuse — import the `mint_token` helper, point at the `smartx/credentials` secret. B1 is a STANDALONE SIBLING, not a ride on SXPL_RESTIN.002 — NOT gated on the .002 coordination or its owner.
        - MANDATORY (Q8 nuance): Path A splits the `model` column by KIND — monthly periods = SmartX *realized* return; daily periods = model.pkl *design* return. LABEL / document the cadence-source split EXPLICITLY in the artifact so the realized-vs-design boundary is visible, not silent. The Q8 realized-vs-design product call is now period-dependent (folds into v0.4) — the BUILD proceeds with the explicit labeling; the portal-wiring step still waits on Andrew's Q8.
        Per PRD §5.3 model_portfolio_benchmarks.json becomes a dual-sourced producer (benchmark columns from the future YCharts pull, the monthly model periods from this SmartX pull) — either split the artifact or build a dual-input producer; make + document the call.
      Phase 2 (portal wiring) — GATED on Andrew Q8: wire the SmartX-sourced model columns into the portal. Q8 (portal shows realized SmartX returns vs design model.pkl returns vs both) is a product decision; a one-time level shift is expected on the source switch. Do NOT wire portal columns until Q8 is ruled — surface it to COO.
    </in_scope>
    <out_of_scope>
      - The YCharts side (benchmark columns, market data) — Phase 2C (TO-C2).
      - Retiring model.pkl — it is RETAINED as the design view; only the performance columns re-source.
      - Standing up a parallel SmartX auth/pull — reuse SXPL_RESTIN's.
      - The Q8 product decision itself — surface it; Andrew rules.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before commit / before the build">
      <step>
        <run>comp-pipescript io &lt;each gold/producer script touched&gt;</run>
        <expect>Load list + COLUMN GAPS + portal consumers for the model_portfolio_benchmarks / model_portfolio_timeseries producer(s) — so the dual-source column change is scoped against the real consumer set.</expect>
        <if_mismatch>If a script is not a comp-pipescript node, fall back to a source read + document.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service &lt;the SmartX-pull lambda/runner&gt;</run>
        <expect>The current IAM surface for the SmartX REST + Secrets Manager boto3 calls — confirm the SXPL_RESTIN-reused auth path's grants cover this pull; flag any gap.</expect>
        <if_mismatch>If a new boto3 call needs a grant, scope it minimally in iam.tf and re-check at Phase 2.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after any iam.tf change">
      <step>
        <run>comp-iam gaps</run>
        <expect>0 new IAM gaps from the SmartX-pull change.</expect>
        <if_mismatch>Resolve the flagged gap in iam.tf before deploy.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast &lt;the changed model_portfolio_* producer function&gt;</run>
        <expect>The downstream consumers of the model_portfolio_benchmarks / model_portfolio_timeseries artifacts — confirm the dual-source change does not silently break a consumer.</expect>
        <if_mismatch>If a new/unexpected downstream node appears, flag to COO before signalling done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SXPL_RESTIN (active, base-lane, COO-owned) — TO-B1 co-scopes with it. MANDATORY: REUSE SXPL_RESTIN's SmartX ROPC-JWT auth + Secrets Manager path; do NOT stand up a parallel SmartX pull. Coordinate with the SXPL_RESTIN.002 owner (0.5.0_AE_OpalETL — the SmartX REST pull-flow TO) on the shared auth path + whether the model-performance pull rides the SXPL_RESTIN pull flow or is a sibling. Both projects are base-lane / 2.0.0_SA_COO — an internal coordination, no cross-suite thread; MCP the SXPL_RESTIN.002 owner and cite this TO.
    MDPF_ASSETS (~B-lane): SmartX is a shared source but performance (this TO) and AUA (MDPF) are orthogonal SmartX dimensions — no conflict (WS-3 confirmed). No coordination needed beyond awareness.
    WS-2/WS-3 Model Portfolios seam (PRD §5.3): the benchmark columns of the same two artifacts are TO-C2's (YCharts). Coordinate the dual-sourced-producer shape with TO-C2 when it dispatches.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0: `historicalperformance` cadence + `performanceValue` units + `models/{id}/statistics` confirmed against real SmartX REST data; any data-shape surprise surfaced before the build.</ac>
    <ac id="AC2">Daily pull of `historicalperformance` / `statistics` for the 5 portal models implemented, reusing SXPL_RESTIN's ROPC-JWT auth (evidence of the SXPL_RESTIN.002 coordination — MCP thread or cited brief).</ac>
    <ac id="AC3">The `model` / `model_return` columns of `model_portfolio_benchmarks.json` + `model_portfolio_timeseries.json` sourced from the SmartX pull; the dual-sourced-producer call (split artifacts vs dual-input producer) made + documented per PRD §5.3.</ac>
    <ac id="AC4">Compiler mandate runs reproduced in the session log (comp-pipescript io, comp-iam service/gaps, comp-blast) + observed result vs expect. CLAUDE.md Rule 14 pre-commit gate on any .py.</ac>
    <ac id="AC5">Portal-wiring step (Phase 2) NOT executed until Andrew Q8 is ruled — Q8 surfaced to COO. The pull + validation (Phase 0/1) may complete without it.</ac>
    <ac id="AC6">Deliverable committed + pushed to origin/CLOUD (push-confirmed — ship-attested != deploy-attested). Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The SmartX-REST model-portfolio-performance daily pull, feeding the model columns of the two model_portfolio artifacts.
    - Phase-0 data-shape confirmation note.
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT stand up a parallel SmartX auth/pull — reuse SXPL_RESTIN's ROPC-JWT path.</rule>
    <rule>Do NOT wire the portal model columns before Andrew's Q8 ruling — surface Q8, hold the wiring step.</rule>
    <rule>Do NOT retire model.pkl — it is retained as the proprietary design view; only the performance columns re-source.</rule>
    <rule>DS owns commit + push + gold-script S3 upload + QA-runner SSM dispatch; PROD triggers route to AE (CLAUDE.md Rule 13).</rule>
    <rule>No emojis in code, briefs, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
