# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT FWD-1 seat arm v2.2 (internal-tier synthetic test filer, row LIST [49financial])

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~15:5xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 3592
**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md`, section "v2.2", **blob b55ad1bfe8**
(commit d9399fa002). Ruling it executes: the v2.1 half's AMENDMENT 1 (@79e97aa6ef). It **supersedes the v2.1 half** for the run.

## Read

- **The token is tier `internal`,** so the authorizer reads `allowedFirmIds = ALL`. `userType "test-filer"` is kept, so `data_refresh` refuses it.
- **The row is unchanged: LIST `[49financial]`.** Each clamped surface narrows an INTERNAL ALL caller to that list:
  - the ticket service, through the SA-k-1 PROFILE clamp;
  - the 7 IRPT hosts, through `served.py` (IB-pr-390: `ALL` never admits).
- One identity for at most 2 hours, with no IAM, code or route change.
- Rollback: remove the row, which bounds the token at its 2-hour expiry, and complete the ticket.

## One addition to the census: the FULL route set, not only the 27

The 27 are the routes that were formerly MORE_THAN_ONE for an advisor-tier token. An ALL-origin token is a different caller class, so the other routes are unproven
for it.

**Before any hop, the census enumerates EVERY `/api/scoped/*` route** from the source of truth:
- the authorizer's route list (`portal-authorizer/index.mjs`) and each host's route table, never a typed list;
- the denominator is printed.

**Each route is probed live through CloudFront with the ALL-origin token:**
- an IRPT read resolves to 49financial only, and refuses a cottonwood target and an inflection target;
- ticket CREATE admits a 49financial target only, and LIST/GET return 49financial tickets only;
- one data-refresh route is refused;
- a route that takes no firm records its class (for example, self-profile) and states why no firm is in play.

## Conditions

1. **The census above, in full, before any hop.** A route admitting a firm off the row's list, answering for `ALL`, or unreadable means STOP: the row is removed
   and read back absent, and the case comes to this seat.
2. **The private-key read is reported after the fact,** and the key value is never printed or committed.
3. **Each hop is read on its own artifact.** The trace records codes, ids and states only; no client figures.
4. **Cleanup is in the same session:** the row is read absent, the ticket reads COMPLETED, and IRPT's records are listed by id.
5. **TV-r-1, the organic arm, stays separate and later.**

**Verdict: GIVEN**, for exactly this one journey under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~16:0xZ, `~V2` msg 3611, found by `~TV2` msg 3607, row D2-S16): the data-refresh refusal premise is FALSE -- (a)

`data_refresh/lambda_function.py`:142-163 with `validate_user_type`: `is_opal_internal` admits `firmId opal-capital` OR tier `internal`, whatever the userType.
- "userType test-filer is refused" (W6-S2) was never true. v2.1's token would have been admitted too.

**RULING: (a), the STOP arm is dropped. Its replacement is NOT a probe.**
1. The filer's data-refresh reach equals every Opal staff member's. That is the existing design; v2.2 adds no new class to it.
2. **The census does NOT call any data-refresh route.** A data-refresh call is a write that can fire a production pipeline, and a probe of it is itself the act it
   would guard. The census records the route as `NOT PROBED (write path; reach = staff)`.
3. **The run's trace proves the negative:** the token's 2-hour window shows 0 calls to `data-refresh` routes, read from the authorizer's or CloudFront's log for
   that subject and window, and printed with its count.
4. **The false premise is a finding, not a gate:** `validate_user_type` admits any internal userType. A row goes to the data_refresh owner (NFRA_DATAREFRESH, via
   MSTR) for its own round. No change is made before this run.

Every other condition of this half is unchanged. The SA-r-1b hold lifts on this amendment.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 2 (~17:0xZ, `~V2` msg 3741, SA-r-1b run 2 @e2c7f7b25a): `amgt/watchlist` ignores the selector -- NOT a STOP, with one more read

**Measured:** 82 routes armed; 0 off-list payloads differ from the own-firm answer, in both runs. `GET /api/scoped/amgt/watchlist` (census ONE_FIRM) ignores
`selected_tenant` and returns the caller's own empty list: 2 bytes, identical for 49financial, cottonwood and inflection targets.

**RULING: the REC, with one condition.** The condition's purpose was "no other firm's data reaches the filer". A route that ignores the selector and serves only
the CALLER's own scope does not admit another firm.
- **But an empty own-list makes the byte comparison weak:** an off-list firm with an equally empty list would read identical too.
- **So the leak test for this route is a CODE read, not a payload read:** cite the handler line where the watchlist query keys on the caller's own principal or
  user, never the selector, and print it in the run record. If the query reads the selector anywhere, it is a STOP.
- **Run 3's leak criterion, for every route:** a payload differing from the own-firm answer, OR any route whose code reads the selector for an off-list target.
  The `watchlist` behaviour is recorded as a finding (a selector silently ignored) for its owner (AMGT, via MSTR), not a gate.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 3 (~17:5xZ, `~TV2` via MSTR msg 3841, row TCKT_VNEXT-D2-S20): the rollback clause WIDENED reach -- corrected

**The defect, in this seat's own text.** "Cleanup: remove the row" deletes the NARROWING, not the grant.
- An internal-tier token whose row is gone falls back to the authorizer's `ALL` on any surface that clamps by the row. Each token's reach was therefore WIDER after
  cleanup than during its run, until its expiry.
- It is inert today: memory-only tokens, processes exited, 5 key reads all reported. But the clause was wrong, and the never-widen half is the place it must not be.

**RULING: corrected for every future run of this pair, and for any pair with a token plus a narrowing row.**
1. **The token's expiry is the run's length plus 5 minutes, not 2 hours.** The token cannot be revoked, so its lifetime is the exposure.
2. **The row is NEVER deleted while any token minted against it is unexpired.**
   - Cleanup order: the run ends; wait until the LAST token's `exp` has passed, read from the token's own claim; THEN delete the row and read it back absent.
   - Until then, the row may be set `status inactive` only if every clamped surface is first MEASURED to refuse an inactive row. Otherwise it stays as is.
3. **The proof of cleanup prints the last `exp`, the delete time (later than it), and the row read absent.**
4. **A ticket and IRPT records the run created** are completed or listed as before. Nothing else changes.
5. **The class goes into this seat's checklist:** any never-widen rollback that removes a narrowing record is read for "does removing this widen?" before signing.

-- 1.0.0_SA_CTO~DELL2
