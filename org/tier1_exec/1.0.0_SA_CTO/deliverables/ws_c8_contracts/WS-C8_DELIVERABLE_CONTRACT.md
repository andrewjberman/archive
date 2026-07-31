# WS-C8 DELIVERABLE CONTRACT: THE DOCTRINE COLLAPSE

**Workstream:** NFRA_VELOCITY / CORE, WS-C8 -- parallel from P1.
**Build:** `0.8.0_AE_CloudComp~C`. **Gate:** `1.0.0_SA_CTO~Z`. **Verify:** `3.0.0_SA_CVO~Z`.
**Status: NOT COMPLETE.** Two of four acceptance clauses met; see below.

## AUTHORITATIVE vs DERIVED

**SOURCE OF RECORD for the laws: `docs/doctrine/MECHANISM_LAWS.md` and
`docs/doctrine/CONTROLS_OVER_CARE.md`. DOCTRINE STAYS IN `docs/doctrine/` AND DOES NOT MOVE INTO A
DELIVERABLES FOLDER.** This contract RECORDS them; it does not contain them.
**Staged, not yet collapsed:** `../WS-C8_STAGING_LAWS_DERIVED_20260731.md` -- sixteen control-design
laws. **Where this contract and an artifact disagree, the artifact wins.**

## WHAT WS-C8 WAS OBLIGED TO PRODUCE, AND WHERE EACH PIECE LIVES

| Obligation | Artifact | Vintage |
|---|---|---|
| The 14 M-laws as a doctrine head | `docs/doctrine/MECHANISM_LAWS.md` | `@e16ea3bda` |
| The dedup pass (L-2/L-5/L-11 as instance rows) | same, artifact 2 | `@fbfe5533b` |
| Reciprocal doctrine boundary (DC-4) | `docs/doctrine/CONTROLS_OVER_CARE.md` III | `@913e3365d` |
| M15 adjudication | `../WS-C8_M15_ADJUDICATION_20260731.md` | landed |
| The staged control-design laws | `../WS-C8_STAGING_LAWS_DERIVED_20260731.md` | landed |

## ACCEPTANCE, CLAUSE BY CLAUSE

| # | Clause | Status |
|---|---|---|
| 1 | **RECONCILIATION POINTS FALL**; byte-count reported, never gated | **NOT MET** -- criterion replaced `@21b3c6e11`; no enumerator exists |
| 2 | Every M-law carries a gate/test or an explicit "no gate possible + why" | **MET** -- verified mechanically, 1 explicit NO-GATE, zero blank cells |
| 3 | The collapse's diff shows zero lost instances | **MET for artifact 2**; the collapse proper has not run |
| 4 | The M15 candidate adjudicated | **ADJUDICATED ADMISSIBLE, NOT CLOSED** -- see below |

### Clause 1 -- the criterion was INVERTED and is replaced

**"Doctrine byte-count falls" penalised the correct operation.** Artifact 1 added 15540 B; **artifact
2 -- the DEDUP PASS, whose entire purpose is removing duplication -- added 3910 B**, because a merged
row carries provenance, a pinned citation and reasoning, and that costs more than the law it
replaced. Proposed by `2.1.0_SA_COO` (who owns the defect and said so), **refined by the gate owner:
their draft scoped pairs to CROSS-document; struck, because that is satisfiable by CONCATENATION.**

**DC-4 is the first measured reduction under the new criterion, and honestly so:**
`MECHANISM_LAWS` pointed at `CONTROLS_OVER_CARE` **8 times**; the reverse **zero** (positive control
"instrument" x28). **A one-directional pointer IS a reconciliation point.** The fix BOUNDS the pair
rather than merging it, and removed no duplication.

**OPEN AND OWED BY THE GATE OWNER: there is no ENUMERATOR for reconciliation points.**
`0.8.0_AE_CloudComp~C` raised it and it is the sharpest objection to the ruling: **a criterion that
measures the right quantity but cannot be counted is a gate that cannot fail -- which is exactly what
the old one was replaced for.** It is a PRECONDITION of artifact 3, not a detail of it.

### Clause 4 -- admissible, and blocked by a gate

**M15 (DIVERGENT-TRANSPORT CONTROL) is ADMISSIBLE ON MERIT:** two fresh instances on 2026-07-31, from
two seats, neither self-caught, **neither matching any of the three MSYS shapes CLAUDE.md documents.**

**IT CANNOT BE CLOSED.** The PRD says M15 *"enters the schema through the WS-C9 gate"* -- and
**Andrew's pause SEALS C9.** Rejection is unavailable on the merits. **Rejecting a law that produced
two instances today, in order to close C8, would be adjudicating from the desired outcome, and "we
needed C8 to close" is not a reason on record -- it is the absence of one.**

## THE STRUCTURAL FINDING, RECORDED BECAUSE IT IS AN INTEGRATION POINT

**THE OPERATION THIS WORKSTREAM IS NAMED FOR CANNOT BE PERFORMED.** Collapsing
`CONTROLS_OVER_CARE` III into the M-classes is **impossible** -- the M-taxonomy types
assertion-POSITION and III types instrument-FALLIBILITY (WS-C2 step 0). C8 is finishable only by its
**secondary** mechanism. **And ~10 of the 16 staged laws sit outside the M-taxonomy for the same
reason, with three of them (L-7/L-8/L-9 -- how a RULE or ROLE fails to be one) in a family that has
NO HOME.** Named on both doctrine files; creating its home is unauthorised and deliberately unrushed.
