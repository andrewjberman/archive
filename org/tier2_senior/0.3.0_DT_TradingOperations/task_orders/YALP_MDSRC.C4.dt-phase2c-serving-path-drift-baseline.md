<task_order>
  <metadata>
    <id>YALP_MDSRC.C4</id>
    <slug>dt-phase2c-serving-path-drift-baseline</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — CTO stimulus-scan recommendation, COO-issued. DT lane is clear (SSCN_DIVDEF closed, no active Pod-3 project). A3/Q1-independent — a current-state baseline. Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P3 — preparatory. Not on any TO's critical path; it establishes a known-state baseline so the Phase-2C YCharts-pull migration's routing work starts from documented ground rather than discovering drift mid-cutover.</priority>
    <sla>~0.5-1 effort-day — a comp-routes-driven baseline capture; no code change.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3.2. Phase 2C is the YCharts market-data pull migration (TO-C2); it re-sources the artifacts behind the Macroeconomics / market-data serving paths.</prd>
    <c2>YALP_MDSRC.C2 — the YCharts market-data pull. Its migration will touch the CloudFront routing for the artifacts it re-sources; C4 baselines that routing surface beforehand.</c2>
  </references>

  <context>
    The Phase-2C YCharts-pull migration (C2) will re-source the artifacts behind the portal's market-data / macro serving paths — the /api/general/* and /json-tiered/* CloudFront routes. Before that migration touches routing, a documented current-state baseline of those routes prevents the migration from discovering routing drift mid-cutover. DT's lane is clear; this is a useful, bounded, A3-independent preparatory audit. Audit only — no code or infrastructure change.
  </context>

  <scope>
    <in_scope>
      - Run comp-routes behaviors and capture the current CloudFront routing for the /api/general/* and /json-tiered/* path families — the routes, their origins, any custom_error_response rules, cache behaviors, and the artifacts each path serves.
      - Identify which of those serving paths correspond to the market-data / macro artifacts the C2 YCharts-pull migration will re-source (cross-reference the PRD §5.2 surface list).
      - Note any drift or surprise in the current routing (a path with an unexpected origin, a stale custom error rule, a behavior inconsistent with the documented design) — flag each as a baseline finding for the Phase-2C work to account for.
      Deliverable: a Phase-2C serving-path drift baseline — the documented current state of the routes C2 will touch, with any drift flagged.
    </in_scope>
    <out_of_scope>
      - Any routing / CloudFront / code change — C4 is a read-only baseline; the migration is C2/D1.
      - Non-market-data serving paths — only the /api/general/* + /json-tiered/* families C2 touches.
      - Fixing any drift found — flag it as a baseline finding; remediation is the migration's or a separate TO's call.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before">
      <step>
        <run>comp-routes behaviors</run>
        <expect>The CloudFront custom_error_response rules + behaviors for the /api/general/* + /json-tiered/* families — the baseline's primary evidence.</expect>
        <if_mismatch>Document any comp-routes gap as a baseline finding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit"><step><run>(none) — baseline doc, no code.</run><expect>No code gate applies.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
    <phase id="3" when="after commit"><step><run>(none) — the baseline doc is its own deliverable.</run><expect>Checked by the ACs.</expect><if_mismatch>N/A.</if_mismatch></step></phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    C4's baseline feeds the Phase-2C migration (C2, then D1 the yang cutover). Hand the baseline to C2/D1 when they reach the routing step. No shared files written (audit-only). If C4 surfaces a live routing defect (not just drift to note), surface it to COO immediately rather than burying it in the baseline.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The current CloudFront routing for /api/general/* + /json-tiered/* captured via comp-routes behaviors — routes, origins, custom_error_response rules, cache behaviors, artifacts served.</ac>
    <ac id="AC2">The serving paths corresponding to the C2-migrated market-data / macro artifacts identified (cross-referenced to PRD §5.2); any routing drift or surprise flagged as a baseline finding.</ac>
    <ac id="AC3">Deliverable: a committed Phase-2C serving-path drift baseline doc, pushed + push-confirmed on origin/CLOUD. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Phase-2C serving-path drift baseline doc (committed, push-confirmed).
    - Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT change any routing / CloudFront config — C4 is a read-only baseline.</rule>
    <rule>Do NOT fix drift found — flag it; remediation is the migration's call. But a LIVE defect (not drift) surfaces to COO immediately.</rule>
    <rule>No emojis in the baseline doc, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
