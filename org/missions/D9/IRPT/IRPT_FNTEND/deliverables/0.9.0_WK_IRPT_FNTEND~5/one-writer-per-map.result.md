# IRPT_FNTEND.TO-FE-s-41 -- one writer per fixture map, and the narrative bound to its own revision

**Worker:** `0.9.0_WK_IRPT_FNTEND~5` | **Branch:** `wk-irpt_fntend-6-5-fe-s-41` (workspace and portal) |
**Portal commit:** `0ebc6b20` (LOCAL; portal is FROZEN) | **Base:** workspace `1f5d387e17`, portal `741bb54b` |
**Order status:** left `pending`, because **F41-AC7 FAILS** (1 fail of 546). Row `IRPT_FNTEND-W5-S5` (BLOCKING).

## 1. The one writer, and why (W2-S24)

`fixtures/smoke/fe-s-14-global.json` now has ONE writer: **`__tests__/fe-s-14/gen-maps.ts`**.

- gen-maps.ts builds the whole map. It composes FE-s-33's two Holdings envelopes into it by calling
  `globalHoldingsEnvelopes(resolveEnvelope, observedHoldings)`.
- `__tests__/fe-s-33/gen-global-holdings.ts` is now a pure module. It exports that function and
  `HOLDINGS_KEY`, and it writes nothing and reads nothing.
- gen-maps.ts reads the observed Holdings envelope from `fe-s-18-holdings-observed.json`, which is
  gen-fixtures.ts' committed output. It refuses to write if that envelope is absent, so the Global map can
  never again be written without its Holdings.
- gen-maps.ts takes an optional output directory as its first argument. Its inputs are always the committed
  files.
- Run order, stated in all three generator headers: `fe-s-18/gen-fixtures.ts`, then `fe-s-14/gen-maps.ts`.

**Why gen-maps.ts, and not gen-global-holdings.ts:**
- The map is FE-s-14's, and every other key in it is built by gen-maps.ts.
- gen-maps.ts already wrote the file whole.
- It is the command a reader regenerating "the FE-s-14 maps" runs. So the writer that must be run is the
  writer that is run, and no order between two scripts has to be remembered. The hazard was a
  remembered-order rule; it is gone.
- The other direction (gen-global-holdings.ts writing the whole map) would have needed it to rebuild
  FE-s-14's resolve and performance keys. That duplicates FE-s-14's logic, or imports a module that writes as
  a side effect.

**The regenerated map is byte-identical to the committed one.** F41-AC4, run into a fresh scratch directory:
17787 bytes both, sha256 `aba71a862457ff7587934c09d5668f938ea8bda069abc713015f008b840b456a` both. The
writer's other three maps also regenerate byte-equal (3 of 3). The map's bytes did not change, so
`fe-s-14-global.json` is not in the portal commit; its sole writer is now the one that reproduces it.

## 2. The narrative re-bound (W2-S27)

- The frozen map took all its non-performance keys from `fe-s-13-wire.json`, including its narrative
  packet. That packet names `perf-9`.
- The frozen map's performance body is `fe-s-16-print-narrative.json`'s. That fixture's own narrative,
  authored beside that body, names `rev-49f-000091`, which is the frozen report's revision.
- `gen-fixtures.ts` now sets `frozen[NARRATIVE_KEY] = frozenNarrative()`: that fixture's narrative, copied
  whole and never edited. It is refused (the generator throws) if it names any revision other than
  `FROZEN_REVISION`.
- Nothing was hand-typed. gen-fixtures.ts was run, and its four outputs in the grant were committed.

F41-AC5 reads the binding two ways, on the wire and through the shipped parser (`parseIrEnvelope` ->
`NarrativePacket.performanceRevision`). It reads it in the frozen map and in each of the three Holdings maps
built from it: **4 of 4 bound to rev-49f-000091**, and each Holdings map's narrative is identical to the
frozen map's. Controls:
- in memory, perf-9 put back: 0 of 4 bound;
- the frozen map at portal `741bb54b` (from history): `narrative names=perf-9 bound=NO`.

## 3. What survives, byte for byte (the fields FE-s-26 and FE-s-33 own)

Each of the four regenerated maps was compared per member with `git show HEAD:<map>`
(`.scratch` python, both sides serialised `indent=2`):

| map | members | key order | members differing | holdings envelope | holdings `status` (FE-s-26) | holdings `nodes` (FE-s-33 tree) | narrative |
|---|---|---|---|---|---|---|---|
| fe-s-18-frozen.json | 9 -> 9 | same | narrative only | byte-equal | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-observed.json | 9 -> 9 | same | narrative only | byte-equal | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-target.json | 9 -> 9 | same | narrative only | byte-equal | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-missing-attribution.json | 9 -> 9 | same | narrative only | byte-equal | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |

The Global map is unchanged byte for byte, so FE-s-33's two Global envelopes (F-49F and F-CW) survive whole.

