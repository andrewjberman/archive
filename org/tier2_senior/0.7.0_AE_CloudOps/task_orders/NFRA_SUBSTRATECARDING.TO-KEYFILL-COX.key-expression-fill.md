# TASK ORDER -- COX · NFRA_SUBSTRATECARDING KEYFILL · THE key_expression FILL FOR THE CARDS CARDED BY `0.7.0_AE_CloudOps~X`

<status>pending</status>

**to:** `0.7.0_AE_CloudOps~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X` · **project:** NFRA_SUBSTRATECARDING (ONE project per instance, Rule 27; a `0.8.0_AE_CloudComp` lane is BARRED from the TOs addressed to the bare base serial) · **cut:** 2026-08-28 19:4xZ from the CERTIFIED final @23dfe292e7
**scope:** the 11 v3 cards under the wave dirs whose `carded_by` is `0.7.0_AE_CloudOps~X` (derived at cut time by glob + schema_version; the list is below and the executor RE-DERIVES it at run time -- a difference is named, never absorbed).

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-keyfill/20260828T1915Z/DECOMP.md @23dfe292e7

cells:
KEYFILL-hpos-1 KEYFILL-hpos-2 KEYFILL-hpos-3 KEYFILL-hpos-4 KEYFILL-hpos-5 KEYFILL-qoos-1 KEYFILL-qoos-2 KEYFILL-qoos-3 KEYFILL-qoos-4
partition: fill_declaration + evidence cells are owned on FOUR lane faces, each for the cards where carded_by == its lane; this face's partition is carded_by == 0.7.0_AE_CloudOps~X (11 cards). Present on this face, DISCHARGED BY THE ISSUER (not owned here): KEYFILL-lzzf-1 KEYFILL-lzzf-2 KEYFILL-lzzf-3 KEYFILL-ilbd-1 KEYFILL-ilbd-2; mechanism KEYFILL-mech-1 KEYFILL-mech-2 KEYFILL-mech-3 KEYFILL-mech-4 KEYFILL-mech-5. Owned elsewhere: KEYFILL-heaw-1 KEYFILL-heaw-2 (4.0.0_SA_CRO~X); KEYFILL-rcgx-1 KEYFILL-rcgx-2 KEYFILL-rcgx-3 KEYFILL-rcgx-4 (0.4.0_DT_ClientPlatform~X).
</decomp_ref>

<owned_cells>
KEYFILL-hpos-1 KEYFILL-hpos-2 KEYFILL-hpos-3 KEYFILL-hpos-4 KEYFILL-hpos-5 KEYFILL-qoos-1 KEYFILL-qoos-2 KEYFILL-qoos-3 KEYFILL-qoos-4
</owned_cells>

<proof_of_spec>
  <criteria>
    <criterion id="KF-COX-AC1" cell_refs="KEYFILL-hpos-1, KEYFILL-hpos-4"/>
    <criterion id="KF-COX-AC2" cell_refs="KEYFILL-hpos-2, KEYFILL-hpos-3"/>
    <criterion id="KF-COX-AC3" cell_refs="KEYFILL-hpos-5"/>
    <criterion id="KF-COX-AC4" cell_refs="KEYFILL-qoos-1, KEYFILL-qoos-2"/>
    <criterion id="KF-COX-AC5" cell_refs="KEYFILL-qoos-3, KEYFILL-qoos-4"/>
  </criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_SUBSTRATECARDING.TO-KEYFILL-COX_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>KF-COX-AC1,KF-COX-AC2,KF-COX-AC3,KF-COX-AC4,KF-COX-AC5</expected_criteria>
  <alignment_denominators>criteria 5/5 carry cell refs; cell_refs resolve into the decomp's 25-id space; owned cells 9/9 reachable from >=1 criterion; cards filled + absent-with-reason + refused == 11 (re-derived)</alignment_denominators>
</proof_of_spec>

## THE CARDS (carded_by == `0.7.0_AE_CloudOps~X`, derived at cut; the executor re-derives)

- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/anchor_catalog.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/baked_static_spec_layers.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/comp_debris.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/comp_ladder.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/dup_scan.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/resource_summaries.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W2/summary_corpus.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W3/cse_store__PATH_A_append.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W3/cse_store__PATH_B_drop.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W3/resource_summaries_store.json`
- `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W3/snap_store.json`

## THE ACT

For EACH card above, set `trust.key.key_expression` to a STRING a consumer can COMPUTE the member's key from in the card's `identity_space` (a path grammar, a column, a derivation, a declared parse -- SUBSTRATE_CARD.v3's own words @bb01a20272), or leave it null with `basis_by_field.key_expression = absent` and the REASON in `trust.key.evidence`. Then: `basis_by_field.key_expression` = **measured** ONLY when the expression was exercised on at least one REAL member of the substrate in this fill (the exercise PRINTED as the triple member -> key -> identity_space, and the key validated against that space's own predicate: a path grammar yields a path, a sha1 derivation yields 40 hex); **held** when declared but unexercised (still admissible, printed as such); **inferred is PROHIBITED** for a key expression; null + absent is a LEGAL outcome counted as ABSENT in the declared denominator. `trust.key.basis` stays the FLOOR of the row (the schema's allOf: measured => every sub-field measured; null => basis_by_field.key_expression absent and basis != measured). Every filled card validates against v3; one deliberately contradictory fixture (measured + null) is REFUSED as the negative arm. Honest absence outranks a plausible string.

## ACCEPTANCE CRITERIA (each cites the cells it discharges)

**KF-COX-AC1 -- COMPUTABLE, EXERCISED, OWNER-DECLARED** (`KEYFILL-hpos-1`, `KEYFILL-hpos-4`): every filled card's expression is exercised on >=1 real member with the triple printed and the key validated against the space predicate; the filling seat is the card's `carded_by` (this lane), so `trust.key.owner` stays truthful.
**KF-COX-AC2 -- BASIS CARRIED, ABSENCE HONEST** (`KEYFILL-hpos-2`, `KEYFILL-hpos-3`): basis_by_field per the rule above (measured only on a real exercise; held for declared-unexercised; inferred never; null+absent legal and counted); the row basis is the floor; an absence carries its reason.
**KF-COX-AC3 -- v3 VALID** (`KEYFILL-hpos-5`): the validator runs over this lane's filled set; PASS count printed with the denominator 11; the contradiction fixture is refused.
**KF-COX-AC4 -- CENSUS + CLEAN CLONE** (`KEYFILL-qoos-1`, `KEYFILL-qoos-2`): every count derived by the run and printed with its denominator (filled / absent-with-reason / refused over 11); the validator replays from a clean clone at --run-commit with the extract released on exit (--keep only for a named forensic case).
**KF-COX-AC5 -- NO EGRESS, PRESERVATION** (`KEYFILL-qoos-3`, `KEYFILL-qoos-4`): no vendor / PyPI / cloud call; pre-fill card bytes are in git history and the pre-fill digests are cited on the report; the diff pre->post is exactly the key rows.

## CERTIFICATION ARMS (bound by the certifier at c0; binding evidence arms, not cell text)

1. Print a real-member member-to-key-to-identity-space triple and validate the key against the target-space predicate.
2. Count basis as measured only when exercised in this fill; declared unexercised is held, inferred is prohibited, and null plus absent remains legal and counted.
3. Name the single exclusion and its reason in the 72-card census.
4. Print EMISSION and DECLARATION against the shared denominator 42; retain and name the three permanent unknowns inside unknown; join only by registry-minted part ID and leave string-name misses unjoined.
5. For declared posture, require basis, card path at commit, and mapping digest where applicable; preserve the pre-fill manifest by digest.

## LANE

The cards live under this lane's own deliverables directory; no scoped grant is needed. Push on CLOUD is integrator-only (LD-0367/0368): commit via `.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~X <0.7.0_AE_CloudOps~X@opal.agent>" -F <msgfile>` and state push state as a MEASURED value.

## BOUNDARIES

No schema byte moves (a schema defect is a finding to the schema owner). No manifest write (the receiver join is `0.4.0_DT_ClientPlatform~X`'s TO). No registry write (ratification is `4.0.0_SA_CRO~X`'s). No card outside this partition. No fetch (availability is not authorization).

## REPORT

To `2.0.0_SA_COO~X` (cc `3.0.0_SA_CVO~X`): the proof_of_spec instance at the path above, the per-card triple lines, the census with denominators, the validator line, the clean-clone line, commit hashes with push state measured.
