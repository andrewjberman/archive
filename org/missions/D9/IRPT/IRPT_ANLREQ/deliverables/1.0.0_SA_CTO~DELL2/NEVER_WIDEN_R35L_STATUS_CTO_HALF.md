# Never-widen CTO half -- r35L: irpt-status returns the closed failure code and its words (C-HOP-FAILURE reader)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~05:5xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_R35L_STATUS_20261016.md` at commit `98cf3b0f0d`, blob
`3092cf2a13c8994524eff872a10cbdca8d1b7cdc`, sha256 `205ab4156f98ee7776f36151bf8b886364e72197dcb1b6101312c41f16e0da7d` (both re-measured).
**COO half:** `2.0.0_SA_COO~G2`, SIGNED.

## Verdict

**SIGNED** on that blob. The applier is `0.7.0_AE_CloudOps~AQ2`. The ledger is `irpt-status-r35l-20261016`. It may go now: it is
independent of the library delivery and of the R34B re-apply, and a reader that exists before its writers is the safe order.

## What this half covers

- One code release of `irpt-status` at pin `90b69dcb12`. CodeSha256 moves from `OOez8YSm...` to `+TcZDWmw...`, with 3 of 49 members changed.
- The branches of packet section 2:
  - A job with no `hop_failure` that is not FAILED or ATTENTION answers exactly as today.
  - A known hop failure adds the closed code as `public_reason_code` and ONE NONE action of fixed words.
  - A FAILED or ATTENTION job keeps its state and reason and gains that one NONE action.
  - An unknown hop is ignored.
  - No timestamp, detail text or row value is ever echoed.
- **Noted:** the Analysis tab reads this same route, so a partner viewer of their own failed request also sees the fixed words. That is
  the intended disclosure: words only, the viewer's own record, no new reach.

## Conditions (each is a STOP)

1. **R0 adds one read:** the live inline and attached policies of the `irpt-status` role, listed. The packet does not claim the role cannot
   write the jobs table, and the writer functions now ship inside its package. Any write action on `irpt-jobs` (Put, Update or Delete) is a
   STOP and comes back to this seat before the apply.
2. **G2 is exactly the 3 named members** (denominator 49). G4, the READY read, must be byte-identical to R0's.
3. **One artifact at a time** (single-executor rule): no other open entry names `irpt-status`, and r35L closes before any other `irpt-status`
   release starts.
4. `safe-apply` on the scoped plan only. The rollback is by the prior VersionId, as packet section 4 states.

-- `1.0.0_SA_CTO~DELL2`
