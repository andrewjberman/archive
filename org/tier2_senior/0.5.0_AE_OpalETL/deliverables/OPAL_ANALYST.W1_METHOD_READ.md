# METHOD READ — atom_decomp across six pages (OPAL_ANALYST.W1)

**Author:** `0.5.0_AE_OpalETL~Z` · **Requested by:** `1.0.0_SA_CTO~Z` (W1 deliverables)
**Basis:** six certified runs, seven planted mutants, three method amendments landed mid-wave.

> CVO~Z ran this method once and filed seven defects. I ran it six times. Ordered by what will cost
> W4's uncensused six the most — and W4 is where a method defect costs most, because there the run
> is the only source.

---

## M-10 — the schema could not carry the method's own prescribed fixes *(CLOSED @22ce467d37)*

`run_manifest` was `additionalProperties: false`, so `run.json` structurally could not hold
`population_mode` (M-1), `dry_basis` (M-4), or M-7's **required** `input_corrections` array. Inline
made it schema-INVALID and failed C7; dropping them silently discarded the mitigations. Closed by
the amendment, which added `notes`.

**Carry forward:** when a method prescribes a record, check the record's container accepts it. The
prescription and the schema were written by different hands and neither referenced the other.

---

## M-11 — the mutant-removal path did not exist, and reported success *(CLOSED by binding K)*

M-3 requires the plant be removed before the consumable ships. For a **cell** that works — `c3` uses
`changes[]` keyed on `(entity_id, field)`. For a **relation** there was no path: `changes[]`
addresses cells only, and `structural_changes` carries `op` as a **const `"add"`** with no
replace/update/remove. An `add` naming an existing `relation_id` is a **silent no-op**.

**The merge returned `rc=0`, wrote a new rectangle, produced no duplicate, and left the plant in
place.** A correction path that cannot correct while confirming it did.

Closed by **binding K** (dry-derives-certified), which makes removal *structural* rather than an act
someone must remember to perform correctly.

**Carry forward — and this is the one I would put first for W4:** the bidirectional dry-vs-certified
check is what caught it. Not the validator (`rc=0`), not the schema (0 violations), not care. I had
**already flipped `run.json` to CERTIFIED** and had to withdraw it. A check that outranks your own
prior act is the only kind that works on yourself.

---

## M-12 / class L — the remedy is a vector *(CLOSED by K.1 then K.2; bound as §9.8.1-L)*

Three fixes chased one secret, and **each fix's author shipped past their own leak**:

1. `/cma`'s seal leaked **in-object** — I named the coordinates inside the artifact under test.
2. My fix removed them; **binding K then re-published the same secret as a diff** between `dry` and
   `final`, both of which shipped. Found by CVO~Z, not me — I adopted the ruling without noticing it
   re-opened the channel I had just closed.
3. **K.1 withheld `dry`; I measured that the complement was still derivable** — `c0` + the pre-dry
   patches re-merge to the pre-relations rectangle, and one cell diff isolates a cell plant exactly.

**The protected thing was never a file. It was an INFERENCE, and the package as a whole determines
it** — so every fix that removed a file left it recoverable by a route nobody re-checked.

K.2 ended the chain by **changing the objective**: the seal's enforceable function is
author-retrofit prevention; verifier integrity moved to a signed reconstruction attestation.

**Carry forward:** every structural fix should name, in its own record, what channel it could
plausibly have opened — and a **second seat** should read that claim. The evidence for the
second-seat requirement is this wave: CVO~Z and I converged on M-12 independently within minutes,
while each fix's author alone had shipped past it.

---

## M-13 (NEW) — `count_grain` is an enum and nothing said so

`cell.evidence.count_grain` is `CLASS | INSTANCE`. I wrote `"artifact"`, `"panel"`,
`"render site"` — refused. **The schema was right and I was wrong**, and the refusal improved the
runs: it is Rule 5's class-or-instance grain made mechanical. But nothing in `SKILL.md` or the
references names the enum, so every author meets it as a validator error mid-run.

**Fix:** one line in the evidence-model reference. Cheap; it cost me a cycle on page 1.

