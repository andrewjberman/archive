# IRPT_ANLREQ workstream T -- DRAFT: FWD-5 sitting 4 (the package half), COO side (issuer 2.0.0_SA_COO~T2, 2026-10-17)

**Status: DRAFT, NOT SIGNED, NOT FOR AN APPLIER.** Nothing here is run. It is written while the sitting is blocked (it needs FWD-1 window 5's packaged ticket, which `2.0.0_SA_COO~Y2` holds for the resident r34k and runs Monday to Friday 00:00Z-13:00Z only) so that the cut is fast once the ticket exists. Every "to measure" line below is read at the pin before the packet is signed. Authority: CTO msgs 10096 and 10104, CVO `ADJUDICATION_v26` and `v27`. Claim levels: *measured* = read from a named file; *held* = a ruling; *to measure* = read at the pin.

## 1. What the sitting must show (held: CTO 10096, 10104; CVO v27)

FWD-5 ACCEPT: "someone signed in for a different firm is refused the ticket and every file in its package; a statement that it is refused does not count". Sitting 3 refused firm B on all 26 made calls but could not serve any control the packaged files. Sitting 4 therefore targets window 5's PACKAGED request and adds, in the SAME sitting:

1. an identity the OWNER RULE admits is SERVED each packaged file (`original-upload`, `report-pdf`, `commentary-pdf`);
2. working controls with REAL ids (no stand-ins) on `request-history`, `narrative` and the no-selection call;
3. `GET /api/scoped/tickets/metrics`.

The write routes (claim, complete, report, package, commentary-draft, commentary-sent, meeting) are OUTSIDE FWD-5's DONE WHEN ("tries the ticket and each package file") and are not owed (CTO 10104); this draft says so, and the meeting POST stays proved offline by `test_cross_firm_meeting_scope.py`.

## 2. The identities (measured from `R59_FWD5_OWNER_RULE_READING_20261017.md`, dc14046fde)

The owner rule (`_scope/owner_reads.py:26-34`, `_scope/interactive_access.py:101-121`): the retained owner's `firm_id` must equal the tenant for EVERY caller; then an `OPAL_GLOBAL` caller is admitted, otherwise the caller must be the owner (same firm and `principal_id`). Three principals, each minted for the sitting only and removed after:

- **Firm B** (`fwd5-cottonwood-r60`, firm `cottonwood`, `allowedFirmIds` [cottonwood]): the refused side, as before.
- **The staff control** (`fwd5-control-r60`, firm `opal-capital`, `allowedFirmIds` [49financial]): admitted by the `OPAL_GLOBAL` clause on a request whose retained owner has `firm_id` = tenant. It serves `ticket-read`, `ticket-list`, `tickets-metrics`, the file routes, `request-read` and `job-status` (the third sitting's synthetic target is the evidence of this clause).
- **The owner control** (to design with `2.0.0_SA_COO~Y2`'s window-5 owner: the synthetic advisor of firm `49financial`, a partner profile plus an active user, minted and removed): a caller whose OWN firm is `49financial` and whose `principal_id` is the retained owner's. Needed because two controls read `UNEXPECTED` for the staff control in sitting 3 (`request-history` and the no-selection call; row filed) and because the no-selection call anchors the bucket on the caller's own firm: only a `49financial` caller can read a `49financial` request without a `selected_tenant`. Whether the staff control already reads those two routes is to measure (the cause of `UNEXPECTED` is unread).

## 3. The routes and the real ids (measured: the merged driver, AR-tz-76, blob 3746dc3354)

14 made calls and 2 EXCLUDED rows per driver run: `ticket-read`, `ticket-list`, `tickets-metrics`, `form-as-filled`, `original-upload`, `opal-report`, `report-pdf`, `commentary-pdf`, `request-read`, `request-history`, `job-status`, `narrative` (takes `--report-id`), `export-receipt` (takes `--export-id`), `request-read-no-selection`. A run without `--report-id` or `--export-id` leaves those two routes UNREACHED. To measure at the pin, read-only and names/ids only: window 5's ticket id, request id, job id, the report id and the export id (or the statement that no export exists, in which case `export-receipt` is reported PAST-FENCE with the control's NOT_FOUND, named as such); the retained owner's `firm_id` equals the tenant; the package keys `original_ref`, `pdf_ref`, `commentary_ref` are present.

## 4. Grading (proposed for `r56_checks.py` v4, to be built when the ids exist)

Per route, the fence is SHOWN iff a working control read ALLOWED (a 2xx `ok` true or a served body) and firm B read REFUSED. Required SHOWN: `ticket-read`, `ticket-list`, `tickets-metrics`, the three file routes, `request-read`, `request-history`, `job-status`, `narrative`, and the no-selection call (the owner control). `form-as-filled` and `export-receipt` may be PAST-FENCE with a stated reason (no form; no export). A control refused by `FIRM_BINDING` or `NOT_AUTHORIZED` on a route, or answering `UNEXPECTED`, is a BROKEN control there and grades nothing (CTO RE-SIGN 4); the sitting says which route. Firm B must read REFUSED on all 14 (exit 0), 0 LEAK.

## 5. Order of the sitting and blast radius (as sittings 2-3, plus one principal)

Mint three principals (readback prints scope and entitlement rows); for the window-5 target run the staff control, the owner control, then firm B (each control exit 0 first); remove all three; two users rows become three, GET-only requests, no write to any ticket, request or job, 5174 reused and never started or stopped. Applier: `0.7.0_AE_CloudOps~IB2`. A LEAK stops the sitting with all principals removed first.

## 6. Not decided here

The owner control's mint (a second helper mode or Y2's own mint for the synthetic advisor) and its credential handling are Y2's design and the CTO's call; this draft only names the need. No sitting is cut before window 5 (CTO 10096).
