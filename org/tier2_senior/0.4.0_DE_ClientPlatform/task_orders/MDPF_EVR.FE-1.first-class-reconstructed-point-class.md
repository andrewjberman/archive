# TO MDPF_EVR.FE-1 — FE first-classing of the `reconstructed` point_class (no urgency; honest degrade holds today)

<task_order id="MDPF_EVR.FE-1" project="MDPF_EVR">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:5xZ</issued>
<status>pending — event-driven at next DE spawn; NO urgency (the loud-degrade path is honest-by-design today)</status>
<priority>P3 backlog — routed per CTO instruction via CRO 174745Z</priority>
</task_order>

## Context

The eclipse-vintage-reconstruction emitter (EVR, Andrew-direct employ 2026-08-14) added
`point_class: "reconstructed"` to the served MDPF provenance lattice (inflection: {438 measured,
7 reconstructed}, CTO-verified). The portal FE (`portal/src/lib/pairedProvenanceRead.ts` — closed
3-enum + loud-degrade law) currently renders `reconstructed` (and `carried`) as estimate-class
with a console warn: honest, but not first-class.

## Objective

First-class `reconstructed` in the FE per the register-rowed precedent for `carried`: extend the
closed enum (type), add the legend entry, and the styling treatment — so a reconstructed point is
visually distinct and self-describing rather than riding the degrade path. Follow the `carried`
implementation as the pattern; comp-transform schema-check + ternary-audit per Rule 20 before
commit. Portal tree stays on DEV (Rule 19).

## Acceptance

The 7 inflection reconstructed points render first-class (distinct legend + styling, no console
warn); `carried` behavior unchanged; the closed-enum law preserved (no open string unions).

<proof_of_spec>
<expected_criteria>reconstructed-first-classed-type-legend-styling; carried-precedent-followed; no-console-warn-on-reconstructed; closed-enum-preserved; schema-check-and-ternary-audit-run</expected_criteria>
<instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/MDPF_EVR/proof_FE-1.json</instance_path>
</proof_of_spec>
