# Addendum — X-Tick Spacing Fix: AdvisorIntelligence DistributionTab
## Supersedes: xtick_spacing_fix.md (original DE task order)

**From:** 0.4.1_RD_ModelPortfolios
**To:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-03-02

---

## DO NOT follow the original task order. Read this first.

The original task order (`xtick_spacing_fix.md`) tells you to add `tickMargin={16}` and bump the bottom margin. That approach was tried on ModelPortfolios and discarded — it does not work. Here is why, and what to do instead.

---

## Why `angle` + `tickMargin` Fails

The recharts `angle` prop rotates the tick label around the **geometric center of the text element**, not the `textAnchor` point. This means `angle={-55}` + `textAnchor="end"` + `tickMargin={16}` does not pin the end of the label to the tick mark — the **middle** of the string ends up adjacent to the tick, and `tickMargin` just shifts the whole misaligned label further from the axis line. The result still looks broken.

---

## The Correct Fix: Custom Tick Renderer

Use an SVG custom tick function that:
1. `translate(x, y)` — moves the SVG origin to the exact tick mark position
2. `rotate(-45)` on the `<text>` element — rotates around `(0,0)` which is now the tick position
3. `textAnchor="end"` on the `<text>` element — places the **end** of the string at `(0,0)` = the tick mark

This is the only approach that guarantees pixel-perfect alignment.

---

## Three Changes to Apply in `DistributionTab.tsx` → `SnapshotDistributionChart`

### Change 1 — Replace XAxis

**Find (approx. lines 1772–1781):**
```tsx
<XAxis
  dataKey="bin"
  stroke="rgba(255,255,255,0.5)"
  tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
  angle={-55}
  textAnchor="end"
  height={72}
  interval={0}
  tickMargin={16}
/>
```

**Replace with:**
```tsx
<XAxis
  dataKey="bin"
  stroke="rgba(255,255,255,0.5)"
  height={50}
  interval={0}
  tick={(props) => {
    const { x, y, payload } = props
    return (
      <g transform={`translate(${x},${y})`}>
        <text
          x={0}
          y={0}
          dy={12}
          textAnchor="end"
          transform="rotate(-45)"
          fontSize={7}
          fill="rgba(255,255,255,0.7)"
        >
          {payload.value}
        </text>
      </g>
    )
  }}
/>
```

Notes:
- Remove `angle`, `textAnchor`, `tickMargin` from XAxis — the renderer handles all of it
- `height={50}` is sufficient at -45° with fontSize 7
- `dy={12}` pushes the label 12px down from the axis line before rotation — gives clean vertical clearance
- Do NOT change `dataKey`, `stroke`, or `interval`

---

### Change 2 — Fix Y-axis label div

**Find (approx. line 1755):**
```tsx
<div className="absolute flex items-center" style={{ top: '30px', bottom: '50px', left: '-20px' }}>
  <span className="text-[11px] text-white/50 whitespace-nowrap" style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}>
    Number of Clients
  </span>
</div>
```

**Replace with:**
```tsx
<div
  className="absolute flex items-center justify-center pointer-events-none"
  style={{ top: '30px', bottom: '50px', left: '-20px', width: '16px' }}
>
  <span
    className="text-[11px] text-white/50 whitespace-nowrap"
    style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}
  >
    Number of Clients
  </span>
</div>
```

Notes:
- `justify-center` was missing — without it the label hangs at the top of the container instead of centering on the plot area
- `width: '16px'` gives the flex container a defined cross-axis size
- `pointer-events-none` prevents hover interference
- `top: 30px` / `bottom: 50px` span exactly the chart margins — flex centering within that range is pixel-perfect without any translate math

---

### Change 3 — Fix X-axis label div

**Find (approx. line 1760):**
```tsx
<div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-4">
  <span className="text-[11px] text-white/50">Client AUA</span>
</div>
```

**Replace with:**
```tsx
<div
  className="absolute -translate-x-1/2 pointer-events-none"
  style={{ bottom: '6px', left: 'calc(50% + 15px)' }}
>
  <span className="text-[11px] text-white/50">Client AUA</span>
</div>
```

Notes:
- `bottom: 0` + `translate-y-4` pushes the label outside the container and can get clipped or bleed into page content below
- `bottom: 6px` sits neatly inside the 50px bottom margin
- `left: calc(50% + 15px)` offsets +15px from the container center to account for YAxis width (40px) minus right margin (10px): `(40 - 10) / 2 = 15px`. This centers the label on the **plot area**, not the container. The chart margin `left: 0` means the YAxis occupies 40px at the left with no additional offset.

---

## Reference Implementation

Every change above matches exactly what is in `portal/src/components/AccountDistributionChart.tsx`. Read that file as your ground truth. The `SnapshotDistributionChart` in `DistributionTab.tsx` is a parallel component — same structure, same fixes apply.

---

## Constraints

- Only `SnapshotDistributionChart` (defined ~line 1702) is in scope. `DistributionTab.tsx` contains other XAxis elements — do not touch them.
- Do not change `angle` on any other element, `globalMaxCount`, tooltip logic, percentile reference lines, or any other chart property.
- Do not push to remote — DT deploys.

## Deliverables

- Code changes to `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx`
- Session log at `logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md`
- Commit message: `"fix(DistributionTab): apply custom tick renderer and axis label centering to SnapshotDistributionChart"`
