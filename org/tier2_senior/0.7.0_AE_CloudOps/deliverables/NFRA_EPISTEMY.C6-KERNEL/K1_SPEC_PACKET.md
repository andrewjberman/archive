# C6-KERNEL K1 SPEC PACKET — for `4.0.0_SA_CRO` base spec cert, then `1.0.0_SA_CTO` arch gate

**Objects:** `Transition_Unit` · `Transition_Manifest` · `Cumulative_Residue_Ledger`
**Spec of record:** `docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md` §2.7 (17,905 B, blob `7cd650d536e7`) **@ `f32a5c0019`**
**Route:** CRO base spec cert → CTO arch gate. Pre-existing in the TO; no step added.
**Fence:** BUILD-STAGING. Nothing wired to a live path, no gate armed, no monitor, no embryo modified. **Activation on any real mutation class is Andrew's worded act.**

## VINTAGE PINS — every citation in this packet resolves at these commits

Per CTO bar item 3. The C4 census cited the rule bank's `:455`/`:501` bare; both moved 22 minutes
later, and the clause that moved was Rule 22's own *"A LINE CITATION WITHOUT A VINTAGE IS NOT A
CITATION"* — the claim was true at its vintage and now reads false. This packet is pinned so it
cannot invert the same way.

| artifact | bytes | blob | commit |
|---|---|---|---|
| `transition_kernel.py` | 30,569 | `5f98f35c8ac6` | **`7b91a7d4b0`** |
| `exercise_kernel.py` | 13,685 | `d341d2372768` | **`b05e98f46a`** |
| `exercise_inexpressibility.py` | 7,156 | `f739e2bc0561` | **`5ab3d9dc91`** |
| `exercise_k6_observation.py` | 6,174 | `1e348de55378` | **`f351a2a916`** |
| PRD §2.7 (spec of record) | 17,905 | `7cd650d536e7` | **`f32a5c0019`** |
| `observation_record.schema.json` (C1 envelope) | 4,262 | `4673036e8d12` | **`6f944857c4`** |
| `NFRA_ONTOLOGY_RULE_BANK.yaml` | 109,632 | `a7446efbf720` | **`5fc45ad69d`** |

---

## 1. THE TWO INEXPRESSIBILITY PROPERTIES — EXERCISED, NOT READ

CTO's bar item 1, discharged at **`5ab3d9dc91`**. The ruling behind it is the load-bearing part:
*"inexpressible" is a claim about what the API REFUSES, and absence-of-a-method in a source file is
exactly the shape that reads clean while a `__getattr__`, a base class, a mixin, or a
dataclass-generated ordering quietly provides it.* A source read cannot settle it.

**Property A — a scalar residue is inexpressible.** 10/10 forbidden ops refused:
`v1<v2`, `v1>v2`, `sorted([v1,v2])`, `float(v1)`, `int(v1)`, `sum([v1,v2])`, `v1+v2` → `TypeError`;
`v1.total()` → `AttributeError`; `ResidueVector(axes={})` and a non-numeric axis → `ValueError`.
The structural evidence CTO asked for by name, printed in the transcript:

```
decorator                    @dataclass(frozen=True)      <- no order=True, nothing generated __lt__
MRO                          [ResidueVector, object]      <- no mixin or base supplying it
'__getattr__' in __dict__    False                        <- nothing synthesises on miss
ResidueVector.__lt__         is object.__lt__             <- resolves to the refusing default
```

**Property B — an agent-self-reported ledger row is inexpressible.** 9/9 refused: `append`,
`add_row`, `submit`, `append_row`, `add`, `insert`, `record_row` all `AttributeError` (seven probed,
seven absent); `record_measurement(..., 7.0, ...)` → `InadmissibleRow`; a non-numeric measurement →
`InadmissibleRow`. Public surface is exactly `[cumulative, record_measurement, rows]` — **no
row-shaped door.**

**POSITIVE CONTROLS, 5/5, in the same transcript**, because CTO named the real gap: an all-`TypeError`
transcript is equally consistent with a *broken object*. `within()` returns its per-axis verdict,
`breached_axes()` returns the list, equality works, `record_measurement(lambda: 3.0)` records a real
`LedgerRow`, `cumulative()` reads it back.

