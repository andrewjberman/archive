# NFRA_ONTOLOGY -- Empirical Grain Scan (bottom-up grounding of the vocabulary + grain)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Trigger:** Andrew-direct (verbatim below). **Status:**
DRAFT -- doctrine-shaping, RAVC MSTR + CTO. Companion to the top-down `NFRA_ONTOLOGY_DESIGN_OF_RECORD.md`
(v0.2) -- this is the EMPIRICAL complement (synthesis, not replacement).

**Andrew-direct (VERBATIM):** *"we never really talked about the vocabulary, how can we expand the vocabulary
in a meaningful high signal way? I feel like we should do some kind of scan across the whole kuzu graph and
assemble every c1 and c2 and try to figure out how to really qualify the language in c3, if we're really
doing everything we can be doing, taking advantage of the granularity or if we're even at the right level of
grain in the vocabulary that defines motifs."*

**MSTR doctrine guardrail (binding):** the right grain **MAXIMIZES SIGNAL** -- NOT "one motif per observed
shape" (a 500-shape vocabulary is a census, not a language -- the catch-all failure one layer up). The grain
is where a motif is COARSE enough to RECUR meaningfully AND FINE enough to DISTINGUISH shapes that mean
different things. Deliverable = a GRAIN DECISION justified by the distribution + high-signal additions each
earning its place by frequency+distinctness. **Print the denominator of every distribution.**

**Provenance (Rule 20):** `comp-kuzu` DB `kuzu_nessie_db`, built 2026-07-18T02:18Z (age ~2.6h), Nessie HEAD
CURRENT (pin==marker), graph_nodes last-write 2.7h ago. Fresh, authoritative vintage.

---

## 1. The real C0/C1 population (denominators)

| Layer | Count | vs my top-down | vs canon-patterns | vs CSE |
|---|---|---|---|---|
| **C0 node types** | **58 distinct** / 20,336 nodes | 11 roles | 23 | 28 |
| **C1 edge types** | **53 distinct** / 35,613 edges | 11 relationships | 16 | 24 |
| **C1 typed triples** `(src)-[edge]->(tgt)` | **109 distinct** | -- | -- | -- |
| **C2 motifs materialized** | **6** (all DEBT; see S3) | -- | 4 pattern-classes | -- |
| **C3 systems materialized** | **1** (`EmergentSystem` -- degenerate/debt: member_motifs = the 3 debt motifs, theme "firm-conditional-display") | -- | -- | -- |

**Finding 1 -- the live vocabulary is ~2x richer than any design input.** 58 node types incl. many neither
canon-patterns nor my design named: `MS_FILE` (4582), `MS_FOLDER` (1031), `MS_USER`, `PipelineFunction`
(1201), `PipelineScript`, `Prop` (359), `PanelCluster` (91), `Page`, `S3Key` (232), `ReactQueryKey`,
`DataFetch`, `TypeDecl` (807), `SSM_DOCUMENT`, `SECURITY_GROUP`, `INSTANCE_PROFILE`, `SERVICE_PRINCIPAL`,
`LAMBDA_LAYER`, `KMS_KEY`. Nodes also carry a `layer` (the L1-L7 stack axis) and a `drift_class` property --
a drift signal ALREADY on the node.

**Finding 2 -- the estate is 4 clean planes** (from the triple grammar): **M365/filesystem** (CONTAINS +
OWNED_BY tree), **React/frontend** (RENDERS/READS_FIELD/PROP_PASSES/INSTANTIATES/CLUSTERS), **pipeline/data**
(CALLS/FLOWS_TO/READS_S3/WRITES_S3/RUNS), **cloud/IAM** (READS/WRITES/ASSUMES/HAS_POLICY/TRIGGERS/ROUTES_TO).

---

## 2. THE GRAIN DECISION (the crux of Andrew's question)

Three candidate grains, sized against the live graph:

| Grain | Distinct shapes | Verdict |
|---|---|---|
| **Instance** (raw edges) | 35,613 | a census -- zero compression. WRONG (too fine). |
| **Abstract archetype** (my 11 relationships) | ~11 | great for NAMING, but collapses `READS_S3`/`READS_SECRET`/`READS_FIELD` into one `consumes` -- LOSES the distinction that makes a motif mean something. TOO COARSE to DEFINE motifs. |
| **Typed triple / typed path** (`src_type`-`edge`-`tgt_type`) | 109 triples; **197** distinct 2-hop path-shapes | **RIGHT.** Tractable AND target-qualified. |

**The 2-hop typed path filtered by recurrence -- the high-signal motif set (denominator: 101,712 total
2-hop paths / 197 distinct shapes):**

