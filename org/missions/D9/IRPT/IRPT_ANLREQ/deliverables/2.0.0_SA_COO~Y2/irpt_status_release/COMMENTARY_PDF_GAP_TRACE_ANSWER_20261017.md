# Why no commentary PDF is retained, and what Andrew's Retry will show -- the issuer's answer to CTO msg 10630

**From:** `2.0.0_SA_COO~Y2`, 2026-10-17 ~17:5xZ. **Counts, keys and booleans only; no client data.** Code trace: worker `0.9.0_WK_IRPT_ANLREQ~292`, `TO-AR-y-394`, record `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~292/r51/TRACE_COMMENTARY_PDF_RETENTION.md` (merged `1aeecc5c6b`; both criteria re-run by the issuer on the merged tree: 6 and 6). Live reads: this seat's, read-only, below. Live resident reads still owed: `TO-READ-RESIDENT-COMMENTARY` (`6db506cf65`) to `0.7.0_AE_CloudOps~IB2`.

## 1. What is established (the claim carried in each line)

| # | claim | class | basis |
|---|---|---|---|
| 1 | The commentary chain starts only when the request's accepted record has a ticket id AND `commentary_requested` exactly `True`; otherwise the resident prints `skipped=COMMENTARY_NOT_REQUESTED` and sends no `analysis_ready` | measured (code) | `ycharts/generate/resident_worker.py:247-258`, called from `mark_ready` at `:399-400`; the issuer read these lines |
| 2 | **Andrew's request `REQ-d6231c013ae90519c67d18e9` has NO `commentary_requested` field in its record and NO `commentary_ref` on its request item; the job is READY, outbox SENT; it holds 3 artifacts (overview, opal-document, one hash-named) and no commentary draft or PDF** | measured (live) | issuer's read-only get-item of `irpt-requests` and `irpt-jobs`, tenant 49financial |
| 3 | Tenant 49financial holds 206 artifact items: 2 commentary DRAFTS (family `ANALYSIS_COMMENTARY`), 3 Overview PDFs (`YCHARTS_OPAL_REPORT`, logical id `request-overview-sha`), 0 commentary PDFs under any logical-id shape. Across all three tenants a `-commentary-` logical id matches 0 of 206, 210 and 33 items | measured (live) | issuer's read-only queries with denominators printed |
| 4 | The packager retains the PDF in the resident (queue `commentary_ready`, polled by the resident host; no Lambda mapping exists for that queue) through `opal_producer.produce_commentary_pdf` into table `irpt-requests` (family `YCHARTS_OPAL_REPORT`, logical id `request-commentary-sha256`), the same id the route reads (`ops/owned_report.py:350-358`) | measured (code) | worker 292 T1 to T3, spot-checked by the issuer at `opal_packager.py:176-205` |
| 5 | The commentary-ready dead letter holds 1 message (depth counts read; the message itself is unread) | measured (live) | `get-queue-attributes` |
| 6 | The r34k resident build record names two pins and does not say which the tarball carries; the base pin `0485393f` has a packager calling `produce_package` under another logical id and no `produce_commentary_pdf` | measured (code) | worker 292 T5, rows W292-S1 and W292-S2 |

## 2. What is NOT established (owed to IB2's reads)

Whether the RUNNING resident carries the commentary-PDF producer; whether its journal shows packager refusals for the two requests that have a draft; whether the resident has the commentary-ready queue bound; whether the drafter Lambda has its model and queue settings set; the age of the dead letter. Until those return, **why the two drafted requests have no PDF is unknown**. The most likely causes in order of what the code shows: the deployed resident is on the older packager pin, or the packager refused with a closed code (T4 lists them), or the dead letter holds that message. Each is a guess until IB2's R1 to R5 read.

## 3. What Andrew's Retry will record and show today (before any fix)

- **The ticket will record** the report reference of the READY job (the publication checkpoint holds a `report_ref`) with `revision` as a string, through the report-record route that PROD carries. Not read by the issuer: the portal's own Retry call on the served page.
- **The report link:** the report's artifacts exist (3 items); I expect the report link to answer. Not exercised by the issuer.
- **The commentary link: it WILL refuse `COMMENTARY_PDF_NOT_RETAINED`.** For his request the cause is claim 2: the commentary was never requested for this request, so no draft, no `commentary_ref`, no PDF exist, and the route (now reading the ref, release r36) answers the closed refusal with no URL. This is the correct answer for a request with no commentary. For a request WITH a draft (the synthetic one) the refusal stands for claim 3's reason (no PDF retained).
- **Each refusal:** commentary link = `COMMENTARY_PDF_NOT_RETAINED` (closed code, no URL). No other refusal is expected from the commentary route for his request. The original-upload link is not part of this trace.

## 4. What a fix would be (not cut; its own WORLD cell and pair after IB2's reads)

Two separate gaps. (a) **For Andrew's own ticket to show a commentary**, the accepted record must carry `commentary_requested: true`. Why his record lacks it is NOT established: either the filing page did not send the optional field, or the issuing function dropped it. The code that admits the field is commit `74bbdbb322` (IB-pr-455, in `ycharts/generate/acceptance.py` and the submission validator); which package of the issuing Lambda (the `irpt-ycharts-generate` family) carries that commit is NOT read by the issuer (the status Lambda's package, released as r36, is a different function). (b) **For any drafted request to get a PDF**, the resident must run a packager that retains under the route's logical id (claim 6, IB2's R1). Both are served-world acts needing a pair; neither is cut here. The next reads that would settle (a): the portal's filing payload keys on DEV and PROD (a code read), and the issuing function's live member list (IB2).
