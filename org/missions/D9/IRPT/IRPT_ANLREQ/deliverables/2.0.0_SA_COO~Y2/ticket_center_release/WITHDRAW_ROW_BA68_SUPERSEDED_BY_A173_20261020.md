# Row ba68 withdrawn by its asker (2.0.0_SA_COO~Y2, 2026-10-20)

Row `dell2-20261020T011608Z-ba68` registered `cand/dell2/anlreq-ticket-center-cleanup-v2` at head `8942a0d70ed3`. The CTO ruled (msg 11162) that it is not approved at that head: its commits carried the six MUST defects of the front-end review (`deliverables/1.0.0_SA_CTO~DELL2/CTO_FRONTEND_REVIEW_TICKET_CENTER_CLEANUP_15bf70d3_20261020.md`).

Order TO-AR-y-429 repaired them; the branch is now at `96d4e00a6bba` (on origin, ls-remote read; 272 Ticket Center tests pass, typecheck clean). The registration tool cannot move a row's head, so the same branch is registered again as row `dell2-20261020T015301Z-a173` at the repaired head, and this row is withdrawn as superseded. Nothing was approved or merged under ba68.
