<task_order>
<id>NFRA_C3MATERIALIZE.TO-L3W3-COX</id>
<status>pending</status>
<assigned_to>0.7.0_AE_CloudOps~X</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_C3MATERIALIZE</project>
<issued_date>2026-08-30</issued_date>

<carrier>Andrew-direct 2026-08-28 ~05:04Z (the /drive loop on NFRA_C3MATERIALIZE) and 14:08Z "Lift everything, time to work buddy" (the L2 hold lifted). Design ruling: 1.0.0_SA_CTO~X msg 81286 + sec 10b @b3873740fe; ruling pin @0f9a2aa6db. Rule 14(e) discharged on the certified subject. STOP: this face is cut from CERTIFIED cells only.</carrier>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260829T1906Z/DECOMP.md @94935b740e

cells:
L3W3-b8a2-1 L3W3-b8a2-2 L3W3-b8a2-3 L3W3-b8a2-4 L3W3-b8a2-5 L3W3-b8a2-6 L3W3-b8a2-7 L3W3-fadd-1 L3W3-fadd-2 L3W3-fadd-3 L3W3-fadd-4
partition: the 34 certified cells are owned on THREE lane faces by the rectangle's `executor_class`; this face owns the cells whose executor_class == 0.7.0_AE_CloudOps~X. Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism L3W3-m-1 L3W3-m-2 L3W3-m-3 L3W3-m-4 L3W3-m-5 L3W3-m-6 L3W3-m-7 L3W3-m-8 L3W3-m-9.

