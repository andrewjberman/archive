# FE-s-13 -- THE SEAM: wire types, the routes.json operation table, the adapters

Worker `0.9.0_WK_IRPT_FNTEND~1`, task order `IRPT_FNTEND.TO-FE-s-13`, round 2.
Workspace worktree `/c/tmp/wk-irpt_fntend-2-2-fe-s-13` (branch
`wk-irpt_fntend-2-2-fe-s-13`, base `6ecffd5b15`); portal worktree
`/c/tmp/wk-irpt_fntend-2-2-fe-s-13/portal` (same branch name in the portal repo,
base `32a744dc`). Push state: **LOCAL** on both, in both repos.

All ten criteria PASS by their own output. Two surprise rows filed:
`IRPT_FNTEND-W1-S16` and `IRPT_FNTEND-W1-S17`.

---

## 1. What was built

**`contracts/wire/`** -- eleven GENERATED TypeScript files, one per producer
schema at `infra/aws/lambda/investor-reporting/_contracts/` @33351469c2, plus
`index.ts` (re-exports + `WIRE_SCHEMA_PINS`, schema name -> sha256 of the schema
FILE). Generator: `__tests__/fe-s-13/gen-wire.ts`, run by hand
(`bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts` from the
portal root); the output is committed and **no test runs the generator** -- a
test that regenerated its own input would certify the generator against itself.
Every generated header carries its source path and sha256, so a re-run on a
changed schema is a diff in review. `producer-fixtures.test.ts` re-digests the
eleven schemas and compares against the pins (`WIRE SCHEMA PINS FRESH: 11 of 11`).

**The operation table.** `IR_ROUTE_TABLE` in
`src/api/endpoints/investor-reporting.ts` is `routes.json` @bef9b459f3: twelve
rows, `${method} ${pathTemplate}` IS each row's `route_key`.

| operation | route_key | binding | status |
|---|---|---|---|
| `directory.search` | `GET /api/scoped/investor-reporting/directory/search` | query | DECLARED |
| `directory.resolve` | `POST /api/scoped/investor-reporting/directory/resolve` | body | DECLARED |
| `performance` | `GET /api/scoped/investor-reporting/performance/{accountSetId}` | query | DECLARED |
| `analysis.submit` | `POST /api/scoped/investor-reporting/analysis` | body | DECLARED |
| `analysis.sections` | `GET /api/scoped/investor-reporting/analysis/{jobId}/sections` | query | DECLARED |
| `narrative` | `GET /api/scoped/investor-reporting/narrative/{reportId}` | query | DECLARED |
| `status.probe` | `GET /api/scoped/investor-reporting/status` | query | DECLARED |
| `status.job` | `GET /api/scoped/investor-reporting/status/{jobId}` | query | DECLARED |
| `export.submit` | `POST /api/scoped/investor-reporting/export` | body | DECLARED |
| `export.receipt` | `GET /api/scoped/investor-reporting/export/{exportId}` | query | DECLARED |
| `export.download` | `GET /api/scoped/investor-reporting/export/{exportId}/download` | query | DECLARED |
| `holdings` | `GET /api/scoped/investor-reporting/holdings/{accountSetId}` | query | **NO-HANDLER-AT-HEAD** |

`irBuildRequest(op, args)` binds path parameters, puts a GET's values in the
query string and a POST's in a JSON body, and **refuses to build** a route whose
path parameter is missing. `LiveClient.send` builds exactly that method and path,
then runs the payload through `contracts/adapt.ts`. Typed refusals:
`NoDeclaredRoute` (reason code `no-declared-route`) for the two retired
operations and `NotYetExercisable` (reason code `no-handler-at-head`) for
holdings -- both measured to issue **zero** requests, not a request that 5xxs.

`irKey`, `clearProtected`, `handleIrResponse`, the revocation rules and the
telemetry redaction are untouched, as ordered.

**`contracts/adapt.ts`** -- ten wire->view adapters and two view->wire request
shapes (`toAnalysisGenerateWire`, the seven-key Generate body; and
`toExportBundleWire`). `FixtureAdapter` detects a PRODUCER fixture (the
`_fixture` + `instance` pair) and serves it through the same adapters, so there
is one code path from wire to view.

