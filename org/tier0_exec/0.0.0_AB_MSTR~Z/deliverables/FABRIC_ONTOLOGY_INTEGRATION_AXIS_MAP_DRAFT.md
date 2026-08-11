# Fabric Ontology Integration — Axis Map v1 (all 3 laptop deliveries folded; per-row concurrence open)

**Mandate:** Andrew-direct 2026-08-11 ~1817Z (verbatim @a7136a5aa9): MSTR-to-MSTR joint
integration, "formalized to some extent"; site-Z instruments work "confined to comp tooling";
laptop work held in the interim (narrow-operative read: new semantic-formalization acts frozen,
in-flight build/QA continues — surfaced at Andrew's terminal both sides, uncorrected).
**Authors:** drafted by 0.0.0_AB_MSTR~Z; laptop concurrence per-row via CRO~B + CVO input
routed through laptop MSTR (no fifth author). Final home: docs/architecture/
FABRIC_ONTOLOGY_INTEGRATION.md, committed by laptop MSTR on CLOUD.
**Verdict vocabulary:** SAME-AXIS-CONFLICT (one axis, two formalizations — needs one canonical
home) · ONE-AXIS-TWO-GRAINS (needs a composition rule) · SAME-WORD-DIFFERENT-AXIS (needs
namespacing) · ADJACENT-COMPATIBLE (needs a separation discipline, already written or to write)
· DISJOINT (no act).

## 1. Inventory register

**Site-Z (all origin/SITEZ):** ssot_establishment.schema.json @22ce467d37 (rectangle / cell /
patch / relations / constraints / run_manifest / rubric / verifier_packet); certification
protocol (seal-at-plant-time, attempts accumulate, PASS / PASS-WITH-REFUSAL / VOID; live
specimen certification.attempt1.VOID.json); OPAL_ANALYST PRD §9.8.1 method classes A–J;
projects/ATOM_DECOMP package + workflows/atom_decomposition/runs/INDEX.json; W0/W1 run records.

**Laptop (delivery 1+2 of 3; all origin/CLOUD):** ATOM_DECOMP method package @d5eda6112f incl.
DOMAIN AXIS PACK 01 (atoms A1–A5 + composition law); PATTERN SPEC v1.0 @d272021791 (9
structural atoms) + §6 shape-transposition doctrine @6e180df78e; SSOT_RECON_MATRIX (cell-state
lifecycle); SYSTEM_DEFINITIONS ratified term registry (comp-estate --definitions);
Kimi SVP contract-v2 artifacts + ratification record; taxonomy law (Rule 24 + R-0006/R-0009);
proof-of-spec layer; P5 debt-identification methodology (liveness-state × disposition schema)
@db365bb06c; Rule-25 dormancy vocabulary @36c3104717/@546e7cb0b5 (LONG-TTL-LIVE ·
CLOSED-PERIOD-IMMUTABLE · build-artifact kind). **PENDING: CRO~B current-state pack + CVO
Kimi-SVP formal artifacts (delivery 3).**

## 2. Axis map (rows final only on per-row laptop concurrence)

| # | Concept | Site-Z formalization | Laptop formalization | Verdict | Remedy / canonical home |
|---|---|---|---|---|---|
| 1 | "cell" | RECTANGLE-CELL: entity_id × field; INTENT = fact TRUTH-STATE (MEASURED/UNMEASURED/INFERRED/NOT_MEASURABLE), evidence-carrying | RECON-CELL: pipeline × product × pattern-leg; INTENT = recon-claim LIFECYCLE (OPEN/HELD/DELIVERED/CERTIFIED) | **SAME-WORD-DIFFERENT-AXIS** (grain AND intent differ) | Namespace, never merge: **rectangle-cell** / **recon-cell**; both registered in SYSTEM_DEFINITIONS |
| 2 | Certification vocabulary | PASS / PASS-WITH-REFUSAL / VOID = outcome of ONE attempt; run terminal state separate (run_manifest.status OPEN/DRY/CERTIFIED/ABORTED) | CERTIFIED (+ CERTIFIED-WITH-ONE-REFUSAL irregular) = claim/run terminal state; CVO structural map concurs: PASS≈CERTIFIED, PASS-WITH-REFUSAL≈CERTIFIED-with-cells-REFUSED, **VOID≈INSTRUMENT-INVALID (a NON-VERDICT)** | **ONE-AXIS-TWO-GRAINS** (+ parity-bar grammar as a third related surface, carried explicitly, not merged — see row 14) | Composition rule: terminal CERTIFIED is reached via a PASS or PASS-WITH-REFUSAL attempt; VOID/INSTRUMENT-INVALID attempts accumulate without advancing. **RECONCILE VOID FIRST (CVO's order): the two fabrics must spell NON-VERDICT identically before anything else — a kill-chain that reads a non-verdict as a pass is the failure this row exists to prevent.** Home = ssot_establishment.schema.json + SYSTEM_DEFINITIONS |
| 3 | patch vs structural atoms | patch = change-unit, merges ONLY through the validator | 9 structural atoms = per-pipeline conformance REQUIREMENT-predicates, remedied by build acts | **ADJACENT-COMPATIBLE** | Separation already written both sides; joint doc cites both lines |
| 4 | Method package identity | projects/ATOM_DECOMP + skill (site-Z landed schema amendment @22ce467d37) | Same package lineage @d5eda6112f (laptop-authored origin) | **ONE ARTIFACT, TWO EDIT STREAMS** | Single canonical file, edits land via the ATOM_DECOMP lane (MSTR/CRO/CRO~A) regardless of authoring fabric — the route exercised today |
| 5 | Term/axis registry | (none independent — consumes) | SYSTEM_DEFINITIONS via comp-estate --definitions, ratified | **DISJOINT (single home exists)** | SYSTEM_DEFINITIONS is THE registry; every new axis/vocab either fabric mints registers there or is a Build-Ladder rung-2 violation |
| 6 | Liveness/dormancy semantics | rectangle cells measure artifact freshness as facts (e.g. smartx frozen-50-trading-days finding, NOT_MEASURABLE disposition discipline) | Rule-25 dormancy vocabulary: 90-day default + exception KINDS (LONG-TTL-LIVE / CLOSED-PERIOD-IMMUTABLE / build-artifact) | **ADJACENT-COMPATIBLE** (fact-measurement vs classification vocabulary) | Site-Z rectangles CITE Rule-25 kinds in disposition cells rather than minting liveness words; kinds live in SYSTEM_DEFINITIONS |
| 7 | Recon matrix vs rectangle | rectangle = truth artifact of a decomposition subject | SSOT_RECON_MATRIX = CTO oversight tracker over 6 legs | **ADJACENT-COMPATIBLE** (workflow tracker vs truth artifact) | Tracker rows may cite rectangle/certification refs; never the reverse |
| 8 | "Kimi Semantic Vertical Pipeline" (the name) | (consumer only) | Andrew's name for the laptop's semantic-evolution surface (Kimi/K3 daily estate-report pipeline + K-call ontology work); NO artifact carries the literal name; CVO owns the loop, CRO~B the validation mandate | **GLOSSARY ROW** | One glossary entry in the joint doc + SYSTEM_DEFINITIONS registration of the name → artifact set |
| 9 | CRO~B formalization stack (substrate model + deterministic cascade @14a955257f, anchor-catalog step-0 @164692f9be, codebase/ms extractor gap spec, CONTENT_MODULE_DESIGN @9b4d484132; four ratified domains api-serving/artifact-serving/observability/ui-dataflow + 90/9/1 cascade @7c1b7a8705) | (none — site-Z has not touched this surface) | APPROVED-BUT-HELD; the named hold-release item | **DISJOINT today; rows 10–13 govern its contact points** | Releases on Andrew's ratification (boundary §3); its vocabulary registers in SYSTEM_DEFINITIONS at dispatch |
| 10 | **Source-of-record FORMAT for formalized truth** | RECTANGLE/PATCH family (grid decomp of a fact table; validator-enforced) | Ontology canon: NFRA_ONTOLOGY_C2C3_CANONICAL.yaml + cover + resolver (graph/relatedness decomp over docs+code); a C3.i inventory is EXPRESSIBLE AS a rectangle | **THE ONE ROW NEEDING A WORKING SESSION** — two formats claiming one office | Proposed office split, to be tested not assumed: rectangle family = truth artifact OF A DECOMPOSITION RUN (bounded subject, run-stamped); ontology canon = STANDING estate ontology (continuously maintained). Bridge: a run's certified rectangle may EMIT canon updates; canon never hand-edits a rectangle. CRO~B + CTO~Z adjudicate per CVO's collision-3 caution (test same-axis before reconciling — a forced merge manufactures a collision) |
| 11 | Structure-axis vocabulary (legislated twice, same day) | M-5 `relations` (edge findings inside a rectangle) + M-9 `structural_changes` (typed patch path) | Ratified domains + substrate {aws\|portal\|codebase\|ms} (estate topology vocabulary) | **ADJACENT-COMPATIBLE, pending laptop per-row read** | Namespace by scope: substrate/domain words are ESTATE-level; rectangle `relations` entries CITE them in `relation_type`/`endpoints`, never re-coin |
| 12 | The shared enums (status: MEASURED/UNMEASURED/INFERRED/NOT_MEASURABLE — VERBATIM identical both sides; evidence shape near-identical incl. CLASS/INSTANCE law) | defined in ssot_establishment.schema.json $defs | defined AGAIN in battery/prompt contracts | **FORKED-VOCABULARY RISK (identical today, divergent by default)** | Single-source: the schema $defs is the machine SSOT; laptop battery/prompt contracts CITE it (path+commit); enum registered once in SYSTEM_DEFINITIONS; any change lands via the ATOM_DECOMP lane and both fabrics inherit |
| 13 | 90/9/1 cascade (deterministic→inferential→user construction stages) vs method classes A–J | §9.8.1 classes A–J | 90/9/1 cascade @7c1b7a8705 | **POSSIBLY ORTHOGONAL — laptop declared A–J UNREAD** | Laptop reads A–J, returns a per-row verdict; no action before that read (an unread-basis verdict is the exact class this exercise exists to catch) |
| 14 | Verdict axes that must NOT merge | attempt-outcome (PASS/PASS-WITH-REFUSAL/VOID) + run terminal (OPEN/DRY/CERTIFIED/ABORTED) | bundle adjudication lifecycle (PENDING/signed/FAILED) + per-criterion VALID/INVALID + parity-bar grammar (MATCH-CLEAN/MATCH-KNOWN-WRONG/DIVERGE/DIVERGE-SOVEREIGN) | **THREE-PLUS DISTINCT AXES — DO-NOT-MERGE row** (CVO collision-2) | The joint doc lists them side-by-side with intent statements; merging any two is the Rule-24 same-grain violation this exercise catches |

## 3. The written boundary (Step 3 — the paragraph both fabrics carry)

> **Site-Z's instruments atom_decomp program is CONFINED TO COMP TOOLING** (Andrew-direct
> 2026-08-11 @a7136a5aa9: "If you stay confined to comp tooling, I think it can work"): its
> subjects are comp-* tools and their registries/validators ONLY. The supervision/broker
> cluster (liveness, watcher, stimulus/fabric-check instruments) is **NOT pre-authorized** and
> requires Andrew's word post-integration. Laptop-side, the hold ("I will hold work on the
> laptop fabric in the interim") is **narrow-operative**: new semantic-structure FORMALIZATION
> acts are frozen — named queue item: CRO~B's substrate/anchor-catalog formalization
> (step-0 anchor-type extension, the four ratified domain names, the coordinate schema, and
> the codebase-extractor's VOCABULARY half), UNDISPATCHED at COO staffing, **released by
> Andrew's ratification of this integration** — while in-flight build/QA continues.
> B6-1/B6-2 and the extractor's build mechanics continue as in-flight build per this
> paragraph's own build/QA clause. *(Precision per CRO~B tranche-1: B6-1/B6-2 is PURE BUILD —
> the F3 capture uploader's upload leg + device schedule, zero semantic-structure content —
> and is a different artifact from the extractor, whose vocabulary half alone is frozen.)*
> Ontology axes are
> minted in ONE place per axis (SYSTEM_DEFINITIONS registration mandatory); the ATOM_DECOMP
> method package is one artifact edited through its owned-paths lane from either fabric.

## 4. Shared DNA (grounded by CRO~B against @22ce467d37 — the reason integration is cheap)

Status enum VERBATIM identical; evidence shape near-identical ({instrument, locator, vintage,
denominator, count_grain CLASS|INSTANCE} ≈ {instrument, intent_denominator, boundary} + same
CLASS/INSTANCE law); same sovereignty triangle (Andrew ratifies / CVO certifies); site-Z's
schema provenance already cites base-CRO's SSOT protocol rulings. The fabrics diverged in
FORMAT and FILE, not in doctrine — row 12's single-sourcing converts the identity from
coincidence to invariant.

## 5. Open to close before ratification

- Laptop per-row concurrence via CRO~B + CVO (rows 1–14; row 13 needs their A–J read first).
- Row 10 working session (CRO~B + CTO~Z): the office split between rectangle family and
  ontology canon — tested, not assumed.
- Row 2's VOID/INSTRUMENT-INVALID spelling reconciled FIRST within the cert row.
- Joint doc assembled from this map → laptop MSTR commits on CLOUD → **Andrew ratifies →
  laptop hold lifts (row-9 stack releases first).**
