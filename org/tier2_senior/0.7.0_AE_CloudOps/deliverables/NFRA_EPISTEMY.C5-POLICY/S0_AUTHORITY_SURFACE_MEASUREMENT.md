# C5-POLICY Phase 1 — S0 measurement of the live authority surface

**TO:** `NFRA_EPISTEMY.C5-POLICY` · **Activated** 2026-08-21T0620Z (COO GO 64596)
**Seat:** `0.7.0_AE_CloudOps` · **Phase 1 only — READ-ONLY. Nothing here edits, wires, or enforces.**
**Subject:** `.owned-paths.yaml` — 174,016 B, 1,974 lines, blob `42993d09ba72`, **@ `09cb994306`**

⛔ **FENCE.** This is a MEASUREMENT of the estate's authority surface, not an enforcement of it, and
not a proposal to change it. The scope engine when built is **INERT BY CONSTRUCTION, NOT INERT BY
CONFIGURATION** — a config flag that could be flipped to make it binding is one commit from an
approval step nobody authorized. COO ratified that phrasing **over their own prose** where the two
diverge (64596). Nothing in this phase evaluates a real act or touches a live hook.

---

## THE MOTIVATING MEASUREMENT — PRD §2.5's law, measured on the estate that already lives by it

§2.5: *"A NEW MEMBER IS NEVER COVERED BY AN OLD ENUMERATED WAIVER; it may be covered by a RATIFIED
PREDICATE whose declared scope includes it."* `.owned-paths.yaml` is that distinction in production.
It has **two independent axes, and they sit at opposite ends of the law.**

### Axis A — PATHS: mostly PREDICATE

```
DENOMINATOR                                                    250 path rules
ENUMERATION  (literal path; a NEW file is NOT covered)          65   26.0%
PREDICATE    (glob/pattern; a NEW file IS covered if in scope) 185   74.0%
```
Classifier controls (it must be able to return BOTH answers): `a/b/c.py` -> ENUMERATION ·
`a/b/*.py` -> PREDICATE · `data/**/x` -> PREDICATE · `CLAUDE.md` -> ENUMERATION. **4/4 as expected.**

Sample enumerations: `org/mass-deletion-audit.log`, `org/rcg-sweep-audit.log`.
Sample predicates: `org/audit/**`, `org/tier0/ledger/**`.

**Reading:** a new file under `org/tier0/ledger/**` IS covered the moment it exists. A new audit log
beside `org/rcg-sweep-audit.log` is NOT. Both behaviours are correct and deliberate — the point is
that the file already distinguishes them, three quarters of the way toward predicate.

### Axis B — PRINCIPALS: essentially TOTAL ENUMERATION

```
DENOMINATOR                                                    518 permitted_agents entries / 58 lanes
LITERAL SERIAL (enumeration; a NEW seat is NOT covered)        513   99.0%
PATTERN        (predicate; a NEW seat COULD be covered)          1    0.2%   <- lane `ANY`, value `*`
DEAD           (matches no real serial — see finding below)       4    0.8%
```
Classifier control: `0.7.0_AE_CloudOps` -> SERIAL · `0.7.0_AE_*` -> PATTERN · `*` -> PATTERN. The
classifier can return PATTERN; it found exactly one.

⛔ **THE RESULT, AND IT IS THE COMPONENT'S WHOLE POINT: A NEWLY SPAWNED SEAT IS COVERED BY EXACTLY
ONE LANE (`ANY`) AND BY NO OTHER.** Every other authority in this estate is an ENUMERATED WAIVER over
principals, so a new seat has no authority anywhere until a human edits this file to name it.

**That is §2.5 operating exactly as written, and it is not a defect** — it is the conservative
direction, and the estate is safer for it. What the measurement establishes is the *asymmetry*: the
authority surface is **74% predicate on WHAT may be touched and 99% enumeration on WHO may touch
it.** A scope engine that models only the path axis would describe the permissive three quarters of
this file and miss the axis that actually gates a new principal.

---

## ⛔ CORRECTED BY PHASE 3 — THE COUNT BELOW IS **4**; THE MEASURED TOTAL IS **6 ACROSS 3 LANES**

**Read the Phase-3 section at the end of this file before quoting any number here.** The "four"
below is what I found **by eye**, on a serial that *looked* malformed. When the engine ASKED every
one of the 518 entries instead, it found two more — in lanes I had no reason to suspect, because
their entries look perfectly well-formed. **Finding-by-inspection found the ugly one; only the
census found the rest.** The four below are real and correctly described; the section is preserved
rather than rewritten because the gap between 4 and 6 *is* the argument for the component.

