<to_id>ADVI_PRTORG.AC-CLOSEOUT</to_id>
<project>ADVI_PRTORG</project>
<title>PRTORG AC1/AC4/AC7 close-out (gated on COTETL ownership_map artifact)</title>
<assigned_to>0.6.0_AE_PartnerETL</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 TO-file backfill, prd-check gap closure)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- 2026-06-17 structural verify PASS (CTO ruled chain-INDEPENDENT, COO GO 182810Z). AC1 (TF module org: partner-firms/cottonwood.tf + cot-pipeline + opal-partner-cottonwood DDB ACTIVE) PASS; AC4 (FE module: _partners/cottonwood 4 files + dispatcher + firmAccess, portal DEV) PASS; AC7 (ownership_map.json exists+well-formed, advisors:{} per §6.1 OUTCOME B) STRUCTURAL PASS. 1 deferred sub-check: AC7 freshness (generated_at 6/9, gold-chain-frozen, tracked via ADVI_COTETL.CHAINFIX) -- non-blocking. RAVC2 to COO 183552Z; COO does the 2-step atomic close.</status>

Close ADVI_PRTORG ACs 1/4/7 once the COTETL chain produces the ownership_map: verify the partner-firm instantiation surfaces against it per the PRTORG PRD v0.1 (Cottonwood driving instance; portal v2.1.119 PROD already live). RAVC2 to COO + CVO close-gate if all ACs met.
