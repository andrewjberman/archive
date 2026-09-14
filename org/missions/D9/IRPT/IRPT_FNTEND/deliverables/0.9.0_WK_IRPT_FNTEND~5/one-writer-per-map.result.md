# IRPT_FNTEND.TO-FE-s-41 -- one writer per fixture map, and the narrative bound to its own revision

**Worker:** `0.9.0_WK_IRPT_FNTEND~5` | **Branch:** `wk-irpt_fntend-6-5-fe-s-41` (workspace and portal) |
**Portal commits:** `0ebc6b20` (first run) and `05bfc442` (Amendment 1), both LOCAL; portal is FROZEN |
**Base:** first run workspace `1f5d387e17`, portal `741bb54b`. Amendment run workspace `069344053b`, portal
`75b26bc8`, which is `0ebc6b20` plus the FE-s-38 sync from DEV `f55538e7`. |
**Order status:** `complete`. F41-AC1 to AC7 PASS by output on the amendment run. The whole suite reads
537 pass, 14 skip, 0 fail of 551 tests. F41-AC8 is recorded for L9.

## 1. The one writer, and why (W2-S24)

`fixtures/smoke/fe-s-14-global.json` has ONE writer: **`__tests__/fe-s-14/gen-maps.ts`**.

- gen-maps.ts builds the whole map. It composes FE-s-33's two Holdings envelopes into it by calling
  `globalHoldingsEnvelopes(resolveEnvelope, observedHoldings)`.
- `__tests__/fe-s-33/gen-global-holdings.ts` is a pure module. It exports that function and `HOLDINGS_KEY`,
  and it writes nothing and reads nothing.
- gen-maps.ts reads the observed Holdings envelope from `fe-s-18-holdings-observed.json`, which is
  gen-fixtures.ts' committed output. It refuses to write if that envelope is absent.
- Run order, stated in all three generator headers: `fe-s-18/gen-fixtures.ts`, then `fe-s-14/gen-maps.ts`.

**Why gen-maps.ts:**
- The map is FE-s-14's, and gen-maps.ts builds every other key in it.
- gen-maps.ts already wrote the file whole.
- It is the command a reader regenerating "the FE-s-14 maps" runs, so the writer that must be run is the one
  that gets run.
- The other direction would have made gen-global-holdings.ts rebuild FE-s-14's resolve and performance keys:
  duplicated logic, or an import of a module that writes as a side effect.

**Byte-identical regeneration.** On the amendment run, F41-AC4 regenerated the map into a fresh scratch
directory:
- the Global map: 17787 bytes, sha256 `aba71a86...b456a`, the same as the committed map;
- the writer's other three maps: 3 of 3 byte-equal.

## 2. The narrative re-bound (W2-S27)

- The frozen map took its non-performance keys from `fe-s-13-wire.json`, whose narrative names `perf-9`.
- Its performance body is `fe-s-16-print-narrative.json`'s. That fixture's own narrative names
  `rev-49f-000091`, the frozen report's revision.
- `gen-fixtures.ts` sets `frozen[NARRATIVE_KEY] = frozenNarrative()`, which copies that narrative whole. It
  throws if the narrative names any other revision.

F41-AC5 reads the binding on the wire and through the shipped parser. On the amendment run, **5 of 5 maps are
bound to rev-49f-000091**:
- the frozen map;
- the three Holdings bases;
- FE-s-32's no-answer map.

Each map's narrative is identical to the frozen map's. Controls:
- in memory, perf-9 put back: 0 of 5 bound;
- the frozen map at `741bb54b`: `narrative names=perf-9 bound=NO`.

## 3. Amendment 1: the fifth map is generated (row W5-S5)

The first run's F41-AC7 failed at `fe-s-32/holdings-in-a-browser.test.ts:256`. The cause was
`__tests__/fe-s-32/holdings-no-answer.json`, a hand copy of the observed map that still named perf-9.
Amendment 1 (`2.0.0_SA_COO~F`, @069344053b) granted that file for one purpose: gen-fixtures.ts generates it.

