# AdvisorIntelligence Mobile Readiness Audit

**Agent:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-04-07
**Task Order:** ADHC_DESIGN.022
**Viewport target:** 375px-428px (iPhone SE / iPhone 14)

---

## Executive Summary

AdvisorIntelligence is currently **desktop-only**. At 375px, every tab has critical
layout failures. The page was designed for 1440px+ with fixed-width sidebars,
fixed-size charts, and data-dense tables. Mobile adaptation would require significant
restructuring, not just responsive class additions.

**Tab mobile value assessment:**
- **Books (ClientsTab):** HIGH mobile value -- advisors checking client AUA on the go
- **Advisors (AdvisorsTab):** MEDIUM -- leaderboard/NNA glanceable on mobile
- **Distribution (DistributionTab):** LOW -- complex charts need large viewports
- **PartnerAnalytics header:** MEDIUM -- summary metrics useful, charts less so

---

## 1. Critical Issues (Page-Breaking at 375px)

### 1.1 Fixed-Width Sidebars Overflow Viewport

| File | Line | Value | Impact |
|------|------|-------|--------|
| DistributionTab.tsx | 663 | `w-[280px]` sidebar | 280px + flex-1 chart = content exceeds 375px |
| DistributionTab.tsx | 906 | `w-[280px]` sidebar | Same -- continuous NNA view |
| DistributionTab.tsx | 1257 | `w-[280px]` sidebar | Same -- continuous AUA view |
| DistributionTab.tsx | 1592 | `w-[280px]` sidebar | Same -- CLA continuous view |

These are the "hero metrics + legend" panels that sit left of chart content. At 375px,
280px sidebar + any chart = overflow. Needs `hidden` on mobile or vertical stack.

### 1.2 Fixed-Size ApexCharts Donuts

| File | Line | Size | % of 375px |
|------|------|------|------------|
| DistributionTab.tsx | 2231 | `width={340} height={340}` | 91% -- only 35px margin |
| ClientsTab.tsx | 1001 | `width={220} height={220}` | 59% -- forces surrounding layout |
| DistributionTab.tsx | 3126 | `PieChart width={200} height={200}` | 53% -- plus legend beside it |

ApexCharts donut `width`/`height` are hardcoded integers, not responsive.
Must wrap in a responsive container or use CSS to constrain.

### 1.3 Tables Without Horizontal Scroll

| File | Line | Table | Columns | Issue |
|------|------|-------|---------|-------|
| ClientsTab.tsx | 1382 | OpenLotsTable | 8 (Name, Ticker, Qty, Cost, Value, Gain, Term, Date) | `overflow-x-auto` present -- OK |
| ClientsTab.tsx | 1477 | ClientsTable | 3+ (Client, AUA, arrow) | `overflow-x-hidden` -- horizontal scroll **disabled** |
| ClientsTab.tsx | 1204 | Cost Basis table | 4-5 | No scroll wrapper |
| ClientsTab.tsx | 1237 | Top Gains table | 4-5 | No scroll wrapper |
| ClientsTab.tsx | 1515 | AccountsTable | 7 (ID, Tax, AUA, Inflows, Outflows, NNA, Positions) | `overflow-x-auto` -- OK |

### 1.4 Non-Responsive Grid Layouts

| File | Line | Pattern | Issue |
|------|------|---------|-------|
| ClientDetailPage.tsx | 108 | `grid grid-cols-2 gap-6` | Fixed 2-col; needs `grid-cols-1 md:grid-cols-2` |
| ClientDetailPage.tsx | 117 | `grid grid-cols-2 gap-6` | Same |

### 1.5 MetricSelector Too Wide

| File | Line | Value | Impact |
|------|------|-------|--------|
| MetricSelector.tsx | 41 | `min-w-[280px]` | Exceeds 375px with padding; dropdown unusable |

---

## 2. Warnings (Degraded but Functional)

### 2.1 Fixed Chart Heights

