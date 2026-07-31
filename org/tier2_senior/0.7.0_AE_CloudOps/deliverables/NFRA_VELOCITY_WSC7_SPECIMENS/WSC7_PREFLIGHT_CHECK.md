# WS-C7 -- THE PRE-FLIGHT CHECK: BINDING A RUN'S ACTUAL BOUNDARY, NOT ITS DECLARED ONE

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Verify:** `3.0.0_SA_CVO~Z`
**Scope grant:** CTO~Z `20260731T150243Z` -- one document, pre-flight only. Shell-reachability
stays queued.
**Binds:** `WSC7_BOUNDARY_DECLARATION_SCHEMA.md` v3 (`153f16f2c`) and
`WSC7_REGISTRATION_INVARIANT_JOIN.md` (`7a285a8c9`).
**Substrate read, not modified.**

---

## 0. A TERM COLLISION, FLAGGED BEFORE ANYTHING IS BUILT ON IT

**"Pre-flight" is already in use in this estate with a DIFFERENT meaning.** Measured:
`comp_coverage_check.py:381` and `:832` and `tool_index.py:3569` all cite ***"`~D` pre-flight
findings 1/2/3"*** -- findings from a **review conducted before a build**, by an agent, about a
design.

**That is not what this artifact describes.** WS-C7's pre-flight is a **machine check a tool
performs on itself at invocation time.** Same word, different actor, different moment.

> **I am naming the collision and NOT resolving it.** Renaming either sense is a vocabulary
> decision and belongs to `1.0.0_SA_CTO~Z`. **This document says "run-boundary check" wherever
> precision matters, and flags the collision as routed item 1.** *A term silently carrying two
> meanings in one program is the `scope`/`locality` class that cost the fabric two hours today.*

---

## 1. THE GAP -- WHAT REGISTRATION CANNOT COVER

| | binds | when | asserts |
|---|---|---|---|
| member 5 (registration) | the **DECLARATION** | commit time | the tool has said what it CAN reach |
| **run-boundary check** | **THIS RUN** | invocation time | what this invocation ACTUALLY reached |

**A boundary declaration is a statement about a tool's CAPABILITY. A finding is produced by a
SPECIFIC INVOCATION.** Those differ, routinely and legitimately:

- `comp-legacywriter` declares `reportable: run_conditional`, `enabled_by: --heat-json /
  --dups-json / --debris-json`. **Measured on the run I exercised: all three UNAVAILABLE.** The
  declaration was accurate; the run was degraded. **Both true at once.**
- Its contract registry held **2 joinable declarations against 439 scored surfaces**. That is a
  property of the registry *today*, not of the tool.

> **A FINDING IS ONLY INTERPRETABLE AGAINST THE BOUNDARY OF THE RUN THAT PRODUCED IT, NOT AGAINST
> THE TOOL'S DECLARED CAPABILITY.** Registration cannot supply that -- it happens once, at commit
> time, and the run happens later under conditions nobody committed.

---

## 2. THE EXEMPLAR ALREADY EXISTS -- BIND TO IT, DO NOT INVENT

`comp_legacywriter.py:1064-1071` already emits exactly this, **before any finding**:

```
ENRICHMENT AXES -- vintage stated, missing means UNAVAILABLE not clean
  comp-heat   (producer CODE recency) : not supplied
  comp-dups   (exact-dup twins)       : not supplied
  comp-debris (RESOURCE invocation)   : not supplied
  *** HEAT UNAVAILABLE -- every surface reads UNAVAILABLE on that axis.
  *** That is a gap in THIS RUN's coverage, never a statement about the surfaces.
```

And its source comment (`:693-694`): ***"A MISSING INPUT IS 'UNAVAILABLE', NEVER A CLEAN COLUMN...
absence of an instrument is not absence of a writer."***

**That sentence is the run-boundary check's entire semantics.** The design work here is not
inventing a mechanism; it is **naming the obligation and stating what it must NOT do.**

*(Provenance discipline, per my correction this morning: I am NOT calling this independent
convergence. `comp-legacywriter` is built to the WS-C1 spec and cites the rule bank 16 times.
Whether its emission pattern shares an upstream with WS-C7 is CTO~Z's open question, and I am
building on neither answer.)*

---

## 3. WHAT A RUN-BOUNDARY CHECK MUST EMIT

Per run, **before findings**, four things:

