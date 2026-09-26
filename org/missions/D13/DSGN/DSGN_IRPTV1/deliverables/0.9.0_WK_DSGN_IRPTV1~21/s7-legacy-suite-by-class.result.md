# DSGN_IRPTV1.TO-IV-e-32 (S7 -- legacy suite by class) -- result

Base measured at portal `72ed1256` (post IV-e-31): `bun test src/pages/InvestorReporting` reported
763 pass / 27 skip / 79 fail (77 real testcase failures + 2 whole-file module-load crashes:
`fe-s-33/fixtures-reach.test.ts`, `fe-s-47/no-status-reason.test.ts`), across ~36 files. This
matches the round-4 analysis's "about 80 legacy failures... about 36 files" (section 2).

## The shared bug family

Nearly every failure traced to one of a handful of systemic defects, fixed at their source
rather than per test (full list in the portal commit message, `03f48301`):

1. `unprojected_grant.kinds` authored as `[]` (array) everywhere it should be `{}` (the wire
   type is `Record<string, number>`) -- generators, shared test helpers, committed fixtures.
2. `internal_correlation_id` (StatusEnvelope's SERVER-ONLY field) leaking into wire-facing
   `status` members the same generators/helpers/fixtures build, which
   `contracts/public-status.ts` correctly refuses.
3. `contracts/public-status.ts` itself over-required `state` and a non-null
   `public_reason_code`, refusing legitimate "no state" / "no reason" wire shapes the
   codebase's own adapters already handle (class G).
4. `resolve-scope`'s firm_id-match rule (envelope's `firm_id` must equal
   `data.verified_request_firm_id`) tripped wherever a generator/test paired the opaque
   envelope convention with the registry-spelled ResolvedScope/DirectoryEntry fixtures.
5. Route-table growth (12 -> 17 DECLARED) left several generators/tests with stale literals
   (missing `requestId` PATH_PARAMS, hardcoded route counts, a missing `accountSetId`
   `selectedReference` now requires, a `dataFor` schema reader that didn't recognize `oneOf`
   or a fixture-less `PublicStatusEnvelope`). Authored the three still-missing producer
   fixtures (AnalysisUploadResult, OwnedAnalysisRequest, OwnedAnalysisRequestHistory),
   schema-validated before commit.
6. A percent-formatted `Metric` (commit `a0fa8137`) now prints `value * 100` + `%`;
   `render/fixtures/bundle.performance.json` still stored whole-percent numbers from before
   that change -- rescaled to fractions.
7. Three assertions retired by later PRD-driven changes, re-scoped with their FWD/commit
   citations (FirmDropdown's one-firm identity slot, FWD-4 v0.8; ProspectJobStatus.tsx as a
   real production consumer, FWD-8 v0.8; the percent-formatted period return, FWD-5 v0.8).

## Where this leaves the round

Full class table: `org/missions/D13/DSGN/DSGN_IRPTV1/ledger/S7_CLASS_TABLE.json` (79 rows,
`base_failures: 79`). IVE32-AC1 (table structure) passes: `VERDICT: S7-TABLE-OK`.

IVE32-AC2 (the live suite's failing set matches exactly the table's Q rows) does **not** pass.
A fresh full run after every fix + the portal commit (`03f48301`) still shows failures beyond
the 4 Q rows: 19 of the original 77 real-testcase rows remain failing (root-caused in the table's
`action` text for each -- mostly the `requirePublicStatus` business_date obligation on
intentionally-dateless status fixtures, and two still-unresolved production render/adapter
questions), plus the two crash-file rows are only partially clean (5 of 8 fe-s-47 tests and most
of fe-s-33's now pass, not all). A run-to-run comparison of the file-system/subprocess-heavy
files (`fe-s-33`, `fe-s-39`, `fe-s-46`) also showed different specific sub-tests failing between
runs -- filed as a surprise row (possible shared-state/order-dependent flakiness in those files,
independent of this cell's fixes).

One genuine regression surfaced from a necessary class-G/H fix and is recorded as a surprise
row: `fe-s-41/one-writer.test.ts`'s STATUS_SCHEMA source fix (reading
`PublicStatusEnvelope.schema.json` instead of the internal `StatusEnvelope.schema.json`) is a
real, non-cosmetic content change to a file `fe-s-46/timeouts.test.ts` polices as changing ONLY
`test(...)` timeout arguments relative to DEV `1f3ce9f0` -- the two tests' invariants conflict,
and `fe-s-46` now fails on that one file. Not resolved this round.

Given IVE32-AC2 fails, `DSGN_IRPTV1.TO-IV-e-32`'s `<status>` is **not** flipped to `complete`.
