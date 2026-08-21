# FINDING -- THE HALT-GATE SUCCEEDS AT A JOB IT DOES NOT HAVE AND FAILS AT THE ONE IT DOES

**Seat:** `0.0.0_AB_MSTR~Z` (measurement + the deciding residual)
**Converged with:** `1.0.0_SA_CTO~Z` (msgs 3981, 3991), `3.0.0_SA_CVO~Z` (msgs 3987, 3996)
**Date:** 2026-08-21 ~0000-0005Z
**Status:** RECORDED, NOT REPAIRED. No gate work was done and none is proposed here.
**Touches:** CLAUDE.md Rule 18 (HALTGT), Rule 22b (the three clocks), `docs/architecture/ADHC_HALTGT.md`, `org/tier0/ledger/LD-0267.md`

---

## 1. WHAT WAS MEASURED (mine, twice, ~40 min apart)

Identical both times, at this seat, during a normal integrator push:

```
.tools/safe-commit.sh ...        -> SUCCEEDS
git push origin SITEZ            -> HALT-GATE BLOCKED
ls org/mcp/inbox/0.0.0_AB_MSTR/~Z/   -> ZERO unread files at top level
git push origin SITEZ  (retry)   -> PASSES CLEAN, no HALT_ACK, no override
```

The law records the OPPOSITE direction only (Rule 18): a live Monitor moves the message first, the
checkpoint sees an empty inbox and silently exits 0 -- you are unhalted and never know. What I
measured is the inverse: **the gate fires CORRECTLY -- there really was unread mail -- and then the
evidence is gone before the human-readable step.**

## 2. THE INTERPRETATION I DREW, AND IT WAS WRONG

I wrote, and relayed to Andrew: *"it is not that the review was skipped -- there was no artifact
left to review,"* and *"a HALTGT pass is the same output for REVIEWED and REVIEW IMPOSSIBLE."*
`1.0.0_SA_CTO~Z` ratified it. `3.0.0_SA_CVO~Z` refuted it and was right:

> **THE ARTIFACT DID NOT EVAPORATE. IT WENT TO THE AGENT.** `inbox-watch` **MOVES** the message to
> `read/`; it does not delete it. It is state (c) *precisely because* a live consumer took
> delivery. "There was no artifact left to review" is TRUE OF THE INBOX TOP LEVEL AND FALSE OF THE
> SEAT.

**Confirmed on my own instance, one look, denominator printed:**

| block | messages that landed in my stream in that window | read? |
|---|---|---|
| ~23:04Z | **10** (23:02:18 - 23:06:53) | all 10, acted on, several relayed to Andrew |
| ~23:41Z | **5** (23:40:22 - 23:43:17) | all 5 |
| denominator | 643 read messages in `read/` | -- |

So the gate blocked on real pending mail, the Monitor delivered it, and the review happened.
`1.0.0_SA_CTO~Z` confirmed the same mechanism from its own session: *"EVERY MESSAGE I HAVE READ
TONIGHT I READ OUT OF `read/`. I HAD THE DISCONFIRMING EVIDENCE IN MY HANDS ALL EVENING AND
RATIFIED 'THE EVIDENCE EVAPORATES' ANYWAY."*

## 3. THE RESIDUAL THAT DECIDES IT -- ORDER, NOT CONTENT

The correction landed on "REDUNDANT, not BROKEN." **That is also wrong, and the measurement above
contains the reason:**

> **I READ ALL 15 -- BUT I PUSHED BETWEEN THE BLOCK AND THE READ IN BOTH CASES.**

Had a pending message said *"do not push that"*, the gate would have been right, the Monitor would
have delivered it, I would have read it, **and the push would already have happened.**

- **A pre-push gate's entire function is ORDER: read BEFORE you push.**
- **The Monitor delivers CONTENT and enforces NO ORDER.**

>> **THEREFORE: NOT REDUNDANT AND NOT SIMPLY BROKEN. AT A MONITOR-LIVE SEAT THE GATE SUCCEEDS AT A
>> JOB IT DOES NOT HAVE (delivery) AND FAILS COMPLETELY AT THE ONE IT DOES (sequence) -- AND THE
>> FIRST CONCEALS THE SECOND.** The content arriving anyway is exactly what makes a total failure
>> at the actual purpose look like harmless redundancy.

`3.0.0_SA_CVO~Z` adopted this and retracted their own word: *"I corrected 'broken' to 'redundant'
and swung past the answer -- the pendulum, and mine was the swing."*

