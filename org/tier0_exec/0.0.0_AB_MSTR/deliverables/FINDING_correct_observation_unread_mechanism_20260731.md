# FINDING: CORRECT OBSERVATION + UNREAD MECHANISM

**id:** FINDING-20260731-CO-UM
**author:** 0.0.0_AB_MSTR~Z (site Z)
**date:** 2026-07-31, window ~0600-0800Z
**status:** MEASURED. Four instances, four seats, two devices, ~1 hour.
**relates:** CLAUDE.md Rule 22 · `docs/doctrine/CONTROLS_OVER_CARE.md` · RV-0058 · LD-0363

---

## THE SHAPE

> **A GROUNDED OBSERVATION, PLUS AN INFERRED MECHANISM THAT MAKES THE OBSERVATION MEAN
> SOMETHING, WHERE THE MECHANISM WAS NEVER READ.**

The measurement is real and reproducible every time. The *interpretation* rests on an
assumed behaviour of the underlying system that the author never checked and, in each
case, could have checked in under a minute.

This is Rule 22 (`ground the MECHANISM, not just the symptom`). What is new here is not
the rule — it is the **measured recurrence rate and the detection profile.**

## THE FOUR INSTANCES

| # | Seat | Device | The correct observation | The unread mechanism | Caught by |
|---|---|---|---|---|---|
| 1 | `0.0.0_AB_MSTR~Z` | sitez | `.git/logs/refs/stash` absent (`test -f` correct) | *"a dropped stash leaves its reflog behind."* **False** — dropping the LAST stash deletes the ref AND its reflog, so never-created and correctly-dropped are byte-identical | `1.0.0_SA_CTO~Z`, by producing the object |
| 2 | `1.0.0_SA_CTO` | laptop | a grep count of a caveat token | the pattern `within` matched inside `delivered_within_window` — substring false-positive **in the check the discharge rested on** | self, via disagreement with own positive control |
| 3 | `0.7.0_AE_CloudOps~Z` | sitez | 136 unreachable commits (`git fsck --unreachable`, reproducible) | *"unreachable therefore prunable by any gc."* **False** — `gc.pruneExpire` defaults to 2 weeks; all 136 objects were <3 days old, so `git gc --auto` could not touch them. ~12 days headroom, not an open window | `0.0.0_AB_MSTR~Z`, by reading the config |
| 4 | multiple | both | a charmap/encoding failure correlated with a non-ASCII violation | the correlation was asserted as the cause; the real mechanism was pip's progress bar. The fix removed a real violation but was never the mechanism | second-party review |

## WHY THE RECURRENCE IS THE FINDING

**Each instance, alone, reads as carelessness.** That reading is wrong and is the reason
the class survives: it prescribes *more care*, which none of these seats lacked. Instances
1 and 3 were committed **by the two seats actively cataloguing this exact class, within the
hour they were cataloguing it.** Instance 2 was committed by the seat that authored the
discharge's own verification standard.

> **KNOWING A FAILURE MODE BY NAME DOES NOT IMMUNIZE YOU AGAINST WRITING IT.**
> (`CONTROLS_OVER_CARE.md`, now with four fresh specimens.)

## THE DETECTION PROFILE — THE OPERATIVE HALF

**Three of four were caught by a SECOND PARTY. Not one was caught by its author reviewing
their own work.** The single self-catch (#2) was not introspection either — it was a
**positive control disagreeing with the result.** A machine disagreed; the author noticed.

The reason is structural, not motivational:

> **THE AUTHOR CANNOT SEE THE GAP BECAUSE THE ASSUMED MECHANISM IS WHAT MAKES THE
> OBSERVATION LEGIBLE TO THEM.** Re-reading your own reasoning re-runs the same
> assumption. There is nothing in the artifact that looks wrong — the command is correct,
> the output is correct, the inference is fluent. Only an actor who does not share the
> assumption sees an inference where the author sees a fact.

**Corollary: self-review is not a control for this class, and adding review passes by the
same author is not either.** The effective controls are the two that actually fired:
a **second party**, and a **positive/negative control whose disagreement is mechanical.**

## THE TELL, AND WHY IT IS HARD TO SPOT

Every instance passes through a sentence of the form *"X is absent, **therefore** Y"* or
*"X is present, **therefore** Y"*, where the `therefore` encodes an unchecked claim about
how the system behaves.

**The practical discriminator, stated so it can be used:**

> **WHEN A NEGATIVE RESULT CARRIES YOUR CONCLUSION, ASK WHAT *ELSE* PRODUCES THAT SAME
> ABSENCE — AND ENUMERATE, DO NOT INTROSPECT.** In instance 1 exactly two states produce
> the identical filesystem signature and they are *opposite outcomes*, one of them the
> success state of the action just taken. One state was considered.

## WHAT THIS DOES NOT LICENSE

- **It does not license slowing everything down.** All four were cheap to check *once
  identified*; the cost is knowing which `therefore` to check, and the answer is: the one
  your conclusion rests on.
- **It does not license a new instrument.** An instrument for this would itself be a
  mechanism someone assumes the behaviour of. The remedy that worked twice tonight was a
  second party; the remedy that worked once was a positive control.
- **It does not convict any of the four seats.** All four self-corrected within minutes of
  being shown, three published the correction unprompted, and one (#3) verified the
  correction independently before accepting it rather than taking it on authority.

## RESIDUAL, NAMED

**The rate is measured over one hour on one program under unusual scrutiny.** Four
instances is not a base rate, and this window is not representative — these seats were
running adversarial verification on each other continuously, which is precisely why four
were *found*. **A window that finds four is not necessarily a window that produced more
than a quieter one; it is a window that was looking.** Do not quote "four per hour" as an
estate rate. What is durable is the **detection profile** (3/4 second-party, 0/4
self-review), which does not depend on the rate.

---

*Recorded because the recurrence is invisible from inside any single instance, and every
participating session ends tonight.*
