# WS-E5 ARTIFACT 1 — the boundary report already exists. **The registry cannot carry it.**

**Seat:** `0.7.0_AE_CloudOps~D` · **Date:** 2026-07-31 · **TO:** `NFRA_VELOCITY_ESTATE.WS-E5` @`8396b9b785`
**Verdict:** **NEGATIVE RESULT, delivered at one detector as designed.** COO 142609Z: *"a negative
result is a first-class deliverable here… I want that as a BLOCKING architectural finding while
redesign is still cheap."*

---

## §1 THE FINDING, INVERTED FROM THE WORKSTREAM'S PREMISE

WS-E5 is framed as making detectors honest about what they cannot see. Measured against one real
detector, **the premise is already satisfied in substance and blocked in form:**

> ### The detector emits a complete boundary report. There is nowhere typed to put it, so it is prose.

The gap is **not** "detectors do not declare their boundaries." It is **"the registry cannot carry
the declaration they already make."**

## §2 EVIDENCE — `comp-legacywriter`, exercised not read

Chosen because it is measurement-time, advisory/read-only, and **off the ETFS/inf path** (COO fence:
`~A` owns the Aug-1 fire). Run 2026-07-31T143546Z.

**All four required boundary elements are present:**

| element | what it emits, verbatim |
|---|---|
| **address space** | `STATIC: examined 8915 file(s) under data, infra/aws, org/modules, portal/scripts` |
| **recall denominator** | `642 distinct (BUCKET,KEY) location(s)` · 859 write-sites / 181 probe-sites / 1224 read-sites |
| **traversal residue** | `BLINDNESS: deployed-vs-repo divergence not modelled; dynamic keys render UNRESOLVED-WRITER (never absent).` |
| **failure direction** | `CAPABILITY : NOT RUN this invocation -- UNVERIFIABLE-BY-THIS-INSTRUMENT… A grant may be REQUIRED-AND-UNOBSERVED; silence here is not absence.` |

It goes further than the standard asks: `PHASE 0 -- SUBSTRATE COVERAGE PRECONDITION` and
`BLINDNESS: comp-kuzu provenance NOT read this run… **Declared, not assumed.**`

**Two form defects, measured:**
- **NOT first-line.** Line 1 is a run header; the boundary block starts at **line 5**.
- **NOT typed.** Grep for the L0a field names (`address_space`, `traversal_residue`,
  `failure_direction`, `recall_denominator`) across the whole output: **0 occurrences.**

## §3 WHY IT IS PROSE — and this is the blocking finding

base CVO (relayed COO 143436Z) read the ratified `contract_record` and found **no field carries a
boundary declaration**: `intent_source · obligation · lifecycle_class · revalidate_by · describes ·
locality · successor`. And `describes` is declared **non-vocabulary and un-lintable**, so it cannot
hold a *checkable* one.

**Two independent methods converged on the same wall.** CVO read the grammar top-down and predicted
the gap. I exercised a detector bottom-up and hit it. Neither knew the other's result.

**So the prose is not sloppiness — it is the only available form.** The detector's author had
nowhere typed to put a boundary declaration and wrote an excellent one in the only medium left.
E5's enforcement design (PRD 193-197) rests on *an estate detector IS a contracted process whose
contract carries its boundary declaration* — and **the carrier does not exist.**

## §4 WHAT I AM NOT DOING

- **NOT extending the grammar.** The specimen goes to the rail authors through the seam (COO → MSTR
  → CORE); `~Z` takes no work from the main fabric directly. **I hand over the specimen, never the
  proposal** — describe-the-specimen-never-the-gap still binds.
- **NOT registering it.** The `process:`-defer seam is with base CTO (COO 143259Z): does the E2
  defer cover estate detectors, or only trigger-topology processes? An estate detector registers as
  a contracted **process**. Unresolved, and not mine to self-certify out of.
- **NOT building a new detector.** The moratorium fence is sharpest here: a sensor is a **boundary
  declaration on an existing detector**, never a new thing that watches. Nothing here fires,
  pages, or notifies.
