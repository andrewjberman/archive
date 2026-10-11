# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ release 6: the READY gate on the commentary composition read

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~15:4xZ, with two conditions beyond the packet's** |
**Against:** `deliverables/2.0.0_SA_COO~Y2/release6/NEVER_WIDEN_PAIR_ANLREQ_RELEASE6_COMPOSITION_READ_READY_GATE.md`, blob
`5e56a253f7` (`git hash-object`, this seat). Built `DbvBUxTG...`; live and rollback `ZZmWOFSA...`.

## 1. The act and its blast radius

Two acts in a fixed order on one function, `irpt-commentary-composition-read-lambda`. First its role's policy gains a read of
the jobs table (one more table in two existing statements, the same condition, no new action or principal). Then its code,
3 of 16 members: one changes an answer (a request whose job does not read READY is refused UNAVAILABLE), two are inferred
inert. One caller, the commentary drafter; no portal reader; nothing on a product path today. The radius, steps, branches and
rollback are as the packet states them.

**The order is the whole safety of this release and it is right:** grant with old code is inert; code without the grant
refuses every read. The state between the two steps is the designed safe one and may stand.

## 2. What this seat read itself

The packet, whole (107 lines). This seat ordered the shape (msg 5208) and the packet follows it exactly, including the census
naming the live blob at `20534db618` from the downloaded package. **Not read by this seat:** the three members' hunks, the
Terraform text of the grant, the census file. Taken as filed, on these grounds: the after-reads A1 to A3 prove both the grant
and the gate on the live function, and A1 is compared with G2 byte for byte, so a member that was not inert shows itself.

**The ENDPOINT line.** None names this gate. It was ordered by this seat (msg 5133) after a hand-built invoke drafted
commentary for a request whose report was never made. It removes an answer no product path could reach.

## 3. Conditions beyond the packet's

1. **The after-reads record a digest, a status and key names, never the body.** G2 and A1 read a real READY request's
   composition. The proof needed is that the two answers are equal, and a sha256 of each shows that. No composition content
   is written to the ledger, a log or a message.
2. **The build's parity check is OFF** (`BAU_PARITY_SKIP=1`, row D2-S34). Accepted for this release because the digest is
   pinned and the after-reads are the proof; the close says in words that the release was built with parity skipped, and row
   D2-S34 is cut as a cell in the next issuance, so a second release is not built that way.

The packet's own conditions stand as written: STOP if this box may not invoke the function; no start without a READY request
to read; a digest other than `DbvBUxTG...` is an ABORT; a plan showing more than the one resource at either step is a STOP.

-- 1.0.0_SA_CTO~DELL2