⛔ **HONEST CEILING, unchanged and not raised at CTO's explicit instruction:** Python has no true
privacy; a determined caller can reach `_rows`. The claim is **inexpressible through the public
API**, not cryptographic integrity. What that distinguishes is the S0 finding — the deploy ledger's
`cmd_open`/`cmd_close_leg`/`cmd_close` exist *precisely to accept an agent's assertion*. Difference in
kind, not a claim of tamper-proofing.

---

## 2. RULE-24 FOUR-POSTULATE RECORDS — layer named FIRST, then the uncovered member hunted

### Axis 1 — `Terminal` (4 values). Declared layer: *the terminal states of ONE governed transition.*

| value | does any effect survive? | is survival bounded? | recovery debt |
|---|---|---|---|
| `COMPLETED` | no — intent achieved | n/a | none |
| `ROLLED_BACK` | **no** | n/a | paid, and the payment is proven |
| `CONTAINED` | **yes** | **yes**, declared | outstanding, **priced**, unpaid |
| `ABANDONED_UNSAFE` | yes | **no** | unpayable — escalation |

- **(i) MECE** — disjoint on the two questions above; CE hunted by asking what a transition past a
  point of no return with unpayable debt would be filed as. Without the fourth value it would be
  mis-filed `CONTAINED`, **asserting a boundedness nobody established**. That is how the uncovered
  member was found.
- **(ii) SAME GRAIN** — all four are whole-transition terminals. `LegOutcome` is a *separate axis*
  precisely so a leg-level value never sits beside a transition-level one.
- **(iii) INTENT COHERENCE** — terminal STATE only. No disposition, blame, or next-action axis mixed in.
- **(iv) STATE COHERENCE — ⛔ NOT SATISFIED, AND DECLARED.** Three values are reachable by kernel
  logic; `ABANDONED_UNSAFE` is reachable **only by escalation**. One remedy does not move all four, so
  a "build the terminal handler" plan silently covers three of four. Named rather than absorbed.

**`CONTAINED` vs `ROLLED_BACK` is the whole point of the axis.** A kernel with only `ROLLED_BACK`
must report a partially-landed transition as rolled back — **false in the direction that HIDES
STRANDED STATE**, which is the 2026-06-11 class NEVER#8 exists for.

### Axis 2 — `LegOutcome` (**5 values, amended**). Declared layer: *the outcome of ONE leg.*

`LANDED` · `REFUSED_PREFIX_SAFETY` · `REFUSED_SUPPORT_HANDOFF` · `ABORTED_AT_CHECKPOINT` ·
**`FAILED_MID_ACT`**

⛔ **AMENDED BY A1 — minted by `4.0.0_SA_CRO` as registry executor, K1 spec cert @ `b895b7e337`,
resolving the CE gap this packet declared as residual 1.** Census run at base before the mint: 0
occupancy across the canon trio + `CLAUDE.md` + `RULINGS`. The amended record rides my implementing
commit; no re-cert.

- **(i) MECE — CE NOW CLOSES.** A leg either landed, was refused before the act (by one of two
  distinct gates, kept separate so the battery can discriminate which fired), aborted deliberately at
  its checkpoint, or **crashed mid-act**. The fifth value is the one I found by hunting and did not
  mint, because minting is an authoring act.
- **(ii) SAME GRAIN** — all five are per-leg. **(iii) INTENT COHERENCE** — outcome only.
- **(iv) STATE COHERENCE** — satisfied; all five are produced by the same code path.

**CRO's reasoning is the load-bearing half and it is why this is not bookkeeping:** *the most
dangerous leg state — possible PARTIAL EFFECTS, i.e. the stranded-state class — must not be the least
recorded.* Before A1, an unexpected mid-act exception propagated and **no `LegRecord` existed at
all**, so the one outcome that can strand state was the one outcome the ledger could not express.

**Implemented behaviour, and RECORDING IS NOT SWALLOWING** — the kernel records the row, marks the
affected residue axis **UNKNOWN** (a crashed act's residue is genuinely unmeasured, never `0` — that
would be the sentinel bug again), and then **RE-RAISES** so the caller still sees the crash.
Exercised as **m8**, asserting *both* limbs because either alone is a different and wrong behaviour:

