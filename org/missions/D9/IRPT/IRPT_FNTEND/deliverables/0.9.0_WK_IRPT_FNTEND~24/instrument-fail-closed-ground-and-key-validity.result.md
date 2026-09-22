# IRPT_FNTEND.TO-FE-s-74 -- result (0.9.0_WK_IRPT_FNTEND~24)

These captures are FIXTURE-FED: the real `investor-reporting` route, served by this worktree's own
`vite` dev server (port 5904, this worker's own block), with every backend request answered at the
network layer by `scripts/ui-smoke.mjs`'s own router (a declared `--fixtures` JSON map) -- no live
route, no live backend, was ever reached. That is the right evidence for THIS card: FE-s-74 hardens
the INSTRUMENT itself (`scripts/ui-smoke.mjs`'s ground walker, its style-inequality branch, and a new
key-validity line), and the instrument's own correctness is a property of its CODE and its CONTROL
ARMS -- does a hardened assertion actually distinguish a genuinely unmeasurable paint from an
ordinary wrong colour, and a genuinely absent selector from a real one? -- not of whether any
particular route's content happened to be live. This is the READY ROOT of round 12: every other
round-12 cell depends on this fix landing first.

## The fix (`portal/scripts/ui-smoke.mjs`, additive only)

1. **`groundColor()` (W20-S2).** The pre-existing walker read ONLY `getComputedStyle(el).backgroundColor`
   and regex-parsed it as `rgba?\(...\)`. A composited/gradient paint (`backgroundImage != 'none'`) left
   `backgroundColor` transparent, and an opaque-but-unparseable colour space (`oklch(...)`/`lab(...)`/
   `color(...)`) never matched the regex either -- both classes fell through silently and the walk
   climbed PAST the real element to whichever solid ancestor it eventually found, misreporting that
   ancestor's colour as the target's own ground. Fixed: at EVERY element the walk visits (not just the
   first), a non-`'none'` `backgroundImage`, or a `backgroundColor` that fails the `rgba?\(...\)` parse
   while non-empty/non-transparent, now STOPS THE WALK on that element and returns a distinguishable
   `{state:'unmeasurable', raw}`; a selector matching nothing returns a separate `{state:'absent'}`
   rather than the same silent `null` both previously produced. Both print
   `EXPECT-GROUND[<css>]: UNMEASURABLE <raw>` and force `process.exitCode = 1` UNCONDITIONALLY -- not
   gated behind `--strict`, because a false PASS/FAIL on an unmeasurable read is exactly the defect
   being closed here.
2. **`--expect-style`'s `!=` branch (C-S146).** `firstComputedStyle` returns `null` only when the
   selector resolves to nothing; the old branch computed `null !== value` as satisfying the
   inequality, a false `PASS`. Both operators (`=`/`!=`) now print `UNMEASURABLE` on a `null` actual
   and set the same unconditional non-zero exit.
3. **`KEY-VALIDITY` (C-S147), new and additive.** Reads `WIRE_CONSUMED_ROUTE_KEYS` live out of the
   owning page's own `contracts/wire/consumed.ts` (page directory derived from the `--fixtures` path,
   not hand-pinned), strips each route's method verb, takes the static prefix up to (not including) its
   first `{param}`, and checks every `--fixtures` key against that candidate set. Prints
   `KEY-VALIDITY: <k> of <N> valid consumed.ts operation keys`, strictly additive beside the untouched
   `FIXTURES-MATCH` (fulfilment) line.

**One self-caught defect before any acceptance run:** the first route-key extraction regex
(`WIRE_CONSUMED_ROUTE_KEYS[^[]*\[([\s\S]*?)\]`) matched the FIRST `[` after the identifier, which is
the `[]` in the field's own `readonly string[]` type annotation, not the array literal -- it read
`KEY-VALIDITY: 0 of 9 valid` on the known-good fixture. Caught by hand-verifying the extraction against
the real file before trusting any acceptance run; fixed to anchor on `=\s*\[` (the assignment,
not the type). Confirmed correct (9 of 9) before F74-AC2 was re-run for record.

## Acceptance (this worktree, dev server port 5904, `IRPT_FE_DEV_PORT` set only while the server ran)

- **F74-AC1** (whole portal typechecks): `$ tsc -b --noEmit` / `rc=0` -- **PASS**
- **F74-AC2** (real CSS gradient on the ground container): `EXPECT-GROUND[...]: UNMEASURABLE
  linear-gradient(rgb(10, 23, 51), rgb(22, 51, 114))` -- **PASS**
- **F74-AC3** (opaque OKLCH background): browser's own computed-style serialization for this property
  reports the literal string `oklch(0.5 0.15 250)` (measured directly, not assumed) -> `EXPECT-GROUND[...]:
  UNMEASURABLE oklch(0.5 0.15 250)` -- **PASS**
- **F74-AC4** (genuinely absent ground selector): `EXPECT-GROUND[...]: UNMEASURABLE (selector matched
  nothing)` -- **PASS**
- **F74-AC5** (REGRESSION: ordinary solid wrong-colour paint): `EXPECT-GROUND[...]: FAIL rgb(196, 203,
  219)`, never UNMEASURABLE -- **PASS**
- **F74-AC6** (`!=` against an absent selector): `EXPECT-STYLE[...]: UNMEASURABLE (selector matched
  nothing)` -- **PASS**
- **F74-AC7** (REGRESSION: `!=` against a REAL, resolved element): literal invocation reads
  `EXPECT-STYLE[...]: FAIL rgb(95, 59, 227)` -- **REFUSED AS WRITTEN (status FAIL), a true and
  correctly-discriminating result, not an instrument defect; see "F74-AC7 adaptation" below for the
  independent confirmation that the control's actual MECHANISM (real element, never UNMEASURABLE)
  is sound.**
