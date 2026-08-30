<task_order>
<id>NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement</id>
<status>pending</status>
<assigned_to>0.8.0_AE_CloudComp~Y</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_C3MATERIALIZE</project>
<issued_date>2026-08-30</issued_date>

<carrier>Rule 14(e) round 1 on the sec-7b rectangle: seal @0ac1ef9a4e (attempt 1), blind nomination 3.0.0_SA_CVO~X 09:19Z, SCORE HIT @a7f731de55; the seat-citation correction AT THE CELL c0'' @85c9fc3e32 (surprise 87230, disarm 87243); certified record rectangle.final.certified.json @391cd500e5 (sha256 09c49480161cd57a7c06e03442abe1277fb503252c9eb49f8fa9c62de1966613) -- 4.0.0_SA_CRO~X ARTIFACT PASS 12:55Z + 3.0.0_SA_CVO~X ARTIFACT PASS 12:57Z on c0'', 1.0.0_SA_CTO~X JSON PASS 87497, FINAL PASS ON ORIGIN 3.0.0_SA_CVO~X 13:48Z + 4.0.0_SA_CRO~X 13:49Z at origin/CLOUD 924d560a32; DECOMP.md @42342fd0ed; render checker @2445be60af. Seat: 2.0.0_SA_COO 87443 (option (c): 0.8.0_AE_CloudComp~Y takes the sec-7b MEASUREMENT unit FIRST, then the DECLARATION unit; Rule 27 satisfied -- the seat holds NFRA_C3MATERIALIZE and nothing else, 87182). STOP: this face is cut from CERTIFIED cells only; every oracle below is the certified cell's text byte-for-byte (self-tested by cut_7B_faces.py).</carrier>

<sequenced_after>the certified record's FINAL PASS ON ORIGIN (both certifiers, 13:48-13:49Z) -- discharged; nothing else. Gate of every owned cell: `now`. NOT sequenced after any candidate: this unit needs none (candidate typed NONE on the rectangle; the DECLARATION unit follows at the same seat, base 87443 order 2-then-1).</sequenced_after>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260830T0852Z/rectangle.final.certified.json @391cd500e5 (sha256 09c49480161cd57a7c06e03442abe1277fb503252c9eb49f8fa9c62de1966613)
workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260830T0852Z/DECOMP.md @42342fd0ed (the rendering; the JSON is the record)

cells:
L3S7B-1c16-1 L3S7B-1c16-3 L3S7B-0b5f-1
partition: the 21 certified cells are 6 planes; this face owns every cell at gate `now` outside PROJECT_MECHANISM (3 cells: L3S7B-1c16-1 (SINGLE_VIEW_BASELINE), L3S7B-1c16-3 (SINGLE_VIEW_BASELINE), L3S7B-0b5f-1 (NULL_BATTERY)). Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism L3S7B-m-1 L3S7B-m-2 L3S7B-m-3 L3S7B-m-4 L3S7B-m-5 L3S7B-m-6 L3S7B-m-7. NOT on this face (later gates, other units): L3S7B-1c16-2 (SINGLE_VIEW_BASELINE, gate after-bridge-declared); L3S7B-4017-1 (CANDIDATE_VIEW, gate after-bridge-declared); L3S7B-4017-2 (CANDIDATE_VIEW, gate after-bridge-declared); L3S7B-4017-3 (CANDIDATE_VIEW, gate after-bridge-declared); L3S7B-0b5f-2 (NULL_BATTERY, gate after-candidate); L3S7B-4565-1 (FUSION_ARMS, gate after-null-battery); L3S7B-4565-2 (FUSION_ARMS, gate after-null-battery); L3S7B-8304-1 (ENTRY_ORACLE, gate after-fusion-arms); L3S7B-8304-2 (ENTRY_ORACLE, gate after-fusion-arms); L3S7B-8304-3 (ENTRY_ORACLE, gate after-fusion-arms); L3S7B-8304-4 (ENTRY_ORACLE, gate after-fusion-arms).

