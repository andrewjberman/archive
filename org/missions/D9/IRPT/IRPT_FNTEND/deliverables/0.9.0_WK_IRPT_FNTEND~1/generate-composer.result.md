# IRPT_FNTEND.TO-FE-s-15 -- the Generate composer: RESULT

**Worker** `0.9.0_WK_IRPT_FNTEND~1` | **issued by** `2.0.0_SA_COO~F` | **cell** `FE-s-15` (decomp v0.2 @430c5fcb4a) | **outcome_ref** FWD-4
**Worktree pair** `/c/tmp/wk-irpt_fntend-2-5-fe-s-15` (workspace, branch `wk-irpt_fntend-2-5-fe-s-15`, cut from CLOUD @7d6db9bcfa) and `/c/tmp/wk-irpt_fntend-2-5-fe-s-15/portal` (portal, same branch name, cut from DEV @84a86c10).
**Portal commits** `e5833214a6` (the composer + the R2 re-pin) and `7305a6bfa9` (the W3-S2 retirement) -- both **LOCAL** (portal is frozen by Andrew-direct: no push, no merge).
**Dev server** started on port 5181 for the captures and killed before this report (`netstat` reads 0 listeners on 5181).

## THE HEADLINE

**14 of 14. Every mechanical criterion passes by output; `F15-AC12` is the judgment criterion and is RECORDED for the CVO at L9.** The task order's `<status>` is flipped to `complete` in the same commit as this file.

`F15-AC8` was REFUSED on the first pass, with its measurement: its second limb (`a source grep of tabs/analysis/ for inputRevision returns 0 hits`) could not be satisfied inside the original write grant, because removing the fallback reds four assertions in `__tests__/fe-s-6/correction.test.ts` and that folder was not in `<paths>`. Measured then: **5 hits against a bar of 0** (row `IRPT_FNTEND-W1-S18`). The issuer's amendment (`IRPT_FNTEND-S24`) widened `<paths>` for exactly that retirement; it is now done, **neither bar moved**, and both limbs pass: `REVISION IDENTITY: preserved` and `INPUTREVISION HITS IN tabs/analysis/: 0`.

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
| wire types | regenerated; only `HoldingsSnapshot.ts` changed body | `tsc -b --noEmit` rc=0 |
| live client | `holdings-snapshot` is DECLARED and ISSUED through the one `send`; `NotYetExercisable` retired for it | `ROUTES MATCHED: 12 of 12`, `NOT-YET-EXERCISABLE: 0`, `HOLDINGS REQUESTS ISSUED: 1 -- /api/scoped/investor-reporting/holdings/fp-8c41d0a7` |
| published map | `default.json` gained the holdings envelope | `KEYS: 12; DECLARED-PATH KEYS: 12`; `DATA REQUIRED-SET SATISFIED: 12 of 12` |

Two things the re-pin touched that the order did not enumerate, both inside `<paths>` and both required for the named result: `contracts/envelope.ts`'s `IR_DATA_ADAPTER` had no entry for `holdings-snapshot` (the one parser refused the operation it could not answer for), and `__tests__/fe-s-14/`'s envelope/header assertions counted 11. The NO-HANDLER-AT-HEAD **status value and its refusal class are KEPT** with an empty population this vintage, exercised directly by a positive control.

## THE COMPOSER

`tabs/analysis/composer.ts` (no React -- every rule is graded by `bun test`), rendered by `tabs/analysis/GenerateComposer.tsx` in the S10 order, mounted ABOVE everything FE-s-6 built.

1 client - 2 accounts (permitted set, confirmable) - 3 the held snapshot WITH its as-of, its immutable id and its retained remainder - 4 zero-to-five ORDERED opaque catalog keys - 5 the optional title (derived for DISPLAY; the request sends `null`) - 6 prepared-for / prepared-by / contacts - 7 the variant, resolved by count and DISPLAYED - 8 the idempotency key.

Design decisions that are NOT free choices, each with its row: the body is built in `composer.ts` because the granted adapter's `report_title: string` cannot carry the contract's `null` (`W1-S20`); the comparison control takes the opaque key itself and the prepared-for block prefills nothing, because v1's wire scope carries neither a catalogue nor a profile (`W1-S19`); `preparing` vs `generating` splits on `request_ref.attempt_number` because v1 has no PREPARING state, and the job state is read from the WIRE status because `LiveClient.send` drops the envelope's `status` (`W1-S21`).

## W3-S2 -- THE RETIREMENT (second pass, under the widened grant)

| retired | replaced by | where |
|---|---|---|
| `deriveInputRevision` (= `corrections.length + 1`) and the derived field on `CorrectionResult` | `requestRevision`, the wire's `identity.revision`, CARRIED and never incremented | `tabs/analysis/correction.ts` |
| `parity.ts` (DELETED) -- a per-section support fact no producer contract carries | `AnalysisReport.extraction_validation` (CERTIFIED / UNCERTIFIED / FAILED + check counts), stated once in its own slot and applied per section | `tabs/analysis/NativeSections.tsx` |
| the header sentence naming the counter | the wire sentence | `tabs/analysis/InputReview.tsx` |

