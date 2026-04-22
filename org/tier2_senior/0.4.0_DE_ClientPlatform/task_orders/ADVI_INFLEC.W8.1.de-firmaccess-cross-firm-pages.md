<task_order>
  <metadata>
    <id>ADVI_INFLEC.W8.1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>complete</status>
    <acked>yes</acked>
    <project_code>ADVI_INFLEC</project_code>
    <priority>P1 — Andrew directive 2026-04-22; ship ASAP on current DE bandwidth</priority>
    <sla>~2h (one-line edit per firm + DEV smoke)</sla>
    <decision_authority>Andrew directive 2026-04-22 (captured in PRD §9 W8 commit 7fae09b9)</decision_authority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §9 W8 (commit 7fae09b9)</ref>
    <ref type="related_to" status="complete">ADVI_INFLEC.W5.2 (Inflection entry add — already complete)</ref>
    <ref type="touched_file_current_state">portal/src/lib/firmAccess.ts lines 20-31 — both firms currently allow only `/market`, `/portfolios`, `/advisor-intelligence`</ref>
  </references>

  <objective>
    Extend `portal/src/lib/firmAccess.ts` `FIRM_ALLOWED_PATHS` so BOTH `'49financial'` and `'inflection'` entries include three additional paths: `/cma`, `/positioning`, `/macro`. No other firms, no other paths.

    Sidebar `Analysis` section will become visible for partner firms for the first time — no section-header gating needed (`App.tsx:310-312` already auto-hides empty sections).

    EXPLICIT SCOPE LOCK: Leave `/attribution`, `/factor-tilts`, `/valuations`, `/correlations` OUT. Andrew named three pages; ship exactly three.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/lib/firmAccess.ts — append 3 paths to each of the two partner-firm Sets</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Both `'49financial'` and `'inflection'` Sets gain exactly `/cma`, `/positioning`, `/macro` (no trailing slashes, no query strings). Existing 3 paths retained.</requirement>
    <requirement id="2">No changes to the export surface of `firmAccess.ts` (no new types, no new functions, no signature changes to `isPathAllowedForFirm` or `FIRM_DEFAULT_LANDING`).</requirement>
    <requirement id="3">Commit with `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"` and `--only -- portal/src/lib/firmAccess.ts <session-log-path>`.</requirement>
    <requirement id="4">Ship to DEV only until W8.3 backend smoke returns PASS under both JWTs. If W8.3 escalates to CTO (any 403/404 on /api/general/* or /v1/* under partner JWT), HOLD W8.1 from PROD merge pending CTO resolution.</requirement>
  </requirements>

  <compiler_tools_mandate>
    Phase 1 (before edit):
    <run>grep -rn "publicApiRequest\|apiRequest\|portal-proxy\|/v1/" portal/src/pages/CapitalMarketAssumptions portal/src/pages/Positioning portal/src/pages/Macroeconomics</run> — confirm each page's data fetch surface (feeds W8.3 enumeration).
    <run>comp-routes trace getPositioningData</run>, <run>comp-routes trace getMacroData</run>, <run>comp-routes trace getCMAAssumptions</run> — CF → origin path per endpoint.
    <run>comp-cache collisions</run> — rule out React Query key collisions from the three pages activating for a second firm.

    Phase 2 (before commit):
    <run>comp-transform schema-check CapitalMarketAssumptions</run>
    <run>comp-transform schema-check Positioning</run>
    <run>comp-transform schema-check Macroeconomics</run>
    Expected: 0 MISSING across all three.

    Phase 3 (after commit):
    Re-run Phase 1 `grep` — confirm no data fetch was added during edit that was not enumerated pre-edit.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="portal/src/lib/firmAccess.ts">
      Last-write owner: 0.4.0_DE_ClientPlatform (W5.2 Inflection entry, 2026-04-21). No concurrent pending TO touches this file. W8.1 is the only active writer.
    </shared_resource>
    <sequencing_gate to="W8.2">
      W8.2 (DT frontend-dev under both JWTs) requires W8.1 deployed to DEV. Signal DT on merge.
    </sequencing_gate>
    <sequencing_gate from="W8.3">
      W8.3 (DT backend curl smoke) runs independently but gates W8.1 PROD promotion — if W8.3 finds 403/404 under partner JWT, hold PROD merge.
    </sequencing_gate>
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="1">`FIRM_ALLOWED_PATHS['49financial']` contains 6 paths: the original 3 plus `/cma`, `/positioning`, `/macro`.</ac>
    <ac id="2">`FIRM_ALLOWED_PATHS['inflection']` contains the same 6 paths.</ac>
    <ac id="3">No other firmIds added; internal `opal-capital` behavior unchanged (always true).</ac>
    <ac id="4">`bunx tsc -b portal/` — zero TS errors.</ac>
    <ac id="5">All three `comp-transform schema-check` runs return 0 MISSING.</ac>
    <ac id="6">Portal DEV loads at least one of the three pages under 49F JWT without console error (manual smoke; full matrix is W8.2's job).</ac>
    <ac id="7">Session log with Compiler Tools section appended to `org/compiler-tools-log.md`.</ac>
  </acceptance_criteria>

  <deliverables>
    <deliverable type="commit">portal/src/lib/firmAccess.ts — 6-line edit (3 path entries per firm)</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/{date}/inflec_w8_1_firmaccess_cross_firm.md` with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT add `/attribution`, `/factor-tilts`, `/valuations`, `/correlations` to either firm. Andrew-scoped to three pages only.</rule>
    <rule>Do NOT add new firmIds or modify the `isPathAllowedForFirm` signature.</rule>
    <rule>Do NOT merge to PROD before W8.3 DT backend smoke returns PASS.</rule>
  </do_not>
</task_order>
