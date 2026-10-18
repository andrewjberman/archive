# FEATURE RECEIPT -- AMGT-cb-1: the Exec Management tab handles all three states of the CEO reading explicitly

Order: `AMGT_RESAPP.TO-AMGT-cb-1.the-portal-ceo-profile-handles-all-three-states-explicitly-after-a-census-of-every-consumer`
Worker: `0.9.0_WK_AMGT_RESAPP~523` (round 121, issued by `2.0.0_SA_COO~R1`)
Row `AMGT_RESAPP-D1-W518-S2`: on the branch, the census reads every consumer inside the page as handling all four states. The two lib consumers are recorded read-only in the census and two rows are filed (W523-S1, W523-S2). Closure of W518-S2 is the issuer's grade on the running page after the landing (`AMGT-cb-2`).

## What the branch carries

- Branch: `cand/dell1/amgt-sa-ceo-three-states` (nested portal repository, `C:/dev/wk-resapp-523/portal`), LOCAL, not pushed. DEV and PROD untouched.
- Head commit: `43762e0d` (`AMGT-cb-1 (AMGT_RESAPP round 121): the Exec Management tab handles all three states of the CEO reading explicitly`).
- Base: PROD `ff611566` (portal-v2.1.240).
- Diff `ff611566..HEAD`: 7 files, 1443 insertions, 13 deletions.

| changed path (portal root) | class |
|---|---|
| `src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx` | page (edited: `CeoProfile`, the header docstring, one helper) |
| `src/pages/SecurityAnalysis/types.ts` | page (edited: `NOT_WRITTEN` added to the `CeoProfileReading.reading` union, nothing else) |
| `src/pages/SecurityAnalysis/__harness__/threeStateCeoProfile.harness.cjs` | page harness (new) |
| `src/pages/SecurityAnalysis/__harness__/ceoConsumerCensus.json` | page census data (new) |
| `src/pages/SecurityAnalysis/__harness__/cb_served_management_TSM_US_Equity.json` | fixture (new; copy of the round121_prep served object) |
| `src/pages/SecurityAnalysis/__harness__/cb_served_management_HD_US_Equity.json` | fixture (new; copy of the round121_prep served object) |
| `src/pages/SecurityAnalysis/__harness__/cb_served_management_RIO_LN_Equity.json` | fixture (new; copy of the round121_prep served object) |

## Census

Taken at base `ff611566` by the native Grep tool, with the denominator printed. Patterns: `ceo_profile_reading`, `ceo_public_profile`, `CeoProfile`, `UNREADABLE_OBJECT`, `NOT_WRITTEN`, `SEARCHED_NOTHING_FOUND`, `SEARCHED_LINKS_UNREADABLE`, `SEARCH_FAILED`, `NOT_SEARCHED`, `data-ceo-profile`. Scopes: `portal/src` (52 hits, 14 files), the outer worktree `lib/` (332 hits, 50 files), `infra/` (0 hits, 0 files). The `NOT_SEARCHED` and `NOT_WRITTEN` patterns also match unrelated fields in `lib/research/metrics` and the section dictionary of `render_pack.py`; those are classed HOMONYM, not CEO.

Counts per class and scope:

| class | portal/src | lib/ | total |
|---|---|---|---|
| CONSUMER | 21 | 9 | 30 |
| PRODUCER | 0 | 83 | 83 |
| TYPE | 8 | 7 | 15 |
| PIN (test, harness or fixture carrying the words) | 23 | 207 | 230 |
| HOMONYM (same word, another field) | 0 | 26 | 26 |
| **total** | **52** | **332** | **384** |

Per file (hits; class):

