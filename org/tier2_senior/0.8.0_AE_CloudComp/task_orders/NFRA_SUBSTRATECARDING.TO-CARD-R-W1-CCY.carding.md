<task_order>
<id>NFRA_SUBSTRATECARDING.TO-CARD-R-W1-CCY</id>
<status>pending</status>
<assigned_to>0.8.0_AE_CloudComp~Y</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_SUBSTRATECARDING</project>
<issued_date>2026-08-30</issued_date>

<carrier>Design-lane RELEASE 1.0.0_SA_CTO~X 84224 (2026-08-30 01:57Z) on the certified 18 cells @3f88172e4d + SCORE 0c88005136 + joint certification (CRO~X 015348Z, CVO~X 015421Z); shape ruling 81777/81015 (re-card, never migrate; card files, never a key on the cells carrier); census @9b2c687dc8. STOP: this face is cut from CERTIFIED cells only.</carrier>

<sequenced_after>NFRA_C3MATERIALIZE.TO-L3W3-CCY ACCEPTED at this seat (Rule 27: one instance, one project at a time); and the TO-CARD-R-AE load-bearing gate</sequenced_after>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260829T1129Z/rectangle.final.certified.json @603f5546dc

cells:
CARD-R-b7dd-1 CARD-R-b7dd-2 CARD-R-b7dd-3 CARD-R-b7dd-4
partition: the 18 certified cells are three CLASS cell sets + 5 issuer mechanism cells; this face carries the wave1_rungs class (4 cells) scoped to the 3 subject(s) below, whose owner resolves to 0.8.0_AE_CloudComp~Y. Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism CARD-R-m-1 CARD-R-m-2 CARD-R-m-3 CARD-R-m-4 CARD-R-m-5.

<owned_cells>
CARD-R-b7dd-1 CARD-R-b7dd-2 CARD-R-b7dd-3 CARD-R-b7dd-4
</owned_cells>
</decomp_ref>

<subjects basis="enumerated FROM the census @9b2c687dc8; owner the v1 card's git creator (b7dd-3: the lane that authored the rung)">
  RECONCILE these against the census at its pin before writing anything; a set that does not reconcile is a REFUSAL for a ruling, never a rounding (b7dd-1, f9fa-3). Print the count beside its denominator on every receipt.
  <subject id="D1_value_grain" path="org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/D1.json" creator="0.8.0_AE_CloudComp~Y" />
  <subject id="D2_path_flow" path="org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/D2.json" creator="0.8.0_AE_CloudComp~Y" />
  <subject id="D3_contract_obligation" path="org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS/D3.json" creator="0.8.0_AE_CloudComp~Y" />
</subjects>

<sequence_gates>after-wave3-seating -- a gated cell may be PREPARED, but its value is written only after the gate's receipt is cited in its evidence. after-wave3-seating is SATISFIED (L3W3 faces cut @b8c47d1233, seated 02:0xZ); the owner rule (b7dd-3) binds this face to the rung's author, which is this seat.</sequence_gates>

<proof_of_spec>
  <criterion id="W1-CCY-AC1" cell_refs="CARD-R-b7dd-1">
    <label>wave1_rungs.scope_and_denominator</label>
    <oracle>Exactly the 8 wave-1 rungs still at schema v1, ENUMERATED FROM the census @9b2c687dc8 and not from any list retyped by the issuer. Print the 8 against the census's own denominator; a set that does not reconcile with the census is a REFUSAL, not a rounding.</oracle>
  </criterion>
  <criterion id="W1-CCY-AC2" cell_refs="CARD-R-b7dd-2">
    <label>wave1_rungs.recard_not_migrate</label>
    <oracle>Each of the 8 is RE-CARDED at v3.1 BY ITS OWNING LANE as an ordinary card. STOP: NO v1->v3.1 MIGRATOR. A migrator would manufacture key_expression, basis and provenance values that v1 never asked its author for -- a value with no measurement behind it, carrying the authority of a schema-conformant field. The whole point of the qualification is that a human named the key expression; a tool inventing one defeats it.</oracle>
  </criterion>
  <criterion id="W1-CCY-AC3" cell_refs="CARD-R-b7dd-3">
    <label>wave1_rungs.owner_per_card</label>
    <oracle>Every card names its OWNING LANE, and the owner is the lane that authored the v1 rung -- not whichever lane is free. A card whose owner did not write the subject cannot answer questions 5, 6 and 7 (coverage, key space, failure mode), which are the ones that draw blood.</oracle>
  </criterion>
  <criterion id="W1-CCY-AC4" cell_refs="CARD-R-b7dd-4">
    <label>wave1_rungs.acceptance</label>
    <oracle>8 of 8 at v3.1, each validating against SUBSTRATE_CARD.v3.1, with key_expression carrying basis measured|held|absent as the schema narrows it. The receipt prints 8 and its denominator; a partial set is reported as partial and never as complete.</oracle>
  </criterion>
</proof_of_spec>

<artifacts_contract>
  Every card is a FILE validating against SUBSTRATE_CARD.v3.1 (org/standards/SUBSTRATE_CARD.v3.1.schema.json -- schema_version const 3.1; NOT SUBSTRATE_CARD.schema.json, which is the legacy v1 contract, const 1), one carrier per qualification, authored by a lane that READ the subject (never generated). Every artifacts_produced row carries commit_or_etag as a resolvable git hex or sha256:<64 hex>, or the EXACT sentinel PENDING-THIS-COMMIT; prose refused. Proofs cite file:line @ commit-ish; every count prints what it is a count of (m-5). Tool runs bound to this TO via comp-to.
</artifacts_contract>
</task_order>
