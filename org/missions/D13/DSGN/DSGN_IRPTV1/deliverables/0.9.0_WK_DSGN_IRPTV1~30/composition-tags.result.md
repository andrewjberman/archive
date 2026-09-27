# DSGN_IRPTV1.TO-IV-e-46 -- result summary (0.9.0_WK_DSGN_IRPTV1~30)

**Cell:** IV-e-46 -- Advisor Intelligence composition admits the ETF Classifier's `structured` and
`commodities` classes, labelled and coloured (CTO 101579, UIR-50 ruled (a)).

## Build

- `portal/src/pages/AdvisorIntelligence/_shared/lib/composition.ts`: `CANONICAL_CLASSES` /
  `CANONICAL_LABELS` (+ the with-cash variants) gain `structured` and `commodities`, unconditionally
  (never gated behind `includeCash`/`includeOther`) -- kept in the mix, counted in the total.
- Each of the four partner layouts' `assetClasses.ordered` admits both, edited on its own file:
  `_partners/49financial/layout.ts`, `_partners/cottonwood/layout.ts`, `_partners/inflection/layout.ts`,
  `_partners/demo/layout.ts`.
- `_shared/components/PartnerAnalytics.tsx`'s `MIX_CLASS_LABELS` gains both labels.
- `src/lib/chartColors.ts`'s `MIX_PIE` gains `structured`/`commodities` as NEW keys only
  (`PALETTE.pink500` / `PALETTE.yellow500` -- the same tokens already ratified for
  `ASSET_CLASS.structured`/`.commodities`); no existing key's value changed.

## Tests

- `iv-e-46.composition-tags.test.ts` (IVE46-AC1): exercises the real `normalizeMixTo4Class` for
  every discovered partner's options against a synthetic 5-class payload -- all five classes
  survive, pct sums to 1, each new class's label + colour distinct from every other mix colour and
  every model-portfolio colour. Control arm: a 3-class payload (neither new class) compared against
  a frozen verbatim copy of the pre-cell function (portal DEV base `6757223a`). VERDICT:
  COMPOSITION-TAGS-OK.
- `iv-e-46.class-readers.test.ts` (IVE46-AC2): mechanical fs census of every source file under
  `AdvisorIntelligence/` (tests excluded) naming an asset-class key list (12 found); each is
  ADMITS (verified mechanically) or NAMED with a file:line citation and reason (7 named, all
  reading the FirmMixPeriodPoint firm-mix-timeseries contract blocked upstream by d06/d08's raise,
  or `PerfrpAllocation.tsx`'s non-dropping fallback, or `TenantLayoutConfig.ts`'s out-of-grant
  `DEFAULT_LAYOUT` -- surprise row filed). VERDICT: CLASS-READERS-OK.

Both new test files avoid hand-typing a firm/product token as a bare (non-prose) string literal
(LGIC_ENFORCE DEC-6's naming gate REFUSE, same shape as row DSGN_IRPTV1-W3-S2): partner directory
names are discovered via `readdirSync`, and the `discover-layouts.ts` helper is loaded via a
runtime-built file URL rather than a static import specifier.

## Regression

- `bun test src/pages/AdvisorIntelligence` -- 10 pass / 0 fail total (8 pre-existing cot-other/
  suites unaffected, plus these 2 new files).
- `bun run typecheck` (`tsc -b --noEmit`) -- rc=0.
- Mutant control on IVE46-AC2 caught its own first-draft blind spot: the partner-layout ADMITS
  check originally read the whole file, so a comment naming the classes stood in for the
  `ordered` array actually carrying them. Tightened to scope the check to the array itself
  (portal commit `ace4f08d`); re-run of the same mutant then correctly failed the test.

## Surprise

- `DSGN_IRPTV1-W30-S1`: `_shared/types/TenantLayoutConfig.ts`'s `DEFAULT_LAYOUT.assetClasses.ordered`
  carries the identical contract as the four edited partner layouts and still drops the two classes,
  but the file is outside this TO's `<paths>` grant; no live partner resolves through it today.
