# TO MDPF_TRGALN.TO-5 — atom_decomp truth-pass on Inflection stacked-bar holes

<task_order id="MDPF_TRGALN.TO-5" project="MDPF_TRGALN">
<issued_to>4.0.0_SA_CRO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:20Z (filed on MSTR spawn-confirm 051811Z; drafted @c11d233)</issued>
<status>complete</status> <!-- 2026-08-14T05:55Z 4.0.0_SA_CRO: truth table + proof @98dbaf099a; COO validation per RAVC4 pending -->
<priority>P0 — STAGED. GO comes ONLY from COO when the §8.2 gate reads true (TO-0..TO-3 applied +
proofed; expected ~06:15Z). Pre-reading the PRD and surfaces before GO is welcome; no mutations and
no findings-driven dispatches before GO. Completes TONIGHT. Andrew's explicit method call:
atom_decomp on ALL relevant surfaces BEFORE any fix is pursued.</priority>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_TRGALN TO-0..TO-3 applied + proofed (§8.2 gate) — COO signals GO" status="pending"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md v1.2 @cebdae6cd8 — §8 verbatim + §8.2 measured localization, §7 proof schema, §9 recorded rulings</ref>
  <ref type="context">TO-6 (surgical backfill, staged at AE-as-container, executor named off YOUR truth table) consumes this TO's deliverable; roll-forward is fallback-only on Andrew's explicit word</ref>
</references>

## SCOPE (PRD §8.2)

atom_decomp truth-pass across the full surface chain: served
`platinum/mdpf/inflection/aggregate-aua-timeseries.json` → gold slice
(`portal/gold/mdpf/inflection/`) → builder (`dim_mdpf_aggregate_aua_timeseries.build_inflection_artifact`
+ carry-forward union logic) → monolith inputs (`orion/inflection/silver/fact_assets`,
`eclipse/inflection/silver/*`) → vendor rawest available.

**Measured starting facts (v1.1, 05:0xZ, 443 served dates 2024-11-01→2026-08-11):**
- 7 FULLY-EMPTY dates (model AND non_model null): 2026-05-20, 05-29, 06-30, 07-10, 07-13, 07-14,
  08-05 — the "did not used to be here" regression class.
- 390/443 dates model_aua sum == 0 (gray-only bars); first nonzero model date 2026-05-15.
- Which zero dates are TRUE history (model program ramp) vs MISSING is exactly what this pass
  adjudicates — assume NEITHER way.
- 2026-08-05 is also the platinum-cutover carry-forward date — correlation TESTED, not assumed.

**Timing context (matters for your reads):** TO-1/2/3 retimes land ~05:45–06:15Z and the TO-3
tonight-refresh exercise re-publishes the served series with as-of 2026-08-13 BEFORE session end —
so pin the vintage of every artifact you read (a read taken pre-refresh and one taken post-refresh
are different documents; date both).

## DELIVERABLE

Per-date truth table for every hollow/empty date:
`TRUE-ZERO | MISSING-AT-SURFACE-X | REGRESSION-INTRODUCED-AT-COMMIT/CUTOVER-Y`,
with the MECHANISM of the 7 fully-empty dates named (grounded per Rule 22 — source/graph citation
with vintage, not inference). Proof artifact per PRD §7 at
`org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-5.json` (claims = per-date
truth entries) — one proof home per project regardless of executing seat.

<acceptance_criteria>
1. Every hollow/empty date carries exactly one truth verdict with surface-level grounding.
2. The 7 fully-empty dates' mechanism named and source-cited (file:line @ commit or live read).
3. 08-05/cutover correlation tested and reported either way.
4. No fixes applied in this TO — truth only; fixes are TO-6's (executor named off your table).
5. Artifact reads carry their read-time vintage (pre- vs post-tonight-refresh).
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>per-date-truth-verdicts, empty7-mechanism-cited, cutover-correlation-tested, no-fixes-applied, vintage-pinned-reads</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-5.json</instance_path>
</proof_of_spec>
</task_order>