```
[FIRED] m8 act() raises -> RECORDED *and* RE-RAISED (A1):
        recorded=FAILED_MID_ACT  re-raised=True  unknown_axes=['objects_written']  rows=0  -> CONTAINED
```

`rows=0` is asserted deliberately: **no measured row is invented for a leg that crashed.** The ledger's
ROW set stays a set of measurements while the OBSERVATION set stays a complete census of acquisitions
*including the ones that could not be made*.

**And `terminal()` refuses to price what it cannot measure.** A transition with a `FAILED_MID_ACT` leg
can never resolve `COMPLETED` or `ROLLED_BACK`, and its reason states that the measured debt is a
**FLOOR, not the debt** — quoting the sum of measured rows as *the* rollback debt would be a
wrong-denominator error inside the very object whose job is pricing rollback.

### Axis 3 — `plane` / `substrate` (CONSUMED, not authored)

C6 does **not** mint these. They are the ratified C1 enums at **`6f944857c4`** — plane ∈ {`DESIRED`,
`APPLIED`, `EXERCISED`}, substrate ∈ {`aws`, `portal`, `codebase`, `ms`} — named in
`RATIFIED_PLANES`/`RATIFIED_SUBSTRATES` so a call site cannot invent a value, and **never branched
on**. No Rule-24 record is owed for an axis this component consumes.

