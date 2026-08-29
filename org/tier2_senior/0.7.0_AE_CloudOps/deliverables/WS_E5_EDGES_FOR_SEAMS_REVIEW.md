# WS-E5 -- EDGES FOR ANDREW'S SEAMS REVIEW

**Author:** `0.7.0_AE_CloudOps~D` | **Requested:** COO 20260731T175544Z (ANDREW-DIRECT HARD PAUSE)
**Question being answered:** do the systems COMPOSE, or did we build several correct things that do not fit?
**Form:** edges (consumes / exposes), NOT accomplishments. **A missing edge is a first-class answer.**

> **HEADLINE, stated first because it is the load-bearing one: E5's TWO PRIMARY CONSUMED EDGES DO NOT
> MEET EACH OTHER.** E5 consumes a boundary-declaration SCHEMA from CORE/WS-C7 and registers into a
> CONTRACT STORE from ESTATE/WS-E1. **The schema is not a field of the store.** Measured, not inferred.
> This is exactly the "several correct things that do not fit" shape. Both halves are individually
> correct and well-built; the join is absent.

---

## 1. WHAT E5 CONSUMES

### 1a. CORE / WS-C7 -- the boundary-declaration schema `@5b92f664d` + `@7a285a8c9`
**BROKEN EDGE -- MEASURED NOT WIRED.** Re-derived by me and independently re-derived by COO before relay:

| probe | result |
|---|---|
| `boundary_declaration` in `NFRA_ONTOLOGY_RULE_BANK.yaml` | **0** |
| POSITIVE CONTROL `contract_record` (same file, same method) | **3** (grep discriminates) |
| NEGATIVE CONTROL, invented token | **0** |
| `@5b92f664d` touched | `WSC7_BOUNDARY_DECLARATION_SCHEMA.md` ONLY |
| `@7a285a8c9` touched | that file + `WSC7_REGISTRATION_INVARIANT_JOIN.md` |

**Markdown design documents only.** The schema is STANDALONE-REFERENCED, not wired.
**Correctly narrowed** from CVO's original "no schema exists" to: *the schema is not a field of the
thing detectors register as.* The schema is real, ratified, and good. It has no socket.

### 1b. ESTATE / WS-E1 -- the estate-contract registry (`contract_record`, rule bank v1.8)
**EDGE EXISTS, ATTACHMENT POINT DOES NOT.** Registration is OPEN per CTO's field-level predicate, and
`contract_record` required/optional terms carry no member that can hold a boundary declaration.
**I did not register, and that was the correct call** -- inventing an attachment point would have been
self-certification, and the declare-time lint (`.tools/contract_declare_lint.py`) rejected exactly that
class three times today when I tried to invent `rejection_reason` and `lifecycle_basis`.
**A fact with no ratified home keeps trying to become a new field. The lint is what stops it.**

### 1c. ESTATE / WS-E2 -- excluded guard/detector/watcher classes
**EDGE WORKS.** Consumed as a **CONTRIBUTING SOURCE with its own provenance, explicitly NOT my
denominator.** It is live-AWS-grounded and covers precisely the class my own `comp-which` enumeration
misses by construction (PRD 190-192: no `comp-manifest-check` ever sees a freshness Lambda, an EC2-side
gold check, or a deploy verify).
**BOUND, stated so nobody promotes it:** EventBridge-triggered, us-east-1 only. Blind to a detector
that runs inside another process, on a box cron, or as a pipeline step. **A borrowed population
presented as a denominator is how a coverage number acquires a basis nobody examined.**

### 1d. CLAUDE.md / estate tooling -- `.tools/msys_argv_guard.py`
**EDGE WORKS, and it is load-bearing for anything that shells a comp-tool from Python.** The comp-tools
are extensionless bash shims: native `subprocess.run` raises `FileNotFoundError [WinError 2]`, and
`shutil.which` reports them PRESENT anyway. **A `which`-guarded suite SKIPS -- silently reporting
UNVERIFIABLE -- on a fully-installed estate.** Any workstream building Python-side conformance checks
inherits this or inherits the bug.

---

## 2. WHAT E5 EXPOSES

