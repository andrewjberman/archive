<task_order>
  <metadata>
    <id>POSN_CUSTOM.001-RD</id>
    <slug>custom-blend-state-and-positioning-summary-column</slug>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.2.1_RD_Positioning</issued_to>
    <date>2026-07-10</date>
    <status>staged</status>
    <project_code>POSN_CUSTOM</project_code>
    <priority>P1 -- Andrew-direct 2026-07-10 ("SSCN_PFOE and POSN_CUSTOM are priorities now, go and proceed them"). GO is LIVE. Begin immediately on spawn. Both Cottonwood AND Inflection want this.</priority>
  </metadata>

  <references>
    <prd>docs/architecture/POSN_CUSTOM.md -- PRD v0.1 (1.0.0_SA_CTO~C, @ e010d37b3). READ IT -- esp. sec.2 (existing state + the no-shared-state seam), sec.3 (architecture + weighted-avg contract + Mode-B solve), sec.4.1/4.2/4.4 (component specs), sec.6 TO-1 (this TO's authority), sec.7 (OQs -- all build defaults resolved).</prd>
    <arch_gate>1.0.0_SA_CTO~C arch-gates your build diff. RAVC back to CTO~C (via COO~C). Do NOT self-close.</arch_gate>
    <baseline>Positioning page (portal/src/pages/Positioning/). Data is SOVEREIGN-CLEAN -- Yang Bloomberg model PKL -> generate_positioning_json.py -> positioning_data.json (Opal model data, NOT bd/49F/Schwab custody). FE-only over already-served data.</baseline>
  </references>

  <context>
    Advisors want a client-specific CUSTOM blend of Opal's 5 model portfolios (UST/ST/INT/LTC/LTA) -- today a manual per-row calculator. This TO adds a 6th "Custom" column/bar to the Positioning Summary driven by advisor-entered weights, recomputed client-side as a weighted average of the 5 models (Andrew: "the logic is already there, it just needs a new UI element"). The ONE real architectural change: lift the custom-blend state to Positioning.tsx so the top summary bar can later drive the bottom HoldingsTab CSM view (POSN_CUSTOM.002) -- they have NO shared state today (PRD sec.2). Persistence across sessions is explicitly OUT OF SCOPE (Andrew+Yang deferred; reset-on-login is fine for now).
  </context>

  <scope>
    Files (all under portal/src/pages/Positioning/):
    1. Positioning.tsx -- LIFT the shared custom-blend state:
         { active: boolean, inputMode: 'weights'|'targetEquity',
           weights: Record<ModelId, number>, targetEquity: number }
       Ephemeral (not persisted). Thread via props or a Positioning-scoped context (your call; keep it local to the page). This is the state POSN_CUSTOM.002 (HoldingsTab CSM) will read.
    2. panels/PositioningSummary.tsx -- the Custom column + dual-input + guardrails:
       - generateSections appends one value per row = weighted average of the 5 models' values IN THE ACTIVE VIEW MODE (portfolio / benchmark / relative). custom[m] = Sum_i w_i * model_i[m](v), weights normalized to 1.
       - Bar section renders a 6th stacked bar from the blended equity/FI.
       - Mode A (model weights): advisor allocates 100% across the 5 models -> weighted-avg blend.
       - Mode B (target equity): advisor enters a target equity % -> interpolate implied model weights
         against the BENCHMARK equity anchors (portfolio.benchmark.allocation.equity, already served, so
         market drift does not move the target). Levers = ST<->INT (PRD sec.7 Q1 default; the other 3 = 0
         in Mode B). CONFIRM the exact lever rule with Yang mid-build -- a contained calc, NOT a start gate;
         build the rest of the column against Mode A first.
       - Guardrails: live Sum weights; if != 100 -> red + inline warning, custom column renders "--" until
         valid (recompute ONLY at Sum=100; no auto-normalize).
    3. shared/gridConfig.ts -- add the 6th (Custom) column to PORTFOLIO_GRID_TEMPLATE + PORTFOLIO_NAMES;
       widen PositioningSummary totalColumns (6->7 incl. label). Grep every 5/6-column assumption
       (PORTFOLIO_GRID_TEMPLATE|PORTFOLIO_NAMES|totalColumns) and verify no hardcoded index cap in
       renderRow/renderContent breaks when row.values length becomes 6.

    A model missing from positioningData -> treat as weight 0 with a SURFACED note; do NOT silently drop
    (silent drop makes the blend sum <100 of intended exposure). AGG and the 5 existing model columns
    stay unchanged.
  </scope>

  <compiler_tools_mandate>
    <phase_1_before_write>comp-transform schema-check PositioningSummary; grep PORTFOLIO_GRID_TEMPLATE|PORTFOLIO_NAMES|totalColumns for every 5/6-column assumption; confirm benchmark equity anchors (portfolio.benchmark.allocation.equity) present in served data for Mode B.</phase_1_before_write>
    <phase_2_before_commit>comp-cache collisions (0 new key); comp-transform schema-check Positioning PositioningSummary (stay clean); bun run typecheck + bun run lint -- both exit 0, transcript in session log.</phase_2_before_commit>
    <phase_3_after_commit>DEV smoke -- Mode A (enter 30/70 ST/INT -> custom bar + all matrix rows = weighted avg; Sum != 100 -> red + no compute); Mode B (target 50% -> implied weights populate + blend recomputes); view-mode toggle applies to the custom column.</phase_3_after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>  <!-- PRD Appendix D: files touched (Positioning.tsx, PositioningSummary.tsx, gridConfig.ts) all under portal/src/pages/Positioning/, owned by POSN_CUSTOM. comp-cache clean; no new query key (reuses ['positioning-data']). No shared files/S3 keys with any other active project. NOTE: POSN_CUSTOM.002 (HoldingsTab CSM) reads the state THIS TO lifts -- same-project sequence, not cross-domain. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Custom column present as the 6th (rightmost) column in bars + matrix; toggling the view mode (portfolio/benchmark/relative) recomputes it as the weighted avg in that mode.</ac>
    <ac id="AC2">Sum weights = 100 enforced: <100 or >100 shows warning + red and the custom column renders "--"; exactly 100 computes.</ac>
    <ac id="AC3">For a hand-checked weight vector, each matrix row's custom value equals Sum w_i*model_i within display rounding.</ac>
    <ac id="AC4">Mode B: entering target equity T yields weights whose blended benchmark equity = T (+/- rounding).</ac>
    <ac id="AC5">bun run typecheck + bun run lint both exit 0 (transcript in session log). /frontend-dev smoke green (DE runs it). AGG + the 5 existing model columns byte-unchanged.</ac>
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT persist the custom blend across sessions / scope it to a user profile -- explicitly deferred (Andrew+Yang). Ephemeral page state only.</rule>
    <rule>Do NOT change the 5 model definitions, the served data, or the AGG view. Do NOT add a 6th real model or trade generation.</rule>
    <rule>Do NOT let the Mode-B lever rule block the TO -- Mode A is fully specified; build against it, confirm Mode-B's ST<->INT interpolation with Yang mid-build.</rule>
    <rule>Do NOT commit or push to PROD. Build on portal DEV; hand to 0.2.0_DE_PortfolioAnalytics for compiler mandate + review + commit; 0.2.0_DT owns the DEV->PROD promote.</rule>
    <rule>No emojis / non-ASCII in code or the session log.</rule>
  </do_not>

  <deliverables>
    - The state-lift + PositioningSummary custom column/bar/dual-input/guardrails + gridConfig widening on the portal DEV working tree.
    - bun run typecheck + bun run lint both exit 0; transcript in your session log.
    - Session log under org/tier3_junior/0.2.1_RD_Positioning/logs/2026-07-10/ (Compiler Tools section mandatory).
    - MCP 0.2.0_DE_PortfolioAnalytics when ready for DE review + compiler mandate + commit.
  </deliverables>

  <handback>
    When done: MCP 0.2.0_DE_PortfolioAnalytics "POSN_CUSTOM.001 RD implementation ready" + files changed + typecheck/lint result. DE runs the 3-phase compiler mandate, reviews vs all 5 ACs, commits; the build diff routes to 1.0.0_SA_CTO~C for arch-gate; RAVC to COO~C. POSN_CUSTOM.002 (HoldingsTab CSM) activates once THIS TO's lifted state lands. Do NOT flip this TO to complete yourself.
  </handback>
</task_order>

<!-- ZOMBIE-RESOLVED 2026-07-13T08:04Z by 2.0.0_SA_COO.
     This TO was <status>pending</status> -- which means DISPATCHED -- while its assignee was
     NOT REGISTERED. Nobody was there. The board read it as ACTIVE work in flight.
     Flipped pending -> staged: `staged` is the TRUE state (scoped, awaiting a GO when a live
     lane exists). NOT flipped to complete -- THE WORK WAS NEVER DONE.
     Detector: .tools/to-liveness-join.py (e8ed4e1d2) -- the join /to-check and fabric-check
     never made. A dispatch into an unverified lane is a hope, not a drive. -->
