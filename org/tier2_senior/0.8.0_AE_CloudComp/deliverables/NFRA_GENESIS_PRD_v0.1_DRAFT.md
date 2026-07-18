# NFRA_GENESIS -- PRD v0.1 (DRAFT): the runnable "spin up a new company's semantic system" SDK

**Macro:** NFRA · **Project:** NFRA_GENESIS · **Author:** 0.8.0_AE_CloudComp~A (Andrew-direct 2026-07-18; "I drive + own it") · **Status:** DRAFT -> route to CTO for docs/architecture promotion + arch-gate · **Plan of record:** approved plan (`~/.claude/plans/`) -- this PRD is its gate-ready condensation.

---

## 1. Motivation
Opal built a complete compiled semantic system -- a versioned graph (Nessie/Iceberg -> Kuzu -> Trino), a C0->C3 compression ladder with a lossless-decompression fidelity gate, ~59 comp-tools, a substrate/layer model, and a closed self-learning loop, all honesty-gated. The SEMCTL charter's thesis (`NFRA_SEMCTL_PRD.md:52`) is that this is a *reference implementation of a general pipeline*, not code-specific. **Andrew-direct:** productize it into runnable tooling -- `genesis up <company>` spins up a new company's graph + ontology-binding + learning loop + tools on the proven stack.

## 2. End-state
One `company.yaml` manifest + one CLI stand up a new tenant: `genesis new|validate|up|verify|loop|status|down`. Acceptance (this pass): **local/sandbox proof** -- `genesis verify --local` proves the loop CLOSES on a scratch Nessie namespace + local Kuzu (zero new cloud spend); `genesis up --dry-run` proves TF validate/plan clean. Opal = the reference instance; no live second company this pass.

## 3. Core idea: PACKAGE + PARAMETERIZE, not rebuild
The machinery exists + is proven runnable. Generalization is narrow -- **exactly TWO bespoke-per-company pieces**:
1. **The recognizer keystone** -- front-end + recognizers -> C0/C1, on the proven `comp_recognizer_sdk.py` (`Recognizer` ABC; `emit_cse` makes an off-enum/provenance-less/non-decompressible CSE physically impossible).
2. **The binding adapter** -- concrete types -> archetypes; a per-company `canon-patterns.yaml`.
Everything else (the CSE algebra `cse_schema.py`, the fidelity/coverage gates `comp_ladder.py`, the graph infra, the loop, the tools, the marker-oracle) is reused mechanism, made tenant-neutral by the manifest. **Key insight:** a new company has no legacy extractors, so the recognizer-SDK IS its production compiler from day zero -- Opal's own re-platforming is out of scope.

## 4. What ships
- **`infra/system/sdk/`** (home; ANY_EXEC_OR_AE): README + the `genesis` CLI + `00_manifest`..`06_verify`.
- **`company.yaml` v1** (frozen at `00_manifest/schema.json`): identity/cloud/substrate/layers/recognizers/adapter/loop/variance_dimensions/honesty/governance. **Invariant:** a tenant may NOT add CSE algebra primitives (a governed shared version-bump only) -- validator-enforced.
- **The parameterized TF module** (`01_provision/`, extracted from the flat Opal `locals{}`-literal root -> `variables.tf` + a generated `company.auto.tfvars`; per-company state key; every ARN composed, no literal account) -- EXEC-LOCKED, routes to CTO.
- **The recognizer-SDK packaging** (`02_recognizer_sdk/`): one authoring surface + front-ends + `genesis new` scaffold; the RESOLVED_SEMANTIC (tree-sitter) tier honest-degrades until P6.
- **The packaged loop** (`04_loop/`): a 6-stage orchestrator WRAPPING the canonical modules (`comp_promote_lifecycle.py` etc.), never re-implementing.
- **The genesis comp-tool suite** (`05_tools/`) registered via the NFRA_COMPREG ATOMIC-BUNDLE law -- EXEC-LOCKED, routes to CTO.
- **`06_verify`**: the three-tier acceptance (`--local` no-cloud primary gate | `--sandbox` throwaway Nessie branch | `--live` post-up smoke).

## 5. Phasing (P0..P6; each independently exercisable)
P0 Charter + manifest v1 + validator + projector + CLI skeleton [**LANDED @cc810c93d**; `genesis validate sandbox` PASS] · P1 TF parameterization (module + variables; up --dry-run clean, zero Opal literals) · P2 recognizer-SDK packaging (genesis new; sample recognizer fidelity-passes) · P3 loop packaging (loop --tick --local runs 6 stages; materialize emits the loop-closing CSE) · P4 genesis up + real sandbox apply (retires the clean-apply-from-zero risk) · P5 genesis verify + tool suite (the load-bearing acceptance) · P6 (deferred, non-blocking): real tree-sitter front-end, slot the CTO-gated NFRA_ONTOLOGY vocab, enable marker-CAS.

## 6. Boundaries / ownership (NO duplication)
Depends on (does NOT rebuild): the compression MECHANISM (NFRA_SYSTEM/SEMCTL), the archetype VOCABULARY (NFRA_ONTOLOGY ~C -- a **pluggable versioned dependency**, NOT yet CTO-gated + an open relationship-vocab doctrine fork; GENESIS ships on `canon-patterns.yaml` v0.1 today, slots the gated vocab at P6), the recognizer framework (NFRA_COMPILERKIT), the graph substrate (NFRA_GLOBGRPH), the promote lifecycle (NFRA_PROMOTE), the tool-registration flow (NFRA_COMPREG). Generalizes the adapter PATTERN (CTO's canon-patterns). **Non-goals:** not authoring/gating the ontology; not re-platforming Opal's live graph; not extending the CSE algebra; not NFRA_SYSTEM's comp-system; not a store-abstraction/multi-cloud SDK; not a live production second company.

## 7. Governance / gating
Charter = an LD ledger entry (S3, design-first, Andrew-direct) -- mirror LD-0310. Owner 0.8.0_AE_CloudComp~A drives + owns; the SDK kit is AE-committable (`infra/system/**` ANY_EXEC_OR_AE); the exec-locked engine generalizations (the TF module, the comp-tool registration) route to CTO as normal SoD. **CTO arch-gate asks:** (a) the company.yaml v1 contract + the no-per-tenant-algebra-fork invariant; (b) the TF module boundary (tenant brings account/VPC/state-bucket as prerequisites; the module creates the rest); (c) the tool-registration bundle spanning `infra/system/sdk/**` + `org/modules/graph/**`; (d) confirm the ontology stays a pluggable dependency (no hard-freeze before its own gate). COO decomposes P1..P5 if a dedicated lane is later wanted (today: ~A drives).

## 8. Acceptance
`genesis validate <sandbox>` clean + `genesis up --dry-run` clean plan (grep-proof: no `313476888478`/`opal-globgrph` literals) + `genesis verify --local` all honesty gates green + the loop-closing materialize CSE proven + `genesis verify --sandbox` real-substrate closure torn down + `comp-manifest-check completeness` PASS on the genesis tool suite. Each phase has its own acceptance test (plan table).
