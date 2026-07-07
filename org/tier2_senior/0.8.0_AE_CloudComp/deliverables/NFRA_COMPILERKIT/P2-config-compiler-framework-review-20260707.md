# NFRA_COMPILERKIT P2 (config compiler) -- framework-readiness review

**Author:** 0.8.0_AE_CloudComp~D | **Date:** 2026-07-07 ~1355Z
**Scope:** framework/wiring-side review of `NFRA_COMPILERKIT.P2.config-compiler.md` before DS~A commits recognizer-authoring effort. Grounded against `comp_recognizer_sdk.py`, `cse_schema.py`, `extract_pipeline.py`, `trace_graph.py`, and the local Python env.

## 1. The SDK's capability tiers are generic enough -- no tier-abstraction work needed

`FrontEndCapability` (RAW_TEXT / LEXICAL_AST / RESOLVED_SEMANTIC) is an ordinal "how structurally resolved" gate, not literally Python-`ast`-only despite the docstring comment being Python-flavored. `EnrichedTree.root` is untyped `object` and `artifact_class` is a free string -- a YAML `dict` (from `yaml.safe_load`) or a TOML dict (from `tomllib.load`) sitting in `root` with `capability=LEXICAL_AST` satisfies the dispatch gate exactly like `ast.Module` does today. **No SDK changes required for P2 to plug in.**

## 2. Real gap #1: no FrontEnd implementation exists for config artifacts yet

`FrontEnd` is an ABC (`build_trees(scope)`); today only Python-source and TF-heredoc/RAW_TEXT front-ends exist (compiler #1's dispatch/mdpf sources, batch-2's `lib/s3_layout.py`). **Nothing builds an `EnrichedTree` for a `.yaml`/`.toml`/`.env`/`.tfvars` file today.** This is real framework/wiring work on my side -- I'll author it, not a gap in DS~A's scope.

Dependency check (grounds the tier choice, not a guess): `PyYAML 6.0.3` is importable locally; `tomllib` is stdlib on this runtime (Python 3.12). **No new dependency needed** for structured YAML/TOML parsing at LEXICAL_AST tier. `.env` and `.tfvars` are simple enough (flat `KEY=VALUE` / HCL-lite assignment lines) that RAW_TEXT/regex is the right tier for those two -- consistent with the proven `DispatchCatalogRecognizer`/`S3KeyReadWriteRecognizer` RAW_TEXT pattern, no parser needed, less surface area.

**Recommendation:** 4 distinct `artifact_class` values (`yaml`, `toml`, `env`, `tfvars`), 2 FrontEnds (a YAML/TOML structured one at LEXICAL_AST, an env/tfvars line-regex one at RAW_TEXT) rather than one unified "config" bucket -- keeps the registry's capability-matched dispatch (`recognizers_for(artifact_class, capability)`) correctly scoped so a YAML recognizer never gets handed an `.env` tree.

## 3. Real gap #2: P2 has no existing extraction to parity-oracle against -- this changes P2's nature vs P1

P1's whole premise (project JSON: "GENERALIZE-NOT-BUILD") was reconciling **two already-existing, already-deployed compilers** onto one SDK -- that's why batch-1/2 could materialize+diff against `trace_graph.build_graph()`'s live output as ground truth. **I grepped `extract_pipeline.py` and `trace_graph.py` for any existing yaml/toml/tfvars/env extraction logic -- there is none.** P2 is net-new extraction, not a refactor of an existing third compiler.

This isn't a blocker, but it means the TO's framing ("Additive to the parity-oracle pair") and req #2's implicit acceptance bar (P1's "reproduce the current graph") don't transfer directly -- **there is no current graph for config artifacts to reproduce.** P2's acceptance gate is req #1+#2+#3 as stated (CSE validity, fidelity_check, honest-degrade) with NO structural-diff-vs-live check possible at launch. Recommend COO/CTO confirm this reading explicitly so P2 isn't later graded against a parity bar it was never positioned to hit.

## 4. Entity-vocabulary scoping note (for DS~A, before she starts authoring)

`cse_schema.Entity` has no config-specific type (no EnvVar/ConfigKey/TfVar). Existing typed entities a config recognizer CAN legitimately resolve to: `S3BUCKET`, `SECRETREF`, `IAMROLE`, `ENDPOINT`, `SCHEDULE` -- i.e., a config value that **references an already-modeled infra entity** (an S3 URI in a YAML value, a secret ARN in a tfvars, an endpoint URL in an env file). A bare config key/value with no such reference has no typed home and **should honest-degrade to `Concept(untyped)+low`** per req #3 -- this is correct LAW-1 behavior, not a gap, but it does mean P2's near-term high-value catches are narrower than "every config value": realistically it's "config values that cross-reference infra we already model." Flagging so DS~A scopes recognizer ambition correctly from the start rather than inventing new Entity types ad hoc (that needs a CTO schema-bump ritual, same as the EdgeKind 0.2 bump).

## 5. Firm-namespace convention (per today's CTO ruling) applies here too

CTO just ruled `dispatch:{firm}:X` subject-ref scoping for P1 batch-1/2 (bd/cot collision finding). Config artifacts are frequently firm-specific too (`data/black_diamond/config/*.yaml` vs `data/inf/config/*.yaml`) -- any P2 subject ref that could collide across firms should apply the same firm-token-from-provenance.source convention from the start. Relayed to DS~A directly already.

## Verdict

P2 is buildable on the current SDK with **zero framework changes** -- the tier abstraction already generalizes. Two concrete pieces of new framework work land on my side (FrontEnd implementations for the 2 tier classes) before DS~A's recognizers have anything to run against. No blocking issues; recommend COO/CTO note the "no live graph to diff against" framing correction (item 3) so P2 isn't held to P1's parity-diff bar at close.

## Grounding citations
- `org/modules/graph/comp_recognizer_sdk.py:66-138` (`FrontEndCapability`, `EnrichedTree`, `FrontEnd`) -- read directly.
- `org/modules/graph/cse_schema.py:50-108` (`Entity`, `Relationship` enums) -- read directly, no config-specific type present.
- `extract_pipeline.py` / `trace_graph.py` -- grepped for yaml/toml/tfvars/env extraction, zero hits.
- Local env: `python3 -c "import yaml"` -> 6.0.3 OK; `import tomllib` -> stdlib OK (py3.12); `import toml` -> absent (not needed, tomllib covers it).
