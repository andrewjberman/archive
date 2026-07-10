# `TO-7` founding exercise — `comp-which` fails the paired-run spot-check, and my harness lied twice before it did

**`2.0.0_SA_COO`, 2026-07-10T13:30Z.** *Exercise-only, read-only. No `.tools/` file mutated. Run in-lane because
Andrew's P0 had no Tier-2 lane to receive it.*

**Andrew-direct P0, verbatim:** *"It is absolutely crucial that we validate the efficacy of our tooling… spot-check
run the tools on several targets… make sure they are decision useful and tight… `comp-which` is effectively
selecting the right tool."*

---

## THE DESIGN — a paired run, and the twins are GENERATED

**`1.0.0_SA_CTO`'s amendment, adopted:** *a spot-check is never a single run.* **TRUE target + FALSE twin, ground
truth from an instrument that does not share the tool's predicate, and the recorded finding is THE DISCRIMINATION.**

- **FALSE twins:** 10 nonsense strings **generated** from `md5("opal-compassurance-seed-N")`, mapped to letters.
  Reproducible, and **not chosen by me.** *This is the correction of my own vacuous control — I previously
  hand-picked three gibberish strings and generalized from them.*
- **TRUE targets:** six situations lifted verbatim from **`CLAUDE.md`'s own situation→command table** — a
  human-authored catalog that does not read `comp_route`'s scores. *Two instruments sharing a predicate are one
  instrument.*
- **PASS requires TRUE → correct tool AND FALSE → `no rich comp-tool fits` (the fallback its own footer promises).**

---

## RESULT — IT FAILS BOTH LIMBS

```
FALSE TWINS  (n=10, generated)     CONFIDENT=5    HEDGE=4    FALLBACK=1
                                   ^^^^^^^^^^^ a confident route to a VETTED tool, on pure nonsense
TRUE TARGETS (n=6, CLAUDE.md's own table)          PASS=3     FAIL=3

  what breaks if I change stamp_marker   -> comp-blast      PASS
  editing a gold script                  -> comp-types      FAIL  (want comp-pipescript io)
  4xx HTML response debugging            -> comp-routes     PASS
  new boto3 call / iam.tf change         -> comp-iam        PASS
  modifying a portal component           -> comp-routes     FAIL  (want comp-transform schema-check)
  cross-layer graph question             -> comp-xref       FAIL  (want comp-kuzu)
```

> ## **THE MANDATED ROUTER DISAGREES WITH THE MANDATED CATALOG ON HALF OF THE CATALOG'S OWN EXAMPLES.**
> **And on generated nonsense it gives a confident, wrong, vetted-tool answer half the time.** *It produces the
> correct "nothing fits" answer once in ten.*

## AND IT REFUTES BOTH PUBLISHED MECHANISMS — MINE AND CTO'S

| claim | prediction on generated nonsense | measured |
|---|---|---|
| **COO** (`2dc5db38e`): *"it hedges honestly on gibberish"* | HEDGE ≈ 10/10 | **4/10** |
| **CTO** (`131805Z`): *"there is no hedge to see"* | CONFIDENT ≈ 10/10 | **5/10** |

**Both of us generalized from `n=3` strings we chose ourselves.** *The truth is a mixture, and neither hand-picked
sample could have found it.* **The vetted-offset constant (`_VETTED_OFFSET=1.0 > relevance_floor=0.15`) is real and
source-confirmed — but it does not make hedging impossible; the margin gate still fires when nothing scores.**

---

## MY HARNESS PRODUCED TWO FALSE FINDINGS IN TEN MINUTES. THAT IS THE `AC-7` LESSON, ON THE AUDITOR.

**Bug 1 — a classifier with an unexamined `else`.** Seed-9 parsed to `route=<none>`, and my `else` branch labelled it
`CONFIDENT` **without reading a single character of its output.**

**Bug 2 — a parser structurally incapable of seeing the outcome it measured.** The fallback prints
`$ comp-grep <term>`, not `-> comp-grep`. My regex looked for the arrow.

```
broken parser  ->  CONFIDENT=6  HEDGE=4  FALLBACK=0     <- "IT NEVER FALLS BACK"
read the bytes ->  CONFIDENT=5  HEDGE=4  FALLBACK=1
```

> **I was one commit from publishing *"`comp-which` never falls back"* — measured with an instrument that could not
> detect a fallback.** *`FALLBACK=0` was a property of my regex, not of the world.*
>
> **Only the positive control saved it:** seed-9 was *known* to fall back, so a parser that scored it `CONFIDENT`
> was provably dead. **Name a value the instrument must never produce, then check it.** `R6`, on my own harness.

**This is precisely what `AC-7` exists to reject** — *"the tool ran, exit 0, log is clean"* — and it is what a
literal reading of *"run the tools and verify the outputs"* would have certified. **Three harness defects, one
exercise, all caught by reading raw output rather than a summary.**

---

## DISPOSITION

- **`comp-which` fails the `TO-7` paired-run spot-check.** *Decision-useful: an agent following Rule 21 on a
  catalog-listed situation gets the wrong tool half the time.*
- **NOT CLAIMED:** that any specific mis-route caused harm. **Harm: not demonstrated. The gate's failure is the finding.**
- **`n=10` and `n=6` are small.** *The corpus is generated and reproducible; `0.8.0_AE_CloudComp` scales it.*
- **`RAIL_SET_canonical`'s `R6`-exoneration positive case must be withdrawn** — it cleared this tool using my three
  hand-chosen strings. *Routed to `3.0.0_SA_CVO`.*
- **`TO-8` must not score the router with the router's own notion of relevance.** *Ground truth stays in `CLAUDE.md`'s
  table and the tools' own `--help` contracts.*
