# verify-channel — ADVI_INFNNA.P2.W4 RE-CERT: DATA-LAYER GREEN (city-key dup RESOLVED)

**archetype:** VALIDATE | **Reviewer:** 3.0.0_SA_CVO | supersedes the 1814Z CONDITIONAL cert
**Artifact:** s3://opal-data-inf/platinum/firm/advisor_nna_canonical.json (generated_at 2026-06-02T18:20:10Z; DS fix c1530451e)

## Verdict: W4 DATA-LAYER gate CLEAN GREEN

The 1814Z CONCERN (city-key case-variant duplicates) is RESOLVED. Independently re-verified on the served artifact:
- STRICT dup-key + casefold-collision parse (object_pairs_hook, mimics the PowerShell ConvertFrom-Json that caught it): **0 collisions** whole-artifact -> strict-JSON-safe. SNOHOMISH+Snohomish merged to single 'Snohomish'; 3 empty-dup pairs gone; 92->88 cities.
- W4 RIGID harness: **636 checks PASS, exit 0** — I1/I2/I3 partition (geo states/cities, advisor clients) all 9 windows to-the-cent; I4a YTD-identity (geo==firm==header $4,225,486.45); I4b q_current cross-view; I5 inflows/outflows; W6 all_pass=True/max_abs_delta=0.0/series_tie_max_abs_delta=0.0.
- DS added an in-build casefold-collision GUARD (hard-exits the emit) -> regression-proof. Belt-and-suspenders with my independent strict-parse.

## Scope of this GREEN (precise)
Certifies the W4 DATA-LAYER spine (W1 canonical artifact: partition-completeness + cross-view identity + strict-JSON integrity + W6 self-recon). The remaining W4 component — **AC4 universal fallback-removal** (no NNA surface, incl ADV-L1, resolves cumulative_chart.nna_geo/nna_adv) — is FE (W2/W3) + requires a code-grep; PENDING W2/W3 landing. I verify AC4 when the FE repoint + fallback-removal ship. Project closure also needs Andrew/CTO rendered-pixel visual smoke.

RAVC2 W4-data-GREEN to DS; CC CTO/COO.
— 3.0.0_SA_CVO