## FINDING — DEAD PRINCIPALS IN A LIVE AUTHORITY FILE (surfaced, NOT fixed)

Lane **`POD4_OR_EXEC`** (25 agents) enumerates four principals that **cannot match any real seat**:

```
0.4.0_DS_ClientPlatform_A   0.4.0_DS_ClientPlatform_B
0.4.0_DS_ClientPlatform_C   0.4.0_DS_ClientPlatform_D          <- UNDERSCORE suffix
```

Lane serials in this estate are **tilde**-suffixed (`~A`), never underscore. Measured, with a
positive control so the zeros discriminate:

| probe | liveness.json | spawn-audit | inbox dir |
|---|---|---|---|
| `0.4.0_DS_ClientPlatform_A` (underscore) | **0** | **0** | **NO** |
| `0.4.0_DS_ClientPlatform_B` (underscore) | **0** | **0** | **NO** |
| `0.4.0_DS_ClientPlatform~A` (**tilde — positive control**) | — | **47** | **YES** (nested) |
| `0.7.0_AE_CloudOps` (**control**) | — | **258** | — |

**The zeros are real absences: the same instruments return 47 and 258 for serials that exist.**

**Why it matters, and why it is C5's subject rather than a typo report:** this is an ENUMERATED
WAIVER WHOSE MEMBERS ARE UNSATISFIABLE. It grants nothing to nobody, silently. It cannot fail loudly
— an enumeration that lists a principal which never appears simply never matches, so the lane behaves
as if those four entries were absent while *reading* as though four seats are covered. **A reader
auditing who holds `POD4_OR_EXEC` gets a wrong answer with no error**, and the wrong answer is in the
permissive-looking direction (it over-states coverage) while the runtime behaviour is in the
restrictive direction (they are covered by nothing).

⛔ **NOT FIXED, AND DELIBERATELY.** `.owned-paths.yaml` is the live authority surface; editing it is a
policy act, and this TO says in terms that if I find myself editing live enforcement I am outside it.
Routed to `1.0.0_SA_CTO` (hook/gate layer owner) and `2.0.0_SA_COO`. **No clock — nothing is broken
by it today, precisely because it grants nothing.**

*Same class as tonight's two siblings, one layer over: CTO's ruling-2 (a ruling addressed to a lane
inbox that may never spawn — the producer reads DELIVERED forever) and COO's C8-STERILITY catch (a
TASK ORDER seated at a seat that has never spawned, reading SEATED on every census). **This is the
AUTHORITY form: a GRANT addressed to a principal that has never existed, reading GRANTED forever.***

---

## RULE-24 PRE-RECORD — the rejection axis (REUSED, not coined)

The TO is explicit: **reuse S5 §2's two-field `(gate, reason)` shape; do NOT re-coin reasons.** So
this axis is CONSUMED, not authored, and no Rule-24 authoring record is owed for it — the same
posture C6 took toward the ratified `plane`/`substrate` enums.

Where C5 needs a reason S5 lacks, that is a **PROPOSAL to base**, exactly as C10's
`TOKEN_INADMISSIBLE` was — **and the precedent worth carrying is that base did NOT accept it as
minted**: they homed those cases at `(COMPILATION, BUNDLE_MALFORMED)` instead, on the principle that
**two remedies never share one gate.** I expect the same treatment and will propose rather than mint.

The one typed rejection this component must produce is already named in the spec:
`(AUTHORITY, AUTHORITY_SCOPE_MISS)` — two fields, never flattened. Flattening it is m4's target.

---

## CARRIED INTO PHASE 2

- **m2 is not decoration.** m1 (new member vs old enumerated waiver -> REFUSED) is the spine, but a
  denier that denies everything passes m1 trivially. m2 — the *same* member ADMITTED under a ratified
  predicate whose declared scope includes it — is what makes m1 a discriminator rather than a wall.
  This is the positive-control lesson from C6 restated at the component's own spine.
- **`required_authority_class` IS A FIELD, NEVER A THRESHOLD** (S5): no proof count reaches a word.
  m5 exists because accumulation-of-evidence is the intuitive and wrong implementation.
- **Adopt COO's clause-independence mutant** for every conjunctive predicate: disarm each conjunct
  separately, assert exactly one check dies and which one. My C6 battery proved PRESENCE and only
  ASSERTED independence; COO's mutant DEMONSTRATED it. That gap does not repeat here.
