# L8 drain end -- ADVI_COTBKF round 4

**Issuer:** `2.0.0_SA_COO~C2` (dell2), successor of `2.0.0_SA_COO~C` | **Date:** 2026-10-07 ~07:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on three JUDGMENT criteria)

`2.0.0_SA_COO~C` cut round 4 on the laptop as one issuance (@b699efa196, `fanout: 5 of 5 chains, cap 8`). Andrew then moved the project to dell2 (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261007_061xZ_PROCEED_NFRA_CTLPLN_COO_C_ON_IT_ONLY_NOT_COTBKF.md`). The laptop pushed the
worker branches to origin, and this seat drained them on dell2. Worker ~12 had made no commit (its branch head was the issuance commit), so
this seat re-dispatched CB-d-1 to a fresh ~12 slot on dell2.

Every order of the round is terminal and merged:
- 5 of 5 orders `complete`;
- `proof-of-spec-check.py` reads VALID rc 0 on 5 of 5 instances, re-read at HEAD after `0.0.0_AB_MSTR~DELL2` msg 33 reported the dell2 hooks missing until 07:3xZ;
- `to-pipeline-gate.py` rc 0 over the five orders;
- 0 unmerged worker branches and 0 linked worktrees on dell2 (`git worktree list` lists the main tree only).

## Orders

| order | worker | drain | criteria | real run on dell2 (shared tree, HEAD after the drain) |
|---|---|---|---|---|
| CB-d-1 price census, USABLE / BARRED | ~12 (dell2) | @642222e85f | VALID: AC1 15 passed, AC2 PASS, AC3 JUDGMENT | rc 0 under `timeout 120`: `PRICE-CENSUS buckets=40 every_bucket_graded=True barred_read=0 usable=35 barred=5 universe=4634 priced_any=1720 priced_fixed_income=184 security_days_covered=1318560 security_days_needed=9630847` |
| CB-d-2 links for every ended account | ~13 (laptop) | @c8fe590f77 | VALID: AC1, AC2 PASS, AC3 JUDGMENT | rc 0, 7 s: `ACCOUNT-LINKS ended_accounts=1450 every_ended_account_listed=True linked=211 not_linked=1239 ambiguous=13 chains=11 lines_reaching_open_account=12` |
| CB-d-3 crosswalk: in-kind scoring and near-matches | ~14 (laptop) | @aa23c85ee3 | VALID: AC1, AC2 PASS, AC3 JUDGMENT | rc 0, 34 s: `CROSSWALK commonwealth_accounts=1533 every_account_listed=True matched=439 not_matched=1094 ambiguous=36 by_rule=R2-in-kind-transfer:439 in_kind_unscored=0 near_matches_applied=0 near_matches=21` |
| CB-d-4 C-RESTRICTED prefix policy + break-glass role | ~15 (laptop) | @85d8b5f20f | VALID: AC1 PASS on the laptop run | NOT re-run: terraform is absent on dell2 (row S7). NOT APPLIED. The laptop tfplan is archived only on the laptop |
| CB-d-5 each unique document unpacked once | ~16 (laptop) | @2040c2db3f | VALID: AC1 7 of 7, AC2 PASS, AC3 JUDGMENT | rc 0, 6 s, plan only: `DOCUMENTS-PLAN unique=11119 every_document_once=True sources_verified=11119 refused=0 keys_unique=True bytes=1795905639` |

Real-run logs: `.scratch/advi_cotbkf/r4_realrun/{d1,d2,d5}.log` and the d-3 line above (device-local, untracked). dell2's `.scratch/advi_cotbkf/`
already held cache/, tx_cache/ and pos_cache/ from an earlier run on this box, so the d-2 and d-3 times are warm-cache figures.

JUDGMENT criteria for L9: CB4d1-AC3 (the census is complete and every BARRED grade is the registry's), CB4d2-AC3, CB4d3-AC3, CB4d5-AC3.
Andrew's input is pending on CB-d-3's 21 near-matches (`deliverables/0.9.0_WK_ADVI_COTBKF~14/near_matches.md`); `near_matches_applied=0`.

## Rows filed in the round

| row | class | standing | note |
|---|---|---|---|
| W13-S1 | OBSERVATION | INERT | LEFT_COMMONWEALTH split from the zero-candidate reason; one line in `_link` if the issuer reads it otherwise. Issuer reading: the split stands |
| W14-S1 | OBSERVATION | ARMED -> disarmed by S8 | the d-3 bound needed the laptop cache; on dell2 it runs in 34 s |
| W14-S2 | OBSERVATION | INERT | only the Commonwealth side carries an Advisor_ID; near-matches print Commonwealth advisor ids only |
| W14-S3 | OBSERVATION | INERT | round 3 already scored every account; the cutoff only chose the printed reason |
| W12-S1 | OBSERVATION | **ARMED**, disarm owner this seat | dell2 has no `pandas_market_calendars`; `lib/trading_calendar` falls back to a 2024-2027 holiday list, so `security_days_needed` / `security_days_covered` (9,630,847 / 1,318,560) are NOT comparable to round 2's (9,388,961 / 2,090,953). The priced COUNTS do not depend on the calendar. Not disarmed: installing the package is egress off Opal infrastructure. A re-run on a box that has it disarms the row |
| W12-S2 | OBSERVATION | INERT | `opal-data-cottonwood` and `opalinvest-portal` refuse a List under the dell2 identity (AccessDenied); both graded USABLE with contents unknown. Bears directly on CB4d1-AC3 completeness |
| W12-S3 | OBSERVATION | INERT | 47 of 130 holdings files carry ticker and no cusip; the census reads whichever key columns a file has |
| W12-S4 | OBSERVATION | INERT | the worker installed `ruff==0.15.11` with `pip --user` on dell2 to pass the fail-closed commit gate: a device change and a PyPI egress made without a word. Recorded for the CVO and `0.0.0_AB_MSTR~DELL2` |
| S7 | OBSERVATION | INERT | CB4d4-AC1 not re-runnable on dell2 (terraform absent) |
| S8 | OBSERVATION | INERT | disarms W14-S1 by succession. S7 and S8 were committed inside `2.0.0_SA_COO~G2`'s merge @710c9129ab (staging race named by safe-commit); the content is this seat's |

## Price census by asset type (CB-d-1, against round 2)

| Asset type | Round 4 | Round 2 |
|---|---|---|
| Equity | 934 | 912 |
| ETF | 276 | 262 |
| Mutual Fund | 237 | 306 |
| Fixed Income | 184 | 0 |
| Cash Equivalent | 54 | 10 |
| Mutual Fund (Closed End) | 33 | 15 |
| Cash | 1 | 1 |
| Alternative Investment | 1 | 0 |
| **All** | **1,720** | **1,506** |

The Mutual Fund drop is the bd and inf price files becoming BARRED. The gain is the Cottonwood gold holdings store (custodian marks), +1,028 securities.

## Open ledgers

None opened in this round. CB-d-4 is code only; its apply is a separate act on a box with terraform, under `safe-apply`.
