<to_id>ETFS_SETUP.W3</to_id>
<project>ETFS_SETUP</project>
<title>ETFS_SETUP W3 (AE~B) -- Cottonwood daily ETF-ownership producer (COTETL gate cleared)</title>
<assigned_to>0.7.0_AE_CloudOps~B</assigned_to>
<consult>0.4.0_DS_ClientPlatform (daily-slice contract)</consult>
<verify>3.0.0_SA_CVO</verify>
<issued_by>2.0.0_SA_COO (ETFS_SETUP decomposition wave-3; Andrew-direct 2026-06-23 "get started"; PRD docs/architecture/ETFS_SETUP.md)</issued_by>
<issued_date>2026-06-23</issued_date>
<status>pending</status>
<!-- GATED on W1 (bucket REUSE + IAM + config + contract). B3 (COTETL CurrentDay freeze) CLEARED -- fix deployed a7a4d974c 2026-06-22 + cot now GO-LIVE ($397.98M@06-22, render+served verified). So W3 is unblocked beyond the W1 foundation. AE~B lane. -->

<objective>
Build the Cottonwood leg of the ETFS write-out model: a cot daily ETF-ownership producer that writes opal-data-etfs/cottonwood/{date}.json per the W1 daily-artifact contract, reading the cot pipeline (opal-data-cot) ONLY.
</objective>

<the_work>
1. COT DAILY PRODUCER: reads opal-data-cot gold (canonical_holdings, or the A_05 assets_dim now built) -> filters to the 4-ETF universe (W1 config) -> aggregates per-ETF market_value -> writes opal-data-etfs/cottonwood/{date}.json per the W1 contract. Cot is now daily-current (COTETL fix + go-live; served $397.98M@06-22).
2. Write-out model: reads opal-data-cot ONLY + writes opal-data-etfs/cottonwood/ prefix; comp-iam-verify no firm-bucket-Deny widening, no cross-firm read (NEVER#1 by construction). NEVER reference the bd bucket (cot is firm-separated from bd).
</the_work>

<compiler_tools_mandate>
comp-which-first; comp-iam gaps/service (cot producer write-out grant); ds-commit-gate (from __future__ import annotations); safe-deploy firm-sep (cot tree -- NEVER bd). comp-iam-verify no cross-firm read.
</compiler_tools_mandate>

<acceptance_criteria>
1. Cot daily producer writes opal-data-etfs/cottonwood/{date}.json per the W1 contract (4 ETFs, source_as_of, market_value sane vs the cot AUA); comp-iam-verified write-out.
2. Reads opal-data-cot ONLY; firm-sep (never bd); no cross-firm read.
3. GATED on W1 landing; RAVC2 COO + CVO. Signals AVGCAP-W3 (Cottonwood leg) once the slice is live.