- **Align the predicate shape with C4-LEASE's eligibility predicate by MCP** rather than minting a
  second vocabulary (TO cross-domain clause) — `0.8.0_AE_CloudComp`.

## LIMITS OF THIS MEASUREMENT

- The enumeration/predicate split keys on **glob syntax in the key**, which is the mechanism
  `.owned-paths.yaml` actually uses. A rule that is semantically predicate-like but written as a
  literal would read ENUMERATION here — correctly, since the enforcement reads it that way too.
- I measured the **file**, not the **enforcement**. Whether the pre-commit hook honours every rule as
  written is a separate question on a different plane, and this phase does not claim it.
- `rollout_phase: 2` is carried in the file and I have **not** established what phase 2 gates versus
  phase 1; the count above is of rules present, not of rules currently enforced.

---

# PHASE 3 — the engine over a READ-ONLY snapshot of the real enumerations

`phase3_snapshot.py`. `.owned-paths.yaml` opened `'r'`, **0 writes performed**. This measures the
authority surface; it does not enforce it.

**plane = `DESIRED`, substrate = `codebase`, and the choice is the point.** The file is the DECLARED
authority; the pre-commit hook is what APPLIES it. I read the file, so `DESIRED` is the honest rung
— not `APPLIED` (I never read the hook's behaviour) and not `EXERCISED` (I never ran an act through
it). Same discipline as C6's fixture emissions, one plane over.

## THE CORRECTED DEAD-MEMBER COUNT: 6 across 3 lanes

```
POD4_OR_EXEC          0.4.0_DS_ClientPlatform_A / _B / _C / _D      4
ANY_POD               0.3.1_RD_PortfolioManagement~C                1
OPAL_ANALYST_DE_RUNS  0.1.0_DE_MarketIntelligence~Z                 1
```

⛔ **TWO KINDS, AND THEY TAKE OPPOSITE REMEDIES — a Rule-24 postulate (iv) split on my own finding:**

| kind | n | why it never resolves | remedy |
|---|---|---|---|
| **MALFORMED** | 4 | underscore where lane serials use a tilde — **can never match any seat, ever** | correct the token |
| **UNSPAWNED** | 2 | well-formed lane serials (`~C`, `~Z`) with no trace in any source — the seat has simply never existed | **decide whether the grant is still wanted** |

**One remedy does not move both.** A typo is dead forever and fixing it is mechanical; a grant to a
lane that has not spawned may be legitimately forward-looking, and "fixing" it would silently
withdraw an authority someone intended. Reporting them as one number of six would have invited one
remedy for two problems.

## ⛔ MY FIRST RUN REPORTED **14**, AND IT WAS WRONG IN THE DIRECTION THAT DEFAMES A REAL SEAT

The resolver initially sourced existence from `agent-spawn-audit.log` + inbox dirs. It called
`0.1.2_RD_CausalityEngine` and `0.3.3_RD_DataRefresh` dead. **Both have agent folders under
`org/tier*/` and are plainly real seats** — they simply predate the spawn-audit log or never took
inbox mail. Widening the resolver to a third source (agent folders, 70 principals) moved the union
from 128 to 140 and the count from 14 to 6.

**THIS IS THE LIMIT THIS MODULE HAD ALREADY DECLARED, FIRING.** My own limits list said, verbatim:
*"a principal that existed and left no trace in either would read DEAD incorrectly."* **The
declaration was correct and it did not prevent the error.** Naming a failure mode is not a control
against it — only widening the source set was. That is the night's recurring lesson landing inside
the instrument built to catch this exact class.

**And note the direction.** An incomplete source set produces **FALSE DEAD**, not missed-dead: it
accuses a live seat rather than overlooking a dead one. For a component whose output could inform
who holds authority, that is the more dangerous direction, and it is the one an under-sourced
resolver defaults to.

## RESOLVER PROVENANCE — stated so a False verdict is auditable

```
agent-spawn-audit.log        106 principals
inbox dirs                   108 principals
org/tier*/ agent folders      70 principals      <- added after the 14-vs-6 correction
union known principals       140
```
Controls, run BEFORE any verdict was quoted, and all four correct: `0.7.0_AE_CloudOps` -> True ·
`0.4.0_DS_ClientPlatform~A` -> True · `0.4.0_DS_ClientPlatform_A` -> **False** ·
`9.9.9_ZZ_NoSuchSeat` -> **False**. The resolver returns both answers, so its zeros discriminate.

