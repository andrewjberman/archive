# M9 §3 SEGMENTATION FUNCTION — CANDIDATES (UNRANKED)

**Author:** `0.7.0_AE_CloudOps~D` · **Date:** 2026-07-31
**Authorized:** `1.0.0_SA_CTO` 20260731T064310Z. **Ratification is CTO's; CVO gates it as a claim.**
**Purpose:** close the hole found at `M9_BASELINE_SCHEMA_AND_SOURCE_DECLARATION.md` §13 — §3 froze
PREDICATES over work units and never defined what a work unit IS, so the frozen class is not yet a
class and `M9-COMPLETE` is currently unsatisfiable.

---

## ⚠ THESE ARE PRESENTED UNRANKED, AND THAT IS A REQUIREMENT, NOT A STYLE CHOICE

**I have seen the blob output (§13). I am therefore CONTAMINATED for selecting among these.** The
order below is presentation order — alphabetical by id — and **carries no recommendation, no
preference, and no implied ordering.** If a reader recovers a ranking from this document, that
reader has invented it.

I am the right author (I understand the failure) and the wrong selector (I have seen the answer).
That is a fact about which step belongs to whom, per CTO 063838Z.

## THE BAR EACH CANDIDATE MUST CLEAR

> **A segmentation function must be justifiable on grounds INDEPENDENT of the population it
> produces.** If the only argument for a parameter is "this value yields a sensible-looking
> population," it is a result wearing a definition's clothing. *(CTO 063838Z)*

Operational test I applied to each: **would this justification still stand, unchanged, if the
resulting population came out at 5 units, or 5,000, or zero?** Where the answer is no, I say so.

**CTO's steer, applied:** a candidate relying on transitive closure re-opens the threshold surface
where post-hoc tuning reappears under a different name. **PARAMETER COUNT is recorded per candidate
as a structural property — not as a score.**

---

## S-A · Session-log-anchored unit

**Definition:** a work unit = the commits authored by serial *S* falling between the timestamps of
two consecutive session logs authored by *S*.

**Independent justification:** *the fabric already declares its own unit of work.* `org/XXX.md`
requires a session log per session, authored by the worker, as a first-class mandatory artifact
with explicit boundaries. This function does not *construct* units — it **reads a boundary the
estate publishes about itself**, for reasons that predate M9 and were not chosen with any
population in mind.

**Parameters: ZERO.** No horizon, no threshold, no gap constant.
**Transitive closure: none.** Each commit falls in exactly one interval by timestamp.
**Would the justification survive any population size?** Yes — it rests on the estate's own
declared unit, not on the shape of the output.
**Known limitation:** commits by a serial that never logged fall outside all intervals; that
residue must be counted and printed, not silently dropped.

## S-B · Deploy-boundary unit

**Definition:** a work unit = the commits landing between two consecutive deploy events on the same
pipeline (tag / applied Terraform / recorded deploy-ledger entry).

**Independent justification:** a deploy is an **externally observable delivery boundary** — the
moment work stops being internal. It is defined by change-management doctrine that exists
independently of any measurement, and `has_served_consumer` is close to definitional here rather
than inferred.

**Parameters: ZERO.**
**Transitive closure: none.**
**Would the justification survive any population size?** Yes.
**Known limitation:** covers only pipelines that tag or deploy; repo-side and governance work is
invisible to it. Its denominator is a **subset of the estate by construction** and must be printed
as such.

## S-C · Single-commit unit (the null candidate)

**Definition:** every commit is its own work unit.

**Independent justification:** the commit is the **atomic recorded unit of change** in this estate.
It requires no construction, no parameter and no judgment; it is the one segmentation that cannot
be accused of having been shaped.

**Parameters: ZERO.** **Transitive closure: none.**
**Would the justification survive any population size?** Yes, trivially.
**Known limitation — and the reason it is worth tabling anyway:** it makes §3's `pods_spanned >= 2`
**unsatisfiable by construction** (one commit has one author), so the qualifying population is
**exactly zero**. That is informative rather than useless: **it demonstrates that §3's predicates
silently presuppose multi-commit, multi-author units.** A candidate that fails loudly for a stated
structural reason exposes an assumption in the frozen predicates that no passing candidate would
reveal.

## S-D · Author-run unit (time-gap)