| recurrence >= K | high-signal motifs | paths covered | coverage |
|---|---|---|---|
| >= 5  | 156 | 101,619 | 99.9% |
| >= 10 | 134 | 101,459 | 99.7% |
| **>= 50**  | **92**  | 100,552 | **98.9%** |
| **>= 100** | **69**  | 98,942  | **97.3%** |

**THE DECISION:** a motif is a **typed multi-hop path at recurrence >= ~50-100**. At that grain, **~70-90
motifs cover ~98% of the estate**, and the noise tail (197 - ~90 = ~105 rare shapes) covers only ~1%. This
is precisely MSTR's target: coarse enough to recur (each recurs 50-100x+), fine enough to distinguish (typed
endpoints separate S3-read from secret-read), and NOT a census (the vocabulary is ~70-90, not 197 or 35,613).

**THE 3-GRAIN MODEL (the "take advantage of granularity" answer):** keep ALL THREE, each with its job --
(a) **instance** = C0/C1 raw (ground truth, LAW-1); (b) **typed-path @ recurrence>=K** = the MOTIF-DEFINING
grain (C2, where the granularity is exploited -- the target-type qualifier is the signal); (c) **archetype**
= the agnostic NAMING/compression layer (my top-down set) that sits ABOVE and describes motifs in
plain-English. The top-down design got layer (c) right; it never built (b).

---

## 3. THE BIGGEST FINDING -- the canonical motif/system layer has NEVER been mined

The 6 materialized `C2Motif` nodes are **ALL DEBT/deviation motifs** (from the debtscan canon-DEVIATION
scorer, catalog classes A1-A9): `SilentDisplayFork`, `CrossFirmAsymmetry`, `HardcodedFirmLiteral`,
`DeadComponent`, `OrphanEndpoint`, `RenderWithoutNullGuard`. **Zero CANONICAL/structural motifs.** The lone
materialized C3 system (`EmergentSystem`) is itself DEGENERATE -- its `member_motifs` are the 3 debt motifs
(silent-display-fork / cross-firm-asymmetry / hardcoded-firm-literal), theme "firm-conditional-display". So
the ONE system is a debt-cluster, not a canonical capability.

So the estate has catalogued only its NEGATIVE space (what is broken) and never its POSITIVE structure (what
the system normally IS). The top-20 structural motifs the scan surfaced -- all recurrence >= 900, NONE
materialized -- are the canonical language that is missing:

```
S3Key OWNED_BY S3_BUCKET CONTAINS S3Key             28902   (the S3 storage motif)
LAMBDA READS  S3_BUCKET CONTAINS S3Key              10425   (the Lambda->S3 access motif)
Module REFERENCES_TYPE TypeDecl HAS_FIELD Field      7185   (the type-usage motif)
LAMBDA WRITES S3_BUCKET CONTAINS S3Key               6312
MS_FOLDER CONTAINS MS_FILE OWNED_BY MS_USER          4569   (the M365 file-custody motif)
EC2 RUNS PipelineScript CONTAINS PipelineFunction    2402   (the pipeline-run motif)
JSXRender RENDERS Field FLOWS_TO Field               1742   (the render-dataflow motif)
PipelineScript CONTAINS PipelineFunction CALLS ...   1623   (the pipeline-call motif)
JSXElement INSTANTIATES ReactComponent PROJECTS_TO   1298   (the component-projection motif)
LAMBDA ASSUMES IAM_ROLE HAS_POLICY IAM_POLICY         914   (the IAM-assume motif)
```

**"Are we doing everything we can be doing?" -- No, emphatically.** The raw granularity is all present; it
has simply never been compressed into a canonical C2/C3 layer. The vocabulary work is therefore not only
"name a few archetypes" -- it is **mine the canonical motif layer at the decided grain** so C2/C3 is populated
with the estate's real structural language (currently 6 debt-only nodes).

---

## 4. HIGH-SIGNAL vocabulary additions the top-down set MISSED (each earns its place by frequency + distinctness)

