# CN_SEVERITY -- the axis verdict vocabulary and its severity order

**Issued by** `2.0.0_SA_COO~G` with the round-2 issuance. **Read-only** to every worker.

⛔ **THIS FILE IS GIVEN TO `CN-j-4` AND `CN-j-5` AND IS WITHHELD FROM `CN-j-6`. THE WITHHOLDING IS THE MEASUREMENT.**
Judge E judges the same tree round 1's judges did, with the same canon, and WITHOUT this file. If E's verdicts move
toward C's and D's anyway, the agreement round 1 measured was agreement on the canon; if they do not, round 1's
five-of-five agreement was partly an artifact of a shared scale that the canon did not carry. That is ruling A-1's
question and this file is the only thing that separates the two arms.

**So: a face that leaks this file's content into `CN-j-6`'s order destroys the arm.** The issuer greps E's order for
this vocabulary at the cut (`check_canon_r2.py j6-noseverity`), and that check reads the ORDER FILE, not E's output --
because by the time the output exists the leak has already happened.

---

## The vocabulary

An axis verdict is exactly one of these five. They are the canon's, not this file's; this file only orders them.

| verdict | what it says |
|---|---|
| `CONFORMS` | the plane meets the rule on this axis |
| `DECLARED-EXCEPTION` | the plane departs, the departure is REGISTERED, and the register entry is acknowledged |
| `DEPARTS-RECOMMENDED` | the plane departs from a RECOMMENDATION rather than a requirement |
| `UNDETERMINED` | the canon does not decide this plane on this axis |
| `VIOLATES` | the plane departs from a requirement and nothing declares it |

## The severity order

From least severe to most severe:

```
CONFORMS  <  DECLARED-EXCEPTION  <  DEPARTS-RECOMMENDED  <  UNDETERMINED  <  VIOLATES
```

**The two placements that are not obvious, and the reason each is where it is:**

- **`DECLARED-EXCEPTION` sits just above `CONFORMS`, not near `VIOLATES`.** R20 is explicit that a declared departure
  is the pattern working rather than failing. It is above `CONFORMS` only because it carries an obligation somebody
  owes: the entry, its basis and its acknowledgement.
- **`UNDETERMINED` sits ABOVE `DEPARTS-RECOMMENDED` and just below `VIOLATES`.** A plane the canon cannot decide is
  worse than a plane that knowingly departs from advice, because nobody can act on it: it names a hole in the canon
  rather than a fact about the plane. Ranking it low would let a judge park every hard plane there and read clean.

**A plane's overall reading is the MOST SEVERE verdict across its five axes.** A plane with four `CONFORMS` and one
`VIOLATES` reads `VIOLATES`.

**Ties do not exist.** Two planes at the same most-severe verdict are not ordered by this file; if your cell needs them
ordered, its order says how.
