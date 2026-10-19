# CTO half -- ONE fresh synthetic commentary end-to-end run (resident, drafter, packager, commentary route)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~19:4xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md`.
I re-measured it: blob `394e573a4ae5902b4121626c31a0c605c35e8968`, equal at commit eaaadedbf3 and in the working tree;
sha256 `13dcef410597407129bcb9c0b952440a63abf63be2b457cd76235e8d35e8ef6b`; 8,023 bytes. COO half signed in the packet.
Ledger `irpt-commentary-e2e-20261017`. Operator: `0.7.0_AE_CloudOps~IB2`.

**SIGNED, with the conditions below.**

## Blast radius (packet section 2, accepted as read)

- **Created, synthetic only:** one `opal-users-v2` row, one upload, one ticket, one request item, one job row, its
  artifacts and blobs, and at most one `commentary_ready` message. Every one is deleted by the key recorded at creation
  (section 4). Andrew's word covers synthetic deletes (`ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md`).
- **Compute:** one resident render, which may call YCharts under the standing 390 s spacing rule. One model call by the drafter.
- **Writers:** one, the synthetic actor.
- **Moves nothing deployed:** no code, role, route, queue, table, schema or secret.
- **Served output moved:** none a client or staff user can see. The synthetic ticket is visible only to its own creator
  while it exists.

**Rollback:** none is needed, because nothing is deployed. Section 4 removes the objects whether the run passes or stops.

## Read at signing

**The portal reads this route's answer.** On PROD (99d2b2a7), `analysis-request-commentary-pdf` goes through the same
adapter as the report PDF (`src/pages/InvestorReporting/contracts/envelope.ts:197` and `:201`, both
`adaptAnalysisRequestPdf`). So the `signedUrl` type against the `download_route.url` contract (rows W293-S1 and S2)
is adapted in one place, the same place that serves the report link. This run still reads the route directly, as the
packet says. The portal-side read is graded once in the portal flag's own DEV smoke.

## Conditions (in addition to section 3)

1. **The API base.** R0 states which deployed API the run calls, by its config source (the `vite.config` proxy target
   name, or the Terraform output name), never as a URL in the receipt. It is the deployed API that the PROD portal
   calls. A local dev server is used only as a proxy to that same API, never as a different backend. Any doubt STOPS
   before step A.
2. **Notifications.** Beyond `TICKET_DL_MAP` reading `{}`, R0 states whether ticket creation posts to Teams or any channel.
   Any recipient outside a synthetic or `@opalinvest.com` address STOPS before step T.
3. **The door.** A refusal at step U is an expected first stop (window 4). The receipt names its closed code, and the
   deletes then run for what exists. No second upload is tried in this pair.
4. **The poll budget** is 30 minutes in total with a 20 s step. Exceeding it is a STOP at the hop it reached, with the
   hop named.
5. **The receipt** carries the packager's own `IRPT_RESIDENT_PACKAGE` line for this run's message (outcome, or
   `retained_for_retry class= code=`), its UTC time, and the dead-letter depth before and after.
6. **On pass,** the receipt prints the PDF's size and content type, and `~Y2` reports to this seat. The portal flag
   `cand/dell2/anlreq-commentary-always-requested` then goes to DEV by its own approval row. Its PROD promote waits on
   Andrew's word (Ticket Center is client-facing).
7. **Timing:** outside the weekday 11:30Z to 14:15Z band. Today is Saturday, so it may run now. It never runs alongside
   another IB2 apply.

---

## ADDENDUM 1 -- SIGNED (2026-10-17 ~20:4xZ): name a synthetic advisor on the upload

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM1_ADVISOR_COO_HALF_20261017.md`.
I re-measured it: blob `02149564860419fbcb11e3add00de8617282af32`, equal at 5f19ba81e7 and in the working tree; sha256
`491648a2bad52856b7db7ff200b4b7b1557dc8701f225d4c2ed48c0495fabade`; 4,454 bytes. COO half signed. Ledger
`irpt-commentary-e2e-2-20261017`.

**Read at signing:** `infra/aws/lambda/investor-reporting/_authz/served.py:1089-1091` raises
`ProspectOwnershipRefused("an on-behalf upload must name the firm advisor")` when the upload names no `advisor_email`
and the tenant is in the actor's `allowedFirmIds`. That is the first run's stop. Neither the door nor the mint is wrong;
the run's steps lacked the advisor.

**Blast radius delta, accepted:** two more synthetic rows at 49financial, written and removed by the existing
`fwd1_advisor.py`. They are one `opal-users-v2` row (no credential, cannot sign in) and one `opal-partner-49financial`
row, and they exist only for the run. Nothing deployed moves.

**Conditions:** all seven of my conditions above stand, and these are added:
1. A2's pre-state refusal reads both rows ABSENT before any write. Monday's window-5 advisor (`...-20261019`) must not
   exist yet or be touched.
2. A closed authorization refusal at R (the route re-authorizes the owner placement, `ops/owned_report.py:347-349`) is a
   STOP at R with its code. It is an informative result, not a failure of this pair.
3. D removes the advisor rows by the tool's own `remove`, read back ABSENT, in the same receipt as the other deletes.

---

## ADDENDUM 2 -- SIGNED (2026-10-17 ~20:5xZ): re-post the identical upload while the door answers RESOLVING

**Addendum:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM2_RESOLVING_COO_HALF_20261017.md`.
I re-measured it: blob `5bddf32c3b213142e35f4d882fe6114de3c55fc3`, equal at d09a236b6c and in the working tree; sha256
`523d0f8380f1bc1ce05096a53711981a06f1aef20e2b2c88bc0822acccccd777`; 4,562 bytes. COO half signed. Ledger
`irpt-commentary-e2e-3-20261017`.

**Read at signing:** `infra/aws/lambda/investor-reporting/intake/uploads.py:522-533`. A retained `RESOLVING` row is
resumed. It is re-dispatched only after `REDRIVE_SECONDS` under a conditional replace, and it answers `RESOLVING` again.
A re-post of the same token creates no second object. The blast radius is unchanged.

**Accepted:** at most 5 identical posts, 3 s apart, the portal's own rule. A fifth `RESOLVING` is a STOP at U, with the
elapsed time and the resident journal's `RESOLVE` line count (window and total printed).

**Note:** if five tries at 3 s all answer `RESOLVING`, the portal's limit may be shorter than the resident's resolve
time. A real filing would then hit the same wall. That stop is a product finding for the next step, not a failure of
this pair.

My seven conditions and ADDENDUM 1's three stand. My condition 3 reads "no second upload": the re-post is the same
upload, not a second one.
