# DSGN_IRPTV1.TO-IV-e-70.model-vs-class-colour -- session log (0.9.0_WK_DSGN_IRPTV1~38)

## Inheritance note

This slot's previous worker instance was stopped by an account limit after building the cell.
This session inherited the uncommitted edits (chartColors.ts, palette.ts, two re-goldened iv-e-12
tests, the new iv-e-70 test) and reviewed them against the Build text, ran the acceptance
invocation, confirmed the re-goldened tests each name their row, and wrote this proof. A
REPOSITORY FREEZE (0.0.0_AB_MSTR, history rewrite running) forbids any git write this turn; every
artifact below is staged in the worktree, uncommitted, pending the issuer's continuation.

## What was wrong (UIR-37, UIC-11)

`ASSET_CLASS.fixedIncome`/`.equity`/`.alternatives`/`.realEstate` were EXACT hue duplicates of
canonical Opal model colours (green500=Intermediate Term, blue500=Long Term, orange500=Ultra-Short
Term, each dE00=0.0000) -- the literal "no hue means both" defect UIR-37 names. Separately,
`tabs/holdings/palette.ts` ACCOUNT_PALETTE's worst internal pairwise CIEDE2000 was dE00=3.3009,
not distinguishable at a glance (UIC-11).

## Fix (reviewed, not re-built, by this session)

- **chartColors.ts.** Each offender moved one step darker within its OWN hue family: fixedIncome
  -> green700 (dE00=21.7122 vs models), equity -> blue900 (20.8323), alternatives/realEstate ->
  orange700 (14.7215; new PALETTE token, reused from modelPortfolioColors.ts's own Ultra-Short
  Term text ink rather than invented). The distance rule (CIEDE2000 dE00 >= 10 vs every
  MODEL_PORTFOLIO_COLORS + EXTENDED_MODEL_COLORS primary) and the full measured record are stated
  in the ASSET_CLASS block comment, per the Build text's instruction. `getAssetClassTextColor`'s
  lightBackgrounds array updated to match (all four movers take dark-enough shades that white text
  clears 4.5:1, verified in-comment).