The whole-suite run re-grades these with the owning cells' own tests:
- F33-AC5 against `git show 0c456933` (FE-s-26's statuses, 3 of 3);
- F33-AC4's trees;
- F33-AC6's Global map.

All three are green in the AC7 run; the one failure is elsewhere (s.5). The `'ADVISORY'` token is untouched.

## 4. The census (F41-AC2), and what it cannot see

**Denominator.** `one-writer.test.ts` walks every file under `__tests__/`: 136 source files (.ts 130, .mjs 6).
Of these, 26 are generators and helpers, 95 are test files and 15 are declaration files. 16 non-source files
are counted and not scanned. 16 of the 136 files make any filesystem write call, at 40 call sites.

**Result.** Exactly one site writes the map: `fe-s-14/gen-maps.ts:147`.

**Controls.**
- A seeded direct writer raises the count to 2.
- A seeded writer that goes through a local wrapper, the way gen-fixtures.ts writes, raises it to 2.
- A seeded reader that names the map in comments and writes a different file leaves it at 1.
- The census over the two real generators at portal `741bb54b` finds 2 of 2:
  - `gen-maps.ts:94`
  - `gen-global-holdings.ts:146`

The seeded sources are `.txt` files under `fe-s-41/seeded/`, so the walk never reads them.

**The rule, and its blind spots.** A write call counts when its first argument, expanded through the same
file's initialisers (four levels), contains the literal file name. A call of a local function whose body
writes also counts. It does NOT see:
- a name assembled from pieces with no literal;
- a path imported from another module;
- a wrapper of a wrapper;
- a write inside a template literal's `${}`;
- any writer outside `__tests__/`.

**The unscoped read for the last blind spot:** `comp-find 'fe-s-14-global' portal --files --all` at the base
reads 14 hits across 1353 files. They are in 5 files: the map itself; gen-maps.ts; gen-global-holdings.ts;
gen-fixtures.ts (a comment); and fixtures-reach.test.ts (a reader). No writer is outside `__tests__/`.

## 5. The failure (F41-AC7) -- BLOCKING row IRPT_FNTEND-W5-S5

**The runs.** The whole suite ran with `IRPT_FE_DEV_PORT=5265`, measured closed both times before the run
(`ConnectionRefusedError` after 2.03 s on 127.0.0.1 and 2.02 s on ::1).

| | pass | skip | fail | tests | files |
|---|---|---|---|---|---|
| Baseline, portal `741bb54b` | 523 | 13 | 0 | 536 | 94 |
| With the change, `0ebc6b20` | 532 | 13 | **1** | 546 | 95 |

**The failure.** `__tests__/fe-s-32/holdings-in-a-browser.test.ts:256`, in "the NO-ANSWER map is the observed
map with ONE member changed: the holdings status".

**The cause: the premise named four children of the frozen map, and there are five.** A census by content
found 5 of 145 JSON files under `portal/src` carrying the frozen performance member:
- the four in the grant, which now name rev-49f-000091;
- `__tests__/fe-s-32/holdings-no-answer.json`, which names perf-9. It was hand-copied from the observed map
  at FE-s-32 (portal `7df6b4a2`), with no generator, and the fe-s-32 test asserts that it differs from the
  observed map in exactly one member.

**Why it cannot be fixed here.** F41-AC5 needs the Holdings maps to carry the re-bound narrative. The only
edit that makes the fe-s-32 test agree is to `holdings-no-answer.json`, which is not in `<paths>`. No edit
was made there.

**What the issuer can do.**
- Grant `holdings-no-answer.json` to a cell. It is the same no-generator hand-copy shape W2-S24 named for
  writers, so deriving it from the observed map is the durable fix.
- Or drain FE-s-41 together with that re-derivation.

Until then, draining `0ebc6b20` as-is turns the shared suite red by exactly this one test.

## 6. Outside the grant, left as found

- **Row W5-S6 (INERT):** running the two ordered generators rewrote four maps outside `<paths>`:
  `fe-s-14-49financial.json`, `fe-s-14-inflection.json`, `fe-s-14-cottonwood.json` and
  `fe-s-16-print-prehistory.json`.
  - Each measured byte-identical to `git show HEAD` (`git diff --quiet` rc=0).
  - Not staged. `git status` still lists them as stat-dirty.
- **A stale comment:** `__tests__/fe-s-33/ambient-shims.d.ts:14-15` still says gen-global-holdings.ts writes
  the Global map. The `writeFileSync` declaration it explains is still used across the program.
- **No capture was taken.** No non-test source file was touched.

## 7. Session log

1. First act: branch `wk-irpt_fntend-6-5-fe-s-41`, `TREE-OK`. Portal worktree on the same branch
   @`741bb54b`.
2. Premises re-grounded:
   - writers at `gen-maps.ts:94` and `gen-global-holdings.ts:57`/`:146`;
   - `perf-9` once in the frozen map;
   - `rev-49f-000091` once as a whole value (twice as a substring, inside `calc-rev-49f-000091`);
   - the Holdings maps built from the whole frozen map.
3. Baseline whole suite at the base: 523 pass, 13 skip, 0 fail across 536 tests in 94 files.
4. Edited `gen-global-holdings.ts` (pure), `gen-maps.ts` (the one writer) and `gen-fixtures.ts`
   (`frozenNarrative`). Wrote `fe-s-41/one-writer.test.ts`, its shims and three seeded controls.
5. Ran `gen-fixtures.ts`, then `gen-maps.ts`. Four maps changed, in the narrative member only; five
   out-of-grant outputs were byte-identical.
6. Ran the criteria:
   - AC1 rc=0;
   - AC2-AC5: 10 pass, 0 fail, and 43 of 43 lines identical on a second run;
   - AC6: `PAIRED: 1 report, 3 views`;
   - AC7: 1 fail.
7. Descendant census, then rows W5-S5 and W5-S6.
8. Portal commit `0ebc6b20` (12 files, named individually).
9. The rows got their own workspace commit, `ae2d191d35` (45 insertions, 0 deletions; the surprise-row-gate
   graded the 2 new rows OK). The proof pins that commit.
10. The first proof check read INVALID on two violations: the rows were pinned PENDING-THIS-COMMIT while
    already committed, and F41-AC7's recorded invocation carried an `export IRPT_FE_DEV_PORT` prefix that
    the criterion text does not. Both were corrected: the rows are pinned to `ae2d191d35`, and the invocation
    is recorded as written, with the port export evidenced in the output lines.
11. This file and the proof instance go in one workspace commit. **No `complete` flip.**
