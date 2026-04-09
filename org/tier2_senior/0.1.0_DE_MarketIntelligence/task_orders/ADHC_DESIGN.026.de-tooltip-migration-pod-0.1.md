# ADHC_DESIGN.026 — Tooltip Migration: Pod 0.1 (MarketIntelligence)

**Owner:** `0.1.0_DE_MarketIntelligence`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN`
**Depends on:** ADHC_DESIGN.025 (DE 0.4.0 ships `<DataTooltip>` + token flip)
**Priority:** Medium — start once `<DataTooltip>` lands on DEV
**Status:** PENDING (BLOCKED until .025 complete)

---

## Background

See full analysis: `org/tier3_junior/0.4.1_RD_ModelPortfolios/deliverables/tooltip-unification-report.md`

Portal-wide tooltip unification. The canonical reference is `AUATrendChart.tsx:230-266`. This TO migrates all pod 0.1 (MarketIntelligence) data tooltips to the shared `<DataTooltip>` component built in TO-025.

**Do not build the component. Do not touch the token. Those are done in TO-025.** Your job is mechanical migration: delete inline div trees, replace with `<DataTooltip>` calls.

---

## Files to migrate (9 sites across 6 files)

All 9 are **Variant A** or **Variant D** — inline div tooltips that need to be replaced with `<DataTooltip>`.

### Market Performance modals (4 files, 6 sites — Variant A)

Pattern: `bg-[hsl(var(--bg-header))] border border-white/20 rounded-lg|md px-3 py-2|px-4 py-3 shadow-xl`

| File | Lines |
|------|-------|
| `portal/src/components/market-performance/FearGreedModal.tsx` | 188, 223, **282** |
| `portal/src/components/market-performance/IndexPerformanceModal.tsx` | 84 |
| `portal/src/components/market-performance/MarketRegimeModal.tsx` | 185 |
| `portal/src/components/market-performance/RSIModal.tsx` | 194 |

**Exception — FearGreedModal line 282:** Per CTO adjudication in TO-025, this is a **floating info popover** (different interaction model from a chart tooltip — it's clickable, not a hover element). Keep it as a popover, but:
- Swap the inline `bg-[hsl(var(--bg-header))] border-white/20` styling to match the `<DataTooltip>` container visuals (silver bg + 2px indigo border + rounded-lg + px-4 py-3 shadow-xl)
- Do NOT convert it to a `<DataTooltip>` component call — it needs to stay a popover because of its interaction model
- Add a code comment explaining why it's the only popover in the migration scope

### Capital Market Assumptions (1 file, 2 sites — Variant A + Helper drift)

| File | Lines | Type |
|------|-------|------|
| `portal/src/pages/CapitalMarketAssumptions/tabs/ExpectationsTab.tsx` | 38 | **Helper tooltip** (not data tooltip) |

The `ExpectationsTab.tsx:38` tooltip is a copy-pasted inline helper tooltip labeled as "canonical indigo tooltip" in the report. It matches the helper visual spec but re-implements it inline. **Replace with the shared `<Tooltip>` component** from `portal/src/components/Tooltip.tsx` — gives you free auto-flip, viewport clamp, and portal rendering.

If this file also has any chart data tooltips, migrate those to `<DataTooltip>` too. Grep the file for `bg-[hsl(var(--bg-` patterns before calling it done.

### Causality Engine (1 file, 1 site — Variant D)

| File | Line | Variant | Notes |
|------|------|---------|-------|
| `portal/src/pages/CausalityEngine/components/ThemeBubbleGalaxy/ThemeBubble.tsx` | 105 | D — hardcoded `bg-slate-900 text-white` | Fully off-theme. Needs full rewrite. |

CausalityEngine is currently **cancelled/deferred** (per `0.1.2_RD_CausalityEngine` status in REGISTRY.md). Migrate anyway — it's a simple mechanical swap and avoids leaving a drift landmine if the page is revived. If the component is difficult to migrate because of its custom bubble-rendering model, flag it back to CTO and we'll exclude it.

---

## Migration pattern (use this for all Variant A sites)

**Before:**
```tsx
<div className="bg-[hsl(var(--bg-header))] border border-white/20 rounded-lg px-3 py-2 shadow-xl">
  <div className="text-white font-bold text-sm mb-2">{label}</div>
  <div className="flex justify-between gap-4">
    <span className="text-white/70 text-xs">Total</span>
    <span className="text-white text-xs font-semibold">{total}</span>
  </div>
  <div className="border-t border-white/20 my-2" />
  {series.map(s => (
    <div key={s.name} className="flex items-center gap-2">
      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: s.color }} />
      <span className="text-white/70 text-xs">{s.name}</span>
      <span className="text-white text-xs ml-auto">{s.value}</span>
    </div>
  ))}
</div>
```

**After:**
```tsx
<DataTooltip
  header={label}
  aggregate={{ label: 'Total', value: total }}
  rows={series.map(s => ({ label: s.name, value: s.value, color: s.color }))}
/>
```

Typical net deletion: ~50-80 LOC per site. Import path: `import { DataTooltip } from '@/components/DataTooltip'`.

---

## Validation

- Visit each of the 4 market-performance modals and hover every chart inside — silver bg, dark navy text, 2px indigo border
- Visit CMA Expectations tab — helper tooltips render via `<Tooltip>` component, no inline re-implementation
- (If migrated) Visit CausalityEngine theme galaxy — bubbles render, tooltip matches canonical
- Run `bun run build` to confirm no TypeScript errors

Commit message: `feat(portal): pod 0.1 tooltip migration to DataTooltip (ADHC_DESIGN.026)`

Ping `1.0.0_SA_CTO` and `0.4.0_DE_ClientPlatform` when done (0.4.0 coordinates the TO-028 final audit sweep).

---

## Out of Scope

- Do NOT touch files owned by other pods (pod 0.2 pages, pod 0.4 ADVI/ClientsTab/ModelPortfolios)
- Do NOT modify `<DataTooltip>` component (read-only dependency from TO-025)
- Do NOT change design tokens (TO-025 handles the one token flip)
- Do NOT add variants, size props, or customization to `<DataTooltip>` — if something doesn't fit, flag it back