- **NOT a commit-time gate.** Measurement-time quadrant only; a commit hook is E3's lane.

## §5 CEILING, NAMED RATHER THAN STALLED AGAINST

Acceptance item 3 (*no new detector past the gate ramp without a contracted boundary declaration*)
rides WS-E3's C-SILENT commit-gate ramp, and **E3 is gated behind lifecycle values** — now `~B`'s
lane, which I do not advance. **The REGISTRATION half is reachable pending the seam; the DENIAL half
is not reachable at all.** Named, per COO's fence 3.

## §6 MY DENOMINATOR — one detector, and I did not survey

**I examined ONE detector.** The honest claim is *"at least one estate detector already emits a
complete boundary report in prose"* — **not** *"detectors already do this."*

I did not begin with a survey, per COO's instruction, and the reason holds up in hindsight: a survey
would have produced a coverage count over an enumeration that structurally cannot see freshness
Lambdas or EC2-side checks — a number I would then have had to distrust. **One detector answered the
architectural question; a survey would have produced a statistic and left it open.**

## §7 THE ASK

The blocking question for CORE, stated as a specimen and not a design:
**a detector that already computes its address space, denominator, residue and failure direction has
no field in `contract_record` to declare them in.** What that implies for the grammar is the rail
authors' call.

---

# §8 THE MUTANT PROOF — REQUIRED, RUN, AND IT **FAILED**. That is the sharpest finding here.

COO required the report to change when the address space changes. **It does not.**

| run | answer size | declared address space | declared denominator |
|---|---|---|---|
| baseline (whole population) | **2,426 lines** | `examined 8915 file(s)` | `642 distinct (BUCKET,KEY)` |
| scoped to one bucket | **181 lines** | `examined 8915 file(s)` | `642 distinct (BUCKET,KEY)` |

**The answer narrowed by 93%. The declared boundary did not move by one character.**

## §8.1 I ruled out the likelier explanation first

A failed mutant usually means the mutant did not mutate. **Discriminating check: the outputs differ
enormously — 2,426 vs 181 lines — so the scope argument unambiguously took effect.** The scoping is
real; the boundary is simply invariant to it.

## §8.2 What the defect IS

**A SCOPED ANSWER CARRIES AN UNSCOPED BOUNDARY.** A reader of the scoped run receives a 181-line
answer about one bucket, accompanied by a denominator computed over the whole estate. Nothing in the
output distinguishes *"what the scan examined"* from *"what this answer ranges over"* — and those
diverged by 93% in this single invocation.

**This is mechanism 2, live:** *"WIDER-THAN-MEASURED — does the CLAIM's axis equal the MEASURED
axis?"*

## §8.3 And it is the arity gap, arrived at from the opposite direction

`test_e5_recall_standard_arity_limits.py` (`@3d9ad164b2`, base serial, 07-30) concluded **from the
type alone** that the L0a boundary report expresses ONE of five mechanisms, and that the other four
are blocked by its **ARITY** — one `source`, one `address_space`, one `head` — so *"a MISMATCH
between the plane measured and the plane a claim ranges over has nowhere to live."*

**That was a prediction from reading the type. This is the same defect measured in a live detector's
output.** The type cannot carry the distinction, so the detector does not draw it — and a 93%
divergence between scan-scope and answer-scope goes unstated.

**Three independent routes, one wall:** CVO read the grammar and found no carrier field; I exercised
a detector and found the substance already written in prose; the mutant found the boundary invariant
to the very thing it is supposed to bound. **A single `address_space` field cannot be both the
scan's and the answer's, and no amount of care in the detector fixes a field that does not exist.**

## §8.4 Status

**Artifact 1 is a NEGATIVE RESULT and it is complete as one.** Registration is open (base CTO
143606Z — the defer is field-level and this detector declares no `cadence` / `delivery_cadence`),
but **what would be registered has no field to hold it, and the one field that exists cannot tell
two address spaces apart.**

Specimen to the rail authors through the seam. **I do not name the field that would fix it.**
