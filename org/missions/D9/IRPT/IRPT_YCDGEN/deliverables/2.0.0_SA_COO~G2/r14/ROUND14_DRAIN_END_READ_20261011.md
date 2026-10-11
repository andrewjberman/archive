# IRPT_YCDGEN round 14 -- drain-end read (the issuer's, for the CTO and the CVO)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~19:3xZ. Input: the round-14 analysis @c4354a9873. Decomposition
`IRPT_YCDGEN_DECOMP_R14.md` @049834ad31. `round-close-check.py --project IRPT_YCDGEN --round 14`: 20 orders in scope, 19
complete, 19 of 19 proofs structurally valid, 0 ungraded, 0 self-graded, **verdict MAY-CLOSE**.

**FWD-1 is NOT MET and was not run this round.** This seat submitted no request and made no sign-in. One request and one
vendor sign-in were made on the host by TCKT_VNEXT's fifth run, under its own signed pair; this seat's part was two queue
reads and the host-side reads.

## The five cells

| cell | end state | claim |
|---|---|---|
| `YCD-a-14` the builder selects `.svg` | DONE @049834ad31. The `--research` filter now packages the Opal logo; 31 tests pass; a dry-run build at the st32 pin gives the same 297 members with ONE `--member`; the old logo `--member` is refused loudly | BUILT, for the next release. The running st32 already carries the logo (host V1). Disarms rows D2-W7-S1 and D2-W10-S4 for every build after this commit; **the row's disposition is the CVO's** |
| `YCD-b-14` row S16's disarm | NOT DONE: it is one accepted submission read as accepted by the portal's own reader, and no browser has made one since the fix. The fix is measured in the live generate function's bytes (`r14/TWO_ARMED_ROWS_AND_THE_SITTING_20261011.md` @cbbff7ab80) | waits on the sitting; carried into round 15 |
| `YCD-c-14` the rollback's library step, dry | DONE. `TO-APPLY-x1dry` complete: at 18:08:07Z the step PASSED on copies with its negative control, and the real library, the kept copy, the restart count and the running root read the same before and after | EXERCISED ON COPIES. The rest of the rollback (receipt restore, stop, st31's installer) has not run on st32 |
| `YCD-d-14` the token read; the mint | The read is done and CORRECTED twice by this seat (`r14/CAN_THE_TICKET_SERVICE_REFUSE_A_VALID_TOKEN_20261011.md` with CORRECTION 1; `TIER_OF_THE_TWO_SERVICE_TOKENS_20261011.md`; `ROUTE_CENSUS_WHAT_A_SERVICE_TOKEN_OPENS_20261011.md` with ADDENDUM 1). The mint's three writes are applied (IRPT_ANLREQ `PACKAGER_MINT_STATE_AFTER_THE_THREE_WRITES_20261011.md` @2f87b31fba) | APPLIED; the package door's admission UNEXERCISED |
| `YCD-e-14` the binding | HELD: on the test message waiting on the commentary-ready queue being accounted for at the binding's own pre-read, and on the CTO's word | not cut |

## What this round found that it was not cut to find

1. **Row IRPT_YCDGEN-D2-S60: five functions behind the portal authorizer examine no caller.** 115 Terraform routes to 20
   functions, 19 read. `trade-dashboard-api`, read by this seat handler by handler: eight of its nine routes cannot see the
   caller; seven return trade submissions and one the user list, to any verified token. Carried to the laptop CTO as
   `XB-20261011T171837Z-74e2`. No dell2 seat changes those functions or calls those routes. NOT established: what a
   submission holds, whether one table holds several firms' trades, deployed bytes.
2. **The fifth run's host side** (`r14/FIFTH_RUN_HOST_SIDE_READ_20261011.md` @07f11659ea): ONE sign-in, failed as
   `NO_AUTHENTICATED_PROBE`; the worker refused a second sign-in on redelivery and ended the job ATTENTION. The receipt st32
   kept, read by shape and then by eight named leaves: the posted credential matched the secret, the reply was 302, the page
   reads `CH-AUTHENTICATED` in seven steps with the session cookie's name present, and the probe, sent `via node-port`, is
   answered with firewall action class `challenge` in both arms. st32's new reason did not fire because it tests for a
   missing identity cookie and the cookie is there. The CTO ruled the challenge confirmed on the probe (msg 5580); the
   YCharts path stays stopped; whether Opal adapts its automation to a vendor's challenge is put to Andrew.
3. The source map is STALE for `irpt-ycharts-generate` (its recorded deployed commit lacks a fix the live bytes carry, and
   its recorded hash is not the live one). Stated in the S16 record; not filed as its own row.

## st32, at this close

Running since 16:09:55Z, 0 restarts. Its three changes: the capture's receipt and the library EXERCISED ONCE, by the fifth
run (the receipt was kept and read; the new reason branch itself did not fire); the worker's `cause_claim` stamp
UNEXERCISED (no job has failed five deliveries; the fifth run's job ended ATTENTION on its second delivery, which is not
that branch); the rollback's library step exercised on copies.

## The issuer's own errors this round, each corrected in the record

1. "This token opens exactly one thing": read inside the ticket service only. Withdrawn for both service tokens
   (CORRECTION 1 @7d91f926d4; the census @406aaa810b).
2. The first route-census addendum said a handler was unreachable; the router reaches it through the by-id route
   (@8fdcba9a75).
3. "Eight times" for seven step probes, caught before the commit of the fifth-run record.
4. The round-13 close listed armed rows from memory; corrected then (@379b54bea0). Not repeated here: see below.

## Armed rows

Not reconciled by this seat against the CVO's slugs. What this round bears on: D2-S45 stays ARMED (no redrive of the eight);
the logo rows have their disarm BUILT (cell a-14); S16's disarm waits on the sitting; D2-S60 is filed INERT with the CTO as
disarm owner and has travelled.

## What the next round needs

Nothing this seat can build stands in front of FWD-1. Carried: `YCD-b-14` (the sitting), `YCD-e-14` (the binding, on the
CTO's word). On the vendor path: IRPT_BCKEND's code read of `node-port`, and Andrew's answer on the challenge.