<owned_cells>
L3S7B-1c16-1 L3S7B-1c16-3 L3S7B-0b5f-1
</owned_cells>
</decomp_ref>

<face_scope amended="2026-08-30T13:5xZ" by="2.0.0_SA_COO~X" grounds="the MEASUREMENT unit -- the unfused single-view baseline on the declared frames, the frame declaration, and the REBUILT clause-1 instrument exercised on perm(W1) as its own control; NO candidate exists and none is needed here">
  FRAMES (rectangle.frames, verbatim): B = 1820 members, predicate 'view 1 AND view 2 MEASURED (both-measured), the judged frame' -- the JUDGED frame; A = 1941 members, 'the full cohort; REPORTED beside B, never carried from or to B (1k(iii))'; pairs_both_measured_B = 8596731; union_pairs = 189764421. IMPLEMENTATION (rectangle.implementation): snf_ksweep.py @cfc5f28fb7 + run_sweep.py @e2ab79fba4 -- the FIXED implementation for this step is the wave-3 engine at these pins unless the design lane names another AT THE CUT; no number produced on any other implementation crosses into this rectangle (1i(ii))
  CARRIER FIELDS every emitted carrier MUST carry (wave-3 m-1, met by construction): carrier_table=CloudNode, entity_domain=L2_STRUCTURE_heterogeneous.
  DESIGN DECLARATIONS binding to this face's cells (DESIGN_DECLARATIONS_AT_THE_CUT_1.0.0_SA_CTO~X.json @e04cad153a, sha256 7dd15d6bea1a4923a6bac0e1f0d7cb517b83c2fbfdafaffcc1366b021baa09fb; declared BEFORE any output, 1.0.0_SA_CTO~X 86981/86990): declaration 1 (frame) -> L3S7B-1c16-3, L3S7B-1c16-1; declaration 4 (null_battery_form) -> L3S7B-0b5f-1; declaration 7 (fixed_implementation) -> L3S7B-1c16-1. The NUMBERS on this face are the design lane's (the headroom distance, the refusal threshold, the null form, the seed, n, ddof, precision, the absolute floor) -- read them at the pin; the issuer declares none (L3S7B-m-4).
  ORDER: L3S7B-1c16-3 (frame declaration) is written FIRST and byte-equal on every carrier; L3S7B-1c16-1 (the unfused baseline) is produced BEFORE any fused arm on this rectangle (its value_domain's produced_before field is the proof; a baseline produced after a fused output is FORM_DEFECT); L3S7B-0b5f-1 (the rebuilt instrument) is exercised on perm(W1) as its own control BEFORE any candidate exists -- if F(W1, perm(W1)) does not read below C1 = SNF(W1, W1) by more than 3 spreads on the same frame and (K, T), the instrument cannot see a permutation and NO clause-1 verdict is admissible on it (declaration 4). HEADROOM (declaration 3): if max(AUC(W1), AUC(V)) on frame B exceeds 0.90 the frame is REFUSED for the 6.3 re-run and the frame question returns to the cut -- with no V yet, AUC(W1) alone is tested here and the refusal, if it fires, is a FINDING on this face, never a value to move.
  NOT A RESULT: nothing on this face names any sec-6 test as passed or failed (rectangle.completion_claim_rule). No L4 act. No candidate view is admitted, built or run here (CANDIDATE_VIEW is gated after-bridge-declared; the DECLARATION unit at this seat is row 0 -> rows 1-4 per 87275).
</face_scope>

<sequence_gates>now -- every owned cell is at gate `now` on the certified rectangle; a cell evaluated out of gate order is FORM_DEFECT (L3S7B-m-7). Produce in the ORDER stated in face_scope.</sequence_gates>

<proof_of_spec>
  <criterion id="L3S7B-CCY-AC1" cell_refs="L3S7B-1c16-1">
    <label>single_view_baseline.auc_w1_unfused</label>
    <oracle>AUC(W1) with NO fusion, on frame B (1,820 both-measured members, pair predicate = both view 1 and view 2 measured) and REPORTED beside on frame A (1,941), on the fixed implementation (IMPL pins on this rectangle), the denominator printed beside each value (pairs judged, of the frame's pair domain). Produced BEFORE any fused candidate output is inspected -- this cell is the headroom precondition's baseline (1k(i)) and clause 2's left operand; without it the design lane's declared headroom distance has nothing to be measured against.</oracle>
    <value_domain>two AUCs (frame B judged, frame A beside) with their pair denominators; implementation pin cited; produced_before = the ISO time of the first fused-arm run on this rectangle, or 'no fused arm run' -- a value produced after any fused output is FORM_DEFECT</value_domain>
  </criterion>
  <criterion id="L3S7B-CCY-AC2" cell_refs="L3S7B-1c16-3">
    <label>single_view_baseline.frame_declaration</label>
    <oracle>The frame is DECLARED on this rectangle before any arm runs: frame B (1,820) judged, frame A (1,941) beside; the pair predicate; the union pair domain 189,764,421 and the both-measured pair count 8,596,731 printed as denominators; and the entity domain's TWO fields (carrier_table CloudNode, entity_domain L2_STRUCTURE_heterogeneous) carried on this carrier and on every carrier this rectangle emits -- the wave-3 m-1 rule met BY CONSTRUCTION, not censused after the fact.</oracle>
    <value_domain>the frame block above, byte-equal on every emitted carrier (a census on close proves it)</value_domain>
  </criterion>
  <criterion id="L3S7B-CCY-AC3" cell_refs="L3S7B-0b5f-1">
    <label>null_battery.instrument_rebuilt</label>
    <oracle>The clause-1 instrument is REBUILT, not reused: the wave-2 permuted arm @c11d1ff734 is carded UNSOUND AS A GATE @4e7016f471. The rebuilt arm carries a per-arm independently seeded RNG with the SEED ON THE ORACLE, one null per artifact, n &gt;= 20 draws for a tail, spread ddof=1, precision declared, (K, T) declared on the oracle, and its own failure signal stated. Exercised FIRST on a permuted W1 as its own control (Addendum 1m(iv)) before any candidate exists.</oracle>
    <value_domain>the instrument's source pin + the seed scheme + n + the declared precision + the control run's null mean/spread on perm(W1), with the failure signal it emitted or did not</value_domain>
  </criterion>
</proof_of_spec>

<artifacts_contract>
  Every input row on every carrier this face emits carries digest_of in {blob-at-pin (pin on the row), s3-etag, served-object (immutable run-addressed URI), content-addressed (retrieval + named gap)} -- a bare sha256 with no digest_of is FORM_DEFECT; a worktree-rendering digest (CRLF checkout) is FORM_DEFECT on a certified row (Addendum 1l(iii), (vi)). Every value carries its basis (measured / inferred / held / absent). Every count prints what it is a count of, with its denominator. Every artifacts_produced row on the proof-of-spec instance carries commit_or_etag as a resolvable git hex or sha256:&lt;64 hex&gt;, or the EXACT sentinel PENDING-THIS-COMMIT (only where the carrying commit covers the artifact); prose refused. The proof instance is authored by the seat, validated on the COMMITTED bytes with .tools/proof-of-spec-check.py (expected ids L3S7B-CCY-AC1,L3S7B-CCY-AC2,L3S7B-CCY-AC3), with the criteria PARSED from this face, never retyped; presented to 3.0.0_SA_CVO~X + 4.0.0_SA_CRO~X (denominator 3 with the issuer); the flip is the issuer's on the joint PASS. Commits via .tools/safe-commit.sh with the seat's author; push is the integrator's; push state stated as measured.
</artifacts_contract>
</task_order>
