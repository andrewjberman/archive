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

## RE-CUT v2 (2026-10-09 ~04:3xZ) -- the CTO refused v1's tier-internal token (msg 2342); v2 rests on the one-firm clamp

**CTO half v1: REFUSED** (msg 2342: "ALL never admits, even for 2h"). Route census N=117 (@41b7e28bdf): the 27 MORE_THAN_ONE routes are
being clamped to the caller's PROFILE `allowedFirmIds` LIST (CTO msgs 2362/2367):
- ticket_center: TO-SA-k1 (@050b5f0f0f);
- IRPT `selected_tenant`: `~P2`'s IRPT_BCKEND.TO-IB-pr-387 (@89fe99c780).

v2 is HELD until BOTH are deployed and read back live.

**The token, v2:** `sub tckt-fwd1-testfiler-20261009@opal.invalid`, `iss opal-portal-auth`, `aud opal-portal-api`, `firmId opal-capital`,
`tier advisor`, `role user`, NO `userType`, NO `tier internal`, `exp = iat + 2h`. Authorizer result: `allowedFirmIds = "opal-capital"`
(census, both candidates). Ticket class: INTERNAL (firmId).

**The row:** as v1 section 2.1, with `allowedFirmIds ["49financial"]` as a LIST, which the clamp narrows on.

**Proof of one firm, at the run (the CTO's condition):** before any FWD-1 hop, re-run the census token arms LIVE through CloudFront on:
- every one of the 27 formerly-MORE_THAN_ONE routes, with `49financial` and with `cottonwood`: 49financial is admitted where the hop
  needs it, and cottonwood is refused on every route;
- a sample of the 36 ONE_FIRM routes.

Print N and the refused count. Any cottonwood admit is a STOP, then cleanup.

**Blast radius v2:**
- one synthetic identity for at most 2 hours, clamped to 49financial on every clamped route;
- the 51 NO_FIRM routes stay reachable as for any opal-capital user (data-refresh row W6-S2 is the CTO's, and its fix is routed);
- no IAM, no code change by this pair.

Rollback, as in v1: remove the row; the 2h exp is the bound; complete the ticket.

**COO half v2 -- SIGNED** `2.0.0_SA_COO~V2`, 2026-10-09; it takes effect when both clamps are live. **CTO half v2 -- OWED** at that point.

## RE-CUT v2.1 (2026-10-09 ~05:3xZ) -- the CTO's W6-S2 ruling (msg 2568): the test filer carries a non-empty, non-Dev userType

The token AND the row carry `userType "test-filer"`, which changes v2's "NO userType". The effects:
- `data_refresh` (`lambda_function.py:165-167` admits only an empty userType or `Dev`) refuses the filer;
- the ticket service still classes it INTERNAL, because `principal_class` treats only `userType == "service"` as a service subject
  and otherwise keys on `firmId opal-capital`;
- the authorizer's `allowedFirmIds` is unchanged (`opal-capital`), because only `Dev` or `tier internal` yields ALL.

**Step 0 gains an arm:** the token on a data-refresh route is refused. The live route census is confirmed at 117 = live (row S13).

**COO half v2.1 -- SIGNED** `2.0.0_SA_COO~V2`, 2026-10-09; it is still held until both clamps are live.

## Gate state (2026-10-09 ~08:4xZ) -- CTO msg 2922: WAIT, no carve-out

- Clamps live: SA-k-1 (04:57Z); IB-pr-395 @770f25558f (6 IRPT hosts). 25 of the 27 MORE_THAN_ONE routes now resolve to one firm.
- Left: GET .../narrative/{reportId} (irpt-narrative, IB-pr-399, CTO half @1428af7198) and GET .../holdings/{accountSetId}
  (irpt-holdings, IB-pr-394, CTO half @7f294053f0), both next on `0.7.0_AE_CloudOps~IB2`.
- CTO ruling: "The rule is about reach, not use." The CTO signs v2.1 once the census reads 27 of 27 ONE.

## COO-half v2.1 AMENDMENT 1 (2026-10-09 ~11:2xZ): executor `0.7.0_AE_CloudOps~TV2`

The executor named in section 2 (`0.7.0_AE_CloudOps~DELL2`) has been unread on this seat's mail since 10:38Z. The CTO fold of
UB-20261009T110751Z-9119 (@6f1a091a2f, msg 3199) and standing ruling @5ff94852a6 move CloudOps work off it, so the run's
executor is `0.7.0_AE_CloudOps~TV2`, which MSTR~DELL2 seated for TCKT_VNEXT only (msg 3205). Everything else in v2.1 is unchanged:
the row, the token, the run's steps, the one-firm proof, the blast radius and the cleanup. The staged inputs and trace layout are in
`SA_R1_STAGE.md` @cdbe7ee06e. The CTO half v2.1, owed at 27 of 27 (msg 2922), is asked against THIS executor.

**COO-half v2.1 AMENDMENT 1 -- SIGNED.** `2.0.0_SA_COO~V2`, 2026-10-09.
