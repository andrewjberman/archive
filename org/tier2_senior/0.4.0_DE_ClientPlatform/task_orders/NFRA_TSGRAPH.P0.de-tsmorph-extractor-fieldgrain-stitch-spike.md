<to_id>NFRA_TSGRAPH.P0</to_id>
<project>NFRA_TSGRAPH</project>
<title>P0 SPIKE — prove the TS-semantic substrate: ts-morph extractor on ONE page-slice + the field-grain stitch (one gold field -> one rendered field, end-to-end)</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>0.7.0_AE_CloudOps (graph-platform: the CodeBuild-run + Nessie/Iceberg->Kuzu emit = the inc-2b drift-producer pattern it just shipped; lean on it for the plumbing, you own the TS extractor)</consult>
<issued_by>2.0.0_SA_COO (Andrew greenlight 2026-06-17 "yes go ahead"; CTO research brief docs/briefs/intra-typescript-semantic-graph-research-20260617.md = b95089ea3)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>pending</status>
<priority>P0 spike — Andrew-direct, low-cost/high-information. The go/no-go gate for the whole NFRA_TSGRAPH project + the input to CTO's formal PRD (build-vs-buy decided by THIS spike's measured evidence).</priority>

<context>
The frontend graph is built by PYTHON REGEX over TSX (comp-tools.yaml: "ts-morph absent on this machine") -> coarse (whole-COMPONENT/ENDPOINT nodes), brittle, semantically blind. That caps all 3 Andrew goals (fine backend->TS field-grain lineage / data-consumption clusters / TS lexical bug-model) AND caused the 06-17 D8 surface-scan FP (portal-AST key-space never intersects the AWS-only derive graph). The fix = a compiler-grade TS-semantic substrate (TS Compiler API via ts-morph) emitting a fine-grained graph into the SAME Nessie->Kuzu platform. P0 proves the spine on ONE slice before any full build.

Andrew's 4 framing decisions are RESOLVED (per CTO brief §11 + registry): run-site = portal CodeBuild (NOT the Python graph machine); build-vs-buy = DEFER to this spike's measured evidence; scope = React-focused v1; spin-up = yes. So this TO is pure execution of §10's P0.
</context>

<deliverable>
A ts-morph / TS-Compiler-API extractor that runs over ONE page-slice and emits the CTO-brief §3 node/edge schema for that slice into the Nessie->Kuzu platform, PROVING the field-grain stitch end-to-end on a SINGLE field.

PAGE-SLICE: recommend the model-portfolios benchmark surface OR an advisor-intelligence page (clean firm-separated data, a known gold->served->fetch->render chain). CTO confirms the exact slice + the one field at GO (their arch-call on the cleanest spine to prove).

PROVE (the one-field end-to-end stitch, each "->" a RESOLVED edge not a regex guess):
  gold-field -> served-artifact-field -> fetch-return-type-field -> adapter-mapping(FLOWS_TO) -> hook-data -> component-prop -> (PROP_PASSES)* -> JSX-RENDERS-field
Emit the §3 nodes (Module/Symbol/TypeDecl/ReactComponent/Hook/Prop/DataFetch/Field/JSXElement + the Expr nodes the one stitch needs) + the resolved edges (REFERENCES/HAS_TYPE/FLOWS_TO/FETCHES/PROP_PASSES/RENDERS) for the slice. Symbol+type resolution must be REAL (TypeChecker getSymbolAtLocation / getTypeAtLocation), not string-matched.
</deliverable>

<run_site>
Portal CodeBuild (the inc-2b drift-producer pattern, ask 0.7.0_AE): the extractor is a Node/TS tool in the portal repo (bun + @typescript-eslint toolchain already there). It runs in CodeBuild, emits JSON to S3, the nightly/derive picks it up into Nessie->Kuzu. Do NOT try to put ts-morph on the Python graph machine (the blocker the brief sidesteps). For the SPIKE, a local CodeBuild-equivalent run (bun + ts-morph in the portal repo) emitting the slice JSON is fine to prove the spine fast; wire the actual CodeBuild job only if the spike says GO.
</run_site>

<acceptance_criteria>
AC1 — EXTRACTOR RESOLVES: the ts-morph extractor resolves symbols + types for the slice (an import/re-export resolves to its def; a fetch's return type yields its Field set; a prop's type resolves) — demonstrably better than the regex baseline (show 1-2 concrete cases regex gets wrong/coarse that the Compiler API gets right).
AC2 — FIELD-GRAIN STITCH PROVEN: the single gold-field -> JSX-render-of-field chain is traversable as a connected path of resolved edges in the emitted graph. The "hard seam" (served-JSON-field -> TS-type-field at the fetch boundary) is bridged via the fetch return type + adapter FLOWS_TO + the React-Query key. Where something is genuinely unresolvable (dynamic URL/key, `as`-cast), it's marked `unresolved` and VISIBLE (platform "no silent Unknown" law) — never a false edge.
AC3 — EMITS INTO THE PLATFORM: the slice's nodes/edges land in Nessie->Kuzu (consult 0.7.0_AE) + a comp-kuzu Cypher query returns the stitch path. Keyed CONSISTENTLY with the cloud/trace graph (so it stitches, fixing the D8 key-space class — show the slice's DataFetch->endpoint->Lambda join works).
AC4 — MEASURED GO/NO-GO (the spike's product): report (a) GO/NO-GO on the substrate w/ evidence; (b) measured INDEX COST (extractor run-time on the slice, extrapolated to full-portal estimate — feeds the incrementality design §8.6); (c) FIELD-GRAIN FIDELITY vs the regex baseline (what the semantic graph catches that regex misses/falses); (d) SCIP-TRANSFORM-EFFORT estimate (the Layer-A buy-vs-build evidence: how much of the symbol/reference backbone scip-typescript would give vs hand-rolling — the §4 / §11.2 decision CTO's formal PRD turns on).
</acceptance_criteria>

<verification_discipline>
Platform law (brief §8.8): the semantic graph is a minutes-stale LABELED traversal surface, NEVER a read-your-own-change verification substrate. Verify the extractor's output against the actual built artifact / the running portal (the F5 rule), not the graph. Carry the provenance-header + freshness contract. No silent Unknown (mark unresolved VISIBLE, like comp-platinum's `url:(not resolved)` + the inc-2b coverage guard).
</verification_discipline>

<ravc2>
RAVC2 to COO (CC CTO): the extractor + the slice's emitted graph + the proven stitch path (comp-kuzu query output) + the AC4 measured go/no-go report. CTO close-reviews the substrate verdict (it feeds their formal PRD). On a GO verdict -> P1 (full-portal extractor + re-back comp-types/comp-transform with parity checks); on NO-GO -> the report says why + the alternative (SCIP-primary / etc.).
</ravc2>

<lane_note>
DE-primary (you own the ts-morph extractor + the portal-TS semantics — the hard/core part). 0.7.0_AE consult for the CodeBuild-run + Nessie/Kuzu emit (its globgrph platform; the inc-2b CodeBuild->S3->derive pattern is the template — it's a small lift for AE since it just built it). If CTO redirects the lane (e.g. AE-primary) at GO, adjust. The org/modules/graph/* extractor code + portal-repo CI = your authoring surface; the Nessie write-path = AE-owned (commit-through-owner if you touch derive code).
</lane_note>
