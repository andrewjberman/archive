# IRPT_FNTEND.TO-FE-s-1 -- result (cell FE-s-1)

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` | **Issued by:** `2.0.0_SA_COO~F` | **Date:** 2026-09-10
**Workspace worktree:** `/c/tmp/wk-irpt_fntend-1-1-fe-s-1`, branch `wk-irpt_fntend-1-1-fe-s-1`
**Portal worktree:** `/c/tmp/wk-irpt_fntend-1-1-fe-s-1/portal` (SEPARATE repo), branch `wk-irpt_fntend-1-1-fe-s-1`

## COMMITS -- both LOCAL, neither pushed

| repo | commit | branch | push state | contents |
|---|---|---|---|---|
| portal | `0322a04a4d144db9bf3211eca5c1bcd05f8099b9` | `wk-irpt_fntend-1-1-fe-s-1` | **LOCAL** (the order forbids push/merge; no `ls-remote` run and none claimed) | 43 files, +7536: contracts (2), client (1), fixtures (31 json + manifest + smoke map), tests (5) + 2 type-only d.ts |
| workspace | this commit | `wk-irpt_fntend-1-1-fe-s-1` | **LOCAL** | proof-of-spec instance, this result file, `surprise-channel/investigations/INVESTIGATION_v1.md`, the TO `<status>` flip |

Portal parent at spawn: `5907cbca98eb091124e38a32debefa355c1d4376`. Workspace parent: `3ceb5201cba09bb4912dfa59772c644cebaa3bf7`.

## CRITERIA -- 6 of 6 PASS by output

### F1-AC1 -- the portal typechecks with the new module and types

**Invocation:** `cd /c/tmp/wk-irpt_fntend-1-1-fe-s-1/portal && timeout 120 /c/Users/AndrewBerman/.bun/bin/bun run typecheck; echo rc=$?`

```
$ tsc -b --noEmit
rc=0
```

**rc:** 0 (expected `rc=0`). **Denominator:** 1 of 1 typecheck project (`tsconfig.app.json`, `include: ["src"]`), 0 diagnostics of 0. All 43 files added by this order live under `portal/src/`, so the program covers every one.

**Second instrument, because `tsc -b` is build-info-backed and a cached green is not a state read:**
`cd .../portal && timeout 240 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json; echo control-rc=$?` -> `control-rc=0`, no diagnostics. Different mode (non-incremental, no `tsBuildInfoFile`), same verdict.

**Discrimination:** the identical invocation on the identical tree BEFORE the two type-only shims were added did NOT pass -- 7 diagnostics: `TS2307` on `node:fs` at `fixtures.test.ts(11,43)` and `source-bounds.test.ts(15,30)`, `TS2307` on `node:url` at `fixtures.test.ts(12,31)` and `source-bounds.test.ts(16,31)`, and `TS7006` at `fixtures.test.ts(30,14)`, `(31,11)` and `source-bounds.test.ts(36,52)`. This green is not one the instrument prints regardless.

### F1-AC2 -- the key builder

**Invocation:** `cd .../portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-1/keys.test.ts`

```
KEYS: 11 of 11 operations namespaced
MISSING-SEGMENT REFUSALS: 12 of 12
NAME-SHAPED SEGMENTS REFUSED: 5 of 5

 10 pass
 0 fail
 137 expect() calls
```

**rc:** 0 (expected `0 fail`). **Denominator:** 10 tests of 10, 0 fail, 137 expect() calls. Per clause: namespace + tenant + fingerprint + revision **11 of 11 operations**; missing-segment refusals **12 of 12** (4 positions x 3 empty forms `''`/`undefined`/`null`, the positions enumerated by SUBTRACTION from the four the signature names rather than by recall); name-shaped segments refused **5 of 5**, plus 2 further refusals with a name pushed into a fixed position; and one test asserting the guard still ADMITS the tokens a real key needs -- a refusal rule that refused everything would pass the negative arm alone.

### F1-AC3 -- 31 fixtures, each parsing as its contract

**Invocation:** `cd .../portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-1/fixtures.test.ts`

```
FIXTURES: 31 of 31
FIXTURES PARSED AS THEIR CONTRACT: 31 of 31
FAILURE FIXTURES CARRYING A FAILING STATE: 10 of 10
SMOKE ROUTES: 11 of 11

 9 pass
 0 fail
 56 expect() calls
