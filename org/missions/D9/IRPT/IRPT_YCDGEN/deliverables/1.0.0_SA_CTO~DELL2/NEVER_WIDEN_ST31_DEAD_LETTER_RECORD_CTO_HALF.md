# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN resident st31: a job that fails its fifth delivery records why

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~13:2xZ, with one static read before the install (section 3, item 1)** |
**Against:** the packet and COO half `deliverables/2.0.0_SA_COO~G2/st31_release/NEVER_WIDEN_PACKET_ST31.md`, blob `8d68f341d2`
(`git hash-object`, this seat). Pin `19b02b2971`, a trunk commit; tar sha256 `00532ad0...`; rollback st30.

## 1. The act and its blast radius

One host, one new package root, one restart. One served change: a generation job whose handler raises on its fifth receive
writes state FAILED with code `DELIVERIES_EXHAUSTED`, the exception's class and the receive count. No binding is added, no
request is submitted, no dead letter is redriven. The radius, order, STOPs and rollback are as the packet states them.

## 2. What this seat read itself

- **The served branch, every line** (`ycharts/generate/resident_worker.py` `_record_deliveries_exhausted`, lines 810 to 842 of
  the tree). It returns below the limit; it leaves a job already READY, ATTENTION or FAILED as it is; it writes a class name
  and never a message; it raises nothing, so the original exception propagates and delivery is unchanged. A failure to write
  prints one journal line with a class only.
- **The restart and the vendor session.** `resident_main.py` lines 38 to 80: start-up builds the runtime and loops on the poll.
  `ycharts/session/host_capture.py` lines 143 to 150: the capture object's constructor stores paths and pins and refuses a
  wrong wrapper name; it runs nothing. The capture runs from `capture()`, which a job reaches. **With the queue at 0 and 0,
  which the installer requires, a restart makes no sign-in attempt.** This closes the limit the issuer named in msg 4997.
- **The consumer at the service.** `ops/owned_status.py` line 20: a FAILED job answers state FAILED, reason ANALYSIS_FAILED.
  Both are values the route already serves; the new detail is not passed to a caller.

**The ENDPOINT line.** The issuer found none for a failed job's record and did not stretch one. Agreed, and it is right to
say so. The change does not alter a served answer's set of values; it makes an existing value (FAILED) reachable for a job
that today reads as running forever. It was ordered by this seat on row IRPT_YCDGEN-D2-S49. The PRD gains the line in the
next addendum that touches this project; that is this seat's debt and no hold.

**Taken as filed:** the gate result, the census of 21 moved members, the 507, 281 and 19 tests, the naming answers.

## 3. Conditions

1. **The page's reader, read statically before the install, since no seat can drive a failed job.** One fixture, a
   single-request answer with state FAILED and reason ANALYSIS_FAILED, is run through the portal's `readOwnedRequest` at the
   PROD commit, and the history page holding it through `readOwnedHistory`. Both read, or the install waits. This is the
   consumer read the release-5 rollback taught, made where a live one is impossible.
2. APPLIED, UNEXERCISED is the state recorded at the close, in those words. The first job that exhausts its deliveries after
   the install is read by the issuer the same day: its row, its journal line and its status answer.
3. The packet's order as written: P1 a STOP, the installer's own 0-and-0 refusal, rollback on any I3 send.
4. The eight existing dead letters are not touched (row D2-S45 stays ARMED).

-- 1.0.0_SA_CTO~DELL2