**Fixtures.** `fixtures/wire/` holds the eleven producer `.valid.json` copied
byte-for-byte; `fixtures/wire/requests/` holds eleven request records, one per
DECLARED route, with the producer fixtures' own ids bound and the paths built by
the client's own `irBuildRequest` -- **this is the file the counterpart
replays**; `fixtures/smoke/fe-s-13-wire.json` serves the page's needs at the
declared paths in wire shape.

---

## 2. FIELD_MAP -- 150 view fields, per type

The denominator is read by REFLECTION over the objects the adapters actually
produce from the producer fixtures, never from the map. Checked in both
directions: a produced key that the map does not name FAILS, and a name in the
map that no adapter produces FAILS.

| view type | fields | view type | fields |
|---|---|---|---|
| StatusEnvelope | 11 | AnalysisReport | 15 |
| DirectoryEntry | 18 | HoldingsSnapshot | 12 |
| ResolvedScope | 16 | NarrativePacket | 15 |
| PerformanceReport | 14 | ExportBundle | 14 |
| AnalysisRequest | 22 | ExportReceipt | 13 |

**150 of 150 mapped. DERIVED FIELDS: 0** over 150 rows, whose `kind` vocabulary
is exactly `CARRIED-AS-IS`, `RENAME`, `RESTRUCTURE`. There is no derived member
to spend, which is the point: a view field that could only be computed is not
computed -- it takes that field's own explicit unknown and is marked
`WIRE_ABSENT` in the map with the reason.

The explicit-unknown rule, stated once in `adapt.ts` and applied everywhere:
nullable -> `null`; a union with an `unknown` member -> `'unknown'` (or
`'UNCERTAIN'` for an envelope state); a non-nullable string ->
`EXPLICIT_UNKNOWN_TEXT`; a list -> `[]`; a boolean whose `false` is the
NON-ASSERTING value (`authoritative`, `validated`, `entitled`) -> `false`.
Never arithmetic, never a read of a neighbouring field.

---

## 3. Consumer files changed -- five, each named

| file | change |
|---|---|
| `tabs/analysis/RequestList.tsx` | additive OPTIONAL `envelope` prop; an UNAVAILABLE envelope renders the state + its public reason code instead of the row list |
| `tabs/analysis/AnalysisTab.tsx` | catches the typed `NoDeclaredRoute` and hands RequestList that envelope (`no-declared-route`). The ONLY view that renders it |
| `export/resolveBundle.ts` | `composeExportBundle` -- the client-side composition that replaces the absent preview route |
| `export/Preview.tsx` | `runPreview` falls back to that composition on `NoDeclaredRoute`, and only on it |
| `export/submit.ts` | `buildSubmitRequest` takes an OPTIONAL sixth argument, the composed bundle, carried as the producer-shaped `wireBundle` that IS the body of `POST .../export` |

Plus `__tests__/fe-s-1/adapter.test.ts` (in grant): the round-1 negatives are
unchanged; three LiveClient arms move onto the route table.

**No view TYPE changed.** The order allows dropping a view field the wire does
not carry OR filling it with the explicit unknown; filling was chosen for every
one, because the view types are read by ~9,000 lines under
`pages/InvestorReporting/` and by five test folders outside this grant -- and
`fe-s-3/source-bounds.test.ts` asserts as its POSITIVE CONTROL that eleven named
return-bearing field names are still present in `contracts/index.ts`. Every fill
is named in FIELD_MAP, so nothing is hidden by the choice.

---

## 4. The two rows

**`IRPT_FNTEND-W1-S16`** -- the face orders the two no-route operations RETIRED
from `InvestorReportingApi` (`previewExportBundle` removed) and says only
`__tests__/fe-s-1/` needs updating. Measured: SEVEN test files in FIVE folders
outside the grant bind those members and the round-1 path literals (fe-s-2,
fe-s-3, fe-s-6, fe-s-9 x2, fe-s-10). Retiring them as written makes F13-AC1 and
F13-AC10 unreachable without writing outside the grant. What was built instead:
the LIVE plane speaks only the route table and refuses both by name; the two
members remain as RETIRED members that only the FIXTURE plane answers, and the
round-1 slug vocabulary is kept as the FixtureAdapter's own fixture-plane
vocabulary. **The cost, stated:** an assertion on the FixtureAdapter's call-log
URL no longer proves anything about the live path -- the declared-path claim
lives on F13-AC2 (the table against routes.json) and F13-AC9 (the browser run).

