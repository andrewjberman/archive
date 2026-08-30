<task_order>
<id>NFRA_C3MATERIALIZE.TO-L3W3-CCX</id>
<status>pending</status>
<assigned_to>0.8.0_AE_CloudComp~X</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_C3MATERIALIZE</project>
<issued_date>2026-08-30</issued_date>

<carrier>Andrew-direct 2026-08-28 ~05:04Z (the /drive loop on NFRA_C3MATERIALIZE) and 14:08Z "Lift everything, time to work buddy" (the L2 hold lifted). Design ruling: 1.0.0_SA_CTO~X msg 81286 + sec 10b @b3873740fe; ruling pin @0f9a2aa6db. Rule 14(e) discharged on the certified subject. STOP: this face is cut from CERTIFIED cells only.</carrier>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260829T1906Z/DECOMP.md @94935b740e

cells:
L3W3-c69f-1 L3W3-c69f-2 L3W3-c69f-3 L3W3-c69f-4 L3W3-c69f-5
partition: the 34 certified cells are owned on THREE lane faces by the rectangle's `executor_class`; this face owns the cells whose executor_class == 0.8.0_AE_CloudComp~X. Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism L3W3-m-1 L3W3-m-2 L3W3-m-3 L3W3-m-4 L3W3-m-5 L3W3-m-6 L3W3-m-7 L3W3-m-8 L3W3-m-9.

<owned_cells>
L3W3-c69f-1 L3W3-c69f-2 L3W3-c69f-3 L3W3-c69f-4 L3W3-c69f-5
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="L3W3-CCX-AC1">
    <cell_refs>L3W3-c69f-1</cell_refs>
    <label>L3C01_floor.consumer_binding</label>
    <oracle>THE SEAT SEATED ON THIS CELL OWNS READING `firm_representation` AND THIS CELL NAMES THE FIELD EXPLICITLY rather than inheriting it from any message. MEASURED by 0.8.0_AE_CloudComp~X at the pin: NO consumer reads it today -- check_stability_L3C01.py @d8725bc60c, 936 lines, `firm_representation` 0 / `effective_partition` 0 / `base_rate` 0 / `mdpf` 0, positive control `permutation_battery` 6. That is the EXPECTED answer (those are wave-3 arm fields on an artifact that did not exist), not a gap in that seat's work -- and it is exactly why the binding needs an owner: a field everyone believes is read that nobody cuts a cell to read drifts to unpopulated. Measured on this project: 0 of 16 defective where a validator rejects, 5 of 39 in the neighbouring free string. The consumer REJECTS on a missing or unresolvable firm_representation; it does not warn.</oracle>
  </criterion>
  <criterion id="L3W3-CCX-AC2">
    <cell_refs>L3W3-c69f-2</cell_refs>
    <label>L3C01_floor.floor_derivation</label>
    <oracle>THIS IS RUN 2, so a floor MAY finally be derived -- and only from run 1's battery, never its own (1b prohibits same-run derivation). floor_derivation.<S> carries derived_from_run_id, derived_at_commit, derived_from_path, derived_artifact_sha256, metric_domain, null, spread, n_permutations, multiplier 3, floor (the checker RECOMPUTES it), deriving_run_observed and sanity. derived_at_commit MUST be a strict ancestor of the carrier.</oracle>
  </criterion>
  <criterion id="L3W3-CCX-AC3">
    <cell_refs>L3W3-c69f-3</cell_refs>
    <label>L3C01_floor.tail_binding</label>
    <oracle>J's derivation is BLOCKED until N >= 20 and carries tail_observed_at_n 6; rho may derive at N >= 5 having no tail. An in-battery draw outside the band of the others at derivation time returns SPREAD_TAIL and REFUSES to derive for that statistic -- not SPREAD_SANITY_FAIL, which is about the deriving run's observed.</oracle>
  </criterion>
  <criterion id="L3W3-CCX-AC4">
    <cell_refs>L3W3-c69f-4</cell_refs>
    <label>L3C01_floor.sanity_arm</label>
    <oracle>floor_S must lie strictly BELOW the observed S of the run it was derived from; a re-derived floor the deriving run itself fails is a finding about the spread being too wide to discriminate, and floor_status stays HELD-UNEXERCISED rather than binding.</oracle>
  </criterion>
  <criterion id="L3W3-CCX-AC5">
    <cell_refs>L3W3-c69f-5</cell_refs>
    <label>L3C01_floor.refusal_on_absence</label>
    <oracle>An absent battery, an absent scheme, a missing derived_from_path or a non-ancestor derived_at_commit each REFUSE the derivation with its own typed result -- PROVENANCE_UNVERIFIED is never a pass, and an unrunnable provenance check is not a passed one.</oracle>
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
