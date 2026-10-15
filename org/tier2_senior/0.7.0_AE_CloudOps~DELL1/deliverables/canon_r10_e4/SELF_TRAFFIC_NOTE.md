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