| # | emits | from schema v3 |
|---|---|---|
| 1 | **which declared inputs were actually available** | resolves `run_conditional` -> concrete for this run |
| 2 | **the realised denominator at each chain stage** | `chains` declares the shape; the run fills the counts |
| 3 | **vintage of every substrate consulted** | a stale substrate is a boundary condition, not a finding |
| 4 | **whether the declaration is STALE** | v3 decay -- `revalidate_by` expired, or tool source moved since |

**Item 4 is where v3's decay becomes operational.** A stale declaration is **LOUD and
NON-ACTIONABLE** at registration; **at run time it is a boundary condition on every finding the run
produces.** Not a block, not a finding, not a claim the tool is wrong -- a stated condition.

---

## 4. THE TWO THINGS IT MUST NOT DO

### 4.1 IT MUST NOT BLOCK ON A DEGRADED BOUNDARY

**A degraded run is a legitimate run.** `comp-legacywriter` with three axes unfed still produced 439
surfaces, 345 scored, and a real verdict. **Refusing to run would have destroyed real output to
avoid an honest disclosure.**

> **Blocking on degradation punishes the tool for telling the truth about its inputs, which is the
> `structurally_invisible` error one layer up:** make the boundary legible, do not make it a
> failure. **The check REPORTS; it does not gate.**

**The one exception is inherited, not new:** if the run-boundary check cannot itself evaluate --
substrate unnameable, declaration unparseable -- **it fails closed**, exactly as the completeness
family already does (*"an unevaluable invariant is not a passing one"*). **Cannot-evaluate and
evaluated-as-degraded are different states and must not share an outcome.**

### 4.2 ITS OUTPUT MUST TRAVEL WITH THE FINDINGS

**A boundary report separated from the findings it qualifies is worse than no boundary report**,
because the findings then circulate bare while a reader believes the qualification exists somewhere.

> **This is the third appearance of one shape in this workstream:** `comp-iam`'s operation list read
> as a deletion warrant (CLAUDE.md, live); a green member 5 read as "the declaration is correct"
> (join, section 2.1); and now a boundary report that exists but does not travel. **In all three the
> artifact is honest and the CONSUMER's inference is wrong** -- and in all three the fix is at the
> point of consumption, not the point of production.

**Concrete requirement:** the run's boundary must be emitted **in the same artifact and before** the
findings -- not a sidecar, not a log line, not a separate `--json`. `comp-legacywriter` does this
already: header block, then dossiers.

---

## 5. THE L-16 OPPORTUNITY -- and why I am NOT specifying it

L-16 says `basis: exercised` is insufficient without a **known-negative**: exercising proves a tool
runs, only a known-negative proves it discriminates.

**The run-boundary check is the natural place to actually RUN one** -- a self-test per invocation
that proves the instrument can still fail. `comp-legacywriter` has `--self-test`; my own CRLF
counter would have died instantly against one.

**I am NOT specifying it here.** A mandatory per-run self-test is a cost decision (every invocation
pays it) and a design decision about what constitutes an adequate negative. **Both are the gate's.**
**Flagged as routed item 2** -- the opportunity is real and the specification is not mine.

---

## 6. WHAT A RUN-BOUNDARY CHECK CANNOT DO

Inherited unchanged from the join (`7a285a8c9` section 2.2), and restated because the run-time
framing invites the same over-read:

- It **cannot** verify the declared address space is the real one -- producer-asserted, no observer
  oracle.
- It **cannot** detect a well-formed wrong finding (**M2**, out of contract).
- It **cannot** make a degraded run into a complete one. **It makes the degradation legible. That is
  the whole benefit and the whole limit.**

> **A green run-boundary report means "this run's coverage is stated," never "this run's coverage is
> good."**

---

## 7. ROUTED TO THE GATE, NOT DECIDED HERE

1. **The term collision (section 0).** `~D pre-flight findings` already means a pre-build review.
   **Rename either sense, or accept the overload with a disambiguator -- CTO~Z's call.** I used
   "run-boundary check" throughout rather than silently redefining an in-use term.
2. **Whether a known-negative self-test is mandatory per run** (section 5) -- cost and adequacy are
   both design decisions.
3. **Where the boundary report lives when a tool has no human-readable output** (pure `--json`
   consumers). `comp-legacywriter`'s header pattern presumes a text surface.
4. **Whether a stale declaration should degrade a run's boundary report or merely annotate it** --
   v3 makes it loud and non-actionable at registration; the run-time consequence is unspecified and
   I did not specify it.

**CONTROL 2 CHECK:** nothing here types where an assertion sits. Not rail vocabulary. `revalidate_by`
and the grain axis are referenced as ruled, never redefined.
