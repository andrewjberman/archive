# NFRA_ONTOLOGY -- per-ARN summary enrichment: the C2/C3 membership clause (COMPSIMILAR C3 unblocker, concrete)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-18. **Trigger:** Andrew-direct *"we need these classifications
included in the ARN node summary, essentially a list of any c2 c3 its included in."* **Status:** DRAFT --
the CONSUMER CONTRACT (my lane); **`~D` wires it into `derive_summary`** (the enricher owner). This is the
long-HELD COMPSIMILAR C3 clause, now concrete + LIVE-verified.

## 1. The ask (delivered as a deterministic membership clause)

Each per-ARN summary gains a clause listing **every C2 motif and C3 system the node is a member of**, each
carried with its classification label. Membership is DETERMINISTIC (graph edges); the class/description is the
additive LLM overlay (readability -- PERMITTED to read `llm_*`, per CTO's line; a summary is a human/agent
read, never a gate).

## 2. The deterministic membership lookup (LIVE-verified @HEAD 20:28Z)

For an ARN, reverse the materialized edges:
- **C2 membership:** `MATCH (m:C2Motif)-[:CONTAINS]->(node {arn}) RETURN m`  -- the motifs that CONTAIN the node.
- **C3 membership:** `MATCH (s:C3System)-[:CONTAINS]->(m) ...` -- the systems those motifs roll up to.

**VERIFIED, `opal-data-bd`:**
```
  in 4 C2 motifs : a-store, a-access, a-serve, b-io
  in 2 C3 systems: object-data (via a-store/a-access/a-serve/b-io), pipeline (via b-io)
```
(The overlap surfaces correctly -- `b-io` puts the bucket in BOTH object-data AND pipeline. A node in no
motif gets NO clause -- no guess.)

## 3. The clause (proposed format -- CONTENT is the ask; ~D owns exact rendering)

```
  membership: C2 [a-store(object-storage), a-access(compute-object-access),
                  a-serve(content-serving), b-io(pipeline-io)]
              C3 [object-data(data-platform), pipeline(data-pipeline)]
```
- Each entry: `<motif|system id>(<llm_class>)`. The `llm_class`/`llm_description` come from the classification
  bank (`NFRA_ONTOLOGY_LLM_CLASSIFICATION.md` @fc1b3c018) until the `llm_*` attrs are attached to the nodes
  (pending emit, behind the OWNS-bump), then from the node attrs directly -- same values.
- **No-guess:** absent membership -> no clause. **Coverage-denominatored:** "N of M summarized nodes carry a
  membership clause; K in no canonical motif" (reuses the UNKNOWN-thin control).
- **Sibling enrichment (~D convention):** a PARALLEL clause + its own `SummaryDoc.membership` field + render
  line -- NOT folded into the C2 motif-role splice (same shape as the variance_verdict contract).

## 4. Determinism + the no-feedback line (both hold)

- **Membership = deterministic** (graph CONTAINS edges) -- reproducible ground truth.
- **The class label = the additive LLM overlay** -- readability only. The summary READS `llm_*`; that is a
  PERMITTED consumer (human/agent readability), NOT a forbidden structural/gate read. The no-feedback lint is
  not tripped: the summary decides nothing structural.

## 5. Handoff

- **`~D`** -- wire the membership clause into `derive_summary` (`summary_corpus.py`): the deterministic C2/C3
  reverse-lookup + the class splice, as a sibling clause. This IS your HELD C3 clause -- now concrete, LIVE
  (13 motifs / 3 systems materialized), + verified. `base` FEEDs the derive_summary walkthrough.
- **me (~C)** -- own the membership contract + the classification bank; verify the enriched summary on a
  sample ARN once ~D wires it (expect opal-data-bd -> the 4-motif/2-system clause above).
- **base** -- coordinator/feed; the membership reverse-lookup Cypher is the exact query the enricher runs.

*-- 0.8.0_AE_CloudComp~C. Per-ARN C2/C3 membership summary contract; reverse-lookup verified on the live graph.*
