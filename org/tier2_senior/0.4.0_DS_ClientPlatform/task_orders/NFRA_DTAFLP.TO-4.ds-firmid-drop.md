<to_id>NFRA_DTAFLP.TO-4</to_id>
<project>NFRA_DTAFLP</project>
<title>TO-4 FIRM-NATIVE: drop FIRM_ID env-switch in forked cot gold (8 FIRM_ID + 4 FIRM_NAME sites per 94c96ab4b map) + cherry-pick README</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0179 Andrew sovereign GO, PROCEED-REDUCED-SCOPE 205454Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>pending -- GO recorded (LD-0179). GATE: post-GLDINC-night-4 + after TO-1b retarget writes. FIRES VIA MORNING RESPAWN (LD-0176 -- DS offline overnight by design; COO morning cycle respawns + dispatches).</status>

Execute the enumerated edit map (docs/briefs/dtaflp-to4-firmid-drop-enumeration-20260610.md): 8 FIRM_ID sites -> 'cottonwood' (incl D_03:95/D_04:132 hardcode fix + C_06 O6B_FIRM_ID -- hardcode or verify runner env), 4 FIRM_NAME sites -> 'Cottonwood Capital Advisors'. Zero S3 path migration (confirmed). FE consumer-check SAFE (CTO: pass-through label only). Add cherry-pick README for future 49F->cot patch flow. Rule 14 gates on every .py edit; Rule 13 deploy cycle. RAVC2 to COO + CTO.
