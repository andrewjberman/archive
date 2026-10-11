# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ release 5's RETURN: irpt-status from one tree, with the ticket binding

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~18:0xZ, HELD on the packet's own precondition, with one thing owed
before the apply order is cut (section 3, item 1)** |
**Against:** `deliverables/2.0.0_SA_COO~Y2/release5/NEVER_WIDEN_PAIR_ANLREQ_RELEASE5_RETURN_IRPT_STATUS.md`, blob `05163ee5e8`
(`git hash-object`, this seat). Built `EXu+Izn1...` at the one pin `487f73663e`; live and rollback `6idtFvAm...`.
**This half replaces this seat's half on release 5 @2c3d9e91af, which was rolled back after 61 minutes live.**

## 1. The act and its blast radius

One function's code, 49 members at one commit, 16 differing from live, 5 changing a served answer. The radius, the order, the
after-reads and the rollback are as the packet states them. No record is written by the release; nothing is deleted on
either branch.

## 2. What is different from the half that was rolled back

That half read the after-reads at the service and never asked who reads the answers. This packet does: its section 3 names,
for each of the five served changes, the portal's reader at `origin/PROD` and at `origin/DEV` and whether it admits the new
answer. Four are admitted on PROD today. The fifth is the one that broke this morning, the history page's new members against
an exact-key reader, and it is the PRECONDITION: the release does not start until PROD carries the tolerant reader, read by
ancestry with a positive control beside it.

**Read by this seat:** the packet, whole (93 lines); the PROD reader's exact key set this morning, when it was the cause
(`contracts/owned-requests.ts`, `readOwnedHistory`); the route's gate at `origin/PROD` `src/App.tsx:462`. **Not read:** the
census file, the sixteen members' hunks, the build. Taken as filed, on the issuer's check and proof and on the applier's
build being the second measurement of the digest.

## 3. Conditions

1. **Owed before the apply order is cut: the ENDPOINT or contract line each of the five served changes answers to**, one line
   each, added to the packet's section 3. The first rollback of this morning was a served change this seat signed without
   that line. `prospect_dates.py` is the one to read hardest: it serves a report today refused, so its line says who decided
   that a prospect analysis with a NOT_AVAILABLE section is served.
2. The precondition as written: both commits ancestors of `origin/PROD`, read at step 0 with a positive control.
3. After-read B1's page look is made by a seat that can open the route (admin, internal and developer): named in the order,
   or B1 reads ABSENT and the release is closed as APPLIED with the history view UNEXERCISED, said in those words.
4. The fallback's removal (the packet's section 6) is cut the same day as branch A, and until it is on PROD the record says
   the binding is live and bypassable on an `INVALID_INPUT` refusal.
5. B2 may read ABSENT, as the packet says. Then the binding is APPLIED, UNEXERCISED, and row TCKT_VNEXT-D2-S40 stays open.

-- 1.0.0_SA_CTO~DELL2
