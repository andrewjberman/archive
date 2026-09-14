# FE-s-35 -- the envelope refusal -- result

Worker `0.9.0_WK_IRPT_FNTEND~5` on `IRPT_FNTEND.TO-FE-s-35`. This is the session log the proof instance names.
The order was read from its WORKER FACE only.

- Workspace worktree: `/c/tmp/wk-irpt_fntend-5-5-fe-s-35`, branch `wk-irpt_fntend-5-5-fe-s-35`, cut from CLOUD @`0a74710f33`.
- Portal worktree: `<WS>/portal`, branch `wk-irpt_fntend-5-5-fe-s-35`, cut from portal DEV @`c2eb8eb4`.
- `node_modules` is the junction. `bun install` was never run.

## First act

`git rev-parse --abbrev-ref HEAD` printed `wk-irpt_fntend-5-5-fe-s-35`, and the tree check printed `TREE-OK`. Portal HEAD at the start was `c2eb8eb48276afb3f33c05e15dcdf602146c0519`.

## Premises re-grounded at portal c2eb8eb4

| Premise (face / issuer) | Measured |
|---|---|
| `investor-reporting.ts:907` `if (isEnvelopeShaped(payload))`; `:936-943` the pre-envelope plane | Held: `:936` `this.preEnvelopeResponses += 1`, then `adapt(payload)`, and the view is returned |
| `envelope.ts` `EnvelopeMismatch` `:93`; header `:34-40` | Held |
| `pre-envelope.test.ts` prints `3 of 3` and `BYPASS STILL OPEN` | Held |
| baseline | typecheck `rc=0`; the AC6 folder set read 274 pass / 2 skip / 0 fail across 38 files, precondition ABSENT |
| `adapt.ts:1098` `report_title: string`; `composer.ts:107` `string \| null` | Held (`:1097`, `:106` at this vintage) |
| "the contract's schema for that field" | NOT held: v1 names `report_title` in 0 of 25 files. Row `IRPT_FNTEND-W5-S2` |
| "2 of 6 suites carry no contract_version ... three tests red in those two" | NOT held as stated: 1 red in those two, and a third file serves a bare body. Row `IRPT_FNTEND-W5-S3` |

## What changed -- portal `357b40551d1ad62ca6808ceaaedbd118c0298048` (LOCAL)

| File | Change |
|---|---|
| `src/api/endpoints/investor-reporting.ts` | The pre-envelope branch of `send()` now throws `EnvelopeMismatch('body', op)`; the `preEnvelopeResponses` doc is corrected (kept, reads 0) |
| `contracts/envelope.ts` | The header's PRE-ENVELOPE BODIES paragraph now describes the refusal; no other change |
| `contracts/adapt.ts` | `report_title` only: `AnalysisGenerateRequestWire.report_title` and `AnalysisGenerateInput.reportTitle` are `string \| null` |
| `tabs/analysis/composer.ts` | `report_title` only: the header paragraph that said the adapter types `string` is corrected |
| `__tests__/fe-s-19/pre-envelope.test.ts` | A fourth body: the bare PerformanceReport document, 0 of 3 identifiers; the CONTROL line is unchanged |
| `__tests__/fe-s-35/no-identity.test.ts` | New: F35-AC4 and F35-AC5 |
| `__tests__/fe-s-1/adapter.test.ts` | The two stubs a transport serves (performance, holdings) are now v1 envelopes; assertions unchanged |
| `__tests__/fe-s-13/routes.test.ts` | The holdings stub (`{ instance: null }`) is now a v1 envelope whose `data` is that object; assertions unchanged |

## Criteria -- deciding runs at portal 357b4055

| Id | Result | Deciding line |
|---|---|---|
| F35-AC1 | PASS | `rc=0` (`tsc -b --noEmit`) |
| F35-AC2 | PASS | `PRE-ENVELOPE BODIES REFUSED: 4 of 4` |
| F35-AC3 | PASS | `CONTROL: a whole v1 envelope on the same path -> ACCEPTED (availability.state=READY)` |
| F35-AC4 | PASS | `PRE-ENVELOPE PLANE ADAPTED: 0`, beside `NO-IDENTITY BODIES REFUSED BY NAME: 8 of 8` and `REFUSAL PUBLIC REASON: ENVELOPE_BODY` |
| F35-AC5 | PASS | `REPORT_TITLE AGREES WITH THE CONTRACT IN BOTH BUILDERS: 2 of 2` |
| F35-AC6 | PASS | 277 pass / 2 skip / 0 fail, 279 tests across 39 files |
| F35-AC7 | RECORDED (judgment) | graded by 3.0.0_SA_CVO at L9 |

**How F35-AC6 was run.** The invocation was run exactly as written, with no port variable. At the deciding run 5181 was `ECONNREFUSED`, so the precondition was ABSENT and F19-AC4/AC5 were SKIPPED by name.

