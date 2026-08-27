# L1-m-graindecl — THE CANONICAL GRAIN, DECLARED AND FALSIFIABLE

**Cell** `L1-m-graindecl` · **TO** `NFRA_C3MATERIALIZE.TO-L1-DTX` · **decomp pin** `@4226a09f74`
**Declared by** `0.4.0_DT_ClientPlatform~X` · **Oracle:** *"a written, falsifiable declaration of the
canonical grain, which NAMES WHAT IT IS NOT and states what observation would show it wrong. The PRD
demands falsifiable, not merely stated."*

---

## THE DECLARATION

> **The canonical grain is the ordered pair `(PLANE, ENTITY)` — not a single universal entity type.**
>
> Every id space declares its own entity grain and the roll-up it uses to reach the plane's
> canonical entity. **Comparison is admissible WITHIN a plane. Across planes it is admissible ONLY
> through an explicitly declared bridge relation**, never through a shared token, a shared string
> shape, or a parse.

**This is a declaration that the estate has FOUR canonical grains, one per plane, plus a named
bridge obligation — not one grain.** That is a weaker and more expensive claim than "the canonical
grain is X", and I am making it because the measurement below refuses the stronger one.

---

## WHY — MEASURED, NOT REASONED

**No single natural grain contains all four spaces.** Measured at `@baca7f07eb`:

| space | its entity | contained by a file? | reaches the others how? |
|---|---|---|---|
| `symbol` | component · type · prop · jsx site | **yes** | roll-up to `file` |
| `file` | a repo path | is the container | — |
| `arn_resource` | a cloud resource | **no** — an S3 bucket is in no file | no containment path at all |
| `chain_motif` | a motif instance over members spanning planes | **no** — it spans them | membership, not containment |

`symbol` and `file` are in a CONTAINMENT relation. `arn_resource` is not inside anything in the repo.
`chain_motif` instances span members across planes by construction. **A grain that claimed to contain
all four would be containing an S3 bucket in a TypeScript file.**

### The roll-ups, each a RELATION with its cardinality

| roll-up | children → parents | fan-in max / mean | declared by the store? |
|---|---|---|---|
| `symbol → file` | 10,265 → 284 | 1,290 / 36.14 | **NO** — 0 of 16,811 portal edges target a Module |
| `chain_motif instance → family` | 6,207 → 13 | 1,649 / 477.46 | **partially** — the 19 family ids exist as nodes |
| `arn_resource → service` | 1,851 → 22 | 678 / 84.14 | **NO** — parsed from the ARN string |
| `pipeline symbol → firm` | 1,337 → 3 | 724 / 445.67 | **NO** — parsed from the id prefix |

**Not one collapses to a single target** (AC5). Three of four are **declared nowhere** and exist only
as a convention inside an id string.

⚠ **AND A LIMIT OF MY OWN INSTRUMENT, STATED SO IT IS NOT READ AS A RESULT.** Every row above shows
`fan-out = 1` (one parent per child). **That is a TAUTOLOGY OF THE PARSE, not a measurement**: each
parse yields exactly one parent string by construction, so the probe *cannot* return fan-out > 1.
The genuine multi-parent case is the CROSS-STORE one measured separately — the firm-blind token
`gold` resolves to `pipeline:bd:gold`, `pipeline:inf:gold` and `pipeline:mdpf:gold`. **A reader
taking `fan-out = 1` as evidence that roll-ups are functions would be reading my instrument, not the
world.**

---

## WHAT IT IS NOT

- ⛔ **NOT the SYSTEM.** `1.0.0_SA_CTO~X` ruled identity grain to EVERY ENTITY on four measured
  failures, three of which were *below* the system grain. A system-grain spine cannot express the
  540 cross-domain memberships, cannot hold "materializer is a relation, not a property", and did
  not help the zero-join.
- ⛔ **NOT the FILE.** `arn_resource` has no file. Declaring `file` canonical would silently drop an
  entire plane, and it would drop it *quietly* — the fusion would still return a matrix.
- ⛔ **NOT the SYMBOL.** The coarser spaces cannot be split down to it. `arn_resource → symbol` is
  not a roll-up in either direction; it is a category error.
- ⛔ **NOT A SINGLE INTEGER POPULATION.** Three of four spaces are multi-substrate (measured), and
  for the two I can fully resolve the PRD's number is exactly ONE substrate's count while the true
  union is larger. A canonical grain that implied one count per space would inherit that error.