<owned_cells>
L3W3-b8a2-1 L3W3-b8a2-2 L3W3-b8a2-3 L3W3-b8a2-4 L3W3-b8a2-5 L3W3-b8a2-6 L3W3-b8a2-7 L3W3-fadd-1 L3W3-fadd-2 L3W3-fadd-3 L3W3-fadd-4
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="L3W3-COX-AC1" cell_refs="L3W3-b8a2-1">
    <label>k_sweep.parameters_declared</label>
    <oracle>K in {20, 50, 100, 200} with T FIXED, declared WITH what would falsify the sweep's reading. State the expected direction before running: wave 2 measured K=20 -> 0.5358 and K=100 -> 0.5961 on the both-measured frame, so a monotone rise is the prior -- and a NON-monotone result is a finding, not an error to re-run away.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC2" cell_refs="L3W3-b8a2-2">
    <label>k_sweep.inputs_pinned</label>
    <oracle>view 1, view 2, view P, the shared cohort and the mask carrier each pinned path @ commit + sha256 of the bytes actually read, verified BEFORE compute and printed. An unpinned input is not an input (certification arm 2).</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC3" cell_refs="L3W3-b8a2-3">
    <label>k_sweep.arms_declared</label>
    <oracle>PER K, on BOTH frames, each with its denominator: (i) fused with view 2 REAL; (ii) fused with view 2 PERMUTED -- C2's complement; (iii) fused with P; and (iv) view 1 fused with ITSELF (C1) -- ALSO PER K, at the same T, implementation, population, pair predicate and frame as (i)-(iii). C1 IS THE METHOD-INTRINSIC BASELINE AND K CHANGES SNF ITSELF (measured: real fusion 0.5510 at K=20, 0.5961 at K=100, c11d1ff734), so a C1 fixed at one K cannot bound method cost at another -- without (iv) per K, movement in (i)-(iii) is confounded between CHANGING METHOD EROSION and CHANGING SECOND-VIEW CONTRIBUTION. The comparison (iii) vs (ii) is the wave's whole question -- if P is flattened as hard as a permuted view, the flattening is METHOD-INTRINSIC; if P survives, it is firm-blindness of the input -- and it DISCRIMINATES ONLY when read against C1 AT THE SAME K.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC4" cell_refs="L3W3-b8a2-4">
    <label>k_sweep.exact_zero_census</label>
    <oracle>The EXACT-ZERO COUNT printed per K as an integer beside every AUC (sec 10a). Hard-K sparsification leaves entries outside each row's top-K at exactly 0.0 through diffusion -- 297,780 pairs (3.5%) tied at the bottom at K=20 -- and rank AUC is NOT tie-invariant. Tie mass moves WITH K, so without this integer a rising AUC cannot be told from fewer ties. One integer per run; its absence REFUSES the row.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC5" cell_refs="L3W3-b8a2-5">
    <label>k_sweep.battery</label>
    <oracle>permutation_battery.<S> per statistic in the 1c/1e shape: scheme as a TYPED STRING (never inferred from prose), n_permutations PER STATISTIC, spread = SAMPLE sd (ddof=1), precision_decimals carried, draws listed. J requires N >= 20 before any floor derives from it (tail_observed_at_n 6 from wave 2); rho is unbound at N >= 5.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC6" cell_refs="L3W3-b8a2-6">
    <label>k_sweep.output_artifact</label>
    <oracle>One artifact per K in the wave-2 union shape: defined over ALL 19,482 entities and ALL 189,764,421 pairs with per-view MEASURED/ABSENT masks, carrying carrier_table AND entity_domain as two distinct fields. An artifact defined only on the measured subset is the intersection in a different coat and is REFUSED.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC7" cell_refs="L3W3-b8a2-7">
    <label>k_sweep.reproducibility</label>
    <oracle>supersedes.chain built as `predecessor.chain + [predecessor]` so no hop can be dropped by construction -- wave 2's chain lost the 1f5d4f6136 hop to a hand-maintained index write. split_half typed per 1e (A): battery_id, seed, half_a_runs[], half_b_runs[], disjoint, n_a, n_b; overlapping run sets are FORM_DEFECT.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC8" cell_refs="L3W3-fadd-1">
    <label>frames.frame_A_full_cohort</label>
    <oracle>The full 1,941 locked cohort: all three AUCs with the mask treatment explicit per entity, the 121 view-2-ABSENT members carrying view-1 pass-through LABELLED as such and never presented as fused values.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC9" cell_refs="L3W3-fadd-2">
    <label>frames.frame_B_both_measured</label>
    <oracle>The 1,820 both-measured sub-cohort reported SEPARATELY beside frame A -- two numbers per view, never one carried from the other (80835).</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC10" cell_refs="L3W3-fadd-3">
    <label>frames.metric_domain_predicate</label>
    <oracle>The metric domain for rho / J / the control is the BOTH-MEASURED pairs, printed AS the predicate with its denominator. Over one-view pairs the 'fused' value is view-1 pass-through and a stability statistic there measures view 1's SELF-agreement -- high for the wrong reason.</oracle>
  </criterion>
  <criterion id="L3W3-COX-AC11" cell_refs="L3W3-fadd-4">
    <label>frames.p_arm_domain</label>
    <oracle>P's own frame printed as its own denominator and never merged into the others: C(1337,2) = 893,116 both-measured pairs against the 189,764,421 union domain. The arm is 6.9% of entities; a reader must see that beside any number it produces.</oracle>
  </criterion>
</proof_of_spec>

<artifacts_contract>
  Every artifacts_produced row carries commit_or_etag in ONE of exactly two forms.
  (a) A RESOLVABLE IDENTITY: a git commit hex (7-40 chars, resolvable by
      `git cat-file -e <hex>^{commit}`), or `sha256:<64 hex>` for a content digest.
  (b) The EXACT sentinel PENDING-THIS-COMMIT -- and ONLY where the artifact is covered by the
      very commit that carries this proof. A proof cannot name its own hash, because the hash
      covers the proof. The ISSUER stamps the real hex at TO close.
  PROSE IS REFUSED. Free-text self-reference is not an identity and, more to the point, is not
  CENSUSABLE: a consumer cannot enumerate unstamped rows when each proof spells the gap its own way.
  MEASURED 2026-08-29 over the 13 NFRA_C3MATERIALIZE proofs: 67 rows, 44 resolvable, 23 not --
  19 of the 23 self-references in FOUR spellings, 8 of them prose. Two of those four spellings
  came from the lanes this face addresses, which is why the contract is stated rather than assumed.
  Size and LastModified are PROPERTIES, not identities: they belong in a sibling field, never here.
</artifacts_contract>
</task_order>
