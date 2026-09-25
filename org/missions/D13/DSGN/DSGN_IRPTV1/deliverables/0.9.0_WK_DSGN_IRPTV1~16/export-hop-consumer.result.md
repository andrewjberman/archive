# DSGN_IRPTV1.TO-IV-e-26 -- export-hop-consumer -- session log

Worker `0.9.0_WK_DSGN_IRPTV1~16`, worktree pair `wk-DSGN_IRPTV1-16` / `wk-DSGN_IRPTV1-16/portal` (base DEV `8242412dde9a3ef807e118f648242cf24ffe2981`).

## (a) submit-export's data-less QUEUED/RUNNING answer

`portal/src/pages/InvestorReporting/export/submit.ts` gains `interpretSubmitExportAnswer`, a pure function over the
GENERATED wire shapes (`ExportReceiptWire` / `PublicStatusEnvelopeWire`, both from `contracts/wire`, never the adapted
view): `data` present is accepted whole (export id = `data.export_ref.export_id`); `data` absent is accepted ONLY
while `status.state` is `QUEUED` or `RUNNING` (export id = `status.operation.revision`); any other state without
`data` refuses by name, naming the state it carried (or its absence).

## (b) the print URL

`portal/src/pages/InvestorReporting/render/PrintEntry.tsx` gains `parsePrintWindow`, reading `?selection=`, `?start=`
and `?end=` from the URL in that order; a Performance print with any one missing refuses by name before any request is
made (not even the bundle fetch). `portal/src/pages/InvestorReporting/export/resolveBundle.ts`'s `ResolveBundleDeps`
gains additive, optional `accountSelection`/`start`/`end`: a caller naming NONE of the three (every round-1 call site
-- `Preview.tsx`, `fe-s-9/resolve.test.ts`, `fe-s-31/every-page.test.ts`) is unaffected (the legacy `businessAsOf`
fallback stands, verified unchanged by diff and by re-running those suites); a caller naming ANY of the three for a
`reportKind: 'performance'` resolve must supply all three or the resolve throws `MissingPrintWindowError` naming the
first one missing, before any request.

## Wire regeneration

`bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts` was run once at the portal root; the diff landed
`SubmitExportResponseWire.data` as optional (matching the schema's own conditional-required, which the generator
already reads off `required`) and picked up one unrelated producer-side drift already live in
`docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json` (`asset_class` gains `'other'`) -- committed as
part of the same regeneration since the cell's own instruction is "regenerate `IR/contracts/wire/**`", not a
selective file.

## Pre-existing, out-of-grant finding

`fe-s-9/resolve.test.ts`'s first test (round-1, not in this order's `<paths>`) fails at HEAD independent of every edit
in this order -- confirmed by a standalone repro against the unmodified fallback branch. Filed as
`DSGN_IRPTV1-W16-S1` (OBSERVATION, INERT); not fixed (out of grant, orthogonal to IV-e-26's four criteria).

## Controls

Mutant: `submit.ts`'s QUEUED/RUNNING branch was disabled in place (`if (false && ...)`), AC1's test failed exactly as
expected (2 named failures), then restored -- confirmed byte-identical to the pre-mutant diff by re-running the test
green. Determinism: AC1/AC2/AC3's exact invocations each run twice back to back, identical VERDICT and pass/fail both
times.
