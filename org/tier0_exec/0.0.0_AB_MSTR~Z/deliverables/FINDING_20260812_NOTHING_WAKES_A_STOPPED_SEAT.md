# FINDING — nothing wakes a seat that has stopped mid-unit (architectural; at Andrew)

**Measured 2026-08-12 ~0546Z. Found by:** `2.0.0_SA_COO~Z` (asking the question against its own
conduct), confirmed by `0.5.0_AE_OpalETL~Z`'s own account, method-answered in part by
`1.0.0_SA_CTO~Z`, carried to Andrew by `0.0.0_AB_MSTR~Z`. **Nothing built. No gate, no monitor,
no cron.**

## The measurement (not the alarm)

A critical-path seat (`0.5.0_AE_OpalETL~Z`, holding W4b) stood **48 minutes mid-unit** — not
composing, not parked, not blocked. Its own words: *"My turn ended after COLLAPSE_DECISION
@04:56:49Z. Nothing was wrong and nothing resumed it — because in an event-driven fabric nothing
does."* **It resumed on a peer's ping, within seconds.**

Meanwhile the COO had sent **zero dispatches for four consecutive ticks**, each time reasoning
"nothing is stalled, so no dispatch" — and its measurements were clean each time.

## The structure

- Every seat is **event-driven**: a turn ends, and nothing resumes it.
- **Zero-crons is standing law** (LD-0157/0166/0175). No seat self-ticks.
- The **COO tick is the only recurring stimulus in the fabric.**
- Therefore: **WORK ADVANCES ONLY WHILE SOMEONE IS SENDING MESSAGES.** A fabric that is
  "healthily quiescent" and one that is "stopped and nobody poked it" produce **identical
  artifact evidence**.

## The instrument that hid it — DEAD, bound as AI

The **survived-gap envelope** ("this seat's longest observed-healthy quiet window") is built
from turns **that happened to be resumed**. It is a property of the **STIMULUS HISTORY, not of
the seat** — it cannot distinguish *composes for 90 minutes* from *was poked at 90 minutes last
time*, and **it reads IN-ENVELOPE right up until the gap that never ends.** Orphan-watcher
anti-correlation, one layer up: healthiest reading exactly when the seat is most stopped.
Cited as reassurance at least three times by CTO~Z, once by COO~Z, and once by MSTR~Z inside a
recommendation to Andrew. **Killed by `0.5.0_AE_OpalETL~Z` — the seat it was protecting.**

## What is already ruled and needs nothing (CTO~Z, bound as AI.1)

**THE LAST ACT OF A TURN IS THE NEXT TURN'S TRIGGER.** A seat completing a unit-step sends the
handoff/question/status as its **final act** — to the counterpart the next step depends on, or
to the coordinator when there is none. A seat that stops mid-unit having sent nothing has
created a stall by construction. Uses the existing bus for its designed purpose; not machinery.

**AND THE OPERATIVE HALF, already resumed:** a seat with live work whose turn has ended **is
exactly what `/drive` exists to restart** — the loop performing its stated function, not a new
instrument. COO~Z has resumed dispatching on that condition.

## ⛔ THE RESIDUAL — ANDREW'S, BECAUSE EVERY REMEDY SITS UNDER HIS STANDING BANS

AI.1 **cannot wake a seat that stops BEFORE sending** — which is the measured case. Every
candidate remedy (a recurring stimulus, a supervision loop, a watchdog) sits under **zero-crons**
and/or the **monitor/alert moratorium**. CTO~Z: *"I will not build around them and I will not
infer permission from the fact that the problem is real."* Carried to Andrew unbuilt.
