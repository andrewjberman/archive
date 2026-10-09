# NFRA_TRNSPT round 15 -- close record: holdings categories from the canonical table (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `83a32cf5d2` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R15.md`, CTO ruling msg 2191 on row D2-W2-S3). TR-j15 merged `4ecf1633cb`:
`R15-J15-OK 6 passed`; drain on the merged tree 161 passed, 0 failed; `commit-gate.sh` clean; `round-close-check --round 15` MAY-CLOSE.

- **What `security_id` is:** an internal id of the form `S:<ticker>` (`docs/contracts/investor-reporting/v1/examples/RequestComposition.synthetic.json:156`),
  not a ticker. The join uses `original.identifier` only when `original.identifier_namespace` is `TICKER` (`:144`;
  `AnalysisRequest.schema.json:166-176`); any other namespace stays UNCLASSIFIED.
- **The join:** against the issuer's snapshot of DynamoDB `etf-classifications` (`data/transcripts/scripts/commentary/classification_source_20261009.json`,
  11,361 rows, ticker + asset_class + sub_asset_class). `holdings_categories` = asset class -> whole percent of CLASSIFIED weight (largest
  remainder); `holdings_coverage` = total, classified, coverage_pct and every unclassified identifier with its weight -- returned by `handler` beside
  the request (`results[i]["holdings_coverage"]`), never in `abstract_request` or `ticket_context`, so no identifier reaches the model.
- Row **D2-W2-S3** is resolved by this join (the normalized input's missing category is no longer needed).

Open at this close: the commentary Lambda's apply waits only on Andrew's standing Kimi word (dell2's open-calls list; CTO msg 2191); the Apple
exception awaits the CVO's review; row D2-S7 (household) is with the CTO and ~V2.