| Addition | Evidence | Why it is distinct (not a duplicate of an existing archetype) |
|---|---|---|
| **`owns` -- a CSE-RECONCILIATION item (NOT a clean add; base C-1)** | `OWNED_BY` = **5,845 edges, the #2 relationship**. `MS_FILE OWNED_BY MS_USER` (4582 = custody), `S3Key OWNED_BY S3_BUCKET` (232 = containment-inverse). | **`OWNED_BY` is POLYSEMOUS:** custody (`MS_FILE OWNED_BY MS_USER` -- a genuine gap) vs containment-inverse (`S3Key OWNED_BY S3_BUCKET` = `contains`, already covered). And **CSE already treats ownership 3 ways** -- `cse_schema.py:306` maps `OWNED_BY -> Relationship.GOVERNS` (coarse, lumped with `HAS_POLICY`); `:143` carries `OWNERSHIP` as a first-class **Qualifier** (a different axis); `comp_coverage_check.py:523` uses it as the containment-rollup direction. So `owns` is **not a clean coverage-gap** -- it must route to CTO as a **CSE-schema RECONCILIATION** (disambiguate custody vs containment-inverse; decide whether custody splits out of `GOVERNS`, promotes the `OWNERSHIP` Qualifier, or is a Custodian-role treatment), reconciled under S5 (no fork). **Do NOT pre-lock it on the RELATION axis.** |
| **`shares-source` / a LATERAL-sibling relationship** | `SHARES_SOURCE` (`PanelCluster SHARES_SOURCE PanelCluster`, 55). | A LATERAL (peer-to-peer) edge -- literally the Variance/twin signal MATERIALIZED as a C1 edge. Validates the Variance operator has real graph signal; a candidate deterministic input to it. |
| **target-type QUALIFIER on `consumes`/`produces`** | `READS`(708)/`READS_S3`(323)/`READS_FIELD`(2110)/`READS_SECRET`(240)/`READS_URL`(48)/`FETCHES`(109); `WRITES`/`WRITES_S3`. | The graph SUBTYPES read/write by WHAT is read. "reads a secret" vs "reads a field" are different motif-roles. The abstract `consumes` must carry the target-type qualifier (kept as an adapter refinement, surfaced in the motif) -- else the motif layer loses its highest-signal distinction. |
| **the HAS_* family disambiguation** | `HAS_FIELD`(4269)/`HAS_PROP`(359)/`HAS_KEY`(85)/`HAS_TYPE`(100)/`HAS_ROUTE`(82)/`HAS_POLICY`(548)/`HAS_PROFILE`(32). | Mostly `contains` (structural membership) -- BUT `HAS_POLICY`/`HAS_PROFILE` are governance ATTACHMENTS (an IAM policy/profile), closer to `guards`. The scan forces the ruling: which HAS_* are `contains` vs `guards`. |
| **code-plane relations** `DECLARES`/`INSTANTIATES`/`REFERENCES_TYPE`/`CALLS` | 1344/1298/1129/1623. | Per D3/D8 mostly the definitional axis -- BUT `CALLS` (invocation) and `FLOWS_TO` (data derivation, 961) are relational (`triggers`/`derives-from`). The scan confirms the D3/D8 scope-out is correct for `DECLARES`/`REFERENCES_TYPE` (definitional) and IN for `CALLS`/`FLOWS_TO` (relational). |

---

## 5. What this means for the top-down design (synthesis)

1. **Layer (c) archetypes were right for NAMING/compression** -- 53 edge-types -> ~11 archetypes is a ~5:1
   compression with real recurrence. Keep the closed set (CTO gate stands).
2. **ADD the missed archetypes:** `owns`/Custody + `shares-source`/lateral -- both high-frequency + distinct.
   (RAVC to the CTO closed-set ruling as empirically-forced additions -- D-decisions, not a re-litigation.)
3. **BUILD layer (b) -- the motif layer -- at the typed-path @ recurrence>=~50-100 grain.** This is the real
   NFRA_ONTOLOGY expansion Andrew is asking for: mine the ~70-90 canonical structural motifs (currently 0
   materialized) so the C2 layer describes what the estate IS, not only its 6 deviations. Then C2->C3
   (connected motif components, NFRA_SYSTEM's existing promotion) can populate the currently-empty C3.
4. **The target-type qualifier travels WITH the abstract relationship** into the motif -- the adapter maps
   `READS_SECRET -> consumes(target=SECRET)`, and the motif keeps the qualifier; the archetype name drops it.

---

## 6. Proposed next (RAVC MSTR + CTO -- doctrine-shaping)

- **NEXT-A (me):** the full typed-motif catalog at recurrence>=K -- the ~70-90 canonical motifs, named in
  archetype terms, as the seed C2 vocabulary. (This is the concrete "assemble every C2" Andrew asked for,
  at the decided grain.)
- **NEXT-B (me):** fold `owns`/Custody + `shares-source`/lateral + the HAS_* / target-qualifier rulings into
  the closed-set proposal (as empirically-forced D-decisions for the CTO gate).
- **NEXT-C (coordinate):** the motif-mining runs on NFRA_SYSTEM's promotion mechanism (I do NOT re-implement
  it) -- the grain decision (recurrence>=K, typed-path) is the parameter it needs; loop 0.4.0_DS~B
  (consultant) on whether the current promotion is grain-parameterizable.
- Grain + vocabulary ARE the language -> RAVC MSTR (doctrine) + CTO (arch). Denominators printed throughout.

*-- 0.8.0_AE_CloudComp~C. Empirical grain scan, all figures from comp-kuzu @2026-07-18T02:18Z (HEAD current).*
