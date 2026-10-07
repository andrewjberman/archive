# IRPT_DASHBD TO-DB-b-37 -- the activity identity re-graded after the three fixes (counts only)

Worker 0.9.0_WK_IRPT_DASHBD~21, round 24 workstream B, cell DB-b-37. The fixes are in `account_activity_lots.py` (with 8 new tests,
31 passing in all); `account_return_daily.py` and every served producer were imported read-only and not edited; S3 was read, never
written. The evidence is `IDENTITY_REGRADE_E2.json` beside this file; `identity_regrade_e2.py` regenerates it. No client figure,
balance or account number is quoted here.

## The fixes (amendment 1)

- Dropped conditional rows. Every call into the served flow rule runs under `served_runtime()` (pandas' `future.infer_string` off,
  the served layer's behaviour; this box carries pandas 3.0.6). 2,603 of 2,603 CONDITIONAL-BY-COUNTERPARTY rows over 24 flow days
  resolve; unresolved 0. The flow cache refuses to classify a day outside the runtime.
- In-kind transfers. 14 in-kind legs over the window: 13 the served flow already admits, 1 (an INTERNAL adjusting entry) it does not
  and the producer now counts as a withdrawal at value. 10 arrivals match their new lots, 4 departures match the lots that left
  (3 on the leg's day, 1 on the next trading day), 7 re-lots by the custodian keep the transfer-date reference. Lots measured from
  that reference carry `basis_source` IN_KIND_TRANSFER_VALUE; the custodian's basis sits beside it in `custodian_cost_basis`.
- Unmapped value movers. Of the 10 types, 8 reach the flow (the conditional cash and in-kind types) and 2 reach income as negative
  components shown beside it: 1 fee-admin row and 1 withheld-tax row.

## The re-grade, same 91 accounts and window

| | round 23 | E2 |
|---|---|---|
| graded | 91 | 91 |
| within one cent (passed) | 52 | 55 |
| above one cent (failed) | 39 | 36 |

- The 36 failures by class: ROUNDING 32 (gap within 0.05), MISSING-TERM 3 (a lot basis above the cash paid; unchanged from DB-b-36),
  OTHER 1 (one in-kind account: a lot table that trails the balance by a trading day, which nets to zero over two days, and a day on
  which the custodian re-selects the lots relieved by the departure before; row W21-S4).
- Against DB-b-36's 9 MISSING-TERM windows: 3 now pass, 2 are now ROUNDING-sized, 1 changed class to OTHER with a far smaller gap,
  3 are unchanged. No gap was plugged: the OTHER window keeps its gap, and its two lagged days keep GAP_ABOVE_ALLOWANCE.
- A sale of under one share in all (one security, one day) could not be linked to one lot of the prior day and was left on the
  custodian's figure.

## The exercise window (FWD-4)

- Chosen from the 91 accounts: of the 55 windows that tie, 3 carry a non-zero realized gain and a non-zero contribution or withdrawal;
  the one with the largest sum of the three terms is named. It is an account opened inside the window by in-kind transfers: 13 of 13
  graded days MEASURED, the window ties within one cent, and all of contributions, withdrawals, realized, unrealized change and
  income are non-zero (beginning value is zero because the account opened inside the window). The other 2 qualifying windows are in
  the JSON beside it, with beginning values that are non-zero.
- Terms, flows and the identity are printed term by term in the JSON, with the unrealized change split into lots and in-kind
  departure gain.

## Controls

- The reproduced flow cache returns a tuple equal to the served `FlowCache.get` on 3 of 3 sampled days.
- The same served call on pandas' default string behaviour differs on the conditional-bearing days: 2 of 2 sampled.
- The re-derivation of the served in-kind value agrees with the served census on every flow day that carries an in-kind leg
  (0 disagreements).