**What changed (portal `05bfc442`, 3 files, 108 insertions, 20 deletions):**
- `gen-fixtures.ts` writes a sixth map, `__tests__/fe-s-32/holdings-no-answer.json`:
  - it starts from the observed map it has just built, every member cloned;
  - one change only: the holdings envelope's `status` becomes `FE_S_32_NO_ANSWER_STATUS`, put in the same
    member position by the existing `withStatus`;
  - `write()` takes an optional base directory, so this map lands in FE-s-32's folder, where its test reads it.
- `FE_S_32_NO_ANSWER_STATUS` is FE-s-32's UNAVAILABLE status, carried verbatim from the map it committed at
  `7df6b4a2`. That is state `UNAVAILABLE`, reason `SOURCE_UNAVAILABLE`, and `source_dates` without a
  business_date. It is not re-derived.
- `fe-s-41/one-writer.test.ts`: F41-AC5 and its perf-9 control now also read the no-answer map.
- The generator prints `FIXTURE MAPS WRITTEN: 6 -- ... fe-s-32/holdings-no-answer.json (9 keys)`, rc=0.

**What the generated map is, measured against `git show HEAD` (`75b26bc8`) and against the observed map:**

| read | result |
|---|---|
| members, key order | 9 -> 9, same order |
| members differing from HEAD | the narrative only (perf-9 -> rev-49f-000091) |
| holdings envelope, status included, vs HEAD | equal (FE-s-32's status survives byte for byte) |
| members differing from the observed map | 1 of 9: holdings |
| holdings envelope vs observed, status removed | equal |
| narrative vs observed and frozen | identical |

The test at `:256` was not edited, and its assertion did not have to change. In the whole-suite run it prints
`NO-ANSWER MAP: 1 of 9 route members differ from the observed map (/api/scoped/investor-reporting/holdings/)`
and passes. FE-s-39 holds that test file.

## 4. What survives, byte for byte (the fields FE-s-26 and FE-s-33 own)

On the amendment run, gen-fixtures.ts regenerated its in-grant outputs **byte-equal to HEAD**:

| map | bytes | status (FE-s-26 / FE-s-32) | nodes (FE-s-33) | narrative, against `741bb54b` |
|---|---|---|---|---|
| fe-s-18-frozen.json | 14603 = HEAD | byte-equal | n/a | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-observed.json | 19202 = HEAD | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-target.json | 19392 = HEAD | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-missing-attribution.json | 18129 = HEAD | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-32/holdings-no-answer.json | 19140 (HEAD 18406) | byte-equal (FE-s-32's) | byte-equal | perf-9 -> rev-49f-000091, the only change |

The first run established, per member against `741bb54b`, that each fe-s-18 map changed in the narrative only.
The whole-suite run also re-grades these with the owning cells' own tests: F33-AC5 (FE-s-26's statuses),
F33-AC4 (the trees), F33-AC6 (the Global map) and FE-s-32's scenario maps (`SCENARIO MAPS CARRYING THEIR WIRE
STATE: 4 of 4`). All are green. The `'ADVISORY'` token is untouched.

## 5. The census (F41-AC2), and what it cannot see

**Denominator, amendment run.** `one-writer.test.ts` walks every file under `__tests__/`:
- 139 source files (.ts 132, .mjs 7): 27 generators and helpers, 96 test files, 16 declaration files;
- 16 non-source files, counted but not scanned;
- 18 of the 139 make a filesystem write call, at 46 call sites.

The FE-s-38 sync added files since the first run's 136.

**Result.** Exactly one site writes the Global map: `fe-s-14/gen-maps.ts:147`.

**Controls:**
- a seeded direct writer: 2 of 140;
- a seeded wrapper writer: 2 of 140;
- a seeded reader: 1 of 140;
- the real pre-FE-s-41 pair at `741bb54b`: 2 of 2, at `gen-maps.ts:94` and `gen-global-holdings.ts:146`.

**Blind spots of the census rule:**
- a name assembled from pieces with no literal;
- an imported path;
- a wrapper of a wrapper;
- a write inside a template literal's `${}`;
- any writer outside `__tests__/`.

**Unscoped reads for the last blind spot:**
- `comp-find 'fe-s-14-global' portal --files --all` at the base: 14 hits across 1353 files, no writer outside
  `__tests__/`.
- `comp-find 'holdings-no-answer' portal --files --all` at `05bfc442`: 13 hits across 1363 files, with
  1 unreadable and 91 binary files not searched. It names 4 files:
  - the map itself;
  - `fe-s-18/gen-fixtures.ts`, its one writer;
  - `fe-s-32/holdings-in-a-browser.test.ts`, a reader;
  - `fe-s-41/one-writer.test.ts`, a reader.
- The AC2 census rule itself is run on the Global map only.

## 6. Outside the grant, left as found

- **Five modified, unstaged files in the portal worktree (row W5-S6).** The ordered generators rewrite them.
  After the amendment run, each was measured byte-equal to `git show HEAD`, with `git diff --quiet` rc=0 on
  each. None was staged.
  - `src/pages/InvestorReporting/fixtures/smoke/fe-s-14-49financial.json` (2967 B)
  - `src/pages/InvestorReporting/fixtures/smoke/fe-s-14-cottonwood.json` (2965 B)
  - `src/pages/InvestorReporting/fixtures/smoke/fe-s-14-global.json` (17787 B; in the grant, but unchanged,
    so there is nothing to commit)
  - `src/pages/InvestorReporting/fixtures/smoke/fe-s-14-inflection.json` (2967 B)
  - `src/pages/InvestorReporting/fixtures/smoke/fe-s-16-print-prehistory.json` (4007 B)
- **A stale comment:** `__tests__/fe-s-33/ambient-shims.d.ts:14-15` still says gen-global-holdings.ts writes the
  Global map.
- **No capture was taken.** No non-test source file was touched.

## 7. Session log

**First run** (base workspace `1f5d387e17`, portal `741bb54b`):
1. TREE-OK. Premises re-grounded.
2. Baseline suite: 523 pass, 13 skip, 0 fail of 536 tests.
3. Generators edited, and `fe-s-41/` written. Generators run. Portal commit `0ebc6b20`, 12 files.
4. AC1-AC6 passed. AC7 read 532 pass, 13 skip, 1 fail of 546 (`:256`).
5. Rows W5-S5 (BLOCKING, ARMED) and W5-S6 (INERT) filed at `ae2d191d35`.
6. Proof and result file committed at `92108d5bcc`. Order left pending.

**Amendment run** (base workspace `069344053b`, portal `75b26bc8`):
1. TREE-OK on `wk-irpt_fntend-6-5-fe-s-41`, in both repos. The five W5-S6 files were present, stat-dirty.
2. Premises re-grounded:
   - `:242-259` asserts one differing member;
   - the no-answer map was committed LF at `7df6b4a2` (checked out CRLF);
   - against the base observed map it differed in holdings only;
   - against the current observed map it differed in holdings and the narrative.
3. The plane re-read before any mint: v1 holds no W5 ids; v2 holds W5-S1 to W5-S6.
4. Edited `gen-fixtures.ts` (the sixth map) and `one-writer.test.ts` (AC5 reads 5 maps).
5. Ran `gen-fixtures.ts` (rc=0, 6 maps), then `gen-maps.ts` (rc=0, 4 maps).
6. Byte and member comparison against HEAD (s.3, s.4, s.6).
7. Port 5265 was measured closed before every test run: ConnectionRefusedError after 2.02-2.06 s, on
   127.0.0.1 and on ::1. `IRPT_FE_DEV_PORT=5265` was exported.
8. The criteria:
   - AC1: rc=0.
   - AC2-AC5: 10 pass, 0 fail. A second run matched it on 41 of 41 lines.
   - AC6: `PAIRED: 1 report, 3 views`.
   - AC7: 537 pass, 14 skip, 0 fail of 551 tests in 96 files, rc=0. The `(fail)` census over the output
     reads 0.
9. Portal commit `05bfc442`: 3 files, named individually.
10. No new row: the amendment granted everything this run needed.
11. This file, the proof instance and the `complete` flip were committed together in one workspace commit.
