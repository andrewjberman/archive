# OPAL_ADVIPOINTERS — lane `0.4.0_DS_ClientPlatform~A`: FIVE-FIELD REPORT + the B_00 REPAIR SPEC

**To:** `1.0.0_SA_CTO` for inclusion in `docs/architecture/OPAL_ADVIPOINTERS_PRD.md`.
**Two asks, one document:** Andrew-direct *"spec the repair and send to CTO for inclusion in
their ADVIPOINTER PRD"* (PART A) + CTO 153942Z five-field lane report (PART B).
**Convention honored:** commits cited not described; every number carries its denominator;
anything not personally verified is labeled **INFERRED**.

---

# PART A — SPEC: INF `B_00` valuation-basis repair (insert-ready, P1-SCRIPTS)

## A.1 Authority

| Element | Source |
|---|---|
| Basis ruling | joint CTO+COO 08-11 window ruling, option **(b) RAW portfolio-domain currentValue** |
| Scope extension to B_00 | **CTO 152134Z** — *"THE BASIS EXTENDS TO B_00 … the ruled law is BASIS-level, not FILE-level"* |
| Discriminator preservation | CTO 152134Z, **ADOPTED verbatim** from my rec |
| Population-axis requirement | CTO 152134Z — *"A VALUE PIN CANNOT SEE A POPULATION CHANGE"*; pins committed pre-build |
| Reserved-choice marker now discharged | `b00_canonical_valuation.py:11` *"THE FIX CHOICE IS AT CTO+COO, not here"* |

## A.2 The defect (measured 2026-08-12, denominator 908 IN_CLIENT_BOOK accounts)

`B_00` sums `activity.ending_mv` — the 3-year-window Activity artifact in which **vendor-ABSENT
coerces to `0.00`**. On today's partition **423 of 908 (46.6%)** read exactly `0.00`; of those
**312 are contradicted by positions** and **111 are corroborated** (312 + 111 = 423 exactly).
The 312 carry **$68,676,658.56**. Plane sum **$140,548,736.81** against a served
`total.aua` of **$209,225,005.59** — a **$68.7M** disagreement on the same quantity.

**Same class, three independent derivations:** B_00's own positions discriminator · the roster
basis · the original fee-earning investigation's suppressed set. All return **312**.

## A.3 ⚠ THE LOAD-BEARING DESIGN DECISION — a CONSUMER-CONTRACT CHANGE, ratification requested

This is the part that must not be decided silently by an implementer, and it is why this is a
spec rather than a commit:

- **`c02_twr_engine.py:112`** gates on **`if b_st != "OK" or e_st != "OK"` → UNCOMPUTABLE.**
  It keys on **`value_status`, NOT on the value.**
- **`b03_valuation_integrity.py:67`** checks `value_status ∈ {ZERO-CONTRADICTED-BY-POSITIONS,
  SOURCE-ABSENT}` → `VARIANCE-EXPLAINED`, **before** its tie test.

**Therefore, repairing only the value and leaving `value_status` activity-based would:**
1. keep all **312** accounts UNCOMPUTABLE in C_02 — the repair would land in the data and
   **change nothing downstream**; and
2. **mask 312 now-clean ties** in B_03 as "explained," hiding a genuine TIE behind a stale
   explanation of a defect that no longer exists.

**PROPOSED (CTO to ratify or amend):** `value_status` describes the **AUTHORITATIVE VALUE**;
the activity-plane discriminator is **preserved under a distinct name** as the provenance
record. This satisfies *"it stops being the VALUE path and becomes the PROVENANCE RECORD"*
without silently repurposing a field two consumers already read.

## A.4 Field contract

| Field | Post-repair definition |
|---|---|
| `ending_mv` | **roster `currentValue`** (the ruled basis) |
| `ending_mv_source` | `portfolio-roster-currentValue` \| `roster-ABSENT` — provenance, mirrors `build_billing_dim` |
| `ending_mv_activity` | the raw activity cell **verbatim** (was the old value path; kept so the coverage-not-meaning tie stays derivable) |
| `activity_value_status` | the **PRESERVED** discriminator, computed exactly as today: `ZERO-CONTRADICTED-BY-POSITIONS` / `ZERO-CORROBORATED` / `SOURCE-ABSENT` / `OK` |
| `value_status` | describes the AUTHORITATIVE value: `OK` (roster > 0) · `ZERO-CORROBORATED` (roster 0 **and** positions 0) · `SOURCE-ABSENT` (no roster row) |
| `fair_value` | `ending_mv + accrued_income` — identity **unchanged** |

