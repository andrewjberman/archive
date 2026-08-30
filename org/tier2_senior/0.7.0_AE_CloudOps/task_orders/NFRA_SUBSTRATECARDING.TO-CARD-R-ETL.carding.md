<task_order>
<id>NFRA_SUBSTRATECARDING.TO-CARD-R-ETL</id>
<status>pending</status>
<assigned_to>0.7.0_AE_CloudOps~K</assigned_to>
<issued_by>2.0.0_SA_COO~X</issued_by>
<project>NFRA_SUBSTRATECARDING</project>
<issued_date>2026-08-30</issued_date>

<carrier>Design-lane RELEASE 1.0.0_SA_CTO~X 84224 (2026-08-30 01:57Z) on the certified 18 cells @3f88172e4d + SCORE 0c88005136 + joint certification (CRO~X 015348Z, CVO~X 015421Z); shape ruling 81777/81015 (re-card, never migrate; card files, never a key on the cells carrier); census @9b2c687dc8. STOP: this face is cut from CERTIFIED cells only.</carrier>

<sequenced_after>NFRA_SUBSTRATECARDING.TO-CARD-R-AE (the load-bearing-two-first gate: derive_stitch.py + kuzu_nessie_load.py cards landed + verified); and, at a seat holding an open NFRA_C3MATERIALIZE L3W3 face, that face's ACCEPTED (Rule 27: one instance, one project at a time)</sequenced_after>

<decomp_ref>
workflows/atom_decomposition/runs/nfra-substratecarding/20260829T1129Z/rectangle.final.certified.json @603f5546dc

cells:
CARD-R-0961-1 CARD-R-0961-2 CARD-R-0961-3 CARD-R-0961-4 CARD-R-0961-5
partition: the 18 certified cells are three CLASS cell sets + 5 issuer mechanism cells; this face carries the uncarded_20 class (5 cells) scoped to the 4 subject(s) below, whose owner resolves to 0.7.0_AE_CloudOps~K. Present on this face, DISCHARGED BY THE ISSUER (not owned here): mechanism CARD-R-m-1 CARD-R-m-2 CARD-R-m-3 CARD-R-m-4 CARD-R-m-5.

<owned_cells>
CARD-R-0961-1 CARD-R-0961-2 CARD-R-0961-3 CARD-R-0961-4 CARD-R-0961-5
</owned_cells>
</decomp_ref>

<subjects basis="enumerated FROM the census @9b2c687dc8; owner the fabric's declared owner (.owned-paths.yaml) refined by the git creator's family; routing reason: AE class owner; 0.5.0_AE_OpalETL created the 4 cse_emit_* writers but has NO live instance and the cap is 20/20; routed to the same AE seat as the load-bearing face, SEQUENCED AFTER it">
  RECONCILE these against the census at its pin before writing anything; a set that does not reconcile is a REFUSAL for a ruling, never a rounding (b7dd-1, f9fa-3). Print the count beside its denominator on every receipt.
  <subject id="infra/aws/globgrph/cse_emit_agent.py" path="infra/aws/globgrph/cse_emit_agent.py" creator="0.5.0_AE_OpalETL" />
  <subject id="infra/aws/globgrph/cse_emit_deploy.py" path="infra/aws/globgrph/cse_emit_deploy.py" creator="0.5.0_AE_OpalETL" />
  <subject id="infra/aws/globgrph/cse_emit_graphhead.py" path="infra/aws/globgrph/cse_emit_graphhead.py" creator="0.5.0_AE_OpalETL" />
  <subject id="infra/aws/globgrph/cse_emit_promote.py" path="infra/aws/globgrph/cse_emit_promote.py" creator="0.5.0_AE_OpalETL" />
</subjects>

<sequence_gates>load-bearing-two-first -- a gated cell may be PREPARED, but its value is written only after the gate's receipt is cited in its evidence. Gated on the AE face's two load-bearing cards (0961-1).</sequence_gates>

<proof_of_spec>
  <criterion id="ETL-AC1">
    <cell_refs>CARD-R-0961-1</cell_refs>
    <label>uncarded_20.load_bearing_first</label>
    <oracle>derive_stitch.py and kuzu_nessie_load.py are carded FIRST and their cards are the gate on the rest. derive_stitch.py writes stitch_graph.json, which is view 2's source in NFRA_C3MATERIALIZE; kuzu_nessie_load.py is the canonical projection loader. Both are load-bearing for a project currently running experiments ON their output, so an uncarded failure mode there is the most expensive one in the estate.</oracle>
  </criterion>
  <criterion id="ETL-AC2">
    <cell_refs>CARD-R-0961-2</cell_refs>
    <label>uncarded_20.scope_and_denominator</label>
    <oracle>The 20 resolvable uncarded subjects (19 manifest writers + rebuild.tmp.SET) enumerated FROM the census @9b2c687dc8. Print 20 with its denominator on every receipt. rebuild.tmp.SET is named explicitly because a subject that looks like a temp artifact is exactly the one a reader silently drops.</oracle>
  </criterion>
  <criterion id="ETL-AC3">
    <cell_refs>CARD-R-0961-3</cell_refs>
    <label>uncarded_20.substrate_test_in_full</label>
    <oracle>Each card answers all 7 questions across the 3 grains -- and 5, 6 and 7 (coverage + denominator, key/identity space, failure mode distinguishable from a genuine negative) are the ones that get skipped and the ones that matter. A card that answers 1-4 and hand-waves 5-7 is not a card.</oracle>
  </criterion>
  <criterion id="ETL-AC4">
    <cell_refs>CARD-R-0961-4</cell_refs>
    <label>uncarded_20.no_card_without_a_reading</label>
    <oracle>A card is written by someone who READ the subject, never generated from its manifest entry. STOP: a generated card is a description that has never been compared with the thing it describes -- the artifact-describes-itself defect, at scale, across 20 subjects.</oracle>
  </criterion>
  <criterion id="ETL-AC5">
    <cell_refs>CARD-R-0961-5</cell_refs>
    <label>uncarded_20.acceptance</label>
    <oracle>20 of 20 at v3.1 with the two load-bearing writers landed and verified first. Partial completion is reported with its numerator AND denominator; 'substantially complete' is not a state.</oracle>
  </criterion>
</proof_of_spec>

<artifacts_contract>
  Every card is a FILE validating against SUBSTRATE_CARD.v3.1 (org/standards/SUBSTRATE_CARD.schema.json), one carrier per qualification, authored by a lane that READ the subject (never generated). Every artifacts_produced row carries commit_or_etag as a resolvable git hex or sha256:<64 hex>, or the EXACT sentinel PENDING-THIS-COMMIT; prose refused. Proofs cite file:line @ commit-ish; every count prints what it is a count of (m-5). Tool runs bound to this TO via comp-to.
</artifacts_contract>
</task_order>
