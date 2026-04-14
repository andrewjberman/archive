<task_order>
  <metadata>
    <id>0.4.0_DT_ClientPlatform-2026-04-13-office-w4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>staged</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_OFFICE_PRD.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_OFFICE.W3.de-ofc-frontend"
                status="pending"
                description="DE frontend OFC changes complete on portal DEV; TypeScript build clean."/>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_OFFICE.W2.ae-dim-upload-gold-run"
                status="pending"
                description="AE QA gold run complete — OFC artifact live in platinum/ (QA runner writes directly to production S3; no separate PROD trigger step)."/>
  </dependencies>

  <objective>
    Push portal DEV → PROD with the ADVI_OFFICE OFC frontend changes. Verify OFC toggle
    is functional end-to-end against the live PROD platinum artifact.
  </objective>

  <context>
    Standard portal DEV → PROD deploy. Confirm that:
    - DE W3 commit is the HEAD of portal DEV branch.
    - AE W2 PROD gold run has completed and platinum artifacts contain `views.ofc`.
    - No other in-flight DE work is staged on portal DEV that should NOT be included.

    After deploy, smoke-test the OFC toggle on PROD:
    1. Navigate to Advisor Intelligence > Distribution tab.
    2. Click OFC toggle — office donut renders with >= 5 office labels.
    3. Click Austin — advisor list renders (Travis Penfield visible).
    4. Continuous AUA + OFC — stacked area chart renders office series.
    5. NNA + OFC — diverging bar chart renders.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before deploying):
    - Confirm `bun run build` passes on portal DEV HEAD.
    - Confirm AE W2 MCP message received (PROD artifact live).
    - Check `git log --oneline portal DEV -5` — confirm DE W3 commit is HEAD.

    Phase 2 (after deploy):
    - Smoke-test OFC toggle on PROD (5-step checklist above).
    - Append to `org/compiler-tools-log.md`.
    - MCP message to 2.0.0_SA_COO: "ADVI_OFFICE W4 complete — portal PROD deployed. OFC toggle live."
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/ submodule (DEV → PROD)</shared_resource>
    <required_action>
      Check git status of portal DEV before deploying — this deploy is intended to ship
      all of the following DE work together in one push:
        - ADVI_REBORN.W6-004 (AdvisorsTab role_combination_breakdown)
        - ADVI_OFFICE.W3 (DistributionTab OFC toggle + types.ts + chartColors.ts)
        - ADVI_PROFAU.004 (PlatinumAdvisorSummary type fix — types.ts)
        - ADVI_PROFAU.005 (fee_summary L3 + total_market_value L4 wire)
      Confirm all four are committed to portal DEV before pushing to PROD.
      If any are missing, coordinate with DE + COO before pushing PROD.
      If additional unrelated DE commits are present on DEV, coordinate with COO before including.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Portal PROD updated; git tag created (portal-v{X.Y.Z}).
    2. OFC toggle visible and functional on PROD (3 toggle buttons: GEO, ADV, OFC).
    3. Office donut renders with labeled office segments in Snapshot AUA mode.
    4. Clicking an office drill shows advisor list.
    5. NNA + OFC diverging bar chart renders.
    6. Continuous AUA + OFC stacked area chart renders.
    7. No console errors on OFC toggle in PROD.
    8. MCP message to 2.0.0_SA_COO confirming deploy + smoke-test pass.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="deploy">portal DEV -> PROD merge + push</file>
    </files>
    <out_of_scope>
      Any backend AWS changes (AE W2 scope). Script changes (DS W1 scope). Type edits (DE W3 scope).
    </out_of_scope>
  </scope>

  <deliverables>
    - Portal PROD deployed; git tag pushed.
    - Smoke-test on PROD confirmed (OFC end-to-end functional).
    - MCP message to 2.0.0_SA_COO.
    - Session log with compiler tools section.
  </deliverables>
</task_order>
