<to_id>ADVI_COTETL.NIGHTLY-VERIFY</to_id>
<project>ADVI_COTETL</project>
<title>COTETL nightly chain morning verification: A_00->D_04 outputs + pipeline-complete marker + RAVC2</title>
<assigned_to>0.6.0_AE_PartnerETL</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 TO-file backfill, prd-check gap closure)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>pending -- GATE: tonight's 02:00Z chain runs unattended (LD-0176); this TO fires at morning artifact review</status>

Morning review of tonight's COTETL chain (02:00Z session -> 02:30Z bronze cron -> auto-silver -> auto-gold): verify cot gold A_00->D_04 outputs in opal-data-cot, pipeline logs clean, pipeline-complete marker present. Includes the staged Schwab 6-feed data flowing through. RAVC2 to COO. Downstream: ownership_map artifact unblocks ADVI_PRTORG AC1/AC4/AC7.
