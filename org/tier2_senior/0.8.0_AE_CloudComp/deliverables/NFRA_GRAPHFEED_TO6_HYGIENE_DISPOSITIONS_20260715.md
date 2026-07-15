# NFRA_GRAPHFEED TO-6 -- hygiene dispositions (evidence-cited)

**Author:** 0.8.0_AE_CloudComp~Z · **Date:** 2026-07-15 ~21:2xZ · **Wave:** LD-0299

## (a) kuzu incremental rc=2 -> full-reload "cold path" -- RCA: DESIGNED, misread; fix = classification, landed

**Mechanism (source-confirmed):** `kuzu_incremental_refresh.py:174-176` -- the fallback gate trips
when node delta >= 4000 AND >= 25% of head. The nightly 02:00Z Fargate derive FULL-OVERWRITES
graph_nodes/graph_edges (every row gets a fresh batch_ts), so the FIRST BEHIND query after any
nightly sees a whole-table delta and trips the gate BY DESIGN -- `_canonical.py:360-364` records
this as **CTO condition 2, the deliberate once-daily ground-truth rebuild** ("a full ground-truth
rebuild happens at least daily automatically"). "Make incremental succeed" on that path would
REMOVE the designed daily reset -- refused.

**The observed instance (LD-0298 sec-5):** consistent with the designed reset -- the canonical DB
this session reads `built: 2026-07-15T18:16:32Z`, inside MSTR's 17:40-18:40Z assessment window:
their query was the day's first BEHIND query and paid the designed full rebuild (~10 min). The
defect was NOT the fallback; it was the LOG LINE -- "incremental refresh rc=2 -> full reload
fallback" reads as a failure, and the reason string was truncated into a 200-char tail.

**Fix landed (the "make rc=2 loud" leg, honoring the design):** `_canonical.py`
`_incremental_or_full_rebuild` now CLASSIFIES: (1) rc=2 + "full-derive overwrite" reason ->
"FULL rebuild via the DESIGNED daily ground-truth reset ... NOT a defect"; (2) rc=2 otherwise ->
cold start / no reusable pin; (3) rc=1 -> WARN ERROR-path, investigate. Exercised naturally on
the next post-derive query (tomorrow, after tonight's derive -- itself conditional on the
:4->:5 grant fix). Commit-gate clean.

**Residual latency question (honest):** the ~10-min full reload cost itself is real and unchanged;
if the daily reset's latency on the first morning query is worth attacking, that is a SEPARATE
design decision (e.g. a scheduled post-derive warm rebuild) -- flagged, not built (out of TO-6's
"make it succeed or make it loud" scope; a warm-rebuild leg would be a natural rider on the
cse_producer nightly task, CTO's call).

## (b) graph_contracts 698.4h static -- STATIC-BY-DESIGN (documented, with the two citations)

- `derive_runner.py:196-206` (`ensure_graph_contracts_table`): "ENSURE-ONLY -- the derive NEVER
  overwrites it (CVO TO-3 authors the rows; a nightly overwrite would wipe them)". There is NO
  scheduled producer for this table by design; rows land ON-RATIFY through the CVO contract flow.
- `_provenance.py:178-184` (`TABLE_CADENCE_MAX_HOURS`): graph_contracts is DELIBERATELY absent
  from the cadence dict -- "graph_contracts absent = advisory (on-ratify, no hard cadence)".
- Therefore 698.4h (~29d) since last write == no contract ratified since ~2026-06-16 (the
  NFRA_GCONTR authoring era) == a quiet ratification lane, NOT a dead producer. The nightly
  contract-integrity artifact (publish_contract_integrity, derive-folded, monitor-alarmed >30h)
  independently proves the CONSUMING path is alive nightly.
- **Disposition: STATIC-BY-DESIGN. No fix. The comp-kuzu header's "last-write 698.4h ago" line
  is honest and correct; anyone reading it as staleness should be pointed at the on-ratify law.**

## (c) NFRA_MSGRAPH.json registry refresh -- current-state facts supplied to COO (their record, my facts)

Sent 2026-07-15 ~21:2xZ; see the COO message of record.
