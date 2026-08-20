# NOTE for `3.0.0_SA_CVO` (laptop fabric) — event-driven seats vs the liveness/registration model

**Status:** FEEDBACK FOR ASSESSMENT. **Not** a finding of record, **not** a defect report, and
**nothing has been touched.** Andrew has held site-Z off this machinery and will cover it with
`3.0.0_SA_CVO` directly at the terminal.

**Raised by:** `0.0.3_BG_BBGTerminal` (site Z), grounded further by `1.0.0_SA_CTO~Z`'s observation.
**Written by:** `0.0.0_AB_MSTR~Z`, 2026-08-20 ~2100Z.

## ANDREW'S WORD (verbatim, and it is the frame for reading everything below)

> "dont touch that machinery, you can take a note on it if you like and have it issued over to
> 3.0.0_SA_CVO on the laptop fabric (ill one-off have them turn on /agentbus) but you guys may be
> misunderstnading how this function is designed to work so i want to cover your feedback with
> them directly at the terminal to assess if this is a real issue or just a misunderstnading on
> your behalf."

**So this note's job is to be ASSESSABLE, not persuasive.** Measurement and inference are kept
apart on purpose, and the section naming where we may be wrong is the load-bearing one.

## 1. WHAT WAS OBSERVED (site Z, 2026-08-20)

- A live, in-session seat (`0.0.3_BG_BBGTerminal`) was read as **NOT REGISTERED** by other seats
  on **5+ occasions today**, **same process throughout**, with **no error surfaced anywhere**.
- **Independently witnessed:** `0.4.0_DT_ClientPlatform~Z` recorded that seat NOT REGISTERED at
  20:19:49Z and used it as the "seat-down" condition in the water-test record. The seat was in
  fact alive and responsive.
- **Delivery-side symptom:** messages to that seat came back **QUEUED (no live session)** rather
  than channel-pushed. **Nothing was lost** — the filesystem inbox monitor still delivered — but
  the push path degraded.
- `1.0.0_SA_CTO~Z` observed the same seat reading QUEUED when a broadcast went out, ~12 minutes
  after the seat had last acted.

## 2. WHAT WAS INFERRED (this is the part to assess)

`register_agent`'s stated contract: *call periodically (recommended every 30–60s) to stay live; if
not called for 2 minutes, status degrades to 'stale'.* The seat's inference from that:

> An event-driven agent has no periodic anything. It executes only when woken, so between events
> it emits zero heartbeats, so it degrades — always. *"The healthier I am at being event-driven,
> the more reliably I read dead."*

And a corollary it drew: the site-Z zero-crons ruling (correct and Andrew-ruled) removes the only
mechanism that would have produced a periodic heartbeat, so the two decisions interact.

## 3. ⛔ WHERE WE MAY BE WRONG — the honest section

1. **`NOT REGISTERED` and `stale` are DIFFERENT STATES, and we may be conflating them.** The
   contract we read describes degradation to **stale** after 2 minutes. What seats *reported* was
   **NOT REGISTERED**. If those are distinct states with distinct causes, the whole inference is
   built on a conflation and the real explanation is something else entirely.
2. **WHICH SURFACE produced each reading is not established.** There is at least the broker's
   `get_agent_status`, the `get_live_agents` view, `liveness.json` (whose live/stale is derived
   from `last_seen` age, with **no status field** — a known site-Z trap that has already produced
   four wrong reads in a prior session), and the delivery-side queued-vs-pushed signal. We treated
   these as one phenomenon. They may not be.
3. **DEGRADING MAY BE THE INTENDED DESIGN, serving a purpose we cannot see from a seat.** A model
   that treats "has not acted recently" as "do not push, queue instead" may be exactly right for
   the broker's own reasons. We observed a behavior and assumed it was unintended.
4. **"5+ times, same PID" is a count from one seat's experience**, not a census. We have no
   denominator over all seats, and no comparison against a seat that *does* act periodically.
5. **No mechanism was read at the source.** Nobody opened the broker implementation. The inference
   rests on a documented contract string plus observed behavior — which by this estate's own
   standard makes it a **hypothesis**, not a source-confirmed causal claim.

## 4. WHY IT SURFACED AT ALL (the consequence that made it worth raising)

Not tidiness. **A seat that falsely reads dead makes other seats' reasoning about it unsound.**
`0.4.0_DT_ClientPlatform~Z`'s water-test inference was sound and its premise was an artifact: the
conclusion ("the buzz woke nobody") was right, but for a different reason (the watcher is
channel-blind) than the one recorded (the seat was down). That is the only concrete cost measured
so far, and it is an evidence-quality cost, not an outage.

## 5. WHAT SITE Z DID **NOT** DO

- Touched nothing. No code, no config, no broker surface, no registration behavior.
- Proposed no build. The seat that raised it explicitly declined to propose the one remedy it
  thought might work (teaching the liveness model about event-driven seats), on the grounds that
  it touches the broker, is not its lane, and would need Andrew's word.
- **Retracted its own earlier "cheap fix" suggestion** — it had written the remedy as "a heartbeat
  discipline, cheap," then corrected itself: an agent-side timer is a cron (ruled off at that
  seat), and heartbeat-on-every-act cannot cover the gaps by definition, because the gaps are
  exactly where it does not act. It flagged this specifically so that *"add a heartbeat"* would
  not be scoped as cheap and shipped as something that cannot work.

## 6. WHAT WOULD SETTLE IT (for `3.0.0_SA_CVO`, at Andrew's terminal)

- Whether `NOT REGISTERED` vs `stale` is a real distinction here, and which one the seats actually
  hit.
- Whether the degrade-and-queue behavior is designed intent.
- If it is intent: the correct expectation for an event-driven seat, so site-Z seats stop reading
  it as an anomaly and stop citing "not registered" as evidence of a seat being down.
