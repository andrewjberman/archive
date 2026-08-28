# TASK ORDER -- COX · NFRA_C3MATERIALIZE B4 · THE STRUCTURE VIEW'S SBM PRODUCER (graph-tool) IN AN AWS CONTAINER

<status>pending</status>

**to:** `0.7.0_AE_CloudOps~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X` · **oracle owner (CONFORMS/FAILS reading):** `4.0.0_SA_CRO~X` · **architecture owner (infra clauses, change-management):** `1.0.0_SA_CTO~X` · **seat:** `0.0.0_AB_MSTR` (spawned 15:08Z, LD-0468 @6c34c02677)
**scope:** 6 entities / 24 cells -- 19 executor cells + 5 mechanism cells on this face · **oracle:** `STRUCTURE_SBM_CONFORMANCE_PREDICATE.md` @b4caea27f0, UNCHANGED · **decomp:** CERTIFIED PASS @d07debaef4 (`3.0.0_SA_CVO~X` attempt 1; final rectangle sha256 4e19b551caeb05b885fed11a5bb584f1f798bf1fce44cdb26d7616daedc8c927 = the sealed dry)

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-b4/20260828T1505Z/DECOMP.md @d07debaef4

cells:
B4-urkd-1 B4-urkd-2 B4-urkd-3 B4-urkd-4 B4-urkd-5
B4-jaho-1 B4-jaho-2
B4-zvjt-1 B4-zvjt-2 B4-zvjt-3 B4-zvjt-4 B4-zvjt-5 B4-zvjt-6
B4-xqdq-1 B4-xqdq-2 B4-xqdq-3
B4-ramh-1 B4-ramh-2 B4-ramh-3
B4-mech-1 B4-mech-2 B4-mech-3 B4-mech-4 B4-mech-5

<owned_cells>
B4-urkd-1 B4-urkd-2 B4-urkd-3 B4-urkd-4 B4-urkd-5
B4-jaho-1 B4-jaho-2
B4-zvjt-1 B4-zvjt-2 B4-zvjt-3 B4-zvjt-4 B4-zvjt-5 B4-zvjt-6
B4-xqdq-1 B4-xqdq-2 B4-xqdq-3
B4-ramh-1 B4-ramh-2 B4-ramh-3
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="B4-AC1" cell_refs="B4-urkd-1, B4-urkd-2, B4-urkd-3, B4-urkd-4, B4-urkd-5"/>
  <criterion id="B4-AC2" cell_refs="B4-jaho-1, B4-jaho-2, B4-ramh-2"/>
  <criterion id="B4-AC3" cell_refs="B4-zvjt-1, B4-zvjt-2, B4-zvjt-3, B4-zvjt-4, B4-zvjt-5, B4-zvjt-6"/>
  <criterion id="B4-AC4" cell_refs="B4-xqdq-1, B4-xqdq-2, B4-xqdq-3"/>
  <criterion id="B4-AC5" cell_refs="B4-ramh-1, B4-ramh-3, B4-mech-4"/>
  <criterion id="B4-AC6" cell_refs="B4-mech-1, B4-mech-2, B4-mech-3, B4-mech-5"/>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_C3MATERIALIZE.TO-B4-COX_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>B4-AC1,B4-AC2,B4-AC3,B4-AC4,B4-AC5,B4-AC6</expected_criteria>
  <alignment_denominators>criteria: 6. Cells: 24 of 24 in the certified decomp -- 19 owned by this executor + 5 mechanism cells discharged on this face (mech-4 by AC5, the rest by AC6); every cell covered by exactly one criterion; backward: every criterion cites >= 3 cells.</alignment_denominators>
</proof_of_spec>

---

## AUTHORITY

**SOVEREIGN GO (added 2026-08-28 15:3xZ, D11 ledger row 20 @d597074d0e):** Andrew-direct at the `0.4.0_DT_ClientPlatform~X` terminal, VERBATIM: *"go ahead with graph-tool in a container"* -- relayed verbatim 78166 (DT~X), concurred `0.0.0_AB_MSTR` 78170 / `3.0.0_SA_CVO~X` 153721Z: the GO for branch (a) IN THE AWS CONTAINER of his ~15:00Z word; not a re-opening of Docker Desktop on the workstation. This TO's executor holds the TO (this face), the GO (78166 + row 20) and the seat (LD-0468).

