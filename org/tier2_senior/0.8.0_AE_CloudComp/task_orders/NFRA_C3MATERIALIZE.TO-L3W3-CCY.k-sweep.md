<task_order>
<id>NFRA_C3MATERIALIZE.TO-L3W3-CCY</id>
<status>pending</status>
<assigned_to>0.8.0_AE_CloudComp~Y</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_C3MATERIALIZE</project>
<issued_date>2026-08-30</issued_date>

<carrier>Andrew-direct 2026-08-28 ~05:04Z (the /drive loop on NFRA_C3MATERIALIZE) and 14:08Z "Lift everything, time to work buddy" (the L2 hold lifted). Design ruling: 1.0.0_SA_CTO~X msg 81286 + sec 10b @b3873740fe; ruling pin @0f9a2aa6db. Rule 14(e) discharged on the certified subject. STOP: this face is cut from CERTIFIED cells only.</carrier>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260829T1906Z/DECOMP.md @94935b740e

cells:
L3W3-dc02-1 L3W3-dc02-2 L3W3-dc02-3 L3W3-dc02-4 L3W3-dc02-5 L3W3-dc02-6 L3W3-dc02-7 L3W3-dc02-8 L3W3-dc02-9
partition: the 34 certified cells are owned on THREE lane faces by the rectangle's `executor_class`; this face owns the cells whose executor_class == 0.8.0_AE_CloudComp~Y. Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism L3W3-m-1 L3W3-m-2 L3W3-m-3 L3W3-m-4 L3W3-m-5 L3W3-m-6 L3W3-m-7 L3W3-m-8 L3W3-m-9.

