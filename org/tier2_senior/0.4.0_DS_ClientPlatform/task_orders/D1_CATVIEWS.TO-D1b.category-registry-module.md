# TO D1_CATVIEWS.TO-D1b — the MDPF category registry module (LAPTOP; GATE-CLEARED, chain head)

<task_order id="D1_CATVIEWS.TO-D1b" project="MDPF_CATVIEWS">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:35Z</issued>
<dated>first substantive row at your THU-AM spawn, behind your R-WATCH/PB-1 Friday-path duties</dated>
<status>pending -- BUILT @be05d938af. D1b-1..D1b-4 measured PASS (existence check controlled; 6 F5 raise-paths exercised with 4 positive controls; Q1-closed shape, data-driven property measured). D1b-5 blocked on the SAME artifact-coverage heuristic as WP-1 -- now characterised, routed to COO/CTO. Deploy leg deliberately NOT run (rides TO-D1c). Terminal status left to COO.</status>
<priority>P1-program; behind the 49F Friday path at the seat</priority>
<authority>D1_ASSET_CATEGORY_VIEWS_PRD.md §4.1 + §6 item 2, at dispatch vintage @3e589fa1eb (CVO verdict @d476339293 absorbed + THE TAXONOMY GATE RULED -- D1_TAXONOMY_GATE_RULING_20260819.md). Placement: LAPTOP by the EITHER-defaults-laptop rule (Andrew-direct ~19:3xZ leaves the residual placement axis to CTO; this row is EITHER, so the default governs).</authority>
</task_order>

## Objective
Build the category registry module per §4.1 — the single ratified vocabulary the whole D1 chain
(projection, portal, D4's flip) reads from. The taxonomy gate is RULED, so you are implementing a
settled composition table, not proposing one: §3's table + the Rule-24 declaration are the contract.

## Mandate (three-phase, standard)
- **Phase 1 (before you write):** the §6 existence check —
  `git log -- data/mdpf/scripts/gold/mdpf_category_registry.py` (expect NO commits; if commits
  exist, STOP and report — the PRD's existence claim is then falsified and the build shape changes).
  Read the crosswalk. `comp-pipescript io <crosswalk consumer> --pipeline mdpf` (the `--pipeline`
  flag is REQUIRED — flagless is rc=2 refused).
- **Phase 2:** `py_compile` + `.tools/commit-gate.sh`. Rule 15 binds: the file opens with
  `from __future__ import annotations`.
- **Phase 3:** import-and-enumerate self-test.

## Acceptance criteria
- **D1b-1 EXISTENCE CHECK RUN + REPORTED** with its denominator, not asserted from the PRD.
- **D1b-2 REGISTRY IMPORTS** and every view node in §3's ruled composition table resolves.
- **D1b-3 F5 BEHAVIORS EXERCISED — both limbs, each printed:** a duplicate registration RAISES and
  an unknown-node lookup RAISES. An unexercised raise-path is not evidence; make each one fail on
  demand and show the failure.
- **D1b-4 D4's ETF SET REPRESENTABLE.** Q1 (four-vs-two: DIVZ/IDVZ/PFDE/PFOE vs the ratified
  `divz|idvz|pfoe|muni|tax` enum) is **AT ANDREW AND NON-BLOCKING** — build to the PRD's proposed
  answer (register all four as SMA-view members, `strategy_id` set only where a real SMA strategy
  exists today: divz, pfoe; idvz/pfde as ETF-product members pending strategy registration) and
  make the member set **data-driven, so a change to Q1's answer is a registry edit and not a code
  edit.** State in your report which shape you built.
- **D1b-5 proof instance VALID rc=0 positional: ids D1b-1..D1b-5.** Expected values cite only
  MEASURED/RULED-class run rows per the protocol's run-verdict vocabulary — an expected value
  resting on an INFERRED-class row is mechanically ineligible and the instance is rejected.

<proof_of_spec>
  <expected_criteria>D1b-1,D1b-2,D1b-3,D1b-4,D1b-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-D1b_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not re-open the taxonomy. The gate is ruled; a composition disagreement is a SURPRISE-CHANNEL
  line to COO, not a unilateral edit.
- Do not deploy in this TO — the deploy leg rides TO-D1c's gold cycle.

## Reporting
COO at existence-check-run and at acceptance. Distinguish success from SILENT FALLBACK explicitly
in the report (CVO named three healthy-looking-failure acceptances in one night; returned work is
held to that line). Surprise channel: one banked line to COO, take no action, keep working.
Session log with a Compiler Tools section = deliverable.

---
## ⚖ Q1 ANSWERED — 2026-08-19 ~20:12Z (Andrew; records @1e0ec3b079 + @3c8c3f1035)
**ALL FOUR ETFs (DIVZ / IDVZ / PFDE / PFOE) are SMA-view members**, with `strategy_id` set **ONLY**
where a real SMA strategy exists today (**divz, pfoe**); **idvz and pfde register as ETF-product
members pending strategy registration.** This is exactly the PRD's proposed shape, so acceptance
criterion D1b-4 is unchanged — but Q1 is now CLOSED, not pending. Keep the member set data-driven
anyway: that property is what made this answer cheap, and it stays cheap for the next change.
