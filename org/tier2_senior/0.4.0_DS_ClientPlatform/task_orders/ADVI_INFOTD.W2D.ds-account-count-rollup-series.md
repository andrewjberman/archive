<task_order>
<metadata>
  <to_id>ADVI_INFOTD.W2D</to_id>
  <project>ADVI_INFOTD</project>
  <title>DS-DATA: add per-model account_count[] columnar series to the MDPF aggregate-aua-timeseries rollup (firm-scoped Trend Count) + republish + served-verify</title>
  <assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED — DS off sanctioned-hold; parallel to RD~B INFOTD.W1. The DATA leg of W2; gates the trivial RD FE consume (INFOTD.W2F).</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct first-promotion-bundle. W2-FE + the held S5 promote wait on this served-verify.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFOTD.md (sec.3.W2 — root cause + 3-change fix)</ref>
    <ref type="fix_site">data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py:191-218 (drops account_count); slice_per_firm():357 (no change needed)</ref>
    <ref type="source">data/mdpf/scripts/gold/mdpf_aggregate_aua.py:316-326 (partition already emits account_count, model-holdings-only)</ref>
    <ref type="contract">docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md:181-183 (by_model[].account_count)</ref>
  </references>
</metadata>

<scope>
**Andrew-direct:** the firm-scoped ModelPortfolios Trend "Count" toggle renders nothing (global Count works). Root cause is DATA, not FE: the served per-firm by_model carries no account-count series even though the partition already computes it (model-holdings-only — exactly Andrew's intent: we do NOT assess non-model account counts).

## The fix (DATA leg — 1 change + republish + verify)
In `build_aggregate_aua_timeseries.py`, add a columnar `account_count[]` series to each `by_model` entry, MIRRORING the existing `model_value[]` accumulate/pad logic (:197-218): read `m.get("account_count")` alongside `m.get("model_value")`, pad `None` on absent dates. `slice_per_firm()` (:357) needs NO change (it spreads by_model). Optional parity: extend the global rollup's per-model series the same way (global Count already works off a separate aum-timeseries.json, so NOT blocking).

## MANDATORY post-steps (banked failure-modes — both bit MDPF this session)
1. **Re-run the rollup + republish (platinum -> json).** Per `feedback_mdpf_partition_reemit_needs_rollup_postdep`: a partition re-emit != serving fix — run `comp-pipescript postdeps` on the script to confirm the full post-chain.
2. **Verify the SERVED artifact, NOT the partition.** Per `feedback_partition_verify_neq_serving_verify_trace_consumer_rollup_path`: confirm `json/mdpf/{firm}/aggregate-aua-timeseries.json` (the FE-consumed artifact, BOTH 49financial + inflection) actually carries the new `account_count` field per by_model entry — check generated_at advanced + the field present, not just the partition. Reconcile the count to the per-day partition `by_model[].account_count`.

## Deploy
Standard DS gold/rollup deploy cycle (Rule 13 — DS owns commit->push->S3->comp-pipescript deployed MATCH->SSM dispatch). Pre-commit gate (Rule 14): ds-commit-gate.sh on the .py edit. This DATA change deploys INDEPENDENT of the portal promotion; the portal only needs the field present in the served artifact at render time.
</scope>

<acceptance>
- [ ] AC-W2D — build_aggregate_aua_timeseries.py emits account_count[] per by_model entry (model-holdings-only, padded on absent dates); rollup re-run + republished; `comp-pipescript postdeps` clean; SERVED json/mdpf/{firm}/aggregate-aua-timeseries.json (49financial + inflection) carries account_count, generated_at advanced, reconciles to the partition by_model[].account_count. CVO independent data-layer verify of the served artifact.
- Then signal RD~B (INFOTD.W2F) + COO that the served field is live so the 1-line FE consume is meaningful.

RAVC2 the served-verify evidence (the served artifact carries account_count, to a sample firm+model) to ws CTO + COO + CVO.
</acceptance>

<notes>
Decomposed by COO from ws CTO PRD e5f750f7f (Andrew-direct). This is your next real item off the sanctioned hold. W2-FE (RD~B: type portal-proxy.ts:407-413 + 1-line consume ModelPortfolios.tsx:476-479) is GATED on your served-verify — flag RD~B + COO when account_count is live in the served artifact. Model-only is preserved automatically (the partition count is already cohort_class-filtered; the FE Non-Model band is value-only). Numbers/dollar values unchanged — this ADDS a count series only.
</notes>
</task_order>
