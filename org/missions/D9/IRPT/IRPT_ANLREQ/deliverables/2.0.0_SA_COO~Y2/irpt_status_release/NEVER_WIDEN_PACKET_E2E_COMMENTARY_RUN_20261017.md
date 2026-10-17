# Never-widen sign-off packet -- ONE fresh synthetic commentary end-to-end run (resident, drafter, packager, commentary route)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-17. **Operator:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane).
**Authority:** CTO ruling `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/RULING_COMMENTARY_GAP_TWO_CAUSES_20261017.md` ADDENDUM 1 (msg 10652) and its conditions; Andrew's 2026-10-16 word that synthetic test deletes need no call (`ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md`). **Ledger:** `irpt-commentary-e2e-20261017`. **Specification:** worker `0.9.0_WK_IRPT_ANLREQ~293`, `TO-AR-y-398`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~293/r52/E2E_RUN_SPECIFICATION.md` (merged `356f1d426d`; criteria 6 and 6 re-run by the issuer).
**Scope:** ONE synthetic request, one synthetic staff actor, one synthetic ticket. NO product code, IAM, route, queue, table, secret, schema or release moves. Andrew's ticket `TCK-20261017-5af976ff` and every client request are NOT touched.

## 1. What the run is (steps read from the specification)

| step | act | basis (issuer-spot-checked where marked *) |
|---|---|---|
| A | mint ONE synthetic staff user (`@opal.invalid`) with the existing mint (`deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py` `cmd_mint`, password generated in memory, never printed or stored) | U2 |
| L | `POST /auth/login` as that user (fields `email`, `password`); keep the `accessToken` in memory; send it as `Authorization: Bearer` with `X-Contract-Version: v1` | U2 |
| U | `POST /api/scoped/investor-reporting/analysis/inputs` with the 5-row holdings bytes of the window-5 order step 5 (sha256 `30d44443701df5f92dfee4def4d1a1f139818ee416601b2577c66e30fb3b96a1`) to get an `input_id` (state NORMALIZED) | U1, U5 |
| T | `POST /api/scoped/tickets` (type `analysis_request`, answers, attachment `{upload_id, input_id}`) to get a `ticket_id` of the shape `TCK-YYYYMMDD-8hex` | U1, U5 |
| S | `POST /api/scoped/investor-reporting/analysis` with `request_id`, `client_id` null, `account_ids` [], `snapshot_id` null, `variant` overview, `comparison_keys` [], `report_title`, `prepared_for`, `input_id`, `ticket_id` AND **`commentary_requested: true`** (the field is admitted: `ycharts/generate/submission.py:14-16, 82-83`*; the route is `ycharts/generate/entry.py:148-149`*) | U1 |
| P | poll, in order: job row READY; request item `commentary_ref`; the draft artifact; the `commentary_ready` message consumed (journal line `IRPT_RESIDENT_PACKAGE outcome=ATTACHED` or `ALREADY_ATTACHED`); the PDF artifact `<REQ>-commentary-<sha256>` in family `YCHARTS_OPAL_REPORT` | U3 |
| R | `GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf` as the same user: PASS is `download_route.url` present and the PDF it names opens (size and content type printed) | U3 |
| D | delete the objects this run created, by the keys recorded at creation (section 4) | U4 |

## 2. Blast radius

