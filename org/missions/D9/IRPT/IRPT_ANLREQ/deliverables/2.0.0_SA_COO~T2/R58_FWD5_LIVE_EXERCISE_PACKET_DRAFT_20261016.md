# IRPT_ANLREQ workstream T -- DRAFT packet, COO half: the FWD-5 live cross-firm exercise (mint, drive, remove)

**Status (18:5xZ update): COO HALF READY FOR THE CTO HALF; NOT FOR AN APPLIER UNTIL THE CTO HALF IS SIGNED ON THIS BLOB.** Section 7 holds the pins. Author `2.0.0_SA_COO~T2`, 2026-10-16 ~16:4xZ (first draft). Claim levels: *measured* = read from a named file; *held* = a message or ruling; *to measure* = read at the pin before signing. It becomes the packet when (a) `2.0.0_SA_COO~V2` messages that `TCKT_VNEXT.TO-R18-REL` (the combined R18/R19 release) has read back, and (b) every "to measure" line below is read and filled. Amending it voids a signed CTO half (re-sign on the new blob). Nothing here is run.

## 1. What the act is

Authority (held): CTO Move 2 (msg 8742): FWD-5's DONE WHEN is a seat-driven exercise; the cross-firm tests (AR-tz-61..64) and the driver exist; the run follows V2's release. Row `IRPT_ANLREQ-D2-S134` stays ARMED until this run reads back.

Three steps, one actor (the single IRPT CloudOps lane under rule 34; the lane is named by the CTO, `0.7.0_AE_CloudOps~AQ2` while it holds the macro), on portal DEV only:

1. **Mint** one scoped second-firm principal: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~219/fwd5_driver/fwd5_mint.py mint --email <name>@opal.invalid --firm <firm B> --allowed-firm-ids <firm B>` (measured header: one users row in `opal-users-v2`, conditional write, bcrypt cost 12, password read from stdin as one JSON object, TTL 3 hours, output only `MINT-OK READBACK-OK` / `MINT-REFUSED <word>`). The address is not the FWD-1 helper's (`fwd1-staff-r41b@opal.invalid`).
2. **Drive** `.../0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py --base <DEV origin> --email <that address> --ticket <firm A ticket> --firm-a <firm A> --firm-b <firm B> --request-id <firm A request> --job-id <firm A job> --out <applier deliverables dir> --go IRPT_ANLREQ.TO-RUN-FWD5.<id>` (measured header: signs in, makes each listed call for ONE ticket of the OTHER firm, verdicts REFUSED / LEAK / UNREACHED / EXCLUDED; exit 0 only if every made call is REFUSED; report `fwd5_run_report.json` holds no body, cookie, token, password or address).
3. **Remove** the principal: `fwd5_mint.py remove --email <that address>`; read `ABSENT GSI` and `ABSENT CONSISTENT`.

## 1a. Scope of the minted principal (held: CTO ruling msg 9670, relayed by V2 msg 9673, 2026-10-16 ~17:0xZ)

After the combined ticket-service release a staff row with neither `allowedFirmIds` nor the global marker is refused (403, firm scope not configured). The ruling: synthetic staff users minted after the release carry `allowedFirmIds` = [the ONE firm the run files under], never `scope_all_firms`; the mint's read-back prints the scope and the entitlement rows; each helper lands that as an amendment to its own helper's pair, which the CTO signs. For this act: `fwd5_mint.py` already writes `allowedFirmIds` as a list of strings from `--allowed-firm-ids` (measured header). To measure at the pin: (a) the mint's read-back does NOT yet print the scope and entitlement rows (header: output is only `MINT-OK READBACK-OK` / `MINT-REFUSED`), so an amendment cell is owed before this packet is signed; (b) the principal is a firm-B principal (its own firm), so its `allowedFirmIds` is [firm B] and it must be refused every call on firm A's ticket.

## 1b. Gate state at 18:1xZ (measured from a message, not read live by this seat)

The combined ticket-service release is LIVE (held: `2.0.0_SA_COO~V2` msg 9734: `opal-ticket-api` CodeSha `JwdnACONAnxw...`, modified 17:57:13Z; TV2's ledger closed 18:01:43Z; V2 ran `r18_rel_check.py` and `r19_rel_check.py` itself: REL-OK both). This is the readback the draft waited on. The base for the driver is the portal dev server on port 5174 as in V2's AR-v33 (measured in `ar_v33_run.mjs`: `BASE = http://localhost:5174`); the applier starts it and stops it after, as AR-v33 did. Firm A is `49financial` (ticket `TCK-20261015-944c84f8`, request and job `REQ-d47252fe74634d0c5cdd8067`: the synthetic row, now restored by t56). Firm B is another firm whose id the ticket service knows. Measured in `infra/aws/lambda/ticket_center/lambda_function.py:1124-1131` (comment): the portal knows 4 firms, `49financial`, `cottonwood`, `demo`, `inflection`; `inflection` is the one not reachable by `/submit-request`. Proposed firm B = `cottonwood` (a partner firm with a real filing path, so a refusal on firm A's ticket is a real cross-firm refusal and not an access gap of the firm itself); `inflection` is the alternative. The CTO half confirms the choice. The principal is firm B's own principal: `firmId` = firm B and `allowedFirmIds` = [firm B].

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

## 7. Measured on 2026-10-16 ~18:5xZ (issuer; offline runs and git reads at HEAD 8d222ddade, nothing live)

- Blob pins at HEAD (`git rev-parse HEAD:<path>`, paths under `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/`): `0.9.0_WK_IRPT_ANLREQ~219/fwd5_driver/fwd5_mint.py` = `ec8607ed57` (AR-tz-69 merged 59b330f528: prints `MINT-SCOPE allowedFirmIds=.. entitlement_rows=..`, refuses nonzero entitlement rows); `.../test_cross_firm_mint.py` = `4c9f115d4e`; `0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver/fwd5_driver.py` = `f59484af11`; `.../test_fwd5_driver_offline.py` = `8816670a56`; `0.9.0_WK_IRPT_ANLREQ~232/fwd5_driver/test_fwd5_driver_exit_semantics.py` = `76ac59cc3f`. The applier hashes the files it runs against these before any step.
- Offline: `fwd5_driver.py --selftest` prints `FWD5-SELFTEST-OK checks=19`; `--plan` sends nothing and states the required ids and the `--go` token; `test_cross_firm_mint.py` R46-TESTS-OK passed=25; the driver's two test files R46-TESTS-OK passed=23.
- Run inputs: ticket `TCK-20261015-944c84f8`, request and job `REQ-d47252fe74634d0c5cdd8067` (tenant `49financial`; the synthetic row, READY, `hop_failure` absent after t56), firm A `49financial`, firm B `cottonwood` (CTO half confirms), base `http://localhost:5174` (portal dev server started and stopped by the applier as in AR-v33). The password: 32 random bytes generated in the applier's memory and handed to the mint and to the driver on stdin only, as in AR-v33.
- The release is live (held, V2 msg 9734); the applier's STOP list: any non-`REFUSED` answer is reported by route name only and the principal is removed first; a mint refusal or `READBACK-BAD` stops the run before any request; the principal's TTL is 3 hours.
- Not claimed: that the driver has ever run against the live service (it has not); that the ticket service refuses firm A's ticket to a firm B principal (that is the run's result).
- Order: after the CTO half, the run order `IRPT_ANLREQ.TO-RUN-FWD5.<id>` goes to the single IRPT CloudOps lane (`0.7.0_AE_CloudOps~IB2`, rule 34), cited in my GO.