Andrew-direct ~15:00Z at the `0.0.0_AB_MSTR` terminal, VERBATIM: *"have htem do it in an aws container, codebuild or whatever their product is on there"* (record `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20260828_1500Z_B4_GRAPHTOOL_IN_AWS_CONTAINER_CODEBUILD.md` @98a25b3112), answering B4 card #2 by substitution: the graph-tool measurement runs in an AWS container in the estate's own account; the workstation Docker branch is CLOSED; the product choice is delegated to the doing seat; the oracle is UNCHANGED; nothing outside B4 is lifted. Chain: L2 STRUCTURE delivered FAILED (TO-L2-CROA complete @86efc5c4eb, consensus 0/19,482 ABSENT-NOT-ZERO) -> oracle @b4caea27f0 -> candidate (b) graspologic FAILED the per-run convergence clause (`0.4.0_DT_ClientPlatform~X` 78038, measured; `4.0.0_SA_CRO~X` upheld; `1.0.0_SA_CTO~X` 78040: branch (a)). D11 ledger rows 18-19. Rule 27: cut from `rectangle.final.certified.json` @d07debaef4 only.

## THE INPUT, READ AT SOURCE

- ORACLE: `org/tier1_exec/4.0.0_SA_CRO~A/deliverables/NFRA_C3MATERIALIZE.TO-L2-CROA/STRUCTURE_SBM_CONFORMANCE_PREDICATE.md` @b4caea27f0 -- degree-corrected SBM; explicitly versioned production implementation; recorded model-selection objective; **N=25** independent runs under the artifact's anchor-derived seed policy; per run: seed, full partition, objective, iterations/convergence state, input digest, implementation version; `W_STRUCTURE(i,j)` = the fraction of the 25 runs co-assigning i and j; discrimination: all 25 records validate, >= 2 distinct off-diagonal affinities, neither uniformly 0 nor 1, the all-one constant-matrix mutant refused. Read N from the oracle; type it nowhere.
- POPULATION: the STRUCTURE entity set in `.../L2_VIEW_ARTIFACTS.json` @f42970fdef (edge-incident non-`semctl` Kuzu node ids as `4.0.0_SA_CRO~X` serialized them; input digest a323f598...). The count is read from the artifact and printed; it is typed nowhere on this face.
- DEVICE/ESTATE FACTS: graph_tool ABSENT in the estate python; Docker Desktop daemon NOT running and NOT to be started; WSL no distro -- all moot: the run is in AWS.
- Your own read-only precedent read (78088 / MSTR direction): the container product the estate already runs, image reachability from the account, the topology object's route into the account's own bucket. Print it as the first section of the report.

## ORDER OF WORK

Precedent read + graph query (AC1.4) -> job definition as code (AC1.3) -> population object + digest check (AC2) -> the oracle run (AC3) -> outputs to the repo (AC4) -> egress/estate checks (AC5) -> teardown + cost (AC1.5) -> report. AC6's mechanism cells are on this face from cut.

## AMENDMENT 2026-08-28 15:4xZ (issuer, on 0.7.0_AE_CloudOps~X 78188 FIRST REPORT + 4.0.0_SA_CRO~X 154415Z UPHELD) -- THE POPULATION OBJECT MUST CARRY THE EDGES; THE ISSUER'S DIGEST CITATION WAS A CENSUS, NOT A FILE

MEASURED by the executor before building (78188): L2_VIEW_ARTIFACTS.json @f42970fdef serializes the 19,482 STRUCTURE node records and ZERO edge rows (95 distinct keys, no edge/src/dst/adjacency at any depth; the 36,549 directed edges appear only as counts); `a323f598...` is `STRUCTURE.computation.input_digest`, a digest over CRO~X's Kuzu topology CENSUS, not over any serialized object. As cut, AC2 (node ids only; no in-container Kuzu rebuild) and AC3 (an SBM over an adjacency) were jointly unsatisfiable, and the failure mode is the dangerous one: a node-only SBM still prints 25 complete records and a consensus, indistinguishable from a measurement. The defect is the ISSUER's (a digest cited by name from a report, never re-derived against an object). RULING:

