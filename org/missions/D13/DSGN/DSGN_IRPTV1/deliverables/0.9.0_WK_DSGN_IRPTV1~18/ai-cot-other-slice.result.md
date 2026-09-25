# DSGN_IRPTV1.TO-IV-e-28 -- result summary (0.9.0_WK_DSGN_IRPTV1~18)

Cottonwood's served `other` mix class (2.0.0_SA_COO~M's batch B, $48.5M / 22 clients, equity -> other per
Andrew's ruling) is now an opt-in "Other" slice, following the existing `includesCash` pattern exactly:

- `composition.ts`: `normalizeMixTo4Class` gains an independent `includeOther` option. Absent, byte-for-byte
  identical to today's 3-class result (verified).
- `TenantLayoutConfig.ts`: `assetClasses.includesOther?: boolean` (optional, defaults falsy -- 49financial,
  Inflection, demo and `DEFAULT_LAYOUT` are unchanged without editing those files).
- `useTenantLayout.ts`: merges `includesOther` from the data-scoped firm, same as `includesCash`.
- `cottonwood/layout.ts`: `includesOther: true`, `assetClasses.ordered` gains `'other'`,
  `colorPalette: { other: PALETTE.purple600 }` (the colour IR's IV-e-27 gives "Other").
- `AdvisorBookView.tsx`: threads `includeOtherInComposition` into all 3 `normalizeMixTo4Class` calls
  (L2/L3/L4 composition).
- `PartnerAnalytics.tsx`: new `resolveMixClassMeta` + exported `MixTile` centralize label/colour resolution
  (previously three duplicated inline maps); the bar-stack, legend and metric-tile sites all gate `other`
  the same way `cash` already is: `(cls !== 'cash' || includesCash) && (cls !== 'other' || includesOther)`.

## Surprises filed

- **DSGN_IRPTV1-W18-S1** (OBSERVATION, INERT): the AdvisorBookView client-drill donut/legend itself lives
  three hops downstream in `ConsolidatedOverviewPanel.tsx` (not in this order's `<paths>`), whose hardcoded
  vertical-legend array excludes `'other'`; empirically, recharts renders no SVG at all under this repo's own
  SSR (`renderToStaticMarkup`, no effects) test convention either. IVE28-AC3 is tested against the real
  composition object AdvisorBookView computes plus PartnerAnalytics' own in-grant, SSR-rendered mix
  legend/tiles, per the refusal clause.
- **DSGN_IRPTV1-W18-S2** (OBSERVATION, INERT): the naming gate (LGIC_ENFORCE DEC-6) REFUSED the first commit
  attempt for hand-typing the registered firm tokens in the new test files -- the same defect class
  DSGN_IRPTV1-W3-S2 already grounded. Resolved the same way: `discover-layouts.ts` finds every partner
  `TenantLayoutConfig` from disk (readdirSync + dynamic import, never naming a firm), and "the Cottonwood
  layout" is identified structurally (`assetClasses.includesOther === true`, asserted unique).

## Criteria

- IVE28-AC1 VERDICT: `NORMALIZE-OTHER-OK`
- IVE28-AC2 VERDICT: `COT-LAYOUT-OTHER-OK`
- IVE28-AC3 VERDICT: `COT-OTHER-SLICE-OK`
- IVE28-AC4: RECORDED, `UNVERIFIABLE-BY-INSTRUMENT` -- graded by `2.0.0_SA_COO~D` on the PROD read of
  relationship z09305589 named in `SIGNOFF_COT_OTHER_20260925.md`.

`bun run typecheck` (`tsc -b --noEmit`): rc=0, 0 diagnostics, before and after every edit in this order.
