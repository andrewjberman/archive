# IRPT_FNTEND.TO-FE-s-81 -- fixture generator repair survives regeneration -- result

**FIXTURE-FED disclosure.** No fixture was hand-authored or hand-edited by this worker. Every value in
this cell's evidence comes from ONE of: (a) the generator's own console output, run verbatim under a
timeout bound; (b) `node -e` reads of the fixture files the generator wrote, as a live side effect of
running it (`fixtures/smoke/default.json`, `fe-s-13-wire.json`, `fe-s-14-print-v1.json` -- none of these
three files is in this cell's `<paths>` grant and none was committed by hand); (c) `bun test` runs of
`__tests__/fe-s-75/parse-control.test.ts` (pre-existing, round 12) and the new
`__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts` (this cell's own grant); (d)
`git diff`/`git log` reads of this worktree. No dev server was needed for this cell (a pure data-contract
fix, no UI surface) -- confirmed no port in this cell's block (5965-5969) was listening before AC5.

## The fix

`__tests__/fe-s-13/gen-corpus.ts`'s shared `envelope()` helper -- the one function
`generateCorpus()`/`generateSmokeMap()`/`generatePublishedMap()`/`generatePrintMap()` all build every
response body through -- never set `unprojected_grant`. FE-s-75 (round 12) hand-repaired
`fixtures/smoke/default.json` directly (12 of 12 entries), but that repair lived only in the fixture
file, not in the generator, so the next `bun run .../gen-corpus.ts` (the file's own documented
invocation) would have silently stripped it back out, and the two sibling files
(`fe-s-13-wire.json`, `fe-s-14-print-v1.json`) never carried the field at all (measured 9/9 and 2/2
missing, per this order's own framing).

**Chosen approach: make `envelope()` emit a correct value (the order's preferred option), not a
refuse-to-overwrite guard.** The generator has no per-route enforcement census to draw a real count
from -- every producer `.valid.json` instance it reads is the FULL authorized document, never a partial
one -- so there is no live signal in this generator's own inputs that could vary the value entry to
entry. The PRD's CONTRACTS clause (v0.7/v0.8, `org/missions/D9/IRPT/IRPT_FNTEND/prd/IRPT_FNTEND_PRD.md:123`)
states the response-envelope guarantee is **present-at-zero**: `unprojected_grant` is NON-OPTIONAL on
every non-refused response envelope, present even where structurally zero (the same guarantee the
`irpt-holdings` route carries). The truthful value for this smoke corpus -- which never constructs a
refusal or a partial-grant scenario -- is therefore the baseline "nothing unprojected": `{count: 0,
denominator: 1, kinds: []}`. This is the EXACT value FE-s-75 hand-set on all 12 `default.json` entries
(verified, see below), so emitting it in the generator is what makes that repair survive a re-run rather
than requiring another hand fix next time.

```ts
const NO_UNPROJECTED_GRANT: Readonly<{ count: number; denominator: number; kinds: readonly string[] }> = {
  count: 0,
  denominator: 1,
  kinds: [],
}

function envelope(operation: string, data: unknown, withStatus: boolean): Record<string, unknown> {
  const body: Record<string, unknown> = { contract_version: 'v1', operation, firm_id: FIRM_ID, data }
  if (withStatus) body.status = status
  body.unprojected_grant = NO_UNPROJECTED_GRANT
  return body
}
```

Key order matches the existing committed `default.json` exactly (`unprojected_grant` last, after
`status` when present) -- confirmed by inspecting `Object.keys()` on every one of its 12 entries before
writing the fix.

Also added `__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts` (this cell's own
grant): widens FE-s-75's `parse-control.test.ts` pattern (which only reads `default.json`) to all three
files the generator produces, reading them off disk as they sit after a regeneration, plus the same
negative control FE-s-75's test runs (an entry with the key stripped still throws
`EnvelopeMismatch('unprojected_grant')`). This is a permanent regression guard inside the whole-suite
run: the fixture files themselves are not in this cell's write grant and are not committed by this
worker (see "Fixture files, deliberately not committed" below), so this test is what keeps a future
`bun run gen-corpus.ts` honest, not a static snapshot.

## Acceptance results

**F81-AC1 -- the whole portal typechecks.**
```
$ cd portal && timeout 180 bun run typecheck; echo rc=$?
$ tsc -b --noEmit
rc=0
```
Matches `<expect>rc=0(?![0-9])</expect>`. **PASS.**

**F81-AC2 -- the generator runs to completion against the current fixture files.**
```
$ cd portal && timeout 120 bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts
REQUEST RECORDS: 12 of 12; SMOKE KEYS: 9; PUBLISHED MAP KEYS: 12 of 12 DECLARED; PRINT MAP KEYS: 2
rc=0
```
rc=0 and the run genuinely regenerated all four outputs (confirmed below). But the criterion's own
`<expect>(?i)wrote|generated|done|complete</expect>` does **not** match this output: none of `wrote`,
`generated`, `done`, `complete` (case-insensitive) appear anywhere in it (`grep -iE
'wrote|generated|done|complete'` against the line returns no match). This generator's closing
`console.log` (gen-corpus.ts:313-316 at HEAD) has used this `RECORDS`/`KEYS`/`DECLARED` vocabulary since
the file's introduction at FE-s-13 (`git -C portal log --oneline -- .../gen-corpus.ts`: `d7b3d615`
FE-s-13, `7151f2c4` FE-s-14 R1, `e5833214` FE-s-15 -- none of those diffs, nor this cell's own edit,
touch the closing print block), so this is a **pre-existing order defect**, not a regression from this
fix. Per BOUNDS ("REFUSE any criterion you cannot satisfy as written ... do not weaken a criterion: an
order defect is reported, and the issuer amends it"), this criterion is recorded **FAIL** with this
measurement, and did NOT edit the console.log wording merely to chase the regex. Filed as row
`IRPT_FNTEND-W31-S1` in `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`
(class OBSERVATION, hazard_standing ARMED, disarm_owner `2.0.0_SA_COO~F`). **FAIL (order-defect, not a
substance defect -- see AC3/AC4/AC5 below for the substance).**

**F81-AC3 -- all three generated fixture files carry `unprojected_grant` on every entry.**
```
$ node -e "...for (const f of [default.json, fe-s-13-wire.json, fe-s-14-print-v1.json]) {...}"
src/pages/InvestorReporting/fixtures/smoke/default.json: 12 of 12 carry unprojected_grant
src/pages/InvestorReporting/fixtures/smoke/fe-s-13-wire.json: 9 of 9 carry unprojected_grant
src/pages/InvestorReporting/fixtures/smoke/fe-s-14-print-v1.json: 2 of 2 carry unprojected_grant
rc=0
```
Matches `<expect>default\.json: 12 of 12 ...[\s\S]*fe-s-13-wire\.json: 9 of 9 ...[\s\S]*fe-s-14-print-v1\.json: 2 of 2 ...</expect>`
exactly. **PASS.**

**Required control (task order's own text, beyond AC3's literal counts): data-equivalence, not merely
field count.** `git diff --stat -- src/pages/InvestorReporting/fixtures/smoke/default.json` after AC2's
regeneration is **empty** -- the regenerated file is byte-identical to round 12's committed hand
repair, same 12 entries, same values, confirmed not merely the same count. The two sibling files
changed ONLY additively: `git diff --stat` shows `fe-s-13-wire.json +47/-1` and `fe-s-14-print-v1.json
+10/-0`, both being exactly nine and two new `unprojected_grant` blocks respectively (one per entry),
with every other field byte-unchanged. The 12 wire request-corpus files (`fixtures/wire/requests/*.json`,
`generateCorpus()`'s output, a separate write path from `envelope()`) show `git status` as modified
purely from a CRLF-normalization warning with zero actual diff lines -- confirmed with `git diff --stat`
returning nothing for that directory, i.e. this fix changed no request-corpus byte.

**F81-AC4 -- FE-s-75's own `parse-control.test.ts` still reads clean against the regenerated
`default.json`.**
```
$ cd portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-75
UNPROJECTED_GRANT PRESENT: 12 of 12
PARSED CLEAN: 12 of 12
CONTROL: removing unprojected_grant from '.../directory/search' throws EnvelopeMismatch('unprojected_grant') -- as expected
3 pass
0 fail
rc=0
```
Matches `<expect>(?<![0-9])0 fail</expect>`. **PASS.** The regeneration changed no OTHER field's
truthful value (per the data-equivalence control above), only added the missing key.

**F81-AC5 -- the whole IRPT_FNTEND suite is green.**
Dev server confirmed not running before this run (`curl` on both worktree-block ports 5965/5966
returned `000`); `IRPT_FE_DEV_PORT` unset.
```
$ cd portal && timeout 600 bun test src/pages/InvestorReporting
...
src\pages\InvestorReporting\__tests__\fe-s-81\generator-output-carries-unprojected-grant.test.ts:
default.json: unprojected_grant present 12 of 12
default.json: parsed clean 12 of 12
fe-s-13-wire.json: unprojected_grant present 9 of 9
fe-s-13-wire.json: parsed clean 9 of 9
fe-s-14-print-v1.json: unprojected_grant present 2 of 2
fe-s-14-print-v1.json: parsed clean 2 of 2
CONTROL: removing unprojected_grant throws EnvelopeMismatch('unprojected_grant') -- as expected
...
641 pass
22 skip
0 fail
2683 expect() calls
Ran 663 tests across 123 files.
rc=0
```
Matches `<expect>(?<![0-9])0 fail</expect>`. **PASS.** This cell's own new test (fe-s-81) participated
in the whole-suite run and passed on all three files plus its negative control -- consistent with the
standalone AC3/AC4 reads above, two different instruments agreeing.

## Fixture files, deliberately not committed

`fixtures/smoke/default.json`, `fe-s-13-wire.json` and `fe-s-14-print-v1.json` are **not** in this
cell's `<paths>` grant (`portal/src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts`,
`__tests__/fe-s-81/`, and the investigation file only) and `.tools/owned-paths-validate.py`'s
`_order_grants` check (exact path / glob / directory-prefix) does not admit them, so this worker did not
stage or commit the regenerated bytes -- consistent with the order's own instruction ("This cell does
NOT touch fixtures/smoke/.../json directly -- only the generator... AC2 regenerates them as a side
effect of running the (fixed) generator, never by hand-editing the JSON"). AC2's own invocation performs
the regeneration wherever it is run (deterministically, from the now-fixed, committed generator source);
AC3-AC5 above were read against that live, uncommitted regeneration in this same worktree, in the
sequence the order's own HOW section describes (run each invocation in order). A fresh checkout of this
worker's branch that runs AC2 before AC3-AC5, in that same order, reproduces the identical evidence.

## Controls

**Mutant.** FE-s-75's `parse-control.test.ts` already carries the required negative control (an entry
with `unprojected_grant` deleted still throws `EnvelopeMismatch('unprojected_grant')`) and this cell's
own new test repeats it independently against all three files' first entries. Both fired as expected in
every run above -- the positive PASS is not vacuous.

**Determinism.** F81-AC2/AC3 run twice in immediate succession (not shown verbatim above for space; both
runs printed byte-identical `REQUEST RECORDS`/`SMOKE KEYS`/`PUBLISHED MAP KEYS`/`PRINT MAP KEYS` lines
and byte-identical `N of N carry unprojected_grant` lines) -- stable.

## Surprise row filed

`IRPT_FNTEND-W31-S1` -- F81-AC2's `<expect>` regex cannot match this generator's actual (pre-existing)
completion-message wording. Filed at
`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`; class
OBSERVATION, hazard_standing ARMED, disarm_owner `2.0.0_SA_COO~F` (the order's own issuer, who must
amend F81-AC2's `<expect>`).

## Status

`<status>` left as issued (`pending`) -- one mechanical criterion (F81-AC2) reads FAIL against its own
literal `<expect>`, so per the governing discipline this order is NOT flipped to `complete`. The
substance the cell exists to fix (the generator repair surviving regeneration on all three files,
data-equivalent to round 12's hand repair) is fully proven PASS by AC1, AC3, AC4 and AC5.

## Addendum -- COO amendment, F81-AC2 re-graded PASS

`2.0.0_SA_COO~F` independently confirmed the order defect above (same command, same worktree) and
amended `F81-AC2` in the shared tree (CLOUD `1edf2d446e`, cherry-picked into this worktree
`843b8851eb`): the criterion now reads `<invocation>... ; echo rc=$?</invocation><expect>rc=0(?![0-9])
</expect>` -- grading on the generator's genuine completion signal instead of the guessed wording. Bar
unchanged (the generator runs cleanly); only the detection mechanism was corrected.

Re-run against the amended invocation, this same worktree, same generator source, same output
vocabulary as originally measured:
```
$ cd portal && timeout 120 bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts; echo rc=$?
REQUEST RECORDS: 12 of 12; SMOKE KEYS: 9; PUBLISHED MAP KEYS: 12 of 12 DECLARED; PRINT MAP KEYS: 2
rc=0
```
Matches `<expect>rc=0(?![0-9])</expect>`. **F81-AC2: PASS.**

All five criteria (F81-AC1..AC5) now read PASS. `proof_of_spec.json` updated (F81-AC2's acceptance row
only; AC1/AC3/AC4/AC5 unchanged, still valid) and re-validated:
`python .tools/proof-of-spec-check.py <instance> F81-AC1,F81-AC2,F81-AC3,F81-AC4,F81-AC5
--governing-order <TO>` -> `VALID (rc=0)`. `<status>` flipped to `complete`. Row `IRPT_FNTEND-W31-S1`
stands as filed (disposition is `disarm_owner` `2.0.0_SA_COO~F`'s to write in the channel; the amendment
commit is the disarming act it names, this worker did not edit the investigation file).
