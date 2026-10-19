# Ticket Center, Analysis Request flow: state on PROD, 2026-10-19 ~20:4xZ (2.0.0_SA_COO~Y2)

Per Andrew's priority order (CTO msg 10899). Claim tags: M = measured by a read (source named), I = inferred, H = held from a seat's report, not re-read by me. PROD portal tip read 20:0xZ: `8cd45f623bdf`. Trade and Meeting Request are ~V2's page.

## What works on PROD
- **A staff Retry records the report.** Andrew's 13:42Z Retry on TCK-20261017-5af976ff wrote `report_ref` at 13:42:03Z with a string revision (M, ticket read-only; the portal fix is in the 8cd45f62 line). Nothing on that ticket was touched by me.
- **The upload door answers.** `irpt-ycharts-generate` ran for IB2's 5 posts at 14:30Z; the resident resolved at 0-13 s on normal runs (M, `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_resolve_live/A_RESOLVE_LIVE.txt`; CloudWatch times there are UTC-4).
- **A report is produced.** Andrew's request completed: run.json COMPLETE, 61-page PDF retained, 290,707 bytes (M, CRO gaps G7).

## What does not work (each has a fix in flight or ordered)
1. **A staff filing for 49 Financial is refused NOT_AUTHORIZED** at 16:38:54Z and 16:39:17Z: the advisor-email lookup finds no partner profile (`_authz/served.py:1109-1111`); a blank email is refused too (`:1089-1091`) (M, CRO G1, G9). Fix: PRD v0.24 O1+O2, not yet cut.
2. **The four attachments never reach the ticket unless commentary is on.** The packager runs only when `commentary_requested` is True (`resident_worker.py:254`); no package since 2026-10-10; Andrew's ticket holds 2 of 4 files that were never attached (M, G7). Fix: v0.24 O5.
3. **"Open report" shows about 427 element cards** (280 builder-only, 144 vendor-not-available, 3 with values) (M, G6). Fix built and merged (AR-y-404 `3676d5836b`, AR-y-408 `31c3dc1d4f`); NOT on the resident until r34l is installed (build running, order `org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-y-406.resident-release-r34l-build-only-two-movers.md`).
4. **The form gives up on a slow resolve.** It re-posts 5 times over about 15 s; two live resolves took 181 s (H, CTO msg 10782). Fix on DEV `10b6fd06fa89`; PROD promote in the DT's hands (`IRPT_ANLREQ.TO-PROMOTE-BACKOFF.portal-upload-resolving-backoff-dt.md`, stopped at a ledger sweep, ruling XA-1c61 relayed).
5. **The form asks for a report type, an advisor email and an "add commentary" box, and the models wait on a four-step chain** (M, G3, G4, G9, G10). Fix: v0.24 O2/O3/O4.
6. **The report link reached Andrew's ticket two days late** (accepted 2026-10-17 05:14:30Z; `report_ref` 2026-10-19 13:42Z) (M, G8).
7. **Irrecoverable request in the DLQ:** `irpt-generation` holds 8 dead messages, the oldest 11.8 days, including REQ-8966d24f (a Cottonwood staff request of 10-08, no ticket) (M, A_RESOLVE_LIVE R3). No redrive or closure proposal yet: the pause bars the cell.

## Not proven
- No clean staff filing with nothing seeded has run end to end on PROD after the fixes (run 4, under the CTO-signed ADDENDUM 4, follows r34l going live). Window 5 stays held (weekday 00:00Z-13:00Z only).

## Order of the remaining ships
Backoff promote (DT) -> r34l install (IB2) -> run 4 -> v0.24 issuance at the pause DONE line.
