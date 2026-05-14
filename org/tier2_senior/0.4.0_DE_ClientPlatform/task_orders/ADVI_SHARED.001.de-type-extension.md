<task_order>
  <metadata>
    <id>ADVI_SHARED.001</id>
    <slug>de-type-extension</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_SHARED</project_code>
    <priority>P0 — critical-path foundation; .002/.003/.006 cannot proceed until type shape lands</priority>
    <sla>~1d wall; standalone (no upstream gates)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §3.2 + §4.2 SHARED.001 + §6.1 compiler mandate template</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §E (`TenantLayoutConfig` field-gap analysis — 8 sub-blocks + §E.9 aggregate shopping list + §E.11 supplement)</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="authority">Andrew direct 2026-05-12 evening post portal-v2.1.82 PROD; routed via CTO PRD v0.1 `54c1ea270`; COO dispatch 2026-05-14 13:13Z per "drive ADVI_SHARED Phase 1 TO authoring" directive</ref>
    <ref type="cross_link">Critical-path foundation: blocks .002 .003 .006. Parallel-OK: .004 .005 (refactor; no type dep).</ref>
    <ref type="cto_ratify">Audit RAVC4 2026-05-12 00:15Z: Item 1 (dataSourcePanel.overlay) RATIFIED + Item 2 (roles.composition.enabled move) RATIFIED + §F PRD framing correction acknowledged</ref>
  </references>

  <context>
    Extend `portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts` per PRD §3.2 target schema. The DE 0.4 audit (§E.1-.8) enumerated 8 sub-blocks of NEW/EXTENDED fields driven by empirical scan of `_partners/49financial/` + `_partners/inflection/` divergence sites. 49F + Inflection layout objects populate every new field with explicit values (no implicit DEFAULT_LAYOUT fall-through for properties that diverge).

    Q2 (asset class taxonomy authority) — author with **portal-only assumption** per PRD §7.2 recommendation: `assetClasses.ordered` is a display ordering / inclusion filter; DS emits all classes regardless; portal filters per layout. If Andrew rules data-side later, .001 adds a `<TODO>` annotation pointing at DS-side taxonomy alignment but the type shape doesn't change.

    §E.11 supplement (PRD §3.2 amendments from audit):
    - `panels.dataSourcePanel.overlay?: ComponentType<{}> | null` (NEW — Inflection FidelityCustodianBar slot)
    - `roles.composition.enabled` moved from `features.*` to `roles.*` block (RATIFIED 2026-05-12 RAVC4)
  </context>

  <objective>
    Land TenantLayoutConfig type extension covering all 8 audit-enumerated divergence dimensions; populate 49F + Inflection layout objects with explicit values for every new field. tsc 0 errors. Zero behavior change (Phase 1 .002+ consumers do the wiring; .001 only declares the contract).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts — extend per audit §E.9 shopping list (identity + dataSources + tabs + panels + assetClasses + roles + features + routes blocks)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/49financial/layout.ts (CREATE if absent — audit §B finding "49F needs `_partners/49financial/layout.ts` for scaffolding canonicality") — populate every new field</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/layout.ts — populate every new field</file>
      <file action="readonly_reference">docs/briefs/ADVI_SHARED_AUDIT.md §E.1-.11 verbatim</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check TenantLayoutConfig</run>
      <expect>Type exports + usage sites enumerated; baseline coverage report.</expect>
      <if_mismatch>If `comp-transform` cannot index the type module (PRD §5.2 noted limitation on dispatcher components), document the gap in session log and proceed with manual grep enumeration of `useTenantLayout` consumers via `grep -rn "useTenantLayout" portal/src/`.</if_mismatch>
    </step>
    <step>
      <run>comp-blast TenantLayoutConfig</run>
      <expect>Downstream consumers limited to existing `useTenantLayout` hook + 4 already-adopted call-sites (PartnerAnalytics partial, AdvisorBookView, ClientsTab, AdvisorPublicProfile per §A audit).</expect>
      <if_mismatch>STOP. New consumers indicate concurrent agent work; surface to COO before extending.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "isInflectionFirm\|firmOverride === 'inf'\|firmOverride === 'bd'" portal/src/pages/AdvisorIntelligence/</run>
      <expect>Audit §A.8 baseline: 32 firmId-conditional sites (15 PartnerAnalytics + 6 AdvisorBookView + 6 ClientsTab + 1 AdvisorPublicProfile + 1 type-file informational + dispatcher allowlist + internal-tier gates).</expect>
      <if_mismatch>If count drifted significantly since audit (2026-05-12), surface delta — likely concurrent INFFIN.011 cross-firm consolidation overlap.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
      <if_mismatch>STOP. Fix type errors before commit.</if_mismatch>
    </step>
    <step>
      <run>/c/Users/AndrewBerman/.bun/bin/bun run dev --port 5175 + curl http://localhost:5175/</run>
      <expect>200; HMR clean; no console errors on initial page load.</expect>
      <if_mismatch>Investigate; ensure `useTenantLayout(firmId)` still resolves correctly with extended config shape.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-blast TenantLayoutConfig</run>
      <expect>Same consumer set as Phase 1 — no new downstream nodes appeared during write.</expect>
      <if_mismatch>Surface to COO; likely another agent committed a new consumer mid-flight.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: TenantLayoutConfig covers every field in audit §E.9 shopping list + §E.11 supplement (dataSourcePanel.overlay + roles.composition.enabled relocation).
    AC2: `_partners/49financial/layout.ts` exists; populates every new field with explicit values (no implicit DEFAULT_LAYOUT fall-through for diverging properties).
    AC3: `_partners/inflection/layout.ts` populates every new field with explicit values.
    AC4: Q2 assumption (assetClasses portal-only) documented inline + `<TODO Andrew Q2 ruling>` annotation if data-side later confirmed.
    AC5: tsc 0 errors.
    AC6: bun run dev smoke clean on both 49F login + Inflection login (initial page load only — no panel-level wiring this TO).
    AC7: Session log Compiler Tools section reproduces every Phase 1/2/3 `<run>` with observed result + pass/fail vs. `<expect>`.
    AC8: MCP RAVC2 to COO with commit hash + diff stats.
  </acceptance_criteria>

  <cross_domain_coordination>
    HARD DEPENDENCIES: none — foundation TO, no upstream gate.

    DOWNSTREAM BLOCKING: .002 (PartnerAnalytics convert) + .003 (BookView + ClientsTab convert) + .006 (canonicalization) all reference the new type fields. Land .001 first.

    PARALLEL-OK: .004 (co-location refactor) + .005 (component extraction) — pure-refactor, no type-shape dep.

    PORTAL SUBMODULE: DT 0.4 owns push. Bundle with .004/.005 ships if possible (single submodule bump).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure portal type extension. No data emit changes; no Lambda redeploys; no chain re-fires.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. TenantLayoutConfig.ts extended per audit §E.9 + §E.11
    2. _partners/49financial/layout.ts created + populated
    3. _partners/inflection/layout.ts updated + populated
    4. Single commit under 0.4.0_DE_ClientPlatform author
    5. Session log with Compiler Tools section
    6. MCP RAVC2 to COO
  </deliverables>

  <ravc>
    DE 0.4 RAVC2 to COO on AC1-8 PASS. COO ratifies + unblocks .002 + .003 + .006 dispatch.
  </ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"` per protocol.

    **Andrew Q2 callout:** PRD §7.2 unresolved. Authoring with portal-only assumption — if Andrew rules data-side, follow-on TO aligns DS gold/mix taxonomy. Non-blocking for .001 ship; type shape correct under either ruling.

    **Compiler context update:**
    ```
    SERIAL=0.4.0_DE_ClientPlatform
    TO_ID=ADVI_SHARED.001
    ```

    **§4.2 critical-path:** SHARED.001 → .002 + .003 → .006 → .007 → .008. .004 + .005 parallelize.
  </notes>
</task_order>
