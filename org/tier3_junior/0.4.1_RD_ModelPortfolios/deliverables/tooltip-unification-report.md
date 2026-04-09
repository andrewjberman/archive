# Portal Tooltip Unification — Analysis & Migration Report

**Author:** 0.4.1_RD (Model Portfolios)
**For:** 1.0.0_SA_CTO
**Date:** 2026-04-09
**Status:** Research / proposal — no code edits yet

---

## 1. Goal

Collapse the portal's ad-hoc tooltip styles down to exactly **two canonical types**:

| # | Type | Purpose | Trigger |
|---|------|---------|---------|
| 1 | **Helper tooltip** | Short hint text (<70 chars). Explains a label, toggle, or metric. | Hover on `HelpCircle` question-mark icon |
| 2 | **Data tooltip** | Rich breakdown of a data point — total, series rows, color swatches, dividers. | Hover on a chart element (Recharts / custom SVG / map) |

Everything else — modal-style floating popovers, info panels that look like tooltips, slate-colored variants — gets migrated to one of these two.

The canonical Data tooltip reference is the one currently rendered in **AUA Trend Analysis** on the Advisor Intelligence page (`portal/src/pages/AdvisorIntelligence/components/AUATrendChart.tsx:230`).

---

## 2. Canonical Type 1 — Helper Tooltip

### Single source of truth
`portal/src/components/Tooltip.tsx` — the shared portal-rendered `<Tooltip>` component.
All helper tooltips should use this component. No inline re-implementations.

### Visual spec (from `Tooltip.tsx:186`)
```
bg        : hsl(var(--semantic-action-primary))   // opal brand indigo, 253 74% 56%
border    : 1px solid white/20
radius    : rounded-md    (0.375rem)
padding   : px-3 py-2
text      : text-sm text-white
wrap      : whitespace-nowrap   (forces short copy)
shadow    : shadow-xl
z-index   : Z_INDEX.dropdown
render    : React portal -> document.body  (escapes stacking contexts)
position  : auto flip + viewport clamp (top/bottom/left/right)
delay     : 200ms hover-in
```

### Copy rules
- One line. Under ~70 characters (enforced visually by `whitespace-nowrap`).
- Sentence case, ends with a period.
- Describes *what a thing is* or *what an action does* — not a data value.

### Trigger convention
Always attached to a `HelpCircle` icon, sized 14px, `text-white/40 hover:text-white/70`, placed immediately to the right of a section title or label. `PanelHeader` already wires this up via its `helpText` prop — use it for panel-level help.

### Status
**Already correct in most of the portal.** Helper tooltips already route through the shared component almost everywhere, including all three helper tooltips on Model Portfolios (`ModelPortfolios.tsx:490, 738, 908`). The one known drift is a copy-pasted inline helper in `CapitalMarketAssumptions/tabs/ExpectationsTab.tsx:38` labeled as "canonical indigo tooltip" — it matches the colors but should be switched to the shared component for free auto-flip/clamp.

---

## 3. Canonical Type 2 — Data Tooltip (a.k.a. "AUA Trend style")

### Reference implementation
`portal/src/pages/AdvisorIntelligence/components/AUATrendChart.tsx:230-266`

### Visual spec (exact classes)
```tsx
// Container
<div className="bg-[hsl(var(--semantic-background-chartTooltipBg))]
                border-2 border-[hsl(var(--primary))]
                rounded-lg px-4 py-3 shadow-xl">

  // Header (date / label)
  <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">
    {date_or_label}
  </div>

  // Aggregate row (Total / Avg / etc.)
  <div className="flex items-center justify-between gap-6 mb-2">
    <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">
      {aggregate_label}
    </span>
    <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">
      {aggregate_value}
    </span>
  </div>

  // Divider
  <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />

  // Per-series rows
  <div className="space-y-1">
    {rows.map(row => (
      <div className="flex items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full"
               style={{ backgroundColor: row.color }} />
          <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">
            {row.label}
          </span>
        </div>
        <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
          {row.value}
        </span>
      </div>
    ))}
  </div>
</div>
```

### Design tokens used
| Purpose | Token | Resolved value (opal-capital theme) |
|---------|-------|-------------------------------------|
| Background | `--semantic-background-chartTooltipBg` | `hsl(222 24% 81%)` — light silver |
| Border | `--primary` → `--semantic-action-primary` | `hsl(253 74% 56%)` — opal indigo, 2px |
| Text (primary) | `--semantic-text-chartTooltip` | `hsl(222 38% 93%)` |
| Text (secondary) | same at `/70` opacity | — |
| Divider | same at `/20` opacity | — |
| Radius | `rounded-lg` | 0.5rem |
| Padding | `px-4 py-3` | — |
| Shadow | `shadow-xl` | — |

