# TO-FE-s-66 result -- 0.9.0_WK_IRPT_FNTEND~16

**These captures (F66-AC6/F66-AC7) are FIXTURE-FED**: the real `/investor-reporting` route, answered
at the network layer by `scripts/ui-smoke.mjs`'s request router with a fixture body -- no live backend
route was reached. That is the right evidence for FWD-12 on this specific cell: FE-s-66's job is that
the answer-bearing fixtures EXIST, are shaped correctly (three keys, `status.state=READY` +
`unprojected_grant` on every key for the full variant; the same with `directory/resolve`'s
`unprojected_grant` narrowed for the partial variant), and drive the page into the READY /
partial-disclosure states so a LATER cell (FE-s-68) and the CVO's L9 read can see them render. It is
not the right evidence for the seven OTHER FWD-12 cards this round covers (their captures answer a
different half of "no re-learning" -- visual conformity on shipped surfaces -- and FE-s-66 makes no
claim there).

## 1. Classification: 16 retired, 4 kept untouched, 0 unclassified

**Whole-portal consumer census, run myself before deleting anything** (Grep tool, path = workspace
root `C:/tmp/wk-irpt_fntend-11-66-fe-s-66`, one call, all 16 dead filenames in one alternation pattern):
**41 files matched**. Of those, **40 are `org/` prose** -- task orders, deliverables (`result.md`,
`proof_of_spec.json`), and surprise-channel investigation/adjudication records that cite the filenames
historically (they were built and consumed by earlier cells, e.g. FE-s-2, FE-s-5, FE-s-6, FE-s-7,
FE-s-8, FE-s-9, FE-s-10, FE-s-11, whose own task orders and proofs are naturally full of these paths).
**Exactly 1 match is portal source code**:
`__tests__/fe-s-33/gen-global-holdings.ts:37`, a header COMMENT ("FE-s-7's Cottonwood fixture
(fixtures/smoke/fe-s-7-cottonwood.json) carries...") citing where a synthetic account id was derived
from -- never an import, `require`, or `readFileSync` of the file. **Denominator: 0 of 41 matches are a
runtime consumer.** Deleted:

```
fe-s-10-global.json      fe-s-10-one-firm.json     fe-s-7-smartx.json        fe-s-7-cottonwood.json
fe-s-9-modal.json        fe-s-9-preview.json       fe-s-11-print.json        fe-s-2-default.json
fe-s-2-one-firm.json     fe-s-3-failed.json        fe-s-5-49f-bd.json        fe-s-5-cottonwood-bd.json
fe-s-5-inflection-orion.json  fe-s-6-needs-correction.json  fe-s-6-uncertain.json  fe-s-8-narrative.json
```

**Kept untouched** (the 4-file ADAPTER-PLANE allowlist, verified still consumed by name outside this
cell's grant): `fe-s-6-ready.json` (`__tests__/fe-s-34/no-status.test.ts:63`), `fe-s-3-loading.json`
(`__tests__/fe-s-39/adapter-plane.test.ts:57`), `fe-s-4-performance.json` / `fe-s-4-analysis.json`
(`__tests__/fe-s-4/manifest.test.ts:205-206`). Their key shapes are the OLD in-process adapter names
(`resolve-scope`, `performance-report`, `export-preview`, ...) -- classified by FILE NAME on the
allowlist, never by body shape, which is the allowlist's whole point.

`fixtures/smoke/` also holds 19 pre-existing WIRE-KEYED files this order never named (`default.json`,
`fe-s-13-wire.json`, the `fe-s-14-*`/`fe-s-15-*`/`fe-s-16-*`/`fe-s-18-*` families, `fe-s-21-queued.json`)
built by other, already-drained round-11 cells that ship their own wire-shaped fixtures; they are
untouched and classify WIRE-KEYED on their own merit (every key begins
`/api/scoped/investor-reporting/` and matches a route template `contracts/wire/consumed.ts`'s
`WIRE_CONSUMED_ROUTE_KEYS` declares). This is why the directory held **37** files before my delete, not
the "twenty" the order's narrative names (16 dead + 4 kept) -- the order's "twenty" describes only the
OLD/legacy population it is retiring/keeping, not the whole directory census at the time this cell ran;
it does not affect any criterion (F66-AC3's `<expect>` is a wildcard `(\d+)` on the WIRE-KEYED count,
never a fixed total), so it is not filed as a row.

`__tests__/fe-s-66/smoke-classification.test.ts` derives its route templates from
`contracts/wire/consumed.ts`'s `WIRE_CONSUMED_ROUTE_KEYS` at run time (never a hand-typed list, so it
cannot silently drift from the contract), and prints:

```
SMOKE FILES: 23; WIRE-KEYED: 19; ADAPTER-PLANE: 4; UNCLASSIFIED: 0
SEEDED-UNCLASSIFIED: correctly flagged ( zz-seeded-unclassified.json )
```

23 = 21 real survivors (37 - 16) + 2 authored this cell. **The control (F66-AC4)**: a throwaway file
keyed `/api/scoped/investor-reporting/not-a-real-route` (WIRE_BASE-prefixed but not one of the 11
declared templates, and not on the 4-file allowlist by name) is copied into a TEMP directory alongside
every real fixture (verbatim), and the classifier is run over that copy. It is the ONLY one of 24 files
classified UNCLASSIFIED -- proving the guard can and does report non-zero when a genuine member of that
bucket exists, not a filter that vacuously always reads 0. Reproduced identically on a second run
(determinism).

## 2. The answer-bearing pair

`fixtures/smoke/reporting-answer-bearing.json` is a byte-identical (`diff` verified, 0 lines) copy of
`__tests__/fe-s-63/fixtures/export-ready.json`: three keys (`directory/resolve`, `performance/`,
`holdings/`), `status.state=READY` with `operation`, `source_dates.business_date`, `actions: []`,
`public_reason_code`, and `unprojected_grant` (`count:0, denominator:1, kinds:[]`) on all three.
`fixtures/smoke/reporting-answer-bearing-partial.json` is identical except `directory/resolve`'s
`unprojected_grant` becomes `{count:2, denominator:5, kinds:["accounts"]}` (`diff` verified, exactly 3
lines differ).

Both captured against the real `/investor-reporting` route at 1440px, dev server on port 5910:

- **f66_ac6.png** (full fixture): renders a `Ready` performance report -- cumulative-return chart,
  period returns, account detail, methods/sources, source attribution. The header strip reads `SELECTION
  No client selected`, `PERMITTED ACCOUNTS 3 of 3 in scope (3 permitted)`, `SCOPE MATCH narrowed`. No
  "not fully projected" fact box.
- **f66_ac7.png** (partial fixture): IDENTICAL body render, but the header strip additionally shows
  **`NOT FULLY PROJECTED -- 2 of 5 accounts not projected`** -- direct visual confirmation that
  `header/ScopeSummary.tsx`'s `scope.availability.unprojectedGrant.count > 0` partial-disclosure fact
  reads this fixture's edit correctly. This is the content FE-s-68 needs.

Both runs printed the OLD line `FIXTURES: 3 declared; 3 matched >=1 URL` -- every declared key matched a
live request, both times.

## 3. F66-AC6 / F66-AC7: REFUSED as literally invoked -- the instrument is not on this base

`scripts/ui-smoke.mjs` in this worktree (375 lines, portal HEAD `243089eb`) carries **zero** occurrences
of `FIXTURES-MATCH`, `--expect`, `--expect-text`, `--expect-style`, `--expect-ground`, `--inject-css`, or
`--delay` -- grep-verified before authoring anything. `IRPT_FNTEND.TO-FE-s-65...md:8` reads
`<status>pending</status>`: FE-s-65, the cell that builds these (per this order's own "THE INSTRUMENT"
clause), has not landed in this worktree's base.

Measured directly: I ran the literal ui-smoke invocation with `--expect` against an existing fixture
before authoring anything -- no `EXPECT` line printed (the flag is silently ignored, not refused; the
script does not validate unknown args), and the run printed `FIXTURES: 9 declared; 3 matched >=1 URL`,
never a `FIXTURES-MATCH:` line in any form. This order's own "THE INSTRUMENT" clause anticipates exactly
this condition ("if `ui-smoke.mjs` refuses `--expect` as an unknown flag, STOP: your base is wrong,
report it") -- the observed behavior (silent no-op) differs from the literal wording (a loud refusal)
but is the same substantive base-is-wrong condition, since it has the same consequence: the
`FIXTURES-MATCH: matched N of N` string F66-AC6/AC7's `<expect>` requires cannot be produced by this
build under any input.

Both F66-AC6 and F66-AC7 were run exactly as the order specifies (after authoring the two fixtures) and
measured **FAIL**, per BOUNDS' REFUSE clause -- the criterion's expectation is not edited or weakened.
Filed as surprise row `IRPT_FNTEND-W16-S1`
(`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`). The
dispatching message to this worker additionally asserted "your criteria only use existing
FIXTURES-MATCH/FIXTURES output" -- that assertion does not hold either: the existing output is
`FIXTURES: N declared; M matched >=1 URL`, a different line with different count semantics, never
`FIXTURES-MATCH: matched N of N`.

The fixtures themselves are correctly authored regardless of this gap (Section 2 above; both criteria's
*substance* -- every declared key matches a live request -- is true and independently confirmed by the
OLD line's own count and by the rendered content difference between the two captures).

## 4. Other criteria

- **F66-AC1** (whole-portal typecheck): `rc=0`.
- **F66-AC2/AC3/AC4**: see Section 1.
- **F66-AC5** (fe-s-34, fe-s-39, fe-s-4 suites): 98 pass / 6 skip / 0 fail of 104 tests across 18 files --
  unaffected by the 16 deletions.
- **F66-AC8** (whole suite): dev server on port 5910 stopped (`Stop-Process` on the PID
  `Get-NetTCPConnection -LocalPort 5910 -State Listen` named) and port verified closed (`curl --max-time
  2` returned `000`, exit 28) immediately before the run; `IRPT_FE_DEV_PORT` unset in that shell. Result:
  615 pass / 22 skip / 0 fail of 637 tests across 115 files.
- **F66-AC9** (judgment): recorded in the proof instance, no verdict given.

## Surprises filed

- `IRPT_FNTEND-W16-S1` (OBSERVATION, INERT) -- Section 3 above: the `FIXTURES-MATCH` instrument FE-s-65
  builds has not landed in this worktree; F66-AC6/AC7 REFUSED as literally invoked.
