# TASK ORDER -- DTX · NFRA_C3MATERIALIZE WP-3b · THE FIRST REAL-SUBSTRATE ADMISSION (B2, with B3 decided inside)

<status>pending</status>

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X` · **label owner (receipts + lane grant):** `1.0.0_SA_CTO~X`
**scope:** 7 entities / 32 cells -- 24 executor cells + 3 receipt cells (the label owner's acts, discharged by this TO's run_commit evidence) + 5 mechanism cells on this face · **contract:** v0.3-candidate+27 FROZEN schema-only (untouched) · **decomp:** CERTIFIED PASS @73f74a2798 (`3.0.0_SA_CVO~X` attempt 1; final rectangle sha256 e1d8265eff6a6ab75d29e65390e9486dde7dc4a190f6e4bdd97654da5c896528 = the sealed dry)

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-wp3b/20260828T1419Z/DECOMP.md @73f74a2798

cells:
WP3B-zadv-1 WP3B-zadv-2 WP3B-zadv-3 WP3B-zadv-4 WP3B-zadv-5
WP3B-utsj-1 WP3B-utsj-2 WP3B-utsj-3 WP3B-utsj-4 WP3B-utsj-5
WP3B-awel-1 WP3B-awel-2 WP3B-awel-3 WP3B-awel-4
WP3B-adtk-1 WP3B-adtk-2 WP3B-adtk-3 WP3B-adtk-4
WP3B-vvxs-1 WP3B-vvxs-2 WP3B-vvxs-3 WP3B-vvxs-4 WP3B-vvxs-5 WP3B-vvxs-6
WP3B-hmez-1 WP3B-hmez-2 WP3B-hmez-3
WP3B-mech-1 WP3B-mech-2 WP3B-mech-3 WP3B-mech-4 WP3B-mech-5

<owned_cells>
WP3B-zadv-1 WP3B-zadv-2 WP3B-zadv-3 WP3B-zadv-4 WP3B-zadv-5
WP3B-utsj-1 WP3B-utsj-2 WP3B-utsj-3 WP3B-utsj-4 WP3B-utsj-5
WP3B-awel-1 WP3B-awel-2 WP3B-awel-3 WP3B-awel-4
WP3B-adtk-1 WP3B-adtk-2 WP3B-adtk-3 WP3B-adtk-4
WP3B-vvxs-1 WP3B-vvxs-2 WP3B-vvxs-3 WP3B-vvxs-4 WP3B-vvxs-5 WP3B-vvxs-6
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="WP3B-AC1" cell_refs="WP3B-zadv-1, WP3B-zadv-2, WP3B-zadv-3, WP3B-zadv-4, WP3B-zadv-5"/>
  <criterion id="WP3B-AC2" cell_refs="WP3B-utsj-1, WP3B-utsj-2, WP3B-utsj-3, WP3B-utsj-4, WP3B-utsj-5"/>
  <criterion id="WP3B-AC3" cell_refs="WP3B-awel-1, WP3B-awel-2, WP3B-awel-3, WP3B-awel-4"/>
  <criterion id="WP3B-AC4" cell_refs="WP3B-adtk-1, WP3B-adtk-2, WP3B-adtk-3, WP3B-adtk-4"/>
  <criterion id="WP3B-AC5" cell_refs="WP3B-vvxs-1, WP3B-vvxs-2, WP3B-vvxs-3, WP3B-vvxs-4, WP3B-vvxs-5, WP3B-vvxs-6"/>
  <criterion id="WP3B-AC6" cell_refs="WP3B-hmez-1, WP3B-hmez-2, WP3B-hmez-3"/>
  <criterion id="WP3B-AC7" cell_refs="WP3B-mech-1, WP3B-mech-2, WP3B-mech-3, WP3B-mech-4, WP3B-mech-5"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_C3MATERIALIZE.TO-WP3b-DTX_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>WP3B-AC1,WP3B-AC2,WP3B-AC3,WP3B-AC4,WP3B-AC5,WP3B-AC6,WP3B-AC7</expected_criteria>
  <alignment_denominators>criteria: 7. Cells: 32 of 32 in the certified decomp -- 24 owned by this executor + 3 receipt cells (label owner) discharged by AC6 evidence + 5 mechanism cells discharged on this face by AC7; every cell covered by exactly one criterion; backward: every criterion cites >= 3 cells.</alignment_denominators>
</proof_of_spec>

---

## AUTHORITY

D11 ledger row 17 (R1 LIFTED -- Andrew-direct 2026-08-28 14:08Z at the `1.0.0_SA_CTO~X` terminal, verbatim *"Lift everything, time to work buddy"*, record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260828_1408Z_LIFT_EVERYTHING_TIME_TO_WORK.md` @676604de18), unblock (2) at the issuer. Sequenced FIRST (77886, concurred `1.0.0_SA_CTO~X` 77896 / `3.0.0_SA_CVO~X` 141857Z / `0.4.0_DT_ClientPlatform~X` 77900) because the WP-3 battery is fixtures-only and the registry reads `vertical_slice_receipt` NULL / `historical_replay_receipt` NULL. Rule 27: cut from the CERTIFIED rectangle only (`rectangle.final.certified.json` @73f74a2798). The lift is cited verbatim and is NOT read as authorising egress, spend or a shared-branch act; the separate B4 egress word ("you have egress", 0.4.0_DT_ClientPlatform~X 78004) covers ONE PyPI fetch for B4 and nothing in this TO.

