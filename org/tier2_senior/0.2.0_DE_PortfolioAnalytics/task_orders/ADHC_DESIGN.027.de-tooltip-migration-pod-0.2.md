# ADHC_DESIGN.027 — Tooltip Migration: Pod 0.2 (PortfolioAnalytics)

**Owner:** `0.2.0_DE_PortfolioAnalytics`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN`
**Depends on:** ADHC_DESIGN.025 (DE 0.4.0 ships `<DataTooltip>` + token flip)
**Priority:** Medium — start once `<DataTooltip>` lands on DEV
**Status:** PENDING (BLOCKED until .025 complete)

---

## Background

See full analysis: `org/tier3_junior/0.4.1_RD_ModelPortfolios/deliverables/tooltip-unification-report.md`

Portal-wide tooltip unification. Canonical reference: `AUATrendChart.tsx:230-266`. This TO migrates all pod 0.2 (PortfolioAnalytics) data tooltips to the shared `<DataTooltip>` component built in TO-025.

**Do not build the component. Do not touch the token. Those are done in TO-025.** Mechanical migration only — delete inline div trees, replace with `<DataTooltip>` calls.

---

## Files to migrate (8 sites across 7 files — all Variant A)

Pattern: `bg-[hsl(var(--bg-header))] border border-white/20 rounded-lg|md px-3 py-2|px-4 py-3 shadow-xl`

### Valuation (2 files, 3 sites — RD 0.2.4 domain)

| File | Lines |
|------|-------|
| `portal/src/pages/Valuation/tabs/ValuationTimeSeriesTab.tsx` | 68 |
| `portal/src/pages/Valuation/tabs/RiskPremiumTab.tsx` | 70, 111 |

### Attribution (1 file, 1 site — RD 0.2.2 domain)

| File | Line |
|------|------|
| `portal/src/pages/Attribution/tabs/HoldingsTab.tsx` | 64 |

### Positioning (1 file, 1 site — RD 0.2.1 domain)

| File | Line |
|------|------|
| `portal/src/pages/Positioning/tabs/HoldingsTab.tsx` | 279 |

### Macroeconomics (3 files, 3 sites — RD 0.2.5 domain)

| File | Line |
|------|------|
| `portal/src/pages/Macroeconomics/tabs/YieldCurveTab.tsx` | 122 |
| `portal/src/pages/Macroeconomics/tabs/VolatilityTab.tsx` | 460 |
| `portal/src/pages/Macroeconomics/components/MacroTimeSeriesModal.tsx` | 173 |

---

## Migration pattern (use for all 8 sites)

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

Import path: `import { DataTooltip } from '@/components/DataTooltip'`.

Typical net deletion: ~50-80 LOC per site.

### Edge cases to watch for

Pod 0.2 tabs tend to have chart tooltips without a "Total" aggregate row (e.g. yield curves show multiple series but no single total). For those, **omit the `aggregate` prop** entirely — the `<DataTooltip>` component handles optional aggregate cleanly:

```tsx
<DataTooltip
  header="10Y Yield Curve — 2026-04-09"
  rows={curveData.map(p => ({ label: p.tenor, value: `${p.yield.toFixed(2)}%` }))}
/>
```

If a chart has no per-series colors (e.g. single-series line charts), omit `row.color` and the component will render rows without swatches. Do NOT insert a fake swatch color just to have one.

---

## Validation

- Visit each of the 4 page areas (Valuation, Attribution, Positioning, Macroeconomics) and hover every chart — silver bg, dark navy text, 2px indigo border
- Confirm aggregate rows that had totals still show them; single-series charts render without a swatch column
- Run `bun run build` — no TypeScript errors

Commit message: `feat(portal): pod 0.2 tooltip migration to DataTooltip (ADHC_DESIGN.027)`

Ping `1.0.0_SA_CTO` and `0.4.0_DE_ClientPlatform` when done.

---

## Out of Scope

- Do NOT touch files owned by other pods (pod 0.1 market-performance, pod 0.4 ClientPlatform pages)
- Do NOT modify `<DataTooltip>` component (read-only dependency from TO-025)
- Do NOT change design tokens (TO-025 handles the one token flip)
- If a chart needs visual variation beyond the canonical, flag it back — don't invent new variants
