# /verify-channel Mode A — ADVI_INFMVP.F1 client-facing GO: Assets Overview zeroes fix (DEV→PROD, demo-critical)

**Verifier:** 3.0.0_SA_CVO (independent portal-DEV code read — NOT COO/DT self-report). **Requested:** COO 2018Z [CLIENT-FACING GO REQUEST]; CVO GO is the client-facing gate per the rollback-first playbook ([[feedback_rollback_first_client_facing_data_emit_deploy]]). **Time:** 2026-05-28T~2027Z. **Fix:** portal/DEV 7c03cd4b, `PartnerAnalytics.tsx:173`.

## VERDICT: GO (client-facing) — code+structural correctness independently verified airtight across all 5 user×firm paths. Live-pixel render is the sole honest-limit → **GO-with-immediate-post-promotion-verify** (NOT GO-gating-on-smoke).

### The fix
`PartnerAnalytics.tsx:173`: `const tenantLayout = useTenantLayout(firmId ?? firmOverride)` (was `useTenantLayout(firmOverride)`). Root cause: external Inflection users have `firmOverride===undefined` → pre-fix hook returned DEFAULT_LAYOUT (49F-shaped) → `auaDonut.source='gold_aua'` → Assets Overview donut-null + stacked-bar-disabled → all-zeroes for Peter.

### Correctness — VERIFIED (independent read of the prop-resolution chain)
Prop origin traced end-to-end:
- `index.tsx:42` — `firmId = internal ? selectedFirmId : (claims?.firmId ?? '49financial')` → firmId is ALWAYS the resolved partner (internal: dropdown pick; external: JWT claim).
- PartnerView (`inflection/index.tsx:154`, `49financial/index.tsx:169`) — `firmOverride = internal ? firmId : undefined`.
- ⇒ the two props are **either equal** (internal admin: both = partner) **or firmOverride===undefined** (external: firmId = partner). In every case `firmId ?? firmOverride === firmId === the correct partner`.

Resolution table (all 5 paths):
| User | firmId | firmOverride | `firmId ?? firmOverride` | Layout | vs pre-fix |
|---|---|---|---|---|---|
| **External Inflection (Peter)** | inflection | undefined | inflection | INFLECTION | was DEFAULT = **the bug; FIXED** |
| Internal → Inflection | inflection | inflection | inflection | INFLECTION | was INFLECTION (via firmOverride) = **no change** |
| External 49F | 49financial | undefined | 49financial | 49F | was DEFAULT (no-op*) = no behavior change |
| Internal → 49F | 49financial | 49financial | 49financial | 49F | was 49F = no change |
| External demo | demo | undefined | demo | demo | was DEFAULT (no-op*) = no behavior change |

Post-fix Peter → INFLECTION_LAYOUT → `auaDonut.source='partner_analytics_views'` → reads `partner_analytics.json#views.aua` — the SAME populated, non-zero path internal admins already render ($205.5M, magnitude-sane vs Peter's book). Root cause correctly addressed.

### No-regression — VERIFIED (sharpest test: every PartnerAnalytics-consumed layout field)
PartnerAnalytics consumes exactly **5** layout fields (grep-confirmed, complete set):
1. `assetClasses.includesCash` — 49F=false / demo=false / DEFAULT=false ✓
2. `assetClasses.ordered` — all three `['fixed_income','equity','alternatives']` ✓
3. `features.auaDonut.source` — 49F/demo/DEFAULT all `'gold_aua'` ✓
4. `features.barChart.stacked` — 49F/demo/DEFAULT all `false` ✓
5. `tabs.partnerAnalytics.defaultViewMode` — 49F/demo/DEFAULT all `undefined` ✓

(*) ⇒ for external 49F/demo, the explicit layout is **field-identical to DEFAULT_LAYOUT** on every consumed field → the firmId pass is a true behavioral no-op even though the returned object differs. For internal admins (any partner) firmId===firmOverride → identical to prior. **No path regresses.** This independently confirms COO/DT's no-regression claim AND extends it to the internal-admin-viewing-partner path their evidence did not explicitly cover (the path I flagged as the highest a-priori regression risk — refuted by index.tsx:42 + PartnerView firmOverride derivation).

Architectural note: the layout hook correctly uses firmId-first (`firmId ?? firmOverride`) while the DATA fetch uses firmOverride-first (`effectiveFirmKey = firmOverride ?? firmId`, inflection:155) — consistent with the documented scope split (layout/tabs/panels = firmId-scoped; data-source = firmOverride-scoped, TenantLayoutConfig.ts:22-46). The fix does not disturb the data path.

### Honest-limit (Step 3.5) — the ONE unverified axis
The live-external **visual render** (real Peter JWT → `X-Firm-Id` injected at the CloudFront edge by auth-validator-edge) is structurally non-reproducible locally. My verification is code+structural (the resolution logic + every consumed field), which is the strongest assertable axis pre-promotion. The rendered-pixels axis is post-promotion by construction — NOT an evasion.

## Routing
**GO → COO: client-facing gate CLEAR.** Disposition on COO's question (smoke GO-gating vs GO-with-immediate-verify): **GO-with-immediate-verify.** The code+structural correctness is independently verified airtight across all paths; gating the demo-critical promotion on the post-promotion smoke would add no safety beyond the rollback-first net. REQUIRED post-promotion: the real Peter-login smoke runs immediately (Andrew/QA, + DT playwright-internal-inflection belt-and-suspenders). Promote via ephemeral worktree rollback-first (Rule 19). If the post-promotion Peter render still shows zeroes → rollback + reopen (residual would be in the CF-edge X-Firm-Id injection, outside the code path I verified). CC CTO. This closes the F1 ratification COO was holding pending-verify.
