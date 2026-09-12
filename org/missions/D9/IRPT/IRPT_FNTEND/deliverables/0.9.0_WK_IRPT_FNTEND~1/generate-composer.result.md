# IRPT_FNTEND.TO-FE-s-15 -- the Generate composer: RESULT

**Worker** `0.9.0_WK_IRPT_FNTEND~1` | **issued by** `2.0.0_SA_COO~F` | **cell** `FE-s-15` (decomp v0.2 @430c5fcb4a) | **outcome_ref** FWD-4
**Worktree pair** `/c/tmp/wk-irpt_fntend-2-5-fe-s-15` (workspace, branch `wk-irpt_fntend-2-5-fe-s-15`, cut from CLOUD @7d6db9bcfa) and `/c/tmp/wk-irpt_fntend-2-5-fe-s-15/portal` (portal, same branch name, cut from DEV @84a86c10).
**Portal commit** `e5833214a6e46ff38ed0d2f7611fb515ff5fcc48` -- **LOCAL** (portal is frozen by Andrew-direct: no push, no merge).
**Dev server** started once on port 5181 for the two captures and killed before this report (`netstat` reads 0 listeners on 5181).

## THE HEADLINE

13 of 14 criteria PASS by output. **`F15-AC8` is REFUSED, with its measurement**: its second limb
(`a source grep of tabs/analysis/ for inputRevision returns 0 hits`) cannot be satisfied by any act inside
this order's write grant, because the symbols it names are imported by `__tests__/fe-s-6/correction.test.ts`
and `__tests__/fe-s-6/` is not in `<paths>`. Measured: **5 hits against a bar of 0**. The order stays OPEN
and its `<status>` is untouched (row `IRPT_FNTEND-W1-S18`; see also `W1-S23` -- the order reads `blocked`,
not the `pending` the spawn stated).

`F15-AC12` is RECORDED, not graded: it is the judgment criterion and the CVO grades it at L9 from the two PNGs.

## R2 -- THE RE-PIN, DONE FIRST

Vintage recorded as the order required: `git log -1 --format=%h -- docs/contracts/investor-reporting/v1` = **`d9c940244a`**
(IB-rt-7: `GET /api/scoped/investor-reporting/holdings/{accountSetId}` DECLARED with handler `irpt-holdings`;
`_denominator` = `declared 12, no_handler_at_head 0, total 12`).

| item | what was done | measured after |
|---|---|---|
| `WIRE_SCHEMA_PINS` | `gen-wire.ts` re-run | `WIRE SCHEMA PINS FRESH: 11 of 11` (HoldingsSnapshot `30eded0a58c9` -> `2665c5191941`) |
| response pins | same run; a 12th envelope generated | `RESPONSE SCHEMA PINS FRESH: 12 of 12` |
| `fixtures/wire/` copies | **no refresh needed** -- already byte-identical to the producer package | `FIXTURE COPIES IDENTICAL: 11 of 11` |
| `fixtures/wire/requests/` | `gen-corpus.ts` re-run; `holdings-snapshot.request.json` added | `REQUEST CORPUS: 12 of 12` |
| wire types | regenerated; only `HoldingsSnapshot.ts` changed body (+`attribution_holdouts`, `clocks`, two as-of fields) | `tsc -b --noEmit` rc=0 |
| live client | `holdings-snapshot` is DECLARED and ISSUED through the one `send`; `NotYetExercisable` retired for it | `ROUTES MATCHED: 12 of 12`, `NOT-YET-EXERCISABLE: 0`, `HOLDINGS REQUESTS ISSUED: 1 -- /api/scoped/investor-reporting/holdings/fp-8c41d0a7` |
| published map | `default.json` gained the holdings envelope | `KEYS: 12; DECLARED-PATH KEYS: 12; FLAT-SLUG KEYS: 0`; `DATA REQUIRED-SET SATISFIED: 12 of 12` |

Two things the re-pin touched that the order did not enumerate, both inside `<paths>` and both required for the
named result: `contracts/envelope.ts`'s `IR_DATA_ADAPTER` had no entry for `holdings-snapshot` (the one parser
refused the operation it could not answer for -- `EnvelopeMismatch on operation`), and `__tests__/fe-s-14/`'s
envelope/header assertions counted 11. The NO-HANDLER-AT-HEAD **status value and its refusal class are KEPT**
with an empty population this vintage, exercised directly by a positive control, because the contract keeps the
distinction on purpose (`routes.json` `_denominator.note`).

## THE COMPOSER

`tabs/analysis/composer.ts` (no React -- every rule is graded by `bun test`), rendered by
`tabs/analysis/GenerateComposer.tsx` in the S10 order, mounted ABOVE everything FE-s-6 built, which is unchanged.