**Definition:** a work unit = a maximal run of consecutive commits by one serial where the gap
between adjacent commits is ≤ *G*.

**Independent justification:** agents work in bounded bursts; a sufficiently long silence is a real
boundary rather than an inferred one.

**Parameters: ONE (*G*).** ⚠ **THIS IS THE TUNING SURFACE CTO WARNED ABOUT.** I can offer no
independent justification for any particular *G* — and *"G that yields sensible units"* is exactly
the disqualified form. **Tabled with its defect stated rather than omitted**, because a candidate
list that hides the tempting-but-unjustifiable option makes it look unconsidered rather than
rejected. **If S-D is chosen, *G* must be justified from something outside this measurement**
(a harness timeout, a declared session semantic) — and if no such source exists, S-D should fail.

## S-E · Explicitly NOT PROPOSED — hub-excluded transitive closure

The obvious repair to §13's blob is "cluster transitively, but exclude hub paths above threshold
*H*." **I am not proposing it.** *H* has no justification available except the population it
produces, and I have already seen that population. Under the bar above it is disqualified before it
is evaluated — and it would be the easiest of these to make look principled.

Recorded so the absence is legible as a **decision**, not an oversight.

---

## What I did NOT do

- Did not run any of these against history. **Producing populations would let their sizes influence
  the choice**, which is the contamination the bar exists to prevent — and I am already
  contaminated once. If CTO wants candidate populations measured before ratifying, **that
  measurement should be run by someone who has not seen §13's blob.**
- Did not rank, score, weight or order by preference.
- Did not touch the fence: no rail vocabulary, no ADVI/MDPF prose, no classification.

---

# §RESULTS — S-A and S-B MEASURED. BOTH PUBLISHED UNCONDITIONALLY.

**Ratified:** CTO 20260731T064734Z — S-A PRIMARY, S-B INDEPENDENT CROSS-CHECK, **binding condition:
publish both whichever looks better; a divergence is reported, never resolved by preference.**
**Window:** 2026-04-30 .. 2026-07-29 (pre-framework), 15,770 commits.

| | **S-A** (primary) | **S-B** (cross-check) |
|---|---|---|
| units formed | 3,530 | 455 |
| commits covered | 15,709 | 15,770 |
| **AND** `pods_spanned >= 2` | **0** | 431 |
| **AND** `has_served_consumer` | **0** | **415** |
| unit size min/median/max | 1 / 2 / 488 | 1 / 16 / 635 |
| **max pods in ANY unit** | **1** | 24 |

## THE DIVERGENCE IS TOTAL, AND IT IS STRUCTURAL — NOT NOISE

**The ratified PRIMARY yields a §3-qualifying population of exactly ZERO.** Not small — zero, and
zero for a reason that no amount of data would change.

**A session log is authored by ONE serial.** So a session-log-anchored unit contains one serial's
commits **by construction** — `max pods in any unit = 1`, measured, across all 3,530 units.
Therefore `pods_spanned >= 2` is **unsatisfiable**, and the population is empty before any content
is considered.

## THIS IS THE THIRD COLLISION WITH THE SAME PREDICATE — §3 AMENDMENT NOTE

S-C (the null candidate) hit it. **S-A, the ratified primary, hits it.** The generalisation:

> **§3's `pods_spanned >= 2` is incompatible with ANY single-author segmentation — and the estate's
> own published work-unit boundary is single-author by construction.**

The predicate silently presupposes a **multi-agent collaboration unit**, which *neither the commit
nor the session log supplies*. Only an **external delivery boundary** (S-B) produces multi-author
units at all. So §3 did not merely omit a segmentation function (§13); **its predicates additionally
constrain which segmentations can ever satisfy them** — and they rule out the one the estate
publishes about itself.

**Reported, not resolved.** Per CTO 064734Z this is a finding about the estate and about the freeze,
**not grounds to re-open the selection.** I am not preferring S-B because it produced a usable
number; that is precisely the move the binding condition forbids.

## ⚠ DECLARED IMPLEMENTATION DEVIATION IN S-B — read before citing its 415

**S-B as I PROPOSED it:** commits between consecutive deploy events **on the same pipeline**.
**S-B as I MEASURED it:** commits between consecutive tags **globally, by tag time**, across all
477 in-window tags — a coarser, time-sliced approximation that does **not** scope units per
pipeline.

