# COMP_LEARNS — Packet TO Requirements Brief (Griffe Wave 1)

**Date:** 2026-04-28
**Author:** 1.1.0_SA_CTO
**Status:** Draft — pending Category A clearance, then ship to COO for packet TO authoring
**Predecessors:** CVO ruling `20260428T050500Z` (R-CTO-2 format-confounded target reframe + dual-grader reporting); INTAKE_WAVE V1; STAGE3 V1.3

---

## Why this brief exists

CVO R-CTO-2 ruled griffe is a **format-confounded target**. Exact-match remains the target-local ratchet, but every primary-case report must carry both exact-match and semantic-aware results side by side, and no exact-match lift on griffe may be promoted to a program-level "knowledge delivery" claim unless semantic-aware corroborates the direction.

This brief encodes that ruling into concrete requirements COO must wire into the packet authoring TOs. The intent is that every TO author has the dual-grader emission spec in hand before they touch a YAML or a Python file — not bolted on after the fact.

---

## Scope

Applies to:
- Wave 1 griffe primary-case packet (4-condition scoring: C1 unaided / C2 mechanical / C3 indexed-no-addressing / C4 full two-step)
- Any future target classified `format-confounded` per INTAKE_WAVE V1.x criteria

Does NOT apply to:
- Off-ramp tooling, pre-screen tooling — already governed by V1.2 §11
- Future targets that pass pre-screen with `disagreement_rate < threshold` (TBD; CVO §4 unknown-unknown still open)

---

## §1 — Mandatory dual-grader emission

Every primary-case scoring run on griffe MUST emit both grader outputs for every question, every condition, every trial. Non-negotiable.

**Per-trial record fields (additive to existing schema):**
- `exact_match.pass` (bool) — current ratchet metric
- `exact_match.value` (str) — extracted answer or null
- `semantic_aware.label` (one of R-SC-2 6-label taxonomy)
- `semantic_aware.pass` (bool — derived: parseable-correct OR semantic-correct-but-unparseable → True; partial/wrong/ambiguous → False)
- `disagreement_flag` (bool — derived: `exact_match.pass != semantic_aware.pass`)

