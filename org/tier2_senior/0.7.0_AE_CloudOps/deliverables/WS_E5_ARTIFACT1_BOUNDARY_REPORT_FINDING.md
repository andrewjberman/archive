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

---

# §9 CORRECTION + THE ANSWER TO THE OPEN WIRED-VS-STANDALONE QUESTION

## §9.1 My §1/§3 headline was too strong. Narrowing it against my own interest.

I wrote *"the registry cannot carry it"* and *"the carrier does not exist."* **A boundary-declaration
SCHEMA does exist** — CORE WS-C7, canonical at `@5b92f664da` (v2) plus the registration-invariant
join `@7a285a8c9f`. `@b2070b35a` is v1 and superseded; I verified all three at source rather than
taking the relay, after COO's own two-step correction and their instruction to apply the same
suspicion to their messages.

**So "no carrier exists anywhere" was wrong.** The correct, narrower claim is below.

## §9.2 MEASURED: the schema is NOT WIRED INTO `contract_record`

This is the open item MSTR is still carrying to CTO~Z. **Measured at current HEAD:**

| check | result |
|---|---|
| files touched by all three C7 commits | **markdown design documents only** — `WSC7_BOUNDARY_DECLARATION_SCHEMA.md`, `WSC7_REGISTRATION_INVARIANT_JOIN.md` |
| `contract_record` optional list (`:385`) | `[successor, expiry_condition, cadence, vintage_probe, describes]` — **unchanged** |
| `boundary_declaration` in the rule bank | **0 occurrences** |
| positive control | a known-absent token also returns 0, so the grep discriminates |

> ### The schema is FULLY SPECIFIED AS A DOCUMENT and has NO FIELD IN THE RATIFIED RECORD.
> **STANDALONE-REFERENCED, NOT WIRED.**

**Consequence for E5's registration half:** a detector can be registered as a contracted process
(base CTO 143606Z opened it), **but its boundary declaration has nowhere to attach inside
`contract_record` today.** CVO's original finding stands, narrowed: not *"no schema exists"* but
*"the schema is not a field of the thing detectors register as."*

## §9.3 What survives unchanged — and it is the part that matters

**§8's mutant failure is untouched by any of this.** The boundary report is invariant to the address
space it bounds: a 93%-narrower answer carried a byte-identical boundary. **That defect is
independent of where the schema lives**, and C7's own discipline is the reason it matters —
*"a fully-conformant boundary declaration is compatible with every value being wrong."*

A wired field would have made that report **conformant**. It would not have made it **true**.

## §9.4 E5's standard, turned on E5 itself

Per COO 145852Z, and it is the right demand: **when I register a boundary declaration, I will be
declaring something I cannot verify.** The invariant binds SHAPE; there is no observer oracle for
whether a declared address space is the real one.

**So this artifact declares its own boundary:**
- `address_space` — ONE detector (`comp-legacywriter`). **Not a survey.**
- `denominator` — **NOT-ENUMERABLE.** I have no verified count of estate detectors, and the
  enumeration available to me is structurally blind to freshness Lambdas, EC2-side checks and
  deploy verifies (PRD 190-192).
- `traversal_residue` — **detected_not_counted.** I know that class exists and is missed; I have
  not counted it. An E2-lane live census is inbound as a **contributing source with its own
  provenance — NOT my denominator.** A borrowed population presented as a denominator is how a
  coverage number acquires a basis nobody examined.
- `failure_direction` — **under_report**, basis **exercised** (§8's mutant is the exercise).
- **PRODUCER-ASSERTED, UNVERIFIED.** These are the standard's boundary, not its backlog.

**E5 has no standing to demand of detectors what it will not do itself.**

---

# §10 DETECTOR 2 — **IT IS NOT A CLASS.** COO's instinct was wrong, and that is the useful answer.

COO 150455Z: *"a second detector to test whether the unscoped-boundary defect is
comp-legacywriter-specific or a CLASS. My instinct is class, and I would rather know."*

**MEASURED: not a class. `comp-trigger` draws the distinction that `comp-legacywriter` does not.**
Deliberately a **different family** — trigger forensics, not writer census — so a shared result would
have been strong class evidence. It is not shared.

## §10.1 The same mutant, run across families

| | baseline | scoped | scope named in header? | denominator wording |
|---|---|---|---|---|
| **`comp-trigger`** | 155 lines · `census -- 142 events-rules + 12 schedules` | 18 lines | **YES** — `forensics for: "mdpf"` | **`142 … SCANNED`** |
| **`comp-legacywriter`** | 2,426 lines · `examined 8915 file(s)` · `642 locations` | 181 lines | **NO** — header byte-identical to baseline | `examined 8915` (scan wording only) |

Both mutations took effect (155→18 and 2,426→181), so neither is a non-mutating mutant.

**`comp-trigger` lets a reader separate the two populations:** it names the query (`forensics for:
"mdpf"`) and labels the number `scanned`. **`comp-legacywriter` does not** — its scoped header is
indistinguishable from its unscoped one.

## §10.2 NARROWING MY OWN §8 AGAIN — and the sharper version is worse for the tool

`comp-legacywriter`'s scoped output **does** contain six scope-flavoured strings, so "no scope
language at all" would have been wrong. **All six are the identical per-row evidence bar:**

> `evidence_bar: NO READER FOUND IN THE SCANNED POPULATION -- this is NOT 'no reader'.`
> **`State the population before acting`**

That is a per-finding caveat, not a header scope declaration — and it makes the defect sharper
rather than softer:

> ### The tool instructs the reader to **"state the population before acting"** while itself not stating which population its own scoped answer ranges over.

The instrument knows the failure mode by name, warns about it per row, and then commits it at the
header level.

## §10.3 What this does to E5's population

COO's own framing: if it were a class, E5's population becomes *"detectors whose declarations would
be wrong"* — a materially different workstream. **It is not.** The population stays *"detectors
needing declarations,"* **with per-instrument variance that must be measured rather than assumed** —
one of the first two already draws the distinction correctly.

**So a survey counting "detectors lacking a boundary declaration" would have been wrong in both
directions**: it would have missed that `comp-legacywriter` already emits one in prose, and missed
that `comp-trigger`'s is scope-correct while the other's is not. Presence is not the axis;
**correctness under scope change is**, and only a mutant reveals it.

## §10.4 Denominator, unchanged and stated

**TWO detectors, chosen for family contrast, not sampled.** `n=2` cannot establish a rate — it can
only refute universality, which is exactly what was asked. **The honest claim is "not universal,"
NOT "rare."** Whether most detectors resemble one or the other is unmeasured and I am not implying it.
