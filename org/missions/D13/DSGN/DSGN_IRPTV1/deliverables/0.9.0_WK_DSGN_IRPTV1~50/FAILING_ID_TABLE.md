# FAILING_ID_TABLE -- TO-IV-e-90: the 43 failing ids of the suite sample, each a REGRESSION with an owner and a cell, or a RETIREMENT asked

Worker 0.9.0_WK_DSGN_IRPTV1~50, 2026-10-11. Baseline `org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~43/SUITE_SAMPLE.json` (portal 7bb81fa8, 43 of 43 ids, three identical runs). Record: `FAILING_ID_TABLE.json` beside this file (full cause and evidence per id). Ruling executed: CTO ROUND-13 ANALYSIS sections 2 and 3. Read-only: no test was run for this table; one 5-line bun probe of `requirePublicStatus` was run on the sampled bytes.

**Counts.** REGRESSION_OWNED 33, RETIREMENT_ASKED 10, total 43 of 43. Of the 14 ids the sample labelled KNOWN-LEGACY: 5 are REGRESSION_OWNED and 9 are RETIREMENT_ASKED. The other named ids: IVE115 RETIREMENT_ASKED (ruled); IVE137 REGRESSION_OWNED UNCUT; F47-AC7 and F47-AC6 REGRESSION_OWNED IV-e-92; F40-AC5 REGRESSION_OWNED IV-e-89.

## REGRESSION_OWNED (33)