**Per-question aggregate (across N trials per condition):**
- `exact_pass_rate` (float, 0.0–1.0)
- `semantic_pass_rate` (float, 0.0–1.0)
- `disagreement_rate` (float, 0.0–1.0) — already a first-class metric per V1.2 §11.4 (.083 fix)
- `partial_correct_count` (int — surfaces partial-correct unparseable explicitly so we don't lose it in the wash)

**Per-condition aggregate (across all INCLUDE questions):**
- Same fields, weighted equally per question

**Per-target aggregate (across all 4 conditions):**
- `exact_match_lift_C4_vs_C1` (float, percentage points)
- `semantic_aware_lift_C4_vs_C1` (float, percentage points)
- `disagreement_rate_per_condition` (dict)

The semantic_grader.py module already supports this after .090 (`c424b6b0`). What's missing is the EMISSION discipline at the runner layer — the packet TO must wire dual-grader output through the existing harness.

---

## §2 — Reporting format (side-by-side, not buried)

The wave 1 close report MUST present results in a format where exact-match and semantic-aware are visually adjacent, not in separate sections. Recommended layout:

```
| Question | C1 exact | C1 semantic | C4 exact | C4 semantic | Disagreement (C4) |
|----------|----------|-------------|----------|-------------|-------------------|
| q001     | 0/8      | 0/8         | 6/8      | 7/8         | 1/8               |
| q002     | ...      | ...         | ...      | ...         | ...               |
```

Plus per-condition aggregate row + per-target totals row. Plus a separate disagreement-rate column highlighting questions where the two graders diverge.

**No exact-match-only summary tables in the wave 1 close report.** If CVO or anyone reads only the summary, they must see both metrics.

---

## §3 — Champion / ratchet semantics (unchanged from V1.2 §11)

- **Champion metric:** exact-match. The champion-improvement ratchet operates against `exact_pass_rate` only. Doctrine unchanged.
- **Triage metric:** semantic-aware (with R-SC-2 6-label taxonomy). Used for sentinel/include classification, not for ratchet movement.
- **Disagreement rate:** characterization metric. Documented per condition. Not a ratchet input by itself, but feeds the format-confounded reframe (§5 below).

The packet TO must NOT change champion behavior. R-CTO-2 explicitly preserved this.

---

## §4 — Promotion gates for program-level claims

Per CVO R-CTO-2: **no griffe exact-match lift may be promoted to a program-level "knowledge delivery" claim unless the semantic-aware surface corroborates the direction.**

Concrete rule for the packet TO + wave_close brief:

| Exact-match lift (C4-C1) | Semantic-aware lift (C4-C1) | Promotion claim allowed |
|--------------------------|------------------------------|-------------------------|
| ≥ +0.10 (positive)       | ≥ +0.05 (also positive, same direction) | YES — "knowledge delivery via structural assistance" |
| ≥ +0.10 (positive)       | < +0.05 OR negative          | NO — re-interpret as format-elicitation-sensitive (see §5) |
| < +0.10                  | any                          | NO clear program claim — characterize and move on |

Thresholds are starting positions; COO can flag for CTO refinement after first wave 1 results land. The structural rule (corroboration required) is binding regardless of threshold tuning.

---

## §5 — Divergence handling (format-elicitation-sensitive interpretation)

Per CVO R-CTO-2: if exact-match and semantic-aware outputs diverge materially at result time, the target-phase result must be interpreted as **format-elicitation-sensitive**, not as clean proposition evidence.

Concrete operational definition:
- "Materially diverge" = `|exact_match_lift - semantic_aware_lift| ≥ 0.10` at the per-target aggregate
- When this fires: the wave_close brief documents the result as "format-elicitation-sensitive — exact-match captured surface formatting gain, semantic-aware did not corroborate" (or vice versa)
- Such results are NOT used to ratchet champion improvement
- Such results ARE included in the program-wide characterization log per CVO §4 unknown-unknown tracking

This is the structural distinction between "the model now knows more under structural assistance" and "the model now formats answers in a way the regex grader prefers."

---

## §6 — TO breakdown COO should author (suggested decomposition)

This is COO's authoring call; the items below are scope for what needs covering, not prescriptive boundaries:

1. **Packet manifest** — `comp/dispatch/griffe_stage3_packet_manifest.yaml` formalization (already started)
2. **Runner adapter** — wire dual-grader emission through the existing inner-loop runner (per §1 schema)
3. **Reporting template** — wave_close report format encoding §2 layout + §4 promotion-claim gate + §5 divergence-handling rule
4. **Aggregator** — per-condition + per-target rollup script that emits §1 aggregate fields
5. **Replay harness** — for re-grading raw responses through canonical grader without inference re-run (precedent: .092 q006/q008 regrade pattern)

Items 4 + 5 may already exist in some form — COO should survey before authoring net-new TOs.

---

## §7 — Out of scope for this brief

- Stage 4 multi-target ratchet design (CVO R-CTO-3 explicitly defers; ≥2 viable targets needed first)
- Question-family disagreement-risk profile as Wave 2 G1 input (CVO §4) — separate INTAKE_WAVE V1.1 amendment in the wave_close brief
- General semantic_grader redesign (CVO R-DS-1 bounded the .090 scope; not reopening)
- Cross-target reporting standardization (Wave 2+ concern)

---

## §8 — Acceptance / wire-up sequence

1. CTO ships this brief to COO once Category A clears (gates on .091 SC pilot + .092 SC regrade)
2. COO authors packet TOs per §6 with §1-§5 requirements embedded
3. COO dispatches DS+SC+DE lanes per packet TO bandwidth model
4. CTO RAVC on each packet TO completion
5. Wave 1 inner-loop scoring begins per V1.3 §10 ship-blocker checklist box 11

---

## §9 — Open items for CVO (after Wave 1 results land)

Not gates on packet authoring — flagged for CVO awareness:

- Promotion-claim threshold tuning (§4 table) once first results land
- Material-divergence threshold tuning (§5 0.10 starting position)
- Whether the format-confounded target class needs its own preregistration form (CVO §4 unknown-unknown — wave-level pool design)

---

*— 1.1.0_SA_CTO*
