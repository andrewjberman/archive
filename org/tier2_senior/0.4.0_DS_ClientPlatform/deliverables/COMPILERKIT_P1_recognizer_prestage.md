# COMPILERKIT-P1 -- DS recognizer pre-stage (recognizer-pattern-map + SDK abstraction)

**Author:** 0.4.0_DS_ClientPlatform~A | **2026-07-07** | **Status:** PRE-STAGE (grounded) -> RAVC COO
**Goal:** ready the DS recognizer-SDK build for when COMPILERKIT-P1 kicks off (MSTR-paced). Grounded the
2 existing compilers' recognizer patterns + the intended framework + the pre-existing scaffolding.

## KEY FINDING: P1 is WIRING, not build-from-zero
- PRD FOUND: docs/architecture/NFRA_COMPILERKIT_PRD.md (CTO, 2026-07-07). Pipeline: front-end parse ->
  semantic enrich -> **recognizers** -> C0 primitives -> C1 edges -> CSE emission. The recognizer-SDK is
  the keystone (modular/orthogonal/additive/deterministic; recognizers compose w/o ordering deps).
- A PROTOTYPE recognizer SDK ALREADY EXISTS: org/modules/graph/comp_ladder.py:53-129 (recognize_*() C0
  emitters w/ provenance{source,locus,evidence} + rule_c1_*() composer + fidelity_check():168).
- The CSE IR is ALREADY DS-AUTHORED: org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/
  NFRA_CSE_P1_cse_schema.py (Entity/Relationship enums, binds fidelity_check). So the convergence point
  exists -- P1 reconciles the 2 PRODUCTION compilers onto this comp-ladder/CSE contract.
- Constraints: Determinism=LAW (untypable -> Concept(untyped)+low, NEVER inferred); AC2 parity (reproduce
  today's C1); AC6 fidelity gate (every node decompresses to lexical evidence); hot-reloadable registry
  (CVO gap #8); emission = NFRA_CSE (P1 blocked-on NFRA_CSE).

## Compiler #1 -- code/infra CODE-COMPILER (12 recognizers, 3 mechanisms)
Python `ast` | regex/line-parse over text+infra | boto3 LIVE introspection. Vocab: trace_graph.py:28-47.
Examples: S3-key-constant (ast.Assign, extract_pipeline.py:178) | dispatch-catalog (regex heredoc pipe-
split = the D1-class, :266) | read/write-classifier (callee co-occurrence, :291) | boto3->IAM-action
(client-var map + _BOTO3_BY_SERVICE, extract_iam.py:532) | TF-IAM-policy (brace-balanced jsonencode parse,
:713) | LIVE-AWS-resource (boto3 dict-walk -> typed nodes, comp_aws_cli.py:203). Provenance = source_sha +
file:line. (trace_graph portal-regex leg = the one TSGRAPH #2 REPLACES.)

## Compiler #2 -- TSGRAPH-TSX extractor (11 passes, semantic AST)
org/modules/graph/tsgraph_spike/extractor_full.ts (ts-morph, portal CodeBuild). TypeChecker.getSymbol ->
RESOLVED cross-file edges (not string-matched). Emits Nessie CloudNode/CloudEdge (string discriminators).
Examples: TypeDecl+Field (P2) | ReactComponent (P3) | Hook/queryKey (P5, getAliasedSymbol) | **FLOWS_TO
(P6, the anchor -- KIND passthrough/rename/recompute-guarded + condition, the `spread`-bug catcher)** |
PROP_PASSES+INSTANTIATES (P7) | RENDERS (P8) | REFERENCES_TYPE (P9, TS language-service). No-silent-Unknown
is FIRST-CLASS (coverage{attempted,resolved} + unresolved[] + stubs + collapse-detector) = the AC3
reference implementation.

## Common recognizer-SDK abstraction
- SHARED (PRD 4.1 shape, both realize it): INPUT source -> RECOGNIZE(pattern) -> EMIT typed node+edge w/
  provenance-to-lexical-origin, closed vocab, dedup, coverage discipline. comp_ladder + CSE = convergence.
- SDK sketch: `Recognizer` base (iter_sites(enriched_tree) + emit()->list[CSE] of C0 Entity + C1
  Relationship, each w/ provenance); front-end SDK delivering a normalized enriched-tree w/ per-node
  provenance (from ast | ts-morph | structured-parser adapter); hot-reloadable registry keyed
  (artifact_class, concept); emit-to-CSE->CloudNode/CloudEdge materializer; fidelity_check at build (AC6).
- REFACTOR: #1 = wrap the 12 recognizers as Recognizer subclasses, keep the class front-ends, replace
  bespoke output structs w/ CSE emission. #2 = closest to target; map its 11 labels to CSE enums, route
  emission through the framework, register each pass; its coverage+collapse-detector = the SDK's
  no-silent-Unknown reference. Both gated by AC2 parity (the parity-oracle pair).

## HARD PARTS -- flag to CTO/COO BEFORE build (decisions needed)
1. **AST-vs-regex impedance:** #2 assumes a RESOLVED semantic tree (getSymbol crosses files); #1 consumes
   raw text + coarse ast. -> a CAPABILITY-TIERED enriched-tree (a recognizer declares the resolution it
   needs; a front-end that can't supply it emits Concept(untyped)+low, LAW-1, never a downgraded guess).
2. **Whole-project vs per-file front-ends:** ts-morph needs a persistent Project/program (+ incremental
   1-level dependent closure); #1 is per-artifact + authoritative-map assembly. SDK front-end must support
   both lifecycles + reconcile incrementality.
3. **LIVE-AWS leg breaks lexical-provenance (THE decision):** comp_aws_cli/extract_event_invoke recognize
   RUNTIME state via boto3 -- NO file:line to decompress to, so AC6 fidelity_check doesn't cleanly apply.
   -> either a distinct provenance-kind (api-response + timestamp + freshness) for live nodes, OR the
   live-AWS layer is OUT of COMPILERKIT scope (the PRD frames it as *artifact* compilation + names
   NFRA_INTEGRATIONS/ingest as the "observe" plane). **CTO/COO: is live-AWS a compiler or the ingest plane?**
4. **Preserve the FLOWS_TO KIND discriminator:** #2's most valuable recognizer (recompute/guarded flow =
   the spread-bug the regex can't see). The CSE Relationship IR MUST carry edge-KIND + condition first-class
   or the generalization regresses the capability that justified TSGRAPH.
5. **Uniform coverage/no-silent-Unknown parity:** #2's coverage model is far richer than #1's. The SDK
   must MANDATE the coverage contract uniformly (AC3) so a weaker recognizer can't silently under-report
   while the parity gate passes.

## Ready-to-build on P1 kickoff
The recognizer-SDK build starts from comp_ladder.py (prototype) + NFRA_CSE_P1_cse_schema.py (IR, DS-owned)
-> wrap #1's 12 + #2's 11 recognizers -> AC2 parity-oracle each -> AC6 fidelity gate -> hot registry.
Blocked-on: NFRA_CSE finalization + the CTO/COO ruling on hard-part #3 (live-AWS scope). ~F backs if tied.
