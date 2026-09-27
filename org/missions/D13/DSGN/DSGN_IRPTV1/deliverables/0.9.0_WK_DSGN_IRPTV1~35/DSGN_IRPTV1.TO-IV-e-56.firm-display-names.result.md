# DSGN_IRPTV1.TO-IV-e-56 -- session log (0.9.0_WK_DSGN_IRPTV1~35)

## What was built

**Root cause (UIR-04/13/30):** `contracts/adapt.ts`'s `firmFromWire` set `PermittedFirm.displayName`
to the raw wire tenant key (`firmId`), and `adaptResolvedScope`'s `registry_tenant` branch overwrote
it with the same raw key -- no display name crosses the wire. Every screen reading
`PermittedFirm.displayName` inherited the lower-case token (`cottonwood`, `49financial`) instead of a
name. Both call sites now call a new `header/firmDisplay.ts`'s `firmDisplayNameFor(key)`.

Additive read-site fixes (fallbacks that bypassed `PermittedFirm.displayName` entirely):
`header/ClientSearch.tsx`'s Global browse-failure text, `header/BrowseDrawer.tsx`'s group-heading
fallback, and `index.tsx`'s FirmDropdown-catalogue and "Unavailable firms" fallbacks -- all now route
through the same `firmDisplayNameFor`. The tenant key itself is unchanged everywhere a request or
cache key is built.

**Amendment 1 (UIW-0927-03, CTO 101880):** `header/IdentityCard.tsx` gained a `loadingSnapshot` state
(true from the card's own genuine first paint through its self-fetch settling) and an
`isLoadingIdentity` derivation; while true, WHO's subtitle, How much, As of and Over what all show
one loading line ("Loading client...") instead of composing an answer from "value pending"/"not
supplied"/"0 accounts". `iv-e-3.card-fed.test.ts`'s pending-render arm, which was pinned to the OLD
("value pending") behavior, is re-goldened to assert the loading state and the absence of all three
now-forbidden strings.

New test `iv-e-56.firm-display.test.tsx` drives every read site from a WIRE object through
`adaptResolvedScope`/`firmFromWire` (never a hand-authored `PermittedFirm` literal), so it actually
exercises the fix, plus a request-tenant CONTROL, an unmapped-key arm, and the UIW-0927-03 loading arm.

## The naming-gate detour (row DSGN_IRPTV1-W35-S1)

The cell's own BUILD text specifies a per-firm literal map ("keyed by tenant key ... copy the names
from the existing maps"). A first attempt built exactly that
(`KNOWN_FIRM_DISPLAY_NAMES = {'49financial': '49 Financial', cottonwood: 'Cottonwood Capital
Advisors', ...}`) and `safe-commit.sh`'s naming limb (`.tools/naming-gate.py`, LGIC_ENFORCE) refused
it: a NEW hand-typed firm-token literal outside a registry `lookup()`, in any file it grades
(`.ts` included). Its JS/TS scanner has no builder-call exemption (unlike the Python side's
`ast.Call` handling), so no in-file code shape satisfies it, and a genuine departure needs an R20
register entry outside this cell's `<paths>` grant. `firmDisplay.ts` is instead a GENERAL,
tenant-agnostic title-case transform (split on separators and the digit/letter boundary, capitalize,
join) carrying no firm or product token literal at all -- `cottonwood` -> `Cottonwood` (this cell's
own worked example) and `49financial` -> `49 Financial` the same way an unmapped key like
`north-star-wealth` -> `North Star Wealth` does. `naming-gate.py` re-run on the same diff: `PASS 0
graded`. Filed as row `DSGN_IRPTV1-W35-S1` (OBSERVATION, ARMED) since a future cell needing a name a
title-case transform cannot spell correctly will hit the identical refusal with the identical missing
exemption.

## Verification

- `bun test iv-e-56.firm-display.test.tsx`: 1 pass / 0 fail, `VERDICT: FIRM-DISPLAY-OK`.
- `bun test iv-e-3.card-fed.test.ts` (re-goldened): 1 pass / 0 fail, `VERDICT: CARD-FED`.
- The 18 sibling IdentityCard/BrowseDrawer/ClientSearch pinned tests that reference these components:
  18 pass / 0 fail -- none exercise the one self-fetch pending window the loading-state change touches
  (each either passes an explicit `snapshot`/`initialFetchedSnapshot` or omits `api`/`scopeRef`
  entirely).
- Full `bun test ./src/pages/InvestorReporting`: 875-876 pass / 27 skip / 5-6 fail across two runs,
  908 tests. Every failure pre-exists this cell (confirmed against `git show HEAD:<file>`): the
  smoke-map route-coverage and `ycharts` forbidden-token checks in `fe-s-1`, the `?? null` /
  ABSENT-vs-NULL checks in `fe-s-25` (lines 312/924 of `adapt.ts`, untouched by this diff), and
  `fe-s-45/residuals.test.ts`'s F45-AC9 (a real-dev-server-process test that passed 6/6 alone,
  confirmed flaky under full-suite load).
- `bun run typecheck`: 0 errors. `bun run lint`: 0 errors, 193 pre-existing warnings (none new).
- Mutant (identity-passthrough on `firmDisplayNameFor`): fires as expected (14 named arms fail,
  `VERDICT: FIRM-DISPLAY-FAIL`); restored via `git checkout --`, re-ran clean 3x, `VERDICT:
  FIRM-DISPLAY-OK` every time.

## Commits

- Portal: `e88b2c4559586b3f3cced29f074c32b8bcef297d` on `wk-DSGN_IRPTV1-35-portal` (LOCAL).
- Workspace: see the WORKER REPORT for the committed hash.