## THE INPUT, READ AT SOURCE

- POPULATION: `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/graph_object_manifest.json` (the EMITTED L0 manifest) @2feca185e7, `as_of.commit_ish` e48a7466ba. Grain = the manifest PART. **Sampling rule: ALL parts (fraction 1.0).** The count is read from the file by the runner and PRINTED beside every count with its provenance (file, pin, as_of, sampling rule, run_commit); it is typed nowhere on this face.
- LEDGER: `org/standards/isck/ledger/engine.py` (`Store.admit` atomic / `anchor` / `replay` / `replay_expecting` / `canonical()`), the WP-3 build (receipt eb15d30b6b @ run_commit d11c341f79); design `org/standards/isck/WP3_LEDGER_DESIGN.md` @d0398b977d sec 2c / 2e / 3 rows 8-12.
- CONTRACT: v0.3-candidate+27 -- `surface_version` REQUIRES `content_digest`, `fingerprint_method`, `normalization_version`, `source_frontier_id`, `producing_run_id`, `publication_state`; `additionalProperties: false`; no byte moves.
- The four boundary notes are the cells' own text: `0.4.0_DT_ClientPlatform~X` 77868 + 77900, `3.0.0_SA_CVO~X` 141857Z (six points), `1.0.0_SA_CTO~X` 77896 + 77904.

## ORDER OF WORK

Population declaration (AC1) -> translator (AC2) -> admission (AC3) -> snapshot surface (AC5) -> replay against the snapshot (AC4) -> evidence + receipts (AC6) -> report. AC7's mechanism cells are on this face from cut.

## AMENDMENT 2 -- 2026-08-28 15:5xZ (issuer, on 0.4.0_DT_ClientPlatform~X 78223 CORRECTION): THE SECOND UNIFORM GAP -- AC2's SEVEN record families, scoped honestly for this slice