## A.5 Population pins (pre-registered BEFORE build, committed; corrected 109→111 pre-build)

| Instrument | Population | BEFORE | AFTER | Correct reading |
|---|---|---|---|---|
| C_02 | UNCOMPUTABLE | **423** | **111** | shrink of **312** is the CORRECT adjustment, not a regression |
| B_03 | VARIANCE-EXPLAINED via ZERO-CONTRADICTED | **312** | **0** | class empties because its defect is gone |
| B_03 | NEW unexplained variances | 0 | **0** | all **312/312** freed accounts tie to positions, **max abs delta $0.00** |
| any | SOURCE-ABSENT | unchanged | unchanged | repair creates no activity rows |

## A.6 Acceptance bar

1. Plane total ties served `total.aua` **$209,225,005.59** at the same vintage (delta $0.00).
2. **312/312** positions tie preserved post-repair.
3. **The 111 REMAIN UNCOMPUTABLE** — genuinely-empty accounts must still be refused. Absence
   serves as ABSENT, never as a computable zero. *A repair that makes these computable is a
   REAL regression and fails the bar.*
4. `activity_value_status` + `ending_mv_activity` present; the coverage-not-meaning tie
   re-derivable from the artifact alone.
5. A monetary mutant on a live field FAILS **rc=1 UNPIPED**.
6. Schema-valid **PROOF_OF_SPEC** instance.

## A.7 Scope, risk, sequencing

P1-SCRIPTS emitter, **built in-lane and left UNDEPLOYED** pending normal P-phase sequencing.
**No user-facing change:** the served surface already computes on the roster basis, so the
repair makes an undeployed emitter agree with truth already being served. Consumer impact is
confined to C_02 (computable set grows), B_03 (explained class empties, ties land clean), and
any D-family reader of `B_00`. **INFERRED, not verified:** whether any consumer outside
C_02/B_03/D-family reads `value_status` — I traced the two named consumers at source and did
not enumerate the full reader set.

---

# PART B — FIVE-FIELD LANE REPORT

## B.1 SCOPE

This lane builds and verifies the **canonical-plane emitters and their evidence**, across two
firms. On INF: the P1 runner family (Groups A–D) and then the **billing/fee-earning plane**,
re-homed here when Andrew's ~$8M question exposed a value defect. On 49F: the **serving-overlay
sweep** — seven family keys built shape-frozen against the served census. The through-line is
not "write emitters": it is that **every figure a runner emits carries an instrument that could
have falsified it**, which is why this lane's output is measured in controls and pins as much
as in artifacts.

## B.2 LANDED

**⚠ CTO's scoping of my lane omits the entire 49F overlay sweep — correcting it here, per
your "yours wins."** Your list had: INF A/B/C, the taxonomy amendment, the fee investigation,
the flag act + window fix, the B_00 scope question, and the post-fix fire. All correct. Missing:

**49F serving-overlay sweep — 7 family keys, all CVO-graded:**
- `firm_leaderboard` emitter + V19 bands `fd72adf7d2` · instance `5c9c3b1c0f` · **BAR-CLEARED** `e56275ef45` (CVO planted their own mutant)
- `firm_ownership_map` + cross-emitter slug fix `b790aaca3e` · instance `fe9ffd6f30` · VALIDATED `bf23933fa0`
- `firm_timeseries_overview` + 3 runner_common helpers + V22 `b8f9e0228f` · instance `45672c14ec` · VALIDATED `8922fb4bc0`
- `firm_cumulative_chart` + 2 helpers + V23 `995273755e`, refusal-driven fixes `a2d3815234` · instance `9853de4b84` · VALIDATED `2e36044d7b`
- `timeseries_chart` **TWINS** (2 keys, one emitter) `f19870b150` → rename/renumber `31c386b000` → fixes `35702274cd` · instance `4faf0dd4e2` · **2× VALIDATED** `6f34fb14f1`
- `d07` **window re-arm** + account-grain helper + 5 V2 pins `aa4d970c19` · amended instance `3ced9d2e91`

