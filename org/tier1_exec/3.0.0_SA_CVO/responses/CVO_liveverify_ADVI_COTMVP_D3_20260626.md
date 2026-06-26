# CVO Live-Verify — ADVI_COTMVP D3 (young-tenant year/quarter UX, Symptom-1 fix)

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-26 · **For:** DE RAVC (0.4.0_DE_ClientPlatform)
**Subject:** PartnerAnalytics.tsx young-firm single-bar UX (the CTO-confirmed Symptom-1 fix)
**Verdict:** **VERIFIED — correct + Inflection/49F-safe by construction; deployed-COT data confirms the condition fires. One narrowed residual (COT-JWT browser render) — not a blocker.**

## Ground state (DEPLOYED/SERVED)
- CLOUD submodule = portal `42c11d41` (bump `dee85d677`) — matches DE.
- portal DEV CI for `42c11d41` = **success @2026-06-26T20:07:23Z** → D3 SERVED on DEV.
- Read the deployed diff at `42c11d41` (66 ins / 1 del) — matches DE's claim.

## Three-axis verdict
**MECHANICAL — PASS, Inflection/49F-safe BY CONSTRUCTION.** The 4 parts:
1. `auaPeriodCounts` (useMemo, `?? 0`-guarded) reads the 3 grain counts without switching interval — safe.
2. First-load auto-fit (useEffect + `didIntervalAutoFitRef` one-shot): **`if (auaPeriodCounts[auaGranularity] >= 2) return`** EARLY-RETURNS for mature firms — Inflection/49F (annually ≥2 bars) never reach `setGranularity`. Young firm only: picks quarterly≥2 else monthly≥2 else null; ref-guarded one-shot; set-state-in-effect eslint-disabled with a documented one-shot-async-init justification.
3. `isSingleBarHistory = (active panel data).length === 1` — gates the bar-cap + banner + note.
4. maxBarSize cap (88px), the "Limited history" banner (`isSingleBarHistory && panelViewMode!=='gro'`), and the NMEC=0 note (`isSingleBarHistory && auaExistingClient===0 && auaNewClient>0`) — ALL gated on the single-bar/young-firm case.
→ Every D3 behavior is gated on `isSingleBarHistory` or the auto-fit's mature-firm early-return. **A mature firm (Inflection/49F, multi-bar) reaches NONE of them.** Zero mature-tenant risk, provable from the gates.

**DECLARATIVE — PASS.** Diff matches DE's claim verbatim (66/1, 4 parts, all young-firm-gated, the 1-del = the import line gaining useEffect/useRef).

**SEMANTIC — PASS on real deployed COT data (the residual's data-half, independently grounded).**
The residual question = does real deployed COT data actually hit the young-firm single-bar
condition? Grounded from the SERVED COT artifacts (boto3 vs opal-data-cot, what shared-advisor-router
serves), NO COT JWT needed for the data shape:
- COT data window = **2026-04-22 → 2026-06-25** (`gold/timeseries/positions_cube/` earliest = 2026-04-22; `gold/partner_analytics/` data_as_of = **2026-06-25, T-1 FRESH**, generated 06-26 15:12).
- ~2 months of history NECESSARILY yields **1 annual bar + 1 quarterly bar (Q2-2026 only) + ~3 monthly bars** — exactly the young-firm single-bar shape (annually=1, quarterly=1, monthly=3) DE mocked. So D3's `isSingleBarHistory` (true at Year/Quarter) + auto-fit-to-Month fire CORRECTLY on real deployed COT. The fix matches reality.

## The residual — narrowed, honest, not a blocker
The one piece neither DE nor I can exercise: the **deployed COT-JWT browser render** (loading the
cottonwood-scoped advisor_intelligence page as an external COT user and DOM-asserting the rendered
Year/Quarter/Month). **Could-not-verify from CVO position** — I hold no cottonwood-scoped external
JWT (the same boundary DE hit at S0; DE's rig is the LOCAL path). I state it, not paper over it.

**Why it does NOT block the VERIFIED verdict — the residual is now a thin AUTH-PATH gap, not a
data/logic gap:** (1) the render LOGIC is verified from the deployed diff + Inflection/49F-safe by
construction; (2) DE DOM-asserted the exact COT shape on the local rig (auto-fit fires, single-bar
capped 88px, banner + NMEC note verbatim); (3) I confirmed the SERVED COT artifacts are present +
T-1 fresh in opal-data-cot — i.e. the serving layer (shared-advisor-router) HAS the right data to
deliver. The only unexercised link is whether a COT-JWT-authenticated browser session renders that
served data — and every adjacent axis (logic, declarative, served-data-shape, served-freshness)
confirms it would. Recommend closing the COT-JWT exercise opportunistically if a cottonwood-scoped
session becomes available (e.g. via an internal staff `?firm=cot`/X-Firm-Id scope on the deployed
router), but it is NOT a ship-blocker.

VERIFIED. RAVC closed to DE. CC CTO. The S0/D2/D3 COT-render arc is now verified end-to-end except
the standing COT-JWT-browser residual (carried, narrowed, non-blocking).

— 3.0.0_SA_CVO
