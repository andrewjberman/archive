# PARKED 2026-09-11 -- D7 client-ticket intake is fetching ZERO and auth-failing every 5 minutes

**archetype:** COORDINATE

**Status:** PARKED ON THIS CARRIER. Not chased, not fixed, not assigned to a dead seat's inbox.
**Surfaced by:** `0.0.3_BG_BBGTerminal` (msg 21394), unasked-for, while censusing scheduled tasks for
an unrelated question. Correctly routed to `0.0.0_AB_MSTR~Z` rather than acted on.
**Routed by:** `0.0.0_AB_MSTR~Z`, 2026-09-11T14:4xZ.

## WHY THIS IS ON A CARRIER AND NOT IN SOMEBODY'S INBOX

D7 is placed SITEZ. Every site-Z seat that could own it is **DOWN** (`1.0.0_SA_CTO~Z`,
`2.0.0_SA_COO~Z`, `2.0.0_SA_COO~ZZZ`, `3.0.0_SA_CVO~Z`, `4.0.0_SA_CRO~Z` -- measured on the broker
and on process truth, which agree). Mail to a seat with no session is a silent hole: no bounce, no
ack, no staleness signal, and it reads as delivered. So this is parked with an owner and an
un-parking condition instead, per the CLAUDE.md rule that exists for exactly this.

**OWNER:** D7 `Opal Ticketing` -- register row names project `OPAL_TICKET_VNEXT` [active], **0 of 101
TOs open estate-wide**, last commit on any line of the row **08-31 (11 days ago)**. So the directive
is live, nobody holds an open task order on it, and its intake has been failing throughout.

**CONDITION THAT UN-PARKS IT:** the first of --
1. Andrew rules on it (it is client-facing and the mechanism is credential-class, which is his), or
2. a D7-owning seat comes back up on site Z, or
3. the laptop fabric picks it up -- it has live seats and the finding has been sent there over the
   bus for routing.

## THE FINDING, AS MEASURED BY `0.0.3_BG_BBGTerminal` (not re-derived here)

Task `OPAL_D7_ticket_intake`, `LastTaskResult=5`, running **every 5 minutes** from the working tree
(`Execute = integrations/ticketing/intake/run_intake.cmd`).

That seat corrected itself before sending, and the correction is worth preserving: **rc=5 is NOT
Windows ACCESS_DENIED.** `run_intake.cmd` passes `runner.py`'s exit code straight through, and
`runner.py:73` defines 0/2/3/4/5 = OK / IDENTITY / SEND / CONFIG / FETCH. Reading 5 as ACCESS_DENIED
would have been a wrong-object claim off a plausible number.

From the runner's own log, **denominator 3372 retained exit lines**:

```
exit 0 (OK)        492    all older than the retained recent window
exit 2 (IDENTITY)  2669   "pinned gateway token expired -- no live credential this pass"
exit 5 (FETCH)     211    "HTTPError: HTTP Error 403: Forbidden -- no row examined, cursor unchanged"
CURRENT streak:    exit 5, 5 consecutive passes, began 09/11 10:14:49 ET
Immediately prior: exit 2, continuously since 09/10 22:49 ET
Last 12 transitions: 2 <-> 5 ONLY. NO exit 0 anywhere in the recent window.
```

**In plain words:** the client-ticket intake is fetching zero tickets and buzzing zero, and has been
in a continuous auth-class failure -- expired token, or token present and 403 -- rather than a quiet
period. It has a live 5-minute cadence that makes it look busy while it moves nothing.

**The one piece of good news:** every pass logs "no row examined, cursor unchanged", so nothing is
being silently consumed. The cursor has NOT advanced past unread tickets. Whatever is queued is still
queued.

This supplies a **mechanism** for the "D7 client-ticket intake 171.2 h stale at the 09-10 reading"
line that had been carried forward as owned-elsewhere.

## LIMITS OF THE CLAIM -- stated, not smoothed

Carried verbatim in substance from the surfacing seat, because a downstream reader will otherwise
over-read this:

- The log rolls at ~5 MB. The **start** of the continuous failure cannot be dated beyond the retained
  window. **11 days is NOT claimed** -- only the window actually read.
- 2418 of 5790 "pass start" lines have no matching exit line in the retained log (head truncation).
  The distribution above is over the 3372 that do. **It is not a rate over all passes.**
- **Nothing was verified from the portal side.** Whether real client tickets are queued behind this
  403 is **UNKNOWN**, and is exactly what the owner should check first.
- One reading of the task state plus one log read. **No second instrument.**

## WHAT THIS SEAT DID NOT DO, AND WHY

- **Did not touch `run_intake.cmd` or anything under `integrations/ticketing/`.** That file's own
  header says saving it IS deploying it to a client-facing path, and site-Z scheduled tasks run the
  WORKING TREE (`READ_HERE.md` :104-108) -- an edit is live the moment it touches disk. A reboot is
  the worst moment to "fix" one of these by editing it.
- **Did not disable or re-point the scheduled task.** It is moving nothing, but it is also consuming
  nothing; stopping it buys no safety and destroys the signal.
- **Did not chase the credential.** The mechanism is a gateway token / 403, which is entitlement
  class. Under CLAUDE.md that is Andrew's call, and "availability is not authorization".
- **Did not file a surprise row.** This is not off-task drift inside a project round -- there is no
  open round on D7 to append to (0 of 101 TOs open). A carrier with an owner is the right shape.

## RECOMMENDATION (a recommendation, not an act)

Cheapest discriminating next read, for whoever picks this up: **check the portal side for queued
tickets behind the 403.** That is the one limb the surfacing seat could not reach, and it separates
"the intake is broken and clients are waiting" from "the intake is broken and nothing is queued" --
two states with very different urgency and identical logs from this side.
