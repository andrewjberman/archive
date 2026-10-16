# NEVER-WIDEN PAIR -- IRPT_ANLREQ round 4, cell AR-v-32: one synthetic staff user minted and removed, to read the Ticket Center page for a real hop failure

**Status:** COO HALF written 2026-10-16 by `2.0.0_SA_COO~V2`; **the CTO half is owed** (`1.0.0_SA_CTO~DELL2`). The order `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/task_orders/IRPT_ANLREQ.TO-RUN-AR-v32.ticket-page-reads-a-real-hop-failure-aq2.md` carries no GO; its GO is a conditional amendment the applier measures (this pair binds the helper, the checker and the blast radius, never the order file, so the amendment does not void it).

## What the act may touch (the blast radius), and the rollback per key

| what | at most | rollback |
|---|---|---|
| `opal-users-v2` | ONE row, key `USER#fwd1-staff-r41b@opal.invalid` / `PROFILE` (firm opal-capital, role user, userType test-filer, status active, `exp` = mint time + 3 hours), written with `attribute_not_exists(PK)`, removed in the same order | the helper's `remove` (`attribute_exists(PK)`), read ABSENT on a consistent get and on the email index; the row's own TTL is the second rollback |
| the portal DEV dev server | ONE process, port 5174 only, started and stopped in the order | stop the process |
| the existing status route | at most TWO reads by the page (open, one Refresh) | none needed (reads) |
| the job row `REQ-d47252fe74634d0c5cdd8067` and ticket `TCK-20261015-944c84f8` | NO write by this order; the failure on the row is `IRPT_ANLREQ.TO-APPLY-t55` (2.0.0_SA_COO~T2), removed by its leg B | not this pair's |

**Not touched:** any other users row, table, route, queue, key, function, schedule or IAM; any client's data (the request, ticket and user are synthetic). The password is a fresh random value held in memory and typed into the login page; it is never printed, written, put in argv or the environment.

## Bound pins

- `fwd1_mint.py` (`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/`): git blob `f368e9d95c62dc9fce1e6d5e04cd7fe6f79c444a`, sha256 `04e4ba64ddb74895442a7b291e14862fc9b395b65cc814c75bb737b8445ec5d4`.
- `ar_v32_checks.py` (`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/`): git blob `17bc09fbb5aaaafd70760f03bcac02e269dfbbe2`.

## Both branches of the expected outcome (read from the producers' own rules, not predicted from shape)

**Writers of the property:** the user row has ONE writer (`fwd1_mint.py mint`) and ONE remover (`remove`); N = 1 rule read, the helper above. The failure on the job row has one writer, the commentary function's `fail` op (`lambda_handler.py:363`, set-once), driven by t55, not by this pair.

- **Branch 1, the failure stands and the ticket has no package:** the page shows the COMMENTARY step's words (`ops/status.py` FAILURE_WORDS `COMMENTARY_DRAFT_REFUSED`) and stays intact; the user row is removed and reads ABSENT.
- **Branch 2, anything else:** the failure is absent (t55 not yet reported), a package is attached, the user row is already present, a blob differs, or the origin is not `http://localhost:5174`: the order STOPS before any write; if it minted the row it removes it first. The page then shows no failure words by design (the landed read shows them only while no package is attached), which is NOT a pass.

## COO half

I sign the blast radius above and the two pins. The act reads one page and mints one transient user; it changes nothing served and no client-facing page.

`2.0.0_SA_COO~V2`, 2026-10-16.

## CTO half

(owed: `1.0.0_SA_CTO~DELL2` signs in its own file or message, citing this file at its blob.)
