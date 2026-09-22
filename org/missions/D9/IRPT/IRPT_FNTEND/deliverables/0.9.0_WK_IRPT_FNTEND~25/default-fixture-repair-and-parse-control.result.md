# FE-s-75 -- default smoke fixture repair and parse control -- result

**FIXTURE-FED disclosure (first, per HOW step 7):** this cell's OWN write surface IS a fixture
(`portal/src/pages/InvestorReporting/fixtures/smoke/default.json`). Nothing here is a state ASSERTED
to be correct that was not independently measured through `contracts/envelope.ts`'s real parser
(`parseIrEnvelope`) and through `scripts/ui-smoke.mjs` against a live dev server. No claim in this
file rests on the fixture's own prose.

## Decision: REPAIR, not retirement

**Census first (F75-AC2), printed denominator, read BEFORE deciding.** The task order's own literal
invocation (`grep -rn ... src/ --include='*.ts' --include='*.tsx' | wc -l`) read **4** hits BEFORE
any edit this cell made:

```
src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts:42   (PUBLISHED_FILE = ...default.json)
src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts:220  (comment)
src/pages/InvestorReporting/__tests__/fe-s-14/published-map.test.ts:4   (comment)
src/pages/InvestorReporting/__tests__/fe-s-14/published-map.test.ts:30  (MAP_PATH = ...default.json)
```

A wider census (comp-find, `--all`, whole tree, not scoped to `src/**.ts,tsx`) found the fixture is
also referenced by `__tests__/fe-s-1/fixtures.test.ts:143` (reads it for the smoke-map key-coverage
test) and `fixtures/index.ts:130` (`SMOKE_MAP_FILE` constant, no further consumer), and -- outside
this repo entirely -- by a CVO probe script
(`org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_FNTEND_ROUND11_PROBES_20260922.mjs:33-34`, which is
the very diagnostic that measured "0 of 12 carry unprojected_grant") and by the producer's own
paired seam test, `infra/aws/lambda/investor-reporting/_contracts/tests/test_seam_paired.py`'s
`consumer_smoke()`, which reads this file out of "the primary checkout" (a DIFFERENT worktree path,
not this one) per `gen-corpus.ts`'s own header comment (:220-224).

**Every one of these is a real, live consumer** (a generator that writes the file, two tests that
read its keys/shape, an external probe, an external paired seam test) -- none is dead. Per this
order's own framing ("if it has zero real consumers left ... the correct fix may be RETIREMENT ...
if it has live consumers, add `unprojected_grant` ... to all 12 entries"), the correct call is
**REPAIR**. F75-AC3 is graded on that basis, not N/A.

**Root shape read first.** `contracts/envelope.ts:278-281` (this worktree HEAD): `parseIrEnvelope`
throws `EnvelopeMismatch('unprojected_grant', operation)` when `!('unprojected_grant' in body) ||
!isUnprojectedGrantShaped(body.unprojected_grant)`. `isUnprojectedGrantShaped` (:200-206) requires
exactly `{count: number, denominator: number, kinds: string[]}`. All 12 of `default.json`'s declared
entries omitted the key entirely (confirmed by direct read of the file before editing).

## The fix

Added `"unprojected_grant": {"count": 0, "denominator": 1, "kinds": []}` to all 12 top-level entries
of `fixtures/smoke/default.json` -- the shape `isUnprojectedGrantShaped` requires, present-at-zero
(the same convention every other repaired fixture in this tree already uses, e.g.
`fixtures/fe-s-15/job.*.json`). The diff is purely additive: `git diff --stat` reads
`1 file changed, 61 insertions(+), 1 deletion(-)` (the one deletion is a closing-bracket line
absorbed into the new block), confirmed by reading every `+`/`-` line of the diff directly -- twelve
identical five-line blocks, nothing else touched.

## Parse-control test (F75-AC4)

