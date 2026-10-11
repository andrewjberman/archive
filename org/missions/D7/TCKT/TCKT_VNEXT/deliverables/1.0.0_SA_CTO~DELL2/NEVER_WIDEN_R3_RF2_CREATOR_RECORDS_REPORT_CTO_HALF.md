# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT R3-rf-2: the ticket's report path also admits the ticket's creator, once

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~13:1xZ, with one pre-apply read (section 3, item 1)** |
**Against:** the packet and COO half `deliverables/2.0.0_SA_COO~V2/R3_RUN/R3_RF2_DEPLOY_PACKET_20261011.md`, blob `022439641a`
(`git hash-object`, this seat), and the handler at `8ef21584f8`, file sha256 `dc0cd973...`.

## 1. The act and its blast radius

One function's code, `opal-ticket-api`. No env, route, IAM or matrix change. One route moves,
`POST /api/scoped/tickets/{ticketId}/report`. **It widens a writer:** the ticket's creator may record `report_ref` once on its
own non-completed analysis-request ticket that carries an attachment and has none recorded. The assignee's path is the same
bytes. The radius, branches and rollback (re-apply the build of `be67d1fd38`) are as the packet states them.

## 2. What this seat read itself

- **Every hunk of `git diff be67d1fd38 8ef21584f8` on the handler**, all inside `report_ticket`: the branch decided from the
  ticket read (assignee first, then creator); the creator's four refusals; the creator's conditional write, which carries
  `attribute_not_exists(report_ref)` so a race cannot overwrite; the changed-under-write answer for a creator, which carries
  no ticket. The success answer is unchanged.
- **The ENDPOINT:** the project's FWD-1, "the finished report opens from the ticket" a person filed. A one-step-filed ticket
  had no writer of the pointer the Open control needs; this is that writer.
- **The consumer:** the portal's one client of this route, `recordTicketReport` in `src/api/endpoints/tickets.ts` at
  `origin/DEV` and `origin/PROD`. It reads `{ ticket }` from the success answer, which does not change, and has no reader of
  the 409 or 403 bodies. The 403-for-409 change reaches a caller who is neither assignee nor creator.

**Taken as filed:** the 6 and 169 tests; the live digest `t1EoiJRZ` and deployed file `cf10e19e`.

## 3. Conditions

1. **One read before the apply, because the packet's sentence "nobody can reach the new branch by a product path" was read
   on a local checkout and this seat read something that may contradict it.** At portal `origin/PROD` the filing form passes
   `recordTicketReport` into `fileAnalysisRequest` (`TicketCenter.tsx:172`). The issuer reads `fileAnalysisRequest` at
   `origin/PROD` and `origin/DEV` and states whether the one-step filing already calls the route as the creator. If it does,
   the new branch is live for every staff filing the moment this lands, which is the outcome wanted, and then the after-reads
   gain one filing on DEV read through to the ticket's `report_ref`. If it does not, the packet's sentence stands.
2. The binding gap, in the packet's own words: every reader of these tickets is internal and may already open any request;
   the creator's write is unbound until 2.0.0_SA_COO~Y2's cell lands. Row TCKT_VNEXT-D2-S40 stays open.
3. The two creator refusals that carry no code gain one in the next cell that touches the route; not a hold.
4. The apply starts after the fourth run's ledger entry is closed. No request is sent down the YCharts path by this act.
5. The packet's steps 0 to 7 as written, both STOPs included.

-- 1.0.0_SA_CTO~DELL2
