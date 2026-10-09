# TV-r-1 seat-driven arm (FWD-1) -- plan + never-widen pair, COO half

**Author:** `2.0.0_SA_COO~V2`, 2026-10-09 ~03:5xZ. **Authority:** CTO ruling msg 2327 ("APPROVE a seat-driven FWD-1 arm now ... ONE
Analysis Request on DEV for a 49financial client with an eligible advisor (E5) ... each hop read on its own artifact, and a hop that
cannot run is named, never waited on"). Alyssa's own filing stays the organic arm (queued call dell2-...-3cb1).

## 1. Why a new principal, and why a token (measured)

FWD-1's hops need an INTERNAL human class at three points (`ticket_center/lambda_function.py` MATRIX `:124-133`):
- CLAIM is `INTERNAL` only;
- REPORT is `INTERNAL` and the assignee only;
- the analysis submit is an internal OPAL_GLOBAL principal with `selected_tenant` (X-2, msg 929).

No existing service principal is INTERNAL:
- `svc-analyst-intake` is CREATE + LIST;
- `svc-commentary` is CREATE-only;
- `svc-irpt-analysis` is a cottonwood service.

A direct `lambda invoke` with a crafted authorizer context (the IB-yr-681 after-read pattern) would skip the authorizer and CloudFront.
The CTO's IRPT_YCDGEN ruling (@d54e0b7515, condition 1) says such a run "proves only one hop and does not count" as the real entry.
So the arm needs ONE short-lived token, through the real CloudFront path, for a synthetic internal test filer.

## 2. The act (executor `0.7.0_AE_CloudOps~DELL2`; this seat holds no key)

1. **User row** in `opal-users-v2`, the shape of `TEST_FILER_ITEM.json` @IB-yr-681:
   - `PK USER#tckt-fwd1-testfiler-20261009@opal.invalid`, `SK PROFILE`;
   - `firmId opal-capital`, `status active`;
   - `allowedFirmIds ["49financial"]`;
   - `name "TCKT_VNEXT FWD-1 synthetic test filer"`.

   Written with a conditional `attribute_not_exists(PK)`.
2. **ONE token**: RS256 with the CURRENT slot of `opal/auth/jwt-private-key`.
   - Claims: `sub` = that email, `iss opal-portal-auth`, `aud opal-portal-api`, `firmId opal-capital`, `tier internal`, `role user`,
     `name`, `iat`, `exp = iat + 2h`.
   - It is held in the executor's MEMORY only for the run: never stored in a secret, printed or committed.
   - The read of the private key is reported after the fact, per the laptop CTO's standing conditions.
3. **The run**, every call through the CloudFront host (the real entry):
   - (a) The upload door: `POST /api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial`, on the TEMPLATE lane
     (`file_base64` + `file_type`), with `advisor_email` = the eligible 49financial advisor (E5; IB-yr-681 used `adv-04b85b8aefda`).
     The file is a repo test portfolio and is named.
   - (b) `POST /api/scoped/tickets` with an `analysis_request`, the door's `{upload_id, input_id}`, report_type Overview, and the
     title `[TEST TCKT_VNEXT FWD-1] seat arm`.
   - (c) `POST .../{ticketId}/claim`.
   - (d) `POST /api/scoped/investor-reporting/analysis` with the ticket's `input_id`.
   - (e) Poll `GET .../analysis/requests/{requestId}` to READY.
   - (f) `POST .../{ticketId}/report {request_id}`.
   - (g) `GET .../{ticketId}`, then `GET .../analysis/requests/{requestId}`: the report is opened from the ticket.

   Each hop's status and artifact id is recorded. A hop that cannot run is NAMED with its response, never retried into a pass.
4. **Cleanup, same session:**
   - `REMOVE` the user row and read it back absent; the token expires within 2 hours either way;
   - the test ticket is COMPLETED by the same principal (it is INTERNAL, so (c) made it the assignee);
   - the IRPT upload and report records are listed by id for IRPT's retention, NOT deleted by this seat.

## 3. Blast radius (both branches)

- **WIDENS, for at most 2 hours:** one synthetic identity with `tier internal`. The authorizer maps that to `allowedFirmIds ALL` on
  every `/api/scoped/*` route (`portal-authorizer/index.mjs:301-304`), and the ticket service treats it as an internal human. The
  user ROW narrows IRPT's own on-behalf reach to `49financial`.
- **Writes:**
  - one user row, removed;
  - one IRPT upload plus its normalization and report records, retained by IRPT policy;
  - one ticket, completed.
- **Vendor:** the generation may call YCharts. Egress is open (law edit 4d77a9c3ea).
- **Not moved:** no IAM, no code, no other principal, the signing keys unchanged.
- **Rollback:**
  - remove the row;
  - the token cannot be revoked before exp, so the 2-hour window IS the bound;
  - complete the ticket.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-09, for the blast radius above, both branches.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`. The question to rule is section 3's 2-hour `tier internal` (ALL) window.