| File | Line | Value | Component |
|------|------|-------|-----------|
| AUATrendChart.tsx | 174 | `height={450}` | Main trend chart -- too tall for mobile |
| AUACompositionChart.tsx | 78 | `height={400}` | Composition chart |
| DistributionTab.tsx | 2161 | `h-[450px]` | Snapshot distribution chart |
| DistributionTab.tsx | 2347 | `h-[450px]` | Snapshot distribution chart |
| PartnerAnalytics.tsx | 1065 | `min-h-[400px]` | Main chart area |
| TimeSeriesPanel.tsx | 52 | `h-[320px]` panel | Client detail chart |
| ConcentrationPanel.tsx | 120 | `h-[320px]` panel | Holdings chart |
| MixTimeseriesPanel.tsx | 94 | `h-[320px]` panel | Mix chart |
| PortfolioBalancePanel.tsx | 34 | `h-[320px]` panel | Tax pie chart |

Mobile recommendation: `h-[250px] md:h-[320px] lg:h-[450px]` pattern.

### 2.2 min-w Constraints on Metric Tiles

| File | Line | Value | Count |
|------|------|-------|-------|
| PartnerAnalytics.tsx | 1993-2061 | `min-w-[180px]` | 6 metric tiles |
| PartnerAnalytics.tsx | 2133-2155 | `min-w-[160px]` | 3 GRO tiles |
| DistributionTab.tsx | 2462-2604 | `min-w-[100px]` | 6+ toggle buttons |
| DimensionSelector.tsx | 41 | `min-w-[160px]` | Select dropdown |

At 375px with 2 tiles at `min-w-[180px]` = 360px + gap = overflow.
Needs `flex-wrap` (present in some cases) but tiles become single-column.

### 2.3 Chart Axis Labels Overlap

| File | Line | Issue |
|------|------|-------|
| AUATrendChart.tsx | 174 | XAxis `height={80}`, angle=-45, 80px consumes 18% of 450px chart height |
| AUACompositionChart.tsx | 78 | XAxis `height={60}`, angle=-45, labels overlap at narrow widths |
| DistributionTab.tsx | 3203 | bottom margin 50px, XAxis angle=-45, interval=0 (all bins shown) |
| DistributionTab.tsx | 730 | YAxis margin `left: 0` clips currency labels |
| DistributionTab.tsx | 1045 | YAxis margin `left: 0` clips currency labels |
| DistributionTab.tsx | 945 | YAxis `width={60}` = 16% of 375px viewport |

---

## 3. Touch Targets Under 44px

### 3.1 Toggle Buttons (CRITICAL -- primary navigation)

| File | Line | Padding | Est. Height | Element |
|------|------|---------|-------------|---------|
| DistributionTab.tsx | 418 | `px-2.5 py-1` | ~28px | View toggle (Snapshot/Continuous) |
| DistributionTab.tsx | 440 | `px-2.5 py-1` | ~28px | Cohort toggle (GEO/ADV) |
| DistributionTab.tsx | 462 | `px-2.5 py-1` | ~28px | Metric toggle (AUA/NNA/CLA) |
| PartnerAnalytics.tsx | 914 | `px-3 py-1.5` | ~32px | Mode toggle |
| PartnerAnalytics.tsx | 1053 | `px-2.5 py-1` | ~28px | Sub-mode toggle |
| AUATrendChart.tsx | 136 | `px-3 py-1.5` | ~32px | View mode toggle |
| AdvisorsTab.tsx | 125 | `px-2.5 py-1` | ~28px | Metric/period toggles |

### 3.2 List Items

| File | Line | Padding | Est. Height | Element |
|------|------|---------|-------------|---------|
| DistributionTab.tsx | 713 | `px-2 py-1` | ~28px | Segment drill-down list item |
| DistributionTab.tsx | 1373 | `px-1 py-0.5` | ~20px | Legend list item (clickable) |
| DistributionTab.tsx | 1657 | `px-1 py-0.5` | ~20px | Legend list item (clickable) |
| ClientsTab.tsx | 655 | `px-3 py-2.5` | ~38px | Advisor dropdown item |

### 3.3 Select Dropdowns

