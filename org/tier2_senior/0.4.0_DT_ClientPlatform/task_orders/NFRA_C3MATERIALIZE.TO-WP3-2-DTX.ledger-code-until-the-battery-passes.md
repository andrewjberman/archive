# TASK ORDER -- WP3-2 (DTX) · NFRA_C3MATERIALIZE L4 / WP-3 THE IDENTITY LEDGER · WAVE 2: THE LEDGER CODE, UNTIL THE BATTERY PASSES FROM A CLEAN CLONE

<status>pending -- cut 2026-08-28 10:4xZ by 2.0.0_SA_COO~X on wave 1's MEASURED completion (8a01dda9ba + ca919d1b09; CVO~X VERIFIED COMPLETE 104041Z); GO on delivery</status>

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X`
**scope:** 36 entities / 130 cells (124 lane + 6 issuer-owned mechanism cells discharged by AC9 evidence) · **contract implemented:** `v0.3-candidate+27` FROZEN schema-only at `d0398b977d` (`bundle:sha256:87ed70800607dbc46c1d6529eea7e551252673b1f26cc1500592fb71ee978abc`)
**project:** `NFRA_C3MATERIALIZE` (directive D11) · **dep_stage:** EXECUTING · **prerequisite (OBSERVED):** TO-WP3-1-DTX complete -- manifest `org/standards/isck/ledger/battery/MANIFEST.json` @8a01dda9ba (190 arm ids, 13 rows, sha256 0a960d5a...), runner `run_battery.py` built (`ran 0 of 190 -- COUNTED; verdict WITHHELD (exit 3)`), engine = single-file SQLite local to the owning device (`ledger/ENGINE_CHOICE.md`)

✅ **DECOMP CERTIFIED** -- PASS @7cbefad614 + addendum @be2564a76f (`3.0.0_SA_CVO~X`); consumable `rectangle.final.certified.json` (sha256 `2776f110...`), face index gated by `check_cell_index.py` @af69d18511.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-wp3/20260828T0938Z/DECOMP.md
rectangle: workflows/atom_decomposition/runs/nfra-c3materialize-wp3/20260828T0938Z/rectangle.final.certified.json -- vintage 540503df0a (the certified dry is byte-identical to c0 at that hash); cite @540503df0a in every AC evidence line

cells (130 of 168 -- 124 lane + 6 issuer-owned mechanism); the 13 `-3` cells are RE-CLAIMED from wave 1 for promote-or-kill (AC7):
plane 1, rows 1-13      *-3 (carrier_dependency, INFERRED -> MEASURED or KILLED)  *-4 (battery_state)  *-5 (clean_clone_result)
clean_clone_runner      WP3-pntm-3 (exercised -- wave 1 left it UNMEASURED by design)
admission_batch         WP3-ecrq-1..4        reference_resolver   WP3-znga-1..4        commit_seq_envelope  WP3-pcio-1..4
machine_binding         WP3-ifbx-1..4        machine_authority_epoch WP3-wbbm-1..4     machine_materializer_lifecycle WP3-zhlw-1..4
machine_contest         WP3-tuum-1..4        voided_derivation    WP3-xyqo-1..4
fold_entity_status      WP3-fhfd-1..4        fold_binding_status  WP3-fqmh-1..4        fold_verification_standing WP3-ecgr-1..4
fold_materializer_status WP3-owuo-1..4       head_materializer_version WP3-mxsr-1..4   head_surface_authority WP3-rnbr-1..4
surface_resolve         WP3-kaoh-1..4        surface_binding_history WP3-stcb-1..4     surface_provenance   WP3-yjyp-1..4
surface_why             WP3-cibm-1..4        surface_coherence    WP3-iiqb-1..4        surface_replay       WP3-rjvp-1..4
receipt_carrier         WP3-mjyb-1..4
issuer-owned mechanism  WP3-mech-1 WP3-mech-2 WP3-mech-3 WP3-mech-5 WP3-mech-6 WP3-mech-7

<owned_cells>
WP3-njzv-3 WP3-njzv-4 WP3-njzv-5 WP3-adtv-3 WP3-adtv-4 WP3-adtv-5 WP3-fyhc-3 WP3-fyhc-4 WP3-fyhc-5
WP3-dlnv-3 WP3-dlnv-4 WP3-dlnv-5 WP3-smto-3 WP3-smto-4 WP3-smto-5 WP3-wouj-3 WP3-wouj-4 WP3-wouj-5
WP3-ahtf-3 WP3-ahtf-4 WP3-ahtf-5 WP3-uaew-3 WP3-uaew-4 WP3-uaew-5 WP3-kano-3 WP3-kano-4 WP3-kano-5
WP3-uzkn-3 WP3-uzkn-4 WP3-uzkn-5 WP3-cshq-3 WP3-cshq-4 WP3-cshq-5 WP3-pzfg-3 WP3-pzfg-4 WP3-pzfg-5
WP3-oqse-3 WP3-oqse-4 WP3-oqse-5
WP3-pntm-3
WP3-ecrq-1 WP3-ecrq-2 WP3-ecrq-3 WP3-ecrq-4 WP3-znga-1 WP3-znga-2 WP3-znga-3 WP3-znga-4
WP3-pcio-1 WP3-pcio-2 WP3-pcio-3 WP3-pcio-4 WP3-xyqo-1 WP3-xyqo-2 WP3-xyqo-3 WP3-xyqo-4
WP3-ifbx-1 WP3-ifbx-2 WP3-ifbx-3 WP3-ifbx-4 WP3-wbbm-1 WP3-wbbm-2 WP3-wbbm-3 WP3-wbbm-4
WP3-zhlw-1 WP3-zhlw-2 WP3-zhlw-3 WP3-zhlw-4 WP3-tuum-1 WP3-tuum-2 WP3-tuum-3 WP3-tuum-4
WP3-fhfd-1 WP3-fhfd-2 WP3-fhfd-3 WP3-fhfd-4 WP3-fqmh-1 WP3-fqmh-2 WP3-fqmh-3 WP3-fqmh-4
WP3-ecgr-1 WP3-ecgr-2 WP3-ecgr-3 WP3-ecgr-4 WP3-owuo-1 WP3-owuo-2 WP3-owuo-3 WP3-owuo-4
WP3-mxsr-1 WP3-mxsr-2 WP3-mxsr-3 WP3-mxsr-4 WP3-rnbr-1 WP3-rnbr-2 WP3-rnbr-3 WP3-rnbr-4
WP3-kaoh-1 WP3-kaoh-2 WP3-kaoh-3 WP3-kaoh-4 WP3-stcb-1 WP3-stcb-2 WP3-stcb-3 WP3-stcb-4
WP3-yjyp-1 WP3-yjyp-2 WP3-yjyp-3 WP3-yjyp-4 WP3-cibm-1 WP3-cibm-2 WP3-cibm-3 WP3-cibm-4
WP3-iiqb-1 WP3-iiqb-2 WP3-iiqb-3 WP3-iiqb-4 WP3-rjvp-1 WP3-rjvp-2 WP3-rjvp-3 WP3-rjvp-4
WP3-mjyb-1 WP3-mjyb-2 WP3-mjyb-3 WP3-mjyb-4
WP3-mech-1 WP3-mech-2 WP3-mech-3 WP3-mech-5 WP3-mech-6 WP3-mech-7
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="WP3-2-AC1" cell_refs="WP3-ecrq-1, WP3-ecrq-2, WP3-ecrq-3, WP3-ecrq-4, WP3-pcio-1, WP3-pcio-2, WP3-pcio-3, WP3-pcio-4, WP3-njzv-4, WP3-njzv-5, WP3-fyhc-4, WP3-fyhc-5, WP3-pzfg-4, WP3-pzfg-5"/>
  <criterion id="WP3-2-AC2" cell_refs="WP3-znga-1, WP3-znga-2, WP3-znga-3, WP3-znga-4, WP3-adtv-4, WP3-adtv-5"/>
  <criterion id="WP3-2-AC3" cell_refs="WP3-ifbx-1, WP3-ifbx-2, WP3-ifbx-3, WP3-ifbx-4, WP3-wbbm-1, WP3-wbbm-2, WP3-wbbm-3, WP3-wbbm-4, WP3-zhlw-1, WP3-zhlw-2, WP3-zhlw-3, WP3-zhlw-4, WP3-tuum-1, WP3-tuum-2, WP3-tuum-3, WP3-tuum-4, WP3-xyqo-1, WP3-xyqo-2, WP3-xyqo-3, WP3-xyqo-4, WP3-dlnv-4, WP3-dlnv-5, WP3-wouj-4, WP3-wouj-5, WP3-ahtf-4, WP3-ahtf-5, WP3-oqse-4, WP3-oqse-5"/>
  <criterion id="WP3-2-AC4" cell_refs="WP3-fhfd-1, WP3-fhfd-2, WP3-fhfd-3, WP3-fhfd-4, WP3-fqmh-1, WP3-fqmh-2, WP3-fqmh-3, WP3-fqmh-4, WP3-ecgr-1, WP3-ecgr-2, WP3-ecgr-3, WP3-ecgr-4, WP3-owuo-1, WP3-owuo-2, WP3-owuo-3, WP3-owuo-4, WP3-mxsr-1, WP3-mxsr-2, WP3-mxsr-3, WP3-mxsr-4, WP3-rnbr-1, WP3-rnbr-2, WP3-rnbr-3, WP3-rnbr-4, WP3-smto-4, WP3-smto-5, WP3-cshq-4, WP3-cshq-5"/>
  <criterion id="WP3-2-AC5" cell_refs="WP3-kaoh-1, WP3-kaoh-2, WP3-kaoh-3, WP3-kaoh-4, WP3-stcb-1, WP3-stcb-2, WP3-stcb-3, WP3-stcb-4, WP3-yjyp-1, WP3-yjyp-2, WP3-yjyp-3, WP3-yjyp-4, WP3-cibm-1, WP3-cibm-2, WP3-cibm-3, WP3-cibm-4, WP3-iiqb-1, WP3-iiqb-2, WP3-iiqb-3, WP3-iiqb-4, WP3-rjvp-1, WP3-rjvp-2, WP3-rjvp-3, WP3-rjvp-4, WP3-uaew-4, WP3-uaew-5, WP3-kano-4, WP3-kano-5, WP3-uzkn-4, WP3-uzkn-5"/>
  <criterion id="WP3-2-AC6" cell_refs="WP3-pntm-3, WP3-njzv-4, WP3-njzv-5, WP3-adtv-4, WP3-adtv-5, WP3-fyhc-4, WP3-fyhc-5, WP3-dlnv-4, WP3-dlnv-5, WP3-smto-4, WP3-smto-5, WP3-wouj-4, WP3-wouj-5, WP3-ahtf-4, WP3-ahtf-5, WP3-uaew-4, WP3-uaew-5, WP3-kano-4, WP3-kano-5, WP3-uzkn-4, WP3-uzkn-5, WP3-cshq-4, WP3-cshq-5, WP3-pzfg-4, WP3-pzfg-5, WP3-oqse-4, WP3-oqse-5"/>
  <criterion id="WP3-2-AC7" cell_refs="WP3-njzv-3, WP3-adtv-3, WP3-fyhc-3, WP3-dlnv-3, WP3-smto-3, WP3-wouj-3, WP3-ahtf-3, WP3-uaew-3, WP3-kano-3, WP3-uzkn-3, WP3-cshq-3, WP3-pzfg-3, WP3-oqse-3"/>
  <criterion id="WP3-2-AC8" cell_refs="WP3-mjyb-1, WP3-mjyb-2, WP3-mjyb-3, WP3-mjyb-4, WP3-mech-6"/>
  <criterion id="WP3-2-AC9" cell_refs="WP3-mech-1, WP3-mech-2, WP3-mech-3, WP3-mech-5, WP3-mech-7"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_C3MATERIALIZE.TO-WP3-2-DTX_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>WP3-2-AC1,WP3-2-AC2,WP3-2-AC3,WP3-2-AC4,WP3-2-AC5,WP3-2-AC6,WP3-2-AC7,WP3-2-AC8,WP3-2-AC9</expected_criteria>
  <alignment_denominators>criteria: 9. Cells: 130 of 168 in the decomp -- 124 proposed to this executor + 6 issuer-owned mechanism cells discharged by AC8/AC9 evidence; all 130 covered by >= 1 criterion (the 26 -4/-5 cells are cited by their component AC and by AC6, deliberately: AC6 is the sec-3 completion evidence and the component ACs are its parts). Unmapped 0; untraceable 0. The 38 cells not claimed here are wave 1's (complete @8a01dda9ba + ca919d1b09).</alignment_denominators>
</proof_of_spec>

---

## AUTHORITY

Design sec 7, the step after the battery: *"ledger code until the battery passes from a clean clone"*, then the receipt. Wave 1's MEASURED completion is the trigger (Stage-3 OBSERVED-completion rule): commit 1 @8a01dda9ba (six battery files under the fourth singular override, CTO~X 77670/77671), commit 2 @ca919d1b09 (instance VALID 0 violations, 53/53 both directions), `3.0.0_SA_CVO~X` VERIFIED COMPLETE 104041Z with an independent replay of every control. **WP-3 completes on this battery passing from a clean clone of the pinned commit, not on code delivery** (sec 3) -- AC6 is the wave's completion evidence; the component ACs are its parts.

## THE INPUT, READ AT SOURCE

`org/standards/isck/WP3_LEDGER_DESIGN.md @ d0398b977d` sec 2c (admission), 2d (the 30 reference rows), 2e (commit_seq envelope + anchors), 3 (the thirteen rows -- every arm id is in the manifest already), 4 (fold tables + HEAD selection + the EFFECTIVE-event machines), 5 (six surfaces), 7 (receipt carrier); `ISCK_CONTRACT.v0.schema.json` + `validate_isck.py` at the same pin for record validation; sec 3b @55a20db49e for AC7's prior. **The ledger IMPLEMENTS the pinned model; it does not revise it** (sec 0, WP3-mech-1): a contract defect found while building is a finding to the issuer for a NEW candidate, never a ledger-side workaround.

## ORDER OF WORK -- the rectangle's `depends_on` edges, not a date

`engine_choice` (done) -> `admission_batch` + `commit_seq_envelope` -> `reference_resolver` -> the four machines -> `voided_derivation` (needs `machine_contest`) -> folds + HEADs -> surfaces -> `receipt_carrier` (needs the runner PASS). Land in that order, committing per unit; cell-level status is the record (partial completion is expressible), and every commit runs the battery -- the arm counts that turn from WITHHELD to PASS are the progress signal, nothing else is.

## ACCEPTANCE CRITERIA (each cites the cells it discharges)

| id | criterion | cells |
|---|---|---|
| **WP3-2-AC1** | **STORE + ADMISSION + ENVELOPE.** The SQLite store per `ENGINE_CHOICE.md`; a WRITE is an atomic BATCH validated at FINAL STATE against (store U batch) (sec 2c) -- the bootstrap pair `{mint_receipt, entity}` admits in either order, an orphan entity is REJECTED; every admitted batch gets a strictly increasing `commit_seq` in the ENVELOPE, never a record field (sec 2e); anchors `as_of publication | frontier | commit_seq` bind to a commit_seq and cut the replay set; a backfilled earlier-dated record is EXCLUDED before its anchor and INCLUDED at event-time after. Arms: L-06-bootstrap-pair-accepted, L-06-orphan-entity-rejected, L-02-forward-ref-within-batch-accepted, L-02-unresolved-at-final-state-rejected, L-01-*, L-03-*, L-12-*. `built: PRESENT`, `exercised: PASS`, `failure_mode` written per unit. | admission_batch, commit_seq_envelope; rows 1, 3, 12 `-4/-5` |
| **WP3-2-AC2** | **THE RESOLVER.** Every one of sec 2d's 30 reference rows enforced by policy (STRICT / STRICT-CONDITIONAL / PARSE-STRICT; the 21 EXTERNAL never resolved); both arms per row exist in the manifest already -- `L-02-unresolved-<record>.<field>` x30 REJECT and `L-02-resolved-<record>.<field>-accepted` x30 ACCEPT, plus `L-02-opaque-migration-ref-accepted`. A resolver that stores a dangling reference does not error -- name the observable that catches it. | reference_resolver; row 2 `-4/-5` |
| **WP3-2-AC3** | **THE FOUR EFFECTIVE-EVENT MACHINES + VOIDED.** Per `binding_id` (row 4), per `authority_id` TOTAL machine with admission-time authorization and actor bound to the authenticated writer (row 6, R4-CRO-6: the schema regex is the structural half, the ledger binds `actor` to the submitting seat BEFORE the family predicate), per materializer lifecycle -- linear chain, single root, single effective supersession, decommission TERMINAL (row 7), per `contest_id` with one corrective slot per event target (row 13); VOIDED = target of an admitted upheld-with-replacement OR nullified contest, advances no machine, feeds no fold (item 8). Every reject AND accept arm in rows 4, 6, 7, 13. | 4 machines, voided_derivation; rows 4, 6, 7, 13 `-4/-5` |
| **WP3-2-AC4** | **FOLDS + HEADS.** The four derivation tables of sec 4 as FUNCTIONS -- top-down precedence, pairwise-overlap controls and the default control per table; authoritative records stay `authored` and an authored value on a derivable axis that disagrees with the fold is REJECTED; the projection object is NOT a record (fails +38 by construction). HEAD selection: unique materializer_version head (`failure_state: no_versions`), surface authority by `(published_at DESC, commit_seq DESC, surface_version_id DESC)` with `tie_broken_by` printed. Arms: L-05-*, L-11-*. | 4 folds, 2 HEADs; rows 5, 11 `-4/-5` |
| **WP3-2-AC5** | **THE SIX QUERY SURFACES** of sec 5 with their evidence shapes -- `resolve` (zero/one/many, never a silent one), `binding_history`, `surface_provenance`, `why` (the status_basis records), `coherence` (five separate axes, never collapsed), `replay` (returns `anchor_commit_seq` beside the estate). Write-then-query fixtures per surface; rows 8, 9, 10, 12's arms pass. | 6 surfaces; rows 8, 9, 10, 12 `-4/-5` |
| **WP3-2-AC6** | **THE BATTERY PASSES FROM A CLEAN CLONE -- the completion evidence.** `run_battery.py` on a FRESH clone of the EXPLICIT build `run_commit` (never the manifest's census vintage) prints `ran N of N` by COUNTING -- N = the manifest's distinct ARM count as the runner counts it (a token cited in two rows is ONE arm; by derivation 188 after the row-2 + row-5 template expansion, with 190 row-citations printed beside it; the runner's number wins over any number written here) -- exit 0: every reject arm REJECTED, every accept arm ACCEPTED, per row. ~~`ran 190 of 190`~~ stood here at the cut: the issuer's own typed count (WP3-mech-3), amended 10:5xZ on CVO~X's 105059Z correction. Falsifiers reported with this AC: an ACCEPT-EVERYTHING engine drives every reject arm into `wrong`; an EMPTY `engine.py` is not a pass; an absent/unresolvable `run_commit` FAILS CLOSED (a distinct exit, not 3 and not 0). `clean_clone_result: PASS` x13 with the run commit named; `battery_state: COMPLETE` x13 (every census id in the manifest, runner count == manifest count); `clean_clone_runner.exercised: PASS`. **No typed count anywhere: quote the runner's own printed line.** A run from a working tree is not this value. | pntm-3; all `-4/-5` |
| **WP3-2-AC7** | **CARRIER PROMOTE-OR-KILL.** Each of the 13 `carrier_dependency` cells moves from INFERRED (sec 3b @55a20db49e) to MEASURED from the fixtures its row's arms construct (a fixture names its `record_type`): ~~PROMOTE when the fixtures' record_type set is a subset of sec 3b's row list; KILL when a fixture falls outside it~~ **AMENDED 12:1xZ (DT~X 77754; issuer ruling): the subset clause compared what a fixture CONSTRUCTS (scaffold included) with what a row is ABOUT -- two populations; its 12-of-13 KILL rate was a property of the instrument. RETIRED as non-decisive, not tuned. The measuring instrument is the carrier VERDICT: a store recording the record_type of every admission per arm, compared to sec 3b's per-row carrier; 13 of 13 AGREE @67f320c4c2 -> PROMOTED to MEASURED.** A KILL under a sound instrument would be a finding against sec 3b routed to `1.0.0_SA_CTO~X` cc the issuer, never a fixture edit to fit the prior. Evidence = the tool's printed per-row line at the run commit. | rows 1-13 `-3` |
| **WP3-2-AC8** | **THE RECEIPT, ONLY THROUGH THE CARRIER.** `wp3_certification_receipt` recorded on the frozen `+27` label via `bundle_identity.py --receipt <kind> --value <receipt commit> <commit>`, where the receipt commit CONTAINS the structured receipt at `org/standards/isck/receipts/<kind>.json` (`kind`, `candidate_id`, `contract_bundle_id`, `manifest_path`, `manifest_digest`, `result`, `evidence_digest`, `run_commit`); the validator's REFUSALS exercised -- a wrong kind, another bundle, a FAIL result, a digest mismatch each write NOTHING; `derive()` exposes the accepted receipt; BUNDLE_LABELS.json never hand-edited. | receipt_carrier; WP3-mech-6 |
| **WP3-2-AC9** | **BOUNDARIES, evidenced.** (mech-1/-7) no byte of the +27 members changed: `bundle_identity.py` member list INTERSECT `git diff --name-only d0398b977d <commit>` = empty, both denominators printed (the R4-DT-5 instrument); (mech-2) the manifest's commit 8a01dda9ba PRECEDES the first ledger-code commit -- `git merge-base --is-ancestor`; (mech-3) every quoted count cites the runner's printed line; (mech-5) FIXTURES ONLY -- zero production substrate reads or writes, positive control run as in wave 1. | WP3-mech-1, -2, -3, -5, -7 |

**Proof-of-spec:** a `proof-of-spec` instance at `<instance_path>` (bidirectional cell<->criterion mapping, denominators **130 cells / 9 criteria**, decomp vintage 540503df0a, `proof-of-spec-check.py` VALID) -- read `PROOF_OF_SPEC.schema.json`, not an example (wave 1's own lesson). Delivery = the instance + the commit hashes + the REPORT to the issuer cc `3.0.0_SA_CVO~X` + `1.0.0_SA_CTO~X`.

## LANE

`org/standards/isck/ledger/**` is `ANY_EXEC`; wave 1 took the fourth SINGULAR override. For a build wave that commits per unit, a per-commit override is a toll: CTO~X (lane owner, 77670) proposed a `permitted_agents` row for `0.4.0_DT_ClientPlatform~X` on `org/standards/isck/ledger/**` for this TO's life -- asked of the lane-table owner at the cut (see the issuer's GO message); until it lands, each commit under the package is a new singular ask to the issuer, cited in the commit body, and `ledger/receipts/` stays under the same rule. **Never `GIT_COMMIT_AUTHOR_OVERRIDE` without an authorization id in the body.**

## BOUNDARIES

- **Implements, never revises.** A contract defect -> finding to the issuer for a NEW candidate (C5 last sentence). The frozen `+27` is not touched; `superseded_by` / `superseded_by_version` are REFUSED on any write after creation and populated only as derived projections.
- **Production population + the L3 cells stay HELD** on the sovereign R1/L2 hold (row 6). Fixtures only.
- **The design is the spec and the spec is FROZEN mid-round** (Rule 27). Off-spec -> one line to `3.0.0_SA_CVO~X` cc the issuer, keep working. A design SEQUENCING defect (the R4-DT-3 class) is the issuer's to re-sequence, not the lane's to route around.
- **Instrument traps already banked this round:** a label composed before its evidence describes the expectation; an example is a sample of the schema; a git pathspec `*` crosses `/`; a working tree is not atomic; a count nobody printed is a claim.

## REPORT

`<status>` here + MCP to `2.0.0_SA_COO~X` cc `3.0.0_SA_CVO~X`, `1.0.0_SA_CTO~X`: the commit hashes, the runner's own printed line from the clean clone, the 13 AC7 verdicts (PROMOTED / KILLED with the fixture cited), the receipt commit + the `--receipt` invocation's output, push state as a MEASURED value. Interim reports per unit are welcome and cost nothing; a BLOCKING surprise routes the moment it is measured.
