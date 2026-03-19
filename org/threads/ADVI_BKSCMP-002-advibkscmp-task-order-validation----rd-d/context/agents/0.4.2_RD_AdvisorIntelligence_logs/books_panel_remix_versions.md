# Books Panel Remix — Version Log

**Session:** 2026-03-18
**Agent:** 0.4.2_RD_AdvisorIntelligence
**File:** `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`
**Group:** `CanonicalBookView` — 4 panels rendered at every drill level (N1/L2/L3/L4)

---

## Panel Map

| Panel | Function | Location |
|-------|----------|----------|
| Firm Overview | `OverviewPanel` | Row 1 of `CanonicalBookView` |
| Asset Class Mix | Left half of `CompositionPies` | Row 2 of `CanonicalBookView` |
| Top Holdings | Right half of `CompositionPies` | Row 2 of `CanonicalBookView` |
| Cost Basis & Tax Liability | `TaxCostBasisPanel` | Row 3 of `CanonicalBookView` |

---

## v0 — Baseline (pre-session)

**Overview:** Grid of flat `bg-white/5` `MetricCard` tiles. Total AUA `text-xl`, others `text-sm`. No hierarchy.
**Mix:** Small donut (pieR=70), 11px legend text, plain rows.
**Holdings:** Duplicate donut pie + scrollable text list, same visual style as Mix.
**Tax:** h-3 stacked bar, `TaxRow` dot+label+pct+amount rows, bare `<table>` for cost basis / gain positions.

---

## v1 — 2026-03-18 — "Remix Group"

**Portal DEV commit:** (pending)
**Changes:** All 4 panels redesigned. `OverviewPanel` extracted as named function.

### Overview Panel v1
- AUA hero: `text-4xl font-black`, labeled with `text-[10px] uppercase tracking-widest`
- Secondary metrics: horizontal segmented strip, `flex` with `border-r` dividers, `text-lg font-bold` values
- `as of {date}` shown inline below AUA

### Asset Class Mix v1
- Larger pie: `pieR=86`, height 200px
- Legend: each item has a mini proportional bar (`h-1 bg-white/10`) filled to the item's actual % allocation
- Opacity dimming on deselect: 0.2 (was 0.3)
- Click interaction preserved

### Top Holdings v1
- **Dropped duplicate pie** — replaced with ranked horizontal bar list
- Each row: rank number (mono) | name (truncated) | pct | colored bar scaled to top holding
- Bar color = asset_class color of each holding
- "Other" bucket shown at bottom in dimmed italic style
- `maxHeight: 240px` scrollable

### Cost Basis & Tax v1
- Stacked bar: `h-5` (was h-3), percentage label inside segments >= 10%
- Tax status: **3 cards** (Taxable / Tax Deferred / Tax Free) with colored border/bg, amount + pct
- Capital Gains TTM: standalone row, `text-lg font-bold`, emerald/red colored
- Tables (cost basis by year, top gain positions): wrapped in `rounded-lg border` card, alternating row stripes, `bg-white/[0.04]` header
- Term badges on gain positions: `bg-amber-500/15 text-amber-400` (Short) / `bg-emerald-500/15 text-emerald-400` (Long)

---

## v2 — 2026-03-18 — "Remix Overview"

**Portal DEV commit:** `b58a3d5`
**Scope:** `OverviewPanel` only + N1 metric order fix

### Overview Panel v2
- 3 equal `flex-1` cards in a horizontal row: AUA | Clients | Accounts
- AUA card: indigo — `border-indigo-500/25`, `bg-gradient-to-br from-indigo-500/15 to-indigo-500/5`, `text-3xl font-black`
- Clients card: sky/cyan — `border-sky-500/25`, `from-sky-500/15 to-sky-500/5`, colored dot + label
- Accounts card: emerald — `border-emerald-500/25`, `from-emerald-500/15 to-emerald-500/5`
- Other label→color mappings in `METRIC_CARD_STYLE`: NNA=violet, Tax Status=amber, Positions=purple
- Each card: colored dot, colored label text (`text-[10px] uppercase tracking-widest`), white value
- N1 call site metric order fixed: Clients before Accounts (so cards read AUA → Clients → Accounts)

---

## Recall Instructions

To recall a specific panel version, restore the function body from the description above.
To recall v0 for any panel, use `git show HEAD~n:portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` and cherry-pick the function.
