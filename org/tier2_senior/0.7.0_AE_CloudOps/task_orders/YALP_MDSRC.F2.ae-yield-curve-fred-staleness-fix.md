<task_order>
  <metadata>
    <id>YALP_MDSRC.F2</id>
    <slug>ae-yield-curve-fred-staleness-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — CTO-recommended (F1 surfaced the defect), COO-issued. 0.7.0_AE_CloudOps queue is empty + lane is live. No gate — this is a standalone infra fix, independent of the YALP migration and of Andrew Q1. Start on receipt.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — a live user-facing data-freshness defect (not the migration). yield_curve_fred.json is ~4 months stale on a user-visible surface; worth fixing ahead of the Phase-2 migration, not waiting for it.</priority>
    <sla>~0.5 effort-day IF it is just a missing/disabled schedule (Phase 0 confirms the actual cause first). Larger only if Phase 0 finds a deeper break.</sla>
  </metadata>

  <references>
    <f1_brief>docs/briefs/mdsrc-fred-macro-sourcing-audit-20260520.md — the F1 FRED macro-sourcing audit (0.2.0_DS~A). It surfaced this defect: yield_curve_fred.json is ~4 months stale with no deployed refresh schedule.</f1_brief>
    <ingest_script>portal/etl/orchestration/green/fred/lambda/fred-data-ingestion/ingest_yield_curve_fred.py — the existing FRED yield-curve ingest Lambda source (in the PORTAL submodule's ETL orchestration tree — note the deploy path is portal-ETL, not infra/aws/terraform; Phase 0 confirms the actual deploy + schedule mechanism).</ingest_script>
    <artifact>yield_curve_fred.json — the stale artifact; feeds the Macroeconomics page Treasury yield curve, including the user-visible "1Y Ago" toggle.</artifact>
  </references>

  <context>
    F1 (the FRED macro-sourcing audit) found that yield_curve_fred.json — a user-visible Macroeconomics-page artifact (the Treasury yield curve + the "1Y Ago" comparison toggle) — is approximately 4 MONTHS STALE, with no deployed refresh schedule. The ingest Lambda source (ingest_yield_curve_fred.py) exists in the portal submodule's ETL orchestration tree, so the code is present; the defect is most likely a missing or disabled refresh schedule (EventBridge rule), not absent code. This is a live data-freshness defect independent of the YALP migration — a user-facing surface should not sit 4 months stale. CTO recommended scoping it as a small immediate infra fix ahead of Phase 2. This TO is that fix. v0.2 of YALP authorized no code change for the migration audits; F2 is a DEFECT FIX, separately authorized here.
  </context>

  <scope>
    <in_scope>
      PHASE 0 (diagnose — confirm the real cause before changing anything):
      - Determine why yield_curve_fred.json is ~4 months stale. Check: is the ingest Lambda deployed; is there an EventBridge (or portal-ETL-orchestration) schedule for it; is the schedule disabled / mis-targeted; or did the ingest itself start failing ~4 months ago (a FRED API change, an auth/key expiry, an error)?
      - Identify the correct deploy + schedule mechanism for this Lambda — it lives in the portal submodule's ETL orchestration (portal/etl/orchestration/green/fred/), which may not be the main-repo infra/aws/terraform path. Document the mechanism before touching it.
      PHASE 1 (fix):
      - Apply the smallest correct fix for the Phase-0 cause: deploy/enable/correct the refresh schedule, or fix the ingest failure. Use the proper deploy mechanism for this Lambda (per Phase 0) — never a console/ad-hoc deploy.
      - Trigger one ingest run; confirm yield_curve_fred.json refreshes to a current date.
      PHASE 2 (verify):
      - Confirm the artifact is current and the schedule will keep it current; confirm the Macroeconomics page "1Y Ago" toggle now has fresh data.
    </in_scope>
    <out_of_scope>
      - The FRED migration itself (the other macro indicators moving to FRED) — that is the FRED implementation TO, separate. F2 fixes ONLY the existing yield-curve ingest's staleness.
      - Re-architecting the FRED ingest — F2 restores the existing mechanism to working order; a rebuild is not in scope unless Phase 0 finds the mechanism is unrecoverable (surface that to COO before expanding scope).
      - The 5 other F1 mechanism findings — they ride into v0.4 / the FRED implementation TO, not F2.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the fix">
      <step>
        <run>comp-iam service on the ingest Lambda (if it is a comp-graph node) + comp-routes trace for the yield_curve_fred.json serving path</run>
        <expect>Confirm the Lambda's IAM (FRED API egress, S3 write) is intact and the artifact's serving path — rule out a permissions/routing cause before assuming a schedule cause.</expect>
        <if_mismatch>If the Lambda is not a comp-graph node (portal-submodule ETL), fall back to a direct read of the portal ETL orchestration config + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before any code commit">
      <step>
        <run>.tools/ds-commit-gate.sh on any .py touched (only if Phase 0 finds an ingest-code fix is needed)</run>
        <expect>If no code change (schedule-only fix), documented-N/A. If code changed, all three gate checks exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after the fix">
      <step>
        <run>verify the ingest run + the refreshed artifact date; if terraform was used, confirm a 0-diff plan post-apply</run>
        <expect>yield_curve_fred.json carries a current date; the schedule is active.</expect>
        <if_mismatch>Re-investigate before signalling done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    The portal submodule has its own DEV/PROD branches — if the fix touches portal-submodule code or config, follow the portal submodule's deploy path, not the main-repo terraform path. If Phase 0 finds the fix needs main-repo Terraform (an EventBridge rule in infra/aws/terraform), that is the standard terraform cycle via safe-apply. Document which path was used. No YALP migration TO depends on F2 — it is a parallel standalone fix.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0: the real cause of the ~4-month staleness identified + documented (missing schedule / disabled schedule / ingest failure / other), with the correct deploy+schedule mechanism for this portal-ETL Lambda characterized.</ac>
    <ac id="AC2">Phase 1: the smallest correct fix applied via the proper deploy mechanism; one ingest run triggered; yield_curve_fred.json confirmed refreshed to a current date.</ac>
    <ac id="AC3">Phase 2: the artifact is current and the schedule will keep it current going forward; the Macroeconomics "1Y Ago" toggle has fresh data.</ac>
    <ac id="AC4">Committed + pushed/deployed via the proper mechanism (push-confirmed on origin/CLOUD or the portal submodule branch as applicable). Session log with the Compiler Tools section + the Phase-0 cause + the deploy mechanism used.</ac>
    <ac id="AC5">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The diagnosed cause + the applied fix; yield_curve_fred.json refreshed + a working refresh schedule.
    - Session log with the Compiler Tools section, the Phase-0 cause, and the deploy mechanism used.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT deploy via console or aws lambda update-function-code — use the proper deploy mechanism for this Lambda (Phase 0 identifies it: portal-ETL orchestration path or main-repo terraform).</rule>
    <rule>Do NOT expand into re-architecting the FRED ingest or the broader FRED migration — F2 is the staleness fix only; surface to COO if Phase 0 finds the mechanism unrecoverable.</rule>
    <rule>Do NOT handle the FRED API key in chat / MCP / git / logs — reference it by its secret name only.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
