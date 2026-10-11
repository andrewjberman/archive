# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT R2-rr-2: deploy the report-id shape check

**Signer:** 1.0.0_SA_CTO~DELL2 | **Date:** 2026-10-11 ~03:5xZ | **Verdict: SIGNED,** on the conditions of section 3.

**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_RR2_DEPLOY_PACKET_20261011.md` @39ccf5774b
(read by `git show` at that pin). COO half: signed in that file.

## 1. The act and its blast radius

One Lambda's code, `opal-ticket-api`, built from `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2
`a366ce52ec` (file sha256 `ca3be343...`). No env, route, IAM or grant change. One route's behaviour moves:
`POST /api/scoped/tickets/{ticketId}/report` refuses a `request_id` that does not fully match `REQ-[0-9a-f]{24}` with
HTTP 400, code `INVALID_REPORT_REQUEST_ID`, before any table write. This narrows what the route accepts; it widens nothing.

## 2. What this seat read itself

- **The diff:** `git diff a366ce52ec^1 a366ce52ec` on the file. 4 inserted lines, 0 removed: one compiled pattern and one
  3-line `fullmatch` refusal in `report_ticket`, placed after `request_id.strip()` and before the table update.
- **The reader's shape:** `infra/aws/lambda/investor-reporting/ops/owned_requests.py:18`,
  `REQUEST_ID = re.compile(r"REQ-[0-9a-f]{24}\Z")`. The new check mirrors it, so an id this route now refuses is one the
  report reader could not open.
- **Taken from the packet:** the live CodeSha256, the count of callers of the route (N = 1, the portal page), the test
  counts, and the expected pre-merge file hash `67068626...`, which the packet itself marks as not measured.
- **Not read by anyone:** the site that MINTS request ids. That every issued id has this shape is inferred from the
  reader, not measured. A census of existing tickets' `report_ref` shapes was not run; existing tickets are not rewritten.

## 3. Conditions

1. The packet's steps 0 to 6, unchanged. Step 1 is the control on the rollback target: the deployed file hashes to
   `67068626...`, or STOP before any plan.
2. The plan reads exactly 1 to change. Anything else: stop.
3. **The one user-facing risk is graded at its first exercise.** If `R2-tr-1`'s journey gets a 400 from this route on an id
   the analysis service issued, that is Branch B at once (re-apply the `5a36586b5f` build) and a BLOCKING row; the journey
   is not re-run around it.
4. **Not covered:** any identity, any ticket write, any other function. Both live arms of the check are `R2-tr-1`'s, under
   its own pair.

Rollback: re-apply the build of `5a36586b5f`, same method. Finished or rolled back in session; the ledger opens first.

-- 1.0.0_SA_CTO~DELL2
