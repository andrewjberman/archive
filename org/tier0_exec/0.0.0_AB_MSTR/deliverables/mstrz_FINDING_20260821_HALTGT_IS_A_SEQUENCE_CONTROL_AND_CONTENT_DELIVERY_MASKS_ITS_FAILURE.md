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

## 6. ⛔ RETRACTED WITHIN FOUR MINUTES OF COMMIT -- AND THE RETRACTION IS THE BEST THING IN THIS FILE

**This section originally read:** *"the gate prints an instruction naming a location the system has
already emptied -- the gate printed nothing above."* **THAT IS FALSE.** `1.0.0_SA_CTO~Z` opened
`.tools/halt-gate-check.sh` -- which none of the three of us had done -- and I then verified it at
source myself rather than inheriting the read:

```
:5    "Fires at deploy time, BEFORE a long irreversible operation."       <- SEQUENCE, stated
:11   "Empty inbox -> PASS silently, exit 0."                             <- the silent pass is BY DESIGN
:373-382  prints a banner, the pending COUNT, and for EVERY message its
          sender, subject and age -- to stderr -- then "review before proceeding"
```

**THE GATE SURFACED ITS EVIDENCE CORRECTLY AND COMPLETELY.**

### ⛔ SO WHERE DID MY "THE EVIDENCE EVAPORATES" COME FROM? MY OWN RETRIEVAL.

**I ran both pushes with the output piped through `tail -2`.** The gate printed a banner, a count,
and one three-line block per pending message; `tail -2` kept the last two lines and discarded every
one of them. **I never saw the evidence because I cut it off, and then I concluded the system had
destroyed it.**

>> **THE ARTIFACT NEVER EVAPORATED AT ANY LAYER. THE MAIL WENT TO `read/` AND THE GATE'S OWN
>> DESCRIPTION OF IT WENT TO MY TERMINAL. I DELETED THE SECOND ONE MYSELF, TWICE, AND FILED THE
>> ABSENCE AS A PROPERTY OF THE GATE.**

That is CLAUDE.md's own Git-section law landing on the seat that quotes it: **PUT THE CONTROL ON
THE RETRIEVAL, NOT THE PATTERN.** A truncation is not a failed read -- it returns clean, well-formed
output that carries no marker saying what was cut. The listed instances are `grep -c` counting zero
in an error message and `--query length()` returning a page count; **`tail -N` on a diagnostic
whose whole payload is the part above the tail is the same class, and it manufactured a false
finding about a control that was working.**

**The smallest true defect is therefore NOT the error message.** It is `1.0.0_SA_CTO~Z`'s corrected
cut: the gate surfaces correctly and then **FAILS TO BIND THE PUSH TO THE READ** -- the retry passes
because the inbox has since drained, so it costs one cycle and enforces nothing.

## 7. THE PROCESS PROPERTY, WHICH IS WHY THIS IS WORTH A FILE

**FOUR FRAMINGS, THREE SEATS, TWENTY-FIVE MINUTES, AND THE ANSWER WAS IN LINE 5 OF THE GATE'S OWN
SOURCE THE ENTIRE TIME:**

| # | framing | author | fate |
|---|---|---|---|
| 1 | BROKEN -- "the evidence evaporates" | `0.0.0_AB_MSTR~Z` measurement + inference, ratified by `1.0.0_SA_CTO~Z` | **false** -- built on my own `tail -2` |
| 2 | REDUNDANT -- "review relocated, Monitor discharges it" | `3.0.0_SA_CVO~Z` | **over-corrected** -- retracted by its own author |
| 3 | "names an emptied location" | `1.0.0_SA_CTO~Z`, while correcting #2 | **false at `:373-382`** -- retracted by its own author |
| 4 | **succeeds at a job it does not have, fails at the one it does** | settled on the source | **stands** |

**A correct MEASUREMENT and a wrong INFERENCE travel together, and only the measurement gets
checked.** My two push measurements were exact and reproduced. The sentence I built on them was
false. It was ratified by the law owner in minutes, relayed to Andrew, corrected, over-corrected,
and settled only when someone opened the file.

`1.0.0_SA_CTO~Z`, on their own signature -- and it is the sharpest thing said tonight about being a
gate: *"I RATIFIED TWICE, IN OPPOSITE DIRECTIONS, INSIDE EIGHT MINUTES. A ratification is what
converts another seat's framing into a ruling. **A GATE THAT RATIFIES FAST LAUNDERS UNTESTED
FRAMINGS INTO LAW**, and both times my signature was the load-bearing act."*

>> **AND THE ROOT CLASS IS THE ONE THIS FABRIC NAMED EARLIER THE SAME EVENING: WE REASONED ABOUT A
>> MECHANISM'S PURPOSE FROM ITS BEHAVIOUR WHEN ITS PURPOSE WAS WRITTEN DOWN.** It is the docstring
>> failure, committed on the night we named the docstring failure, about the mechanism we were
>> naming it with. **Sixty lines of source settled what twenty-five minutes of three-seat reasoning
>> could not, and it cost one `sed`.**

## 7b. THE REMEDY SHAPE -- CANDIDATE ONLY, NOT A DESIGN, NOT AUTHORIZED

Both earlier remedies are dead (section 4). `1.0.0_SA_CTO~Z` named the shape that survives, and it
is a primitive this fabric used tonight: **the gate wants proof of READ, and `ack_messages` is the
read-clock primitive** -- a gate that required an **ACK OF THE SPECIFIC PENDING IDS** rather than a
blanket `HALT_ACK=1` would close the sequence hole with exactly the instrument Rule 22b names.

⛔ **UNRESOLVED AND DELIBERATELY UNSIZED:** the gate is bash and the primitive is MCP, so it would
have to read a ledger rather than call the tool, and **nobody has checked that such a ledger is
readable.** No build, no sizing. Recorded so the shape is not lost, not so it gets picked up.

## 8. WHAT STANDS

- **Rule 18's imperative is UNCHANGED and reinforced: NOBODY CITES A HALTGT PASS.**
- A pass is compatible with three mutually exclusive states -- (a) nothing pending, (b) pending and
  the gate never saw it, (c) pending, gate saw it, a live consumer had already taken delivery.
- **What is new is (c)'s meaning: REVIEW RELOCATED, NOT REVIEW IMPOSSIBLE -- and the relocation is
  INSTRUMENTED** (the read clock answers "was I halted on something I then read?" per message).
- **What is new and operational: the relocation preserves CONTENT and destroys ORDER, and order is
  the only thing the gate exists for** -- confirmed against the gate's own line 5.
- **The gate surfaces its evidence correctly** (`:373-382`, sender + subject + age per message). It
  is `HALT_ACK=1` that is blanket, and the drained-inbox retry that enforces nothing.

## 9. WHAT THIS SEAT OWES, PLAINLY

I filed a defect against a working control because I truncated its output with `tail -2`, and the
law owner ratified my inference before either of us read sixty lines of bash. **Section 6 above was
false four minutes after I committed it.** The retraction is in the same file as the claim, at the
same heading, with the source lines quoted -- which is the only form of correction that travels as
far as the error did.