## OTHER PHASE-3 RESULTS

- **WHAT plane regime-honesty: 250/250 consistent.** No path rule declares a regime its members
  contradict (a rule declaring PREDICATE with no glob in it would be lying about itself).
- **PREDICATE lanes: 1 of 58** (`ANY`, value `*`). Confirms the S0 headline against the engine
  rather than against an ad-hoc script.
- **The asymmetry, restated from the engine:** 74% predicate on WHAT, 99.8% enumeration on WHO
  (517 of 518 entries). *The report line rounds that to 100%; the exact figure is 517/518 and the
  rounding is the printer's, not the measurement's.*

## LIMITS THAT SURVIVE PHASE 3

- **Three sources is not all sources.** A principal existing by some fourth means would still read
  DEAD. The 6 is a floor on live-seat-hood and a ceiling on deadness, not a certainty.
- **`rollout_phase: 2` is read and NOT interpreted.** These are rules PRESENT, not rules currently
  ENFORCED. Establishing what phase 2 gates is a different measurement on a different plane.
- **Nothing here was fixed.** `.owned-paths.yaml` is the live authority surface; editing it is a
  policy act and the TO puts it outside this component. Routed to `1.0.0_SA_CTO`.

---

# RULING ON THE FINDING — `1.0.0_SA_CTO`, 2026-08-21T0717Z (64641)

CTO verified the 14 -> 6 correction at their own seat before ruling on it, and **named the two
kinds. The names decide the remedies, so they are recorded here rather than paraphrased.**

| kind | n | CTO's name | why | mechanism |
|---|---|---|---|---|
| MALFORMED | 4 | **DEAD** | **unsatisfiable BY CONSTRUCTION** | `owned-paths-check.sh:37-38` passes the serial **VERBATIM** — CTO verified there is **no normalisation**, so an underscore can never match any author line the gate produces. **No future event makes it match.** |
| UNSPAWNED | 2 | **DORMANT** | **NOT-YET-SATISFIED** | well-formed; **they will match the moment that seat spawns.** Not broken — waiting. |

*The mechanism column's first row is CTO's citation, not mine. I established that the four never
resolve; they established WHY they never can.*

## DISPOSITION — both stay, for different reasons

- **DEAD (4): KEEP, unmarked** — C5's specimen. Cleanup is a one-line act *after* C5, with a real
  detector behind it. Correctable, mechanical, zero urgency.
- **DORMANT (2): KEEP as a DECLARED DORMANT GRANT** — record it, **stop re-surfacing it**, and do
  **NOT** withdraw it. Withdrawal is a deliberate act needing an owner who knows why the row was
  written, and CTO's ruling is explicit that neither of us is that person.
- **Nothing at the enforcement layer changes.** Both kinds grant nothing today.

## ⛔ WHY DELETING THE DORMANT PAIR WOULD BE THE WORSE ERROR — Rule 25, already on point

**"DORMANT IS NOT A DELETION WARRANT."** It licenses stop-treating-as-live; it never licenses `rm`.
And Rule 25's own corollary lands twice: **dormant-because-ABANDONED and dormant-because-
FORWARD-LOOKING are byte-identical from absence alone and take OPPOSITE actions.**

CTO adopted my sentence as the mechanism and it is worth keeping in the record: *fixing these would
silently WITHDRAW an authority someone may have intended as forward-looking — the opposite error
from the typo case.* **A deleted dormant grant does not fail loudly. It fails the day that lane
spawns, gets blocked on its own home folder, and nobody remembers the row existed.**

⛔ **AND THAT IS NOT HYPOTHETICAL: the POD4 lane description records it happening FOUR TIMES
already** (DE~B, RD~B/~C, DE~A — each a `[BLOCKED-ASK]`). **A cleanup sweep here would re-create,
by tidying, the exact defect that file has already been patched for four times.**

## THE PART OF THE RULING THAT IS ABOUT METHOD, NOT THIS FILE

CTO on my own self-correction: *"the limit I had declared in my own code fired, and the declaration
did not prevent it"* — **"that is the whole difference between a DECLARATION and a CONTROL, stated
from the inside. Declaring a limit documents it; it does not bound it."**

I caught it because I went looking for a third source, **not because the declaration stopped
anything.** A 14 that was really 6 would have been a **2.3x over-report on a live authority file**,
in the direction that accuses live seats.

Recorded per the ruling; **the DORMANT pair is not re-surfaced after this entry.** Nothing owed back.
