# Portfolio Management - UI Design Specification

## Overview

Redesign the Portfolio Management page to match the canonical panel design framework used throughout the Opal portal. This page is a **tool/write function** (not read), so we'll use **mock data** for the snapshot and time series sections.

---

## Reference Pages for Design Patterns

Study these existing pages for design patterns:

| Pattern | Reference File |
|---------|----------------|
| Page header + snapshot metrics | `Positioning/Positioning.tsx` |
| Panel framework (Card variant="gradient") | `Positioning/components/HoldingsTable.tsx` |
| Time series charts | `FactorTilts/tabs/FactorTiltTimeSeriesTab.tsx` |
| Radial/summary charts | `Positioning/components/PortfolioRadialCharts.tsx` |
| Tab navigation | `Positioning/Positioning.tsx` |
| Table with sorting/filtering | `Positioning/components/HoldingsTable.tsx` |
| Color tokens | `lib/designTokens.ts` |

---

## Page Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PAGE HEADER                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ [Icon] Portfolio Management           [Strategy Selector: PFDE ▼]     │ │
│  │ Review and execute portfolio rebalancing trades                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│  PORTFOLIO SNAPSHOT (Panel - always visible)                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │ │
│  │ │   AUM   │ │Positions│ │  Beta   │ │ Active  │ │Expected │ │Turnover│ │ │
│  │ │ $30.2M  │ │   72    │ │  1.02   │ │ Share   │ │ Alpha   │ │  8.2% │ │ │
│  │ │         │ │         │ │         │ │  12.4%  │ │  1.8%   │ │       │ │ │
│  │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│  PERFORMANCE TIME SERIES (Panel - always visible)                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Performance vs Benchmark                              [1M|3M|6M|1Y]    │ │
│  │ ┌────────────────────────────────────────────────────────────────────┐ │ │
│  │ │                    ════════════════════════                        │ │ │
│  │ │              ══════                      ══════                    │ │ │
│  │ │         ═════                                  ═════               │ │ │
│  │ │    ═════  Portfolio ━━━  Benchmark ━━━              ═════          │ │ │
│  │ └────────────────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│  WORKFLOW TABS                                                              │
│  ┌──────────────────┬──────────────────┬──────────────────┐                │
│  │   ① Import       │   ② Review       │   ③ Export       │                │
│  └──────────────────┴──────────────────┴──────────────────┘                │
├─────────────────────────────────────────────────────────────────────────────┤
│  TAB CONTENT AREA                                                           │
│  [Content varies by active tab - see below]                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Section 1: Portfolio Snapshot Panel

### Design Requirements

- Use the `Panel` component from `@/ui/components/panels` (PanelHeader, PanelContent pattern)
- OR use `Card variant="gradient"` with proper styling
- 6 metric cards in a responsive grid (6 columns on desktop, 3 on tablet, 2 on mobile)
- Each metric card should have:
  - Icon with colored background (following existing color patterns)
  - Label (uppercase, small, muted)
  - Value (large, bold, white)
  - Optional delta/change indicator

### Metrics to Display (Mock Data)

| Metric | Mock Value | Icon | Color |
|--------|------------|------|-------|
| AUM | $30.2M | DollarSign | emerald-500 |
| Positions | 72 | Briefcase | blue-500 |
| Beta | 1.02 | TrendingUp | purple-500 |
| Active Share | 12.4% | Activity | amber-500 |
| Expected Alpha | +1.8% | Target | cyan-500 |
| Turnover | 8.2% | RefreshCw | rose-500 |

### Color Pattern Reference

Follow the color tokens from existing panels:
```typescript
// From designTokens.ts / existing components
emerald: 'bg-emerald-500/10 text-emerald-400'
blue: 'bg-blue-500/10 text-blue-400'
purple: 'bg-purple-500/10 text-purple-400'
amber: 'bg-amber-500/10 text-amber-400'
cyan: 'bg-cyan-500/10 text-cyan-400'
rose: 'bg-rose-500/10 text-rose-400'
```

---

## Section 2: Performance Time Series Panel

### Design Requirements

- Use `Card variant="gradient"` wrapper
- Header with title + period selector buttons (1M, 3M, 6M, 1Y)
- Recharts AreaChart with dual series (Portfolio vs Benchmark)
- Follow the chart styling from `FactorTiltTimeSeriesTab.tsx`
- Height: 200-250px