| file | hits | class |
|---|---|---|
| `portal/src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx` | 21 | CONSUMER (`CeoProfile`, lines 190-274; the four header-docstring hits attributed to it; call site line 390) |
| `portal/src/pages/SecurityAnalysis/types.ts` | 8 | TYPE (interface line 835, union words 838-842 at base, fields 914-915 at base) |
| `portal/src/pages/SecurityAnalysis/__harness__/execText.harness.cjs` | 3 | PIN (ceo tail regex and the NOT_SEARCHED reason) |
| `portal/src/pages/SecurityAnalysis/__harness__/tabs.harness.cjs` | 2 | PIN (count of `data-ceo-profile` equal to the served word) |
| `portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.{SAP_GY,HD_US,COST_US,BA_US,BABA_US}_Equity.json` | 1 each (5) | PIN |
| `portal/src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json` | 3 | PIN (fixture; not asserted for the CEO line) |
| `portal/src/pages/SecurityAnalysis/__harness__/aiFill.fixture.json` | 1 | PIN (fixture) |
| `portal/src/pages/SecurityAnalysis/__harness__/execFixture.{CSL_AU,CAT_US,6861_JP}_Equity.json` | 3 each (9) | PIN (fixtures) |
| `lib/research/print/render_pack.py` | 15 | CONSUMER 7 (`_ceo_profile_sentence`, lines 994-1009) + HOMONYM 8 (section `NOT_WRITTEN` dictionary) |
| `lib/research/aifill/block_mgmt_bio.py` | 2 | CONSUMER (object input, lines 47, 116) |
| `lib/research/api/scoped_amgt.py` | 40 | PRODUCER (`ceo_profile_reading`, lines 4883-5019; served at 5287 and 5347) |
| `lib/research/management/ceo_search.py` | 22 | PRODUCER |
| `lib/research/management/enrich.py` | 19 | PRODUCER |
| `lib/research/management/proxy_officers.py` | 2 | PRODUCER |
| `lib/research/management/management.schema.json` | 7 | TYPE |
| `lib/research/metrics/generation_writer.py` | 2 | HOMONYM (`REASON_NOT_SEARCHED`) |
| `lib/research/metrics/chatter_axis.py` | 5 | HOMONYM (coverage `NOT_SEARCHED`) |
| `lib/research/metrics/tests/test_q4_rank_declared_set.py` | 10 | HOMONYM (by location; not read line by line) |
| `lib/research/metrics/tests/test_chatter_incomplete.py` | 1 | HOMONYM (by location) |
| `lib/research/api/tests/test_ca1_ceo_reading_three_states.py` | 20 | PIN |
| `lib/research/print/tests/test_ca1_ceo_three_states.py` | 14 | PIN |
| `lib/research/management/tests/test_reproject_public_profile.py` | 37 | PIN |
| `lib/research/management/tests/test_jp_president_and_readable_reasons.py` | 12 | PIN |
| `lib/research/api/tests/test_generation_and_pool_routes.py` | 12 | PIN |
| `lib/research/management/tests/test_management.py` | 8 | PIN |
| `lib/research/api/tests/test_ceo_reading_new_basis.py` | 8 | PIN |
| `lib/research/management/tests/test_ceo_basis_plain.py` | 7 | PIN |
| `lib/research/print/tests/fixtures/bw2_sections.json` | 6 | PIN |
| `lib/research/api/tests/test_fallback_roster_served.py` | 4 | PIN |
| `lib/research/api/tests/test_served_reasons_plain.py` | 4 | PIN |
| `lib/research/aifill/tests/test_block_mgmt_bio.py` | 4 | PIN |
| `lib/research/print/tests/test_by1_reason_mapper.py` | 4 | PIN |
| `lib/research/print/tests/test_bw2_pack_form.py` | 4 | PIN |
| `lib/research/print/tests/test_ay1_dated_figures_and_served_thesis.py` | 5 | PIN |
| `lib/research/print/tests/test_ax4_brand_form.py` | 3 | PIN |
| `lib/research/print/tests/test_bz2_rich_management_equals_pdf.py` | 3 | PIN |
| `lib/research/management/tests/test_domain_verified_fallback.py` | 3 | PIN |
| `lib/research/management/tests/test_bloomberg_fallback.py` | 3 | PIN |
| `lib/research/print/tests/fixtures/bx_served_thesis_{RIO_LN,GOOGL_US,ICT_PM}.json` | 3 each (9) | PIN |
| `lib/research/print/tests/fixtures/bz_served_thesis_{BA_US,GOOGL_US,HD_US,ICICIBC_IN,ICT_PM,KMB_US,RIO_LN,TSM_US}.json` | 3 each (24) | PIN |
| `lib/research/print/tests/fixtures/bv2_quote_blocks.json` | 2 | PIN |
| `lib/research/print/tests/fixtures/bw2_management_bundle.json` | 2 | PIN |
| `lib/research/api/tests/test_an6_repairs.py`, `test_bz2_rich_route_management_input.py` | 1 each (2) | PIN |
| `lib/research/api/tests/test_management_officer_set.py` | 2 | PIN |
| `lib/research/print/tests/test_bx3_cleared_machine_passages.py` | 1 | PIN |
| `lib/research/api/tests/test_bw4_print_pack_degrades.py` | 1 | PIN |
| `lib/research/management/tests/test_ceo_search.py` | 1 | PIN |
| `lib/research/management/tests/test_proxy_officers_persist.py` | 2 | PIN |

