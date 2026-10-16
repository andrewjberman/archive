# E4 measurement window: requests this seat made on opal-data-assets (for subtraction in E4_READER_MEASURE.md)

The eleven request-metrics configurations have been live since 2026-10-15T15:59:00Z. Requests the seat 0.7.0_AE_CloudOps~DELL1 itself made on `opal-data-assets` inside the window are listed here so the hourly table is read net of them. Sizes are from the records named; counts are not exact request counts.

| time (UTC) | act | prefix touched | record |
|---|---|---|---|
| 15:57-16:00 | L1 before print (list, head) | bucket-level, none inside the window | canon_r10_e4/L1_before_print.txt |
| 16:03-16:35 | gold-carry order: before and after prints of 16 served objects, 4 state keys, workbook listings (head, get for sha256), package zip get and put | portal/gold/mdpf/*, gold/mdpf_revamp/*, gateway/global/{bronze,silver}/taxsma_workbook/*, portal/gold/mdpf/_code/ | canon_r10_gold/*_print_*.json |
| 16:15:04 | put of the 1,958,957 B gold package | portal/gold/mdpf/_code/mdpf-gold-lambda.zip | ledger mdpf-canon-r10-gold-carry-deploy-dell1-20261015 |
| 16:19:38-16:20:54 | mdpf-gold-lambda qa_local invoke (the lambda's own reads of gold inputs and workbook snapshot writes) | portal/gold/*, gateway/global/* | canon_r10_gold/L4_response.json |
| 16:32:52-16:33:08 | publisher hand-run (reads opal-data-assets gold, writes opal-data-portal-v2, not this bucket) | portal/gold/mdpf/* | canon_r10_pub/L4_response.json |

Any later act of this seat on the bucket is appended below before the L3 read.
| 2026-10-16 16:08-16:12Z | r11 (ADHOC.canon-r11-muni-custom-deploy) before print: list+head+get of 16 served objects, 514 staged gold/mdpf_revamp keys (head + get), package zip get, manifest get; 1083 requests to opal-data-assets (r11_print.py counter), plus 3 each to opal-data-mdpf, opal-data-49financial, opal-data-cottonwood; the SMArtX/assignment partition reads (about 10 requests, one 52 KB parquet) | portal/gold/mdpf/*, gold/mdpf_revamp/*, gateway/global/*, smartx/platform/silver/*, blackdiamond/cottonwood/silver/fact_model_assignment/* | canon_r11_muni/canon_r11_before_print_20261016.json |
| 2026-10-16 16:17:32Z | put of the 1,985,336 B gold package; one get-object read back | portal/gold/mdpf/_code/mdpf-gold-lambda.zip | ledger mdpf-canon-r11-muni-custom-deploy-dell1-20261016 |
| 2026-10-16 16:24:19-16:25:39Z | mdpf-gold-lambda qa_local invoke (the lambda's own reads of gold inputs, workbook snapshot writes) | portal/gold/*, gateway/global/* | canon_r11_muni/L4_invoke.txt |
| 2026-10-16 16:27-16:29Z | r11 after print, same 1083 requests to opal-data-assets | same prefixes as the before print | canon_r11_muni/canon_r11_after_d4_20261016.json |
| 2026-10-16 15:42-16:30Z | the co-seated AE lanes on this box (IB2, DB2, ZS, SC1, HV1 and others) share the IAM user cloudops-dell1-agent-user; their requests on the bucket are NOT listed here and cannot be subtracted from the table | -- | git log of the day |
