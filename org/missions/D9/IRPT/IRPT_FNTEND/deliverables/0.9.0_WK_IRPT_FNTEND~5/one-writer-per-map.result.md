# IRPT_FNTEND.TO-FE-s-41 -- one writer per fixture map, and the narrative bound to its own revision

**Worker:** `0.9.0_WK_IRPT_FNTEND~5`

**Runs and commits.** Portal is FROZEN, and every commit below is LOCAL.

| run | branch (workspace and portal) | base | portal commit |
|---|---|---|---|
| first run | `wk-irpt_fntend-6-5-fe-s-41` | workspace `1f5d387e17`, portal `741bb54b` | `0ebc6b20` |
| Amendment 1 | `wk-irpt_fntend-6-5-fe-s-41` | workspace `069344053b`, portal `75b26bc8` | `05bfc442` |
| Amendment 2 | `wk-irpt_fntend-6-5b-fe-s-41`, a fresh pair | workspace `78b011df6a`, portal `87f83b86` (DEV with FE-s-38, 39, 40 and 41 drained) | `39be77ec` |

`0ebc6b20` and `05bfc442` are both ancestors of `87f83b86` (`merge-base --is-ancestor` rc=0, with a positive control).

**Order status:** `complete`. F41-AC1 to AC7 PASS by output on the Amendment 2 run, which was on a fresh CRLF
checkout with no generator run in place. The whole suite reads 549 pass, 16 skip, 0 fail of 565 tests. F41-AC8
is recorded for L9.

## 0. Amendment 2: F41-AC4 compares with the COMMITTED map (row S64)

**The defect.** F41-AC4 and its CONTROL compared the generator's output with `fe-s-14-global.json` as checked
out.
- The map is stored LF.
- This box runs `core.autocrlf=true` with no `.gitattributes`, so a fresh checkout renders the map CRLF.
- The first two runs passed only because `gen-maps.ts` had rewritten the map LF in that worktree.

**Before the fix, on this fresh worktree.** Nothing was touched first.

| read | value |
|---|---|
| `git ls-files --eol` (map) | `i/lf w/crlf attr/ src/pages/InvestorReporting/fixtures/smoke/fe-s-14-global.json` |
| `one-writer.test.ts` | **8 pass, 2 fail**: F41-AC4 and its CONTROL |
| AC4 verdict line | `REGENERATED MAP EQUALS THE COMMITTED MAP: no` |
| regenerated | 17787 bytes, sha256 `aba71a86...b456a` |
| "committed" (the checkout) | 18424 bytes, sha256 `6f0299a7...35b16`, 637 CR bytes more |
| writer's other maps | `REGENERATED EQUAL TO COMMITTED: 0 of 3` (also CRLF checkouts) |

**The fix** (portal `39be77ec`, `__tests__/fe-s-41/` only, 2 files, +105/-9).
- F41-AC4, its CONTROL and the writer's-other-maps line read the committed side with `git cat-file blob
  HEAD:<path>`.
- The bytes are raw and never decoded: `spawnSync` with `encoding: 'buffer'`.
- `ambient-shims.d.ts` gains that one overload, because the portal program has no `@types/node`.

**Committed blob, or a normalised checkout read? THE BLOB, and why:**
- **It is the object the criterion names.** "Compared byte for byte with the committed `fe-s-14-global.json`"
  means the stored object. `git cat-file blob` applies no checkout filter and no line-ending conversion, so the
  bytes compared are the bytes committed. The vintage is printed beside the verdict (`at portal HEAD
  39be77ec`).
- **A CR-stripped read of the checkout answers a different question.**
  - It would call a committed blob that genuinely carries CRLF equal to LF output.
  - It reads the WORKING COPY, so an uncommitted in-place edit would be graded as committed. That is the very
    state that masked S64 on the first two runs.
- **The cost.** The test needs `git` and a HEAD that contains the map. The HISTORY arms already needed `git`. A
  missing blob fails closed: `expect(blob.rc).toBe(0)`, with git's stderr printed.

**After the fix, same worktree, the map still `i/lf w/crlf`:**

```
  git ls-files --eol: i/lf w/crlf attr/ src/pages/InvestorReporting/fixtures/smoke/fe-s-14-global.json
  committed   = git cat-file blob HEAD:src/pages/InvestorReporting/fixtures/smoke/fe-s-14-global.json at portal HEAD 39be77ec -> rc=0
  regenerated 17787 bytes sha256 aba71a862457ff7587934c09d5668f938ea8bda069abc713015f008b840b456a CR bytes 0
  committed   17787 bytes sha256 aba71a862457ff7587934c09d5668f938ea8bda069abc713015f008b840b456a CR bytes 0
  checked out 18424 bytes sha256 6f0299a726d44fd1f3f4af5972c159b6cb138a20261f0eaa27eba0b133535b16 CR bytes 637 (not the compared object)
