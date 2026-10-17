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
