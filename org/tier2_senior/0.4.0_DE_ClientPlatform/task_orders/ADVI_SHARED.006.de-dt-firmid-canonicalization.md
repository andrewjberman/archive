<task_order>
  <metadata>
    <id>ADVI_SHARED.006</id>
    <slug>de-dt-firmid-canonicalization</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <coordinates_with>0.4.0_DT_ClientPlatform (api/endpoints/advisor-intelligence.ts touch zone)</coordinates_with>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. (1) .002 SHIPPED 79e35429 (PartnerAnalytics 15-site convert; semantic-split finding: isInflectionFirm -> 3 distinct layout semantics); (2) .003 SHIPPED 5fb03386 (BookView + ClientsTab 12-site convert + bundled @deprecated panels.roleComposition migration + 5 BC field removals). firmId literal surface now shrunk to dispatcher + L3 partner-constants + L4 api endpoint per audit §G — exactly the staged-rename scope per PRD §3.1. Audit §A.4 single-site AdvisorPublicProfile.tsx:57 firmIdFromOverride helper folds into this .006 canonicalization sweep per DE 0.4 .003 RAVC2 note.</dispatch_unblock_condition>
    <project_code>ADVI_SHARED</project_code>
    <priority>P0 — root-cause fix for prefetchQuery cache saturation incident (DE `ff54d611` revert); 4 cache-key collisions resolve via canonicalize-upstream per audit §D</priority>
    <sla>~1d wall post-unblock</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §3.1 canonical firmId namespace + §4.2 SHARED.006 + §6.2 cross-domain coordination block</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §G firmId namespace literal census (4-layer) + §D cache-key collision resolution map</ref>
    <ref type="cto_ratify">Session66 RAVC4 BONUS §H.5: prefetchQuery saturation hypothesis ratified — SHARED.006 firmOverride canonicalization is root-cause fix for DE's `ff54d611` Step 6 revert. Coordination path (a): superseded TO `576056e67` SUPERSEDED-BY-SHARED.006.</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="upstream_dep">SHARED.002 + .003 RAVC2 PASS</ref>
    <ref type="cross_link">Coordinates with: FIRMSEP.10 Cottonwood live ship (must land BEFORE Cottonwood goes live, otherwise Cottonwood user lands on default 49F view silently — per PRD §6.2). Sequencer: COO.</ref>
  </references>

  <context>
    Canonicalize the 4-layer firmId namespace ambiguity per audit §G:
    - **L1 — `firmAccess.ts`** canonical namespace (`'bd' | 'inf' | 'cottonwood' | ...`)
    - **L2 — `AdvisorIntelligence/index.tsx`** dispatcher (PARTNER_VIEWS map)
    - **L3 — `_partners/{firm}/constants.ts`** internal FIRM_ID
    - **L4 — `api/endpoints/advisor-intelligence.ts`** LAMBDA_FIRM_ID map

    Today these diverge: 49F is `'bd'` at L1/L4 but `'49financial'` at some L2 keys; the divergence creates 4 empirically-confirmed cache-key collisions (audit §D) — same React Query key + different response types per firmId namespace = cache corruption.

    **Convergence rule:** every layer reads canonical from L1 (`firmAccess.ts`). Delete `LAMBDA_FIRM_ID`. Delete `isInflectionFirm` helper (replaced by `useTenantLayout(firmId).identity.firmId === 'inf'` if a check is needed, or by the type-narrow access patterns from .002/.003). Introduce `CanonicalFirmId` TypeScript type alias for the union.

    **§H.5 ratified hypothesis:** the prefetchQuery cache saturation that DE 0.4 reverted in `ff54d611` (Step 6) is the empirical symptom of L1/L2/L3/L4 firmId divergence — converging to L1 canonical eliminates the cache-key collision class entirely. SHARED.006 is root-cause fix; reverted prefetchquery TO `576056e67` SUPERSEDED.

    **Staged rename per §9 risk mitigation:**
    1. Rename L3 first (constants — internal scope; lowest blast)
    2. Rename L2 (PARTNER_VIEWS keys — dispatcher scope)
    3. Delete L4 LAMBDA_FIRM_ID map (api routing — collapse to L1)
    4. Delete `isInflectionFirm` helper (now unused post-.002+.003)

    Each rename a separate commit; reversible per-step.
  </context>

  <objective>
    Converge all 4 firmId namespace layers on L1 (`firmAccess.ts`). Delete LAMBDA_FIRM_ID map + isInflectionFirm helper. Introduce `CanonicalFirmId` type alias. Zero React Query cache-key collisions (verified via comp-cache collisions).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/49financial/constants.ts — rename L3 FIRM_ID to L1 canonical</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/constants.ts — rename L3 FIRM_ID to L1 canonical</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/index.tsx — rename L2 PARTNER_VIEWS keys to L1 canonical</file>
      <file action="delete">portal/src/api/endpoints/advisor-intelligence.ts LAMBDA_FIRM_ID map — collapse to L1 firmAccess.ts read</file>
      <file action="delete">portal/src/pages/AdvisorIntelligence/_shared/helpers/isInflectionFirm.ts (or wherever defined) — superseded by useTenantLayout</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/_shared/types/CanonicalFirmId.ts — type alias for L1 union</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-cache collisions</run>
      <expect>4 audit-documented collisions (advisor-book-view + timeseries-overview + firm-leaderboard + partner-analytics) per §D.1-.4.</expect>
      <if_mismatch>If new collisions appeared since audit, fold into scope. If existing collisions resolved by concurrent work, narrow scope.</if_mismatch>
    </step>
    <step>
      <run>comp-routes trace advisor-intelligence</run>
      <expect>L4 LAMBDA_FIRM_ID consumers enumerated; api endpoint routing path mapped.</expect>
      <if_mismatch>If non-obvious consumers, surface to COO — may need DT 0.4 coordination.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "LAMBDA_FIRM_ID\|isInflectionFirm" portal/src/</run>
      <expect>Bounded set — most consumers eliminated by .002 + .003. Residual consumers itemized for staged rename.</expect>
      <if_mismatch>Excess consumer surface — pause and surface to COO.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors after each staged rename commit.</expect>
    </step>
    <step>
      <run>comp-cache collisions (post-rename)</run>
      <expect>0 collisions.</expect>
      <if_mismatch>STOP. Identify residual collision source; finish rename.</if_mismatch>
    </step>
    <step>
      <run>bun run dev + visual smoke 49F + Inflection critical pages</run>
      <expect>Behavior identical; React Query cache hydrates correctly post-rename.</expect>
    </step>
    <step>
      <run>Validate Cottonwood layout path (FIRMSEP.10 readiness) — confirm `'cottonwood'` L1 namespace honored everywhere post-rename even with no `_partners/cottonwood/` dir yet</run>
      <expect>L1-only consumers handle Cottonwood gracefully (no crash; falls through to default empty state).</expect>
      <if_mismatch>Surface to COO + DT 0.4 — FIRMSEP.10 Cottonwood ship-time blocker.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-cache collisions</run>
      <expect>0 collisions sustained.</expect>
    </step>
    <step>
      <run>comp-blast firmAccess.ts</run>
      <expect>Consumer count IS the new L1-canonical-converged total (expected to grow modestly as L2/L3/L4 sites now read from L1).</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: All 4 firmId layers converged on L1 (`firmAccess.ts`).
    AC2: LAMBDA_FIRM_ID map deleted; api/endpoints/advisor-intelligence.ts reads L1.
    AC3: `isInflectionFirm` helper deleted (superseded by useTenantLayout).
    AC4: `CanonicalFirmId` type alias created.
    AC5: comp-cache collisions = 0 sustained (Phase 3 verification).
    AC6: 49F + Inflection visual/behavioral parity post-rename.
    AC7: Cottonwood L1 readiness gate PASSes (no crash; default-handled).
    AC8: Staged commits per §9 risk mitigation (4 separate commits: L3 → L2 → L4 → helper delete).
    AC9: Session log + RAVC2 MCP.
  </acceptance_criteria>

  <compiler_tools_mandate>Phases above. **Auto-rule 2 trigger:** new state driving React Query — `comp-cache collisions` MANDATORY at Phase 1 + Phase 2 + Phase 3 per CLAUDE.md auto-rules.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES:
    - SHARED.002 + .003 RAVC2 PASS (firmId literal surface shrunk to dispatcher files)

    SEQUENCER (COO):
    - SHARED.006 must land BEFORE FIRMSEP.10 Cottonwood live ship (PRD §6.2). Otherwise Cottonwood user lands on default 49F view silently.

    COORD: DT 0.4 (api/endpoints/advisor-intelligence.ts touch zone — L4 LAMBDA_FIRM_ID map deletion).

    PARALLEL-RISK: avoid concurrent commits to firmAccess.ts during .006 ship; coord internally with DT 0.4.

    SUPERSEDES: TO `576056e67` `prefetchquery-saturation-root-cause` (per session66 RAVC4 ratification).

    PORTAL SUBMODULE: DT 0.4 push (multi-step rename; bundle as one submodule bump or split per stage at DT discretion).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure portal canonicalization. No data emit / Lambda redeploy / chain refire.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. 4 staged rename commits (L3 → L2 → L4 → helper delete) per §9 risk mitigation
    2. CanonicalFirmId type alias
    3. comp-cache collisions = 0 verification
    4. Cottonwood readiness gate evidence
    5. Session log with staged-rename evidence + RAVC2 MCP
  </deliverables>

  <ravc>
    DE 0.4 RAVC2 to COO on AC1-9 PASS. COO ratifies + relays Cottonwood-ready signal to FIRMSEP.10 owner. INFFIN.011 cross-firm consolidation (RD lane) compatible post-.006.
  </ravc>

  <notes>
    **Why .006 is P0:** root-cause fix for prefetchQuery cache saturation that DE 0.4 reverted in `ff54d611` (Step 6). The revert was a defensive backstop; .006 fixes the underlying namespace collision. Once .006 ships, the prefetch can be re-introduced safely.

    **Author identity:** `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.

    **Cottonwood-ready signal:** AC7 verification IS the gate for FIRMSEP.10 to proceed. COO routes the signal to AE 0.7 / DT 0.4 (FIRMSEP.10 owners) post-RAVC2.
  </notes>
</task_order>
