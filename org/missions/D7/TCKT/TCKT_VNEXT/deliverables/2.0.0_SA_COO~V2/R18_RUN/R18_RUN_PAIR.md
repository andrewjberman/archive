# TCKT_VNEXT round 18 -- one live run of the trade form and the meeting request on DEV: never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~V2` (dell2), 2026-10-14. **Executor:** `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R18-RUN` (staged). **Outcomes graded:** FWD-10 and FWD-11 (PRD v0.6), due 2026-10-24.
**CTO half owed by:** `1.0.0_SA_CTO~DELL2`, who ruled the driven coordinator arm on msg 7832 (call (b)) and added msg 7853's two conditions, both carried below.
**Model:** the R16 crawl pair `R2_RUN/R2_CW1_CRAWL_PAIR.md` and `r16_cw2_crawl.py` (one synthetic `.invalid` identity, one token of at most 20 minutes, key and token in memory only, removal after `exp` read ABSENT).

## 1. The firm, the file and the readiness gate

- **Firm:** `cottonwood` (the unused test firm of the earlier runs). Both tickets are filed for it. The trade form's object lands in `opal-data-cottonwood` at `portal/cottonwood/state/ticket_attachments/trade-form/<32 hex>/<name>`.
- **The file:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_RUN/PLACEHOLDER_TRADE_FORM.pdf`: one page, 643 bytes, the words "PLACEHOLDER TRADE REQUEST FORM - synthetic - contains no client data". It is named a placeholder on the screen (FWD-10).
- **Start gate (all read, any failing is a STOP before anything is minted):** (1) `TO-R18-REL` is `complete` and `R18_CHECKS/r18_rel_check.py` prints `REL-OK`; (2) the portal DEV bundle carries BOTH forms: the candidate `cand/dell2/tckt-meeting-and-trade-form` @c05e3dda is merged on DEV by `portal-merge-forward.sh` under the CTO's approval row `dell2-20261014T202745Z-2131` (approved, Opal-internal) and the DEV site serves it (the applier prints how it read that);
  (3) the live routing reads `meeting_request.primary` = `["jeanette@opalinvest.com"]` exactly; (4) no open ledger names `opal-ticket-api`, `opal-tickets`, `opal-users-v2` or the ticket stack, in any live worktree (print the denominator).

## 2. The two identities (synthetic, internal tier, minted for this run only)

Both: `opal-users-v2` `PK USER#<address>`, `SK PROFILE`; `firmId opal-capital`, `status active`, `userType "test-filer"`, `allowedFirmIds` the LIST `["cottonwood"]`, written with `attribute_not_exists(PK)` and read back PRESENT with ConsistentRead before a token is minted.