Act 3 @e3ed3922eb emitted THREE of AC2's seven families (mint_receipt, entity, entity_binding: 42 / 42 / 42) and printed `translated 42 | errored 0`, which beside a green AC3 reads as AC2 discharged -- DT~X corrected it before anyone read it that way. The generation/provenance half measured a SECOND uniform gap of the same shape as the first: of 42 parts, 28 name a materializer and every one of the 28 lacks `semantic_layer` + `canonical_role` (one distinct missing-field set); 14 carry no generation at all; `materializer_version.bundle_digest` (REQUIRED by the frozen schema) is unreachable on 42 of 42 because `generation.materializer_digest` is present on none -- and a digest is a COMPUTED fact over an artifact's bytes, not a declarable value. RULING (a combination; the translator's refusal posture stays exactly as it is):

- **`semantic_layer` + `canonical_role` (declaration gap, 28 parts):** the design lane extends the mapping as DATA (`1.0.0_SA_CTO~X`, L0_PART_IDENTITY_MAPPING v0.2 -- values by the part's materializer class, basis `held`, cited per part); the declaration pass applies it into the emitted manifest's generation block the way v0.1 filled `part.identity`; a materializer whose values cannot be declared with evidence stays ERRORED, counted.
- **`bundle_digest` (computed fact):** the EMITTER computes `generation.materializer_digest` at compile time WHERE the materializer is a repo artifact -- the git blob (single file) or tree (directory) digest at the population pin, method printed -- and emits `materializer_version` for those parts; where the materializer is not a repo artifact (lambda / s3-hosted / a runtime-named family) the digest is an EXPLICIT absence and `materializer_version` is OUT for that part, per-part, counted. Nothing is invented.
- **`source_frontier` + `materialization_run`:** these are the SLICE's OWN records, not the manifest's -- the population's frontier (the two pins, `as_of`, the preservation copy's digest) and the slice run itself -- emitted by the RUNNER at admission time. In scope NOW; this is what makes AC4's `as_of frontier F` anchor reachable.
- **AC2 is therefore read as:** the seven families are attempted for every part; the record-type census prints EMITTED / ERRORED / OUT-OF-REACH per family with the reason class (declaration gap / uncomputable digest / no generation on the part); refusals are the finding. **AC4 is read as:** both anchors (frontier F, commit_seq HEAD) exercised once `source_frontier` exists -- act 3's commit_seq-only line stands as partial and says so. AC3, AC5 unchanged.
- Option (iii) of 78223 (identity half only, the rest to the next TO) is NOT taken: it would fix the population and quietly narrow the receipt the registry is waiting for. The next vintage (the ratification re-read at `4.0.0_SA_CRO~X`) still produces the fuller population later; this slice admits what is honestly reachable now and prints the rest.

## ACCEPTANCE CRITERIA (each cites the cells it discharges)

## AMENDMENT 2026-08-28 15:0xZ (issuer, on 0.4.0_DT_ClientPlatform~X 78073 BLOCKING + 3.0.0_SA_CVO~X 150659Z UPHELD) -- THE FIRST REAL FINDING, AND THE ISSUER'S CRITERION DEFECT

Unit 1 @6176b7d4ae measured `translated 0 | ERRORED 42 | reconciliation 42 of 42` -- ONE uniform gap: the pinned L0 manifest carries none of the contract's five required identity fields (`entity_class`, `plane`, `entity_grain`, `identity_scope`, `identity_policy`) on any part. The translator's refusal to map `part_class` -> `entity_class` by name was CORRECT (utsj-3 working). The defect is the ISSUER's: this face pinned a population whose vocabulary was never checked against the contract at decomp time. RULING (option (b), CVO-preferred): the five fields are DECLARED per part by the L0 EMITTER, never mapped by the translator --

- **AC1 (population) is amended:** the population becomes the RE-EMITTED L0 manifest carrying the five fields; its new pin and `as_of` are PRINTED beside every count; the old pin @2feca185e7 stays on the report as the vintage the finding was measured at. The count is still read from the file.
- **AC2 (translator) is amended with a DECLARATION PASS that precedes it, in the executor's own emitter (`org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/l0_compile_w3.py`):** per part, each of the five fields is DECLARED with `basis_by_field` + evidence -- `plane` and `entity_grain` from the L1 canonical grain declaration (`D11_L1/L1_CANONICAL_GRAIN_DECLARATION.md`: the ordered pair (PLANE, ENTITY), four planes, cited per part); `entity_class` and `identity_policy` with MEMBERSHIP CHECKED against the contract's registered vocabularies (ISCK_CONTRACT.md sec 3.15; `vocab/entity_classes.json` and the identity_policy vocab, read at build time); `identity_scope` from the contract enum {logical, fabric_instance, device_instance, run_occurrence} by the part's home, with the reason printed. A value that cannot be declared with evidence is an EXPLICIT `absent` (basis_by_field = absent) and that part stays ERRORED at translation -- the gap becomes a per-part count, never a silent fill. Nothing is invented; a name-similarity mapping is refused by construction. The emitter's own printed line (parts seen | declared 5/5 | absent-by-field counts) is the acceptance.
- **AC3-AC5 stand as written** over the re-emitted population; the N=0 vacuity is answered by the declaration pass, and the positive control's N is whatever the runner prints. Per CVO~X's disposition, AC4/AC5 machinery may be built and exercised against the battery fixtures meanwhile with real-substrate results marked UNMEASURED; no flip until a positive pinned-population run admits N>0 and exercises replay + snapshot.
- **The finding is preserved:** the 42/42 ERRORED line at @2feca185e7 is the first row of this TO's evidence, not a defect to erase.

---
**WP3B-AC1 -- POPULATION DECLARED, NEVER TYPED** (`WP3B-zadv-1..5`): the runner opens the population file at the pin; grain = part; sampling ALL with the rule printed; D11's own deliverables admitted KNOWINGLY and flagged `observer=true` (count printed); every count line carries its provenance line.

**WP3B-AC2 -- TRANSLATOR: CLAIMS CARRIED, NOTHING FABRICATED** (`WP3B-utsj-1..5`): per part, the bootstrap pair {mint_receipt, entity} + entity_binding (native_key = the part's home) + materializer / materializer_version from `generation.materializer`; ONE source_frontier for the population at as_of; ONE materialization_run for the slice; record-type census printed, only frozen-schema types; `part.basis` maps to the record's claim fields and never upgrades; a required field the part cannot supply ERRORS the part with the field named (no synthetic default anywhere -- the negative arm greps the translator); byte-identical batches on the same pin (`canonical()`); no S3/AWS/vendor call, no credential, no client bucket.

**WP3B-AC3 -- ADMISSION THROUGH 2c, REFUSALS ARE THE FINDING** (`WP3B-awel-1..4`): every write via `Store.admit` (atomic; `Rejected` writes nothing; head_commit_seq unchanged on refusal); `admitted + refused + errored == denominator`, printed; every `Rejected` preserved VERBATIM (code, message, responsibility id) in the evidence file; the store is SQLite, device-local, private -- nothing outside the run directory is opened for write except the published snapshot.

**WP3B-AC4 -- REPLAY AT NAMED ANCHORS** (`WP3B-adtk-1..4`): two anchors at least -- `as_of frontier F` (the population's source_frontier batch) and `as_of commit_seq HEAD` -- each bound via `Store.anchor` and printed; `replay_expecting` claims checked against the recorded state, outcomes preserved (a disagreeing claim is a printed refusal, not a crash); the sec-2e backfill arm in BOTH directions (a later batch with an earlier event time EXCLUDED from an anchor admitted before it, INCLUDED at event-time position after); the replay set from the PUBLISHED SNAPSHOT opened alone equals an independent load (record-id sets equal; `anchor_commit_seq` printed by both).

**WP3B-AC5 -- THE SNAPSHOT IS A SURFACE, NOT A COPY (B3 decided here)** (`WP3B-vvxs-1..6`): the published artifact is produced by `VACUUM INTO` or the sqlite backup API -- NEVER a copy or hash of the live WAL-mode main file (the method is printed); ONE `surface_version` admitted with `content_digest` over the published artifact's bytes under a DECLARED `fingerprint_method` + `normalization_version`, `source_frontier_id` + `producing_run_id` set, `publication_state` per row 10 (publish only from a succeeded run); the admitting batch's envelope `commit_seq` is bound to `surface_version_id` in the RECEIPT/EVIDENCE -- never a field of the record; POSITIVE control: the artifact opened ALONE returns exactly N admitted rows with the expected frontier and `anchor_commit_seq`; NEGATIVE control: the naive main-file copy, opened alone, returns fewer rows or fails to open -- retained, and it MUST fail (a passing negative arm voids the digest); the snapshot + its receipt are the shared carrier; no consumer path opens the live store.

**WP3B-AC6 -- CLEAN-CLONE RUN + THE TWO RECEIPTS** (`WP3B-hmez-1..3`): the slice runs from a fresh unique clone at `--run-commit` (exit 0/1/3/4 semantics as `run_battery.py`; never deletes a destination); a second seat's replay reproduces admitted/refused/errored; the evidence (`org/standards/isck/receipts/vertical_slice_{receipt.json,evidence.txt}` and `historical_replay_{receipt.json,evidence.txt}`) is in the shape `bundle_identity.py --receipt` consumes, `run_commit == its own evidence`; the RECORDING on v0.3-candidate+27 is the label owner's act (`1.0.0_SA_CTO~X`, `receipt_problem(run_commit, kind, rec) is None`; registry NULL -> RECORDED for both kinds) -- this TO delivers the evidence, not the registry write.

**WP3B-AC7 -- MECHANISM, ON THIS FACE** (`WP3B-mech-1..5`): mech-1 the scoped lane grant (LANE below); mech-2 NO performance claim -- any throughput sentence must be a printed measurement or absent; mech-3 no bridge cell populated, no fusion; mech-4 the lift cited verbatim, nothing wider; mech-5 the certifier never the author (this decomp was certified by `3.0.0_SA_CVO~X` from the issuer's c0; the executor measures, the certifier verifies).

## LANE

The deliverables land under **`org/standards/isck/ledger/**`** (the slice runner, translator, fixtures/flags if any) and **`org/standards/isck/receipts/**`** (evidence + receipt files) plus this seat's own `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/**` (the PROOF_OF_SPEC instance, the published snapshot artifact). The first two are ANY_EXEC since the strike @25fc2f5d1a: **`1.0.0_SA_CTO~X` grants a scoped `.owned-paths.yaml` row for `0.4.0_DT_ClientPlatform~X` on those two subtrees for this TO's life, same shape as @f94ef2f3d1 / @5bde064942, exercised by the first refused commit, struck on the flip.** Until the row lands, the executor's first commit there is REFUSED -- that refusal is the exercise, not a defect.

## BOUNDARIES

- Fixtures for the SUBSTRATE TIERS only where the design needs them; the population is the REAL manifest. No production write outside the device-local store and the repo. No egress of any kind (the B4 word covers B4 alone).
- Adequacy at production volume is UNCLAIMED. `2c ADMISSION` at volume stays unmeasured unless a printed measurement says otherwise.
- No bridge population, no fusion, no L3 cell -- WP-5 waits on this TO and on WP-4.
- The contract does not move. If the slice needs a contract byte, that is a FINDING routed to the label owner, never an edit here.

## REPORT

Route completion to `3.0.0_SA_CVO~X`, cc issuer, with: the runner's printed lines (denominator + provenance; admitted / refused / errored; the observer count; the record-type census; the two anchors' commit_seq; the snapshot method, digest, fingerprint_method, normalization_version; positive and negative control outcomes), the run_commit, the evidence paths, the proof-of-spec instance VALID line, and **PUSH STATE as a MEASURED value** (ls-remote read). Refusals are findings: list every one. The issuer flips this face on the certifier's verdict; the label owner records the receipts on the run_commit.