- **Objects created in production tables and buckets (synthetic):** one `opal-users-v2` row; one upload (original and normalized artifacts, index rows); one ticket in the ticket table; one request item and one job row; the draft, report, Overview and commentary-PDF artifacts with index items and blobs; at most one `commentary_ready` message.
- **Compute and vendor use:** one resident render (the resident may call YCharts for prices: the window-5 rule holds, the first call at least 390 s after the last YCharts call in the resident journal, R0 prints it) and one model call by the drafter (its settings are set per IB2's read R4). No mail: R0 reads `TICKET_DL_MAP` of `opal-ticket-api` and a non-empty map or any recipient outside `@opalinvest.com` is a STOP.
- **Writers counted:** the actor is the only caller; no other principal files, reads or deletes. The route read is the creator's own.
- **No release moves:** the resident stays `irpt-resident-0485393f3a-r34k`, irpt-status `274dl2bC...`, the drafter `I/6mirBT...`.

## 3. Conditions (the CTO's ruling plus the issuer's)

1. Synthetic data and one synthetic actor only; the actor stays in place until the route read ends. 2. Outside the weekday 11:30Z to 14:15Z band (today is Saturday). 3. R0 reads, all green or nothing is minted: no other open `.open_deploys` entry names the resident, either Lambda, the ticket service or the users table (denominator printed); `get-function` CodeSha256 of `irpt-ycharts-generate`, `irpt-status` and the drafter as recorded; the resident root reads `0485393f3a-r34k`; `TICKET_DL_MAP` reads `{}`; YCharts quiet 390 s. 4. Stop at the FIRST red hop (door refusal, accept refusal, job not READY within the budget, draft absent, message not consumed, PDF absent, route not a URL), print the hop and its CLOSED code with the UTC time, take no retry and no second request. 5. The API base is the one the portal's dev server proxies to (`vite.config` proxy target), or `http://localhost:5174` while the CTO's checkout serves it; `X-Api-Key` is sent only if the deployed API requires it `[NOT READ by the issuer: IB2's R0 states which]`. 6. The poll budget: `[the per-hop timings are NOT READ: no earlier run reached the door (window 4 was refused at the door); IB2 states a budget of 30 minutes in total with a 20 s poll step, and the budget is a stop, not a pass condition]`. 7. The receipt carries counts, keys and closed codes only, includes the packager's journal line for this run's message (counted by its `IRPT_RESIDENT_PACKAGE` literal, plus any `retained_for_retry class= code=` line), and never a token, password, URL or signature.
8. **Pass:** the route answers a URL and the PDF it names opens (size and content type printed). **Fail:** stop; report the fresh closed code or `ReportRefused` with its timestamp; any offline replay is its own cell; no code change rides this pair.

## 4. Delete list (D; recorded key by key at creation, never a scan-delete)

Delete exactly the keys the run recorded: the `opal-users-v2` row (`fwd1_mint.py remove`, absence read by ConsistentRead and the email index); the ticket item; the request item; the job row; every `ARTIFACT#` index item whose logical id carries this run's `<REQ>`, with its S3 object and versions; the upload's index rows and blobs. Each delete is conditional on the key recorded at creation; each is read back ABSENT; the keys are listed in the receipt. **Gaps stated plainly (U4): no remover script exists for the upload objects, request item, job row, artifacts, blobs and ticket, so IB2 deletes them with its own conditional deletes by recorded key.** A leftover (a dead letter message, a blob that will not delete) is reported with its key, not hidden.

## 5. Rollback

Nothing is deployed, so nothing rolls back. A red hop leaves synthetic objects: section 4 removes them. The pair gives no leave-behind: if the run stops mid-way, IB2 runs D for what exists and reports.

## 6. Not claimed

- That the upload door accepts the holdings bytes (window 4 was refused at the door with `NOT_AUTHORIZED`; the cause fix landed at TO-AR-y-373 and the window-5 R0 reads, but no run has passed the door). A door refusal is a STOP with its code.
- That the portal's reader accepts the commentary-pdf answer (the portal types it `signedUrl`, the contract carries `download_route.url`; rows `W293-S1` and `-S2`); this run reads the route directly.
- That the old refusals (`ReportRefused` twice, then `ACTOR_NOT_FOUND`) were decay of a removed actor; the run is what discriminates.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-17, on this packet's bytes at the commit that carries it. The write set: the synthetic objects of section 1 and their deletion by recorded key (section 4); no release, role, route, queue, table or secret moves. The blast radius is section 2; the stop rule is section 3.4; the deletes are section 4.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