### Structural rules (what makes a data tooltip "canonical")
1. **Silver background + 2px indigo border.** Not `border-white/20` or `border-white/10`.
2. **Rounded-lg**, not `rounded-md`.
3. **px-4 py-3 container**, not `px-3 py-2` (helper spacing).
4. **Bold header row** at `text-sm` showing the primary label/date.
5. **Optional aggregate row** at `text-sm` for totals, then a divider.
6. **Per-series rows** at `text-xs` with a 2x2 round color swatch, label at `/70` opacity, value at full opacity `font-medium`.
7. **No `whitespace-nowrap`.** Data tooltips wrap / size to content; they're not constrained like helper tooltips.
8. Renders via Recharts `content=` prop or a custom hover handler — not through `components/Tooltip.tsx`.

---

## 4. Contrast observation (please adjudicate)

`--semantic-background-chartTooltipBg` (`222 24% 81%` — silver, 81% lightness) paired with `--semantic-text-chartTooltip` (`222 38% 93%` — near-white, 93% lightness) is a **~1.6:1 contrast ratio** — fails WCAG AA.

The archived light theme at `portal/docs/archive/unused-themes/opal-capital.light.css:47` defined `--semantic-text-chartTooltip: 221 65% 27%` (dark navy). That pairs with the silver background at roughly 8:1 — passes AA.

Current `portal/design/themes/opal-capital.css:74` uses the near-white value, which reads as a merge artifact from the dark/light theme collapse. On screen, the 2px indigo border and bold font weight mask the problem, but the body text is washed out.

**Recommendation:** flip `--semantic-text-chartTooltip` in `design/themes/opal-capital.css` to `221 65% 27%` (the archived light-theme value). This keeps the AUA Trend look identical except that the text becomes crisp dark-navy-on-silver. No component code changes required — every existing canonical tooltip picks it up automatically.

If CTO disagrees with flipping the token (e.g. wants the tooltip to stay white-text), the alternative is to darken the background: swap `--semantic-background-chartTooltipBg` to `var(--navy-tooltip)` / `221 44% 10%`. That gives white-on-dark-navy with the same indigo border — a different aesthetic but also WCAG-compliant.

---

## 5. Non-conforming tooltip inventory (portal-wide)

Everything below renders as a data tooltip but does **not** match the AUA Trend canonical. Sorted by variant.

### Variant A — "Navy header + white/20 border"  (13 call sites)
`bg-[hsl(var(--bg-header))] border border-white/20 rounded-lg|md px-3 py-2|px-4 py-3 shadow-xl|2xl`

