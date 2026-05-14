<task_order>
  <metadata>
    <id>ADVI_SHARED.002</id>
    <slug>de-partneranalytics-convert</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. Original conditions met: (1) .001 SHIPPED 755dc104 + 8df348bd0 + CTO RAVC4 ACCEPT; (2) ADVI_INFTGT CLOSED 2026-05-13 (no overlap risk); (3) ADVI_INFGRO.005 Phase 2 portal-local shipped (d4e28cca; DT push pending — merge surface bounded). CTO ratify on parallel dispatch acknowledged. Q5 sequencing call: option (c) gate met via INFTGT closure + INFGRO.005 commit landing; no further hold needed.</dispatch_unblock_condition>
    <project_code>ADVI_SHARED</project_code>
    <priority>P0 — worst-offender file (15 firmId-conditional sites); drives asset-class taxonomy + auaDonut.source + barChart.stacked field validation</priority>
    <sla>~1d wall post-unblock</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §3.2 + §4.2 SHARED.002 + §6.1 compiler mandate template</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §A.1 PartnerAnalytics 15-site inventory + §D.4 cache-key collision (partner-analytics granularity)</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="upstream_dep">SHARED.001 type extension (must RAVC2 PASS first)</ref>
    <ref type="cross_link">Companion: .003 (BookView + ClientsTab — sibling DE convert TO; parallel-OK once .001 lands). Coordinates with: .006 canonicalization (waits for .002+.003 to route through useTenantLayout)</ref>
  </references>

  <context>
    `portal/src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx` is the worst-offender file (15 firmId-conditional sites per audit §A.1). Convert from inline `isInflectionFirm` / `firmOverride === '<literal>'` branches to `useTenantLayout(firmId)` config-driven dispatch.

    Audit §A.1 site breakdown:
    - 3 asset-class taxonomy filter sites at lines 1494/1641/1856 (the `.filter(cls => cls !== 'cash' || isInflectionFirm)` pattern — see PRD §1.2)
    - auaDonut.source-specific branching
    - barChart.stacked rendering paths
    - granularity defaults
    - Misc per-firm cosmetic branches

    Each site reads from `layout.{block}.{field}` per .001's extended TenantLayoutConfig instead of hardcoded conditionals.

    **§D.4 cache-key collision:** `['partner-analytics', 'granularity', 'firmOverride']` resolves via SHARED.006 canonicalize-upstream — no `cacheKeyNamespace` field added. .002 leaves the cache key alone; .006 swaps the firmOverride literal source.
  </context>

  <objective>
    Convert PartnerAnalytics.tsx's 15 firmId-conditional sites to `useTenantLayout(firmId)` config-driven dispatch. Zero behavior change for 49F + Inflection (config values must reproduce current behavior exactly). New-firm onboarding becomes a TenantLayoutConfig populate; no code edit.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx — convert 15 sites per audit §A.1</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts (from .001)</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_partners/{49financial,inflection}/layout.ts (from .001)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check PartnerAnalytics</run>
      <expect>15 sites' field accesses map to layout-block fields populated in .001.</expect>
      <if_mismatch>STOP. If a site's required field isn't in .001's type extension, surface to COO — likely a .001 audit gap.</if_mismatch>
    </step>
    <step>
      <run>comp-blast PartnerAnalytics</run>
      <expect>Downstream consumers + parent dispatcher chain unchanged from audit baseline.</expect>
      <if_mismatch>Concurrent project (ADVI_INFTGT/INFGRO) committed new consumer; surface to COO before write.</if_mismatch>
    </step>
    <step>
      <run>git log --since="$DATE_RAVC2_FOR_001" -- portal/src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx</run>
      <expect>Empty or only .001's own commits — no concurrent commits during dispatch_held window.</expect>
      <if_mismatch>Merge conflict risk. Surface to COO; may need to rebase before write.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
      <if_mismatch>STOP. Fix.</if_mismatch>
    </step>
    <step>
      <run>bun run dev + curl + visual smoke: 49F + Inflection PartnerAnalytics page</run>
      <expect>Behavior identical to pre-edit baseline (charts, donuts, granularity defaults all match).</expect>
      <if_mismatch>STOP. Config values must reproduce current behavior exactly.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>grep -n "isInflectionFirm\|firmOverride === '" portal/src/pages/AdvisorIntelligence/_shared/components/PartnerAnalytics.tsx</run>
      <expect>Zero matches OR only the §3.6 allowlist patterns (none expected for PartnerAnalytics — fully convertible per audit).</expect>
      <if_mismatch>Residual literals; finish the conversion before RAVC2.</if_mismatch>
    </step>
    <step>
      <run>comp-blast PartnerAnalytics</run>
      <expect>Same consumer set as Phase 1.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Zero `isInflectionFirm` / `firmOverride === '<literal>'` branches in PartnerAnalytics.tsx outside §3.6 allowlist.
    AC2: All 15 audit §A.1 sites converted to `useTenantLayout(firmId)` field access.
    AC3: 49F + Inflection visual + behavioral parity (no regression).
    AC4: tsc 0 errors.
    AC5: bun run dev smoke clean per partner login.
    AC6: Session log captures comp-transform schema-check + diff summary + visual diff per partner.
    AC7: MCP RAVC2 to COO with commit hash + per-site delta count.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Per phases above. Inherits PRD §6.1 standard template.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES:
    - SHARED.001 type extension RAVC2 PASS (type fields exist)
    - Q5 sequencing: ADVI_INFTGT P1/P2 wave 2 + ADVI_INFGRO Stage 1 .005 (DE portal GRO side-by-side, touches PartnerAnalytics) ship FIRST per PRD §7.5 option (c) recommendation

    MERGE-CONFLICT RISK: ADVI_INFGRO.005 (DE portal GRO side-by-side) touches PartnerAnalytics. COO sequences — confirms INFGRO.005 close before unblocking .002.

    PARALLEL-OK: .003 (sibling DE convert TO; different files).

    PORTAL SUBMODULE: DT 0.4 owns push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure FE refactor. No data emit changes.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. PartnerAnalytics.tsx converted (15 sites → layout config)
    2. Single commit under 0.4.0_DE_ClientPlatform author
    3. Session log with Compiler Tools section
    4. MCP RAVC2 to COO
  </deliverables>

  <ravc>
    DE 0.4 RAVC2 to COO on AC1-7 PASS.
  </ravc>

  <notes>
    **Dispatch hold:** Q5 option (c) sequencing. COO MCP unblocks after INFGRO.005 close + INFTGT P1/P2 wave 2 close.

    **Q2 dep:** if Andrew rules asset-class taxonomy data-side post-.001, .002 still ships against portal-only config; follow-on TO aligns DS taxonomy without re-touching .002.

    **Author identity:** `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.
  </notes>
</task_order>
