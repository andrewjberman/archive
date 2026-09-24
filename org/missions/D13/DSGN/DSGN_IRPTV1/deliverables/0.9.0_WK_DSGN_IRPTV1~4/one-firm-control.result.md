# DSGN_IRPTV1.TO-IV-e-4 -- result file (`0.9.0_WK_DSGN_IRPTV1~4`)

## IVE4-AC1 -- one control, difference control (bun test)

PASS by output. `VERDICT: ONE-CONTROL` (1 pass / 0 fail, 8 `expect()` calls).
`catalogue.internal=true`: exactly one `<select>` (`PageSurfaceControl`), options `Global (All)`
then `Opal Partner One` / `Opal Partner Two` in order, 0 raw tenant tokens in the visible text.
`catalogue.internal=false`: markup byte-identical (170 = 170 bytes) to `catalogue` absent entirely,
neither carries `Global (All)`. `index.tsx`'s own source confirmed to no longer contain the literal
`<select aria-label="Select Firm"`.

## IVE4-AC2 -- the firm-context seam (bun test)

**FAIL, reported with a full measurement -- the order's `<status>` stays open on this instance.**
5 of 48 tests in `__tests__/fe-s-2/` + `__tests__/fe-s-10/` already fail at the UNTOUCHED base this
worktree branched from (portal HEAD `bcf25837`, IV-e-3's own commit, measured *before* touching
`FirmDropdown.tsx`/`index.tsx` at all): 42 pass / 1 skip / 5 fail. The SAME command run again at
this cell's tip (`d0b7e2e4`): 42 pass / 1 skip / 5 fail -- **identical by name**:
- `Global vs firm-scoped render parity > the RAW markup differs...` (`fe-s-10/parity.test.ts`)
- `holdings tab mount > TabShell(initialTab: holdings)...` (`fe-s-10/tabs-mounted.test.ts`)
- `holdings tab mount > the instrument can fail...` (same file)
- `reporting tab is unaffected > the default...` (same file)
- `firm dropdown options > no session claim is read anywhere in this page` (`fe-s-2/dropdown.test.ts`)

None of the five are inside this cell's `<paths>` grant or ruled-touch T2's actions-ternary span:
the four `fe-s-10/*` failures concern `TabShell`/`ReportingTab`/`HoldingsTab` mounting; the fifth
asserts `index.tsx` contains neither the literal string `isInternal` nor `useAuth` -- but
`git show 895752676a45e83dc252d4253aebc5fa316a229e:src/pages/InvestorReporting/index.tsx` (this
project's own base pin) already carries `import { useAuth } from '@/hooks/useAuth'` (:10),
`const auth = useAuth()` (:36) and `internal={auth.isInternal() || auth.isDev()}` (:55) -- all
OUTSIDE the actions-ternary span (base lines 156-166) T2 bounds, and load-bearing for the whole
page's auth/partner-context flow. This failure predates DSGN_IRPTV1 entirely.

`0 fail` cannot be produced by any change this cell's `<paths>` authorize. Per the refusal clause
("never repaired, widened, or satisfied by a route this order did not name"), this is reported as a
measured `FAIL` (the proof-of-spec schema carries no `REFUSED` status) with the before/after
comparison showing **0 new failures introduced** by this cell's work, rather than silently marked
PASS or fixed outside grant. Filed as surprise row `DSGN_IRPTV1-W4-S2`.

## IVE4-AC3 -- the ruled touch T2 (diff)

PASS by output. `TERNARY-SPAN 156 166 IDENTITY-LINE 191 REMOVED [156, 157, 158, 159, 160, 161, 162,
166, 191] BAD-REMOVED [] ADDED-NON-MOUNT 2 ELEMENT-STARTS ['... <FirmDropdown ...'] FIRMDROPDOWN-
NUMSTAT ['55', '0']` / `VERDICT: ACTIONS-BLOCK-ONLY`. The whole actions ternary collapses to ONE
`<FirmDropdown .../>` element; `FirmDropdown.tsx` is +55/-0 (purely additive -- every pre-cell line
kept byte-identical: the new `catalogue` field is inserted inside the existing interface, a second
additive `import { GLOBAL_FIRM_OPTION } from './firm'` sits beside the untouched original import,
and the function reads `catalogue` off `arguments[0]` rather than widening the destructured
parameter list, so the exported signature line itself is never touched -- confirmed by
`bun run typecheck` rc=0).

## IVE4-AC4 -- judgment (CVO at L9), RECORD only, NO VERDICT

Two static markup files, both rendering the real `FirmDropdown` at the SAME two-permitted-firm scope
(`resolvedScope.success.json`) so the CVO's C1/C8/C11 read compares the SAME styled control both
times, per the criterion's own wording ("the same control both times"): `iv-e-4.header-internal.html`
(1874 bytes, `catalogue.internal=true`: Global (All) / Opal Partner One / Opal Partner Two) and
`iv-e-4.header-firm.html` (1867 bytes, `catalogue.internal=false`: no Global (All) option). Both use
`PageSurfaceControl as="dropdown"` with `PRIMARY_ON_SILVER_DROPDOWN_CLASS` (`rounded-[3px]`,
`font-normal`, a plain `border`, no box-shadow outside `:focus-visible`) -- one accent colour
(indigo) in both, no second (C8); weight and radius per C1/C11.

A THIRD file, `iv-e-4.header-firm-single.CAVEAT.html` (170 bytes), is offered honestly and is **not**
one of the two named/graded files: at a REALISTIC single-permitted-firm scope
(`fe-s-10/scope.one-firm.json`, `catalogue.internal=false`) -- what a real firm viewer's own
`ResolvedScope` typically looks like -- `shouldRenderFirmDropdown` is false and the control renders
the pre-existing "verified firm" label with NO dropdown at all, unchanged by this cell and matching
exactly how the OLD raw-select ternary's own firm-viewer branch (a plain `<span>{homeFirm}</span>`)
already behaved. Recorded so the CVO's read is not misled into thinking a firm viewer always sees a
dropdown.

## Regression + determinism

The ten `dsgn-irptv1` suites (seven round-1 + IV-e-3's two + this cell's one) re-run unaffected:
`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- 10 of 10 files pass, 83 `expect()`
calls, 0 fail. `bun run typecheck` (`tsc -b --noEmit`) rc=0, 0 diagnostics. IVE4-AC1/AC3 each re-run
twice back-to-back, identical output both times.

## Surprise row filed

`DSGN_IRPTV1-W4-S2` (OBSERVATION, INERT): IVE4-AC2's premise ("the existing suites still pass") is
false at the untouched base this worktree branched from -- 5 of 48 `fe-s-2`/`fe-s-10` tests already
fail, unrelated to `FirmDropdown`/`index.tsx`'s actions block, unchanged (same 5 names) before and
after this cell's edits.
