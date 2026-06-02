<task_order>
<metadata>
  <to_id>MDPF_SCOPED.S5</to_id>
  <project>MDPF_SCOPED</project>
  <title>RD-FE: external partner users land on their firm-scoped Model Portfolios view, not Global(All) — consume the auth-resolved firm (generalize to all external partners)</title>
  <assigned_to>0.4.2_RD_AdvisorIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>READY-TO-DISPATCH (decomposed by COO from ws CTO scoping handoff 9de86aae3, Andrew-direct 2026-06-02). Action when the RD FE lane is live — 0.4.2_RD_AdvisorIntelligence~B currently offline; spawn pending MSTR (offline) / Andrew. CTO bundling the spawn into the Andrew-direct escalation alongside AE OPS1.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct; the final FE-scope defect on the MDPF_SCOPED close path. FE-only, single-file, proven in-repo pattern (low risk). Sits alongside the 2026-05-29 reopen D1/D2/D3 lineage.</priority>
  <references>
    <ref type="scoping_brief">docs/briefs/mdpf-inflection-scoped-modelportfolios-login-scope-fix-20260602.md (9de86aae3, ws CTO)</ref>
    <ref type="bug_site">portal/src/pages/ModelPortfolios.tsx:257-259, 696</ref>
    <ref type="reference_pattern">portal/src/pages/AdvisorIntelligence/index.tsx:37-42 (live, correct)</ref>
    <ref type="auth_claims">portal/src/contexts/AuthContext.tsx:110-142, 551-553</ref>
    <ref type="firm_config">portal/src/lib/firmAccess.ts:31-43, 90-97; ModelPortfolios.tsx:151-155</ref>
  </references>
</metadata>

<scope>
**Andrew-direct:** signing into the portal as `peter@inflectionwealth.com` (Inflection Wealth Mgmt), Model Portfolios shows the **Global(All)** view (designed for Opal/internal) instead of the **firm-scoped Inflection** view. Fix so external partner users land on their own firm's scoped Model Portfolios.

## Root cause (single, portal-side — case b: firm mapped but page doesn't consume it)
`portal/src/pages/ModelPortfolios.tsx`:
- L257-258: `const { isInternal, isDev } = useAuth()` — destructures ONLY isInternal/isDev; **never reads claims/claims.firmId**.
- L259: `selectedFirmId` **unconditionally defaults to `'global'`** for every user.
- L696: the partner selector (only control that mutates selectedFirmId) renders **only when `internal`**.
- Every per-firm branch keys off `selectedFirmId !== 'global'` (L267,277,380,452,568,641,...). A non-internal user can never move off `'global'` → permanently pinned to Global(All).

**NOT Inflection-specific — ANY external partner (e.g. a 49F external user) hits the same wall. The fix MUST be general (consume the auth-resolved firm), not an Inflection special-case.**

## Fix shape (mirror the proven AdvisorIntelligence pattern, adapt for the synthetic 'global' id)
```ts
const { isInternal, isDev, claims } = useAuth()
const internal = isInternal() || isDev()
const [selectedFirmId, setSelectedFirmId] = useState<string>('global')   // internal selector state
const effectiveFirmId = internal ? selectedFirmId : (claims?.firmId ?? 'global')
```
- Route ALL downstream data-scoping reads through `effectiveFirmId` instead of `selectedFirmId` (every `selectedFirmId !== 'global'` branch, the two per-firm queries, donut/trend/bell-curve scoping).
- Keep the selector gated to `internal` (external users get NO selector — correct; locked to their firm). Internal users keep today's behavior (selector + Global default = no regression).
- `'opal-capital'` always satisfies isInternal(), so external claims.firmId is only ever a partner slug already in the page's id space (`'inflection'`/`'49financial'`) — no id translation needed beyond the internal→'global' default.

## CRITICAL — React-Query cache-key threading (blast-radius callout, brief §8)
React-Query keys already include `selectedFirmId`. When you switch the scoping variable to `effectiveFirmId`, thread it through the cache keys **consistently** so keys reflect the EFFECTIVE scope — otherwise a stale Global cache can bleed into a firm view. Verify no other code path assumes `selectedFirmId` is the selector state where it should now read `effectiveFirmId`.

## NOT in scope (verified clean by CTO — no AE/DE/DS TO)
- Backend provisioning correct: `opal-users-v2` base-table (PK=USER#peter@inflectionwealth.com, SK=PROFILE) carries firmId="inflection". (The email-index GSI is KEYS_ONLY → returns firmId=null = projection artifact; read the BASE table, ignore the GSI null.)
- claims.firmId flows end-to-end (proven: AdvisorIntelligence already scopes external Inflection users off it).
- Inflection tenant config + per-firm MDPF endpoints already exist + typed.
- LOW-PROBABILITY CONTINGENCY ONLY: if during build you find claims.firmId is NOT in the /auth/me payload (contradicting the AdvisorIntelligence evidence), STOP and flag COO — that would add a small AE task to project firmId into /auth/me. Do not assume; verify claims.firmId arrives before building on it.
</scope>

<acceptance>
**CLOSURE IS A VISUAL SMOKE GATE — NOT data-layer.** This is a rendered-pixel defect (correct data + broken FE passes every data gate but fails the user; feedback_portal_closure_needs_visual_smoke_not_just_data_verification). Closure requires a rendered-view smoke by Andrew or /frontend-dev (ws CTO will review the diff + can run the smoke with Andrew). Headless-Chrome FE smoke is fabric-down, so the rendered-pixel confirmation falls to Andrew/CTO-with-Andrew.

- [ ] AC1 — login as peter@inflectionwealth.com → Model Portfolios shows the **Inflection-scoped** view (7 Inflection models; per-firm donut + trend + bell-curve re-scoped), NOT Global(All).
- [ ] AC2 — a **49 Financial external** user lands on the 49F-scoped view (generality check), NOT Global.
- [ ] AC3 — an **internal/Opal** user (or isDev) still gets the partner selector + Global(All) default (NO regression).
- [ ] AC4 — external user sees **no** partner selector (locked to their firm); switching is internal-only.
- [ ] AC5 — typecheck/lint green; portal DEV `ci.yml` GREEN before any PROD promotion. Deploy via the canonical 5-phase "deploy prod" procedure (Rule 19 ephemeral worktree; main portal tree stays on DEV).

RAVC2 the diff + AC1-AC5 evidence to ws CTO + COO. Deploy to PROD only after Andrew/visual-smoke approves.
</acceptance>

<notes>
Decomposed by COO per ws CTO handoff (Andrew-direct 2026-06-02). Single worker TO (this FE fix); the brief's "TO-2 visual-smoke gate" is folded here as the closure acceptance (performed by Andrew/frontend-dev/CTO-with-Andrew, not a spawned worker). Natural owner 0.4.2_RD_AdvisorIntelligence~B authored the MDPF_SCOPED S1 partner-mode scaffold + the 2026-05-29 reopen D1/D2/D3 fixes + owns the AdvisorIntelligence reference page. MDPF_SCOPED close now has 3 work-inputs: data-axis (CLOSED, 3x-verified), scheduling-axis (OPS1/AE_CloudOps), and this FE login-scope (S5/RD~B). The latter two both gated on MSTR-spawn (offline) → Andrew.
</notes>
</task_order>
