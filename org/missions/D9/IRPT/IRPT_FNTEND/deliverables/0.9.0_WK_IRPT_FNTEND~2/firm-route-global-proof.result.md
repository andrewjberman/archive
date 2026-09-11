# IRPT_FNTEND.TO-FE-s-14 -- result

**Worker:** `0.9.0_WK_IRPT_FNTEND~2` · **Cell:** `FE-s-14` (round 2, decomp v0.2 @430c5fcb4a)
**Branch (both repos):** `wk-irpt_fntend-2-4-fe-s-14` · **push state:** LOCAL (never pushed; no `ls-remote` claim is made)
**Workspace worktree:** `/c/tmp/wk-irpt_fntend-2-4-fe-s-14` (HEAD at seating `ffa98ac525`; order AMENDED by the issuer at `25862ece09` -- R1 item 7)
**Portal worktree:** `/c/tmp/wk-irpt_fntend-2-4-fe-s-14/portal` (base `8cc43736`)

## VERDICT

**16 mechanical criteria PASS by output; `F14-AC11` is RECORDED (judgment, graded at L9).**
**`<status>` flipped to `complete`.** The proof instance is VALID (`proof-of-spec-check` rc=0) and
every mechanical criterion passes by its own output -- both halves, not one.

### The one bar that first failed, and how it closed

As first reported, `F14-AC10` (`bun test src/pages/InvestorReporting` -> `0 fail`) read
**381 pass, 1 skip, 1 fail**. The failure was `__tests__/fe-s-1/fixtures.test.ts:116`, asserting
that `fixtures/smoke/default.json`'s key set EQUALS the eleven round-1 flat consumer slugs -- while
R1 item 5 of this same order re-bases that file to the eleven DECLARED v1 paths and `F14-AC16`
grades the re-base. The two key sets cannot both hold (`IR_OPERATIONS` carries the two operations v1
serves with **no** route and omits `holdings-snapshot`, which v1 declares), and `__tests__/fe-s-1/`
was not in the original `<paths>`. This worker refused to flip on a VALID instance with a failing
bar and filed **BLOCKING row `IRPT_FNTEND-W2-S10`**.

The ISSUER AMENDED the order on that row (workspace `25862ece09`, **R1 item 7**): `__tests__/fe-s-1/`
is granted for exactly that ONE assertion, which now reads the eleven DECLARED v1 paths from
`docs/contracts/investor-reporting/v1/routes.json` -- the same set `F14-AC16` grades -- comparing per
route TEMPLATE, since the keys bind real path parameters no route table can predict. Three lines were
removed inside that single test (`git diff -U0` -> `@@ -119,3 +145,23 @@`); no other line of
`__tests__/fe-s-1/` changed, and the file's other eight tests pass untouched. `F14-AC10` now reads
**382 pass, 1 skip, 0 fail**; `F14-AC1` stays `rc=0`.

**The row is NOT closed by that amendment and was not edited.** Its second pin stands and is not this
worker's to touch: the counterpart's
`infra/aws/lambda/investor-reporting/_contracts/tests/test_seam_paired.py` still asserts the OLD
consumer form (`len(smoke) == 11`, the last-segment set, `consumer_path in smoke`) and will read RED
against a consumer file that is now MORE conformant, not less, once this branch reaches the primary
checkout. The issuer carries it to L10.

## THE BASE THIS ORDER WAS HANDED, AND WHAT IT READS NOW

| | ORDERED BASE `8cc43736` | this branch `e1d78ce6` |
|---|---|---|
| `bun run typecheck` | rc=2 (2 errors) | **rc=0** |
| `bun test src/pages/InvestorReporting` | 351 pass / 1 skip / **6 fail** (55 files) | 382 pass / 1 skip / **0 fail** (60 files) |

All six base failures are repaired. The seventh -- created by the ordered re-base of
`default.json`, rowed as `W2-S10` and closed under the amended grant -- is repaired too.

## CRITERIA