| File | Line | Padding | Element |
|------|------|---------|---------|
| PartnerAnalytics.tsx | 973 | `px-3 py-1.5` | Firm picker dropdown |
| AUATrendChart.tsx | 154 | `px-3 py-1.5` | Window selector |
| AssetIntelligenceTab.tsx | 161 | `px-3 py-1.5` | Dimension selector |

---

## 4. Charts Audit

### 4.1 Recharts (ResponsiveContainer)

All Recharts charts use `ResponsiveContainer width="100%"` which adapts width.
Issues are:
- Fixed heights that are too tall for mobile
- Axis labels that overlap at narrow widths
- Margin `left: 0` clipping Y-axis labels
- Legend placement assumes wide viewport

### 4.2 ApexCharts (Fixed Integer Dimensions)

ApexCharts donuts use `width={N} height={N}` -- **not responsive**.
These are the most critical chart issues:
- DistributionTab.tsx:2231 -- 340x340
- ClientsTab.tsx:1001 -- 220x220

Fix: Wrap in a div with `max-w-full` and use `width="100%"` or calculate
dynamically from parent ref.

### 4.3 Recharts PieChart (Fixed Dimensions)

- DistributionTab.tsx:3126 -- `PieChart width={200} height={200}`
  with fixed `cx={100} cy={100} innerRadius={60} outerRadius={92}`

Unlike ApexCharts, Recharts PieChart can use ResponsiveContainer.
Migrate to: `<ResponsiveContainer width="100%" height={200}>`

---

## 5. Tables Audit

| Table | File:Line | Columns | Scroll | Sticky | Mobile Strategy |
|-------|-----------|---------|--------|--------|----------------|
| OpenLotsTable | ClientsTab:1382 | 8 | `overflow-x-auto` | Header sticky | Horizontal scroll OK; needs sticky first col |
| ClientsTable | ClientsTab:1477 | 3 | `overflow-x-hidden` | Header sticky | FIX: change to overflow-x-auto; 3 cols could stack |
| AccountsTable | ClientsTab:1515 | 7 | `overflow-x-auto` | Header sticky | OK; needs sticky first col |
| Cost Basis | ClientsTab:1204 | 4-5 | None | None | NEEDS scroll wrapper |
| Top Gains | ClientsTab:1237 | 4-5 | None | None | NEEDS scroll wrapper |
| Snapshot | AssetIntelligenceTab:186 | Variable | `overflow-auto` | None | OK but no sticky cols |
| AdvisorSummary | ClientsTab:1585 | Card layout | N/A | N/A | Cards stack -- OK |

---

## 6. Text Audit (Sub-12px)

### 6.1 9px Text (ILLEGIBLE on mobile)

| File | Line | Usage |
|------|------|-------|
| ClientsTab.tsx | 1167 | `text-[9px]` -- tax status percentage in stacked bar |
| ClientsTab.tsx | 1261 | `text-[9px]` -- term badge (Short/Long) |
| ClientsTab.tsx | 1360 | `text-[9px]` -- term badge function |
| ClientsTab.tsx | 1443-1457 | `text-[10px]` lot detail rows (9 instances) |

### 6.2 10px Text (Hard to Read on Mobile)

**Pervasive across ClientsTab.tsx:** Lines 837, 840, 846, 850, 856, 860, 866,
870, 973, 976, 984, 995, 1053-1086, 1099-1103, 1158, 1181, 1184, 1207-1260,
1386-1393, 1480-1526, 1612, 1620, 1628, 1634, 1643, 1660.

**Also in:** PartnerAnalytics.tsx (control labels, metric panels),
DistributionTab.tsx (axis labels, control labels), AdvisorsTab.tsx (tooltips).

### 6.3 11px Text

| File | Line | Usage |
|------|------|-------|
| ClientsTab.tsx | 770, 777 | Metric panel labels |
| ClientsTab.tsx | 1085-1086 | Holdings labels |

---

## 7. Design Flaws

### 7.1 Two-Column Layouts Without Collapse Points

