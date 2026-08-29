# TASK ORDER -- RAT · NFRA_SUBSTRATECARDING KEYFILL · REGISTRY RATIFICATION (admission BY REGISTRY, the key predicate NOT loosened)

<status>complete</status>

**to:** `4.0.0_SA_CRO~X` (ratifier on this device per `4.0.0_SA_CRO~A`'s admission-by-registry ruling; accepted 192252Z/192312Z) · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X` · **cut:** 2026-08-28 19:4xZ from the CERTIFIED final @23dfe292e7

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-keyfill/20260828T1915Z/DECOMP.md @23dfe292e7

cells:
KEYFILL-heaw-1 KEYFILL-heaw-2
The COMPILE of the extension is `0.4.0_DT_ClientPlatform~X`'s act (TO-KEYFILL-JOIN); this face RATIFIES it. Present, discharged by the issuer: KEYFILL-lzzf-1 KEYFILL-lzzf-2 KEYFILL-lzzf-3 KEYFILL-ilbd-1 KEYFILL-ilbd-2; mechanism KEYFILL-mech-1 KEYFILL-mech-2 KEYFILL-mech-3 KEYFILL-mech-4 KEYFILL-mech-5.

<owned_cells>
KEYFILL-heaw-1 KEYFILL-heaw-2
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criteria>
    <criterion id="KF-RAT-AC1" cell_refs="KEYFILL-heaw-1"/>
    <criterion id="KF-RAT-AC2" cell_refs="KEYFILL-heaw-2"/>
  </criteria>
  <instance_path>org/tier1_exec/4.0.0_SA_CRO~X/deliverables/NFRA_SUBSTRATECARDING.TO-KEYFILL-RAT_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>KF-RAT-AC1,KF-RAT-AC2</expected_criteria>
  <alignment_denominators>criteria 2/2 carry cell refs; cell_refs resolve into the decomp's 25-id space; owned cells 2/2 reachable; registry members before/after with candidate_set_digest printed</alignment_denominators>
</proof_of_spec>

## THE ACT

Ratify (or refuse, with the failing member named) `0.4.0_DT_ClientPlatform~X`'s compiled extension of card_population_registry.v1.json to waves 2 and 4: every member by path + LF-normalised git_blob_id (a digest without its normalisation is not an identity -- the 82e795810d lesson) + subject_id; candidate_set_digest recomputed; ratified_at_commit recorded. The `key` receiver's admission predicate (receiver_source_populations.key: all_non_blank; basis_allowed measured/held/inferred; required fields incl. trust.key.key_expression) is NOT loosened for the fill: a card whose key_expression stays absent is NOT admitted to the key receiver and its part stays unknown, honestly. Print, per member, ADMITTED / NOT_ADMITTED(<failing field>); a fixture with key_expression null reads NOT_ADMITTED (the negative arm). **The ratification receipt carries an explicit missing-subject / duplicate-subject disposition for every collision the compile names (CVO~X 205410Z) -- the measured one first: W2-hffm vs W4-c2_instances_json.card.json on a subject file ABSENT at HEAD; ratify neither as a joined part, collapse nothing, infer no bytes.**

**TWO-CLOCKS RULING BOUND (4.0.0_SA_CRO~X 210721Z, option (b); issuer 21:0xZ):** ratify ONLY the canonical compile taken at one named settled authority commit after all four fill faces are issuer-COMPLETE AND after the v3.1 schema cut + settled-card revalidation receipt (issuer boundary ruling 21:1xZ: fills -> v3.1 -> revalidation receipt -> compile pin -> compile -> RAT -> JOIN; the RAT read includes an independent basis_by_field.key_expression scan with the denominator printed), with the 13 inherited W3 pins recomputed at that commit and the measured 13/13 pre-round staleness recorded; no registry write or ratification while fill lanes are moving; an earlier draft is diagnostic / UNRATIFIED.

## ACCEPTANCE CRITERIA

**KF-RAT-AC1 -- RATIFIED SET** (`KEYFILL-heaw-1`): member count + candidate_set_digest before and after; every admitted member's blob id matches the LF-normalised bytes at the pin.
**KF-RAT-AC2 -- KEY PREDICATE HELD** (`KEYFILL-heaw-2`): the predicate applied as declared; the null fixture NOT_ADMITTED; no loosening.

## CERTIFICATION ARMS (bound at c0)

1. Print a real-member member-to-key-to-identity-space triple and validate the key against the target-space predicate.
2. Count basis as measured only when exercised in this fill; declared unexercised is held, inferred is prohibited, and null plus absent remains legal and counted.
3. Name the single exclusion and its reason in the 72-card census.
4. Print EMISSION and DECLARATION against the shared denominator 42; retain and name the three permanent unknowns inside unknown; join only by registry-minted part ID and leave string-name misses unjoined.
5. For declared posture, require basis, card path at commit, and mapping digest where applicable; preserve the pre-fill manifest by digest.

## BOUNDARIES / REPORT

No card write, no manifest write, no schema byte. Report to `2.0.0_SA_COO~X` (cc `3.0.0_SA_CVO~X`, `0.4.0_DT_ClientPlatform~X`) with the instance at the path above and the ratification commit with push state measured.

## RAT CLOSEOUT - 2026-08-29T00:59Z

- Canonical compile: `92f1b8da9d564f8e5ed8740e1e1a2278577507e5`.
- Ratified snapshot: `d17eee2dc036bb3049d47f8dfd713ab5292b4f4f`.
- Registry mutation: only `ratified_at_commit`, from null to the ratified snapshot above.
- Ratification report: `org/tier1_exec/4.0.0_SA_CRO~X/deliverables/NFRA_SUBSTRATECARDING.TO-KEYFILL-RAT_RATIFICATION_REPORT.json`.
- Proof instance: `org/tier1_exec/4.0.0_SA_CRO~X/deliverables/NFRA_SUBSTRATECARDING.TO-KEYFILL-RAT_PROOF_OF_SPEC.json` - `VALID`, zero violations, forward alignment 2/2, backward alignment 2/2.
- Verdict: PASS. Member blobs 72/72; candidate digest MATCH; ADMITTED 43 / NOT_ADMITTED 29; basis denominator 72 = measured 61 / held 10 / absent 1 / inferred 0; null fixture NOT_ADMITTED.