| id | status | deciding line |
|---|---|---|
| F14-AC1 | PASS | `rc=0` |
| F14-AC2 | PASS | `ALLOWED: 3 of 3` |
| F14-AC3 | PASS | `REFUSED: 2 of 2` + `FIRMACCESS DIFF: +3 -0` |
| F14-AC4 | PASS | `CLICKED: Holdings` (49financial) |
| F14-AC5 | PASS | `CLICKED: Holdings` (inflection) |
| F14-AC6 | PASS | `CLICKED: Holdings` (cottonwood) |
| F14-AC7 | PASS | `DID NOT LAND` (`LOC : /market`) |
| F14-AC8 | PASS | `GLOBAL PATH: absent` |
| F14-AC9 | PASS | `CLICKED: Holdings` (internal Global) |
| F14-AC10 | PASS | `0 fail` (382 pass / 1 skip / 0 fail across 60 files), after R1 item 7 |
| F14-AC11 | RECORDED | judgment; four PNGs described in the instance, no verdict |
| F14-AC12 | PASS | `ROUTES MATCHED: 11 of 11`, `CONSUMER-UNCALLED ROUTES: 3`, `NOT-YET-EXERCISABLE: 1` |
| F14-AC13 | PASS | `ENVELOPES PARSED: 11 of 11` |
| F14-AC14 | PASS | `REFUSALS: 3 of 3` |
| F14-AC15 | PASS | `HEADER SENT: 12 of 12` |
| F14-AC16 | PASS | `PUBLISHED MAP: v1` |
| F14-AC17 | PASS | `13 pass / 0 fail`, `LATO OFF-ORIGIN: 0` |

## EVERY FILE CHANGED, BY ITEM

### R1 item 1 -- the shim (commit `7151f2c4`)
- `portal/src/pages/InvestorReporting/__tests__/fe-s-13/ambient-shims.d.ts` -- `node:crypto`'s
  `update` widened to `string | Uint8Array`; nothing else in the shim changed.

### R1 item 2 -- the v1 pin (commit `7151f2c4`)
- `__tests__/fe-s-13/gen-wire.ts` -- reads `docs/contracts/investor-reporting/v1/`: 11 document
  schemas AND the 11 response envelopes, the latter enumerated from `routes.json`'s own
  `response_schema` fields; resolves `$ref` into the sibling wire types so a response SLICE carries
  the producer's own property types.
- `contracts/wire/{AnalysisReport,AnalysisRequest,DirectoryEntry,ExportBundle,ExportReceipt,HoldingsSnapshot,NarrativePacket,PerformanceReport,RenderPackage,ResolvedScope,StatusEnvelope}.ts`
  -- regenerated; each now carries the optional `contract_version` const.
- `contracts/wire/responses.ts` -- NEW, generated: 11 envelope types plus `RESPONSE_SCHEMA_PINS`,
  `RESPONSE_OPERATIONS` and `RESPONSE_STATUS_REQUIRED` (read from each schema's own
  `x-response-contract.status_required`).
- `contracts/wire/index.ts` -- regenerated; re-exports the response types, states the v1 pin
  authority.
- `__tests__/fe-s-13/producer-fixtures.test.ts` -- schemas from v1, fixtures still from the
  producer package (v1 publishes none -- row W2-S9), both sources PRINTED; adds the response-pin
  freshness arm (`RESPONSE SCHEMA PINS FRESH: 11 of 11`).
- `__tests__/fe-s-13/routes.test.ts` -- reads the v1 carrier; asserts the table's operations ARE
  the contract's; prints the three consumer-uncalled routes and the one not-yet-exercisable.

### R1 item 3 -- operation ids (commit `7151f2c4`)
- `src/api/endpoints/investor-reporting.ts` -- `IrDeclaredOperation` and `IR_ROUTE_TABLE` renamed
  to the producer's ids; `IR_RETIRED_OPERATIONS` is v1's NOT-A-ROUTE pair (`submit-correction`,
  `export-preview`); `submitCorrection` refuses instead of POSTing a correction body to
  `/analysis`; the list-shaped read is refused under `IR_UNSERVED_LIST_OPERATION`; a
  `submitAnalysisRequest` method is added for the submission route.
- `__tests__/fe-s-13/no-route.test.ts` -- the NOT-A-ROUTE pair is read FROM `routes.json`; a new
  arm proves the list refusal names itself and not the submission.
- `__tests__/fe-s-13/gen-corpus.ts` -- v1 operation keys, the record slug IS the operation id.

### R1 item 4 -- the header and the envelope (commits `7151f2c4`, `9e7ea2f3`)
- `contracts/envelope.ts` -- NEW: the one parser. Version and operation checked, `firm_id` carried
  opaque, `status` required where the contract says so, refusal codes rendering UNAVAILABLE with
  the code and withholding `data`, every refusal naming the FIELD and never the value.