The DistributionTab uses a `flex` with `w-[280px]` sidebar + `flex-1` chart
at 4 different locations. These have no breakpoint-driven collapse.
At 1024px this is marginal; at 375px it's broken.

**Recommendation:** `hidden md:flex md:w-[280px]` for sidebar, with a
collapsible drawer or bottom sheet on mobile.

### 7.2 Metric Tile Rows Without Flex-Wrap

PartnerAnalytics.tsx has rows of 2-3 metric tiles with `min-w-[160px]`/`min-w-[180px]`.
While `flex-wrap` is present in some places, the tiles wrap to single column
but don't adjust their internal layout (still centered, still wide padding).

### 7.3 Tooltip Width

Multiple tooltips use `min-w-[200px]` which at 375px leaves only 175px margin.
Combined with portal-rendered tooltips, these can extend off-screen.

### 7.4 Fixed-Position Chart Labels

DistributionTab.tsx:2798 uses hardcoded `style={{ top: '30px', bottom: '50px',
left: '-20px', width: '16px' }}` for Y-axis label positioning. These pixel
values won't adapt to mobile chart sizing.

---

## 8. Enhancement Opportunities

### 8.1 Progressive Disclosure (HIGH impact)

- **Books tab:** Show only the overview panel + client list on mobile.
  Tax panel, cost basis, and concentration charts collapse into expandable
  accordions. Advisors check client AUA/NNA on mobile -- tax details are
  secondary.

- **Distribution tab:** Show only the donut + legend on mobile (snapshot mode).
  Continuous charts and bell curves are desktop features. Hide sidebars;
  show legend as collapsible below chart.

- **PartnerAnalytics header:** Show only the current period metric tiles
  on mobile. Collapse chart into "View chart" button.

### 8.2 Swipeable Tab Pattern

The 3-tab navigation (Distribution / Advisors / Books) should support
horizontal swipe gestures on mobile. Standard pattern with CSS `scroll-snap`.

### 8.3 Simplified Mobile Table Views

For 7-8 column tables (AccountsTable, OpenLotsTable), consider:
- Card view on mobile: each row becomes a card with key-value pairs
- Keep table view on desktop with `hidden md:table` / `md:hidden`

### 8.4 Responsive Chart Heights

Replace all `h-[450px]` / `h-[320px]` with responsive variants:
```
h-[250px] md:h-[320px] lg:h-[450px]
```

### 8.5 ApexCharts Responsive Config

ApexCharts supports `responsive` option:
```js
responsive: [{
  breakpoint: 480,
  options: { chart: { width: 280 } }
}]
```
Use this instead of fixed width/height.

### 8.6 Touch-Friendly Toggle Buttons

All toggle buttons (`py-1`, `py-1.5`) should use `py-2.5` minimum on mobile
to reach 44px touch targets. Pattern: `py-1.5 md:py-1.5` (same on desktop,
larger on mobile via base class).

---

## Files Covered

| File | Findings |
|------|----------|
| AdvisorIntelligence.tsx | 1 (page layout OK) |
| components/PartnerAnalytics.tsx | 25+ |
| components/AUATrendChart.tsx | 5 |
| components/AUACompositionChart.tsx | 3 |
| components/AUACompositionChart.tsx | 3 |
| components/DimensionSelector.tsx | 1 |
| components/MetricSelector.tsx | 1 |
| components/HeaderMetrics.tsx | 0 (already responsive) |
| tabs/DistributionTab.tsx | 40+ |
| tabs/AdvisorsTab.tsx | 15+ |
| tabs/ClientsTab.tsx | 45+ |
| tabs/AssetIntelligenceTab.tsx | 3 |
| ClientDetail/ClientDetailPage.tsx | 2 |
| ClientDetail/panels/TimeSeriesPanel.tsx | 2 |
| ClientDetail/panels/PortfolioBalancePanel.tsx | 2 |
| ClientDetail/panels/MixTimeseriesPanel.tsx | 2 |
| ClientDetail/panels/ConcentrationPanel.tsx | 2 |
| ClientDetail/panels/AISummaryPanel.tsx | 1 |