- **REACH (consumers of the changed entries), confirmed by this session with a fresh grep of every
  `from '@/lib/chartColors'` importer**: `Positioning/panels/PositioningSummary.tsx`,
  `Positioning/tabs/HoldingsTab.tsx` (ASSET_CLASS_COLORS + ASSET_CLASS_HEXES),
  `Attribution/constants/holdings-shared.tsx`, `CapitalMarketAssumptions/tabs/ExpectationsTab.tsx`
  all import `ASSET_CLASS.fixedIncome/.equity/.alternatives` directly and repaint automatically.
  `InvestorReporting/tabs/holdings/DrillTree.tsx` and `AllocationBars.tsx` import `ASSET_CLASS` too
  but only read `.other`/`.cash` (confirmed: DrillTree.tsx's only live `ASSET_CLASS.*` reference is
  `ASSET_CLASS.other` at its `colorForServedModelCode` fallback), so unaffected. The Holdings tab's
  own page-local override (`tabs/holdings/assetClass.ts`, IV-e-43) took its values from separate,
  hand-picked PALETTE tokens and does not inherit this fix -- confirmed out of scope, untouched
  (file not in this cell's `<paths>`).
- **palette.ts.** ACCOUNT_PALETTE replaced: 14 entries from an exhaustive farthest-point search
  over Tailwind slate/zinc/neutral/stone (100-900), first filtering any candidate within dE00<10 of
  a model or ASSET_CLASS colour, then maximizing the worst-case pairwise distance. Measured: worst
  internal pairwise dE00=6.7642 (more than double the old 3.3009), worst vs model=16.5342, worst vs
  ASSET_CLASS=10.2760.
- **DrillTree.tsx.** No edit needed -- in grant, but its only `ASSET_CLASS.*` read is `.other`
  (unchanged); its other colour reads go through the page-local, out-of-scope `ASSET_CLASS_COLOR`.

## Test (this session ran, did not author)

`iv-e-70.model-class-colour.test.ts` -- self-contained CIEDE2000 (sRGB->linear->XYZ D65->CIELAB->
dE00, matching the iv-e-49/iv-e-51 family's own established practice). Four arms: published
reference-pair control, OLD-PAIR negative control (proves the check catches the historical defect),
the ASSET_CLASS-vs-model dE00>=10 sweep (population: MODEL_PORTFOLIO_COLORS deduped, excluding
Non-Model, plus a 60-probe sweep of the real `getModelColor` for the hidden EXTENDED_MODEL_COLORS
primaries), and the ACCOUNT_PALETTE >=12-entries/all-pairs/no-shared-hue battery. VERDICT:
MODEL-VS-CLASS-COLOUR-OK, 4 pass / 0 fail, run twice with identical output (see Controls).

Two re-goldened tests (`iv-e-12.cash-green.test.ts`, `iv-e-12.positioning-reader.test.ts`) each
carry a new comment block naming "amendment 2, IV-e-70" and the CTO ruling, and update their
pinned literals to the post-IV-e-70 hexes; `iv-e-12.positioning-reader.test.ts` additionally
asserts each mover landed on the SPECIFIC new value (`IVE70_NEW`), not merely "moved". Both pass:
VERDICT: CASH-GREEN-OK; VERDICT: POSITIONING-ONLY-CASH-MOVED.

## Controls (this session ran)

- **Mutant**: in-worktree-only (Edit tool, never staged) revert of `ASSET_CLASS.fixedIncome` back
  to `PALETTE.green500`. Re-ran IVE70-AC1 -- 1 of 4 tests failed, VERDICT line replaced by the
  expected failure text naming the exact-duplicate. Restored via the Edit tool; sha256 of
  `chartColors.ts` measured `405e2ac9...8a10d2` both before the mutant and after restoration
  (byte-identical). Re-ran clean: VERDICT: MODEL-VS-CLASS-COLOUR-OK, 4 pass / 0 fail.
- **Determinism**: IVE70-AC1's exact invocation run twice post-restore -- identical VERDICT lines,
  identical measured dE00 values, 4 pass / 0 fail both times.

## Compiler tools

- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors.

## Declared exclusions

- `modelPortfolioColors.ts` -- READ ONLY per the CTO ruling; unedited, confirmed.
- `DrillTree.tsx` -- in grant, no edit needed (see Fix section).
- The two AdvisorIntelligence tests -- amendment 1's own text: "read and run, never edited". Both
  confirmed byte-unedited this session and both now PASS unedited (IVE70-AC3); the S4 defect they
  surfaced was resolved entirely inside `chartColors.ts`, never by touching these two files.
- Starting a server for IVE70-AC2's live-page read -- forbidden by the task order's Environment
  clause; recorded UNVERIFIABLE-BY-INSTRUMENT, CVO-graded at L9.
- All git writes this turn -- REPOSITORY FREEZE (0.0.0_AB_MSTR); every artifact is
  STAGED-AWAITING-GATE, committed by the issuer post-freeze.

## Surprises

Five rows on file at this slot's coordinate (`DSGN_IRPTV1-W38-S1..S5`). S1 predates this cell. S2
and S3 are INERT, informational, unrelated to this cell's own edits. **S4** was the one this cell's
own work first surfaced: the fixedIncome pick chosen to clear THIS cell's dE00>=10 model-distance
bar (margin 21.7, `green700`) landed close enough to `ASSET_CLASS.commodities` (green900, CTO
101681) to break that colour's own ratified dE00>=20 bar in two out-of-grant tests
(`AdvisorIntelligence/__tests__/iv-e-49.commodities-distance.test.ts`,
`iv-e-51.commodities-chromatic.test.ts`). Was ARMED, disarm_owner 1.0.0_SA_CTO named. **S5 (this
turn) disarms S4**: amendment 1 delivered the naming S4 called for, this cell re-picked fixedIncome
to `lime600` (see the Amendment 1 section above), both AdvisorIntelligence tests now pass unedited
(6 pass / 0 fail, was 6 pass / 2 fail), and S5 records `hazard_standing` INERT, `disposition`
GRADUATED.

## Amendment 1 (issuer ruling, 2026-09-28 ~13:2xZ, disarming row W38-S4)

The issuer named exactly the side S4 flagged as out of this cell's call ("1.0.0_SA_CTO names which
side moves") and ruled it INTO this cell: re-pick `fixedIncome` (and any other mover) to clear BOTH
this cell's own dE00>=10 model-distance bar AND commodities' ratified dE00>=20 bar at once, reading
and running (never editing) the two AdvisorIntelligence tests. `ASSET_CLASS.commodities` stays
read-only (unchanged, still `PALETTE.green900`).

**Search.** `green700`'s own margin against models (21.7) came at the cost of a 14.0 margin against
commodities (bar 20) -- too close. An interpolation search along the entire green600-green700 RGB
ramp found no point clearing both bars by more than ~2.65 simultaneously (the two bars pull in
opposite directions on that ramp: darker clears the model bar better, lighter clears the commodities
bar better). Per the amendment's own text ("a hue outside the green family is allowed"),
`fixedIncome` now takes `PALETTE.lime600` (`#65a30d`), a lime/olive-green PALETTE token already
present (used elsewhere only in `GEO_PALETTE`, no existing `MIX_PIE`/`ASSET_CLASS`/model collision):
MEASURED dE00=17.9307 vs its nearest model ('50/50 ST/INT', an EXTENDED_MODEL_COLORS blend, margin
7.93) and dE00=28.1954 vs commodities/green900 (margin 8.20, IDENTICAL to green900's own
pre-existing documented margin against `ASSET_CLASS.other`/gray500 -- lime600 does not sit in the
population that constrained green700). `hueOf('#65a30d')` = 84.8 degrees, still inside the
`iv-e-12.cash-green.test.ts` green band [80,160], so `fixedIncome` still reads as a green hue.
`equity`/`alternatives`/`realEstate` are UNCHANGED (both already cleared the commodities bar: blue900
at 35.17, orange700 at 51.21).

**Text colour.** `lime600` needs DARK text (white-on-lime600 measures 3.089:1, below 4.5:1) --
`getAssetClassTextColor`'s `lightBackgrounds` array gained `PALETTE.lime600` (gray900-on-lime600
measures 5.743:1, clearing the bar); this is the OPPOSITE branch from the other three movers, which
all still take white text unchanged.

**Re-goldened tests re-goldened again.** `iv-e-12.cash-green.test.ts`'s `BASE_ASSET_CLASS.fixedIncome`
and `iv-e-12.positioning-reader.test.ts`'s `IVE70_NEW['Fixed Income']` both updated from `#047857`
(green700) to `#65a30d` (lime600), each file's own comment block gaining a third "amendment" note.
Both re-run clean: VERDICT: CASH-GREEN-OK; VERDICT: POSITIONING-ONLY-CASH-MOVED.

**IVE70-AC3 (new criterion, amendment 1's control).** `iv-e-49.commodities-distance.test.ts` and
`iv-e-51.commodities-chromatic.test.ts` run UNEDITED against the changed registry: 6 pass / 0 fail
(was 4 pass / 2 fail with green700). `iv-e-51`'s own mechanical census again picks `PALETTE.green900`
as the largest-margin winner (min dE00=28.1954 against `MIX_PIE.other`), matching what
`ASSET_CLASS.commodities`/`MIX_PIE.commodities` actually hold -- the exact invariant S4 found broken.

**Mutant/determinism re-run.** Same method as before (revert `fixedIncome` to `PALETTE.green500` in
worktree only, via Edit tool): IVE70-AC1 fails 1 of 4 as expected; restored; sha256 of
`chartColors.ts` measured `92e6f231...5c683cf` both before the mutant and after restoration
(byte-identical). IVE70-AC1 and IVE70-AC3 both re-run clean post-restore, output identical to the
values recorded in the proof instance.

**Disarm.** Row `DSGN_IRPTV1-W38-S5` appended to the investigation file: disarms S4
(`hazard_standing` INERT, `disposition` GRADUATED), citing the amendment's own text as the naming
act and the re-measured 6-pass/0-fail result as the evidence. All 22 JSON blocks in the investigation
file re-validated this turn (`json.loads` 22/22 clean; S5 validated against
`investigation_item.schema.json` via `jsonschema.validate` -- VALID). `surprise-row-gate.py` itself
reads staged/committed content (git-diff-driven), not a standalone file argument, and cannot be
meaningfully exercised under the repository freeze (no `git add` permitted this turn) -- the
JSON-syntax + schema checks above are the mechanical substitute available in-worktree.

## READY TO COMMIT

Per the mid-task freeze instruction, no commit was made this turn. See the final WORKER REPORT
message for the exact paths, subjects and evidence the issuer commits post-freeze.