```

**rc:** 0 (expected `0 fail`). **Denominator:** 9 tests of 9, 0 fail. The 31 is read **from disk** (`readdirSync`, `.json` at depth 1) and cross-checked against the manifest in BOTH directions -- listed-but-absent `[]` and present-but-unlisted `[]`. A count taken from the manifest would certify the manifest against itself. Contract parse **31 of 31**; array fixtures validated per member. Failing-state arm **10 of 10** contracts (a failure fixture that is READY is a second success fixture). Smoke map **11 of 11** routes. The `.json`-at-depth-1 filter is disclosed as `IRPT_FNTEND-W1-S2`.

### F1-AC4 -- telemetry redaction

**Invocation:** `cd .../portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-1/redaction.test.ts`

```
SENTINELS ABSENT FROM TELEMETRY: 4 of 4

 9 pass
 0 fail
 52 expect() calls
```

**rc:** 0 (expected `0 fail`). **Denominator:** 9 tests of 9, 0 fail. **4 of 4** named leak vectors absent, each carried by a sentinel value that appears nowhere else in the repository -- so a record containing one could only have got it from the response -- plus 5 further stems (`zzsentinel`, `/var/task`, `Bearer`, `deadbeef`, `abc123`) asserted absent. **Positive arm:** the same record still carries operation, revision, publicReasonCode, httpStatus and outcome by value; a redactor that emitted nothing would pass the negative arm alone. **Mechanism:** the record is built by ALLOW-LIST from named inputs, not by copying a response and deleting fields -- one test hands `buildTelemetry` the entire hostile response and asserts the output still has exactly its nine keys.

### F1-AC5 -- parity, revocation, call log

**Invocation:** `cd .../portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-1/adapter.test.ts`

```
METHOD PARITY: 11 of 11
CALL LOG: 11 of 11
CACHE AFTER 403: 3 of 6 keys remain
CACHE AFTER ENVELOPE REVOCATION: 3 of 6 keys remain
LIVE ROUTES EXERCISED: 11 of 11

 15 pass
 0 fail
 95 expect() calls
```

**rc:** 0 (expected `0 fail`). **Denominator:** 15 tests of 15, 0 fail. Parity **11 of 11** at two grains -- a type-level annotation (which fails F1-AC1's typecheck if either implementation drifts) and a runtime method check whose denominator is `IR_OPERATIONS`, not a remembered list. Call log **11 of 11**, urls compared as an ORDERED list. Revocation: 6 seeded keys -> 3 remain; the **negative half is asserted separately** (2 of 2 keys for the OTHER fingerprint survive, plus 1 non-namespaced key), because a clearer that emptied the whole cache passes the positive half. Both revocation arms covered: a 403 status, and a 200 whose envelope names revocation. Live routes **11 of 11** through an injected transport.

### F1-AC6 -- source bounds

**Invocation:** `cd .../portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-1/source-bounds.test.ts`

```
SOURCE-BOUND CHECKS: 14 of 14 clean (2 files x 7 tokens)

 3 pass
 0 fail
 6 expect() calls
```

**rc:** 0 (expected `0 fail`). **Denominator:** 3 tests of 3, 0 fail. **14 of 14** = 2 files x 7 tokens (`document.cookie`, `Set-Cookie`, `orion`, `blackdiamond`, `ycharts`, `imap`, `mailbox`), matched case-insensitively. A **positive control** sits beside the absence verdict: the same read asserts a token that IS present (`investorreportingapi`) and that the file exceeds 1000 bytes, so a wrong-path or empty read cannot render as a clean green. A third test asserts the ACTS the tokens stand for -- `localstorage`, `sessionstorage`, `document.`, `window.location` -- are absent from both files.

## CONTROLS

**Mutant -- FIRED-AS-EXPECTED, three of three.** A passing assertion never mutated has never been tested, so each mutant targets a different criterion's load-bearing assertion.

| # | mutation | criterion | observed |
|---|---|---|---|
| 1 | moved `fixtures/directory.terminated-entitled.json` out of the directory | F1-AC3 | `FIXTURES: 30 of 31`, **6 pass / 3 fail** |
| 2 | appended `// mutant: reads document.cookie for the orion session` to the client module | F1-AC6 | `FORBIDDEN TOKEN HITS:` printed, `SOURCE-BOUND CHECKS: 12 of 14 clean`, **1 pass / 2 fail** |
| 3 | replaced the missing-segment `throw new IrKeyError(...)` in `assertSegment` with `return 'missing'` | F1-AC2 | **8 pass / 2 fail** |

