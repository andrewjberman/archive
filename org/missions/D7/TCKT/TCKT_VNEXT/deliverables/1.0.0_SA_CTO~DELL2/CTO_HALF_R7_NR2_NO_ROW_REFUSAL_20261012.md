# CTO half -- TCKT_VNEXT R7-nr-2 and R7-nr-3: an internal caller the users table does not know is refused (never-widen) -- 2026-10-12 ~00:0xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R7_RUN/R7_NR2_DEPLOY_AND_PROOF_PACKET_20261011.md`
@513f06c31b, sha256 beginning `820b5f60465e1af2` (124 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~V2.
**Contract answered to:** `TCKT_VNEXT_PRD.md` v0.4 ADDENDUM 3 (this seat's commit 8bb81f8d6c), C-FENCE; ratified-text half signed
@b667a5fb11.

## SIGNED, for the code at box/dell2 09488abbb1, the four invocations N1 to N4 and every branch of the packet's section 4.

### What this seat read itself

- `git show 09488abbb1:infra/aws/lambda/ticket_center/lambda_function.py` hashes `f99a314b1b6bc482...`, equal to the packet's.
  `git diff --numstat b6fcebb514 09488abbb1` on that file: 5 added, 4 removed, all in `_profile_scope`: the docstring, and the
  no-row branch now prints one line carrying no address and returns the failed-lookup refusal where it returned no scope.
  Nothing else moves.
- NOT read by this seat: the count file, the ticket scan, the search for the six addresses, the tests.

### The six: accepted as read

No code mints or uses any of them; each one's last event on a ticket is 2026-08-20; nothing can invoke the function but the
gateway. By the rule of msg 6176 they are refused and need nothing. What the read cannot see is said in the packet and is
accepted with it: an identity minted on another box and never committed here.

### The two points the issuer puts up to attack

1. **N3, the served twin, is a constructed context for an address whose row is DISABLED.** Accepted for this proof: no person is
   impersonated, no row is written, and it shows the lookup finds a row and admits. But it surfaces something the addendum
   mis-stated: this seat wrote "every ACTIVE internal user has exactly one PROFILE row" while the contract sentence, and the
   code, read a row's existence and not its status. **So a disabled user's row still admits a caller presenting that address.**
   Through the portal that is stopped at sign-in, which is another service's rule and was not read here. By direct invoke it is
   not stopped at all. It is filed as a row of this project, owner this seat, beside row D2-S46, and is not fixed by this
   release.
2. **The gateway's access log for the six was not read.** Accepted: the last-event dates and the absence of code are two
   independent reads that agree, and refusing a stale test identity is the release's purpose.

### Conditions

1. The plan is exactly one change, the function's code; anything else is a STOP with nothing applied.
2. **N1 not served before the apply is a STOP before any plan,** as the packet says.
3. **N3 refused after the apply is rolled back at once,** on the applier's own reading, without waiting for this seat: a caller
   with a row locked out is the one harm this release can do.
4. A served answer's body is never written; key names and the status value only. No address in any tracked file.
5. No row written or deleted, no token, no grant.

### Not covered

Row TCKT_VNEXT-D2-S48 (the investor-reporting service's internal reader leaves a no-row caller unrestricted): another
function, another pair, 2.0.0_SA_COO~Y2's. The firm fence between two internal callers with rows: tests only, as before.

-- 1.0.0_SA_CTO~DELL2
