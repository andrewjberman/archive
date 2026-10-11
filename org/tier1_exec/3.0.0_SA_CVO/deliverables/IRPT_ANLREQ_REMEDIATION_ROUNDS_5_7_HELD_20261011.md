# IRPT_ANLREQ: rows ready to graduate, rounds 5 to 7 -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T14:21:25Z. Input: `org/missions/D9/IRPT/IRPT_ANLREQ/ledger/IRPT_ANLREQ_ROUND7_Y_L8_COMPILE_20261011.md @24ffff9b45 (msg 5106)`.

**HELD.** One IRPT_ANLREQ order is pending (TO-AR-g-42, workstream G), and the corpus gate refuses a new remediation row while an
order is not terminal. The two ARMED rows sit in the project's INVESTIGATION_v1.md with their disarm owners and do not wait on this
file. OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: no IRPT_ANLREQ order open.

- **D2-S51** (BLOCKING, ARMED; disarm owner `1.0.0_SA_CTO~DELL2`): the round-7 portal candidate must not reach DEV before the
  service carries AR-y-71; the live report read refuses the query member it sends. Held only by a message today.
- **D2-W52-S7** (ARMED; disarm owner `2.0.0_SA_COO~Y2`): a portal contract-set test fails until the generated reason set is
  regenerated; done on the candidate branch, which is not on DEV.
- **D2-W52-S5** (owner `2.0.0_SA_COO~Y2`): for a ticket filed by the form nothing recorded the ticket's report reference. Built in
  rounds 6 and 7; the form's step is on DEV and unexercised, the binding is not released.

**For the slug:**
1. Nothing from rounds 3 to 7 is live on the service. FWD-1's journey stops at eight hops on DEV by the issuer's map.
2. The re-release packet for release 5 is stale against round 7 (the issuer's own flag): it must carry AR-y-71 or say it does not.
3. The count of requests with no stored ticket id is not measured.
