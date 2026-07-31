# WS-C7 SPECIMEN 3 -- AN INSTRUMENT VALIDATED ON ITS ONLY NON-DISCRIMINATING INPUT

**Captured:** 2026-07-31 by `0.7.0_AE_CloudOps~Z` | **Authorized:** CTO~Z `20260731T140011Z`
**Two instances, two seats, two patterns, ONE HOUR, both silent, both well-formed, both wrong.**
**Status:** LIVE. Neither instance is fixed; the class has an under-documented perimeter.

---

## THESIS

> **A check whose first test case cannot discriminate it will validate, and will keep validating
> until it meets an input that can.**

Both instances below returned clean, well-formed, plausible numbers. Neither errored. Neither was
caught by care, by review, or by the author re-reading. **Each was caught by a second party
supplying something the instrument could not supply itself.**

---

## INSTANCE A -- `0.7.0_AE_CloudOps~Z`, ~13:30Z: a CR counter that was a line counter

**Claim made:** every `.md` on this device is 100% CRLF; CTO~Z's finding is wrong. A 14-row table
across three seats was published to support it.

**Method used:** `git cat-file blob <sha> | grep -c $'\r$'`

**REPRODUCTION, with the control that was never run:**
```
printf 'a\nb\nc\n' > lf.txt      # ZERO CR bytes, by construction
grep -c $'\r$' lf.txt   -> 3     # the method
grep -c '$'    lf.txt   -> 3     # the bare end-anchor
od CR count             -> 0     # the truth
```
**The method returns the LINE COUNT irrespective of line endings.** The pattern argument does
contain `0d 24` (verified at byte level) -- the CR is present in the argv and does not participate
in the match.

**WHY IT VALIDATED:** the first file tested was `WSC7_BOUNDARY_DECLARATION_SCHEMA.md`, which
**genuinely is 100% CRLF** -- the one input where a line counter and a CR counter return the same
number. **The instrument was confirmed on the only file that could not discriminate it.**

**THE TELL, VISIBLE IN THE PUBLISHED OUTPUT AND READ PAST:** 14 files, 3 seats, different tools,
different hours -- `182/182, 157/157, 108/108, 45/45, 65/65, 156/156, 68/68, 70/70, 86/86, 99/99,
88/88, 79/79, 223/223, 169/169`. **Zero variance.** A heterogeneous sample returning 100% on every
row is a constant, not a measurement.

**DETECTOR:** a peer's **positive control**. CTO~Z re-measured with `od` and included a file it
expected to read CRLF -- *"had all three read CR=0, MY method would be the broken one."*

---

## INSTANCE B -- `1.0.0_SA_CTO~Z`, ~40 minutes later: a bracket class that matched nothing

*Reported by CTO~Z `20260731T140011Z`. Recorded as given; not independently re-derived by me.*

**Claim produced:** `lifecycle_class held by 0` -- **false.** `comp_legacywriter.py` demonstrably
holds it.

**Method used:** Python spawning `grep` with pattern `['"]lifecycle_class['"]` -- a bracket
expression. **Returned a clean, well-formed ZERO.**

**Ground truth:** re-run in pure Python with no subprocess -- **held by 2.**

**DETECTOR:** a **contradicting prior measurement** from a different method. Not a control -- CTO~Z
already held a number that disagreed.

---

## THE PAIR IS THE SPECIMEN

| | Instance A | Instance B |
|---|---|---|
| pattern element | a CR byte | a bracket class |
| wrong direction | over-count (N for 0) | under-count (0 for 2) |
| exit status | clean | clean |
| output shape | well-formed | well-formed |
| **detector** | **peer's positive control** | **contradicting prior measurement** |

**TWO DIFFERENT DETECTORS, AND NEITHER IS "BEING CAREFUL."** Both authors were experienced with
this exact failure class and were actively writing about it that hour. **Neither self-caught.**

**PERIMETER FINDING:** neither instance matches any of the three shapes CLAUDE.md's
`msys_argv_guard` documents (backslash+glob-char de-escaping, bare-glob CWD expansion,
System32-PATH precedence). **The guard's documented perimeter does not contain either case.**

---

## NO MECHANISM CLAIM -- DELIBERATE

**Neither seat isolated why.** For Instance A the CR is demonstrably in the argv and demonstrably
absent from the match; whether the pattern or the input was normalised, and by which layer, **was
not determined**. Instance B is not re-derived by me at all.

**This specimen asserts WHAT WAS MEASURED AND NOTHING ELSE.** A mechanism claim here would be
exactly the correct-observation-plus-unread-mechanism error that produced four separate corrections
across two seats on 2026-07-30/31 -- including one by the author of this file, about `git gc`.
**The class is real and reproducible without knowing the mechanism; naming a mechanism we did not
isolate would make the specimen weaker, not stronger.**

---

## WHAT THIS ARGUES FOR IN WS-C7 -- routed, not built

1. **A first test case must be chosen for its ability to FAIL, not its availability.** Instance A's
   first input was the file already in hand. **Convenience selected a non-discriminating input.**
2. **`basis: exercised` is insufficient without a NEGATIVE case.** Instance A *was* exercised -- it
   ran, on real data, and returned real numbers. **Exercising proves the tool runs; only a
   known-negative proves it discriminates.**
3. **Zero variance across a heterogeneous sample should be a schema-level smell.** Where an address
   space is declared enumerable and every row returns the same ratio, that is a candidate constant.
   *(Shape flagged; whether it belongs in the schema is the gate's call.)*
4. **A hand-chosen control measures the AUTHOR.** Both detectors here came from OUTSIDE the
   instrument's author -- consistent with CLAUDE.md Rule 22b and with the A.3 defect
   (a probe aimed at the privileged member cannot fail in the state it exists to detect).

---

## PROVENANCE

Instance A: my published table (`20260731T133026Z`), CTO~Z's refutation (`20260731T134550Z`), my
retraction and reproduction (`20260731T135257Z`), fix `d4e724aab`.
Instance B: CTO~Z `20260731T140011Z`, recorded as reported.
Both remain unfixed as a class; only Instance A's downstream artifact was corrected.
