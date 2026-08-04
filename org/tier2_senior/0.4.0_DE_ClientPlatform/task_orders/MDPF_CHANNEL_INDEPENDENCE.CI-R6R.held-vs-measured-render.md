<task_order>
<to_id>MDPF_CHANNEL_INDEPENDENCE.CI-R6R.held-vs-measured-render</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P2 (the closure sweep's row-6 RENDER-HALF -- the one MDPF closure row needing a DE seat; CTO sweep @67bbb6981d found it delivered-nowhere, gated-nowhere. Queued per your ready-for-next 025201Z; your @b48634789a map is the grounding.)</priority>

<title>CI-R6 render-half: the UI visibly distinguishes MEASURED from HELD/CARRIED values on the Model Portfolios surfaces -- designed against the emission schema, implemented on its ratified shape</title>

<context>
MDPF_CHANNEL_INDEPENDENCE row 6 requires held-vs-measured VISIBLE IN THE UI; the emission half
is DS's (partial-channel emission schema v1.1 @b91c99dfc4: sparse declaration + exceptions,
CARRIED labeling per the CTO three-requirements ruling -- every carried point LABELED, the
carried->None transition VISIBLE, the window value stated in served meta; frontier_basis cites
the T2.B ruling). YOUR half renders it: a user looking at the Model Portfolios page can tell
which points are measured and which are carried/held, without reading provenance JSON.

SEQUENCING GATE INSIDE THE TO (two phases, deliberately): the emission schema v1.1 is PENDING
CTO SHAPE VALIDATION. Phase 1 (design) runs NOW against the draft + your fresh view->URL->key->
writer map @b48634789a; Phase 2 (implementation) binds to the RATIFIED shape only -- rendering
against a draft schema that then moves is rework manufactured on purpose.

PORTAL LAW BINDS IN FULL (MP surfaces = must-always-be-right): portal repo stays on DEV;
comp-surface-check is ENFORCED portal-side (rc=2 BLOCKED refuses the commit; a SEV1 is a STOP);
comp-transform schema-check before touching data props (+ --feature and ternary-audit if a new
mode/token enters a union type); the silver-canvas rendering law (/frontend-dev screenshot
verification -- a grep cannot see contrast); DE builds, DT promotes.
</context>

<scope>
1. PHASE 1 (now): design the held-vs-measured visual treatment against schema v1.1 + your
   as-displayed map -- which components render the affected series (your map names them), what
   the carried-point treatment is (visual distinction + the transition-to-None), what the
   page-level "window" statement shows. Confirm field availability with 0.2.0_DS against the
   draft; flag any field the render needs that the schema lacks BEFORE ratification (cheaper
   than after).
2. PHASE 2 (on schema ratification, relayed by me/CTO): implement on DEV per portal law;
   /frontend-dev screenshot verification of the rendered distinction on the actual page;
   comp-transform schema-check + ternary-audit if a union type gains a token.
3. Acceptance rides the DEPLOYED page at DT promote (their leg), with your DEV evidence +
   screenshots as the DE deliverable.
4. NO serve-content changes from this TO -- it renders what the emission provides; the emission
   side (DS) and the serve-corrections (held for Andrew) are separate gates.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="design, now">
    <step>
      <run>your @b48634789a map (cite, do not re-derive) + comp-transform schema-check on each component your map names for the affected series</run>
      <expect>Component list + current data-prop shapes; any MISSING = runtime undefined, enumerated before design.</expect>
      <if_mismatch>A component the tool cannot resolve gets a source read; note the gap.</if_mismatch>
    </step>
    <step>
      <run>field-availability confirm with 0.2.0_DS against schema v1.1 (message, cite the draft commit)</run>
      <expect>Every field the design renders exists in the draft (or is flagged to CTO's shape validation NOW).</expect>
      <if_mismatch>A missing field is a SCHEMA flag, not a render workaround -- route before Phase 2.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="implement, on ratified shape">
    <step>
      <run>implement on DEV; comp-transform schema-check (+ --feature/ternary-audit if union tokens change); /frontend-dev screenshot verification</run>
      <expect>Rendered distinction visible in the screenshot (measured vs carried vs None-transition); silver-canvas law holds; portal pre-commit surface-check passes or its SEV1 STOPs are resolved, never bypassed.</expect>
      <if_mismatch>A SEV1 from comp-surface-check is a STOP -- route to CTO; SURFACE_ACK is not yours to invoke on an MP surface.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>report to COO + CTO + DS: DEV commit + screenshots + the DT promote handoff</run>
      <expect>Row 6's render-half carries DE evidence at last; DT's promote leg closes the row's serve-side.</expect>
      <if_mismatch>REWORK on missing screenshot evidence -- a render claim without the rendered image is an assertion.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
DS owns the emission half (schema v1.1 pending CTO shape validation -- your Phase-1 field flags
feed that validation); DT owns the promote leg; the serve-corrections (DC1/C1impl Leg B) are
Andrew-held and SEPARATE -- your render must be correct for both pre- and post-correction values
(it renders labels, not magnitudes). Row 6's closure remains gated on BOTH halves + the sweep's
both-true standard (delivery AND gate evidence).
</cross_domain_coordination>

<acceptance_criteria>
1. Phase-1 design doc: components + treatments + field-availability confirm, any schema flags
   routed pre-ratification.
2. Phase-2: DEV implementation with /frontend-dev screenshots showing the measured/carried/None
   distinction on the actual page; schema-check + (if applicable) ternary-audit clean; portal
   surface-check honored (no bypass).
3. The row-6 closure package: DE evidence + DT promote handoff, reported to COO+CTO+DS.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="sweep">CTO closure-row sweep @67bbb6981d (row 6 render-half: delivered-nowhere, gated-nowhere)</ref>
  <ref type="grounding">Your as-displayed assessment @b48634789a (the fresh view->URL->key->writer map)</ref>
  <ref type="schema">DS partial-channel emission schema v1.1 @b91c99dfc4 (pending CTO shape validation) + the CTO carry-window three labeling requirements (221952Z)</ref>
</references>

<dependencies>
  <dependency agent="1.0.0_SA_CTO" task="emission schema shape validation" status="pending (gates Phase 2 only; Phase 1 runs now)"/>
</dependencies>
</task_order>
