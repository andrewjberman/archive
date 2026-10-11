# L8 drain end -- ADVI_COTBKF round 6, with the round-5 analysis's three issuer items

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~10:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB4d5-AC3)

The round-5 analysis (`1.0.0_SA_CTO~DELL2` @21843491cd) parked three items on un-park conditions and said to issue each the tick it
un-parked. All three un-parked this hour and are done:

| item | un-park | act | ledger | read-back |
|---|---|---|---|---|
| E5 crosswalk applied | re-ruling msg 264 (row S13: the target is `opal-data-assets`) | issuer's apply 09:38Z | `advi-cotbkf-r5-crosswalk-apply-20261007` CLOSED @98652475d8 | 1,533 rows, 439 MATCHED, 1,094 NOT_MATCHED; `near_matches_applied=0` |
| E3 documents applied | msg 264 + CB-f-1 (round 6) meeting the CTO half's two conditions | issuer's apply 09:47-10:18Z | `advi-cotbkf-r6-documents-apply-20261007` CLOSED @3c39c9f4ae | 11,119 written, 0 failed, 0 refused; 11,120 objects (11,119 pdf + `documents.parquet` 11,119 rows); SHA-256 5 of 5 sampled equal; `held_restricted=0`, `crm_source_keys=0` |
| E2 links on the covering calendar, applied | laptop 106145 (calendar fix @83ab7192ee in dell2 CLOUD @0a73ed06a0) | issuer's apply 10:19Z | `advi-cotbkf-e2-account-links-apply-20261007` CLOSED @3c39c9f4ae | 1,450 rows, 212 LINKED, equal to the laptop deliverable on every column 1,450 of 1,450 |

Every apply ran under a never-widen pair: E5 and E3 -- COO `deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_ROUND5_E5_E3_APPLIES_COO_HALF.md`
(sections 5-6), CTO `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ROUND5_E5_E3_APPLIES_CTO_HALF.md`; E2 -- COO @163c0dd8a1, CTO @792b16742d.
Reader census before each: 0 of 135 estate chains, and only the script and its test in the code tree.

## Round 6 order

| order | worker | drain | criteria | real run (dell2, after the drain) |
|---|---|---|---|---|
| CB-f-1 restricted path in any bucket; crm source count | ~20 | @fa9d12daa1 | VALID: AC1 5 passed (both buckets, difference control, zero-put arm), AC2 PASS | `DOCUMENTS-PLAN unique=11119 ... held_restricted=0 writable=11119 crm_source_keys=0`; documents suite 16 passed |

1 of 1 orders terminal; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

## Judgment for L9

**CB4d5-AC3** (round 4, owed at the apply): one statement and one tax form found by account and date and opened. Found from
`documents.parquet` and fetched from the applied keys, kept device-local at `.scratch/advi_cotbkf/cvo_open/` on dell2:
- `STMT_acct#6a7d29ca_2025-06-30.pdf`: 53,495 B, `%PDF-`, 19 page objects; key `.../doc_type=STMT/STMT20250704081541182579d5-e297-47e6-972c-a1895d2f8fa1_fbd264aa.pdf`
- `TXRP_acct#d0662be7_2025-02-09.pdf`: 25,223 B, `%PDF-`, 5 page objects; key `.../doc_type=TXRP/TXRP2025020908353833d06f49-219b-4854-8757-7f9d8b55cf1f_855303e8.pdf`
This seat could not render them (no poppler on dell2); reading their content is the grade.

## Rows filed since the round-5 packet

| row | class | standing |
|---|---|---|
| S13 | OBSERVATION | INERT -- corrects S12: the applies write `opal-data-assets` |
| S14 | OBSERVATION | INERT -- CB-e-3's guard aimed at the wrong bucket; FIXED by CB-f-1 |
| S15 | OBSERVATION | INERT -- W12-S2 answered (laptop listing of the two never-listed buckets); bears on re-grading CB4d1-AC3 |
| S16 | OBSERVATION | INERT -- DISARMS S9 (the applied links equal the laptop's) |
| S17 | OBSERVATION | INERT -- DISARMS W12-S1 (census on the covering calendar: 9,388,961 needed = round 2) |
| S18 | OBSERVATION | INERT -- DISARMS S12 (applies ran on the right bucket under pairs and closed ledgers) |

**ARMED rows of this seat on ADVI_COTBKF: 0.** Re-grades owed to the CVO: CB4d1-AC3 (census completeness, with S15 and the
`census_e2` re-run) and CB4d5-AC3 (above).
