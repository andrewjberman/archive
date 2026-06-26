# INFMVP.F5 FE-Removal — Pre-Staged GO-Ready Diff (Option-A locked)

**Author:** 0.4.0_DE_ClientPlatform · **Date:** 2026-06-26 · **For:** 2.0.0_SA_COO (pre-stage; apply on Andrew F5-GO + producer-ship)
**Status:** PRE-STAGED — NOT applied. This is the exact FE change, parked GO-ready so the cutover is mechanical the instant the gates clear.

> **Pre-stage only — do not commit to portal yet.** Two gates remain before this applies: (1) Andrew picks **F5** (not Cottonwood); (2) the **producer ships first** — D_01 must emit canonical all-roles into `views.nna.adv` (Option A) BEFORE this FE override is removed, or the donut reverts to architect-scope and re-opens the per-advisor route divergence ADVI_NNAATTR fixed. **Ordering is strict: producer → tie-out PASS → this FE removal.**

---

## 1. The change — ONE block removed, fetch retained

**File:** `portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx`
**Memo:** `nnaSnapshot` (`const nnaSnapshot: PeriodSnapshot | null = useMemo(...)`)

**DELETE lines 2601–2632** (the F5 override: the comment block + the `if (canonicalNna && cohort === 'adv' && ...)` segment-swap). The memo then returns `base` directly — i.e. it reads the producer's `cohortView.donut` (`views.nna.adv`), which under Option A now already carries canonical all-roles values.

### Diff (unified, pre-staged)

```diff
     const base: PeriodSnapshot = {
       donut: cohortView.donut,
       distribution: cohortView.distribution,
       metrics: { aua: Math.abs(cohortView.metrics.nna), client_count: cohortView.metrics.client_count },
     } as PeriodSnapshot

-    // ADVI_INFMVP.F5: override ADV donut segment NNA values with canonical window totals.
-    // ADVI_NNAATTR.TO-2 (AC4 -- RETAINED LOAD-BEARING; CVO #9 verified DIVERGENT 2026-06-22): this override
-    // sources canonical w.nna per-advisor totals (all-roles) onto the ADV donut. CVO's AC4 gate resolved
-    // DIVERGENT on the served artifacts: legacy views.nna.adv is ARCHITECT-scoped + additive (Sigma segments
-    // == firm 102.5M) while canonical is ALL-ROLES + non-additive (49/52 advisors diverge). This override IS
-    // the F-1 cross-route unification AT THE DONUT LAYER -- removing it reverts the donut to architect-scope
-    // and re-opens the per-advisor route divergence ADVI_NNAATTR exists to fix. So KEEP, do NOT remove.
-    // KNOWN FINDING (P2, DS/AE data-layer lane -- NOT a FE removal): this injects all-roles (non-additive ~405M)
-    // values into a donut whose declared whole is architect-additive (102.5M) -> parts-don't-sum-to-whole tension.
-    // The FE override is the correct STOPGAP; the clean fix migrates the partner_analytics views.nna.adv donut
-    // SOURCE to emit canonical all-roles + decides whole-semantics, retiring this override. Until then it STAYS.
-    if (canonicalNna && cohort === 'adv' && base.donut?.segments?.length) {
-      const canonWindow = PERIOD_TO_CANONICAL_WINDOW[selectedPeriod] ?? 'q_current'
-      const firmTotal = canonicalNna.firm.windows[canonWindow]?.nna ?? base.metrics.aua
-      const overriddenSegments = base.donut.segments.map(seg => {
-        const advisorEntry = canonicalNna.advisors[seg.key]
-        const w = advisorEntry?.windows[canonWindow]
-        if (!w) return seg
-        return {
-          ...seg,
-          aua: Math.abs(w.nna),
-          value: w.nna,
-          period_inflows: w.inflows,
-          period_outflows: -Math.abs(w.outflows),
-        }
-      })
-      return {
-        ...base,
-        donut: { ...base.donut, segments: overriddenSegments },
-        metrics: { ...base.metrics, aua: Math.abs(firmTotal) },
-      } as PeriodSnapshot
-    }
+    // ADVI_INFMVP.F5 RETIRED (P2 data-layer migration): the ADV donut now reads canonical all-roles directly
+    // from the producer (views.nna.adv emits canonical per Option A) -- the FE STOPGAP override is no longer
+    // needed. heroMetrics still consumes canonicalNna independently (see below); the fetch is retained.

     return base
-  }, [analyticsData, metric, selectedPeriod, cohort, canonicalNna])
+  }, [analyticsData, metric, selectedPeriod, cohort])
```

### What does NOT change (verified — these keep `canonicalNna` load-bearing)
- **`canonicalNna` fetch (line 925)** — RETAINED. `heroMetrics` (1535–1550) reads `canonicalNna.{firm,state,city,advisor,client}.windows[W]` at every grain, independent of the donut; AdvisorAnalytics + AdvisorPublicProfile also consume it. Removing the fetch would break the hero numbers.
- **`PERIOD_TO_CANONICAL_WINDOW` (line 794)** — RETAINED (heroMetrics window mapping path also references the canonical window vocab).
- Only the dep-array entry `canonicalNna` is dropped from `nnaSnapshot` (no longer referenced inside that memo). `react-hooks/exhaustive-deps` stays clean — verify with the lint gate at apply time.

---

## 2. Apply-time checklist (mechanical, ~10 min once gated)
1. Confirm the producer shipped: `views.nna.adv` (49F + inflection) now carries canonical all-roles segment values + firm window totals (DS/AE RAVC + comp-validate on the served artifact).
2. Apply the §1 diff in the portal DEV tree.
3. `comp-transform schema-check SnapshotDistributionView` + `ternary-audit` (no new undefined; cohort fork intact).
4. `comp-cache collisions` — confirm the canonical query-key still has live consumers (heroMetrics/AdvisorAnalytics/AdvisorPublicProfile) so the retained fetch is justified.
5. **Served tie-out (the acceptance gate):** legacy-overridden render == canonical-sourced render, per advisor × window, on 49F + inflection. Under Option A this is value-invisible to the user (the producer now emits exactly what the override computed). Donut segment values, firm center, distribution histogram unchanged through the cut.
6. `bun run` typecheck clean; commit via safe-commit under DE author; DT QA-gate + DEV push.

---

## 3. Why this is safe to pre-stage now
- It is a **parked artifact**, not a portal commit — zero risk, nothing ships pre-decision.
- Option-A lock (COO) means the FE change is now fully determined: the override comes out, the donut reads the producer. No design ambiguity left on the FE leg.
- If Andrew picks **Cottonwood**, this shelves cleanly (delete the parked doc). If **F5**, the cutover is mechanical — no fresh analysis at GO.

Lane: DE (me) owns this FE removal + the tie-out spec. Gated on DS producer-ship + Andrew F5-GO. RAVC2 to COO.