All three restored from byte copies taken before mutation. After restoration: the refusal line is present at `investor-reporting.ts:101`, the fixture file is back on disk, all five test files re-run at rc=0, and the typecheck is rc=0.

**Determinism -- STABLE.** Each of the five test files run twice back-to-back on the unchanged tree; outputs diffed with the wall-clock duration line removed (a timing value, not a result). **5 of 5 IDENTICAL**. Every counted line is stable across runs. No test reads a clock it does not control -- the adapter's timestamp source is injectable and the fixed-timestamp assertion uses it.

## WHAT WAS BUILT, AND THE THREE THINGS IT REFUSES TO LET A SCREEN DO

- **Termination is not access.** `DirectoryEntry.termination` and `DirectoryEntry.access` are separate objects, and the validator REFUSES a payload where either carries the other's field. The `directory.terminated-entitled.json` negative is a terminated relationship that is still fully entitled.
- **Unknown is a value.** Every classification union carries an explicit `unknown`; the vendor supervised flag is `'yes' | 'no' | 'unknown'` because a boolean renders unknown as false. The validators refuse `false` and `'Client'` in a cohort or classification slot by name.
- **A percentage never travels without its denominator.** `HoldingsNode` carries `denominator` beside `pctOfParent` / `pctOfTotal`, and the validator flags a percentage whose denominator is null.

Additional: an unsupported metric is `{supported:false, value:null, unavailableReason:<code>}` and the validator refuses a numeric value beside `supported:false` -- that is the render-as-zero defect, blocked at the fixture gate.

## DECLARED LIMITS

- The `/api/scoped/investor-reporting/<op>` routes **do not exist** (IRPT_BCKEND B15 builds them). `LiveClient` is exercised against an INJECTED transport, which proves routing, verb, envelope extraction and error mapping -- **not** that any server answers. **NO LIVE VENDOR CALL was made** and none is claimed.
- `api-client.ts`, `portal-proxy.ts` and `market.ts` were imported or read for convention and are **unmodified**; the portal commit touches 43 files, none of them these.
- No screen, hook or React component is in this cell. No latency, TTL or retry value is an acceptance value anywhere in this deliverable.

## SURPRISES -- 2 rows, both in `surprise-channel/investigations/INVESTIGATION_v1.md`

- **`IRPT_FNTEND-W1-S1`** (OBSERVATION, **ARMED**, disarm owner `2.0.0_SA_COO~F`) -- F1-AC1 and F1-AC2..AC6 could not both pass without ambient type declarations the order does not name. `portal/tsconfig.app.json` sets `types: ["vite/client"]` and `include: ["src"]`, so neither `bun-types` (absent from `node_modules` entirely) nor `@types/node` (installed, excluded from the program) is loaded, and every test file failed `tsc` with TS2307. Resolved INSIDE the grant with two TYPE-ONLY shims in the granted test folder rather than by editing the ungranted tsconfig. ARMED because a later cell adding `@types/node` to the `types` array would collide `node-builtins.d.ts`'s `interface Dirent` against `@types/node`'s `class Dirent` in the same ambient module -- a green typecheck breaking on an edit nobody would connect to this folder.
- **`IRPT_FNTEND-W1-S2`** (OBSERVATION, INERT) -- "lists `fixtures/` and asserts 31 files" cannot be a literal listing: the same order places `fixtures/index.ts` and `fixtures/smoke/default.json` in that directory, so a literal listing returns 33 and the 31 is only reachable under a stated filter.

## PROOF OF SPEC

`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~1/IRPT_FNTEND.TO-FE-s-1.contracts-client-adapter-fixtures.proof_of_spec.json`

```
python .tools/proof-of-spec-check.py <instance> F1-AC1,F1-AC2,F1-AC3,F1-AC4,F1-AC5,F1-AC6
proof-of-spec-check | structural=jsonschema | acceptance rows=6 | violations=0
  alignment-forward-1 (criterion -> cell): 6/6 criteria carry >=1 cell_ref
  alignment-forward-2 (cell_ref -> decomp): 1/1 distinct cell_ref(s) resolve to an id declared in the decomp
  alignment-backward (declared cell -> criterion): 1/1 cell(s) declared in the TO's <owned_cells> are reachable from >=1 criterion
  surprises-frame: 2 entries; 2 open with a row id; 2 resolve to a channel row; mode ENFORCE
VALID (rc=0)
```

**rc=0 AND every mechanical criterion PASS-by-output**, so the task order's `<status>` flips to `complete` in the same commit as this file and the instance.