REGENERATED MAP EQUALS THE COMMITTED MAP: yes
  the same output against the map AS CHECKED OUT (the pre-amendment read): NOT equal
THE WRITER'S OTHER MAPS, REGENERATED EQUAL TO COMMITTED: 3 of 3
```

The shell's own `git ls-files --eol` read `i/lf w/crlf` before and after every run. The result: 10 pass, 0 fail.

**The comparison is not a constant.** Every arm below works in memory, and nothing is written to disk.

| arm | expected | read |
|---|---|---|
| the committed blob re-serialised whole | equal | `yes` |
| round-4 shape (Holdings removed, 3045 bytes) | not equal | `no` |
| **the regenerated map with ONE content byte changed** (offset 83, `'v' -> 'x'`, 17787 of 17787 bytes, so the byte loop decides, not the length) | not equal | `no` |
| **the committed map rendered CRLF** (18424 bytes, 637 CR), as this box checks it out | not equal | `no` |

The last arm shows the compare normalises nothing. A CR-only difference still reads not-equal, and the verdict
is `yes` only because the COMMITTED side is read.

**Two further edits, both in `fe-s-41/`:**
- AC3's evidence line said `COMMITTED MAP BYTES UNCHANGED BY THE SCRATCH RUN`, but it reads the checkout. It now
  says `THE MAP AS CHECKED OUT, BYTES UNCHANGED BY THE SCRATCH RUN`. No criterion's expect reads that line.
- The test header states the blob rule and why.

**Not done, by the amendment's bounds:**
- No generator was run in place.
- No map was rewritten.
- No `.gitattributes` was added.

**Left as found (row W5-S7, OBSERVATION, INERT).** F41-AC5 says "read from the committed frozen map", but it
reads the five maps as checked out. JSON.parse ignores line endings, so it cannot go red from a CRLF checkout.
It would, however, read an uncommitted in-place edit as if it were committed. Amendment 2 scopes the fix to AC4
and its CONTROL.

## 1. The one writer, and why (W2-S24)

`fixtures/smoke/fe-s-14-global.json` has ONE writer: **`__tests__/fe-s-14/gen-maps.ts`**.

- gen-maps.ts builds the whole map. It composes FE-s-33's two Holdings envelopes into it by calling
  `globalHoldingsEnvelopes(resolveEnvelope, observedHoldings)`.
- `__tests__/fe-s-33/gen-global-holdings.ts` is a pure module. It exports that function and `HOLDINGS_KEY`, and
  it writes nothing and reads nothing.
- gen-maps.ts reads the observed Holdings envelope from `fe-s-18-holdings-observed.json`, which is
  gen-fixtures.ts' committed output. It refuses to write if that envelope is absent.
- The run order is stated in all three generator headers: `fe-s-18/gen-fixtures.ts`, then `fe-s-14/gen-maps.ts`.

**Why gen-maps.ts:**
- The map is FE-s-14's, and gen-maps.ts builds every other key in it.
- It already wrote the file whole.
- It is the command a reader regenerating "the FE-s-14 maps" runs, so the writer that must be run is the one
  that gets run.
- The other direction would have made gen-global-holdings.ts rebuild FE-s-14's resolve and performance keys.
  That means duplicated logic, or an import of a module that writes as a side effect.

**Byte-identical regeneration, against the COMMITTED blobs (Amendment 2 run):**
- the Global map: 17787 of 17787 bytes equal, sha256 `aba71a86...b456a`;
- the writer's other three maps: 3 of 3 byte-equal.

## 2. The narrative re-bound (W2-S27)

- The frozen map took its non-performance keys from `fe-s-13-wire.json`, whose narrative names `perf-9`.
- Its performance body is `fe-s-16-print-narrative.json`'s. That fixture's own narrative names
  `rev-49f-000091`, the frozen report's revision.
- `gen-fixtures.ts` sets `frozen[NARRATIVE_KEY] = frozenNarrative()`, which copies that narrative whole. It
  throws if the narrative names any other revision.

F41-AC5 reads the binding on the wire and through the shipped parser. **5 of 5 maps are bound to
rev-49f-000091:**
- the frozen map;
- the three Holdings bases;
- FE-s-32's no-answer map.

Each map's narrative is identical to the frozen map's. Controls:
- in memory, perf-9 put back: 0 of 5 bound;
- the frozen map at `741bb54b`: `narrative names=perf-9 bound=NO`.

## 3. Amendment 1: the fifth map is generated (row W5-S5)

The first run's F41-AC7 failed at `fe-s-32/holdings-in-a-browser.test.ts:256`. The cause was
`__tests__/fe-s-32/holdings-no-answer.json`, a hand copy of the observed map that still named perf-9.
Amendment 1 (`2.0.0_SA_COO~F`, @069344053b) granted that file for one purpose.

At portal `05bfc442`, `gen-fixtures.ts` writes it from the observed map with one change only. The holdings
status becomes `FE_S_32_NO_ANSWER_STATUS`, carried verbatim from FE-s-32's map at `7df6b4a2`.

- The test at `:256` was not edited, and its assertion did not have to change.
- In the Amendment 2 whole suite it prints `NO-ANSWER MAP: 1 of 9 route members differ from the observed map
  (/api/scoped/investor-reporting/holdings/)` and passes.
- FE-s-39 holds that test file.

## 4. What survives, byte for byte (the fields FE-s-26 and FE-s-33 own)

The Amendment 1 run established each of these, against HEAD and against `741bb54b`:

| map | status (FE-s-26 / FE-s-32) | nodes (FE-s-33) | narrative, against `741bb54b` |
|---|---|---|---|
| fe-s-18-frozen.json | byte-equal | n/a | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-observed.json | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-target.json | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-18-holdings-missing-attribution.json | byte-equal | byte-equal | perf-9 -> rev-49f-000091 |
| fe-s-32/holdings-no-answer.json | byte-equal (FE-s-32's) | byte-equal | perf-9 -> rev-49f-000091, the only change |

Amendment 2 changed no map. The whole suite re-grades these with the owning cells' own tests, and all are green:
- F33-AC5 (FE-s-26's statuses);
- F33-AC4 (the trees);
- F33-AC6 (the Global map);
- FE-s-32's scenario maps (`SCENARIO MAPS CARRYING THEIR WIRE STATE: 4 of 4`).

The `'ADVISORY'` token is untouched.

## 5. The census (F41-AC2), and what it cannot see

**Denominator, Amendment 2 run.** `one-writer.test.ts` walks every file under `__tests__/`:
- 148 source files (.ts 136, .mjs 12): 32 generators and helpers, 100 test files, 16 declaration files;
- 16 non-source files, counted but not scanned;
- 22 of the 148 make a filesystem write call, at 54 call sites.

The first run scanned 136 files and Amendment 1 scanned 139. The FE-s-38, 39 and 40 drains added files since.

**Result.** Exactly one site writes the Global map: `fe-s-14/gen-maps.ts:147`.

**Controls:**
- a seeded direct writer: 2 of 149;
- a seeded wrapper writer: 2 of 149;
- a seeded reader: 1 of 149;
- the real pre-FE-s-41 pair at `741bb54b`: 2 of 2, at `gen-maps.ts:94` and `gen-global-holdings.ts:146`.

**Blind spots, stated in the test header:**
- a name assembled from pieces with no literal;
- an imported path;
- a wrapper of a wrapper;
- a write inside a template literal's `${}`;
- any writer outside `__tests__/`.

**Unscoped reads, Amendment 1 run:**
- `comp-find 'fe-s-14-global' portal --files --all`: no writer outside `__tests__/`.
- `comp-find 'holdings-no-answer' portal --files --all`: 13 hits across 1363 files, naming 4 files. They are
  the map itself, gen-fixtures.ts as its one writer, and two readers.

## 6. Outside the grant, left as found

- **This worktree is fresh (Amendment 2).** No generator was run in place. `git status` before and after the
  whole suite shows only the two `fe-s-41/` files modified, and no map. So the first run's five modified,
  unstaged files (row W5-S6) do not exist here.
- **Correction to the Amendment 1 record (row S64).** That run called those five files "byte-equal to HEAD,
  stat-dirty only". The generator had in fact rewritten CRLF checkouts as LF. The claim compared LF to LF, and
  that is the state which hid S64. It is recorded here and not rewritten above.
- **A stale comment.** `__tests__/fe-s-33/ambient-shims.d.ts:14-15` still says gen-global-holdings.ts writes the
  Global map.
- **F41-AC5 reads the working copy** (row W5-S7). See s.0.
- **No capture was taken.** No non-test source file was touched.

## 7. Session log

**First run and Amendment 1:**
- Base workspace `1f5d387e17` / `069344053b`.
- Portal commits `0ebc6b20` and `05bfc442`.
- Rows W5-S5 (BLOCKING, ARMED) and W5-S6 (INERT) at `ae2d191d35`.
- AC7 read 537 / 14 / 0 of 551 on the Amendment 1 run, in a worktree where the map had been rewritten LF (S64).

**Amendment 2** (fresh pair; workspace `78b011df6a`, portal `87f83b86`):
1. TREE-OK on `wk-irpt_fntend-6-5b-fe-s-41` in both repos. The portal was clean. Every smoke map, and
   `holdings-no-answer.json`, reads `i/lf w/crlf`. `core.autocrlf=true`; `.gitattributes` is absent.
2. The plane was re-read before any mint. v1 holds 41 ids with no W5; v2 holds 174, with W5-S1 to W5-S6, S63 and
   S64.
3. Port 5265 was measured closed before every `bun test` run: `ConnectionRefusedError` after 2.01-2.04 s, on
   127.0.0.1 and on ::1. `IRPT_FE_DEV_PORT=5265` was exported.
4. **RED first:** `one-writer.test.ts` 8 pass / 2 fail, `REGENERATED MAP EQUALS THE COMMITTED MAP: no`,
   `i/lf w/crlf`.
5. The fix, in `fe-s-41/one-writer.test.ts` and `fe-s-41/ambient-shims.d.ts`.
6. The criteria. Each `bun test` run had the port measured first and read `i/lf w/crlf` before and after.
   - AC1 `rc=0`.
   - AC2-AC5 10 pass / 0 fail, twice:
     - on the uncommitted tree;
     - at the committed HEAD `39be77ec`.
     The two runs agree on 49 of 49 lines, after normalising ANSI codes, timings, the mkdtemp suffix and the
     HEAD hash.
   - AC6 `PAIRED: 1 report, 3 views`.
   - AC7 549 pass / 16 skip / 0 fail of 565 tests across 100 files, rc=0. The output is 1564 lines, and its
     `(fail)` census reads 0.
7. Portal commit `39be77ec`: 2 files, named individually.
8. Row W5-S7 (OBSERVATION, INERT) committed at `1e9a07f037`. The diffstat is 22 insertions only.
9. Baselines: `to-pipeline-gate.py --self-test` 0 of 72 arms failed; `proof-of-spec-check.py --self-test` 42 of
   42.
10. This file, the proof instance and the `complete` flip go in one workspace commit.
