<task_order>
<id>NFRA_SUBSTRATECARDING.TO-CARD-R-W4-COX</id>
<status>pending</status>
<assigned_to>0.7.0_AE_CloudOps~X</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_SUBSTRATECARDING</project>
<issued_date>2026-08-30</issued_date>

<carrier>Design-lane RELEASE 1.0.0_SA_CTO~X 84224 (2026-08-30 01:57Z) on the certified 18 cells @3f88172e4d + SCORE 0c88005136 + joint certification (CRO~X 015348Z, CVO~X 015421Z); shape ruling 81777/81015 (re-card, never migrate; card files, never a key on the cells carrier); census @9b2c687dc8. STOP: this face is cut from CERTIFIED cells only.</carrier>

<sequenced_after>NFRA_C3MATERIALIZE.TO-L3W3-COX ACCEPTED at this seat (Rule 27); and the TO-CARD-R-AE load-bearing gate</sequenced_after>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260829T1129Z/rectangle.final.certified.json @603f5546dc

cells:
CARD-R-f9fa-1 CARD-R-f9fa-2 CARD-R-f9fa-3 CARD-R-f9fa-4
partition: the 18 certified cells are three CLASS cell sets + 5 issuer mechanism cells; this face carries the w4_remote class (4 cells) scoped to the 7 subject(s) below, whose owner resolves to 0.7.0_AE_CloudOps~X. Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism CARD-R-m-1 CARD-R-m-2 CARD-R-m-3 CARD-R-m-4 CARD-R-m-5.

<owned_cells>
CARD-R-f9fa-1 CARD-R-f9fa-2 CARD-R-f9fa-3 CARD-R-f9fa-4
</owned_cells>
</decomp_ref>

<subjects basis="enumerated FROM the census @9b2c687dc8; owner the certified cell f9fa-2 names the seat; subjects = the census sec-2 cells-only list, reconciled against the carrier @a5fffa2bb7">
  RECONCILE these against the census at its pin before writing anything; a set that does not reconcile is a REFUSAL for a ruling, never a rounding (b7dd-1, f9fa-3). Print the count beside its denominator on every receipt.
  <subject id="code_heat_snap" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
  <subject id="cse" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
  <subject id="cse_test_24458e6c" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
  <subject id="cse_test_bb57a916" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
  <subject id="fedobs_coevolution_snap" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
  <subject id="fedobs_coverage_snap" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
  <subject id="ms_heat_snap" path="cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7" creator="0.7.0_AE_CloudOps~X" />
</subjects>

<sequence_gates>after-wave3-seating -- a gated cell may be PREPARED, but its value is written only after the gate's receipt is cited in its evidence. after-wave3-seating is SATISFIED; authorship follows the cells carrier's author (f9fa-2).</sequence_gates>

<proof_of_spec>
  <criterion id="W4-COX-AC1">
    <cell_refs>CARD-R-f9fa-1</cell_refs>
    <label>w4_remote.carrier_is_a_card_file</label>
    <oracle>The 7 wave-4 REMOTE subjects get CARD FILES under a D11_CARDS_W4 root. STOP: NO KEY FIELD BOLTED ONTO THE CELLS CARRIER. ONE CARRIER FOR THE QUALIFICATION -- a key living in a cells file and a key living in a card file are two carriers of one quantity, and they disagree silently the moment either is amended.</oracle>
  </criterion>
  <criterion id="W4-COX-AC2">
    <cell_refs>CARD-R-f9fa-2</cell_refs>
    <label>w4_remote.authorship</label>
    <oracle>0.7.0_AE_CloudOps~X authors them, as the author of the cells carrier (cells.0.7.0_AE_CloudOps~X.json @a5fffa2bb7). Authorship follows who measured the subject, not who has capacity.</oracle>
  </criterion>
  <criterion id="W4-COX-AC3">
    <cell_refs>CARD-R-f9fa-3</cell_refs>
    <label>w4_remote.scope_and_denominator</label>
    <oracle>Exactly the 7 enumerated FROM the census @9b2c687dc8, reconciled against the cells carrier's own membership. Print both counts; if the cells carrier and the census disagree, that disagreement is the finding and the cut stops for a ruling rather than picking the larger number.</oracle>
  </criterion>
  <criterion id="W4-COX-AC4">
    <cell_refs>CARD-R-f9fa-4</cell_refs>
    <label>w4_remote.acceptance</label>
    <oracle>7 of 7 card files, each validating against v3.1, each naming the cells carrier it qualifies. The cells carrier is NOT edited by this work.</oracle>
  </criterion>
</proof_of_spec>

<artifacts_contract>
  Every card is a FILE validating against SUBSTRATE_CARD.v3.1 (org/standards/SUBSTRATE_CARD.schema.json), one carrier per qualification, authored by a lane that READ the subject (never generated). Every artifacts_produced row carries commit_or_etag as a resolvable git hex or sha256:<64 hex>, or the EXACT sentinel PENDING-THIS-COMMIT; prose refused. Proofs cite file:line @ commit-ish; every count prints what it is a count of (m-5). Tool runs bound to this TO via comp-to.
</artifacts_contract>
</task_order>