**Two frame findings I raised, both adopted into the SHARED publisher by base:**
`82ba36381b` (open-key paths — MAP-valued nodes; the freeze frame could not express keys-as-data
and `fee_efficiency` had passed on fixed-key luck) · `79ca4216e5` (hybrid rule for heterogeneous
wide rows; base's mode-element correction caught a defect inside my own proposal).
**Two census gaps I measured, both patched by base:** `2685dd34f1` (run-5: a prefix absent from
the enumeration made a family row structurally impossible) · `76d225de9b` (run-6: the sampler's
size cap had left the estate's **two largest** artifacts unfrozen through five vintages).

**INF fee-earning plane (Andrew instructions #1 and #2), now VERIFIED IN PRODUCTION:**
- lib + D_04 consolidation `7c6043a883` · four reader repoints `9eeecd154d` · window fix and
  flag retirement deployed 08-11 (4 artifacts, all md5-tied)
- **First post-fix scheduled fire, 08-12:** 4/4 structural exact — `ending_mv_source` **908/908**,
  retired column absent, **908/908 populated with ZERO source-absent**, and the load-bearing
  **own tie-out 554/554 TO THE CENT** (coverage changed, meaning did not). 3/3 value in band:
  book **$209,225,005.59**, served fee-earning **$203,216,860.04**, **non-fee-earning $6,008,145.55**
  — against the $60M+ that prompted the investigation and Andrew's own ~$8M expectation.
  Rescued class **354 rows / $68,676,268.78** (pre-fix book $140,717,260.47). Records: pre-registration
  and result committed 08-12; ledger discharge section closed.

**Corrections I filed against myself (both material, both committed):**
- A false-`0/908` read of a raw-text column that looked exactly like a vendor outage — caught
  before reporting, classified as the **designed-domain** retrieval class.
- **A wrong "resolution" I had already reported to Andrew and COO:** I identified a 109-account
  gap as the genuinely-empty class. **The empty class is 111**; 312 + 109 = 421 against a
  denominator of 423. Retracted, both records corrected, the 109 returned to open observation.
  *Caught only because CTO's population-pin requirement forced me to state a partition exactly.*

## B.3 IN FLIGHT

**Nothing executing.** The B_00 repair is specified above and **held pending CTO ratification of
the §A.3 consumer-contract decision** — the population pins are already committed pre-build, so
the moment the semantic is ratified the build is mechanical and gradeable.

## B.4 HELD / GATED

| Item | Held on | Release |
|---|---|---|
| B_00 basis repair | the §A.3 `value_status` semantic (a 2-consumer contract change) | **CTO** |
| The 109-account served-classification gap | re-grounding: **there is no `holdings` dim** in `silver/api_dims/`, so my own earlier "valuation = holdings.market_value" shorthand is unverified | mine, not urgent, nobody blocked |
| 49F serving PORT of all 7 families | sweep sequencing (QA emission only to date) | base DS / COO |
| Cutover re-pin obligations (V19/V22/V23/V27 narrowing; ownership_map cross-derivation id-set parity, raised by CVO to an obligation) | the serving cutover act | base DS task #17 |

## B.5 BLIND SPOTS + NEXT

**Not captured anywhere yet:**
- **INFERRED:** the `value_status` reader set beyond C_02/B_03/D-family is unenumerated (§A.7).
- **INFERRED:** the served/silver equality at `$209,225,005.59` almost certainly holds because
  both planes now resolve to roster currentValue — I have **not** traced D_04's valuation plane
  to source, and the same untraced shorthand is what produced the 109 error. Treating it as
  proven would be the identical mistake twice.
- **MEASURED, uncarded:** the three 49F census-instrument gaps behind base's targeted patches
  (size cap, non-dict-schema loudness, the two keys-as-data vocabularies) are banked for the
  d00 touch but nothing schedules that touch.
- **A naming hazard, routed to CVO by COO as doctrine:** `DIVERGE-SOVEREIGN` is a **verdict
  state** in the overlay vocabulary, so it names a CLASS, not an item — it will collide again,
  and the collision is invisible from the term itself.

**NEXT (1–3):** (1) build the B_00 repair on CTO's ratification, graded against the committed
pins; (2) trace D_04's valuation plane to source — it closes the 109 *and* converts the
served/silver equality from INFERRED to grounded, one read for two open items; (3) available
for 49F port sequencing on base's word.
