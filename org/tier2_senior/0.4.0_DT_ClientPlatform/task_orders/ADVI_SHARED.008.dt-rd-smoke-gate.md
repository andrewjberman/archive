<task_order>
  <metadata>
    <id>ADVI_SHARED.008</id>
    <slug>dt-rd-smoke-gate</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <coordinates_with>0.4.2_RD_AdvisorIntelligence (visual smoke + Playwright)</coordinates_with>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>(1) .001 + .002 + .003 + .004 + .005 + .006 + .007 ALL RAVC2 PASS. .008 is the Phase 1 close gate — runs only when every other Phase 1 TO has shipped.</dispatch_unblock_condition>
    <project_code>ADVI_SHARED</project_code>
    <priority>P0 — Phase 1 close gate; DEV deploy + cross-partner regression validation before Phase 2 scaffolding tool</priority>
    <sla>~0.5d wall post-unblock</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §4.2 SHARED.008 + §8 acceptance criteria</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="upstream_dep">.001-.007 all RAVC2 PASS</ref>
    <ref type="cross_link">Phase 1 close; Phase 2 (.009-.011 scaffolding tool) unblocks on .008 RAVC2.</ref>
  </references>

  <context>
    Phase 1 close gate. All Phase 1 TOs (.001-.007) have shipped to portal DEV via DT 0.4 submodule bumps; .008 is the cross-validation gate:
    - TypeScript + Playwright smoke
    - DEV deploy (CloudFront invalidation + endpoint health)
    - Cross-firm regression — 49F + Inflection visual + functional smoke across critical pages
    - Lint baseline confirmation (≤10 warnings per PRD §8 AC-3)
    - Cache-key collision sustained-zero (per .006 AC5)

    RD 0.4.2 owns visual smoke (Playwright capture + manual verification on critical pages). DT 0.4 owns DEV deploy + endpoint health + Playwright orchestration.
  </context>

  <objective>
    Phase 1 close gate: validate ADVI_SHARED Phase 1 ships clean on DEV with zero cross-firm regression. Land DEV deploy. Confirm lint baseline + cache-collision-zero. Sign Phase 2 unblock condition.
  </objective>

  <scope>
    <files>
      <file action="orchestrate">Portal DEV deploy via DT 0.4 normal cycle (submodule pointer bump + CloudFront invalidation)</file>
      <file action="visualize">RD 0.4.2 visual smoke on critical pages × 2 partners (49F + Inflection)</file>
      <file action="run">Playwright suite under `portal/.frontend-dev/testing/` per /frontend-dev plugin</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>git log --oneline --since="$DATE_PHASE_1_START" -- portal/</run>
      <expect>All .001-.007 commits present + no surprise commits (concurrent project ships should have landed BEFORE .002/.003/.006 dispatch unblock per Q5 sequencing).</expect>
      <if_mismatch>Surface to COO — sequencing failure.</if_mismatch>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | wc -l</run>
      <expect>≤10 residual warnings per PRD §8 AC-3.</expect>
      <if_mismatch>Surface to RD — .007 may need follow-on sweep.</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions</run>
      <expect>0 collisions (sustained from .006).</expect>
      <if_mismatch>STOP. .006 verification regressed.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run build</run>
      <expect>Build clean.</expect>
    </step>
    <step>
      <run>DT 0.4: submodule pointer bump on parent CLOUD; push to remote</run>
      <expect>portal-v{X.Y.Z} tagged + pushed; CloudFront origin updated.</expect>
    </step>
    <step>
      <run>DT 0.4: CloudFront invalidation</run>
      <expect>Cache invalidated; DEV endpoint serves new bundle.</expect>
    </step>
    <step>
      <run>RD 0.4.2: Playwright smoke per `/frontend-dev` plugin against DEV — 49F login + Inflection login + Cottonwood login (latter expected fallback to default)</run>
      <expect>All three partner flows clean; no regression vs baseline.</expect>
    </step>
    <step>
      <run>RD 0.4.2: manual visual smoke on critical pages × 2 partners (PartnerAnalytics, AdvisorBookView, ClientsTab, AdvisorPublicProfile, DistributionTab, BusinessIntelligence)</run>
      <expect>Zero visual regression.</expect>
    </step>
    <step>
      <run>Empirical /Advisors tab smoke (49F + Inflection) — repro of the localhost spinner pattern flagged by RD 2026-05-14 morning</run>
      <expect>No infinite spinner; pages settle within bun-pre-bundle norm (~5-10s).</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-blast useTenantLayout</run>
      <expect>Consumer count grew significantly post .002 + .003 + .006 — expected.</expect>
    </step>
    <step>
      <run>Document Phase 2 unblock condition met</run>
      <expect>.009-.011 scaffolding tool TOs unblockable.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: DEV deploy clean (portal-v{X.Y.Z} tagged + pushed + CloudFront invalidated).
    AC2: Playwright smoke per /frontend-dev — 49F + Inflection + Cottonwood-fallback all PASS.
    AC3: Manual visual smoke critical pages × 2 partners — zero regression.
    AC4: Lint count ≤10 (PRD §8 AC-3).
    AC5: comp-cache collisions = 0 sustained.
    AC6: tsc 0 errors.
    AC7: /Advisors tab spinner regression NOT reproduced.
    AC8: Session log with deploy evidence (tag + invalidation ID + Playwright report path).
    AC9: MCP RAVC2 to COO + announce Phase 1 close + Phase 2 unblock.
  </acceptance_criteria>

  <compiler_tools_mandate>Phases above.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: ALL Phase 1 TOs (.001-.007) RAVC2 PASS. .008 is the gate.

    POST-CLOSE: .009 + .010 + .011 (Phase 2 scaffolding tool) unblock; .012 + .013 (Phase 3 regression gate + docs) author per CTO ratify post-.008.

    PORTAL SUBMODULE: DT 0.4 push — bundle a clean Phase 1 close in single submodule pointer bump if possible.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Phase 1 close gate — pure portal validation + deploy.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. portal-v{X.Y.Z} tagged + pushed (DT 0.4)
    2. CloudFront invalidation (DT 0.4)
    3. Playwright smoke evidence (RD 0.4.2)
    4. Manual visual smoke evidence (RD 0.4.2)
    5. Session log + RAVC2 MCP to COO
    6. Phase 1 close announcement
  </deliverables>

  <ravc>
    DT 0.4 RAVC2 to COO on AC1-9 PASS. COO ratifies + announces Phase 1 close + relays to Andrew for Phase 2 scaffolding tool GO.
  </ravc>

  <notes>
    **Phase 1 close discipline:** .008 is the gate. Do NOT short-circuit AC2/AC3 — full visual smoke is mandatory. Cross-firm regression risk is HIGH per PRD §9 (Inflection visual regression during refactor flagged HIGH severity).

    **Author identity:** `--author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>"` for orchestration commits. Visual smoke commits author under RD 0.4.2.

    **Phase 2 readiness signal:** AC9 RAVC2 explicitly states "Phase 2 unblocked" so COO can dispatch .009 + .010 + .011.
  </notes>
</task_order>