### 2a. To WS-E3 -- the enforcement half, riding E3's C-SILENT commit-gate ramp
**EDGE DECLARED, NOT YET LOADED.** This is the ceiling I was told to NAME rather than discover.
E3 is itself gated behind lifecycle values, which are `~B`'s lane. **The dependency is real and
correctly ordered; it is simply not live.** Naming it is the deliverable, not resolving it.

### 2b. To WS-E1 and any registering producer -- the ACCEPTANCE STANDARD for a declaration
`org/modules/graph/tests/test_e5_estate_conformance_suite.py` `@da632d81d6` (on origin).
Ten specimens; **every specimen carries its own live mutant plus a MUTANT-APPLIED PRECONDITION.**
**EXERCISED LIVE: 3 of 10** (specimens 2, 10, 10b). The other 7 carry mutant DESIGNS and are marked
DECLARED-NOT-EXERCISED -- **a green on those asserts the design is stated, NOT that the estate passes.**

### 2c. To base CTO -- a live instrument defect
`comp-legacywriter`'s scoped answer carries an UNSCOPED boundary: answer narrows 2426 -> 297 lines,
declared boundary identical at `examined 8916 file(s)` / `642 distinct (BUCKET,KEY)`.
Owner COO, routed. **Sharpest form:** the tool warns its reader *"STATE THE POPULATION BEFORE ACTING"*
on every row, while not stating which population its own scoped answer ranges over.

### 2d. >> A CORRECTION TO WHAT E5 CAN EXPOSE AT ALL -- discovered today, changes the standard <<
I reported `comp-trigger` as the scope-correct counter-example. **Running it properly refutes my own
claim: its denominator does NOT track scope either** (both forms print `142 events-rules + 12
schedules`). **BOTH measured instruments carry scope-invariant denominators.**

**Therefore the predicate E5 exposes CANNOT be "the denominator tracks scope."** It must be a
**LEGIBILITY** predicate: *name the address space you ranged over, and label the count as the SCANNED
population.* `comp-trigger` does both (`forensics for: "mdpf"` + `... scanned`); `comp-legacywriter`
does neither -- its header names the run, the spec and the source HEAD, never the target.
**If C7's schema is wired on the assumption that a conforming declaration varies with scope, it will
be wired to the wrong predicate.** This is the single most important thing E5 brings to the review.

---

## 3. THE SEAM IN ONE LINE, FOR THE REVIEW

```
CORE/WS-C7 boundary schema  --X-->  ESTATE/WS-E1 contract_record     <-- NOT WIRED (measured)
ESTATE/WS-E5 suite          -------> the acceptance standard for whatever that join becomes
ESTATE/WS-E5 enforcement    --?-->  ESTATE/WS-E3 C-SILENT ramp        <-- declared, gated, not live
ESTATE/WS-E2 census         -------> E5 as a CONTRIBUTING source, never a denominator
```
MSTR~Z independently surfaced the C7-vs-D3 seam as one of five cross-fabric integration points.
**I am the ESTATE-side predictor of it, and it was predicted FROM THE TYPE before it was measured:**
the 07-30 arity test (`test_e5_recall_standard_arity_limits.py` `@3d9ad164b2`) showed the L0a
boundary-report type has arity ONE source / ONE address_space / ONE head -- so a mismatch between the
plane MEASURED and the plane a claim RANGES OVER **has nowhere to live in the type.**
Predicted from the type, then found in a live detector. That is a type system earning its keep.

## 4. THE BOUNDARY OF THIS DELIVERABLE (E5's standard, turned on E5)

- **PRODUCER-ASSERTED, NOT VALIDATED.** The registration invariant binds SHAPE and can never bind
  TRUTH. There is no observer oracle for whether a declared address space is the real one.
  **The worst outcome for E5 is a field that carries a declaration and READS AS VALIDATED** -- that
  is the `comp-iam` deletion-warrant class, and E5 would be building the surface it exists to close.
- **DENOMINATOR of the edge enumeration: the workstreams named in my TO plus those I measured
  against.** I did not sweep the ESTATE PRD for edges I was not already touching. **An edge nobody
  wrote down is not in this document** -- and given the headline finding is a MISSING edge, the
  absence of others here is not evidence of their absence.
- **n=2 on the instrument comparison.** Chosen for contrast, not sampled. Two instruments can refute
  universality and **cannot establish a rate. NOT UNIVERSAL -- never "rare."**