- ⛔ **NOT a token match.** `resource_summaries` measured `crosses_spaces = FALSE` while carrying
  ARNs — an ARN row key inside one Iceberg table. Same token, different grain.

---

## ⛔ WHAT OBSERVATION WOULD SHOW THIS WRONG

**This declaration is refuted by any ONE of the following. Each is a real, runnable check.**

1. **A COMMON PARENT EXISTS.** Exhibit a single entity type that all four spaces roll up to
   **without a hand-written parse** — i.e. reachable through relations the stores themselves
   declare. *Current state: the store declares 0 of 16,811 portal edges into a Module, so even the
   symbol→file roll-up is parse-only. If declared edges appear that carry all four to one parent,
   the per-plane split is unnecessary and this declaration is wrong.*

2. **A PLANE IS NOT CLOSED.** Exhibit two entities in the SAME declared plane that cannot be
   compared at that plane's grain. *That would mean the plane is not a valid comparison scope and
   the grain must be finer than I declared.*

3. **THE BRIDGE IS UNNECESSARY.** Exhibit a cross-plane comparison that is sound WITHOUT a declared
   bridge relation — a join across planes on a shared key that is measurably the same grain on both
   sides. *One case would show the bridge obligation is over-strict.*

4. **THE CONTAINMENT CLAIM IS FALSE.** Exhibit an `arn_resource` or a `chain_motif` instance that IS
   contained by a file in the same sense a `symbol` is. *That would collapse the four planes toward
   one and refute the "no single natural grain" premise this rests on.*

**Falsifier 1 is the cheap one and it is the one I would run first.** It is a query over declared
edges, not a judgement.

---

## WHAT THIS COSTS, STATED BECAUSE A DECLARATION THAT HIDES ITS COST IS A WISH

**Four canonical grains plus a bridge obligation is strictly more expensive than one grain.** Every
cross-plane consumer must now name the bridge it is using, and there is currently **no declared
bridge for any pair** — three of the four roll-ups above are parse-only, so the bridges do not
merely need declaring, they need *building*.

**I am declaring it anyway, because the cheaper claim is measurably false**, and because the failure
mode of the cheaper claim is the one the PRD names: a fusion across mixed grain does not error, it
returns a beautifully-formed matrix comparing a React prop to a gold script.

---

## ⛔ THE EVIDENCE THAT PERSUADED ME, AND IT IS AGAINST MY OWN WORK

While measuring these four spaces I mis-derived an id space **five times**, every time by taking a
PATTERN instead of a DECLARED TYPE OR GRAIN:

| # | what I did | result | true value |
|---|---|---|---|
| 1 | regexed portal ids containing `/` as file paths | swept in `endpointurl:/api/...` URL routes → 4,978 | 374 |
| 2 | keyed on node_type but split only on `#` | admitted `path:LINE:symbol` → 4,933 | 374 |
| 3 | read `nodes[].id` where the declared key is `node_id` | **silent 0** for a 6,161-id substrate | 6,138 |
| 4 | merged `motif:` with `motifi:` on a shared prefix | 6,113 crossing | 6,090 |
| 5 | read parse-imposed `fan-out = 1` as a property of the world | (caught before publishing) | tautology |

**Not one was caught by a control.** Three were caught by contradicting an earlier measurement of my
own, one by reading a sample the probe printed, one by re-reading the probe.

> **This is the argument for the declaration, made against the seat that wrote it.** The lane
> building the spine mis-derived the spine's own objects five times in one session *while trying to
> be careful and while holding the rule in mind*. A canonical grain that must be RE-DERIVED BY EACH
> CONSUMER will be re-derived wrongly. **Declaring it is not tidiness; it is the only mechanism that
> has ever stopped this class**, and CLAUDE.md §4's consuming-half law says why: holding a rule in
> mind does not produce compliance — only something that refuses the value does.

---

## STATUS

`status: DECLARED` · `basis: measured` · `evidence: this document + @38d60dc, @baca7f07eb probes` ·
`owner: 0.4.0_DT_ClientPlatform~X`

**Not yet certified.** `3.0.0_SA_CVO~X` certifies. Falsifier 1 is the attack I nominate against this
cell, and it is cheap to run.
