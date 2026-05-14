<task_order>
  <metadata>
    <id>ADVI_SHARED.003</id>
    <slug>de-bookview-clientstab-convert</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. (1) .001 SHIPPED 755dc104 + CTO RAVC4 ACCEPT; (2) ADVI_INFTGT CLOSED 2026-05-13 (AdvisorBookView + ClientsTab touch zone no longer active). Note: DE may absorb the @deprecated panels.roleComposition.enabled migration during .003 per the .001 BC decision (1-LOC AdvisorPublicProfile rewire flagged in DE session log c835a0e54).</dispatch_unblock_condition>
    <project_code>ADVI_SHARED</project_code>
    <priority>P0 — drives dataSources.staticPaths field validation; sibling to .002</priority>
    <sla>~1d wall post-unblock</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §4.2 SHARED.003</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §A.2 AdvisorBookView 6 sites + §A.3 ClientsTab 6 sites + §D.1 cache-key (advisor-book-view) + §D collision-resolution map</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="upstream_dep">SHARED.001 type extension RAVC2 PASS</ref>
    <ref type="cross_link">Companion: .002 (PartnerAnalytics). Parallel-OK once .001 lands.</ref>
  </references>

  <context>
    Convert two files per audit §A.2-.3:
    - `portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx` (6 firmId-conditional sites)
    - `portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx` (6 firmId-conditional sites)

    Drives `dataSources.staticPaths` field (from .001 type extension) validation — both files read partner-specific static S3 path patterns from the layout instead of inline branching.

    **§D.1 cache-key collision** `['advisor-book-view', 'advisorId', 'firmOverride']` — touched by SHARED.006 firmOverride canonicalization (not this TO). .003 leaves the key alone; .006 canonicalizes upstream.
  </context>

  <objective>
    Convert AdvisorBookView.tsx + ClientsTab.tsx's 12 total firmId-conditional sites (6+6) to `useTenantLayout(firmId)` config-driven dispatch. Zero behavior change.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx — 6 sites per audit §A.2</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx — 6 sites per audit §A.3</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check AdvisorBookView + comp-transform schema-check ClientsTab</run>
      <expect>All 12 sites' field accesses map to layout blocks from .001.</expect>
      <if_mismatch>STOP if missing fields; surface to COO.</if_mismatch>
    </step>
    <step>
      <run>comp-blast AdvisorBookView + comp-blast ClientsTab</run>
      <expect>Consumer chain unchanged.</expect>
      <if_mismatch>Concurrent project commit; surface.</if_mismatch>
    </step>
    <step>
      <run>git log --since="$DATE_RAVC2_FOR_001" -- portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx</run>
      <expect>Empty during dispatch_held window OR only orthogonal commits.</expect>
      <if_mismatch>Surface merge-conflict risk to COO.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
    </step>
    <step>
      <run>bun run dev + visual smoke: 49F + Inflection AdvisorBookView + ClientsTab</run>
      <expect>Behavior identical pre/post.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>grep -n "isInflectionFirm\|firmOverride === '" portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx</run>
      <expect>Zero matches outside §3.6 allowlist.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Zero firmId-conditional branches in AdvisorBookView.tsx + ClientsTab.tsx outside §3.6 allowlist.
    AC2: All 12 sites converted (6 + 6).
    AC3: 49F + Inflection visual + behavioral parity.
    AC4: tsc 0 errors.
    AC5: Session log + RAVC2 MCP.
  </acceptance_criteria>

  <cross_domain_coordination>
    HARD DEPENDENCIES: SHARED.001 RAVC2; Q5 option (c) sequencing — ADVI_INFTGT P1/P2 wave 2 close (likely touches AdvisorPublicProfile / ClientsTab).

    PARALLEL-OK: .002 (different files).

    PORTAL SUBMODULE: DT 0.4 push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE refactor only.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. AdvisorBookView.tsx + ClientsTab.tsx converted
    2. Single commit (or split per-file if cleaner)
    3. Session log + RAVC2
  </deliverables>

  <ravc>DE 0.4 RAVC2 to COO on AC1-5 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.

    **Audit §A.4 single-site `AdvisorPublicProfile.tsx` 1 firmId branch** — NOT in .003 scope; folds into .007 lint residual sweep OR .006 canonicalization (whichever lands first naturally absorbs it).
  </notes>
</task_order>