**`IRPT_FNTEND-W1-S17`** -- five places where the producer's contract and the
view type do not map 1:1, each carried as an explicit unknown rather than
guessed: `access.entitled`'s UNKNOWN has no boolean to live in; the capability
vocabularies differ in both directions; two wire analysis stages collapse onto
one view stage; `protected_pdf_ref` carries a SERVER-ONLY storage key where the
view requires an authorized route (so it adapts to `null`); and
`optional_facts.benchmark` is an unstructured object the view's `BenchmarkFact`
cannot be built from. The row also records that no versioned contract artifact
(`docs/contracts/investor-reporting/v1/`) exists in this worktree, so the two RAW
pins are the authority. **For the counterpart, the protected-artifact one has a
product consequence**: an artifact the browser is meant to download has no
authorized route on the contract.

---

## 5. Acceptance -- every criterion, its deciding line

| id | deciding output | denominator |
|---|---|---|
| F13-AC1 | `rc=0` | whole-program `tsc -b --noEmit` over `src/`; positive control (planted TS2322) exits 2 |
| F13-AC2 | `ROUTES MATCHED: 11 of 11`, `NOT-YET-EXERCISABLE: 1` | 11 declared + 1 no-handler read from routes.json's own `_denominator`; both directions; 0 requests issued for holdings |
| F13-AC3 | `PRODUCER FIXTURES ADAPTED: 11 of 11` | 11 of 11 contracts; copies identical 11 of 11; pins fresh 11 of 11; adapters claimed 10 of 11 |
| F13-AC4 | `REQUEST CORPUS: 11 of 11` | 11 records vs 11 declared routes, both directions; analysis body 7 of 7 keys exactly |
| F13-AC5 | `RESOLVED-KEY LEAKS: 0` | 21 objects (11 records + 10 adapted), recursive key walk; 4 scanned keys printed; control returns the planted two |
| F13-AC6 | `DERIVED FIELDS: 0`, `FIELD MAP: 150 of 150` | 150 fields across 10 view types by reflection; control names a planted key as unmapped |
| F13-AC7 | `189 pass / 0 fail` | bun's path argument is a FILTER SUBSTRING: 18 files (fe-s-1's 7 + fe-s-10/11/13) -- a SUPERSET of the target, never a subset |
| F13-AC8 | `NO-DECLARED-ROUTE: 2` | 2 of 2 from the client's own `IR_RETIRED_OPERATIONS`; 0 of 12 routes serve either; render arm reads a FIXTURE envelope, and a fourth test ties that fixture to the code the live refusal raises |
| F13-AC9 | `CLICKED: Holdings`, rc=0 | 2 of 8 smoke keys matched -- the page's actual load path; the six dead keys are the two the live client REFUSES plus four with no caller on load |
| F13-AC10 | `344 pass, 1 skip, 0 fail` | 53 files, against a 322 / 48 base. +22 tests, +5 files; not one round-1 test lost |

Controls: the mutant arm fired on all three limbs (typecheck, leak walker,
field-map reflection); determinism STABLE across two full passes.

**Instrument caveat, disclosed:** F13-AC3's digests compare WORKING-TREE bytes on
both sides. Both repos run `core.autocrlf=true` and neither carries a `*.json`
eol rule, so both render identically on a fresh checkout -- but a future
`.gitattributes` rule on one side and not the other would break the comparison
without breaking the copy.

---

## 6. Commits (all LOCAL)

| repo | commit | subject |
|---|---|---|
| portal | `fb3339df` | FE-s-13(1/3): wire types, the routes.json operation table, and the adapters |
| portal | `d7b3d615` | FE-s-13(2/3): the producer fixtures, the request corpus, the wire smoke map and the fe-s-13 battery |
| portal | `3a8a3959` | FE-s-13(3/3): the consumers follow the map, and the round-1 negatives hold |
| workspace | this commit | the two rows, this result, the proof instance, the screenshot, the status flip |

The portal gitlink was never staged in the workspace repo.