### Chart Styling

```typescript
// Portfolio line
stroke: '#4CAF50' // Green
fill: 'url(#portfolioGradient)' // Green gradient fade

// Benchmark line
stroke: '#64748b' // Slate/gray (muted)
fill: 'url(#benchmarkGradient)' // Gray gradient fade
strokeDasharray: '4 4' // Dashed line for benchmark
```

### Mock Data Structure

Generate 365 days of mock performance data:
```typescript
const mockPerformanceData = generateMockTimeSeries({
  days: 365,
  portfolioVolatility: 0.15,
  benchmarkVolatility: 0.12,
  portfolioAlpha: 0.02, // 2% annual alpha
})
```

---

## Section 3: Tab Content Areas

### Tab 1: Import

**Purpose**: Upload optimizer output file (JSON or pickle)

**Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  UPLOAD PANEL (Card variant="gradient")                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │     ┌──────────────────────────────────────────────┐     │  │
│  │     │          [Upload Icon]                       │     │  │
│  │     │                                              │     │  │
│  │     │   Drag and drop your optimizer output here   │     │  │
│  │     │        or click to browse                    │     │  │
│  │     │                                              │     │  │
│  │     │         [.json]  [.pkl]                      │     │  │
│  │     └──────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  IMPORT PREVIEW (Card variant="gradient") - Shows after upload  │
│  ┌─────────────────────────────────┬─────────────────────────┐  │
│  │ Import Summary                  │ Trade Breakdown         │  │
│  │ ─────────────────               │ ─────────────────       │  │
│  │ Strategy: PFDE                  │ ┌───┐ ┌───┐ ┌───┐      │  │
│  │ As of Date: Jan 15, 2024        │ │32 │ │28 │ │12 │      │  │
│  │ Total Positions: 72             │ │BUY│ │SELL│ │HOLD│     │  │
│  │ AUM: $30.2M                     │ └───┘ └───┘ └───┘      │  │
│  │ Expected Turnover: 8.2%         │                         │  │
│  └─────────────────────────────────┴─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Design Notes**:
- Drag-drop zone: dashed border, highlight on drag-over with primary color
- File type badges in monospace font
- After upload: show success state with green checkmark
- Preview panel uses 2-column layout

---

### Tab 2: Review

**Purpose**: Review and edit trade recommendations

**Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  TRADE SUMMARY PANEL (Card variant="gradient")                  │
│  ┌───────────┬───────────┬───────────┬───────────┬───────────┐ │
│  │  BUYS     │  SELLS    │ TURNOVER  │ OVERRIDES │  HOLDS    │ │
│  │   32      │   28      │   8.2%    │    0      │   12      │ │
│  │  $2.4M    │  $2.1M    │   $2.3M   │           │           │ │
│  │  ↑ green  │  ↓ red    │  ↔ blue   │  ✏ amber  │  — gray   │ │
│  └───────────┴───────────┴───────────┴───────────┴───────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ACTION BAR                                                     │
│  72 positions • 32 buys • 28 sells    [Accept All] [Reset All] │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TRADE TABLE (Card variant="gradient")                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Search...]  [Sector ▼]  [Action ▼]      72 trades [CSV]  │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │ Ticker│Name     │Sector│Curr%│Sugg%│Delta│Alpha│Action│...│  │
│  │───────┼─────────┼──────┼─────┼─────┼─────┼─────┼──────┼───│  │
│  │ AAPL  │Apple Inc│Tech  │3.20 │3.80 │+0.60│0.012│ BUY  │...│  │
│  │ MSFT  │Microsoft│Tech  │4.10 │3.50 │-0.60│0.008│ SELL │...│  │
│  │ ...   │...      │...   │...  │...  │...  │...  │...   │...│  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Table Columns**:
| Column | Width | Align | Notes |
|--------|-------|-------|-------|
| Ticker | 80px | left | Bold, monospace |
| Name | flex | left | Truncate with tooltip |
| Sector | 120px | left | Badge style |
| Current Wt | 80px | right | 2 decimals + % |
| Suggested Wt | 80px | right | 2 decimals + % |
| Delta | 80px | right | Color-coded (+green, -red) |
| Alpha | 80px | right | 4 decimals |
| Action | 70px | center | Badge (BUY=green, SELL=red, HOLD=gray) |
| Override | 60px | center | Checkbox |
| Final Wt | 80px | right | Input (disabled until override checked) |
| Comment | 150px | left | Text input |