⛔ **THE ONE DEPARTURE IN THIS BUILD, stated here because a cert should not discover it:** K6's
criterion and CTO's bar item 5 both say emit `plane=APPLIED`. **The fixture run emits
`EXERCISED`/`codebase`.** C10-PRECOND hardcodes `APPLIED`/`aws` correctly *there* — it performs real
conditional writes against real S3 objects. C6's exercise touches no cloud substrate, so `APPLIED/aws`
would assert a plane the measurement never stood on: a false record authored into the artifact whose
entire job is carrying a plane honestly. Both are **constructor parameters**; an activated call site
(Andrew's worded act only) passes `APPLIED/aws`. Raised to CTO 040924Z.

---

## 3. TOKEN CENSUS — word-boundary occupancy, per file, with controls

Six canon files read (**6 of 6 readable**; an absent file is not searched and its zero would not be
covered): `CLAUDE.md` 89,556 B · `RULE_BANK` 109,632 B · `SYSTEM_DEFINITIONS` 94,711 B ·
`canon-patterns` 15,219 B · `RULINGS` 31,064 B · `PRD_EPISTEMIC` 17,729 B.

**CONTROLS RUN FIRST, so a clean census is known to discriminate:** positive `Observation_Record`
= 2 (`SYSTEM_DEFINITIONS` 1, `PRD_EPISTEMIC` 1); negative `zzzNoSuchTokenAbc9999` = 0.

**22 newly-minted tokens: 20 at zero occupancy, 2 occupied — and both are correct.**
`Transition_Unit` = 1 and `Cumulative_Residue_Ledger` = 1, **both in the PRD only**. Those are the
spec's own names, which this component realises. **That is the citation, not a collision** — a zero
there would have meant I was building against a name §2.7 does not use.

**Six reused generic tokens, censused separately so the two classes are never conflated:**
`COMPLETED` = 4, `CONTAINED` = 1, `LANDED` = 9; `Checkpoint`/`Interval`/`Terminal` = 0.
**Each occurrence inspected, not just counted:** all are English prose, none is a schema value on a
colliding axis. Specifically `RULE_BANK:553` **@ `5fc45ad69d`** reads *"IS CONTAINED BY
`AEventMotif`"* — prose; the containment relation family is `CONTAINS`/`CONTAINS_DRILLDOWN`
(`RULE_BANK:141`), **not** `CONTAINED`. And `CONTAINED` is §2.7's own word (*"terminals incl.
rollback+containment"*), so it is the spec's vocabulary, not a coinage.

**SUBSTRING-COLLISION CHECK — the `BUILD-OTHER`/`NON-BUILD-OTHER` class: NONE.** No token
word-boundary-matches inside any sibling. Run because COO's census on the `phase` enum caught exactly
this hours ago (`grep -w BUILD-OTHER` matched inside `NON-BUILD-OTHER`, raw 59 = 58 siblings + 1
genuine), which would have put two values on one axis in a **permanent** substring relationship —
every future census, audit or grep keyed on one silently including the other, forever, with no error.

---

## 4. S6 ABSENCE SEMANTICS — on every nullable, a null names what its absence DISQUALIFIES

| site | the absence | what it disqualifies |
|---|---|---|
| `ResidueVector.within()` | an axis present in the residue, **absent from the envelope** | the axis is **DISQUALIFIED, not blessed** — an undeclared limit is not a permitted one |
| `CumulativeResidueLedger.cumulative()` | **no measurements at all** | returns `None`, not a zero vector — "nothing measured" is not "residue zero" |
| `SupportClaim.check()` | `actual_at(now)` returns `None` | the claim is refused — an absent lease is not an unexpired one |
| `substantive_result` on a refused acquisition | value `None` | state `UNKNOWN` **with a reason**, never a missing record |

The second row is a bug the battery caught on its first run, kept in the docstring rather than
erased: I had manufactured a sentinel axis `{"_no_measurement": 0.0}` to keep the return type
non-Optional, and **this module's own S6 rule refused leg 1 of every transition** — the sentinel was
a scalar *"nothing here"* wearing an axis name, precisely what `ResidueVector` exists to forbid.
*The component's own thesis firing against its author.*

---

## 5. RESIDUALS — declared, not absorbed

1. ~~**`LegOutcome` CE gap.**~~ **RESOLVED by A1 @ `b895b7e337`** — CRO minted `FAILED_MID_ACT` as
   registry executor and I implemented it; see Axis 2 above and battery case m8. Struck rather than
   deleted so the route is legible: *the builder found and declared the gap, the registry executor
   minted the value, the builder implemented it.* At no point did I widen an axis on my own
   authority, which is the whole reason the residual was declared instead of quietly filled.
2. **`PointOfNoReturn` DELETED @ `7b91a7d4b0`.** Found by auditing this module before handing it over:
   `defined=1, raised=0`, against a control of `raised=3` for `PrefixSafetyViolation`. Deletion is the
   correct fix, not wiring it up — crossing a declared point of no return is a **legitimate act**, not
   a refusal; the refusal comes later at the safe-terminal clause (which m2 exercises), and the
   concept lives on the Terminal axis as `ABANDONED_UNSAFE`. **The hazard was not inertness:** a
   reader would reasonably write a caller catching an exception that cannot occur — a handler for an
   unreachable branch, which reads as defensive and is dead.
   `KernelRefusal` remains `defined=1, raised=0` and that is **correct** — it is the base class, never
   raised directly. Stated so it does not read as a second dead token.
3. **The census tests token PRESENCE, not AXIS BINDING.** It answers *"does a canon file mention this
   token"*, not *"is it bound on a colliding axis"*. The controls bound the instrument's
   discrimination, not its semantics. I inspected all six reused-token occurrences by hand for that
   reason; the method does not scale and is not claimed to.
4. **`harm_model` is a STAMP ONLY** (rider (a) — §2.9 is not buildable spec). Nothing is built against it.
5. **K5's abort runs on a FIXTURE**, which the TO sanctions ("scratch/fixture"). It is not a
   real-plane rollback, and the proof says so rather than implying an exercised production recovery.

---

## 6. WHAT THIS PACKET ASKS FOR

CRO base spec cert on the three objects against §2.7 **@ `f32a5c0019`**. Then CTO's arch gate, whose
five bar items are addressed: item 1 §1 (exercised), item 2 §2 (four postulates, layer-first), item 3
§0 + throughout (vintage pins), item 4 §2/§5 (staged vs executing stated), item 5 §2 (K6 landed first,
with the plane departure declared).

Evidence is reproducible at the pins above: `python exercise_inexpressibility.py` (24/24),
`python exercise_kernel.py` (8/8), `python exercise_k6_observation.py` (3/3 schema-valid) —
all true rc=0 read UNPIPED.
