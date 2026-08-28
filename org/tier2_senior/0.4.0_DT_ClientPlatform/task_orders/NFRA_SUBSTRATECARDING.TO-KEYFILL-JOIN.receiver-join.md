# TASK ORDER -- JOIN · NFRA_SUBSTRATECARDING KEYFILL · THE RECEIVER JOIN (manifest `key` receiver) + THE REGISTRY COMPILE HALF

<status>pending</status>

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X` · **ratifier of the registry:** `4.0.0_SA_CRO~X` (its own TO) · **cut:** 2026-08-28 19:4xZ from the CERTIFIED final @23dfe292e7
**sequencing:** runs AFTER the four lane fill TOs report (KEYFILL-DTX/COX/CCX/CCY) and after `4.0.0_SA_CRO~X` ratifies the registry extension; the join admits ONLY registry-ratified members. This lane also holds its own fill TO (KEYFILL-DTX) -- same project, Rule 27 satisfied.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding-keyfill/20260828T1915Z/DECOMP.md @23dfe292e7

cells:
KEYFILL-rcgx-1 KEYFILL-rcgx-2 KEYFILL-rcgx-3 KEYFILL-rcgx-4
compile half (owned by this lane as compiler, ratified by 4.0.0_SA_CRO~X on its face): the registry v1 extension by path + git_blob_id (LF-normalised) + subject_id with a recomputed candidate_set_digest -- the ACT is here, the RATIFICATION is KEYFILL-heaw-1 KEYFILL-heaw-2 on 4.0.0_SA_CRO~X's face. Present, discharged by the issuer: KEYFILL-lzzf-1 KEYFILL-lzzf-2 KEYFILL-lzzf-3 KEYFILL-ilbd-1 KEYFILL-ilbd-2; mechanism KEYFILL-mech-1 KEYFILL-mech-2 KEYFILL-mech-3 KEYFILL-mech-4 KEYFILL-mech-5.
</decomp_ref>

<owned_cells>
KEYFILL-rcgx-1 KEYFILL-rcgx-2 KEYFILL-rcgx-3 KEYFILL-rcgx-4
</owned_cells>

<proof_of_spec>
  <criteria>
    <criterion id="KF-JOIN-AC1" cell_refs="KEYFILL-rcgx-1"/>
    <criterion id="KF-JOIN-AC2" cell_refs="KEYFILL-rcgx-2, KEYFILL-rcgx-3"/>
    <criterion id="KF-JOIN-AC3" cell_refs="KEYFILL-rcgx-4"/>
  </criteria>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_SUBSTRATECARDING.TO-KEYFILL-JOIN_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>KF-JOIN-AC1,KF-JOIN-AC2,KF-JOIN-AC3</expected_criteria>
  <alignment_denominators>criteria 3/3 carry cell refs; cell_refs resolve into the decomp's 25-id space; owned cells 4/4 reachable; parts denominator = the manifest's part count (re-derived; 42 at cut)</alignment_denominators>
</proof_of_spec>

## THE ACT

1. COMPILE the registry extension for waves 2 and 4 in the registry's own form (path + LF-normalised git_blob_id + subject_id; candidate_set_digest recomputed and printed before/after) and hand it to `4.0.0_SA_CRO~X` for ratification at a recorded commit -- the population at cut: 0.4.0_DT_ClientPlatform~X 18, 0.7.0_AE_CloudOps~X 11, 0.8.0_AE_CloudComp~X 30, 0.8.0_AE_CloudComp~Y 13 = 72 v3 cards.
2. After ratification and the lane fills: for every manifest part, JOIN by the registry's MINTED part id (never a name or a path); a part whose registry-admitted card resolves 1:1 and passes the registry's `key` admission predicate (all_non_blank; basis measured/held/inferred; `trust.key.key_expression` required) takes `key.claim_status = declared`, `key.key_expression` from the card, basis + evidence (card path @ its commit) + owner carried, and the mapping digest where a mapping applies; a part with no admitted card, two candidate cards, or a string-name miss stays `unknown` and is PRINTED as such (unjoined / ambiguous / no card) -- nothing is invented.
3. Print EMISSION and DECLARATION against the SAME parts denominator, side by side, never summarised: EMISSION = parts carrying all four receivers with a coherent claim_status; DECLARATION = declared / unknown, with the three permanently-unknown-by-construction parts (affinity_matrix, identity_and_succession, similarity_network_fusion) counted INSIDE unknown and NAMED there, never subtracted, never listed as outstanding.
4. Preserve the pre-fill manifest digest-addressed under D11_MANIFEST/preserved/ BEFORE the pass; validate the re-emitted manifest against L0_GRAPH_SUBSTRATE_MANIFEST.schema.json (every key receiver's required fields present on every part); PASS printed with the parts denominator.

## ACCEPTANCE CRITERIA

**KF-JOIN-AC1 -- ONE-TO-ONE BY MINTED ID, NOTHING INVENTED** (`KEYFILL-rcgx-1`): per-part join line (card or no card / ambiguous / unjoined); admission strictly by the ratified registry + the key predicate.
**KF-JOIN-AC2 -- TWO NUMBERS, PERMANENT UNKNOWNS INSIDE** (`KEYFILL-rcgx-2`, `KEYFILL-rcgx-3`): EMISSION and DECLARATION printed against one denominator; the three by-construction parts named inside unknown.
**KF-JOIN-AC3 -- RECEIVER VALID, PRE-FILL PRESERVED** (`KEYFILL-rcgx-4`): L0 validation PASS with the denominator; the pre-fill manifest preserved by digest and cited.

## CERTIFICATION ARMS (bound at c0)

1. Print a real-member member-to-key-to-identity-space triple and validate the key against the target-space predicate.
2. Count basis as measured only when exercised in this fill; declared unexercised is held, inferred is prohibited, and null plus absent remains legal and counted.
3. Name the single exclusion and its reason in the 72-card census.
4. Print EMISSION and DECLARATION against the shared denominator 42; retain and name the three permanent unknowns inside unknown; join only by registry-minted part ID and leave string-name misses unjoined.
5. For declared posture, require basis, card path at commit, and mapping digest where applicable; preserve the pre-fill manifest by digest.

## LANE / BOUNDARIES / REPORT

D11_MANIFEST is this lane's own deliverables dir. No card write on this face (the fills are the lane TOs); no registry RATIFICATION here (the compile is handed to `4.0.0_SA_CRO~X`); no schema byte. Report to `2.0.0_SA_COO~X` (cc `3.0.0_SA_CVO~X`, `4.0.0_SA_CRO~X`) with the instance at the path above, the join lines, both numbers, the preserved digest, commit hashes with push state measured.