- `contracts/adapt.ts` -- three SLICE adapters (`adaptAnalysisSubmission`,
  `adaptAnalysisReportSlice`, `adaptExportDownload`) for the three slice responses.
- `src/api/endpoints/investor-reporting.ts` -- `irBuildRequest` emits `X-Contract-Version: v1`;
  `IrTransport` carries headers; `LiveClient.send` parses the envelope, counts pre-envelope bodies
  (`preEnvelopeResponses`, row W2-S11) and takes the ack from `status` for `submit-export`
  (row W2-S12).
- `fixtures/wire/requests/*.request.json` -- 11 records, renamed to the operation ids, each with a
  `headers` object taken from the client's own builder.
- `__tests__/fe-s-14/{envelope,header}.test.ts` -- NEW (F14-AC13/14/15).

### R1 item 5 -- the published map and the print route (commits `7151f2c4`, `9e7ea2f3`)
- `fixtures/smoke/default.json` -- re-based to v1 (11 DECLARED-path keys, envelope bodies, the two
  NOT-A-ROUTE keys gone). **This is the change behind the F14-AC10 failure** -- row W2-S10.
- `fixtures/smoke/fe-s-13-wire.json` -- re-based the same way.
- `fixtures/smoke/fe-s-14-print-v1.json` -- NEW: the print route's two v1 needs.
- `__tests__/fe-s-17/fonts-served.test.ts` -- reads the netlog BESIDE it, and states which plane
  the committed capture was taken on.
- `__tests__/fe-s-17/fixtures/fe-s-17.netlog` -- NEW, committed: 146 rows, 3 of 3 Lato faces 200
  from the dev origin.
- `render/PrintEntry.tsx` -- composes the bundle on `NoDeclaredRoute`, the pattern
  `export/Preview.tsx` already used; `export/resolveBundle.ts` -- `composeExportBundle` names the
  `schemaVersion` of the shape it composes, without which the render package's version gate refused
  every composed bundle (row W2-S13).
- `__tests__/fe-s-14/published-map.test.ts` -- NEW (F14-AC16).

### R1 item 7 -- the one round-1 assertion (commit `9e68a9aa`, the issuer's amendment)
- `portal/src/pages/InvestorReporting/__tests__/fe-s-1/fixtures.test.ts` -- the assertion pinning
  `default.json`'s keys reads the eleven DECLARED v1 paths from the contract's own `routes.json`
  (bidirectional: each route owns exactly one key, each key resolves to exactly one route), with the
  retired form's count still printed beside it as a recorded number. One hunk, three lines removed,
  nothing else under `fe-s-1/` touched.

### R1 item 6 + THE CELL (commit `e1d78ce6`)
- `src/lib/firmAccess.ts` -- three added lines, nothing else (`+3 -0` against `edab15b5`).
- `__tests__/fe-s-14/{allowlist,one-firm}.test.ts`, `__tests__/fe-s-14/gen-maps.ts`,
  `__tests__/fe-s-14/ambient-shims.d.ts` -- NEW.
- `fixtures/smoke/fe-s-14-{49financial,inflection,cottonwood,global}.json` -- NEW, v1 envelopes.

## ROWS FILED

`IRPT_FNTEND-W2-S9` (OBSERVATION/INERT) · `-S10` (**BLOCKING/ARMED**, disarm_owner `2.0.0_SA_COO~F`) ·
`-S11` (OBSERVATION/ARMED, disarm_owner `2.0.0_SA_COO~F`) · `-S12` (OBSERVATION/INERT) ·
`-S13` (OBSERVATION/INERT) · `-S14` (OBSERVATION/INERT).

## WHAT THE ISSUER MUST DECIDE (not decided here)

1. **The counterpart half of W2-S10, still open.** The portal pin is closed by R1 item 7. The
   producer's `_contracts/tests/test_seam_paired.py` still asserts the old consumer form and will
   read RED on the drain; it is the counterpart's file, named in the row and carried to L10.
2. **The pre-envelope carry (W2-S11).** One line closes it, plus one out-of-grant test edit.
3. **`submitExport`'s narrowing (W2-S12)** -- interface change or an FE-s-16 read.
4. **v1 fixtures (W2-S9)** -- publish them, or name the producer package as the fixture source.

Dev server on `127.0.0.1:5182` was killed before this report.