1 client (the header's resolved selection, never re-entered) - 2 accounts (the permitted set, confirmable
checkboxes; "an account number is a display label") - 3 the held snapshot WITH its as-of and its immutable id,
plus the retained remainder when the producer carries one - 4 zero-to-five ORDERED opaque catalog keys, capped
and de-duplicated - 5 the optional title (derived for DISPLAY; the request sends `null`) - 6 prepared-for /
prepared-by / contacts - 7 the variant, resolved by count and DISPLAYED, `auto` unless picked - 8 the
idempotency key.

`RevisionIdentity.tsx` renders the seven identity fields the schema names, read through the FE-s-13 adapter:
`identity.{request_id,revision,ingestion_gate_revision,destination_policy_revision}`, `stage`,
`release.{policy_version,state}`. A correction is a FIELD of a NEW submission, so it does not move them --
measured as byte-identical markup (1618 bytes each).

Design decisions that are NOT free choices, each with its row:
- the body is built in `composer.ts` rather than through `toAnalysisGenerateWire`, whose `report_title: string`
  cannot carry the contract's `null`; the key set is asserted EQUAL to the adapter's own
  `ANALYSIS_GENERATE_KEYS`, so the two producers cannot drift (`W1-S20`);
- the comparison control takes the opaque key itself and the prepared-for block prefills nothing, because v1's
  wire scope carries neither a catalogue nor a profile; both absences are printed on the page (`W1-S19`);
- `preparing` vs `generating` splits on `request_ref.attempt_number` because v1's StatusEnvelope has no
  PREPARING member, and the job state is read from the WIRE status because `LiveClient.send` returns `data` and
  drops the envelope's `status` (`W1-S21`).

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| F15-AC1 | PASS | `rc=0` | whole portal, `tsc -b --noEmit` |
| F15-AC2 | PASS | `REQUEST KEYS: 7 of 7`; `SNAPSHOT: body smartx:sx-2026-09-09 \| held smartx:sx-2026-09-09`; `COMPARISON KEYS: opal_lt -> opal_st` | 7 of 7 keys |
| F15-AC3 | PASS | `RESOLVED-KEY LEAKS: 0` over `resolved, viewer_policy, verified_request_firm_id, vendor_ids` | 2 objects scanned; control finds 2 planted |
| F15-AC4 | PASS | `VARIANT BY COUNT: 4 of 4` | 4 counts (0,1,2,5) |
| F15-AC5 | PASS | `REFUSED: 2 of 2`; `SUBMITS REACHING THE CALL LOG: 0` | 2 refusal arms |
| F15-AC6 | PASS | `SENDS: 2; DISTINCT IDS: 1`; then `SENDS: 3; DISTINCT IDS: 2`; `REQUEST ID: stable-on-retry, new-on-change` | 6 of 6 inputs move the key |
| F15-AC7 | PASS | `JOB STATES: 5 of 5`; `DISTINCT LABELS: 5 of 5`; `WAF REFRESH -> needs-attention`; `INPUTS PRESERVED: deep-equal` | 5 fixtures; 9 of 9 wire states mapped |
| F15-AC8 | **FAIL** | limb 1 `REVISION IDENTITY: preserved`; limb 2 `INPUTREVISION HITS IN tabs/analysis/: 5` against a bar of 0 | 12 source files scanned |
| F15-AC9 | PASS | `CLICKED: Analysis`, rc=0 | 1 capture, 390 wide |
| F15-AC10 | PASS | `CLICKED: Analysis`, rc=0 | 1 capture, 390 wide |
| F15-AC11 | PASS | `398 pass, 1 skip, 0 fail` | 399 tests across 65 files |
| F15-AC12 | RECORDED | the two PNGs beside this file | judgment -- CVO at L9 |
| F15-AC13 | PASS | `ROUTES MATCHED: 12 of 12`; `NOT-YET-EXERCISABLE: 0` | 12 routes in the contract |
| F15-AC14 | PASS | `28 pass, 0 fail` | 28 tests across 5 files |

The baseline the order stated (376 pass / 1 skip / 6 fail on DEV @84a86c10) was reproduced in this worktree
before any edit, and the six failures were exactly the fe-s-13 (4) / fe-s-14 (1) / fe-s-1 (1) rows R2 addresses.

## WHAT WAS NOT DONE, AND WHY

- **W3-S2's removal half.** `parity.ts`'s local derivation and the `inputRevision` fallback stay. Removing
  either reds another cell's battery (`__tests__/fe-s-6/`: 4 assertions on `inputRevision`, 3 tests on parity)
  that this order may not edit. The identity half of W3-S2 IS done and measured. Row `W1-S18`.
- **The corpus's `snapshot_id`.** `gen-corpus.ts` binds it to the scope fingerprint while the composer sends the
  snapshot's own revision. Not changed: re-binding the seam artifact is not an act this order names. Row `W1-S22`.
- **No push, no merge, no rebase** in either repo.

## ROWS FILED

`IRPT_FNTEND-W1-S18` (BLOCKING, INERT) - `W1-S19` - `W1-S20` - `W1-S21` - `W1-S22` - `W1-S23` (all OBSERVATION,
INERT), in `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.