**Design Notes**:
- Follow `HoldingsTable.tsx` patterns exactly
- Sticky header on scroll
- Row highlight on hover (`hover:bg-white/5`)
- Overridden rows get subtle amber background (`bg-amber-500/5`)
- Max height with scroll (600px)

---

### Tab 3: Export

**Purpose**: Final review and CSV download for Schwab

**Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  EXPORT CONFIGURATION (Card variant="gradient")                 │
│  ┌─────────────────────────────┬─────────────────────────────┐  │
│  │ Schwab Account Number       │ Export Summary              │  │
│  │ ┌─────────────────────────┐ │ ─────────────────           │  │
│  │ │ [                     ] │ │ Strategy: PFDE              │  │
│  │ └─────────────────────────┘ │ Trades to Export: 60        │  │
│  │                             │ Estimated Value: $4.5M      │  │
│  │                             │ Overridden: 3               │  │
│  └─────────────────────────────┴─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TRADES TO EXECUTE (Card variant="gradient")                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Read-only trade table - HOLD trades filtered out]        │  │
│  │ Shows only BUY and SELL trades that will be exported      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  CONFIRMATION (Card variant="gradient")                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [✓] I confirm I have reviewed all trades and am ready     │  │
│  │     to export for execution.                              │  │
│  │                                                           │  │
│  │ This will generate a CSV file formatted for Schwab's      │  │
│  │ trade upload system.                                      │  │
│  │                                        ┌─────────────────┐│  │
│  │                                        │ Download CSV    ││  │
│  │                                        │ [↓]             ││  │
│  │                                        └─────────────────┘│  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Design Notes**:
- Download button: Primary color, disabled until checkbox checked
- Warning messages in amber if validation fails
- Success message in green when ready to export
- Trade table is read-only (no edit columns)

---

## Mock Data Generator

Create `utils/mockData.ts` with generators for:

```typescript
// Mock portfolio metrics
export const MOCK_PORTFOLIO_METRICS = {
  aum: 30_200_000,
  positions: 72,
  beta: 1.02,
  activeShare: 0.124,
  expectedAlpha: 0.018,
  turnover: 0.082,
  asOfDate: '2024-01-15',
}

// Mock trade data (72 positions)
export function generateMockTrades(): TradeRecord[] {
  // Generate realistic mock trades across sectors
  // Mix of BUY (32), SELL (28), HOLD (12)
}

// Mock performance time series (365 days)
export function generateMockPerformance(): PerformanceDataPoint[] {
  // Generate daily returns with slight alpha
}
```

---

## Color Palette Summary

| Element | Color Token | Usage |
|---------|-------------|-------|
| BUY action | emerald-400/500 | Badges, positive deltas |
| SELL action | red-400/500 | Badges, negative deltas |
| HOLD action | white/40-60 | Muted, neutral |
| Override indicator | amber-400/500 | Warning, user changes |
| Primary button | hsl(var(--primary)) | Download, primary actions |
| Panel background | Card variant="gradient" | All panels |
| Text primary | white | Values, important text |
| Text secondary | white/60-80 | Labels, descriptions |
| Text muted | white/40 | Hints, disabled |

---

## Implementation Checklist

- [ ] Refactor `PortfolioSnapshot.tsx` to use Panel component pattern
- [ ] Create `utils/mockData.ts` with generators
- [ ] Update `PerformanceChart.tsx` to match canonical chart styling
- [ ] Redesign `ImportTab.tsx` with proper panel layout
- [ ] Redesign `ReviewTab.tsx` with summary panel + action bar
- [ ] Redesign `ExportTab.tsx` with configuration + confirmation panels
- [ ] Update `TradeTable.tsx` to match `HoldingsTable.tsx` exactly
- [ ] Add responsive breakpoints for mobile/tablet
- [ ] Ensure all colors follow design tokens
- [ ] Test with mock data throughout

---

## Files to Reference

```
src/ui/components/panels/           # Panel, PanelHeader, PanelContent
src/components/Card.tsx             # Card variant="gradient"
src/pages/Positioning/              # Overall page structure
src/pages/FactorTilts/              # Time series charts
src/lib/designTokens.ts             # Color tokens
src/pages/Positioning/components/HoldingsTable.tsx  # Table patterns
```