- **AC2 (population input) is amended:** the ONE object placed in the account's own bucket is the CANONICAL NORMALIZED OBJECT `4.0.0_SA_CRO~X` produces (154415Z) carrying BOTH the exact 19,482 STRUCTURE node ids AND the 36,549 directed edge rows at anchor `bb01a202721f9c3a719a3a662319cebc194a1720`, with a SHA-256 DECLARED BY CRO~X over THAT object together with its NORMALISATION (byte form, line endings, key order, encoding) -- the refuse-on-mismatch arm targets that declared digest and nothing else. `a323f598...` is retired from this face as a carrier digest; it stays cited as the census it is. One object, own bucket, no Kuzu rebuild in-container -- unchanged.
- **Digest normalisation (78188 finding 4):** every digest on this face and in the report STATES its normalisation; a CRLF-checkout of the same content that changes the raw digest is not a mismatch and is not a match either until normalised -- print both when they differ.
- **AC3 is unchanged** and now runnable: the inference runs over the edge rows of that object; the per-run records cite the object's declared digest as `input digest`.
- **Module path (78188 sec 5):** the executor requests a NEW module `infra/aws/terraform/c3materialize-b4/` with its own state key (a one-shot measurement job must not share the globgrph derive-runner image's blast radius -- five task definitions ride it). The issuer CONCURS with the reason; the grant and the module ruling are `1.0.0_SA_CTO~X`'s (architecture owner), same-turn per 78173.
- **Rule 20 (78188 sec 6):** `comp-kuzu` timed out twice on a bounded count; that is an instrument observation, not a graph result and not a bypass. The citation AC1.4 requires may come from any query listed in `org/modules/graph/graph-call-manifest.yaml` (QUERY, never rebuild); if every listed instrument times out, that is a FINDING to the tool owner (`1.0.0_SA_CTO~X`) on the report, and no cloud change is made until a citation exists.
- The BLOCKING item (78188 sec 3, class BLOCKING, ARMED) is DISARMED by this amendment once CRO~X's object + declared digest land; the executor names the landing on its next report. AC2/AC3 stay blocked until then, exactly as CRO~X upheld.

**CARRIER LANDED (2026-08-28 16:0xZ, closes the AMENDMENT's BLOCKING item):** the AC2 population object is `org/tier1_exec/4.0.0_SA_CRO~A/deliverables/NFRA_C3MATERIALIZE.TO-L2-CROA/STRUCTURE_POPULATION_CARRIER.json` @afa8833b5c (git blob b5b2d0db0a7f...; object SHA-256 `b4231e6374ce4360c05fed99a527eaec9e00be23c4858369148869c7ff044dfd`; normalisation: UTF-8, canonical JSON sort_keys=true compact separators ensure_ascii=false, exactly one terminal LF, nodes ascending id, edges ascending; directed multigraph, edge-row multiplicity preserved -- 36,549 rows, 36,548 unique triples, 1 duplicate tuple, ruled intentional by CRO~X and verified by CVO~X; verifier `verify_structure_population_carrier.py` beside it). That SHA-256 is the refuse-on-mismatch referent; the node and edge counts are read from the object and printed. AC2 -> AC3 are GO.

**ORACLE DISPOSITIONS (2026-08-28 17:50Z, `4.0.0_SA_CRO~X` 175019Z, oracle owner; recorded by the issuer, criteria set unchanged):** (1) SEED: option (a) ADMISSIBLE -- `gt.seed_rng(seed_requested % 2**32)` conforms when the reduction is declared on every run record, `seed_requested` is verified count/order/value against the commit-pinned 25-value `STRUCTURE_SEED_MANIFEST.json` (@8eec9f0b30), and each record carries `seed_requested`, `seed_effective` and the mapping; the 25 published values reduce to 25 unique effective seeds, zero collisions; no re-publication. (2) CONVERGENCE: record-breaking equilibration ADMITTED under `1.0.0_SA_CTO~X` 78442's best-seen contract (declared criterion, initial best, comparison metric, absolute improvement tolerance, wait window, max-sweeps, sweeps since last minimum, `best_seen_sweep`, `terminal_sweep`, stop reason, run state, `emitted_state=best_seen`, partition/objective coherence from the same state); a ceiling exit remains NOT_CONVERGED. **AC3 conformance requires 25/25 CONVERGED fits; any smaller converged subset is DIAGNOSTIC only.** CRO~X accepts `3.0.0_SA_CVO~X`'s code-face fidelity PASS at @708110ffa8; the corrected rerun is GO; build 3 (`03eec232`) stays diagnostic-only. Runtime disarm stays CVO~X's on printed records; final CONFORMS / FAILS / UNMEASURED stays CRO~X's.

## ACCEPTANCE CRITERIA (each cites the cells it discharges)

**B4-AC1 -- THE CONTAINER RUNTIME** (`B4-urkd-1..5`): CodeBuild by default (ECS/Batch only with the reason printed) -- NOT Docker Desktop, no workstation Docker anywhere; the graph-tool image reference, digest and version PRINTED FROM THE RUNNING CONTAINER (never from a tag) -- that is the oracle's "explicitly versioned implementation"; the job definition (buildspec / task definition) is a repo artifact in your lane and any AWS resource it needs goes through Terraform via `safe-apply` (NEVER-9) -- never a console click, never a bare apply; the dependency graph is QUERIED AND CITED before any cloud change (rule 20; `org/modules/graph/graph-call-manifest.yaml` -- query, never rebuild); one bounded job, resources torn down after, the run's cost (or CodeBuild minutes) printed, no standing schedule (NEVER-5).

**B4-AC2 -- THE POPULATION INPUT** (`B4-jaho-1..2`, `B4-ramh-2`): the STRUCTURE entity set placed as ONE object in the account's own bucket for the job -- never a client (49F/ADVI/MDPF) bucket, never a Kuzu rebuild inside the container; the container verifies the input digest before run 1 and REFUSES on mismatch (the negative arm: a corrupted copy is refused); the object list mounted into the job is printed and is one object; estate graph data only, no client data in, no data out of the account.

**B4-AC3 -- THE ORACLE RUN** (`B4-zvjt-1..6`): graph-tool imports in the container, version printed; N=25 degree-corrected SBM inferences (`minimize_blockmodel_dl`, `deg_corr=True`) under the anchor-derived seed policy, seeds printed; each run records seed, full partition, objective (description length), iterations/convergence state, input digest, implementation version -- as RECORDS, not prose; `W_STRUCTURE` computed from the 25 partitions only; the three discrimination lines printed and the all-one mutant printed REFUSED; wall time per run and in total.

**B4-AC4 -- OUTPUTS** (`B4-xqdq-1..3`): the 25 run records, the consensus artifact, the gate lines and the job log land in the repo under your deliverables with the job id and the input digest (digest-addressed; paths on the report); the CONFORMS / FAILS reading of the records is `4.0.0_SA_CRO~X`'s and never yours -- UNMEASURED where a clause did not print; no bridge cell, no fusion, no L2 view rewrite (the STRUCTURE view's re-delivery is a separate `4.0.0_SA_CRO~X` act on CONFORMS).

**B4-AC4 OUTPUT SHAPE (issuer face line 2026-08-28 18:1xZ on `4.0.0_SA_CRO~X` ORACLE RULING 180747Z + clarification 180855Z, `3.0.0_SA_CVO~X` 180923Z; clarification of ENCODING, not a relaxation of the observable W contract; criteria set unchanged):** candidate `ec6a9a58` reached 25/25 CONVERGED under the admitted criterion and was then OOM-killed (exit 137) at the consensus allocation -- a logged convergence OBSERVATION only, AC3 NOT COMPLETE / UNMEASURED, no CONFORMS credit, its records lost (the refusal-evidence arm was not on that pin). W_STRUCTURE over 19,482 nodes does not fit as an enumerated JSON pair list, and the oracle does not require one. **SELECTED CARRIER, named for CVO certification: the CANONICAL W_STRUCTURE FACTORIZED VIEW -- a DISTINCT artifact with its own schema/type** carrying: (i) the canonical node order; (ii) all N=25 full, aligned partition vectors (the aligned FACTORS of W, not incidental evidence); (iii) the exact evaluator `W(i,j) = sum_r [partition_r[i] == partition_r[j]] / 25` with the exact INTEGER numerator 0..25 and the declared denominator 25 (never float-only semantics); (iv) the total unordered off-diagonal pair domain defined with NO threshold / top-K / omission / default ambiguity; (v) anchor, carrier digest, seed/run provenance and the canonical artifact digest (sha256, normalisation declared); (vi) a repo VALIDATOR that answers arbitrary (i,j) exactly and REFUSES malformed alignment. The 25 raw partition records ALONE do not satisfy emission. The exact streamed columnar `(i,j,count)` artifact with explicit default zero is ADMISSIBLE only if the executor declares that switch on the record BEFORE the run -- never silently. In either form: the discrimination gate is computed EXACTLY from the factorization (>=2 distinct off-diagonal affinity values, neither uniformly 0 nor uniformly 1; the all-one factorized mutant REFUSED), with witnesses/counts published for independent replay. **A corrected rerun is REQUIRED at a NEW pin** carrying the buildspec refusal-evidence arm and the factorized consensus artifact, with a controlled nonzero runner exit exercised to prove real records upload while build failure is preserved; the memory guard is RECALIBRATED to the FINAL algorithm's measured peak incl. numpy temporaries (the 110 B/dict-pair constant is evidence against the OLD implementation, not a guard for the new one) and an over-budget projection control REFUSES before allocation. Bigger compute alone is not an admissible answer to artifact shape.

**B4-AC4 EVIDENCE KEYS (issuer face line 2026-08-28 19:0xZ on `0.4.0_DT_ClientPlatform~X` 190228Z + `4.0.0_SA_CRO~X` 190409Z + `3.0.0_SA_CVO~X` 190541Z; clarification of AC4's 'digest-addressed', not a new criterion):** the served proof object at `c3materialize-b4/out/SBM_RUN_RECORDS.json` (18:28:49Z, 2,877,798 B, sha256 538b3e09...) was OVERWRITTEN at the same key by a later build (18:55:36Z, 2,881,485 B, sha256 d658eb91...) on a bucket with versioning NOT enabled (positive control: `lambda-artifacts` returns Enabled) -- a control verified on the served copy whose artifact no longer exists at that key; CRO~X retained the exact downloaded copy. FROM THIS LINE: every published evidence object is written to an IMMUTABLE, RUN-ADDRESSED key (`.../out/<build-id>/<artifact>` or equivalent) carrying the build id and the input digest; no build ever writes a key an earlier build wrote; the report cites each object by key + size + sha256 + s3api UTC LastModified. Second finding, same family (A VALUE MUST CARRY ITS CLAIM): every record in the served object carries `convergence_label_basis = stability_check_with_demonstrated_failing_arm` while no run in that artifact fired the failing arm (all 25 `stop_reason = wait_window_elapsed`, no control block present) -- a claim field asserting provenance the artifact cannot support; such a field is populated ONLY when the artifact itself carries the control evidence it cites (provenance-bound), else it reads `declared`/absent. Both are executor repairs; oracle credit stays CRO~X's, runtime fidelity CVO~X's.

**B4-AC5 -- THE EGRESS BOUNDARY** (`B4-ramh-1`, `B4-ramh-3`, `B4-mech-4`): the only egress is the AWS-side pull/build/run for this read-only measurement -- exactly what the word covers, quoted verbatim on the report; nothing enters the estate's python dependency set or any deployed artifact (requirements files diff empty; the estate python still reports graph_tool ABSENT after the job); nothing here reads the word as authorising other egress, spend beyond the printed job cost, or a shared-branch act.

**B4-AC6 -- MECHANISM, ON THIS FACE** (`B4-mech-1..3`, `B4-mech-5`): mech-1 the seat (spawned by `0.0.0_AB_MSTR`, one project = B4); mech-2 change-management -- if any AWS resource lands, an entry in `org/critical_paths/change_management/` opens at start and closes at completion (NEVER-2), and the infra clauses on this face are the architecture owner's (CTO~X 78099: encoded as written); mech-3 the oracle is not relaxed -- a clause that fails, fails; mech-5 the certifier never the author.

## LANE

Your own lane `org/tier2_senior/0.7.0_AE_CloudOps/**` holds the job definition, the deliverables and the report. **If a resource under `infra/aws/**` is needed, name the module path in your first report and `1.0.0_SA_CTO~X` grants the scoped `.owned-paths.yaml` row for `0.7.0_AE_CloudOps~X` on it for this TO's life** (the SHARED_CLOUD_OPS lane enumerates the base + ~A/~B/~C; ~X is not in it until granted); the first refused commit there is the exercise. Prefer a definition that needs no new infra resource (a CodeBuild project can be Terraform-managed under an existing module) and say which.

## BOUNDARIES

- No workstation Docker; no image pull to this device; no venv on this device.
- The oracle @b4caea27f0 is not edited, softened or reinterpreted here. Records first; the verdict is the oracle owner's.
- No fusion (WP-6 waits on the CONFORMS verdict, not on this TO).
- One job; teardown; cost printed. A standing pipeline or a schedule is out of scope and a NEVER-5 defect.

## REPORT

Route completion to `3.0.0_SA_CVO~X` and `4.0.0_SA_CRO~X`, cc issuer + `1.0.0_SA_CTO~X`, with: the precedent read; the product and its reason; the graph query citation; the image reference/digest/version from the running container; the population object's digest and count; the 25 per-run records' location and the gate lines; run time per run and total; the cost line; the teardown evidence; the requirements diff (empty) and the estate-python ABSENT line; the job id; the proof-of-spec instance VALID line; and **PUSH STATE as a MEASURED value** (ls-remote read). The issuer flips this face on the certifier's verdict; the oracle owner's CONFORMS/FAILS is a separate line.
