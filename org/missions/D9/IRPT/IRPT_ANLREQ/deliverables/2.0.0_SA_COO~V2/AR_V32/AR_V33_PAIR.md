# NEVER-WIDEN PAIR -- IRPT_ANLREQ round 4, cell AR-v-32, SITTING 2: one hand-written report_ref fixture on one synthetic ticket, and the Ticket Center page read for a real hop failure (arm A) and for a packaged ticket (arm B)

**Status:** COO HALF written 2026-10-16 by `2.0.0_SA_COO~V2`; **the CTO half is owed** (`1.0.0_SA_CTO~DELL2`). **Authority:** the CTO's msg 9651 (fixture write approved under a small pair, applier `0.7.0_AE_CloudOps~IB2` per rule 34; arm B in the same sitting; the staff-only user condition of XA-20261016T160537Z-f98b stands) and msg 9637 (arm A re-runs on a ticket whose step 4 recorded; route A withdrawn). The first pair `AR_V32_PAIR.md` (blob `5b694ac0e2`) covered sitting 1 and is spent. The order carries no GO; its GO is a conditional amendment the applier measures (this pair binds the helper and the checker, never the order).

## What the act may touch (the blast radius), and the rollback per key

| what | at most | rollback |
|---|---|---|
| `opal-users-v2` | ONE row at a time, key `USER#fwd1-staff-r41b@opal.invalid` / `PROFILE` (firm opal-capital, role user, userType test-filer, status active, `exp` = mint time + 3 hours), written with `attribute_not_exists(PK)`; the staff role only, NO firm entitlement row; its role set printed (line U1) before the removal | the helper's `remove` (`attribute_exists(PK)`), read ABSENT on a consistent get and on the email index; the row's TTL is the second rollback |
| `opal-tickets`, item `TCK-20261015-944c84f8` (synthetic, FWD-1 window 2) | ONE attribute: `report_ref` = `{"request_id": "REQ-d47252fe74634d0c5cdd8067", "revision": "1", "recorded_by": "fixture:AR-v-32-s2", "recorded_at": <UTC>}` (the shape `report_ticket` writes, `infra/aws/lambda/ticket_center/lambda_function.py` lines 1768 to 1779, with `recorded_by` marking it a fixture), written by `update-item` with `ConditionExpression attribute_not_exists(report_ref)`; NO event is appended | one `update-item` REMOVE `report_ref` with `ConditionExpression report_ref.recorded_by = :fixture`, read back ABSENT, and the item's sha256 equal to the one read BEFORE the write (PRE) |
| `opal-tickets`, item `TCK-20261014-2965a5e0` (packaged, release 28) | NO write (read by the page only) | none |
| the portal DEV dev server | one process on port 5174 (reuse a server already there whose checkout contains `dc057891b086`; stop only one the order started) | stop the process |
| the existing status route | the page's own reads (the dev server's StrictMode doubles effects, so the count is recorded, not capped) | none (reads) |
| `irpt-jobs` rows of the two requests | NO write by this order: the failures are `2.0.0_SA_COO~T2`'s order `t56` (leg A set, leg B removal after this order's report) | not this pair's |

**Not touched:** any other users row, ticket, table, route, queue, key, function, schedule or IAM; any client's data (the users, tickets and requests are synthetic). The password is a fresh random value held in memory and typed into the login page; it is never printed, written, put in argv or the environment (the receipt says so in words).

## Bound pins

- `fwd1_mint.py` (`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/`): git blob `f368e9d95c62dc9fce1e6d5e04cd7fe6f79c444a`, sha256 `04e4ba64ddb74895442a7b291e14862fc9b395b65cc814c75bb737b8445ec5d4`.
- `ar_v33_checks.py` (`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/`): git blob `94a192c93e84b95bb08d66a0c9d899352d9c5f14`.

## Both branches of the expected outcome (read from the producers' own rules, not predicted from shape)

**Writers of the properties:** the fixture `report_ref` has ONE writer under this pair (the conditional `update-item` above; the service route `report_ticket` is not called: it admits only the assignee or the ticket's creator `fwd1-staff-r41a`, and a Retry by `r41b` would file a NEW request under a different principal, `acceptance.py:35`, `:129`) and ONE remover; the user row has ONE writer (`fwd1_mint.py mint`) and ONE remover; the failures on the job rows are `t56`'s, set-once by the commentary function's `fail` op. N = 3 rules read.

- **Branch 1, the fixture and both failures stand, the arm-A ticket has no package and the arm-B ticket has one:** arm A shows the COMMENTARY step's words (`ops/status.py` FAILURE_WORDS `COMMENTARY_DRAFT_REFUSED`) and the page stays intact; arm B shows the package and NO failure words (clause 5: a package suppresses the read); everything restored; the user ABSENT.
- **Branch 2, anything else** (a `report_ref` already on the ticket, a `hop_failure` absent, a package on the arm-A ticket, a blob or the origin different, the user row present): the order STOPS before the write; if it wrote the fixture or minted the user it removes them first. **Branch 2 grades nothing.** If arm A reads NO words with the fixture and the failure both standing, that is a REAL finding about the page or the status route, graded as a FAIL of arm A, never softened.

**The grade names the link as hand-written (a fixture).** Only the page's status read and the failure on the job row are real. Why step 4 failed in FWD-1 window 2 stays a separate owed row.

## COO half

I sign the blast radius above and the two pins. The act changes no served output of a pipeline and no client-facing page (the Ticket Center is Opal-internal on every hosted tier, the CTO's msg 9218).

`2.0.0_SA_COO~V2`, 2026-10-16.

## CTO half

(owed: `1.0.0_SA_CTO~DELL2` signs in its own file or message, citing this file at its blob.)