- **F74-AC8** (one bad fixture key, authored `__tests__/fe-s-74/fixtures/one-bad-key.json`):
  `KEY-VALIDITY: 8 of 9 valid consumed.ts operation keys` -- **PASS**
- **F74-AC9** (all-valid positive control, `fe-s-18-holdings-observed.json`): `KEY-VALIDITY: 9 of 9
  valid consumed.ts operation keys` -- **PASS**
- **F74-AC10** (REGRESSION: `FIXTURES-MATCH` unreplaced): `FIXTURES-MATCH: matched 3 of 9` -- **PASS**
- **F74-AC11** (whole suite green, dev server stopped and port reverified closed, `IRPT_FE_DEV_PORT`
  unset): `627 pass / 22 skip / 0 fail / 2642 expect() calls / Ran 649 tests across 119 files.
  [58.14s]` -- **PASS**
- **F74-AC12** (judgment, graded by the CVO at L9): RECORDED, no verdict taken. Evidence: every
  UNMEASURABLE/PASS/FAIL line above was produced by running the instrument, none hand-typed; F74-AC5,
  F74-AC7 (adapted) and F74-AC10 exercise the identical round-11 invocation SHAPES (plain
  `--expect-ground`/`--expect-style`/`--inject-css`/`FIXTURES-MATCH` against ordinary solid colours)
  and read exactly as round 11 would have read them -- unchanged.

## F74-AC7 adaptation (surprise row `IRPT_FNTEND-W24-S1`)

The literal invocation names `--expect-style '[data-slot="holdings-breadcrumb"]::color!=rgb(95, 59,
227)'` after `--click Holdings` and expects `PASS`. Run VERBATIM, it reads
`EXPECT-STYLE[[data-slot="holdings-breadcrumb"]::color]: FAIL rgb(95, 59, 227)` -- a TRUE,
correctly-discriminating result, not an instrument defect: `DrillTree.tsx:179-192` shows every
`holdings-breadcrumb` button (any drill depth) shares the identical className
`text-[hsl(var(--primary))] underline`, and that file's own comment (`:182-187`) records the
navy-vs-purple choice as "a judgment call this order does not make -- recorded for the CVO", i.e.
still genuinely undecided at this worktree's HEAD. No click sequence changes this element away from
primary purple, so the literal comparator (which equals the live colour) can never PASS given the
current, correct state. `DrillTree.tsx` is outside this worker's `<paths>` grant and the colour choice
is explicitly not this order's to make.

**Reported this as REFUSED-AS-WRITTEN (proof_of_spec status FAIL on the literal invocation, per
BOUNDS: "do not self-grade past a failure ... an order defect is reported, and the issuer amends
it")** -- exactly the same discipline FE-s-65's worker applied to its own AC16 in round 11. To confirm
this is genuinely a spec-assumption mismatch and not a real gap in the hardening, additionally ran the
identical selector/operator/click-step/fixtures with the comparator adapted to `rgb(22, 51, 114)`
(navy, a value independently known to differ from the live colour): it reads
`EXPECT-STYLE[[data-slot="holdings-breadcrumb"]::color]: PASS rgb(95, 59, 227)` -- a genuine PASS on
a real resolved element via the same non-null branch the control exists to exercise, never
UNMEASURABLE. Both runs are reported truthfully in the proof-of-spec instance; the criterion's own
`<expect>` text was not weakened and `DrillTree.tsx` was not touched. Filed `IRPT_FNTEND-W24-S1`
(OBSERVATION, INERT) at
`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.

**Consequence for `<status>`:** with one criterion (F74-AC7) genuinely refused as written, this
task order's `<status>` stays `pending`, not `complete` -- eleven of twelve criteria PASS-by-output
(F74-AC12 is judgment, recorded with no verdict), one is REFUSED with its measurement, none is
self-graded past a failure.

## Controls

**Mutant.** Extracted the pre-fix instrument verbatim (`git -C portal show HEAD~1:scripts/ui-smoke.mjs`,
run from a temporary sibling file inside `scripts/`, deleted immediately after both runs) and re-ran
F74-AC2's exact gradient invocation and F74-AC6's exact absent-selector-inequality invocation against
it: the mutant printed `EXPECT-GROUND[...]: PASS rgb(255, 255, 255)` (the exact silently-climbed-past
false PASS W20-S2 names) and `EXPECT-STYLE[...]: PASS null` (the exact false PASS C-S146 names). The
fixed instrument prints `UNMEASURABLE` on both of the same invocations. FIRED-AS-EXPECTED.

**Determinism.** F74-AC2's own invocation run twice in immediate succession against the same live dev
server; `EXPECT-GROUND`, `FIXTURES-MATCH` and `KEY-VALIDITY` lines diffed byte-for-byte identical
(`diff` rc=0).

## Portal commit
`portal/scripts/ui-smoke.mjs` (the three fixes above) and new test surface
`src/pages/InvestorReporting/__tests__/fe-s-74/fixtures/one-bad-key.json`. Committed at portal
`b762ac14f47b90e531fac53b7f023e25c3ad1570`, LOCAL on branch `wk-irpt_fntend-12-74-fe-s-74-portal`
(portal frozen); not pushed.

## Workspace commits
Surprise row `IRPT_FNTEND-W24-S1`, this proof-of-spec instance, this result file and the `<status>`
flip -- see WORKER REPORT for the final hash. LOCAL on branch `wk-irpt_fntend-12-74-fe-s-74`, not
pushed.
