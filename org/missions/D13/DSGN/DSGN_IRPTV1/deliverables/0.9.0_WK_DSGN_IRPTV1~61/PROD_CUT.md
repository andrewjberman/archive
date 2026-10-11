# The PROD cut, in plain words

Written by 0.9.0_WK_DSGN_IRPTV1~61 for task order DSGN_IRPTV1.TO-IV-e-111. Nothing here is pushed, to DEV or to PROD. The exact record is `PROD_CUT.json` beside this page.

## What it is

One candidate on top of portal PROD `37aa1247ee`: portal branch `wk-dsgn-irptv1-r25-61-prodcut`, head `fc876722f5af6e92f8f045982e1b1d7ad73755f7` (two commits; the first took only the staged half). It changes 8 files, all under `src/pages/InvestorReporting/` or the one endpoint file. It carries four things and nothing else:

- **The history reader** (`readOwnedHistory`, ruling (B)). It now takes both answers the service can serve, the two-key page and the contract's page. Test: IVE99-HR, 6 tests.
- **The two missing irpt-status reads.** The Branded PDF link and the original-file link: two route rows, two client methods, and the envelope adapter for the original-file link. Test: a new IVE111-SR, 4 tests (DEV's tests for them sit in Ticket Center, outside this cut).
- **`retained_ref`** on the report sections reader. No page prints it. Test: IVE106, 3 tests; a deliberate break of the vendor-form line made it fail (2 pass, 1 fail) and the file was restored.

No page is changed to show any of it. The Holdings face, the Opal wording, the Prospect opener, the labels, the wider wire and fixture folders and the Ticket Center callers are left out (nine lines in `left_out`).

## Where it is live

The Investor Reporting page and its print view. The page route sits behind admin, the Opal firm and user type Dev. The print route admits a render token as well, and so stays "unsure" under the push law.

## The print route's import closure: four changed files are in it

Method: the build's own module graph, read by a one-off rollup plugin in an uncommitted wrapper config (deleted after; a copy is in `closure_method/` with the two scripts that compute the closure and the controls). From `render/PrintEntry.tsx`, static and dynamic imports reach 106 source files; the chunk graph (the PrintEntry chunk and 60 chunks it reaches, 558 source modules) agrees on the changed files. Control: `AnalysisDocument.tsx`, which the print entry imports, is found. Negative control: `tabs/holdings/HoldingsTab.tsx` is in the build and absent from the closure.

In the closure: `src/api/endpoints/investor-reporting.ts` and `contracts/adapt.ts` (the print entry imports both directly), and `contracts/envelope.ts` and `contracts/owned-requests.ts` (through the endpoint file). The other four changed files are three tests and a types-only file. No small clean separation moves the four out: the endpoint file is the print entry's own import. Verdict: **WAITS_ON_ANDREW** (row DSGN_IRPTV1-D2-W61-S2), as the ruling says any file in that closure does.

## Checks

PROD's own suite reads 1088 pass, 27 skip, **42 fail** against today's workspace contract. The candidate reads 1101 pass, 27 skip, 42 fail, with the identical 42 failing: it adds none and fixes none (row DSGN_IRPTV1-D2-W61-S1). So the second criterion reads FAIL on the suite count as written; making the 42 pass means bringing the rest of the range. Lint 0 errors (319 warnings, the same as PROD), typecheck clean, build clean.
