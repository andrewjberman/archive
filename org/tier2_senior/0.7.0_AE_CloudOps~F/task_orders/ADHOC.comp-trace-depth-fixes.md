<task_order>
<to_id>ADHOC.comp-trace-depth-fixes</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~F</issued_to>
<date>2026-08-04</date>
<status>complete</status>
<!-- COMPLETE 2026-08-04T2344Z: all named items landed @ffb41a849 + T0 restore @3293a0cda; CVO
     RAVC CLOSE 232812Z (6/6) + 234335Z (T0 restore, dial FULLY CLOSED); CTO accepted DEPTH-1
     232056Z. T2 untouched (PRD-gated). Override trailers discharged by ~B @4527d310e.
     Session log: logs/2026-08-04/dial_fixes_trace_depth_2145-2330Z.md -->
<priority>P1 (ANDREW-DIRECT ~1900Z fan-out @fc42aacc5: parallel seats on the spine-tool items; this seat takes the trace+depth fix set)</priority>

<title>comp-trace fixes T0/T1/T3/T5/T6 + comp-depth DEPTH-0/DEPTH-1 -- per the CVO dial records; T2 EXCLUDED (PRD-gated)</title>

<context>
Andrew ordered agents fanned out on the spine-tool open items (CVO record @fc42aacc5). THE SPECS
are CVO's dial records (comp-trace + comp-depth) -- read them in full first; CVO verifies each
item on landing. Fix shapes already stated by CVO for TO decomposition (their 191013Z routing +
earlier T(N) shapes): T1 NOT-FOUND universe/denominator/near-match (mirror comp-blast's repaired
rc=3 form), T3 provenance header printing both vintage axes (comp-kuzu header = the reference;
NOTE the header PRINTING is an engine edit separate from ~A's registration declaring the vintage
fields), T5 bare-call usage text (shim-form, not cli.py form), T6 exact-id self-selection flag,
T0 per the trace record, DEPTH-0/DEPTH-1 per the depth record (incl. the rc=2-on-out-of-enum
boundary CTO routed).

⛔ T2 IS EXCLUDED -- it waits on the PRD's family-ambiguity ruling (CTO's own elevation);
building it early builds a form the PRD may overrule.
</context>

<scope>
Exactly the named items from the two dial records (records win conflicts; surface, never
adjudicate). Exercise-before-and-after per item; CVO's baselines are the pre-fix controls.
No re-dials, no items beyond the named set, no registration work (that set is ~A's).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read both dial records in full + reproduce each named item (pre-fix controls, verbatim)</run>
    <expect>Every item reproduced or its delta named to CVO before building.</expect>
    <if_mismatch>STOP on non-reproducing items -- re-ground with CVO.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>per item: post-fix exercise (fails pre-fix, passes post-fix); unrelated-output byte-stability shown</run>
    <expect>Both directions captured; T2 surface untouched (grep your diff for the T2 family form -- absent).</expect>
    <if_mismatch>STOP on any T2-shaped change or unintended surface.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>report per item to CVO + me + CTO; cite ~A's registration seam where T3's header touches their declared vintage fields</run>
    <expect>CVO verifies without a follow-up ask; ~A seam cited.</expect>
    <if_mismatch>REWORK per CVO.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
~A holds the registration set (trace/depth canonical registration + kuzu K3 contracts feed) and
the comp-blast (a) rework -- T3's header PRINTING touches the same vintage fields their
registration DECLARES: cite each other, engine edit here, declaration there, conflicts route CVO
-> CTO. ~B holds the kuzu K-fixes in parallel (no shared files expected; K3 contracts are
theirs).
</cross_domain_coordination>

<acceptance_criteria>
1. Every named item: pre-fix control + post-fix exercise captured.
2. T2 untouched, shown.
3. CVO verify-on-landing per item; ~A seam cited on T3.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="authority">ANDREW-DIRECT ~1900Z fan-out (CVO record @fc42aacc5)</ref>
  <ref type="spec">comp-trace + comp-depth DIAL RECORDS (CVO deliverables) + CVO 191013Z fix-shape routing</ref>
</references>
<dependencies><none/></dependencies>
</task_order>
