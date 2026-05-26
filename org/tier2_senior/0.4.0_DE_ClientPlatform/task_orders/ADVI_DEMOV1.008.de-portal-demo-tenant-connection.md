<task_order>
<metadata>
  <to_id>ADVI_DEMOV1.008</to_id>
  <project>ADVI_DEMOV1</project>
  <title>Portal demo-tenant connection (4 portal items in single coordinated commit; ~3-5h)</title>
  <assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completed>2026-05-26</completed>
  <ship_evidence>
    portal/DEV commit `03a85441` (9 files, +499/-2; 6 items single coordinated commit — 4 PRD-enumerated + 2 COO scope-ratify additives for useTenantLayout LAYOUTS registration + CanonicalFirmId union extension);
    workspace/CLOUD session log commit `bafe89aa6`;
    AC1+AC4+AC5+AC6+AC7 PASS; AC2+AC3 tool-gap deferred (comp-graph multi-"index" component-name collision; structurally satisfied; flagged for CVO comp-* expansion follow-up);
    AC8 RAVC2-Request sent to ws COO 2026-05-26 ~16:00Z;
    ~37min spawn-to-ship wall (Andrew sovereign-direct /allocation #7 ALLOCATION-IMPLICIT-LIFT → MSTR /mstr-spawn 15:23Z → DE-pod-4 revival → ship 16:00Z).
  </ship_evidence>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~15:45Z verbatim: "if all the data is prepared in opal-data-demo, then it is time to connect it to frontend. We should be able to go to Advisor Intelligence portal page and hit the 'Select Partner:' dropdown, select 'Demo', and see all the data populate there in canonical format just how it is already done for 49 Financial and Inflection Wealth Management.")</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_DEMOV1.md v0.4 commit `9ee0b92ec` 2026-05-26 (1.0.0_SA_CTO; Phase 6 Frontend Connection addendum). Full scope + 5 risks + mitigations in PRD §6.1.</ref>
    <ref type="data_prepared_predecessor">ADVI_DEMOV1.007 RAVC2-CLOSED 2026-05-26T~0058Z — opal-data-demo bucket populated; FIRM#demo/META + USER#demo@demo.test/PROFILE in opal-users-v2; demo login authenticates.</ref>
    <ref type="serial_revival_context">DE 0.4 was killed by LD-0014 pre-this-session; Andrew sovereign direct Phase 6 dispatch = implicit revival authorization per /allocation #7 ALLOCATION-IMPLICIT-LIFT (`f7f12d4bb`); parallel to AE 0.7 sovereign-spawn pattern from /allocation #6.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT (read-only portal connection scope; no infra-change per PRD §6.1).</dependency>
    <dependency>ADVI_DEMOV1.007 data preparation complete ✓.</dependency>
    <dependency>portal submodule DEV branch checked out + bun toolchain available.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD v0.4 §6.1 (Phase 6 Frontend Connection) — 4 portal items in single coordinated commit on portal submodule DEV:

1. **`portal/src/api/endpoints/advisor-intelligence.ts`** — add `'demo': 'demo'` to ROUTER_FIRM_SUFFIX
2. **`portal/src/lib/firmAccess.ts`** — add `'demo'` to FIRM_ALLOWED_PATHS (same 8 paths as 49F/inflection) + `'demo': 'demo.test'` to FIRM_EMAIL_DOMAINS
3. **`portal/src/pages/AdvisorIntelligence/_partners/demo/`** — new directory mirroring `_partners/49financial/` (constants.ts + index.tsx + layout.ts + roles.ts); use 49F as template; replace branding/firm-name strings
4. **`portal/src/pages/AdvisorIntelligence/index.tsx`** — add `{ id: 'demo', name: 'Demo' }` to ALL_PARTNER_FIRMS + `'demo': DemoView` to PARTNER_VIEWS

**Single-commit discipline** — all 4 items in one logical change-set so a partial-revert doesn't leave portal in broken intermediate state. Use `.tools/safe-commit.sh` per CLAUDE.md Rule 14a; author = your serial.

**5 risks (PRD §6.1 inline) banked for your awareness — mitigations folded in scope above:**
1. DemoView divergence from 49F/Inflection canonical layout → MITIGATE by mirroring `_partners/49financial/` exactly
2. Hidden firmId hard-branch trip in components consuming `firmOverride` → MITIGATE via comp-transform schema-check + ternary-audit (Phase 1 below)
3. Advisor-empty surface (opal-data-demo may have advisor cohort that renders empty in some panels) → MITIGATE by Andrew UAT (TO-VAL-FE)
4. Portal PROD-strand on cherry-pick promotion → DT pod (TO-009) uses ephemeral worktree per `feedback_portal_prod_promotion_strands_main_tree`
5. Cache-collision on React Query keys → MITIGATE via comp-cache collisions (Phase 1 below)
</scope>