New file `__tests__/fe-s-75/parse-control.test.ts` (this cell's own surface), three cases:
1. every entry carries `unprojected_grant` (12 of 12, printed);
2. every entry parses clean through the real `parseIrEnvelope` (12 of 12, printed, no catch);
3. **a control is a claim** (HOW step 4): a negative-control case removes `unprojected_grant` from
   one entry and confirms `parseIrEnvelope` still throws `EnvelopeMismatch` with `.field ===
   'unprojected_grant'` -- so the positive result above is not vacuous; the parser genuinely still
   enforces the field, this fixture now genuinely satisfies it.

`bun test src/pages/InvestorReporting/__tests__/fe-s-75`: **3 pass, 0 fail, 4 expect() calls.**

## Surprise filed (IRPT_FNTEND-W25-S1)

`default.json` is GENERATED, not hand-authored: `__tests__/fe-s-13/gen-corpus.ts`'s own header says
"the output is committed", and `generatePublishedMap()` writes exactly this file via an `envelope()`
helper that never sets `unprojected_grant`. `gen-corpus.ts` is outside this order's `<paths>` grant,
so it is not edited here -- but a future re-run of the documented generator invocation (`bun run
src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts`) would silently strip this repair back
out. Measured the same defect on two sibling files the identical helper produces:
`fixtures/smoke/fe-s-13-wire.json` (9 of 9 entries missing the field) and
`fixtures/smoke/fe-s-14-print-v1.json` (2 of 2 missing) -- confirming the defect lives in the shared
generator, not uniquely in the one file this order owns. Filed as
`IRPT_FNTEND-W25-S1` (class OBSERVATION, hazard_standing ARMED, disarm_owner `2.0.0_SA_COO~F`) in
`INVESTIGATION_v2.md`.

## Acceptance results

- **F75-AC1** (typecheck): `tsc -b --noEmit` -> rc=0. PASS.
- **F75-AC2** (census): printed above, 4 hits pre-edit (scoped invocation); repair decided on that
  plus the wider consumer census. PASS (the criterion only asks for a printed number; `^[0-9]+$`).
  NOTE: re-running the identical invocation AFTER this cell's own edits (which added a new test file
  under `__tests__/fe-s-75/` that itself mentions the fixture path three times, in its own header
  comment and its own `FIXTURE_PATH`/`describe` strings) now reads **7**, still `^[0-9]+$`. Both
  numbers are reported for a complete record; the decision-driving read was the pre-edit 4.
- **F75-AC3**: `ui-smoke.mjs` against the repaired fixture, `--expect '[data-slot="scope-error"]'
  --expect-text '...::Scope could not be resolved'` -> `ASSERT-CONTENT: 0 of 2 met` -- matches
  `<expect>` verbatim. The control F67-AC3 originally wanted now genuinely reads clean: no
  parse-error-driven false content. PASS.
- **F75-AC4**: `bun test .../__tests__/fe-s-75` -> `3 pass`, `0 fail`. PASS.
- **F75-AC5**: dev server stopped, port 5910 verified closed (`curl` -> `000`), `IRPT_FE_DEV_PORT`
  unset, `bun test src/pages/InvestorReporting` -> `630 pass, 22 skip, 0 fail, 2646 expect() calls,
  Ran 652 tests across 120 files`. PASS.
- **F75-AC6**: JUDGMENT. RECORD, no verdict taken here: repair (not retirement) was the call given
  the measured consumer census above; no other fixture family was touched (this cell's only edits
  are `fixtures/smoke/default.json` and the new `__tests__/fe-s-75/` directory).

## Commits

- Portal: `a7f7ce23` (branch `wk-irpt_fntend-12-75-fe-s-75-portal`, LOCAL, portal frozen) -- fixture
  repair + parse-control test.
- Workspace: this result file + proof-of-spec instance + investigation row + status flip, committed
  via `.tools/safe-commit.sh` on branch `wk-irpt_fntend-12-75-fe-s-75`, LOCAL.
