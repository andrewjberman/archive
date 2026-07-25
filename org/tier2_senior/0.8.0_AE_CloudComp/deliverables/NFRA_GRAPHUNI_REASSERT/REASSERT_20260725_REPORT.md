# NFRA_GRAPHUNI.P2/D2 -- Fresh Coverage-Parity Re-Measurement (CVO~Z dispatch 20260725T055641Z)

**Author:** `0.8.0_AE_CloudComp~D` · **2026-07-25** · **Ruling chain:** Andrew-direct "reopen it, have CVO
deal with it" -> CVO~Z dispatch (independently re-verified my prior claims before ruling) -> this
measurement · **Verifies:** `3.0.0_SA_CVO~Z`

**Method:** the existing P0-CVO fixture's own deterministic recipe (`FIXTURE_ATTESTATION.md` §7), not a new
approach. `repro_1`'s sample reused unchanged. `repro_2_capture_layer_a.py` re-pointed: monkeypatched
`cli._get_graph()` to return `comp_marker_read.py`'s `as_tracegraph()` projection instead of the local
`.comp-graph/graph.json` cache, then drove the REAL `cli.main()`/`cmd_blast`/`cmd_trace`/`cmd_xref` code
paths in-process (argv simulated, stdout captured) -- the answer-formatting logic is byte-identical to
production; only the graph source changed. S3 ids canonicalized firm-aware per §7's precondition
(`NFRA_GRAPHUNI.P1-D.bucketless_to_qualified.json`, expand-before-compare) so a bucket-qualification
difference cannot masquerade as a coverage gap. Script:
`deliverables/NFRA_GRAPHUNI_REASSERT/repro_2_capture_layer_a_REPOINTED.py` (this lane's own path, not
CVO~B's fixture directory -- read from there, wrote nothing there).

**comp-platinum NOT re-measured this pass** -- confirmed via source read that it does not consume
`TraceGraph`/`.comp-graph/graph.json` at all (a separate routing/DAG/dataflow cache, `graph_cache.py`), so a
clean graph-source swap does not apply to it. Flagged, not silently skipped; a comp-platinum re-measurement
needs a different method (re-pointing `extract_routes`/`extract_pipeline`'s AWS-resource inputs), out of
scope for this pass.

---

## Headline result: **13/45 (29%) match. The regression is REAL and STILL PRESENT today -- not resolved by
a month of estate growth. But it is sharper and more localized than the month-old finding suggested.**

| Tool | Match | Rate |
|---|---|---|
| `comp-blast` | 11/28 | 39% |
| `comp-trace` | 2/8 | 25% |
| `comp-xref` | 0/9 | 0% |
| **Total** | **13/45** | **29%** |

Marker-head grounding: `marker_head=5957908056775835011`, `built_at=2026-07-24T18:01:18Z` (yesterday, live).

## The specifically-requested sharp case: `gold:D_01.partner_analytics` blast radius

**Script-level target (the exact case cited a month ago, expected 216): re-derived TODAY at 13.**
Near-identical to the month-old number -- **this is not a stale finding, it reproduces cleanly on fresh
data.** All 19 canonicalized ids present in the new answer are a strict subset of the old 239; the 20
missing (of many more truncated) are entirely OTHER gold script/function nodes
(`gold:A_00.accounts_dimension`, `gold:A_01.advisor_assignments`, `gold:A_02.fee_rate_history`,
`gold:A_03.positions_cube`, `gold:B_00.canonical_holdings`, ...) -- real cross-script dependencies the old
TraceGraph carried and the marker-head projection does not currently surface for this target. Zero extras
(the new answer is a strict subset, never a false-positive addition).

**Function-level target `gold:D_01.partner_analytics:generate_header_metrics` (expected 39): MATCHES
EXACTLY. 39/39, zero missing, zero extra.** This is the sharper finding this pass adds: **the regression is
NOT uniform across the family -- function-grain blast radius is clean; script-grain is where it breaks.**

## Why this points precisely at one mechanism, not "kuzu is generally incomplete"

`comp_marker_read.py`'s own `_project()` docstring names the exact suspect: a **"SCRIPT-GRAIN s3 ROLLUP"**
step that exists specifically to roll function-level `READS_S3`/`WRITES_S3` edges up to their containing
script (existential: a script reads/writes s3 iff a contained function does), because the pre-delta
TraceGraph modeled this at BOTH grains (script<->s3, 445 edges + some function-grain, 131) while the
marker-head compute population is function-grain only. **The clean function-level match + the broken
script-level match is exactly the signature this rollup mechanism would produce if it under-populates**
(the direct function-to-function/function-to-s3 edges resolve fine; the derived script-to-script
reachability THROUGH a shared s3 artifact does not fully materialize).

## comp-xref: 0/9, but two different failure shapes -- not one defect

Read past the headline 0% (per the attestation's own §5 discipline: gross rates hide detector-specific
weakness):
- **6 of 9 cases are NEAR-misses** (e.g. `log`: old=80/new=81; `gold/dimensions/accounts_dimension_latest.parquet`:
  old=1/new=1, zero missing either way) -- these fail the STRICT set-equality bar but the deltas are small
  and one-directional (extras, not losses), consistent with **legitimate growth since the fixture's 2026-06-30
  vintage**, not a coverage regression. `getPlatinumPartnerAnalytics`: old=1/new=1 but 5 portal component
  files missing -- likely a real, separate gap (portal-side xref), not measured further this pass.
- **2 of 9 are COMPLETE zero-coverage**: `data/black_diamond/scripts/gold/D_04.client_portal_summary.py`
  (old=50, new=**0**) and `data/inf/scripts/gold/INF_D_04.client_portal_summary.py` (old=64, new=**0**).
  Both are **file-path-form** xref queries against script-level nodes -- the same grain (script, not
  function) that the blast-radius finding above already implicates. This is corroborating evidence for the
  same root cause from a second, independent tool, not a new mystery.

## What this changes about the 3-option architectural decision

The month-old finding was aggregate (node/edge totals, one flagship blast number). This pass's function-vs-script
split is new information relevant to choosing among the three options CVO~Z named:
- **"Re-populate at build_graph fidelity"** and **"re-run build_graph pinned to marker head"** are both
  broader than what the evidence now supports needing -- the gap looks concentrated in ONE mechanism (the
  script-grain rollup / cross-script-via-s3 reachability), not a wholesale population shortfall.
- **"Re-baseline the fixture"** would paper over a real, reproducible, still-present gap -- not recommended
  on this evidence.
- **A fourth option this measurement surfaces, not previously named:** targeted repair of the script-grain
  rollup logic in `comp_marker_read.py::_project()` specifically, re-measured against this same fixture
  before any broader re-population work. Smaller, more targeted than the three original options -- routing
  as a finding, not a ruling (design decision, CVO~Z's/CTO~Z's call).

## Denominator + honesty notes

45 total targets attempted (28 blast + 8 trace + 9 xref) = the full deterministic sample, none skipped or
sampled-down. `comp-platinum` (16 + 4 = 20 more targets in the full fixture) explicitly NOT attempted this
pass, stated above, not silently absent from the totals. Full per-target detail (all 45, including the
missing/extra id lists truncated to 15-20 in this report) in
`deliverables/NFRA_GRAPHUNI_REASSERT/REASSERT_20260725_result.json`.

**What this lane did NOT do:** did not modify `cli.py`, `platinum_cli.py`, or `comp_marker_read.py` --
read-only, in-process monkeypatch confined to this measurement script. Did not attempt to fix the
script-grain rollup gap. Did not re-measure comp-platinum. Did not choose among the disposition options --
routing the sharper finding back to CVO~Z per the ruling chain.
