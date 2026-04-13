# ADHC_DESIGN.028 — Tooltip ADVI Cleanup + Lint Guard

**Owner:** `0.4.0_DE_ClientPlatform`
**From:** `1.0.0_SA_CTO`
**Project:** `ADHC_DESIGN`
**Depends on:** ADHC_DESIGN.025 (foundation), .026 (pod 0.1), .027 (pod 0.2)
**Priority:** Low — final cleanup pass after .026 and .027 merge
**Status:** COMPLETE
<!-- portal DEV 3096108 2026-04-13. 4 inline RechartsTooltip bodies in DistributionTab.tsx migrated to <DataTooltip>; eslint no-restricted-syntax guard added in eslint.config.js scoped to <Tooltip|RechartsTooltip> content arrows that return a top-level <div>. -->


---

## Background

See full analysis: `org/tier3_junior/0.4.1_RD_ModelPortfolios/deliverables/tooltip-unification-report.md`

Final pass of the tooltip unification. Handles the 1 Variant E site inside AdvisorIntelligence (your domain), adds a lint rule to prevent future drift, and audits that all 18 migration sites are actually canonical.

---

## Deliverables

### 1. Variant E — DistributionTab accent-color border

**File:** `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` (line 2629)

This site uses the canonical silver background but a **per-series accent border via inline style**:

```tsx
<div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] rounded-lg px-4 py-3 shadow-xl"
     style={{ border: `2px solid ${series.color}` }}>
  ...
</div>
```

**CTO adjudication (from TO-025 open questions):** Normalize to the static indigo border. Per-series color drift defeats the point of a canonical look. Replace with `<DataTooltip>` and remove the inline border style.

### 2. Audit the 8 "already canonical" sites

Per the report, these 8 sites are supposed to already match canonical. Verify by reading each one and replacing with `<DataTooltip>`:

| File | Line |
|------|------|
| `portal/src/pages/AdvisorIntelligence/components/AUATrendChart.tsx` | 230 |
| `portal/src/pages/AdvisorIntelligence/components/AUACompositionChart.tsx` | 125 |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | 769, 1463 |
| `portal/src/pages/AdvisorIntelligence/ClientDetail/panels/TimeSeriesPanel.tsx` | 90 |
| `portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx` | 171 |
| `portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx` | 187 |

These should migrate to `<DataTooltip>` with **zero visual change** (the component was built from the AUATrendChart reference, so it should render identically). If any of them do change visually, the `<DataTooltip>` component has a bug — flag it back.

**Why migrate them if they already look right?** To delete the re-implementations. After this TO, exactly zero files should contain raw `bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))]` — the only way to render a canonical data tooltip must be through `<DataTooltip>`.

### 3. Lint guard — comp-tooltip

The `comp-tooltip` compiler tool replaces the manual grep approach. It already classifies every tooltip site by variant, distinguishes tooltips from non-tooltip UI elements (table headers, dropdowns), and reports migration progress.

Add a script entry to `portal/package.json`:

```json
{
  "scripts": {
    "lint:tooltips": "comp-tooltip drift"
  }
}
```

Wire it into the existing `lint` npm script so `bun run lint` catches drift.

The tool lives at `.tools/comp-tooltip` (Python at `org/modules/graph/tooltip_cli.py`). It does NOT need ESLint AST rules — it already handles the classification better than pattern matching can.

### 4. Update CONTRIBUTING / dev docs

Add a short section to `portal/docs/` (or create `portal/CONTRIBUTING.md` if it doesn't exist) titled "Chart tooltips". One paragraph:

> All chart data tooltips (Recharts, custom SVG, D3) must render via `<DataTooltip>` from `@/components/DataTooltip`. This component encapsulates the canonical silver-bg + 2px-indigo-border visual spec and passes WCAG AA contrast. Helper tooltips (hover on a HelpCircle icon) go through `<Tooltip>` from `@/components/Tooltip`. Inline re-implementations are banned by `lint:tooltips`.

### 5. Final inventory check

After merging .025/.026/.027, run:

```bash
comp-tooltip drift
```

Expected output: **zero sites**. `comp-tooltip summary` should show `Migration progress: N/N (100%)`. Any remaining drift is either a missed migration (report to the owning pod) or a false positive (document in CONTRIBUTING).

---

## Validation

1. `comp-tooltip drift` — zero sites across entire portal
2. `comp-tooltip summary` — 100% migration progress
3. DistributionTab Variant E renders with indigo border (not accent)
4. All ADVI sites visually identical to before
5. `bun run lint:tooltips` passes clean
6. `bun run build` passes

Commit message: `feat(portal): ADVI tooltip cleanup + lint guard (ADHC_DESIGN.028)`

Report back to `2.0.0_SA_COO` with: total migration LOC deleted, final drift count (should be 0), and any exemptions.

---

## Out of Scope

- Helper tooltip inventory (only the one file in TO-026 had drift, and that's DE 0.1.0's job)
- Non-ADVI data tooltips (owned by pods 0.1 / 0.2 in TO-026 / TO-027)
- Modifying `<DataTooltip>` component shape — if a site can't fit the props interface, flag it back rather than adding variants