`MODELED_KIND`, `isModeled` and `inOrdinalOrder` moved into `NativeSections.tsx` unchanged -- they read the wire's own `section_type` and `page` and were never part of the local derivation.

**The FE-s-6 assertions were CARRIED, never deleted.** `correction.test.ts`'s chain `1 -> 2 -> 3` on a derived counter is now `0 -> 1 -> 2` on the `corrections` array the contract carries, **with the wire revision asserted equal at every step** -- the half the old counter got wrong. `sections.test.ts`'s three per-section arms are now report-level arms over the same three sections: certified (all SUPPORTED), uncertified (all UNSUPPORTED with the producer's own code and unconfirmed count), and no verdict at all (UNSUPPORTED -- the safe default, preserved verbatim). The two things the WIRE genuinely no longer carries are rows, not deletions: **`W1-S24`** (v1 publishes no per-section support verdict) and **`W1-S25`** (the producer, not the browser, issues the next revision). Each row names the assertions it covers.

The arithmetic that shows nothing was dropped: **the same 399 tests, and `expect()` calls RISING from 1813 to 1822.**

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| F15-AC1 | PASS | `rc=0` | whole portal; the intermediate run NAMED the 7 broken callers (TS2305 + TS2339 x6, all in fe-s-6) |
| F15-AC2 | PASS | `REQUEST KEYS: 7 of 7`; `SNAPSHOT: body smartx:sx-2026-09-09 \| held smartx:sx-2026-09-09` | 7 of 7 keys vs the adapter's own denominator |
| F15-AC3 | PASS | `RESOLVED-KEY LEAKS: 0` | 2 objects scanned; control finds 2 planted |
| F15-AC4 | PASS | `VARIANT BY COUNT: 4 of 4` | counts 0,1,2,5 read out of rendered markup |
| F15-AC5 | PASS | `REFUSED: 2 of 2`; `SUBMITS REACHING THE CALL LOG: 0` | 2 arms; control sends 1 |
| F15-AC6 | PASS | `REQUEST ID: stable-on-retry, new-on-change` | 2 sends/1 id, then 3 sends/2 ids; 6 of 6 inputs move the key |
| F15-AC7 | PASS | `JOB STATES: 5 of 5`; `INPUTS PRESERVED: deep-equal` | 5 envelope fixtures; 9 of 9 wire states mapped |
| F15-AC8 | **PASS** | `REVISION IDENTITY: preserved` **and** `INPUTREVISION HITS IN tabs/analysis/: 0` | 7 of 7 identity fields; 0 hits over 11 files, asserted, with a positive control |
| F15-AC9 | PASS | `CLICKED: Analysis`, rc=0 | 1 capture, 390 wide, re-taken at `7305a6bfa9` |
| F15-AC10 | PASS | `CLICKED: Analysis`, rc=0 | 1 capture, 390 wide, re-taken at `7305a6bfa9` |
| F15-AC11 | PASS | `398 pass, 1 skip, 0 fail`, **1822 expect() calls** | 399 tests across 65 files |
| F15-AC12 | RECORDED | the two PNGs beside this file | judgment -- CVO at L9 |
| F15-AC13 | PASS | `ROUTES MATCHED: 12 of 12`; `NOT-YET-EXERCISABLE: 0` | 12 routes in the contract |
| F15-AC14 | PASS | `28 pass, 0 fail` | 28 tests across 5 files; **nothing under `__tests__/fe-s-13/` was touched by the retirement pass** (`git status` named only fe-s-15, fe-s-6 and tabs/analysis), so this was re-run as a confirmation |

The baseline the order stated (376 pass / 1 skip / 6 fail on DEV @84a86c10) was reproduced in this worktree before any edit, and the six failures were exactly the fe-s-13 (4) / fe-s-14 (1) / fe-s-1 (1) rows R2 addresses.

## WHAT WAS NOT DONE, AND WHY

- **The dead `parity` objects in `fixtures/fe-s-6/report.released.json` and `fixtures/smoke/fe-s-6-ready.json`.** No code reads them now. The amendment granted `__tests__/fe-s-6/` for the retirement, not another cell's fixtures, and a fixture edit no test grades is how a silent change lands. Row `W1-S24`.
- **Anything else under `__tests__/fe-s-6/`.** `_load.ts`, `variants.test.ts` and `source-bounds.test.ts` are untouched and pass unchanged (19 of 19 in that battery).
- **The corpus's `snapshot_id`** (`gen-corpus.ts` binds the scope fingerprint; the composer sends the snapshot's own revision). Not this order's act. Row `W1-S22`.
- **No push, no merge, no rebase** in either repo; `portal` never staged in the workspace repo.

## ROWS FILED

`IRPT_FNTEND-W1-S18` (BLOCKING, INERT -- **discharged** by the issuer's amendment and by this pass) · `W1-S19` · `W1-S20` · `W1-S21` · `W1-S22` · `W1-S23` · `W1-S24` · `W1-S25` (all OBSERVATION, INERT), in `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.