Earlier the same run met a FOREIGN dev server on 5181 (a DSGN worktree's vite). There F19-AC4/AC5 graded that tree: 0 of 2 and 0 of 2. See row `IRPT_FNTEND-W5-S1`.

Supplementary evidence, not the deciding run: the same file with `IRPT_FE_DEV_PORT=5197` against a vite started from THIS worktree read `BODIES MOUNTED: 2 of 2` and `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2`. The refusal does not break the enveloped mount path. The server was stopped afterwards.

Bun's folder arguments are prefix filters: `fe-s-1` also collects `fe-s-10` through `fe-s-18`. That is why the denominator is 39 files.

## Controls

**Mutant.** The pre-fix bytes of `investor-reporting.ts` and `adapt.ts` (read by `git show c2eb8eb4:<path>`) were copied over the working files. The mutant carries `this.preEnvelopeResponses += 1` once and `readonly report_title: string` once. The two new test files were then run, and the files restored from byte copies. The sha256 of each restored file equals its backup, and portal `git status --short` read 0 lines.
- pre-envelope: `MISSING ALL THREE -> rejected=false reason=null state=FAILED`, `PRE-ENVELOPE BODIES REFUSED: 3 of 4`, 0 pass / 1 fail.
- no-identity: `NO-IDENTITY BODIES REFUSED BY NAME: 0 of 8`, `PRE-ENVELOPE PLANE ADAPTED: 8`, `REPORT_TITLE AGREES WITH THE CONTRACT IN BOTH BUILDERS: 1 of 2` (adapt.ts reads `string`, DISAGREES), 1 pass / 2 fail. The positive control still passed under the mutant, as it must.

**Determinism.** Two same-input runs of each new test were compared line by line with the timing stripped: pre-envelope 14 of 14 lines identical, no-identity 30 of 30.

## What a no-identity body did before and does now (for L9, F35-AC7)

At the pre-fix bytes (the mutant run):
- `performance-report` RESOLVED TO A VIEW, and the counter read 1. This is the "guessed view".
- The other 7 operations whose request reached the transport surfaced as `IrRequestError` with no public reason code, because the operation's own adapter threw on a document of another shape. `envelopeFromRefusal` renders that as the generic FAILED envelope, indistinguishable from a transport failure.

Now:
- All 8 are `EnvelopeMismatch` naming `body`, with public reason `ENVELOPE_BODY`.
- `envelopeFromRefusal` renders each as `UNAVAILABLE` carrying `ENVELOPE_BODY`.
- The 3 operations with no declared route are refused before any request, unchanged.

NOT measured: a mounted browser page served a no-identity body. The browser driver serves only the enveloped maps its scenario builder writes, and both (`fe-s-19/browser-driver.mjs`, `fe-s-19/mounted-from-wire.test.ts`) are outside this order's `<paths>`. The claim is shown at the client and at the one state rule, not in a rendered panel.

## Rows filed (INVESTIGATION_v2.md)

- `IRPT_FNTEND-W5-S1` -- OBSERVATION, ARMED (disarm_owner 2.0.0_SA_COO~F): the browser criteria's precondition reads MET on a foreign tree at the default port.
- `IRPT_FNTEND-W5-S2` -- OBSERVATION, INERT: v1 has no schema for `report_title`; the type was read from UI_CONTRACT.md S10.
- `IRPT_FNTEND-W5-S3` -- OBSERVATION, INERT: the bare-body premise. 1 red in the two named files, not 3, and a third file serving a bare body.
- `IRPT_FNTEND-W5-S4` -- OBSERVATION, INERT: the dev server and `tsc -b` write caches through the junction into the shared `node_modules`.

## Not done, with reasons

- `LiveClient.send`'s `adapt` parameter is now unread on every path. The signature is kept, because changing it touches all 11 call sites; the code comment says so.
- Stubs that are never served are unchanged: `fe-s-13/no-route.test.ts` (three `{}` refused by route first) and `adapter.test.ts`'s parity-test transport (never called).
- Rows `IRPT_FNTEND-W2-S11` and `IRPT_FNTEND-W1-S39` (ARMED) name exactly the disarm this cell performs. Their disposition is the CVO's at L9, and neither row was edited.
- The port and probe in `fe-s-27/_dev-server.ts` (row W5-S1), and a v1 request schema (row W5-S2), are outside `<paths>`.

## Commits

- Portal `357b40551d1ad62ca6808ceaaedbd118c0298048` "FE-s-35: refuse a response body with no v1 envelope; one report_title type in both builders" -- LOCAL on `wk-irpt_fntend-5-5-fe-s-35`; the portal is frozen.
- Workspace: the commit that carries this file, the proof instance, rows W5-S1..S4 and the order's `complete` flip -- LOCAL on `wk-irpt_fntend-5-5-fe-s-35`.
