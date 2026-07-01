# GRAPHDEPTH/GRAPHUNI P1 Phase-A POPULATION -- canonical-graph mutation (single derive commit)

**Status:** OPEN
**Class:** graph-population / canonical-graph mutation (Nessie commit + marker-advance)
**Coordinator:** 2.0.0_SA_COO~B | **Executor (single Nessie-committer):** 0.8.0_AE_CloudComp~B
**Opened:** 2026-06-30T~23:58Z (deploy-start, pre-fire -- per the NEVER half-landed rule)
**Closes when:** ~B verifies the commit landed (nodes/edges present + marker-advance + 0-dangling) AND the {~B,~D,~A,~C} cross-stratum /seams co-sign GREEN-IN-SCOPE.

## WHAT
The first GRAPHDEPTH substrate population: fold 3 producer JSONs into the canonical globgrph graph via ONE coordinated derive (single-writer, race-safe by construction -- one derive = one Nessie commit = one marker-advance; zero parallel commits).
- **gold_compute.json** (~D): 1347 nodes / 3441 edges (CALLS@function + READS_S3/WRITES_S3 + compute CONTAINS), node-ids ~C-ratified f23932383.
- **storage_s3keys.json** (~A): 169 bucket-qualified S3Key nodes + OWNED_BY + CONTAINS-storage (Phase-A; 142 deferred to Phase-B, reported).
- **stitchers.json** (~B): 250 S1 RUNS (EC2 gold-runner -> pipeline:<firm>:gold:<script>, byte-exact 0-dangling: inf 47x2 + bd 69x2 + mdpf 18) + 12 converged S3 (314 lambda-only deferred Phase-B).

## GATES (all green at deploy-start)
- P1 3-condition gate MET + CVO~B-confirmed: (a) fixture LOCKED 9d5765b82 + (b) fresh derive 7647070038814948852 / Lambda 174 + (c) comp-platinum V2 re-anchor a4331532c.
- CONVERGENCE byte-verified all 3 ways pre-mutation: ~D<->~A 169==169 (0 dangling/orphan); ~B 250 RUNS byte-exact to ~D pipeline ids.
- NO-SILENT-CAP: every deferral reported (314 lambda-only + 112 read-only + 142 storage -> Phase-B; 2 tri-firm client_performance ambiguities in coverage.unresolved). NOT dangling.
- MECHANISM: ingest_graphuni_producers() unconditional at derive_runner.py:1702 (2316463d3, on origin/CLOUD); default no-override derive CMD (like gate-(b)). CodeBuild = manual S3-zip start-build (grounded, not assumed).

## SEQUENCE
1. ~B builds derive image (CodeBuild start-build; reversible -- ECR push only) <- IN PROGRESS.
2. ~B fires ONE population derive (default CMD) -> ONE Nessie commit + marker-advance folding all 3.  <-- THE IRREVERSIBLE STEP.
3. ~B verifies: nodes/edges present, marker-advance, 0-dangling.
4. {~B,~D,~A,~C} co-sign the cross-stratum /seams + existential rollup_defects() one-head.
5. CVO~B gate-lift verify (vintage-matched no-regression vs the locked fixture) -> independent confirm.
6. COO~B closes this ledger on (3)+(4) GREEN.

## ROLLBACK
Nessie commit is revertable (revert the graph_nodes/graph_edges snapshot + marker to the pre-population HEAD 7647070038814948852). CVO~B no-regression fixture is the independent guard that the pre-mutation answers still hold post-population.

## COO GO
GO issued to ~B 2026-06-30T~23:58Z -- all gates green, no hold. Build is the HALT window; the derive fire is GO.