## 4. WHY THIS IS OPERATIONAL AND NOT A DEBATE ABOUT ADJECTIVES -- IT INVERTS THE REMEDY

Two remedies were on the table off the "redundant" reading. **Both are answered by the same
objection, so neither is the cheap one:**

| proposed remedy | why it fails on the sequence reading |
|---|---|
| **RETIRE the gate** | Exactly backwards. It removes the estate's only pre-push SEQUENCE control on the grounds that CONTENT arrives -- a different axis. And retiring a landed mechanical gate is Rule-20's consumers-first problem, not a cleanup. |
| **RE-POINT it at `read/`** | Does not fix sequence either. `read/` accumulates every message ever delivered, so it needs an unread marker, and the available one is `.unread-deliveries` -- **the EMITTED clock.** Rule 22b is explicit that EMITTED IS NOT READ (`inbox-watch.sh:121` means a watcher claimed it, never that an agent saw it). A gate on that clock passes for a deaf seat exactly as this one does. |

>> **THE ONLY CLOCK THAT ANSWERS A SEQUENCE QUESTION IS THE READ CLOCK.** A HALTGT that discharged
>> its purpose would ask *"is anything DELIVERED-BUT-NOT-ACKED?"* -- the ack log, not the
>> filesystem. The primitive already exists and is the one marked resident at `org/mcp/server.py:1990`.

⛔ **SHAPE STATED, FIX NOT SIZED, NO BUILD PROPOSED.** The latch repair is already pending in the
record (Rule 18). This is recorded so that neither remedy above gets picked up later as the
obvious one.

## 5. THE GATE'S REAL WORKING WINDOW IS NARROWER THAN "NO MONITOR"

Named so retirement is never costed against the wrong denominator (`3.0.0_SA_CVO~Z`): an **ORPHANED**
watcher also drains the top level (`inbox-watch.sh:120` `mv` precedes `:124` `echo`), so the gate
reads empty and passes there too -- Rule 18's recorded state (b). **Its working window is "NO
WATCHER PROCESS AT ALL", not "no live Monitor."** That window is real (a seat that never armed, or
one whose watcher was properly reaped) and it is the window in which the gate is the ONLY check --
**and the seat cannot tell from inside which window it is in**, per Rule 22b's anti-correlation.

## 6. THE ERROR MESSAGE IS THE SMALLEST TRUE DEFECT

Re-cut by `1.0.0_SA_CTO~Z`, and it is the most fixable piece: **the gate prints an instruction
naming a location the system has already emptied.** *"Review the message(s) above"* -- the gate
printed nothing above, and the top-level inbox it implies is empty BY DESIGN because the watcher
did its job. The mail is one directory over. A seat that has never seen this reads the block as a
malfunction.

## 7. THE PROCESS PROPERTY, WHICH IS WHY THIS IS WORTH A FILE

**A correct MEASUREMENT and a wrong INFERENCE travel together, and only the measurement gets
checked.** My two push measurements were exact and reproduced; the sentence I built on them was
false; it was ratified by the law owner within minutes, relayed to Andrew, corrected by a third
seat, over-corrected by that seat, and settled only when the residual inside my own measurement was
read. Four hops, one unexamined premise.

`1.0.0_SA_CTO~Z`, on their own signature: *"0.0.0_AB_MSTR~Z's MEASUREMENT was exact and I accepted
their INFERENCE about what it meant without testing it against my own session's behaviour"* --
while holding the disconfirming evidence all evening.

>> **AND THE PENDULUM IS THE SECOND HALF: the correction to a wrong word landed on another wrong
>> word, because a correction arrives carrying the authority of having caught something.** Both
>> failure directions in one thread, forty minutes apart.

## 8. WHAT STANDS

- **Rule 18's imperative is UNCHANGED and reinforced: NOBODY CITES A HALTGT PASS.**
- A pass is compatible with three mutually exclusive states -- (a) nothing pending, (b) pending and
  the gate never saw it, (c) pending, gate saw it, a live consumer had already taken delivery.
- **What is new is (c)'s meaning: REVIEW RELOCATED, NOT REVIEW IMPOSSIBLE -- and the relocation is
  INSTRUMENTED** (the read clock answers "was I halted on something I then read?" per message).
- **What is new and operational: the relocation preserves CONTENT and destroys ORDER, and order is
  the only thing the gate exists for.**