The per-file rows sum to the scope totals (portal 52, lib 332). `infra/` holds no hit.

CONSUMER rows (the census data file, `src/pages/SecurityAnalysis/__harness__/ceoConsumerCensus.json`):

| consumer | scope | SERVED | NOT_WRITTEN | UNREADABLE_OBJECT | SEARCHED_NOTHING_FOUND | at base |
|---|---|---|---|---|---|---|
| `CeoProfile` (`ExecManagementTab.tsx` 190-274) | portal | true | true | true | true | NOT_WRITTEN and UNREADABLE_OBJECT were false (fell to the default sentence) |
| `_ceo_profile_sentence` (`render_pack.py` 998-1017; call sites 1155 PDF, 1879 rich) | lib, read-only | true | true | true | **false** | SEARCHED_NOTHING_FOUND falls through to the reason (1016-1017); surprise row W523-S1 |
| `block_mgmt_bio.py` 116-127 | lib, read-only | false | false | false | false | object input, no state sentence; surprise row W523-S2 |

Counts after the edit: the portal consumer row has all four states true; the two lib consumer rows and the census's TYPE rows are the only non-page entries. Base: the page consumer had two states false (NOT_WRITTEN, UNREADABLE_OBJECT) and the union had six words.

## Pins

Pinning assertions in the page's harness folder, checked against the edited page. Each is listed with its old and new text. No assertion pins today's no-public-profile sentence or the old UNREADABLE_OBJECT default for a null profile (surprise row W523-S3), so no assertion needed re-scoping.

| # | where (portal) | assertion, old | assertion, new | re-scoped |
|---|---|---|---|---|
| P1 | `__harness__/execText.harness.cjs:124` | `ceoTail`: `<p data-ceo-profile="[^"]*"[^>]*>` (any state) | unchanged | no (matches any state) |
| P2 | `__harness__/execText.harness.cjs:139, 163` | the CAT (NOT_SEARCHED) reason's final period is read from the fixture and the tail must carry it | unchanged (NOT_SEARCHED prints the same markup) | no |
| P3 | `__harness__/tabs.harness.cjs:377-378` | `countOf(execHtml, 'data-ceo-profile="' + reading + '"') === 1` | unchanged: the page still carries the object's raw word on `data-ceo-profile` for the third sentence (the tabsFixture readings are unknown words such as `NOT_CONFIRMED_INSTRUMENT_CANNOT_SAY`) | no (holds) |
| P4 | `__harness__/execFallback.harness.cjs`, `execPattern.harness.cjs` | no CEO-state assertion (they read the roster and the officer table) | unchanged | not pins |
| P5 | `__harness__/tests/uiContractFixtures.json` (3 hits) | fixture for the lead-panel rankings; the CEO block is data, not asserted | unchanged | not a pin |

The round-103 green instrument (AC2) runs every harness on the branch and at base; its result is in the report.

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis (Exec Management tab, `CeoProfile`) | /security-analysis | Opal-internal | internal |

No other page is changed. No shared file is changed.

## Shared files

- none

## Not carried

Each path absent from the branch: the count is `git diff ff611566 HEAD -- <path> | wc -l`, read at HEAD `43762e0d`.

| path | diff lines |
|---|---|
| `package.json` | 0 |
| `bun.lock` | 0 |
| `src/lib/firmAccess.ts` | 0 |
| `src/App.tsx` | 0 |

## How to look

1. From the workspace: `cd portal && bun run dev:live --port 5174` (dev builds use port 5174 only).
2. Open `/security-analysis`, choose the Exec Management tab.
3. `TSM US`: the CEO line reads `CEO public profile: No CEO profile has been written for this company yet.`
4. `RIO LN`: the same sentence.
5. `HD US`: `CEO public profile (EDWARD P. DECKER): searched, nothing found -- ...` (unchanged from PROD).
6. A failed read (the forced corrupt object) reads `CEO public profile: The CEO profile could not be read.` Only the harness proves this state; no served name carries it today.

The harness is the worker's proxy (`node src/pages/SecurityAnalysis/__harness__/threeStateCeoProfile.harness.cjs`, run from the portal root). The page-level grade is the issuer's, after the landing (`AMGT-cb-2`).
