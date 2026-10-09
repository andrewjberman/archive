# NFRA_OPSWKF -- Andrew-direct 2026-10-09 ~05:0xZ: trade intake through the Ticket Center; fit read

**Author:** `2.0.0_SA_COO~O2` (dell2). **For:** `1.0.0_SA_CTO~DELL2`, a PRD addendum (FWD-1's shape changes).

## 1. Andrew's words (verbatim, in session at the 2.0.0_SA_COO~O2 terminal)

> Check my MS Teams chat with Menachem Goldstein. We are going to talk in two weeks but he made a little list of some
> things he'd want which i think we can go get a head start on now. I think these things really can be handled in
> MCPINDEX on the sitez box as far as how claude gets the data in question. Your work is more likely going to focus on
> how to set this up in the ticket center, focused on how trade requests can be submitted there with a custom shape,
> potentially using the trade submission engine even if trade submission portal page is not surfaced to the advisor
> themselves.

## 2. The operations lead's list (Teams 1:1, Menachem Goldstein, 2026-10-07T22:36Z, read via the gateway)

Billing; Trade rec; Post model update rec; High cash account alert FA; Assets transfer alert FA; Restricted account
alert FA. He offered a sitting "after billing cycle (two weeks from now)" (2026-10-08T13:55Z).

Placement per Andrew: how Claude gets the data for these -> NFRA_MCPINDEX (site Z). None of the six is trade-request
intake. The three FA alerts are NOT ordered as alerts here (moratorium; Andrew's word not yet given -- asked in session).

## 3. Fit read (read-only; every claim cited at the bytes; Explore pass, the C-NO-SEND item re-printed by this seat)

| Piece | Exists | Cite |
|---|---|---|
| `trade_request` ticket type, no questions yet | yes | `infra/aws/lambda/ticket_center/lambda_function.py:79` |
| Type-driven questions + generic answer validation | yes | `lambda_function.py:78-112`, `:643-689` |
| Routing trade_request -> menachem@ primary | yes | `infra/aws/terraform/ticket-center/main.tf:316-320` |
| `linked_submission_id` on a ticket (unvalidated) | yes | `lambda_function.py:559`, `:1131`; `portal/src/api/endpoints/tickets.ts:91-103` |
| Client `/submit` accepts type/title/description only | limit | `lambda_function.py:134-148`, `:1047-1050` |
| TicketCenter page internal-only, form not schema-driven | limit | `portal/src/App.tsx:500-506`; `portal/src/lib/firmAccess.ts:104-113`; `TicketCenter.tsx:219-229` |
| Engine submit route, callable without the page | yes | `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf:343-350`; `submission_handler.py:96` |
| Engine initiator taken from BODY, not token | gap | `trade-submission-handler/src/submission_handler.py:117` |
| Engine statuses PENDING_APPROVAL/APPROVED/REJECTED/EXECUTED; append-only audit_events | yes | `trade-workflow-handler/src/config.py:46-50`; `submission_handler.py:164-173` |
| Ticket <- engine status write-back | absent | no trade-pipeline code names a ticket |
| **Execute emails a brokerage** | yes | `workflow_handler.py:357-410` (send at `:409`) |

**C-NO-SEND finding.** `trade-workflow-handler/src/config.py:24-29`: every `BROKERAGE_EMAILS` list is andrew@ +
menachem@ today; the real broker addresses (Schwab, Fidelity, IBKR, Vident) sit in comments awaiting SES production
access. A ticket-originated trade must never reach that Execute send, or the fence must be explicit in the addendum.

## 4. Smallest path (proposal for the addendum; the CTO rules)

1. Questions on `trade_request` (fund, securities list or upload, weights date, attestations); likely one new answer kind.
2. Advisor intake: `/submit` accepts `answers` for `trade_request`, firm-scoped server-side.
3. Bridge: create/claim -> `trades/submit` with identity from the token; write `submission_id` to `linked_submission_id`.
4. Status write-back: engine transitions append to the ticket's `events[]` and move its status.
5. Execute fence for ticket-originated trades.

**Write-surface collision:** TCKT_VNEXT (`2.0.0_SA_COO~V2`, rounds live on dell2) writes `lambda_function.py`,
ticket-center `main.tf`, `TicketCenter.tsx`, `tickets.ts`. The shared edit is held to the one `TYPE_DEFINITIONS` entry;
new code goes in new files (a `TradeRequestParts.tsx`, a bridge module).

## 5. Ask of the CTO

A PRD addendum re-shaping FWD-1 from "row in his SharePoint workbook" to "trade-request ticket in the Ticket Center,
bridged to the trade engine, status back on the ticket", with the C-NO-SEND fence named, and a ruling on whether the
SharePoint workbook leg stays in FWD-1 or moves to the enrichment list.

-- 2.0.0_SA_COO~O2
