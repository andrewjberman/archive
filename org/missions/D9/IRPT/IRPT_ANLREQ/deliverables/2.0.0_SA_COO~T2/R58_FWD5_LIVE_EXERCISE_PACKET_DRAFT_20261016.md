# IRPT_ANLREQ workstream T -- DRAFT packet, COO half: the FWD-5 live cross-firm exercise (mint, drive, remove)

**Status: DRAFT, NOT SIGNED, NOT FOR AN APPLIER.** Author `2.0.0_SA_COO~T2`, 2026-10-16 ~16:4xZ. Claim levels: *measured* = read from a named file; *held* = a message or ruling; *to measure* = read at the pin before signing. It becomes the packet when (a) `2.0.0_SA_COO~V2` messages that `TCKT_VNEXT.TO-R18-REL` (the combined R18/R19 release) has read back, and (b) every "to measure" line below is read and filled. Amending it voids a signed CTO half (re-sign on the new blob). Nothing here is run.

## 1. What the act is

Authority (held): CTO Move 2 (msg 8742): FWD-5's DONE WHEN is a seat-driven exercise; the cross-firm tests (AR-tz-61..64) and the driver exist; the run follows V2's release. Row `IRPT_ANLREQ-D2-S134` stays ARMED until this run reads back.

Three steps, one actor (the single IRPT CloudOps lane under rule 34; the lane is named by the CTO, `0.7.0_AE_CloudOps~AQ2` while it holds the macro), on portal DEV only:

1. **Mint** one scoped second-firm principal: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~219/fwd5_driver/fwd5_mint.py mint --email <name>@opal.invalid --firm <firm B> --allowed-firm-ids <firm B>` (measured header: one users row in `opal-users-v2`, conditional write, bcrypt cost 12, password read from stdin as one JSON object, TTL 3 hours, output only `MINT-OK READBACK-OK` / `MINT-REFUSED <word>`). The address is not the FWD-1 helper's (`fwd1-staff-r41b@opal.invalid`).
2. **Drive** `.../0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py --base <DEV origin> --email <that address> --ticket <firm A ticket> --firm-a <firm A> --firm-b <firm B> --request-id <firm A request> --job-id <firm A job> --out <applier deliverables dir> --go IRPT_ANLREQ.TO-RUN-FWD5.<id>` (measured header: signs in, makes each listed call for ONE ticket of the OTHER firm, verdicts REFUSED / LEAK / UNREACHED / EXCLUDED; exit 0 only if every made call is REFUSED; report `fwd5_run_report.json` holds no body, cookie, token, password or address).
3. **Remove** the principal: `fwd5_mint.py remove --email <that address>`; read `ABSENT GSI` and `ABSENT CONSISTENT`.

## 2. To measure before signing

- V2's readback message for TO-R18-REL (code and env released; the ticket service carries the fence); the DEV origin the driver is aimed at (the ticket service's address, not a client page).
- Firm A and firm B: two real firms on DEV, one ticket, request and job of firm A that already exist (no creation by this act). Which firm is B, and that the principal's `allowedFirmIds` is B only.
- The password source: one stdin object supplied by the applier from its own session; nothing typed into a file or the order.
- The N writers of the `opal-users-v2` row for this email: one (the mint); the remove is the only delete.
- A dry run of `fwd5_driver.py --plan` and `--selftest` at the pin (offline; both must exit 0), and `test_fwd5_driver_offline.py` plus the exit-semantics test green at the pin.

## 3. Expected outcomes (both branches)

- All made calls REFUSED, exit 0: FWD-5's seat-driven exercise is graded OK; S134 disarms via its `disarm_owner`.
- Any LEAK (exit 1): STOP at once, remove the principal first, report the route name only (never a body); the release is the defect and goes to V2 and the CTO. Any UNREACHED (exit 2): not a pass; report which call, remove the principal, no retry without the issuer's order.

## 4. Blast radius and rollback

One users row on DEV (self-expiring at 3 hours, removed by step 3); GET calls to one ticket service on DEV; no write to any ticket, request or job; no S3 key, no schedule, no Terraform, no Lambda code. Rollback = step 3, and the row's TTL if the applier is interrupted. A NEVER-2 ledger entry opens at start and closes at step 3; the order's `<paths>` name the deliverables folder, the ledger and the sentinel.

## 5. Who

Pair: this COO half; the CTO half (`1.0.0_SA_CTO~DELL2`) signs the blob. Applier: the IRPT CloudOps lane under an order cut only after the signed half and V2's readback. No order is cut from this draft.
