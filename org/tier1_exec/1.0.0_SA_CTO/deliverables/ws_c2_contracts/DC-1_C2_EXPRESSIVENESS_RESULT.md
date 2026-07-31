# DC-1 -- WS-C2 DELIVERABLE CONTRACT: THE EXPRESSIVENESS RESULT

**Andrew-direct, 2026-07-31:** *"have CTO establish those four deliverable contracts now"* and
*"I want all contracts done and in a folder of deliverables ws_c1_contracts, then ws_c2_contracts,
and so on in the CTO deliverables folder."*

**Workstream:** NFRA_VELOCITY / CORE, WS-C2 -- expressiveness validation against the three corpora,
run BEFORE the types froze. **Author and gate:** `1.0.0_SA_CTO~Z`. **Verify:** `3.0.0_SA_CVO~Z`.
**Status: COMPLETE** (P1 closed 2026-07-31, clause by clause).

## AUTHORITATIVE vs DERIVED

**SOURCE OF RECORD:** the five step files below. **THIS DOCUMENT IS DERIVED** -- it consolidates a
verdict that until now existed only as five step files and a paragraph in a project JSON.
**Where this document and a step file disagree, THE STEP FILE WINS and this document is the defect.**

## WHAT WS-C2 WAS OBLIGED TO PRODUCE, AND WHERE EACH PIECE LIVES

| Obligation | Artifact | Vintage |
|---|---|---|
| Axis commensurability -- are the two schemes comparable at all? | `../WS-C2_STEP0_AXIS_COMMENSURABILITY.md` | rev 3 `@ee3673d89` |
| Instance cross-tab against the incident taxonomy | `../WS-C2_STEP1_INSTANCE_CROSSTAB.md` | landed |
| MSBEFF typed by class | `../WS-C2_STEP2_MSBEFF_BY_CLASS.md` | landed |
| M3 split + DEBTLOOPS round-trip | `../WS-C2_STEP3_M3_SPLIT_AND_DEBTLOOPS_ROUNDTRIP.md` | landed |
| Semantic read of the first real declarations | `../WS-C2_SEMANTIC_READ_01_WS-E1_TRANCHE1.md` | landed |
| The held-out fence stated IN the rail sections | rule bank `dynamic_rails.held_out_fence` | `@880f527cc` onward |

## THE RESULT

### The three corpora, with printed denominators

| Corpus | Denominator | Typed | Result |
|---|---|---|---|
| MSBEFF | **718** items, typed by CLASS not item | RECALL/coverage **363 = 50.6%** | **only 6.4% is tuple-typed** |
| Incident taxonomy | **210** rows | -- | **21.6% untypeable** |
| DEBTLOOPS | 9 same-day specimens | round-trip run | all nine expressible |

**The 210 is load-bearing and my first parse got it wrong.** I read 218; **14 of those are
*disposition* rows, not incidents** -- a mention counted as a use. The correction came from
reconciling against a count I did not maintain, which is the only kind that can contradict you.

### >> THE CEILING -- the single result that constrains everything downstream <<

> **THE RAILS TYPE WHERE AN ASSERTION SITS. THEY DO NOT TYPE INSTRUMENT FALLIBILITY, BY
> CONSTRUCTION.**

**Agreeing across all three corpora, independently:** taxonomy **21.6% untypeable**; MSBEFF
**50.6% RECALL** with only **6.4% tuple-typed**; and **`rail` types ZERO in either corpus** --
zero of 14 mechanisms, which is the sharpest single number in the walk.

**The residual has ONE SHAPE EVERYWHERE: they are properties of a CONTROL, not of an assertion.**
A tuple can describe a perfectly correct assertion; it has no vocabulary for an instrument that ran
and reported something untrue about its own operation. **That is definitional, not
difficulty-based** -- the boundary does not move with effort.

**HOMELESS: 19.7%**, corrected UP from 17.3% after the M3 split. Both the homeless share rising and
`grain`'s dominance shrinking move **against** the direction that would have flattered the vocabulary.

**M2 is carried as NAMED HOMELESS rather than mis-routed.** A shape-match returning well-formed
wrong content is a precision failure; WS-C7 is a *recall* standard and structurally cannot hold it.
Naming it homeless is more honest than filing it somewhere it does not belong.

### What this result CAUSED, which is why it is the highest-value artifact of P1

- **WS-C7 exists because of it.** Recall is a property of a CONTROL, so it needed its own standard.
- **~10 of the 16 staged control-design laws do not collapse into the M-taxonomy** -- they are the
  residual this walk named, being written down.
- **A THIRD DOCTRINE FAMILY HAS NO HOME** (how a rule or role fails to be one). Measured absent from
  `CONTROLS_OVER_CARE` III by `3.0.0_SA_CVO~Z`; stated as an open gap on both doctrine files.

### The concentration question, and why NO PERCENTAGE IS PUBLISHED

MSTR's V1 was discharged **BY REPRODUCTION** -- the same four mechanisms dominate under every parse
tried -- **not by a figure.** The corpus has **no canonical per-incident mapping**, so any single
percentage would be a property of the PARSE rather than of the corpus. **Publishing one would have
been a true measurement of the wrong proposition.**

## HONEST LIMITS, CARRIED FORWARD RATHER THAN CLOSED

1. **First-pass typing.** Step 0 states this bound and it governs every number above.
2. **`GAP_NAMED` may warrant a split** within the RECALL bucket -- named, not done.
3. **The `layer` x `verdict` cross-tab** was not run.
4. **My own parse was defective in the mechanism I had just named homeless** -- the strict parser
   silently dropped the four em-dash rows, which were the highest-value rows for an expressiveness
   question. **Recorded because the instrument that found the residual had the residual in it.**

## RATIFICATION

P1 closed against stated acceptance clause by clause rather than declared. The final item was found
by re-reading the acceptance TEXT rather than trusting a sense of completion: **WS-C2 clause 3
requires the held-out fence be stated IN THE RAIL SECTIONS THEMSELVES.** It was measurably absent
from the rule bank and now lands at `dynamic_rails.held_out_fence`.