| cell | n | ids | owner | cause |
|---|---|---|---|---|
| IV-e-89 | 1 | window.test.ts | 2.0.0_SA_COO~D2 | The portal calendar fallback spans 2024-2027 while lib/trading_calendar.py spans 2010-2027 (Expected 2024 Received 2010); the portal takes its fallback from the one frontier. |
| IV-e-91 | 1 | iv-e-17.bridge-dropped.test.ts | 2.0.0_SA_COO~D2 | The test spawns fe-s-13/content-pins.test.ts and fails only on 'content-pins.test.ts rc=1, expected 0'; its own arms (no bridge cast, 17 of 17) print true. It clears when IV-e-91 fixes the content-pins ids (it is not itself one of |
| IV-e-91 | 18 | content-pins.test.ts; content-pins.test.ts; content-pins.test.ts; producer-fixtures.test.ts; producer-fixtures.test.ts; request-corpus.test.ts; request-corpus.test.ts; routes.test.ts; routes.test.ts; ... | 2.0.0_SA_COO~D2 | Contract files in the workspace tree (docs/contracts/investor-reporting/v1: 22 DECLARED routes, unprojected_grant, download_route) are ahead of the portal half; CTO ROUND-13 ANALYSIS section 3 row D2-W43-S2: the portal moves. |
| IV-e-92 | 6 | iv-e-18.fields-rescope.test.ts; iv-e-25.states-rescope.test.ts; suite-complete-check.test.ts; suite-complete-check.test.ts; suite-complete-check.test.ts; suite-complete-check.test.ts | 2.0.0_SA_COO~D2 | The test spawns bun at C:/Users/AndrewBerman/.bun/bin/bun (ENOENT on this device); resolve bun from the environment. |
| IV-e-92 | 2 | no-status-reason.test.ts; no-status-reason.test.ts | 2.0.0_SA_COO~D2 | The test reads fixtures/wire/AnalysisReportResponseData.valid.json from git HEAD; that file is absent (the tree holds AnalysisReport.valid.json; the data type name comes from the generated contracts/wire/responses.ts). Recorded fi |
| UNCUT | 1 | iv-e-116.generate-journey.test.tsx :: IV-e-116 -- Generate leads to the request's own status view and the li... | 2.0.0_SA_COO~D2 | Stale source-text pin, not a lost behaviour. ARM(b) matches the press branch by the literal 'const outcome = await submitComposition(submitter, scopeRef, inputs)'; GenerateComposer.tsx now reads 'await submitWithTenant(scope, submitter, scopeRef, inputs)' (the tenant fix, rows S55/S59, line 418) and |
| UNCUT | 1 | iv-e-137.comparison-resolve-and-name.test.tsx :: IVE137 -- a comparison is resolved before it is added, and named > (f)... | 2.0.0_SA_COO~D2 | Stale source-text pin. The second expect looks for "if (initialCatalogue || !api || api.kind !== 'live') return" in GenerateComposer.tsx; line 267 now reads "...api.kind !== 'live' || tenantMissingFor(scope, scopeRef)) return" (the tenant fix). The first expect (resolveComparison before addCompariso |
| UNCUT | 1 | iv-e-26.wire-regen.test.ts :: IVE26-AC3 -- gen-wire.ts regeneration is idempotent, data is optional,... | 2.0.0_SA_COO~D2 | gen-wire.ts throws UnrenderableSchemaError at OwnedAnalysisRequest.schema.json#/properties/persist_inputs/properties/report_index/alternatives/1/properties/report_id: the contract (IRPT_BCKEND IB-pr-411, aff85bff09) declares report_id, revision and retention_ref as empty schemas {} and the generator |
| UNCUT | 1 | fixtures.test.ts :: fixture set > the smoke map covers every scoped route, one entry each | 2.0.0_SA_COO~D2 | fe-s-1/fixtures.test.ts reads docs/contracts/investor-reporting/v1/routes.json: 22 DECLARED routes. The portal's fixtures/smoke/default.json holds 12 keys, so ten declared routes match no key (selection-create, directory-browse, custody-report-read, custody-report-persist, analysis-input-upload, ana |
| UNCUT | 1 | absent-vs-null.test.ts :: F25-AC3 -- `?? null` is refused wherever the contract distinguishes > ... | 2.0.0_SA_COO~D2 | The assertion still holds and the product violates it: the scan finds five '?? null' coalesces on contract-distinguished fields in contracts/adapt.ts (status?.state line 312; section.value 941 and 990; section.reason 977; wire.facts.frozen_as_of 1360), where W35-S3 saw two. Cell needed: for each of  |

## RETIREMENT_ASKED (10)

| ids | assertion retired | ruling |
|---|---|---|
| iv-e-109.accounts-ordinal-scale.test.ts; iv-e-110.drill-bar-classes.test.ts; iv-e-111.skip-single-level.test.ts; iv-e-112.one-scope.test.ts; iv-e-25.colour-by-code.test.ts | ARM3/ARM4 (git diff <BASE> -- src/pages/ModelPortfolios.tsx must print 0 bytes): the file carries no diff against the commit this test's own session started from. The test's behavioural arms (ARM1/ARM2 and, in IVE112, the onSelect/onAccountDrill arms) pass in  | ASKS A RULING (none found) |
| iv-e-115.order-and-disclosure.test.tsx | ARM1: assetClassRank over the class list returns [0,1,2,3,4,5,6,7,8] (nine ranks, Cash 0 .. Unclassified 8). | org/missions/D8/MDPF/MDPF_SECCLASS/task-orders/MDPF_SECCLASS.TO-SC-e23.portal-six-class-lists.md:30 |
| iv-e-69.performance-finished.test.tsx | UIC-08: WORDED_REFUSAL_WORDS.OBJECT_NOT_COVERED contains the phrase 'the Opal Capital service team'. | org/missions/D13/DSGN/DSGN_IRPTV1/STATUS.md:66 |
| source-bounds.test.ts | FORBIDDEN list entry 'ycharts': neither api/endpoints/investor-reporting.ts nor contracts/index.ts may contain the token. | ASKS A RULING (none found) |
| absent-vs-null.test.ts :: F25-AC2 -- ABSENT and NULL are two diffe; absent-vs-null.test.ts :: F25-AC2 -- ABSENT and NULL are two diffe | F25-AC2 arm: a status whose source_dates.business_date is an explicit null is admitted by parseIrEnvelope and rendered, distinguishable from an absent date (NO_SOURCE_AGE_YET vs SOURCE_DATE_MALFORMED). | ASKS A RULING (none found) |

## UNCUT cells named (5 ids, 5 cells)

- `iv-e-116.generate-journey.test.tsx :: IV-e-116 -- Generate leads to the request's own status view and the li...`: re-pin the regex at iv-e-116 ARM(b) to the submitWithTenant call and show the pre-fix control still fails it.
- `iv-e-137.comparison-resolve-and-name.test.tsx :: IVE137 -- a comparison is resolved before it is added, and named > (f)...`: re-pin the literal; the property (the catalogue read runs only on the live client) still holds.
- `iv-e-26.wire-regen.test.ts :: IVE26-AC3 -- gen-wire.ts regeneration is idempotent, data is optional,...`: decide whether the portal generator renders {} as unknown, or IRPT_BCKEND types those three members in the contract; then regenerate.
- `fixtures.test.ts :: fixture set > the smoke map covers every scoped route, one entry each`: add the ten smoke entries (bodies from the committed wire fixtures), or fold into IV-e-91 by amendment.
- `absent-vs-null.test.ts :: F25-AC3 -- `?? null` is refused wherever the contract distinguishes > ...`: for each of the five, carry absent as absent or record the field's contract reading that admits null; owner is the lane that owns contracts/adapt.ts.

## What this table did not establish

- No test was re-run; every cause is read from the three identical run logs, the test source and the product source at portal 7bb81fa8 (read by content). Where a cause is a one-line source-pin it was matched to the source line, not re-executed.
- F40-AC5 and the 18 contract ids rest on the CTO ruling and the sample; this table did not re-diagnose them. IVE17-AC3 is attributed to the content-pins ids by its own printed text (rc=1 from content-pins), not by a run after a fix.
- No ruling retiring the Model Portfolios diff arms, the `ycharts` token or the F25-AC2 null arm exists that this worker found: adjudications/ and remediations/ were searched by Grep for the row ids and test names (ADJUDICATION_v7 lists W21-S4 and W35-S3 as known failures without ruling on them; REMEDIATION_v7:11 says none of the 14 cites a retiring ruling) and the two CTO analyses were read for sections 2-3; they are not read whole. Those retirements are asked, not cited.

