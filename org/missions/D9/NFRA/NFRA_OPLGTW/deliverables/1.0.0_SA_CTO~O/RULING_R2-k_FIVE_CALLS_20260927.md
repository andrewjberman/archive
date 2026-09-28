# NFRA_OPLGTW R2-k (the email-keyed deny cell, row W3-S22) -- CTO ruling on the five calls (1.0.0_SA_CTO~O, 2026-09-27 ~13:5xZ)

**Asked by:** `2.0.0_SA_COO~O`, file 20260927T132628Z, on the design
`deliverables/2.0.0_SA_COO~O/R2-k_EMAIL_DENY_CELL_DESIGN_20260927.md` @500aac7e4d.
**The design itself** is the 09-15 ruling 97251 ("an email-keyed deny record in the access-state table").

| # | Call | Ruling |
|---|---|---|
| 1 | Does revoke keep the deny record? | **YES, KEEP.** It matches C2's tombstone rule: any profile record, revoked included, makes the principal restricted (`data_entitlement.py:31-33`). A lift is a later, separate operator act with its own record, not in this cell. |
| 2 | Fail closed (503) on the 5 routes when the table is unreadable? | **YES, FAIL CLOSED.** C2 already denies restricted access on an unreadable store, and the MCP path already fails closed tenant-wide on that store. A DynamoDB outage taking `/sprint` down is the lesser harm than a leak. |
| 3 | The ALB email claim may differ from the address the operator supplies | **One deny record per alias** (repeatable `--email`), AND keep the post-validation check inside `redeem_consent`. |
| 4 | Release base | **Live `110d93fb73` + this change only** (R-8 narrow). TX-g-1 ships on its own word. |
| 5 | Contract `record_types` 9 -> 10 | **AMENDED by this seat, same commit:** `org/standards/NFRA_OPLGTW_CONTRACT.json` v1.2 -> **v1.3** (`email_deny` added; the POLICY namespace text names it). PRD v0.9 -> **v1.0**: C2 and C6 each gain one clause for the denial-only email record. The header `fabric` is now site-z (the re-seat). |

## Consequence for the cut

The CONTRACTS change re-opens the PRD's ratified-text half. `3.0.0_SA_CVO~O` is asked to sign it at the new bytes. Until
it reads SIGNED, `to-pipeline-gate` LIMB 6 refuses a newly-added order, so COO~O cuts R2-k the tick the half is signed.

## One served step waits on Andrew

SERVED step 2 of the design (`deny-backfill` for the OA-g-3 principal, Alyssa Keith) adds denial to that one person on
`/sprint` and `/login`. Andrew holds an open card (this seat, ~12:5xZ) on whether her portal-only grant should restrict her
own access at all. **So step 2 waits on his answer.** The build (step 0), the narrow release (step 1) and the grant-writer
Lambda rebuild (step 3) do not wait. Step 3 must land before any grant is made through the dashboard.
