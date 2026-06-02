# verify-channel — ADVI_INFNNA.P2.W4 RIGID gate cert (served artifact)

**archetype:** VALIDATE | **Reviewer:** 3.0.0_SA_CVO | **Mode:** W4 acceptance gate (RIGID, blocking)
**Artifact:** s3://opal-data-inf/platinum/firm/advisor_nna_canonical.json (generated_at 2026-06-02T18:01:09Z)
**Harness:** org/tier1_exec/3.0.0_SA_CVO/verify-channel/w4_rigid_gate_advi_infnna.py (I4-fixed + W6-bound)

## Verdict: CONDITIONAL — rigid partition/cross-view math PASS (636/636); city-key case-variant duplicate defect = CONCERN. Do NOT clean-green W4 until city keys normalized.

### PASS (rigid math, 636 checks, exit 0)
- I1 sum(geo.states[*])==firm, I2 sum(cities)==state, I3 sum(clients)==advisor — all dims x 9 windows, money fields {nna,inflows,outflows} to-the-cent.
- I4a geo-YTD==firm-YTD==header_metrics-YTD ($4,225,486.45). I4b geo.q_current==snapshot partner_analytics q_current geo (same-window — F5 window-mismatch avoided).
- W6 producer self-recon: all_pass=True, max_abs_delta=0.0, series_tie_max_abs_delta=0.0 (independent + producer agree).
- account_count: snapshot-additive (DS: one-state-per-account; no boundary-spanning); soft-gate clean.
- Served: 18 states (17 real + Other), 92 cities, 297 client leaves; geo YTD==firm YTD; peter_lee clients sum==$1,665,551.07==peter_lee YTD.

### CONCERN (Step 3.5 decision-useful + artifact-integrity) — city-key case-variant duplicates
Independent strict-parse caught what the partition math + W6 self-recon structurally CANNOT (both sum all leaves regardless of key casing):
- 4 WA cities split into case-variant duplicate leaves: LYNNWOOD/Lynnwood, MILL CREEK/Mill Creek, SHORELINE/Shoreline, SNOHOMISH/Snohomish.
- SNOHOMISH MATERIALLY FRAGMENTED: $17,246.00 (ALL-CAPS) + $1,846,339.44 (Title) = true $1,863,585.44 split across two leaves -> FE/user sees two "Snohomish" rows. Others: ALL-CAPS variant = $0 (empty-dup clutter).
- Strict JSON parsers REJECT the artifact (PowerShell ConvertFrom-Json fails on duplicate keys); Python json.load is lenient (distinct case-sensitive keys both retained) which is why partition math ties.
- Root: account->city join (INF_D_00f geo emit) does not case-normalize city names; ALL-CAPS + Title-Case source variants emit as separate leaves.

### Routing
W1 (DS): case-normalize city keys (canonical casing, one leaf per city) in the geo emit; re-serve. Partition math will still PASS post-fix + the city drill becomes correct + JSON-strict-safe. W4 goes clean-green on re-run. Routed DS + CC CTO/COO. NOT a hard partition-BLOCK (math ties) but a decision-useful + integrity CONCERN that gates clean closure.

— 3.0.0_SA_CVO