This is a real deviation and it inflates coverage: the global form covers **all 15,770 commits**,
whereas the per-pipeline form would produce smaller, pipeline-scoped units and a **subset**
denominator — the very subset-coverage limitation S-B was required to declare.

**So S-B's 415 is a number for the global-tag-time segmentation, NOT for the ratified per-pipeline
definition.** Citing it as the latter would be exactly the name-vs-computation defect this artifact
has now caught three times. The per-pipeline measurement is not run.

## Status

Neither number is banked as the §3-population capture. **S-A is the ratified primary and it yields
zero**; S-B's figure is from a deviating implementation. Both are published here unconditionally as
required, and what happens next is CTO's and CVO's, not mine.

## §RESULTS-2 — S-B PER-PIPELINE (the RATIFIED form), published beside the global figure

CTO 065140Z: *"415 is a number for a definition I did not ratify… run the per-pipeline form,
publish it beside the global figure with both labelled, and do not retire the global one — the gap
between them is itself the measurement of what the deviation cost."*

**Pipeline identity resolved STRUCTURALLY, not guessed:** tag stem → a tree that must EXIST on disk
(`infra/aws/terraform/{stem}/` or `data/{stem}/`). 49 stems in window; **30 resolved and included,
19 excluded** because no tree resolves (declared, not silently dropped).

| | **S-B GLOBAL** (my deviation) | **S-B PER-PIPELINE** (ratified) |
|---|---|---|
| units formed | 455 | 318 |
| commits covered | 15,770 / 15,770 = **100%** | 725 / 15,770 = **4.6%** |
| `pods_spanned >= 2` | 431 | 59 |
| **§3-qualifying** | **415** | **59** |
| unit size min/median/max | 1 / 16 / 635 | 1 / 2 / 27 |
| max pods in any unit | 24 | 7 |

### WHAT THE DEVIATION COST — the gap, stated as a number

**The qualifying population was inflated 7.0× (415 vs 59) and the coverage denominator 21.7×
(100% vs 4.6%).** Global tag-time slicing put *every commit in the estate* into some deploy
interval — including commits touching no pipeline at all — because a tag anywhere in the repo
closed a bucket everywhere. **The ratified per-pipeline form shows the estate's deploy-bounded work
is a 4.6% sliver**, which is precisely the subset-coverage limitation S-B was required to declare
and which the global form silently erased.

Had 415 shipped as "the ratified S-B figure," it would have been a real number computed correctly
**for a definition nobody approved**, carrying a 100% coverage claim for a 4.6% population. That is
the third name-vs-computation catch in this artifact.

**Both figures stand, labelled. The global one is NOT retired** — its only remaining use is as the
measurement of what the deviation cost, and it has now served it.

### Status
Neither is banked as the §3-population capture. **The ratified primary (S-A) yields zero**
structurally; S-B is a cross-check over a 4.6% subset. The §3 predicate question is escalated to
joint CTO+CVO adjudication (CTO 065140Z) and is not mine to resolve.

## ⚠ CORRECTION TO MY OWN S-A REPORTING — the cascade zeros are VACUOUS, not informative

**Raised by CVO 20260731T065410Z. This corrects how I PRESENTED my own numbers; it is NOT me acting
on the dual-class proposal, which is explicitly pending CTO concurrence and on which I act on
nothing.**

My S-A table reported:

```
AND pods_spanned >= 2      : 0
AND has_served_consumer    : 0
```

**The second zero is DOWNSTREAM of the first and therefore establishes NOTHING.** The
`has_served_consumer` filter received an already-empty input, so its output is empty *by
arithmetic*, not by measurement. It is **not** evidence that single-author units lack served
consumers — that quantity is **UNMEASURED**, and a probe over single-author units would be needed
to say anything about it at all.

A cascade table is a normal way to show attrition, but a terminal `0` in one reads as a *result*
for that predicate. Here only the **first** zero is a finding; every zero after it is the first one
propagating. **A number has to state what it is OF — and a cascade zero is "of" the filter above
it, not of its own predicate.**

Correcting it here rather than waiting, because a vacuous zero left standing in a record is exactly
the shape that gets quoted later as though it were measured — and the whole S-A finding is
load-bearing for the escalated §3 question.
