# Ticket Center on PROD: Trade Request and Meeting Request, measured state (2.0.0_SA_COO~V2, 2026-10-19 19:40Z)

Asked by the CTO (msg 10900, Andrew's dell2 priority order). Base: origin/PROD `8cd45f623bdf` (`git -C portal ls-remote origin refs/heads/PROD` read 19:37Z). Drain: 0 worker branches, 0 worktrees of this lane (five TCKT_VNEXT branches merged into box/dell2).

## Meeting Request -- WORKS on PROD (measured, exercised)
Run: TO-R20-PROD2 by 0.7.0_AE_CloudOps~TV2, 18:11Z to 18:29Z, https://opalinvest.dev, ticket TCK-20261019-c50b4967.
- Filer filed a Meeting Request; it showed "Waiting for the coordinator" (shot prod_filer_waiting).
- Coordinator, inside ONE routing window (open 18:16:24Z, closed 18:23:40Z), saw the proposed times and "Confirm this time" and confirmed one (shot prod_coordinator_controls).
- Filer reloaded and read "Confirmed for 2026-10-26 14:00 ET ... by tckt-r20-pcoord-20261019@opal.invalid" (shot prod_filer_confirmed).
- Routing restored: meeting_request.primary = jeanette@opalinvest.com alone, read back. Ticket and both synthetic rows deleted 18:29:30Z, ABSENT. Two protected tickets present.
- My re-run of `r20_prodjourney_check_v2.py` (blob 9ff30a5d38, the signed blob): self-test R20-PRODJOURNEY-SELFTEST-OK, live check RUN-OK (prodjourney). I read all three shots.
- Contrast of the confirmed line, my own measurement from the PNG: 10.10:1 (ink 209,212,217 on 25,38,67; matches TV2's 10.1). Gate 4.5.
- Not claimed: AC2J (the judgment half) is the CVO's to grade; email delivery (WE_DL_UNCONFIGURED reads as designed); Meeting flow for a real coordinator address.

## Trade Request -- REACHABLE on PROD, NOT exercised end to end
- MEASURED: the New Ticket type list on PROD lists Trade Request (the run's recorded type options: Trade Request, Service Request, Meeting Request, Other, Analysis Request). TicketCenter.tsx at 8cd45f62 no longer filters trade_request and imports TradeFormOpen from ./TradeRequestParts.
- MEASURED (scratch trial on a PROD base, before the release): trade and meeting tests 45/0, Ticket Center folder 221/0, tsc OK. DEV commit c05e3dda is titled "Trade Request as a form upload; engine submit unwired".
- MEASURED (reads only, route not called): POST /api/scoped/tickets/attachment-upload exists, AWS_PROXY to opal-ticket-api, both attach env values set, role policy opal-ticket-attachments-trade-form-policy attached.
- NOT MEASURED: no Trade Request ticket was filed on PROD; the upload was never called; the S3 policy's resource list against the bucket and prefix was not read; "engine submit unwired" means a filed trade ticket reaches the ticket store but triggers no trade engine call.
- To close the gap: one synthetic Trade Request filed with one small attachment on PROD under the same window discipline, by CloudOps. NO such order is cut (Andrew's pause: no new cell, order or round).

## Open
- CVO grade of R20PROD2-AC2J; L8 part 5; then the L10 slug (after every order of the round is terminal and every row dispositioned).
- FWD-11 on PROD (due 2026-10-24) is now exercised for Meeting; Trade is the remaining half.
