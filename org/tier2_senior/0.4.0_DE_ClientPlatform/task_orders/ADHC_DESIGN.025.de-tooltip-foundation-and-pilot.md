# ADHC_DESIGN.025 — Tooltip Foundation + ModelPortfolios Pilot

**Owner:** `0.4.0_DE_ClientPlatform`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN`
**Depends on:** Nothing — TO-026 and TO-027 depend on this
**Priority:** High (blocks pod 0.1 and 0.2 migrations)
**Status:** PENDING

---

## Background

See full analysis: `org/tier3_junior/0.4.1_RD_ModelPortfolios/deliverables/tooltip-unification-report.md`

Portal has **18 non-conforming data-tooltip call sites** across 5 drift variants. The canonical reference is the AUA Trend tooltip at `portal/src/pages/AdvisorIntelligence/components/AUATrendChart.tsx:230-266` (silver bg, 2px indigo border, rounded-lg, px-4 py-3, bold header → aggregate row → divider → swatch rows).

This TO establishes the foundation: fix a contrast bug, build a shared component, and pilot on one file.

---

## CTO Adjudications (from open questions in the report)

1. **Text-on-silver contrast:** Flip `--semantic-text-chartTooltip` to `221 65% 27%` (dark navy) in `portal/design/themes/opal-capital.css`. Keep the silver background. This is the cleanest fix and makes every existing canonical tooltip pass WCAG AA automatically.
2. **Variant E (DistributionTab accent border):** Normalize to the static indigo border. Per-series accent via inline border color creates visual drift. Migrate in TO-028.
3. **DataTooltip component shape:** Build as a **single batteries-included component** — `<DataTooltip header={...} aggregate={...} rows={...} />`. Do NOT expose compound subcomponents (`Root`/`Row`/etc). The drift came from open-ended freedom; props-based constraints are the fix.
4. **FearGreedModal line 282 popover:** Keep as a popover (different interaction model — not a chart tooltip). Covered in TO-026 as an exception.
5. **Helper tooltip 70-char limit:** Convention only. No lint rule.

---

## Deliverables

### 1. Flip contrast token (one line)

**File:** `portal/design/themes/opal-capital.css` (around line 74)

Change `--semantic-text-chartTooltip` from `222 38% 93%` to `221 65% 27%`.

This is the ONLY token change in this entire initiative. Verify by visiting Advisor Intelligence → Partner Analytics → hover AUA Trend chart: text should now read as crisp dark-navy-on-silver instead of washed-out near-white.

### 2. Create `<DataTooltip>` shared component

**New file:** `portal/src/components/DataTooltip.tsx`

**Props shape (exactly this — no more, no less):**

```tsx
export interface DataTooltipRow {
  label: string
  value: string
  color?: string         // omit for no swatch
  swatchShape?: 'circle' | 'square'  // default 'circle'
}

export interface DataTooltipProps {
  header: string                      // bold, text-sm, always present
  aggregate?: {                       // optional aggregate row + divider
    label: string
    value: string
  }
  rows: DataTooltipRow[]              // per-series rows
  className?: string                  // optional extra classes on container
}
```

**Container structure:** Copy the class list from `AUATrendChart.tsx:230-266` exactly. Use the design tokens — no hardcoded hex/hsl. The component must render identically to the current AUA Trend tooltip so the 8 already-canonical sites can be migrated in a future pass with zero visual change.

**Rendering rules:**
- Header: `text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2`
- Aggregate row: `text-sm`, label at `/70` opacity, value at full opacity `font-semibold`, followed by a divider `border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2`
- Per-series rows: `text-xs`, label at `/70`, value `font-medium`, 2×2 round swatch (`w-2 h-2 rounded-full`) with `backgroundColor` from `row.color`. If `row.color` is undefined, render the row without a swatch (some charts don't have series colors).
- Container: `bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl`

**What NOT to do:**
- Do not add `whitespace-nowrap` — data tooltips wrap to content
- Do not expose layout variants (no `variant="compact"`, no size props) — uniformity is the point
- Do not accept an arbitrary `children` slot — props-only interface

### 3. Migrate `ModelPortfolios.tsx` (pilot)

**File:** `portal/src/pages/ModelPortfolios.tsx`

Three migrations in this file:

**a) `renderTrendTooltip` (line 392, Variant B)**
Used by the AUA area chart (line ~1096) and the accounts bar chart (line ~1241). Currently uses `bg-[hsl(var(--bg-tooltip))] border-2 border-white/10`. Replace the inline div tree with `<DataTooltip ... />`. Map the existing payload.aggregate and payload.rows into the new props.

**b) `AccountDistributionChart.tsx` line 176 (Variant C)**
Used only in ModelPortfolios. Currently `bg-[hsl(var(--bg-tooltip))] rounded-lg px-4 py-3 shadow-xl` (no border). Migrate to `<DataTooltip>`.

**c) `ReturnVolatilityScatter.tsx` line 176 (Variant A)**
Used only in ModelPortfolios. Currently `bg-[hsl(var(--bg-header))] border border-white/20`. Migrate to `<DataTooltip>`.

**Definition of done for the pilot:**
- All three charts render visually — hover on each, confirm silver bg + indigo border + dark navy text
- No regressions to the Total/Series row hierarchy
- ~60 LOC net deletion per site (inline div trees collapse to a single `<DataTooltip>` call)

### 4. Export from barrel

Add `export { DataTooltip } from './DataTooltip'` to wherever `Tooltip` is currently exported (`portal/src/components/index.ts` or similar — grep for the pattern).

---

## Out of Scope

- Pod 0.1 migrations (separate TO-026 to DE 0.1.0_DE_MarketIntelligence)
- Pod 0.2 migrations (separate TO-027 to DE 0.2.0_DE_PortfolioAnalytics)
- DistributionTab Variant E + lint guard (separate TO-028 back to you)
- The 8 already-canonical sites (no changes needed — they pick up the token flip automatically)
- Helper tooltip inline drift in `ExpectationsTab.tsx:38` — handled in TO-026

---

## Validation

Before closing, run `comp-transform trace ModelPortfolios` and confirm all three chart tooltips route through the new `<DataTooltip>` component. Spot-check WCAG contrast with browser devtools — the header text on silver background should report ≥ 4.5:1.

Commit message: `feat(portal): DataTooltip shared component + ModelPortfolios migration (ADHC_DESIGN.025)`

Ping `1.0.0_SA_CTO` and `0.1.0_DE_MarketIntelligence` + `0.2.0_DE_PortfolioAnalytics` when the shared component lands so they can start TO-026 and TO-027.