| role | address (the date stamp is the run's, fixed in the GO amendment) | does |
|---|---|---|
| filer | `tckt-r18-filer-<YYYYMMDD>@opal.invalid` | files the Trade Request and the Meeting Request |
| coordinator | `tckt-r18-coord-<YYYYMMDD>@opal.invalid` | confirms one proposed time on the meeting ticket, inside the routing window |

**Tokens:** one RS256 token per identity, the CURRENT signing slot, `iss opal-portal-auth`, `aud opal-portal-api`, `tier internal`, `role user`, `userType "test-filer"`; `exp` at most 20 minutes after `iat`. Held in memory and the one browser context only; never written, logged or traced. The key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`. **Jeanette's address is never given to a seat or a token.**

## 3. The act (executor: a `0.7.0_AE_CloudOps` lane seat on dell2; this seat holds no key)

0. Open the NEVER-2 ledger entry first and keep it open until BOTH identity rows read ABSENT and the routing reads restored.
1. The start gate of section 1.
2. **Mint:** the filer row and token. (The coordinator row and token are minted at step 5, inside the window.)
3. **Trade Request, in a browser on portal DEV** signed in as the filer: choose New Ticket, Trade Request, the firm `cottonwood`, choose the placeholder PDF, submit. The page makes the three calls (upload-presign, the browser's PUT to the presigned URL, ticket create); no call replaces a click. Then ConsistentRead the ticket: `ticket_type trade_request`, `status open`, `attachment.key` under `portal/cottonwood/state/ticket_attachments/trade-form/`; `head-object` on that key returns `ContentLength` 643; open the form from the ticket row in the page and read that it opens. Record `tf_ticket`, `form_key`, `form_name`.
4. **Routing window opens:** read the live `ROUTING_MATRIX` (record `routing_before`; it must read `meeting_request.primary` = jeanette alone, else STOP). Mint the coordinator row and token. Set `meeting_request.primary` to the coordinator ALONE by `safe-apply` from a scratch worktree copy of the stack whose `main.tf` differs from the committed one in that one value; the plan must show exactly ONE attribute change (the Lambda environment's `ROUTING_MATRIX`) and nothing else, else STOP. Read it back (`routing_during`). **The window is the routing widening and is the only time it is wider than the committed tree.**
5. **Meeting Request:** as the filer choose Meeting Request, the firm, who, purpose, two proposed times, submit. ConsistentRead the ticket: `ticket_type meeting_request`, `status open`, the stored `routing.primary` = the coordinator alone. Record `mt_ticket`. As the coordinator, in the browser, CONFIRM one of the two times. ConsistentRead: `meeting.status confirmed`, `meeting.time` the clicked time, `meeting.by` the coordinator address, `status` still `open`. Record `coordinator_identity`, `mt_confirmed_time`.
6. **Routing window closes:** re-apply the COMMITTED tree under `safe-apply` (the plan again one attribute change, back); read it back (`routing_after`): `meeting_request.primary` = jeanette alone. The window ends only when that read passes.
7. **Removal:** wait until BOTH tokens' `exp` have passed, delete both rows, read each ABSENT with ConsistentRead. Close the ledger only after this and step 6.
8. Write `R18_RUN_RESULT.json` (keys as the order lists them) and the proof instance; the issuer's `R18_CHECKS/r18_run_check.py` is the criterion.

**The writes the identities may make:** the filer: the upload-presign, one PUT to the presigned URL, two ticket CREATEs, and the GETs the page makes for the board and the form; the coordinator: ONE `POST .../{meeting_ticket}/meeting`. No claim, no complete, no report, no package, no IRPT write, no other ticket.

## 4. Blast radius (what the run may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-tickets` | two new items (the trade and the meeting ticket), the meeting one gains a `meeting` member | tickets have no delete route; both are test tickets for `cottonwood`, left `open` (the issuer queues their closing as its own card, as with the earlier test tickets). No client sees them |
| `opal-data-cottonwood` object `portal/cottonwood/state/ticket_attachments/trade-form/<hex>/PLACEHOLDER_TRADE_FORM.pdf` | one 643-byte synthetic object created | **left in place**: deleting it is an S3 delete, which needs Andrew's word; the issuer queues that call at the run's close (the earlier synthetic objects' call `dell2-20261014T134418Z-2106` is the precedent). It holds no client data |
| `opal-users-v2` | two rows created, then deleted after `exp` | delete + ConsistentRead ABSENT, each |
| Lambda `opal-ticket-api` environment | `ROUTING_MATRIX` changed for the window, then restored | the committed tree re-applied; the prior value is recorded (`routing_before`: jeanette alone, the committed value, which the release left; the value before the release was manav and alyssa, recorded in `R18_REL_RESULT.json`) |
| mail | **none.** CREATE calls `notify_dl_isolated`, which resolves recipients from `TICKET_DL_MAP`; the live map reads as an EMPTY object (issuer's read-only read of the function configuration, 2026-10-14), so the resolver REFUSES and the handler logs `WE_DL_UNCONFIGURED` and sends nothing. CLAIM's client notice is never reached (no claim). The meeting route calls no notifier (its tests spy on it). The coordinator's real address is not in any list the run can mail | the trace records the `WE_DL_*` token each CREATE logged; `WE_DL_SENT` or `WE_CLIENT_SENT` is a surprise row and a STOP |
| cottonwood restricted prefix | not touched | the role's change is bounded to the trade-form prefix; any request outside it is a STOP |

No IAM, code or route change in this run. No client figures in any tracked file.

**Both branches.** (A) Every read passes: both tickets are open, the form is on S3, the coordinator's confirm is stored, routing is restored, both rows are ABSENT: `RUN-OK`. (B) A write is refused, the plan shows more than the one attribute, or any STOP fires: the window is closed FIRST (restore routing), the rows are removed after `exp`, and the refusal is recorded with its status and reason. A STOP inside the window never leaves the synthetic coordinator as the primary.

## COO half -- SIGNED 2026-10-14 by `2.0.0_SA_COO~V2`

I read the order, the R16 crawl pair, the live configuration for the mail statement and the readiness gate. The routing window (steps 4 and 6) is the widening and it is bounded in time by the closing read. The CTO half is owed; the GO to `TO-R18-RUN` is an amendment citing this file's blob and the CTO's signature, written only after `TO-R18-REL` reads `REL-OK` and the candidate is on DEV.

## COO half -- AMENDMENT 1 (2026-10-14, `2.0.0_SA_COO~V2`): the browser's origin is `http://localhost:5174`, read not assumed (a narrowing, no widening)

Read-only reads for this amendment: `aws cloudfront list-distributions` shows ONE hosted portal distribution, `EVTSA9VEHNZVH`, whose domain `d2n2nzpeqf34ge.cloudfront.net` carries the aliases `opalinvest.dev` and `www.opalinvest.dev`: it serves PROD, there is no hosted DEV hostname; and `portal/vite.config.ts` proxies the dev server's `/api/*` to that distribution. So "portal DEV" means the DEV branch's dev server on `http://localhost:5174` (the one dev port, workspace law), which reaches the live API through the proxy. Consequences, binding on the run:
1. Sections 1 and 3 read "the browser" as a Playwright browser on dell2 opened on `http://localhost:5174`, served by `bun run dev --port 5174` from a checkout of the portal's `DEV` branch that carries the candidate `cand/dell2/tckt-meeting-and-trade-form` @c05e3dda (merged by `portal-merge-forward.sh` under approval row `dell2-20261014T202745Z-2131`). The start gate's second item reads that checkout's HEAD, not a hosted site.
2. The browser's PUT of the form to the presigned S3 URL is cross-origin from `http://localhost:5174`. That origin is in the laptop's CORS list (`COO~B1`'s pair: PROD `https://opalinvest.dev` and `https://www.opalinvest.dev`; DEV `http://localhost:5174`), so no origin is added. The CloudFront domain `d2n2nzpeqf34ge.cloudfront.net` and every other local port are NOT admitted: a run that opens either is a STOP.
3. The dev server is stopped when the run ends; the synthetic tokens live in that browser context only.
Both branches, blast radius, rollback and mail statement are unchanged. The CTO half of this amendment is owed.

## COO half -- AMENDMENT 2 (2026-10-16, `2.0.0_SA_COO~V2`): the run splits; PART 1 (FWD-11, the Meeting Request) runs now; PART 2 (FWD-10, the Trade Request) waits (a narrowing, no widening)

**Why:** `0.7.0_AE_CloudOps~TV2` STOPPED at the start gate before anything was minted (msg 9764, row `TCKT_VNEXT-D2-S56`): the DEV New Ticket type list does not offer Trade Request (`portal/src/pages/TicketCenter/TicketCenter.tsx` line 730, hide commit `4d601023`, 1.0.0_SA_CTO~DELL2, on Andrew's word of 2026-10-13 ~18:5xZ: "we should not push this til we actually have a functioning channel for that"; the candidates `c05e3dda` and `12c164a0` do not lift it). Step 3 says "choose Trade Request in the browser; no call replaces a click", so FWD-10 cannot be run as written. The Meeting Request (step 5) does not depend on it.

**PART 1 (now), FWD-11 only.** Sections 1 to 3 read with these changes and no others: (a) start gate item (2) reads "the portal DEV checkout carries the MEETING form" (it does: `c05e3dda` and `12c164a0` are ancestors of origin/DEV) and does not require Trade Request in the type list; (b) step 3 (the Trade Request, the presign, the PUT, the trade ticket CREATE) and every claim about the form object, the form key and the placeholder file are SKIPPED: no object is written to S3, no trade ticket exists; (c) the filer files ONE ticket (the Meeting Request) and the coordinator makes ONE `POST .../{meeting_ticket}/meeting`; (d) the criterion is `R18_CHECKS/r18_run_check_meeting.py` (the same check with the trade parts removed; it reads RUN-BAD at the base), and the result file carries the meeting subset of its keys; (e) the two identities, the routing window (steps 4 and 6), the removal (step 7) and the mail statement are UNCHANGED, `allowedFirmIds ["cottonwood"]` on both rows, the page origin `http://localhost:5174` printed. **Blast radius per key shrinks:** `opal-tickets` ONE new item (the meeting ticket, left open), no `opal-data-cottonwood` object, two identity rows created and deleted, the Lambda `ROUTING_MATRIX` changed for the window then restored.

**PART 2 (later), FWD-10.** NOT in this amendment. It needs the Trade Request in the DEV type list, which is Andrew's hide to lift or a CTO-approved scratch build with the filter removed (never pushed): the CTO's call, asked separately. When ruled, PART 2 runs steps 3 and the object legs under this pair's original sections and its own GO, the form's S3 object listed by key and VersionId.

**Both branches** are the pair's section 4's, restricted to the meeting arm. The CTO half of this amendment is owed.