<owned_cells>
L3W3-dc02-1 L3W3-dc02-2 L3W3-dc02-3 L3W3-dc02-4 L3W3-dc02-5 L3W3-dc02-6 L3W3-dc02-7 L3W3-dc02-8 L3W3-dc02-9
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="L3W3-CCY-AC1" cell_refs="L3W3-dc02-1">
    <label>view_P.population_binding</label>
    <oracle>The 1,337 pipeline symbols are DIRECT MEMBERS of the 19,482 -- prove it at the pin, do not inherit it: exact string equality against the L2 STRUCTURE entity_set @64ae1ae879, expect 1,337 of 1,337, and print BOTH directions so a one-sided match cannot read as membership. Cite 1.0.0_SA_CTO~Y's positive_arm_probe.json as the pinned input and the certified overlap @bdc1246987. NO CHAIN is authorized: the 4-hop cloud-node -> arn -> motif -> symbol -> firm composition is MOOT and REFUSED (it would traverse a COVER bridge backward through an undeclared hop to reach entities already in the set).</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC2" cell_refs="L3W3-dc02-2">
    <label>view_P.feature_derivation</label>
    <oracle>W_P(i,j) = 1 if firm(i) == firm(j) else 0 over the 1,337, firm taken from pipesym_to_firm rows L3W1-ypbj-1..8 at the SETTLED registry pin -- read the shard, never re-parse independently. The shard's own fan-in (bd 724 / inf 594 / mdpf 19) is a FLOOR to reproduce, not a number to copy.</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC3" cell_refs="L3W3-dc02-3">
    <label>view_P.coverage_measured_absent</label>
    <oracle>MEASURED 1,337 / ABSENT 18,145 over denominator 19,482 = 6.9%. ABSENT STAYS MASKED AND NEVER BECOMES A COMPARABLE VALUE: a 0.0 is a MEASURED statement of no affinity, ABSENT is the statement that nothing was measured, and converting the 18,145 (93.1% of the population) to 0.0 would silently move the metric domain off the ruled both-measured C(1337,2) = 893,116 onto the full union while every number still printed a denominator. ABSENT is ABSENT, never zero, and carries the same per-pair mask shape wave 2 used; entity order is the mask carrier's (ascending index in the entity_set @64ae1ae879).</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC4" cell_refs="L3W3-dc02-4">
    <label>view_P.role_typing</label>
    <oracle>role = CONTROL_ONLY and six_three = 6.3_NOT_A_RESULT, both TYPED on the artifact rather than stated in prose, with circularity typed beside them: P's firm label IS the 6.3 cohort label on these same entities (parse agreement 1,337/1,337), so fusing view 1 with P and evaluating 6.3 on that cohort would INHERIT the thing being tested. The row prints its 6.3 number AND labels it not-a-result. A consumer reading role must be able to reject on it.</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC5" cell_refs="L3W3-dc02-5">
    <label>view_P.basis_declarability</label>
    <oracle>basis = INFERRED (segment-2 parse -- the SAME parse the certified cohort labels carry, admissible at the same typed basis and NEVER promoted to measured) and declarability = NAMED_GAP_STORE_OWNER, carried exactly as the shard says. A DECLARED per-entity firm is the L1-spine named gap and does NOT gate this wave.</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC6" cell_refs="L3W3-dc02-6">
    <label>view_P.base_rate</label>
    <oracle>P's base rate PRINTED BESIDE EVERY P ROW at every K: same_firm_pairs 438,018 (C(724,2) 261,726 + C(594,2) 176,121 + C(19,2) 171) / cross_firm_pairs 455,098 / denominator 893,116 / fraction_ones 0.4904, typed as arms[P].base_rate per the design lane @6d23af95b9. STOP: IT IS A FRAME THE READER NEEDS, NOT A DISCOUNT TO APPLY: the sweep's AUC is a ROC-AUC over pairs and ROC-AUC is INVARIANT TO CLASS PREVALENCE by construction (ranks within each class; the positive:negative ratio cancels). A near-balanced P therefore does NOT inflate its AUC. 0.8.0_AE_CloudComp~X supplied this number with the opposite consequence attached and withdrew that consequence itself at 81337; PR-AUC would be prevalence-sensitive, this is not. NO ROW MAY DEFLATE A P RESULT BY THIS FRACTION.</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC7" cell_refs="L3W3-dc02-7">
    <label>view_P.firm_representation</label>
    <oracle>THE ONE LIVE FIELD NAME for this quantity, ruled @9cfa4eebbf: `firm_representation`. arms[P].effective_partition is RETIRED as a live name and survives only as a SCHEMA-DECLARED ALIAS -- do NOT emit it as a second token, because two live names for one quantity disagree silently (0.8.0_AE_CloudComp~X 81407). Carry under it: bd_vs_inf semantics; `mdpf_share_of_ones: 0.00039` TYPED; and the sharp form -- MDPF SEPARATION IS UNMEASURABLE IN THIS ARM, not merely small. mdpf is 19 symbols contributing 171 of the 438,018 same-firm pairs, so P is EFFECTIVELY a two-block bd-versus-inf partition and any per-firm reading of this sweep is a bd-versus-inf reading that must say so rather than implying three-firm coverage. Untouched by the prevalence correction -- representation, not base rate.</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC8" cell_refs="L3W3-dc02-8">
    <label>view_P.coverage_vs_fanout</label>
    <oracle>State BOTH, because a census table places them side by side and the pair reads as a contradiction: pipesym_to_firm's cardinality_class = UNMEASURED is about FAN-OUT at the full-id grain (unmeasurable by construction on a roll-up), NOT about coverage. COVERAGE is the shard's own join run L3W1-ypbj-3: |left| 1,337, |right| 3, |join| 1,337, ZERO unresolved. An arm claiming full coverage beside a bridge row reading UNMEASURED is consistent, and the cell must make that legible without a reader re-deriving it.</oracle>
  </criterion>
  <criterion id="L3W3-CCY-AC9" cell_refs="L3W3-dc02-9">
    <label>view_P.provenance</label>
    <oracle>Every input cited path @ commit with the bytes' own sha256 where the pin does not bind content, INCLUDING the pinned cell input KSWEEP_POSITIVE_ARM_PROBE.json @fb0a013b04 (schema nfra-c3materialize.l3w2.ksweep.positive-arm-probe/1.0) which LISTS the 1,337 member ids with their labels -- so the cell cites a pinned population, not a description of one. The ruling is cited via `ruling_pins` and the `pins` map -- this cell names NEITHER a pin count NOR a push state. [HISTORICAL] It previously said the ruling was cited with ALL THREE PINS and called one of them the stale on-origin pin. Both halves are spent: ruling_pins is exactly two entries, and mechanism.dual_citation already records that the published-pin-is-stale framing ended when window 37 published the amendments. A cell restating a count or a state is a SECOND CARRIER of what the map and ruling_pins already hold. [/HISTORICAL]</oracle>
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
