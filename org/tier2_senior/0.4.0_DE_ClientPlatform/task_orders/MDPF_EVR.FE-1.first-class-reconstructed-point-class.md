# TO MDPF_EVR.FE-1 — FE first-classing of the `reconstructed` point_class (no urgency; honest degrade holds today)

<task_order id="MDPF_EVR.FE-1" project="MDPF_EVR">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:5xZ</issued>
<status>cancelled</status>
<cancelled_at>2026-08-15T18:25:00Z</cancelled_at>
<cancelled_by>2.0.0_SA_COO (issuer)</cancelled_by>
<cancellation_ruling>Andrew-direct at the MSTR terminal 2026-08-15 ~0350Z, VERBATIM: "i dont want to draw attention to the interpolated points at all, no one cares about that, its more problematic to open up the can of worms and seed doubt rather than just another data point that is probably within 10bps anyway on a random day no one cares about". Record: org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20260815_NO_FIRST_CLASSING_RECONSTRUCTED_POINTS.md (MSTR broadcast 20260815T181807Z). Status is CANCELLED (the need went away by ruling), NOT superseded (nothing met it another way). SCOPE OF THE RULING, narrow: FE presentation only -- the EVR emitter + outputs (Andrew "yes to both" @e4251a4567), the server-side point_class lattice, and the ratified EVR honesty conditions are UNTOUCHED. Open question MSTR surfaced to Andrew and did NOT adjudicate: whether today's estimate-class + console-warn rendering should itself be softened -- collides with the ratified `reconstructed-never-measured` honesty condition; his to resolve; NO work pends on it. The carried "DE FE-1 spawn-or-defer-date" item is DISCHARGED (no spawn, no date, not an 08-16 item).</cancellation_ruling>
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
