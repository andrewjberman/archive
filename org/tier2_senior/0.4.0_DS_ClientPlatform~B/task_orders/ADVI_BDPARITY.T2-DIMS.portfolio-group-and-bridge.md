# TO ADVI_BDPARITY.T2-DIMS — dim_portfolio_group + bridge_group_account (LAPTOP; BUILD-ONLY)

<task_order id="ADVI_BDPARITY.T2-DIMS" project="ADVI_BDPARITY">
<issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:05Z</issued>
<dated>when staffed -- staged now</dated>
<status>staged -- **BUILD-ONLY**. Served consumption GATED on the §9-Q3 book-definition word (CVO P2-1).</status>
<priority>P2</priority>
<authority>D2_ADVI_49F_E2E_PRD.md §4b + §6 row 6 at dispatch vintage @c379cb6521. Placement: LAPTOP (Andrew-direct: "D2 is certainly laptop fabric").</authority>
</task_order>

## Objective
Build `dim_portfolio_group` + `bridge_group_account` from the daily allocation export, keyed on the
**Primary-group partition key.**

## THE PRIMARY-KEY DISCIPLINE IS THE WHOLE POINT
Acceptance requires that **ZERO CROSS-GROUP SUMS ARE EXPRESSIBLE IN CONSUMERS.** Not "are avoided"
— **not expressible.** An account that can be summed into two groups is the same double-count class
that D3's overlap invariant exists to prevent and that cot BD's relationship-grain already produces
if collapsed naively. Make the shape prevent it rather than relying on every future consumer to
remember.

## Downstream awareness
This artifact is consumed CROSS-PRD: D3's TO-D3.4 gates partly on the D2-threaded
`dim_portfolio_group`/`bridge_group_account` for the advisor slice. It is built here and consumed
there — one home, one producer.

## Acceptance criteria
- **T2-1 DIMS LAND IN THE 49financial GOLD GRAMMAR** (Rule 17b: gold is parquet,
  `{table}/date={D}/`).
- **T2-2 BRIDGE COVERS THE EXPORT'S FULL MEMBERSHIP** — denominator printed (members in the export
  vs members in the bridge).
- **T2-3 ZERO CROSS-GROUP SUMS EXPRESSIBLE** — demonstrate the primary-key discipline structurally,
  not by inspection.
- **T2-4 NO SERVED CONSUMPTION** while the build-only fence stands.
- **T2-5 proof instance VALID rc=0 positional: ids T2-1..T2-5.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>T2-1,T2-2,T2-3,T2-4,T2-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~B/deliverables/ADVI_BDPARITY.T2-DIMS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at built, cc DE (D3 TO-D3.4 consumes this) and CTO. Session log w/ Compiler Tools section.
