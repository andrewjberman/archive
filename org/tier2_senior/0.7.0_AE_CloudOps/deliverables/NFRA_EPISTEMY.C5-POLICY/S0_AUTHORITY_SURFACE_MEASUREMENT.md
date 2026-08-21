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

## ⛔ FINDING — FOUR DEAD PRINCIPALS IN A LIVE AUTHORITY FILE (surfaced, NOT fixed)

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
