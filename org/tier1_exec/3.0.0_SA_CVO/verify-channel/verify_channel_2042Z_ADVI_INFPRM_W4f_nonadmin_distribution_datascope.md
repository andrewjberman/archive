# VERIFY-CHANNEL ANALYSIS — ADVI_INFPRM.W4f non-admin Distribution data-scope (pre-landing, COO-routed)

- **Verifier:** 3.0.0_SA_CVO — analysis anchored to my W4a edge-exemption read (COO data-scope question, 2026-06-02)
- **Timestamp:** 2026-06-02T20:42Z
- **Context:** Andrew pixel-smoke CORRECTED the non-admin model: Inflection non-admins get **[Distribution, Profile]** (Distribution at full fidelity), NOT Profile-ONLY. W4f (FE-only, RD~C-dispatched) reverts the P2-a `&& isFirmAdmin` guard on the distribution branch. This analysis is PRE-W4f-landing.

## P2-a reversal — ACKNOWLEDGED (not a regression)
My P2-a recommendation (guard distribution with `&& isFirmAdmin`, fixed in 328a8459) hardened the **superseded** model (non-admin = Profile-only). Under Andrew's corrected model, distribution is intended-shared, so W4f's removal of that guard is **correct by directive** — when I re-verify W4f, the missing distribution guard is NOT a re-introduced leak. The no-BI-leak invariant shifts to: **Books tab stays admin-only** (Firm-Overview/BI lives there) — that guard (`:254 && isFirmAdmin`) must remain. (Good vindication of the rendered-pixel gate as the model-correctness check — the honest-limit I flagged on the W4b cert.)

## DATA-SCOPE ANSWER: non-admin Distribution advisor-drills are SELF-SCOPED at the edge (.004a)

**Decisive evidence (code-read, both layers):**
- FE: the ADV-cohort relationship-drill (DistributionTab `stackedPeriodsQuery`, W4c) fires `getPlatinumAdvisorSummary(drillParent, ...)` → for Inflection routes to `getPlatinumAdvisorSummaryStaticInflection`, which fetches `${PLATINUM_BASE}/advisors/${advisorId}/book.json` (advisor-intelligence.ts:1081-1093). `PLATINUM_BASE = '/api/scoped/advisor-intelligence/platinum'` (:859).
- Edge: that URI `/api/scoped/advisor-intelligence/platinum/advisors/{advisorId}/book.json` EXACTLY matches the `.004a` `ADVISOR_SCOPING_PATH_PATTERNS[1]` = `/^\/api\/scoped\/advisor-intelligence\/platinum\/advisors\/([^/]+)\/.*\.json$/` (auth-validator-edge index.mjs ~:88).
- `.004a` rule: for a NON-admin, the requested advisorId **must equal `jwt.advisorId`**; admins (`role==='admin' || firmRole==='admin'`) are exempt (`getAllowedAdvisorIds` returns null, ~:196-203). This is the SAME admin-exemption I security-verified in W4a — confirmed firm-safe there.

**Therefore, with non-admin Joe on full Distribution:**
| Surface | Edge behavior | Renders for non-admin Joe? |
|---|---|---|
| Aggregate Distribution (geo/adv donuts, state/city breakdowns, firm timeseries) | firm-aggregate path (partner_analytics), NOT advisor-scoped | YES — same as Peter |
| GEO-cohort state/city drill | firm-aggregate (no per-advisor fetch) | YES |
| ADV-cohort drill into **his own** advisor (joe_x) | `.004a`: advisorId == jwt.advisorId | YES |
| ADV-cohort drill into **another** advisor (peter_lee, patrick) | `.004a`: advisorId != jwt.advisorId | **NO — edge 403 (advisor_scoping_denied)** |

## Implication for W4f sufficiency ("same fidelity as Peter")
W4f FE-only (un-guard distribution) delivers the **aggregate** Distribution at same fidelity (donuts/breakdowns/geo-drill render for non-admins). It does NOT, by itself, deliver **cross-advisor relationship-drill** — the edge `.004a` 403s a non-admin drilling any advisor other than themselves. So:
- If Andrew's "same fidelity" = **aggregate Distribution analytics** (the donuts/breakdowns) → **W4f FE-only SUFFICES**; the per-advisor relationship-drill legitimately stays self-scoped (Joe drills his own book; that's arguably the correct privacy boundary — one advisor shouldn't see another's individual client relationships).
- If Andrew's "same fidelity" = Joe can ALSO drill into **any** advisor's relationship timeseries like Peter → **W4f FE-only is INSUFFICIENT**. It requires an **edge `.004a` change** (relax advisor-scoping for non-admins on the Distribution drill path) — a SECURITY-MODEL decision (should a non-admin advisor see other advisors' client books?), owned by CTO/Andrew, implemented by AE. This is the multilayer-seam class: the FE revert and the edge gate must be co-decided for the rendered intent.

## Recommendation
1. **Smoke probe (decisive):** at the W4f joint smoke, have non-admin Joe drill an advisor OTHER than himself in ADV+AUA Distribution. My code-read predicts a 403 / "No relationship data." That empirically resolves which interpretation holds.
2. **Andrew-intent clarification** (CTO/COO): is non-admin "full Distribution" the aggregate analytics, or also cross-advisor relationship-drill? The privacy implication (advisor-sees-other-advisors'-clients) makes this an explicit decision, not a default.
3. W4f as-FE-only is correct + sufficient for interpretation (a); flag interpretation (b) as needing an edge `.004a` decision BEFORE the smoke concludes "fidelity gap" — so it's not mis-read as a W4f FE defect.

HONEST-LIMIT: code-read prediction; the 403-vs-render is empirically confirmed at the smoke. Anchored to the W4a edge analysis (same admin-exemption mechanism, confirmed firm-safe).
