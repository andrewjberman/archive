<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.026</id>
    <slug>ae-types-index</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>done</status>
    <completed>2026-05-14</completed>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>Wave 1 (.027 + .028) RAVC2 PASS — confirms empirical-leverage validators ship before multi-tenant-readiness tools</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — Wave 3 multi-tenant readiness; supports FIRMSEP / Cottonwood / future-partner work + canonicalization PRD audit scope</priority>
    <sla>~1-1.5 days wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-026</ref>
    <ref type="anchor_brief">DE 0.4 brief `2a542e519` (`docs/briefs/comp-types-index-tool-brief-20260514.md`) — SHARED.001 manual-grep fallback for type-module indexing</ref>
    <ref type="empirical">SHARED.001 TenantLayoutConfig extension empirically required manual grep enumeration when `comp-transform schema-check` returned "Component not found" on type-only modules.</ref>
    <ref type="cross_link">Wave 3 sibling: .031 comp-adapter-audit (shares TS AST setup). Future canonicalization PRDs (FIRMSEP.10, ADVI_SHARED v0.2) directly benefit.</ref>
  </references>

  <context>
    `comp-transform schema-check` and `comp-blast` walk component graph (file → JSX → imported types). Both return "Component not found" for type-only modules (TypeScript `interface` / `type` / `const` in `.ts` files with no JSX).

    DE 0.4 hit this empirically on SHARED.001 (`TenantLayoutConfig` type extension; ~29 consumer sites verified via manual `grep -rn "useTenantLayout"`). The 10-min manual fallback was workable but the §3.X.1 canonicalization-PRD template addition explicitly requires global grep — `comp-types index <TypeName>` is the structurally-clean replacement.

    **Bonus architectural insight from DE 0.4's brief (banking-worthy):** the `--firm-conditional-sites` mode co-searches for `firmOverride === '<value>'` sites in the same scope as a type's consumers — multi-tenant audit primitive. This makes `comp-types index --firm-conditional-sites TenantLayoutConfig` directly answer the audit §G 4-layer firmId namespace question that took DE 0.4 manual grep to enumerate in SHARED.006.

    **Default-fallback sites column** (DE's other banked insight): consumers reading the type frequently default via `?? DEFAULT_LAYOUT` / `?? false` / `?? null`. These are silent-drift risk sites where shape changes don't fail loudly. Surface as their own column.
  </context>

  <objective>
    Land `comp-types` family of subcommands:
    - `comp-types index <TypeName>` — primary mode. Output: Consumers / Mutations / Exported alias chains / **Default-fallback sites**.
    - `comp-types blast <TypeName>` — what breaks if Type changes shape?
    - `comp-types fields <TypeName>` — enumerate fields with per-field consumers.
    - `--severity warn|error` — match v0.2 TO-11 convention.
    - `--firm-conditional-sites` — co-search for `firmOverride === '<value>'` sites in same scope (multi-tenant audit primitive).

    Validates against DE 0.4's manual-grep baseline (≥29 TenantLayoutConfig consumer sites returned in <5s vs 10min manual).
  </objective>

  <scope>
    <files>
      <file action="create">.tools/comp-types (new binary)</file>
      <file action="create">org/modules/graph/types-index/{TypeName}.yaml (per-type index manifest)</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_shared/types/TenantLayoutConfig.ts (validation anchor)</file>
      <file action="readonly_reference">docs/briefs/comp-types-index-tool-brief-20260514.md (DE 0.4 spec)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>cat docs/briefs/comp-types-index-tool-brief-20260514.md | head -50</run>
      <expect>DE 0.4 brief enumerates the spec; align signature decisions before ts-morph integration.</expect>
      <if_mismatch>If brief absent or short, surface to DE 0.4 + COO; need spec clarity.</if_mismatch>
    </step>
    <step>
      <run>npm list typescript ts-morph 2>&1 | head -10  (or equivalent for the AST library you choose)</run>
      <expect>TS AST library available OR identify install step.</expect>
      <if_mismatch>Setup TS AST library first (likely `ts-morph` per PRD §15.4 dependencies).</if_mismatch>
    </step>
    <step>
      <run>grep -rn "useTenantLayout" portal/src/ | wc -l</run>
      <expect>Baseline manual-grep count: ~29 per DE 0.4 SHARED.001 finding. This is the validation target.</expect>
      <if_mismatch>If significantly different, surface — manual-grep baseline may need refresh.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-types index TenantLayoutConfig</run>
      <expect>≥29 consumer sites returned in <5s. Per-site fields: file, line, consumer-pattern (useTenantLayout / direct-prop / default-fallback). Time MUST be <5s per AC1.</expect>
      <if_mismatch>STOP. AC1 is load-bearing.</if_mismatch>
    </step>
    <step>
      <run>comp-types index TenantLayoutConfig | grep -c "default-fallback"</run>
      <expect>≥4 default-fallback sites detected (DE 0.4 brief calls them out architecturally novel; this is the silent-drift-risk surface).</expect>
      <if_mismatch>Default-fallback detection incorrect; refine pattern.</if_mismatch>
    </step>
    <step>
      <run>comp-types index TenantLayoutConfig --firm-conditional-sites</run>
      <expect>Cross-references with `firmOverride === '<value>'` sites; correctly enumerates the 4-layer firmId namespace consumers per SHARED audit §G.</expect>
      <if_mismatch>--firm-conditional-sites mode incorrect; this is the multi-tenant primitive.</if_mismatch>
    </step>
    <step>
      <run>comp-types blast TenantLayoutConfig</run>
      <expect>Downstream-blast view: what breaks if Type shape changes? Returns blast radius (≥29 sites).</expect>
    </step>
    <step>
      <run>comp-types fields TenantLayoutConfig</run>
      <expect>Per-field consumer enumeration (e.g., `assetClasses.includesCash` → 3 consumers per SHARED.002 site delta).</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Validate against DE 0.4's manual baseline: did comp-types index land all ≥29 sites that DE enumerated by hand?</run>
      <expect>Set difference = empty. Tool MATCHES manual baseline.</expect>
      <if_mismatch>Tool incomplete OR DE baseline incomplete; reconcile.</if_mismatch>
    </step>
    <step>
      <run>Test on ≥2 other types (e.g., `CanonicalFirmId`, `AdvisorTimeseriesPoint`)</run>
      <expect>No crashes; output ranks/structure consistent.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-types index TenantLayoutConfig` returns ≥29 consumer sites in <5s (validates against DE 0.4 manual-grep baseline).
    AC2: Default-fallback sites column populates (`?? DEFAULT_LAYOUT`, `?? false`, `?? null` patterns).
    AC3: `--firm-conditional-sites` correctly enumerates 4-layer firmId namespace consumers per audit §G.
    AC4: `comp-types blast` + `comp-types fields` subcommands functional.
    AC5: Per-type yaml manifest persisted under `org/modules/graph/types-index/`.
    AC6: `--severity warn|error` matches v0.2 TO-11 convention.
    AC7: Tested on ≥2 additional types without crash.
    AC8: Session log + RAVC2 MCP to COO with manual-baseline validation evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: DE 0.4 brief read + TS AST library setup + manual-grep baseline establish
    Phase 2: comp-types index/blast/fields + --firm-conditional-sites + --severity
    Phase 3: manual-baseline diff + ≥2 other types tested
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Wave 1 (.027 + .028) RAVC2 — sequencing per PRD §15.5 recommendation.

    PARALLEL-OK: Wave 3 sibling .031 comp-adapter-audit (shares TS AST setup; share ts-morph install).

    DOWNSTREAM CONSUMERS: FIRMSEP.10 Cottonwood frontend wiring (canonicalization audits), ADVI_SHARED v0.2 if authored, any future tenant/firm/partner namespace work.

    NO PORTAL CODE CHANGES (this is a tool that READS portal source).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `.tools/comp-types` binary with index / blast / fields subcommands + flags
    2. `org/modules/graph/types-index/` manifest directory + ≥3 type yaml files
    3. Manual-baseline validation evidence (DE 0.4 reconciliation)
    4. Session log + RAVC2
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-8 PASS.</ravc>

  <notes>
    **AC1 + AC3 are load-bearing:** the ≥29-sites-in-<5s benchmark + multi-tenant primitive (`--firm-conditional-sites`) are the value-delivering surfaces per DE 0.4 brief.

    **Banking opportunity:** DE 0.4's "default-fallback sites" insight is structurally novel — output column architecturally distinct from blast/consumer columns because it captures silent-drift-risk specifically. Worth a memory entry post-ship.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
