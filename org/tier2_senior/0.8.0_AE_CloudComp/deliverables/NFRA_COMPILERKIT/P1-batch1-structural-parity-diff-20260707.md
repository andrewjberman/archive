# COMPILERKIT-P1 batch-1 -- structural parity diff (recognizer-materialized vs LIVE trace_graph.build_graph)

**Author:** 0.8.0_AE_CloudComp~D | **Date:** 2026-07-07 ~1330Z
**Requirement:** P1 req #2 (the 2 lexical compilers reconciled as a parity-oracle pair, reproduce the current graph) -- the next parity slice flagged in `comp_recognizers_code.py`'s own NOTE ("full structural diff vs the LIVE extract_pipeline dispatch C1 = the next parity slice").

## Method

Ran `trace_graph.build_graph()` (the LIVE extractor, same one that feeds the served graph) and `comp_recognizers_code.parity_run()` (batch-1: DispatchCatalogRecognizer + MdpfDispatchRecognizer) side by side, filtered both to `edge_type == TRIGGERS` with `target.startswith('gold:')` (the dispatcher->gold-script class this parity-oracle targets; excludes the unrelated eventbridge->lambda TRIGGERS class which shares the same closed-vocab label), and diffed per dispatcher-source-script.

## Result by source script

| Source | live | recognizer | common | only-live | only-recognizer |
|---|---|---|---|---|---|
| `mdpf-daily-dispatch.sh` | 11 | 11 | 11 | 0 | 0 |
| `data/black_diamond/scripts/gold/gold_dispatch.sh` | 30* | 28 | 28 | 2 | 0 |
| `data/inf/scripts/gold/orion-gold-dispatch.sh` | 45 | 63 | 45 | 0 | 18 |

*BD live count is inflated by a subject-namespace collision -- see Finding 4.

## Findings (each grounded against source before being asserted)

**1. mdpf -- exact parity.** 0 diff. The MdpfDispatchRecognizer fully reproduces the live graph for this dispatcher. No action.

**2. BD `gold_dispatch.sh` -- 2 real gaps in the new recognizer, both explainable by scope, not bugs:**
   - `gold:gold_prof` -- grounded at `gold_dispatch.sh:317`: `python3 "$SCRIPTS/gold_prof.py" "$SCRIPTS/$filename" $flags` -- an OUTER-WRAP performance-telemetry invocation around every dispatched script (NFRA W2(a), CTO-ratified), not a CATALOG heredoc entry. DispatchCatalogRecognizer only parses the CATALOG block (lines 235-303) by design -- this is a distinct invocation pattern (wrapper-invoke) the current recognizer class doesn't target. Not a defect; a scope note for a future recognizer if this edge is wanted.
   - `gold:gldinc_ss4c_weekly` -- grounded at `gold_dispatch.sh:1397`: `python3 "$SCRIPTS/gldinc_ss4c_weekly.py" --run-date "$RUN_DATE"` -- a direct Wed-conditional invoke outside the CATALOG. **This is the SAME node already flagged as DEBTSCAN Blocker 1 (ss4c-dangle) in the base-lane wind-down handoff.** Confirms the mechanism precisely: the legacy `parse_gold_direct_invoke` recognizer (committed `75d93eaf7`) is NOT wired into `comp_recognizers_code.BATCH1` (currently `[DispatchCatalogRecognizer, MdpfDispatchRecognizer]` only -- no direct-invoke recognizer). Wiring an SDK-based direct-invoke recognizer closes both the COMPILERKIT parity gap AND the DEBTSCAN ss4c-dangle in one fix.

**3. Orion `orion-gold-dispatch.sh` -- 18 targets ONLY the recognizer catches (POSITIVE finding, not an over-match).** Spot-verified 2 of the 18 directly against source: `orion-gold-dispatch.sh:284-285` lists `INF_API_PULL_ASSETS_V2|pull_inflection_assets_v2.py|--upload-bronze` and `INF_API_SILVER_ASSETS_V2|convert_assets_v2_to_silver.py|...` as real CATALOG entries. These ARE genuine dispatcher->script relationships that exist in source but are ABSENT from the live `trace_graph.build_graph()` output -- i.e. the legacy extractor is under-catching/stale for orion's catalog, and the new SDK recognizer is MORE complete here, not noisier. (Did not spot-check all 18 individually -- pattern-consistent with the 2 verified, but flagging as unverified-by-sample for the remaining 16 per honesty discipline.)

**4. Firm-namespace subject collision (correctness concern, not yet a proven bug).** BD's and cot's `gold_dispatch.sh` both produce recognizer subject ref `dispatch:gold_dispatch` -- IDENTICAL despite being two different firms' scripts at two different paths (`data/black_diamond/...` vs `data/cot/...`). This is why the live-graph "gold_dispatch" row above shows 30 while BD-alone is 28: BD (28 targets) and cot (27 targets) sets nearly fully overlap under the collided subject key, which would understate true edge count if ever persisted node-per-subject-ref. Given CLAUDE.md's bd<->cot firm-separation NEVER-rule (gate-blocked at commit + IAM Deny at runtime for buckets/pipeline trees), a node-identity collision between the two firms' dispatch nodes in the shared graph is worth a CTO ruling before batch-2/3 recognizers compound the pattern -- e.g. does the subject ref need a firm-scoped prefix (`dispatch:bd:gold_dispatch` / `dispatch:cot:gold_dispatch`)? Not blocking P1 close; flagging now while it's cheap to fix.

## Verdict

Batch-1 (2/2 recognizers) is at **materialize-and-mostly-diff-clean parity** for mdpf (exact) and orion (recognizer is a strict superset, positively -- fixes a live staleness gap). BD has 2 explainable scope gaps, one of which (`gldinc_ss4c_weekly`) is the known DEBTSCAN blocker and has a concrete fix (wire a direct-invoke recognizer into `BATCH1`). One open correctness question (firm-namespace collision) needs a CTO ruling before it compounds across batch-2/3.

## Grounding citations
- `org/modules/graph/trace_graph.py:259` (`build_graph`) -- live extractor, exercised directly.
- `org/modules/graph/comp_recognizers_code.py:139` (`parity_run`) -- recognizer materializer, exercised directly.
- `data/black_diamond/scripts/gold/gold_dispatch.sh:317,1397` -- read directly, both citations verbatim-grounded.
- `data/inf/scripts/gold/orion-gold-dispatch.sh:235-303` (CATALOG heredoc) -- read directly, 2/18 targets spot-verified.
