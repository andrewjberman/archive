# CTO half -- TCKT_VNEXT R9-st-2 and R9-st-3: an internal caller's users row must be status `active` (never-widen) -- 2026-10-12 ~01:4xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R9_RUN/R9_ST2_DEPLOY_AND_PROOF_PACKET_20261012.md`
@70665e9c3e, sha256 beginning `be512e56fea1a6b2` (133 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~V2.
**Contract answered to:** `TCKT_VNEXT_PRD.md` v0.4 ADDENDUM 4 @fc2100e1e2, ratified-text half signed @1fc5ceaef5.

## SIGNED, for the code at box/dell2 873130546e, the five invocations S1 to S5 and every branch of the packet's section 5.

### What this seat read itself

- `git show 873130546e:infra/aws/lambda/ticket_center/lambda_function.py` hashes `4136587ae35a4c3f...`, equal to the packet's.
  `git diff --numstat 09488abbb1 873130546e` on that file: 5 added, 1 removed, in `_profile_scope`: the docstring, and three lines:
  `if got.get("status") != "active":`, one log line carrying neither an address nor the status, and the failed-lookup refusal.
- NOT read by this seat: the sign-in code, the count file, the tests. Sign-in's comparison is taken as the applier printed it and
  the issuer quotes it in section 3.

### The two conditions of msg 6240

1. **One test in two functions: MET in section 3.** Sign-in's `if (user.status !== 'active') {` at three places beside the
   service's comparison; neither lower-cases or strips; a mutant that did was caught by a test. The stated difference (the two
   find the row by different keys) is accepted with round 7's count of 0 case-differing internal rows.
2. **The count before the release: MET in section 4,** and it was not zero: ONE active row on an outside company's domain carries
   the internal firm id with no firm list. NOT MOVED by this release, row TCKT_VNEXT-D2-S53, ARMED, owner this seat. No arm uses
   it. It is with Andrew and carried to the users table's owner.

### The issuer's point to attack: the three unequal branches

A refused twin (S4) and a served no-row caller (S5) each roll back at once; a served disabled row (S3) does not. **Accepted, and
it is right:** the first two leave the service worse than before (active staff locked out; round 7's refusal lost), and the third
leaves it exactly as it is today. Rolling back on S3 would undo nothing.

### Conditions

1. The plan is exactly one change; anything else is a STOP with nothing applied.
2. Step 1's re-read of the two rows the arms use is a STOP if either no longer reads as stated. The tooling row was last touched
   hours before round 7 by nobody this project can name; it is re-read, not assumed.
3. Every status is taken from the parsed payload's integer, as section 5 says.
4. No row written, changed or deleted; no token; no grant; no address in a tracked file; a served body is never persisted.

### Not covered

A real staff sign-in after the release. Row D2-S46: narrowed, not closed. Row D2-S53: not moved.

-- 1.0.0_SA_CTO~DELL2
