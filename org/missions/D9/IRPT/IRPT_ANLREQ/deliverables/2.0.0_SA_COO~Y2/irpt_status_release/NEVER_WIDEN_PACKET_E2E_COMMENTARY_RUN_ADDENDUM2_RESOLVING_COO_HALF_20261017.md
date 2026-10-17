# ADDENDUM 2 to the never-widen packet for the synthetic commentary end-to-end run -- the identical upload is re-posted while the door answers RESOLVING (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-17 ~20:5xZ. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` (blob `394e573a4ae5902b4121626c31a0c605c35e8968`, CTO half `f0fbfde004`) and its ADDENDUM 1 (blob `02149564860419fbcb11e3add00de8617282af32`, CTO half `fec24f492d`). **Ledger:** `irpt-commentary-e2e-3-20261017`.

## 1. What the second run found (IB2 msg 10666, receipt `A_E2E2.txt` commit `93ece7b175`; issuer graded: E2E2-AC1 16, AC2 0, AC3 CLOSED)

With the advisor named, the door AUTHORIZED the actor and answered the upload `RESOLVING` (state `RESOLVING`, `input_id` null; `intake/uploads.py:486-516`): the service accepted the file and queued it for the resident to resolve (`uploads.py:547-` the resident half). `RESOLVING` is a WAIT, not a refusal. The portal itself handles it by re-posting the IDENTICAL request (same upload token), at most `UPLOAD_MAX_TRIES = 5` times with `UPLOAD_WAIT_MS = 3000` between tries, and files nothing unless a try answers `NORMALIZED` (`portal/src/pages/TicketCenter/analysisRequest.ts:79-82, 361-373`, AR-y-144, CTO ruling 4). The first-run packet's "one upload try" and the CTO's condition 3 ("no second upload is tried") were written for a door REFUSAL; read literally they also stopped this run at the first `RESOLVING`. IB2 stopped there and said so.

## 2. The change

Step U re-posts the IDENTICAL upload request (same body bytes, same upload token, same `advisor_email`) while the answer is `RESOLVING`, at most 5 posts in all, 3 s apart, exactly the portal's own rule. The first answer that is `NORMALIZED` gives the `input_id` and the run goes on to step T. A refusal (any closed code other than `RESOLVING`), or the fifth `RESOLVING`, is a STOP at U with its code AND the elapsed time from the first post to the last answer (CTO msg 10668); no new token, no new file, no other upload. On a stop at `RESOLVING` after five tries, the receipt adds one count: the lines of the resident journal that name the upload-resolution step (`RESOLVE`) since the first post, with the journal window and total as denominator. Everything else in the packet, ADDENDUM 1 and the CTO's conditions stands.

## 3. Blast radius delta

None beyond the packet: the same one upload object and index rows, written once and re-read by identical posts (idempotent by token, `uploads.py:526`, a RESOLVING row is resumed). A second upload object is NOT created. The resident does one extra resolve step.

## 4. Known leftover, stated (no change asked)

The second run could not delete one synthetic blob: the upload's original-holdings CSV (118 bytes, key `irpt/49financial/state/original_holdings/ART-<id>/<file>.csv`), `AccessDenied` for IB2's principal (receipt `LEFTOVER.txt`); its index rows are deleted. Each run that reaches the upload leaves one such blob. Whether the retention policy expires it is NOT READ. It is listed by key in the receipt, as the CTO's deletion rule requires. No call is made to widen anyone's reach. Per the CTO (msg 10668), the third run's step D deletes that blob through the application's own deletion path IF a read finds one (cell `AR-y-402`, which principal the application deletes that prefix with, code and policy only); if it finds none, the object is recorded as a surprise row with an owner and the receipt lists its key. No IAM change either way. The receipt prints whether the third upload's original-holdings object lands on the SAME `ART-` key as the second run's (the key shape is in the second run's `LEFTOVER.txt`; the id is the repository's own binding of owner, family and logical id, `repository.py:390-395`).

## 5. Not claimed

- That the resident resolves the upload within five tries (3 s apart is shorter than the resident's 20 s long poll, `resident_worker.py:939-940`, so five tries may all answer `RESOLVING`; the portal has the same limit). If so, the stop at U with the journal count is the result, and the next step is the CTO's.
- That the staff user can read the route for the advisor-owned request (ADDENDUM 1 section 4).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-17, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUM 1. The write set is unchanged; the upload is re-posted, not re-created.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
