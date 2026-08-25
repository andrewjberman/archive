<task_order>
<id>MDPF_3FIRMS.3F-BF1</id>
<title>Cottonwood interpolated-backfill PRODUCER — the interpolator + point_class[] + two-lock absence floor, mutant-gated before serve</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-BF (Interpolated Backfill) — build, DS lane</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<advisory>4.0.0_SA_CRO (owns the interpolation design / the canonical schema @708661904)</advisory>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-23T03:52Z</issued_at>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_3FIRMS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>ANDREW-DIRECT "I need both right now immediately" -> CTO 035119Z -> decompose + GO NOW.</priority>

<authorization>
Andrew-direct 022726Z (interpolated backfill) + "Ok i need both right now immediately" 0351Z -> CTO
acceleration 035119Z -> COO decomposition. CVO decomposition-clearance @816d48cc9 (pinned pair signed).
</authorization>

<references>
  <ref type="spec-schema-SOURCE-OF-TRUTH">CRO interpolation delta @708661904 — THE CANONICAL BUILD SCHEMA</ref>
  <ref type="spec-aggregation">CTO aggregation v0.3 @be91775dd — aggregation design. ⚠ its §4 schema block is RULING-RECORD-NOT-BUILD-SURFACE; do NOT copy it.</ref>
  <ref type="cvo">3.0.0_SA_CVO sign-off @816d48cc9 (R-5: pin binds these EXACT commits; a spec change re-enters review)</ref>
  <ref type="andrew">org/tier1_exec/2.0.0_SA_COO/andrew_direct_20260723T0215Z_canonical_names_colors_and_interpolated_backfill.md</ref>
</references>

<scope>
Build the Cottonwood interpolated-backfill PRODUCER: reconstruct an APPROXIMATE historical model-level
series for the pre-overlap period, from current-day accounts tracked backward via inflows + fuzzy match,
per CRO's design. **It is an ESTIMATE, conspicuously labeled, served-layer only — NEVER measured data.**

⚠ **SCHEMA SOURCE OF TRUTH = CRO's @708661904, verbatim. Do NOT copy CTO's v0.3 §4 block** (it is
RULING-RECORD-NOT-BUILD-SURFACE; delta-wins-on-disagreement; a disagreement is an R-5 review item, not a
local decision). One schema, one source, never two blocks kept identical by hand.

**DELIVERABLES:**
1. The interpolator producer emitting the approximate series per @708661904.
2. **The additive `point_class[]` array in the served slice** (non-breaking) — every point carries its
   class (measured | interpolated) so provenance rides the value and cannot be lost between data and render.
3. **The TWO-LOCK ABSENCE VALIDATOR** — floor = `max(model_creation_date, account_first_existence_date)`;
   the PRODUCER refuses to emit an interpolated point below the floor AND a standalone VALIDATOR refuses
   it independently. Both locks, machine-checked. "Work it out backwards" is bounded by when the models
   and accounts actually existed — you cannot interpolate a value for a date before its subject existed.
</scope>

<binding_laws priority="NON-NEGOTIABLE EVEN AT SPEED — Andrew overrides WAITING, never CHECKS">
⛔ **CVO's MUTANT SET RUNS BEFORE ANYTHING SERVES. The planted-point test + the both-enum-strings test are
NON-NEGOTIABLE.** Speed comes from not waiting, NOT from skipping a mutant test. A producer that serves
before its mutant set is green is out of scope regardless of the deadline.
⛔ **NEVER WRITTEN TO BRONZE/SILVER AS IF MEASURED.** The interpolated series is a served-layer overlay
ONLY. Bronze is raw (17a); silver is measured (17). An interpolated value in either layer is the
fabrication class — the exact thing the `point_class[]` + labeling design exists to prevent.
⛔ **APPROXIMATE + CONSPICUOUSLY LABELED, NEVER PRESENTED AS EXACT.** Andrew: "doesn't need to be exact."
The reconciliation with the MEASURED fingerprint-ban (cosine 0.62-0.98, a past date's strategy not
recoverable from holdings alone) IS the honest labeling — an estimate marked as an estimate is not
fabrication; an estimate presented as real is.
⛔ **THE TWO-LOCK FLOOR IS EXERCISED, not prose** — the acceptance below runs a below-floor input and
confirms BOTH the producer and the validator refuse it.
⛔ **R-5:** this TO binds @708661904 + @be91775dd EXACTLY. If either spec changes, it re-enters CVO
review before it binds — do NOT accept an amended spec as a free change.
</binding_laws>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read CRO's @708661904 schema in full; confirm the point_class enum + the floor inputs are as specified</run>
      <expect>Schema internalized from the SOURCE (not CTO's §4); point_class enum values named; floor = max(model_creation, account_first_existence).</expect>
      <if_mismatch>If @708661904 is ambiguous, MCP CRO — do NOT fill the gap from CTO's §4 block or from inference.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>py_compile + ds-precommit-check + ruff clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP.</if_mismatch>
    </step>
    <step>
      <run>CVO MUTANT SET: the planted-point test + the both-enum-strings test</run>
      <expect>BOTH green. A planted interpolated point is caught; the enum-string handling is correct on both values.</expect>
      <if_mismatch>⛔ HARD STOP. Nothing serves until the mutant set is green. This is non-negotiable at any speed.</if_mismatch>
    </step>
    <step>
      <run>TWO-LOCK FLOOR EXERCISE: feed a below-floor date; confirm producer refuses AND validator refuses</run>
      <expect>Both locks fire independently. A below-floor interpolated point cannot be emitted or can pass the validator.</expect>
      <if_mismatch>⛔ A single-lock pass is a fail — the floor is two independent refusals by design.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Verify the served slice carries point_class[] with correct measured|interpolated labels; NO bronze/silver write occurred</run>
      <expect>point_class[] present + correct; bronze + silver untouched (ETag check on the relevant partitions).</expect>
      <if_mismatch>⛔ ANY bronze/silver write is a fabrication-class violation — STOP and escalate.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Served-layer overlay only. NO write to bronze or silver. The interpolated series is
  a gold/served artifact carrying point_class[]; measured partitions are untouched.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="served slice + point_class[]" shared_with="0.4.0_DE (3F-BF2)">
    DE's FE accessor reads point_class alongside value. Your point_class[] contract IS DE's read contract —
    circulate the exact shape so his paired-read accessor and your emit agree.
  </resource>
  <resource path="canonical schema @708661904" shared_with="4.0.0_SA_CRO">
    CRO owns the design. Consult; do not re-derive. R-5 on any change.
  </resource>
</cross_domain_coordination>

<dependencies><dependency type="spec" name="pinned pair @708661904 + @be91775dd (CVO-signed)" status="signed"/></dependencies>

<acceptance_criteria>
1. Interpolator producer emits the approximate series per @708661904 (schema from the SOURCE, not CTO §4).
2. `point_class[]` additive array in the served slice, non-breaking, correct measured|interpolated labels.
3. **CVO mutant set (planted-point + both-enum-strings) GREEN — exercised, before any serve.**
4. **Two-lock absence floor EXERCISED** — a below-floor input refused by BOTH producer and validator.
5. **ZERO bronze/silver write** (ETag-verified untouched) — served-layer overlay only.
6. Interpolated points are conspicuously classed for DE's render; never emitted as exact/measured.
7. Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail.
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO. Escalate immediately if: the mutant set cannot be made green (do NOT serve
without it), a below-floor point passes either lock, or any interpolated value reaches bronze/silver.
</escalation>
</task_order>
