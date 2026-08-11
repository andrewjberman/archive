# Fabric Ontology Integration — Axis Map (DRAFT, pending laptop delivery 3 of 3)

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
| 2 | Certification vocabulary | PASS / PASS-WITH-REFUSAL / VOID = outcome of ONE attempt; run terminal state separate (run_manifest.status OPEN/DRY/CERTIFIED/ABORTED) | CERTIFIED (+ CERTIFIED-WITH-ONE-REFUSAL irregular) = claim/run terminal state | **ONE-AXIS-TWO-GRAINS** (attempt-outcome feeds lifecycle-terminal) | Composition rule: a run/claim reaches CERTIFIED via a PASS or PASS-WITH-REFUSAL attempt; VOID attempts accumulate without advancing; laptop's CERTIFIED-WITH-ONE-REFUSAL := terminal state whose certifying attempt was PASS-WITH-REFUSAL (regularizes the irregular). One vocabulary, grain-qualified, home = ssot_establishment.schema.json with SYSTEM_DEFINITIONS registration |
| 3 | patch vs structural atoms | patch = change-unit, merges ONLY through the validator | 9 structural atoms = per-pipeline conformance REQUIREMENT-predicates, remedied by build acts | **ADJACENT-COMPATIBLE** | Separation already written both sides; joint doc cites both lines |
| 4 | Method package identity | projects/ATOM_DECOMP + skill (site-Z landed schema amendment @22ce467d37) | Same package lineage @d5eda6112f (laptop-authored origin) | **ONE ARTIFACT, TWO EDIT STREAMS** | Single canonical file, edits land via the ATOM_DECOMP lane (MSTR/CRO/CRO~A) regardless of authoring fabric — the route exercised today |
| 5 | Term/axis registry | (none independent — consumes) | SYSTEM_DEFINITIONS via comp-estate --definitions, ratified | **DISJOINT (single home exists)** | SYSTEM_DEFINITIONS is THE registry; every new axis/vocab either fabric mints registers there or is a Build-Ladder rung-2 violation |
| 6 | Liveness/dormancy semantics | rectangle cells measure artifact freshness as facts (e.g. smartx frozen-50-trading-days finding, NOT_MEASURABLE disposition discipline) | Rule-25 dormancy vocabulary: 90-day default + exception KINDS (LONG-TTL-LIVE / CLOSED-PERIOD-IMMUTABLE / build-artifact) | **ADJACENT-COMPATIBLE** (fact-measurement vs classification vocabulary) | Site-Z rectangles CITE Rule-25 kinds in disposition cells rather than minting liveness words; kinds live in SYSTEM_DEFINITIONS |
| 7 | Recon matrix vs rectangle | rectangle = truth artifact of a decomposition subject | SSOT_RECON_MATRIX = CTO oversight tracker over 6 legs | **ADJACENT-COMPATIBLE** (workflow tracker vs truth artifact) | Tracker rows may cite rectangle/certification refs; never the reverse |
| 8 | Kimi SVP semantic-evolution vocabulary | (not yet mapped — awaiting delivery 3) | contract v2 manifests, adjudication states | **PENDING delivery 3** | — |
| 9 | CRO~B anchor-catalog / coordinate schema | (not yet mapped — awaiting delivery 3) | UNDISPATCHED under the hold (the first hold-lift release item) | **PENDING delivery 3** | — |

## 3. The written boundary (Step 3 — the paragraph both fabrics carry)

> **Site-Z's instruments atom_decomp program is CONFINED TO COMP TOOLING** (Andrew-direct
> 2026-08-11 @a7136a5aa9: "If you stay confined to comp tooling, I think it can work"): its
> subjects are comp-* tools and their registries/validators ONLY. The supervision/broker
> cluster (liveness, watcher, stimulus/fabric-check instruments) is **NOT pre-authorized** and
> requires Andrew's word post-integration. Laptop-side, the hold ("I will hold work on the
> laptop fabric in the interim") is **narrow-operative**: new semantic-structure FORMALIZATION
> acts are frozen — named queue item: CRO~B's substrate/anchor-catalog formalization
> (step-0 anchor-type extension, four ratified domain names, coordinate schema,
> codebase-extractor B6-1/B6-2), UNDISPATCHED at COO staffing, **released by Andrew's
> ratification of this integration** — while in-flight build/QA continues. Ontology axes are
> minted in ONE place per axis (SYSTEM_DEFINITIONS registration mandatory); the ATOM_DECOMP
> method package is one artifact edited through its owned-paths lane from either fabric.

## 4. Open to close before ratification

- Delivery 3 (CRO~B pack + CVO Kimi-SVP artifacts) → rows 8–9 + any new rows.
- Laptop per-row concurrence (CRO~B + CVO input, MSTR channel).
- Andrew ratification → laptop hold lifts (row-9 item releases first).
