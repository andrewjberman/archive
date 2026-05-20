<task_order>
  <metadata>
    <id>YALP_MDSRC.D1</id>
    <slug>ae-yang-pipeline-per-surface-cutover</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <co_owner>A DS partner for the per-surface diff validation (0.1.0_DS / 0.2.0_DS per the surface domain) — COO finalizes at dispatch.</co_owner>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED — Phase 2D. GATED on Phase 2C complete (TO-C1 credential pipeline + TO-C2 market-data pull both RAVC-complete) — there is nothing to cut over to until the YCharts pull exists. COO flips status->pending + fires the GO on TO-C1 + TO-C2 close. Requires PRD v0.3 on origin/CLOUD.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2D. The final step — switches portal surfaces off the Bloomberg data_pkl onto the YCharts pull, behind a parallel-run diff gate.</priority>
    <sla>~3-5 days (PRD §7).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. This TO = §7 Phase 2D TO-D1. Read §5.2 (the migration matrix — the 17 YCharts-touched surfaces), §2.1 (the yang-pipeline manifest).</prd>
    <valgate>ADHC_VALGATE — the Class-C baseline-comparison discipline; TO-D1's per-surface parallel-run diff gate REUSES it (PRD §9), does not invent a new one.</valgate>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 §7 Phase 2D — the cutover. Once the YCharts pull exists (TO-C2) and authenticates (TO-C1), switch each migrated surface from the Bloomberg `data_pkl` path to the YCharts pull — ONE surface at a time, behind a parallel-run diff gate (YCharts value vs Bloomberg-pkl value, within tolerance, before cutover). On completion the yang `manifest.json` shrinks to `model_pkl` + the Excel workbooks only — the `data_pkl` dependency retires for the 17 YCharts-touched surfaces.
  </context>

  <scope>
    <in_scope>
      - Per-surface cutover: switch each of the 17 YCharts-touched surfaces (7 replaceable + 10 hybrid input legs) from the `data_pkl` path to the YCharts pull, ONE surface at a time.
      - Parallel-run diff gate per surface: before cutting a surface over, run the YCharts-pull value against the live Bloomberg-pkl value, confirm within tolerance. REUSE the ADHC_VALGATE Class-C baseline-comparison discipline (PRD §9) — do not invent a new gate. A surface only cuts over after its diff gate passes.
      - On all surfaces cut over: shrink the yang `manifest.json` to `model_pkl` + the Excel workbooks (`cma_excel` / `peer_excel` / `attribution_excel` / `saa_excel`) — the `data_pkl` field retires.
      - Fold in the doc-hygiene fixes: the stale SFN reference `yang-generate-benchmark-returns` (no source dir; real producer is `yang-model-portfolio-benchmarks` — WS-2 §6.4-1) and the undeclared `saa_excel` manifest field (WS-2 §6.4 / PRD §11).
    </in_scope>
    <out_of_scope>
      - The YCharts pull build — TO-C2. The credential pipeline — TO-C1. The SmartX model-perf pull — TO-B1.
      - The proprietary / Bloomberg-pkl-only surfaces (model_pkl, the workbooks) — they STAY on the manual pkl path; not cut over.
      - Any portal-component logic change — sources change, page logic does not (unless an artifact shape changes — then per-page DE/RD coordination).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before each cutover">
      <step>
        <run>comp-blast &lt;each changed generator/artifact&gt;</run>
        <expect>The full downstream consumer set of the surface being cut over — so the source switch does not silently break a consumer.</expect>
        <if_mismatch>If an unexpected downstream node appears, hold the cutover + RAVC1 COO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after each cutover">
      <step>
        <run>comp-routes behaviors</run>
        <expect>Serving paths unchanged by the source switch — the cutover changes the data source, not the route.</expect>
        <if_mismatch>If a serving path moved, RAVC2 COO before proceeding to the next surface.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after all cutovers">
      <step>
        <run>comp-pipescript io  on the shrunk yang manifest producers  +  parallel-run diff-gate evidence per surface</run>
        <expect>Every cut surface passed its diff gate within tolerance; the manifest no longer requires `data_pkl`.</expect>
        <if_mismatch>Any surface failing its diff gate does NOT cut over — surface the discrepancy to COO (that is the gate's purpose).</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Gated on TO-C1 + TO-C2 (Phase 2C). REUSES the ADHC_VALGATE Class-C baseline-comparison discipline for the diff gate. A DS partner runs the per-surface diff validation (domain-matched: 0.1.0_DS for WS-1 surfaces, 0.2.0_DS for WS-2). Portal DE/RD (Pods 1+2): if a cut surface's artifact shape changes, per-page coordination — enumerate it. yang-pipeline is 0.5.0_AE_OpalETL's lane — audit + cutover in one lane.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Each of the 17 YCharts-touched surfaces cut over one at a time, EACH behind a passing parallel-run diff gate (YCharts vs Bloomberg-pkl within tolerance) reusing the ADHC_VALGATE Class-C discipline. Per-surface diff evidence in the session log.</ac>
    <ac id="AC2">The yang `manifest.json` shrunk to `model_pkl` + the Excel workbooks — the `data_pkl` field retired; the proprietary/Bloomberg-pkl-only surfaces still served from the manual path.</ac>
    <ac id="AC3">Doc-hygiene fixes folded in: the stale `yang-generate-benchmark-returns` SFN reference corrected to `yang-model-portfolio-benchmarks`; the `saa_excel` manifest field declared in PORTAL_DATA_FLOW.md.</ac>
    <ac id="AC4">comp-blast / comp-routes / comp-pipescript runs reproduced in the session log. Deploy per the standard cycle. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The 17-surface cutover (each diff-gated); the shrunk yang manifest; the two doc-hygiene fixes.
    - Session log with Compiler Tools section + per-surface diff-gate evidence. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT start before TO-C1 + TO-C2 are RAVC-complete — there is nothing to cut over to without the YCharts pull.</rule>
    <rule>Do NOT cut a surface over without its parallel-run diff gate passing — a failing diff HOLDS that surface + surfaces the discrepancy (that is the gate's purpose, per PRD §11).</rule>
    <rule>Do NOT cut over the proprietary / Bloomberg-pkl-only surfaces — they stay on the manual pkl path.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
