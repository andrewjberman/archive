<to_id>NFRA_DTAFLP.TO-4</to_id>
<project>NFRA_DTAFLP</project>
<title>TO-4 FIRM-NATIVE: drop FIRM_ID env-switch in forked cot gold (8 FIRM_ID + 4 FIRM_NAME sites per 94c96ab4b map) + cherry-pick README</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0179 Andrew sovereign GO, PROCEED-REDUCED-SCOPE 205454Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- FIRM_ID env-switch DROPPED -> firm-native 'cottonwood', EXECUTED + deployed opal-data-cot (6ce1ff5fc: 8 FIRM_ID + 4 FIRM_NAME, fixed D_03:95/D_04:132 latent hardcode bug, README_FIRM_NATIVE_DIVERGENCE.md). GO LD-0179 (Andrew) released the writes ahead of the GLDINC-night-4 gate (firm-separation writes independent of GLDINC parity cutover). RAVC2-accepted by COO 2026-06-11 1622Z session.</status>

Execute the enumerated edit map (docs/briefs/dtaflp-to4-firmid-drop-enumeration-20260610.md): 8 FIRM_ID sites -> 'cottonwood' (incl D_03:95/D_04:132 hardcode fix + C_06 O6B_FIRM_ID -- hardcode or verify runner env), 4 FIRM_NAME sites -> 'Cottonwood Capital Advisors'. Zero S3 path migration (confirmed). FE consumer-check SAFE (CTO: pass-through label only). Add cherry-pick README for future 49F->cot patch flow. Rule 14 gates on every .py edit; Rule 13 deploy cycle. RAVC2 to COO + CTO.