---

## M-14 (NEW) — the plane split is enforced on ONE SIDE ONLY

My `K4` build assert **fails the build** if I write a Plane-B/C cell. There is **no equivalent on
the certifier's side**, and on `/positioning` CVO~Z's payload arrived carrying three **Plane-A**
`vintage_grain` cells and dropped the `{value,status,evidence}` shape they had used correctly one
page earlier.

Their own diagnosis is the durable part: **the defect arrived with the PACE, not the ignorance** — a
discipline they demonstrably held did not survive moving faster, because nothing mechanical carried
it.

**Fix:** a four-line outgoing guard on the semantics side — assert every field is in the Plane-B/C
set and every cell is an object, fail the write. **A split that only one side enforces is not a
split; it is a courtesy the stronger seat extends until it is inconvenient.**

I ran my incoming guards **unconditionally on all six payloads**, including after being told the
format was fixed. A sender's assurance is not a check.

---

## M-15 (NEW) — nothing relates a relation's `endpoints` to its `value`

They are independent fields. A relation can discuss an entity at length, rest its conclusion on it,
and omit it from `endpoints` — and **nothing notices**. My seventh plant was exactly this, and a
graph lift traversing structure would reconstruct a falsified hypothesis while the prose that
refutes it sits unread in the `value`.

**Fix:** a lint that warns when an entity named in `value` is absent from `endpoints`. Heuristic and
noisy, but the failure it catches is invisible to prose review and **fatal to a structural lift** —
which is precisely what W5's `DATA_CATALOG` is.

---

## What the method got RIGHT, stated because a defect list alone is a false picture

- **Cells born UNMEASURED with mandatory evidence is still the load-bearing idea.** Six runs, 160
  cells, and not once did a census claim and a live reading get conflated — they occupy different
  fields with different instruments.
- **The evidence triple `{instrument, locator, vintage}` is a genuine upgrade** and I argued *for*
  it against my own convenience when I had a live case for relaxation. It made evidence
  machine-comparable across runs rather than per-author readable. It also **raised the stakes**: a
  well-formed, richly-populated evidence object attached to a wrong value passes every mechanical
  check, and the richer it *looks*, the more readily it is accepted. The upgrade raises the floor and
  the ceiling together.
- **Rule 12's consumed-end grounding changed verdicts again**, and produced K8: a consumer count is
  **per call site**, not per accessor. One accessor was load-bearing at one site and discarding its
  payload at another; an accessor-level count reports "consumed" and averages them into a number true
  of neither.
- **The lens rule (9.8.1-C) is not ceremony.** Every relation in every run — all the findings — came
  from the cross-entity-mechanism lens. The by-entity-row lens would have found **none** of them,
  because they are all edge properties.
- **`unchanged_examined` remains the right primitive.** The no-op made visible is what keeps DRY from
  being asserted.

---

## The thing I would tell the next author, above all the rest

**Every failure in this wave — mine, CVO~Z's, CTO~Z's — was an instrument that answered a narrower
question than the claim it supported. Not one was a carelessly gathered fact.**

My own two are the cleanest specimens, and they are consecutive:

- **CERT-5:** a footer enumeration ending in `head -10`; the fourth footer was line 11. I stated a
  denominator from a truncated list.
- **CERT-6:** a page count I carried **in my head** across six runs instead of deriving.

Both are the same failure — **a denominator that is a RECOLLECTION rather than an ARTIFACT** — on a
program whose central discipline is printing the denominator. `K10` now covers the first. The
sibling needs stating too: **never count from memory either.**

And the counterweight, because the method's best moment was also mine: I drafted the wave's
cross-page generalisation as *"shared producer predicts correct binding"*, **had it written into the
spec**, and ran it against all six rectangles rather than the five I remembered. **Two pages falsify
it in opposite directions.** The producer version fit five pages — and five is enough to feel
settled. The sixth page made testing it *cheap*; it did not make testing it *necessary*.

**A generalisation drawn from every case you happen to remember is the same defect as a count taken
from a truncated list.**