This is the dominant drift pattern. Dark navy background (#151f36-ish), thin white border, no indigo accent.

| File | Line |
|------|------|
| `portal/src/components/market-performance/FearGreedModal.tsx` | 188, 223, 282 |
| `portal/src/components/market-performance/IndexPerformanceModal.tsx` | 84 |
| `portal/src/components/market-performance/MarketRegimeModal.tsx` | 185 |
| `portal/src/components/market-performance/RSIModal.tsx` | 194 |
| `portal/src/components/ReturnVolatilityScatter.tsx` | 176 |
| `portal/src/pages/Valuation/tabs/ValuationTimeSeriesTab.tsx` | 68 |
| `portal/src/pages/Valuation/tabs/RiskPremiumTab.tsx` | 70, 111 |
| `portal/src/pages/Attribution/tabs/HoldingsTab.tsx` | 64 |
| `portal/src/pages/Positioning/tabs/HoldingsTab.tsx` | 279 |
| `portal/src/pages/Macroeconomics/tabs/YieldCurveTab.tsx` | 122 |
| `portal/src/pages/Macroeconomics/tabs/VolatilityTab.tsx` | 460 |
| `portal/src/pages/Macroeconomics/components/MacroTimeSeriesModal.tsx` | 173 |

Note: the FearGreedModal `line 282` is a floating info popover, not a chart tooltip. It's visually a tooltip so the inventory still applies, but the refactor may need to keep it as a popover component rather than a Recharts tooltip.

### Variant B — "Navy tooltip + white/10 border"  (1 call site — **Model Portfolios target**)
`bg-[hsl(var(--bg-tooltip))] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl`

| File | Line | Notes |
|------|------|-------|
| `portal/src/pages/ModelPortfolios.tsx` | 392 | `renderTrendTooltip` — used by both the AUA area chart (1096) and the accounts bar chart (1241). **This is the first planned edit.** |

Close to canonical in layout (aggregate row + divider + swatch rows, `px-4 py-3`, `rounded-lg`) but uses the dark navy bg and a `white/10` border instead of the silver bg + indigo border.

### Variant C — "Navy tooltip, no border"  (1 call site)
`bg-[hsl(var(--bg-tooltip))] rounded-lg px-4 py-3 shadow-xl`

| File | Line |
|------|------|
| `portal/src/components/AccountDistributionChart.tsx` | 176 |

### Variant D — "Slate-900 floating bubble"  (1 call site)
`bg-slate-900 text-white p-4 rounded-lg shadow-2xl z-50`

| File | Line |
|------|------|
| `portal/src/pages/CausalityEngine/components/ThemeBubbleGalaxy/ThemeBubble.tsx` | 105 |

Fully off-theme (hardcoded slate). Needs full rewrite to canonical.

### Variant E — Dynamic accent-color border (edge case)
| File | Line | Notes |
|------|------|-------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | 2629 | Uses the silver bg but a per-series accent border via inline style. Adjudicate: keep as an allowed variation, or force to indigo? |

### Already canonical (8 call sites — reference / do-not-touch)
- `AdvisorIntelligence/components/AUATrendChart.tsx:230`
- `AdvisorIntelligence/components/AUACompositionChart.tsx:125`
- `AdvisorIntelligence/tabs/DistributionTab.tsx:769, 1463`
- `AdvisorIntelligence/ClientDetail/panels/TimeSeriesPanel.tsx:90`
- `AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx:171`
- `AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx:187`

---

## 6. Proposed migration plan

1. **Flip text token** (one line in `design/themes/opal-capital.css`) — fixes contrast on all 8 already-canonical sites plus every migrated site. *Or* CTO picks the navy-background alternative.
2. **Create a shared `<DataTooltip>` component** at `portal/src/components/DataTooltip.tsx` that wraps the canonical container + header + aggregate + divider + rows layout. Exposes a props shape that maps directly onto Recharts `content` payloads. Current call sites each re-implement the same div tree — a shared component deletes ~60 lines per site and enforces the spec structurally.
3. **Migrate Model Portfolios first** (`ModelPortfolios.tsx:363` `renderTrendTooltip`). This is the pilot — one file, two charts, clean before/after diff.
4. **Migrate Variant A (13 sites).** Most are simple swaps: replace the navy-bg div with `<DataTooltip>`.
5. **Migrate Variants B/C/D (3 sites).**
6. **Adjudicate Variant E** (DistributionTab accent-color border) — either allow as documented exception or normalize.
7. **Delete the inline helper in `ExpectationsTab.tsx:38`**, replace with `<Tooltip>` component.
8. **Add an ESLint rule** (or at minimum a `CONTRIBUTING` note) forbidding inline `bg-[hsl(var(--bg-header))] border border-white/20 rounded-lg` patterns that render chart tooltips. Forces new charts through `<DataTooltip>`.

Total surface area: **18 call sites** to migrate, **1 token** to flip, **1 new shared component** to create.

---

## 7. Open questions for CTO

1. **Text-on-silver contrast:** flip `--semantic-text-chartTooltip` to dark navy (recommended), or flip `--semantic-background-chartTooltipBg` to dark navy and keep white text?
2. **Variant E (per-series accent border):** keep as allowed customization of the canonical data tooltip, or normalize to the static indigo border?
3. **DataTooltip component shape:** do you want it as a low-level primitive (`<DataTooltip.Root>`, `<DataTooltip.Row>`, etc.) or a single batteries-included component that takes `header`, `aggregate`, `rows[]` props? My recommendation: the single-shot props-based component — the drift comes from open-ended freedom, and almost every existing tooltip uses the same header+aggregate+rows shape.
4. **FearGreedModal line 282 floating popover:** migrate to DataTooltip or leave as a popover (different interaction model)?
5. **Helper tooltip character limit:** enforce `<70` in code (truncation / lint rule) or leave as convention?

Once decisions 1 and 3 are made, the migration is mechanical and I can land it file-by-file starting with `ModelPortfolios.tsx`.
