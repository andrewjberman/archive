# DSGN_IRPTV1.TO-IV-e-3 -- result file (`0.9.0_WK_DSGN_IRPTV1~4`)

## IVE3-AC1 -- built behaviour, fetched (bun test)

PASS by output. `VERDICT: CARD-FED` (1 pass / 0 fail, 12 `expect()` calls).
`fetchIdentityCardData` (exported from `header/IdentityCard.tsx`) exercised against a stubbed
`InvestorReportingApi`: `getHoldingsSnapshot` called 1 of 1 times, `searchDirectory` called 1 of 1
times, scoped to `scopeRef` (`tenant`/`scopeFingerprint`/`revision`) with `kinds: ['account']`.
The resolved values, handed to `IdentityCard` through its TEST-ONLY seed props
(`initialFetchedSnapshot` / `initialFetchedAccountEntries` -- `HoldingsTab.tsx`'s own documented
pattern, since `renderToStaticMarkup` runs no effect): HOW MUCH `$6,024,455.54` present; AS OF WHEN
`2026-09-09` present; CHIPS `2 of 2 named, 0 ids`. A separate render with `api`+`scopeRef` given and
no seed reads `value pending` (the card's genuine first-paint state) with the fed total absent.

## IVE3-AC2 -- the chip toggle, difference control (bun test)

PASS by output. `VERDICT: CHIP-NARROWS` (1 pass / 0 fail, 8 `expect()` calls).
`handleAccountChipClick` / `handleRestoreAllClick` (the exact functions each chip's `onClick` calls)
exercised directly with a recording `onNarrow` double, since `renderToStaticMarkup` cannot fire a real
click: arm 1 narrows to one account (`Narrowing.scope.accountIds=["acct-1001"]`,
`row.entry.accountId=acct-1001`, called exactly once); arm 2 clicking the active chip again restores
the full permitted set; arm 2b the "All accounts" control restores from a different narrowed state;
arm 3 with `onNarrow` absent the round-1 mount shape (`scope`/`selection`/`row`/`accountEntries` props
only) still renders its 2 of 2 chips, as inert `<span>`, never a clickable `<button>`.

## IVE3-AC3 -- the ruled touch T1 (diff)

PASS by output. `NUMSTAT: ['1\t1\tsrc/pages/InvestorReporting/index.tsx']` /
`CHANGED: 2 OUTSIDE-MOUNT: []` / `VERDICT: ONE-LINE-MOUNT`. The mount line's props grew to
`api={api} scopeRef={selectedScopeRef} onNarrow={select}` alongside the unchanged
`scope`/`selection`/`row`; no other line of `index.tsx` changed, `header/ScopeSummary.tsx` untouched,
no new import needed (`api`, `selectedScopeRef` and `select` already exist in `SelectionWorkspace`).

## IVE3-AC4 -- judgment (CVO at L9), RECORD only, NO VERDICT

Static markup: `iv-e-3.identity-card.html` (this folder), rendered via `renderToStaticMarkup` over the
real `IdentityCard`, fed through `fetchIdentityCardData` against the same stubbed api as IVE3-AC1
(`resolvedScope.success.json` / `directoryEntry.success.json` / `holdingsSnapshot.success.json` plus
adapted per-account directory entries, `onNarrow` supplied). 4310 bytes.

No smoke PNG this round: `fixtures/smoke/dsgn-irptv1-cottonwood.json` (IV-e-2's new fixture, chain B)
does not exist on this worktree's base (`895752676a`, chain A's own provisioning point) -- IV-e-2 has
not merged into this worktree's history, so the smoke script has nothing to point at. This is stated,
not worked around: the criterion itself makes the PNG conditional ("if IV-e-2's fixture renders it"),
and IVE3-AC1/AC2 already exercise `IdentityCard` directly against the real fixtures.

Self-check against `portal/DESIGN.md` (my own read, not a verdict -- the component law is unchanged
from round 1 by this cell): `Panel variant="nested"` + `PanelHeader` + `PanelContent`; every ink value
`hsl(var(--palette-navy))` / `hsl(var(--palette-darkGray))`, no `text-slate-*` idiom; `tabular-nums` on
the custody total and the business date. The brief's bar, read off the markup: WHO = "Coastal Ridge
Trust" / "Opal Partner One -- Relationship"; HOW MUCH = "$6,024,455.54"; OVER WHAT = two chips reading
"Coastal Ridge Trust ****4417" and "Coastal Ridge IRA ****9903" (names + masked tails, 0 raw ids); AS
OF = "2026-09-09" -- all four answerable from the header alone, without opening a tab. The chips render
as `<button data-slot="account-chip">` (clickable, since `onNarrow` was supplied to this render) and an
"All accounts" restore control appears once a chip is active -- the toggle affordance is present and
discoverable in the markup, though not exercised interactively in this particular static render (the
render's `selection` prop is `null`, so no chip starts active).

## Regression + determinism

The seven round-1 `dsgn-irptv1` suites re-run unaffected after this cell's edits:
`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- 9 of 9 files pass, 75 `expect()`
calls, 0 fail. `bun run typecheck` (`tsc -b --noEmit`) rc=0, 0 diagnostics. IVE3-AC1/AC2/AC3 each
re-run twice back-to-back, identical output both times.

## Surprise row filed

`DSGN_IRPTV1-W4-S1` (OBSERVATION, INERT): the pre-commit risk-reflex (`comp-pulse`) HELD this
worker's `index.tsx` edit against four unrelated `AdvisorIntelligence` partner components, apparently
matched by the shared basename `index.tsx` rather than full path or import graph -- the cited memory
concerns the Cottonwood ADVI Books tab's server-artifact drill chain, nothing InvestorReporting-related.
Read, found unrelated, not treated as a blocker; filed for whoever owns the `comp-pulse` danger map.
