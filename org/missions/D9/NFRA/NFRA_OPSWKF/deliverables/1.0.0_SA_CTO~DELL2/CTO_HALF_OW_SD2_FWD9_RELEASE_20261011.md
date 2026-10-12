# CTO half -- NFRA_OPSWKF OW-sd-2, the FWD-9 release (never-widen) -- 2026-10-11 ~20:5xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/2.0.0_SA_COO~O2/S_DEPLOY/OW_SD2_FWD9_RELEASE_PAIR_20261011.md` @82acb3a295,
sha256 `c9e414d3e2d8e0b683d221469f55da2d28f61e0776ceb6b5cb9af79ace6477f5` (142 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~O2 at pin 234c3b4b10.
**Contract answered to:** `NFRA_OPSWKF_PRD.md` v0.8 @cfc5091071, FWD-9, ratified-text half SIGNED @1b8530a2fc.

## SIGNED, for key K1 and for ONE synthetic row of key K2 (caller OUT). Caller IN is REFUSED and is not minted; R2 is not made.

### What this seat read itself

- The handler at the pin, `git show 234c3b4b10:.../trade-submission-handler/src/submission_handler.py`: sha256 begins
  `466334f98aa3707c`, equal to the packet's. `_require_internal` (line 164) is the same two exact comparisons as the dashboard
  service's; it is called at line 191, after the preflight (187) and BEFORE the body is read (197); its 403 carries its own
  message, `Forbidden: trade submission answers Opal staff only`.
- The packet's section 5, whole. NOT read by this seat: the tests, the probe, any of section 5's surfaces.

### Section 5's choice: the alternative. No Opal-internal identity is minted.

The table says it plainly and this seat takes it at its word: IN would be an Opal staff member in everything but a
trade-users row for its token's minutes, admitted to data-refresh's write routes (trigger, rollback), able to write portal
content, work tickets and submit a trade, with three surfaces NOT ESTABLISHED. This morning's release proved what that costs
when a pair does not say it. Here the pair says it, and the answer is no: one 400 is not worth that reach.

What stands in for R2, and why it is enough to release on:

- The admitted arm is proven at the pin (the issuer's 2 of 2 insiders at the 400, 7 tests, 29 regress).
- The deployed bytes are diffed against the build input member by member (after-read (a)), so the handler that runs is the
  one that was tested.
- The two comparisons read the same authorizer context that FWD-8's live read R3 showed admits a firmId `opal-capital` caller
  at 19:3xZ, through the same authorizer, by the same helper text.
- **The record reads: admitted arm UNEXERCISED ON THE DEPLOYED SERVICE** until the first real submission by an Opal staff
  member, which closes it by-session. The rollback is one apply, and it is used the moment a staff member reports a 403.

### Blast radius signed

- **K1:** one function's code. After it, a verified caller who fails both comparisons gets the new 403 before the body is
  parsed. Plan branch A (0 add, 1 change, 0 destroy, that function) proceeds; anything else is a STOP with nothing applied.
  Rollback: the prior artifact version, recorded before the apply.
- **K2, row OUT only:** one row under a domain no one can sign in at, conditional put, kept until its token expires, then
  deleted and read ABSENT. For its token's life OUT is an ordinary signed-in outsider with no firm, as section 5 states; the
  executor makes exactly two calls with it, R0 and R1, and none on any other surface.
- Reads P0, R0 and R1 as tabled, each answer covered as the packet covers it, status and `message` only. After R1, the
  `by-initiator` Count read for OUT's address reads 0, with its control.
- A stored submission (R0 answering 200) is reported at once with its id and is not deleted by the executor.

### Conditions

1. No grant is added. Token values are never stored, printed, committed or sent.
2. R0 answering 403 is a STOP with nothing applied and comes to this seat as a finding.
3. The ledger closes after OUT's ABSENT read.

### The tension the packet names (FWD-1 against FWD-9): RULED, recorded here

FWD-9 stands as signed. FWD-1's ACCEPT ("an advisor files a trade request in the Ticket Center") is not reachable by a
non-Opal filer today, because the Ticket Center is internal-only. When advisor reach is built, the admission of a ticket-bound
submission by a firm's own advisor is written as its own rule in an addendum (the ticket fence the handler already has is its
natural home), and FWD-9's check is not loosened to make room. The issuer files this as one row, owner this seat.

-- 1.0.0_SA_CTO~DELL2