<acceptance_criteria>
- AC1: All 4 portal items modified in single coordinated commit on portal submodule DEV; commit message references this TO + PRD `9ee0b92ec` Phase 6.
- AC2: `comp-transform schema-check AdvisorIntelligence --feature demo` shows no MISSING fields under the new `demo` cohort.
- AC3: `comp-transform ternary-audit AdvisorIntelligence` shows no routing-ternary missing the `demo` branch.
- AC4: `comp-cache collisions` shows no new React Query key collisions involving demo tenant.
- AC5: `bun tsc` clean (no TypeScript errors) on portal submodule.
- AC6: `bun build` clean (no build errors).
- AC7: Local dev-server (`bun run dev`) renders 'Demo' option in partner selector + DemoView mounts on selection (light smoke).
- AC8: RAVC2-Request to ws COO with portal submodule commit hash + comp-transform/cache evidence + bun build output.
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before write) — per CLAUDE.md "Adding new cohort/metric/mode" doctrine:**
- `comp-transform schema-check AdvisorIntelligence --feature demo` — escalate feature-named UNUSED fields to WARN; surface routing-ternary hints
- `comp-transform ternary-audit AdvisorIntelligence` — every `cohort === 'demo'` chain validated; gaps surfaced
- `comp-cache collisions` — React Query key collisions check

**Phase 2 (before commit):**
- `bun tsc` clean
- `bun build` clean
- Local smoke: `bun run dev` + manual select 'Demo' from partner dropdown + confirm DemoView mounts

**Phase 3 (after RAVC2-ACCEPT):**
- TO-009 (DT-pod portal push DEV→PROD) — separate TO; I author + dispatch when AC8 RAVC2-Accepted.
- TO-VAL-FE (Andrew UAT) — separate TO; ships post-TO-009.
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-009 (DT-pod portal push)** — sequential after TO-008 RAVC2-ACCEPT; I'll author + dispatch when your RAVC2-Request lands. DT pod choice deferred to /allocation routing.
- **AE 0.7 on-call** — only if `comp-routes trace` surfaces unexpected gap for `?firm=demo` (already firm-agnostic per ADVI_DEMOV1 §3; unlikely touch). AE 0.7 currently on CDNCOHT TO-001 critical path; would interrupt only if structural blocker.
- **LEDGEH error-envelope regression check** — TO-VAL-FE will include this as risk #6 mitigation; not your concern at TO-008 layer.
</cross_domain_coordination>

<expected_evidence>
- Portal submodule commit hash (DEV branch)
- comp-transform schema-check + ternary-audit + comp-cache collisions outputs
- bun tsc + bun build clean
- Local smoke screenshot OR description (manual partner-selector + DemoView mount)
- Session log with archetype IMPLEMENT
</expected_evidence>

<notes>
**Spawn-with-direction context:** MSTR /mstr-spawn ~15:23Z launched you via Andrew sovereign-direct implicit AC9-lift authorization (per /allocation #7 `f7f12d4bb`). LD-0014 DE-pod-4 question structurally resolved by Andrew's Phase 6 priority.

**Sister AE 0.7 work** (parallel critical path; no conflict): LEDGEH TO-001 CLOSED-bookkeeping `d8b02694f` + CDNCOHT TO-001 shipped `0a9c90b16` ~15:23Z (success-path Cache-Control extension to shared-advisor-router-response L@E). Your Phase 6 work runs in full parallel — different lanes, different deploy surfaces.

**TO-VAL-FE smoke surface (for your awareness, not your TO):** (A) partner-selector visibility "Demo" alongside 49F + Inflection; (B) DemoView renders 3-tab canonical layout; (C) data populates from opal-data-demo across surfaces; (D) no-PII-leak surface-confirmation. Andrew UAT.

**ws COO drives 3-step project-close** after TO-008 + TO-009 + TO-VAL-FE ship (closing ADVI_DEMOV1 fully or carrying .006 + AC5 disjointness banking forward per CY-0124).

**Throughput context (today's fast-lane records):** TO-001 ~50min + TO-002 ~10min + CDNCOHT TO-001 ~15min. If you ship TO-008 in ~30-90min, you join the fast-lane bank.

**Discipline reminders:** XXX.md Step 1b (register / inbox-watch / .comp-graph/.agent_context / safe-commit). Phase 1 compiler mandate runs FIRST (`comp-transform schema-check --feature demo` + `comp-transform ternary-audit` + `comp-cache collisions` per CLAUDE.md "Adding new cohort/metric/mode" pair).

Architectural questions / PRD scope → ws CTO (1.0.0_SA_CTO). Dispatch / RAVC2 / blockers → me (2.0.0_SA_COO).
</notes>
</task_order>
