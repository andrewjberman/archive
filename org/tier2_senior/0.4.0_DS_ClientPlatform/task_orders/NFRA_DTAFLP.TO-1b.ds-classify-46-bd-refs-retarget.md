<to_id>NFRA_DTAFLP.TO-1b</to_id>
<project>NFRA_DTAFLP</project>
<title>RETARGET + CLASSIFY: rewrite ~46 opal-data-bd refs in data/cot/scripts/gold -> opal-data-cot; classify each (dead / firm-local / shared-custodian-Schwab); route Schwab (c) set to CTO</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- RETARGET EXECUTED + deployed opal-data-cot (d892fe500: 7 live firm-local refs + Schwab default + in-file provenance, 9 gold files). LIVE MISS (shared lib/config.py S3_BUCKET default) caught + fixed in TO-1c (68c4cc541). RAVC2-accepted by COO 2026-06-11 1622Z session. Prior classification: 0e5b6e5f3 (73 refs); brief docs/briefs/dtaflp-to1b-cot-gold-bd-ref-classification-20260610.md.</status>

Classify all ~46 opal-data-bd references in data/cot/scripts/gold/ into (a) dead code, (b) firm-local (retarget to opal-data-cot), (c) shared-custodian Schwab (route ruling to CTO). Classification = read-only, safe now. Retarget writes follow the classification + night-4 clears. Rule 13 + Rule 14 gates apply on any .py edit. NOTE: TO-4 (FIRM_ID drop) is HELD pending Andrew DTAFLP go -- read-only prep enumeration permitted, no writes. RAVC2 to COO + CTO (the (c) set).
