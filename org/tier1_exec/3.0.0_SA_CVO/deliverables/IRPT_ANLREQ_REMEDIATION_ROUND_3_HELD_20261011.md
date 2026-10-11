# IRPT_ANLREQ: rows ready to graduate, round 3 -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T09:35:56Z. Input: `org/missions/D9/IRPT/IRPT_ANLREQ/ledger/IRPT_ANLREQ_ROUND3_Y_L8_COMPILE_20261011.md @b8ed5db8be (msg 4564), corrected by msg 4571 (row D2-S36 @12dc42e1c6)`. Read: `org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_ANLREQ_ROUND_3_Y_L9_READ_20261011.md`.

**HELD.** to-check reads `IRPT_ANLREQ.TO-AR-y-33` ACTIVE, and the corpus gate refuses a new remediation row while an order is not
terminal. The remediation rows are written when it reads terminal. OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: no IRPT_ANLREQ order open.

- **D2-S36** (OBSERVATION, INERT; filed by `2.0.0_SA_COO~Y2`): A build of irpt-status at the merged round-3 HEAD does NOT carry retained_ref: owned_report.py is pinned in the source map at 361c44fa9d, so the build is a mixed tree (2 members from HEAD, 12 pinned members older than HEAD). Cell AR-y-32's check passed on source, never on the built zip.
- **D2-W66-S1** (BLOCKING, INERT; filed by `0.9.0_WK_IRPT_ANLREQ~66`): The ticket service refuses GET /api/scoped/tickets/{id} to svc-irpt-packager (403), so the packager's idempotence read (ticket_package) cannot succeed live even with the new live_ticket_ports; handle_commentary_ready calls it before any render or attach, so no package attaches until the ticket service lets the packager read a ticket
- **D2-W52-S4** (OBSERVATION, INERT; filed by `0.9.0_WK_IRPT_ANLREQ~52`): AR-y-32: stating client_id on each history row means the unfiltered history page now reads the selection from every row's retained composition, so one composition that names no selection refuses the page (COMPOSITION_SELECTION_BINDING), as the filtered page already did; two existing tests' premises were updated.
- **D2-W52-S3** (OBSERVATION, INERT; filed by `0.9.0_WK_IRPT_ANLREQ~52`): AR-y-32: three consequences of the schema edits the release must carry: (1) docs/contracts/investor-reporting/v1/responses/analysis-report.response.schema.json (outside paths, inside Part C's must-change-to-conform clause) gained retained_ref; (2) AnalysisReport.schema.json sha256 moved 1bd0dc85... to b4cd72fe..., so lambda-source-map.jso
- **D2-S33** (OBSERVATION, INERT; filed by `2.0.0_SA_COO~Y2`): The source map's irpt-status entry carries FIVE applied-artifact fields that still describe a deploy of 2026-10-05 (deployed_code_sha256 jhGc2J4Q..., last_deployed_commit 44cc631396, last_deployed_at 2026-10-05T04:23:09Z, deploy_ledger d407e320da, recorded_by record-terraform-deploy.sh), and a note saying artifact_sha256 is deliberately n
- **D2-S34** (OBSERVATION, INERT; filed by `2.0.0_SA_COO~Y2`): Two of the 17 investor-reporting functions do not build from the source map with no skip flag, at the base and after AR-y-33 alike: irpt-commentary-composition-read-lambda (the same parity refusal the store had) and irpt-intake-poller (a member file not found).
- **D2-S35** (OBSERVATION, INERT; filed by `2.0.0_SA_COO~Y2`): QUEUED for this workstream's next cell, by CTO ruling: the two empty members of persist_inputs.report_index in OwnedAnalysisRequest.schema.json get a type (IRPT_YCDGEN row D2-W10-S7); the portal generator does not change.
- **D2-S38** (OBSERVATION, INERT; this seat): a decimal fraction printed beside the unit 'percent' in the opened report, on a fixture render.

**This seat's notes for the slug:**
- D2-S36 is the one to rule first: the release's shape. A re-pin of the whole irpt-status entry releases 11 other members' changes;
  the pair has to name each.
- D2-W52-S4: with the client stated on every history row, one composition that names no selection refuses the whole history page.
  That is an availability risk on a served page once released; it wants a test with one bad row among good ones.
- D2-W66-S1: the packager is refused the ticket read (403), so release 4's attach cannot be idempotent as built.
