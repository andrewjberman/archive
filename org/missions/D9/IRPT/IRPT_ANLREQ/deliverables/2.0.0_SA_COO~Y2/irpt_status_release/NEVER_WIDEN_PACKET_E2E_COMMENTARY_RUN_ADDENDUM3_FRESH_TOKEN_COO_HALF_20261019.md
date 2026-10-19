# ADDENDUM 3 to the never-widen packet for the synthetic commentary end-to-end run -- run 4 uses a FRESH upload token and distinct holdings bytes (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-19. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` (blob `394e573a4ae5902b4121626c31a0c605c35e8968`) and its ADDENDUMS 1 (blob `02149564860419fbcb11e3add00de8617282af32`) and 2 (blob `5bddf32c3b213142e35f4d882fe6114de3c55fc3`). **Ledger:** `irpt-commentary-e2e-4-20261019`. **Authority:** CTO ruling ADDENDUM 4 (msg 10731): "Run 4 uses a fresh token and distinct bytes."

## 1. Why

Run 3 (IB2 receipt `A_E2E3.txt`, issuer-graded 17, 0, CLOSED) reused run 2's upload token. My run 3 order never said "fresh token"; that omission is the issuer's. The upload id is derived from the firm, the principal and the token (`intake/uploads.py:371`), so run 3 re-posted run 2's already-resolved or already-queued upload, and its five `RESOLVING` answers with 0 resolve journal lines say nothing about a new upload. Run 3 also left the same original-holdings blob as run 2 (rows `IRPT_ANLREQ-D2-S211`, `-S214`: the application has no deleter).

## 2. The change to the pair (everything else in the packet, ADDENDUMS 1 and 2 and all the CTO's conditions stands)

| step | change |
|---|---|
| R0 | adds: the upload token to be used and the sha256 of the holdings bytes to be used are printed and compared with the tokens and hashes recorded in the receipts `A_E2E2.txt` and `A_E2E3.txt` and `LEFTOVER.txt`; a token or hash equal to an earlier run's is a STOP before any write |
| A | the synthetic staff user is `fwd1-commentary-e2e4-20261019@opal.invalid` (not an earlier run's address) |
| A2 | the synthetic advisor is minted with `fwd1_advisor.py mint --date 20261018` (address `irpt-w5-advisor-20261018@opal.invalid`). It is NOT the date `20261017` of runs 2 and 3 and NOT `20261019`: Monday's window-5 advisor `irpt-w5-advisor-20261019@opal.invalid` must not exist yet or be touched (CTO ADDENDUM 1, condition 1). R0 reads both the `20261018` and the `20261019` advisors ABSENT first. The upload carries `advisor_email=irpt-w5-advisor-20261018@opal.invalid` |
| U | the `upload_token` is FRESH: a newly generated random value of at least 16 bytes, hex or base64, generated in memory at the moment of the first post and never written to a file or message (only its first 6 characters and its sha256 are printed). The holdings bytes are DISTINCT from the earlier runs': the window-5 five-row file with the `Dollars` value of the `SPY` row changed from `100` to `101` (header and the other four rows unchanged); the receipt prints that file's sha256, which must differ from `30d44443701df5f92dfee4def4d1a1f139818ee416601b2577c66e30fb3b96a1`. The five-post re-post rule of ADDENDUM 2 is unchanged and uses this one token. A fifth `RESOLVING` stops with the elapsed time and the `RESOLVE`-literal count; the literal and the table or queue to read are those that `TO-AR-y-407` (worker 298) names in `X3` and `X6`, which IB2 reads from `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~298/r56/RESOLVE_PATH_TRACE.md` at HEAD when it reaches the step (if that record is absent, the receipt counts the literal `RESOLVE` and says so) |
| K | the receipt line `K same_art_key` compares this run's original-holdings object key with the keys in `LEFTOVER.txt` of runs 2 and 3 and must read `no` (a fresh token and distinct bytes give a different upload id by `uploads.py:371`); a `yes` is a STOP at U |
| D | as in ADDENDUM 2; the leftover original-holdings blob of this run is filed as a surprise row with the object key, owner `2.0.0_SA_COO~Y2`, like `S214`; no IAM change |

## 3. Blast radius delta

None beyond the packet and ADDENDUMS 1 and 2: one more synthetic user, advisor (distinct date) and upload, and one more standing original-holdings blob (the application has no deleter, `D2-S211`).

## 4. Order of work at IB2 (the CTO's ruling)

The resident release for the 425-cards fix (`TO-AR-y-404`, build cell `TO-AR-y-406`) goes first in IB2's queue; run 4 follows it and never runs alongside another IB2 apply or install. If the release restarts the resident, run 4's `R0` reads the then-running root and records it.

## 5. Not claimed

- That a fresh token resolves. The resident's resolve path is under trace (`TO-AR-y-407`); the positive control for the live path is Andrew's 13:43Z filing, counted by a separate read-only order, not by this pair.
- That the staff user can read the commentary route for the advisor-owned request (ADDENDUM 1 section 4).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-19, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 and 2. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
