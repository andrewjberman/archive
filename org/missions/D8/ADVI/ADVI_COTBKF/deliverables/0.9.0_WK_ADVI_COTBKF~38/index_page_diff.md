# Commonwealth index page-count diff (CB-r-2)

Served: `s3://opal-data-assets/commonwealth/cottonwood/silver/document_index/date=2026-06-23/document_index.parquet` (VersionId `xS7loply3Eug2dT30ffGOyFgfQt7K8OM`, 11119 rows).
Built locally with `--page-counts page_counts.csv`; nothing was applied.

| measure | value |
|---|---:|
| built rows | 11119 |
| page_count filled | 11087 |
| page_count null | 32 |
| rows whose page_count moved | 11087 |
| rows differing in any other column (or held by one index only) | 0 |
| same columns and row keys | True |
| only page_count differs | True |

## Null rows by reason

- encrypted: 1
- not_a_pdf: 31

## The null rows

| document_id | doc_type | reason |
|---|---|---|
| ADVS201709211627321064a3f7-da0f-4ed3-bf13-aef1.pdf|469bee7d|12912 | ADVS | not_a_pdf |
| ADVS2017092211474294c17bd2-e7cd-48c3-b93b-1f90.pdf|469bee7d|12912 | ADVS | not_a_pdf |
| ADVS20200923185753e3d5200b-9852-4298-af2a-8d78.pdf|fe579bf4|13316 | ADVS | not_a_pdf |
| NCSD2016112216423525e08063-ffa2-4024-9ef4-3716.pdf|c5a65548|491 | NCSD | not_a_pdf |
| NCSD20161122164636f73c03cf-9d5f-473b-8306-b747.pdf|c5a65548|491 | NCSD | not_a_pdf |
| NCSD20170118180347ccff4ad2-aa11-483e-9e5f-14f9.pdf|6893f3fa|623 | NCSD | not_a_pdf |
| NCSD201701181810218a391c88-885a-4978-8f53-a707.pdf|6893f3fa|623 | NCSD | not_a_pdf |
| NCSD20170118181911864630b2-77c6-4f12-a396-2d11.pdf|6893f3fa|623 | NCSD | not_a_pdf |
| NCSD201701181825509edabf4e-8a4f-4b6a-b136-2f7a.pdf|6893f3fa|623 | NCSD | not_a_pdf |
| NCSD2017011910035387640ea7-ffd1-4355-b3b6-4928.pdf|7a5f778f|247 | NCSD | not_a_pdf |
| NCSD20170123101044beada002-9b29-4e8f-af6c-25af.pdf|7a5f778f|247 | NCSD | not_a_pdf |
| NCSD2017020112091132b06a72-0a2c-4e23-ae0b-b615.pdf|ff9947de|431 | NCSD | not_a_pdf |
| NCSD2017053011533921aa0e12-4e2b-48cc-ab6d-ecb7.pdf|e281e31e|1660 | NCSD | not_a_pdf |
| NCSD2017060117212693617918-eb59-4fc5-949d-75c0.pdf|48fa11e1|1106 | NCSD | not_a_pdf |
| NCSD20170601181329e9745884-504b-477b-8baf-21a4.pdf|48fa11e1|1106 | NCSD | not_a_pdf |
| NCSD20180501135837dca26ef7-6192-4e14-9de6-82d0.pdf|c9a2d0f1|75689 | NCSD | not_a_pdf |
| NCSD20181112142758239cf728-f56a-4367-894a-1809.pdf|7fe8f119|476 | NCSD | not_a_pdf |
| NCSD20220112224021aaf675bf-6dfb-4f98-9846-b430.pdf|4bdc6cd2|24412 | NCSD | encrypted |
| NCSD2022060914291065009b9f-cdcd-4c01-b0bd-db54.pdf|d1439359|1507 | NCSD | not_a_pdf |
| NCSD20230206180722bcdcacaa-5e16-4f43-bfaf-ce43be2efef4.pdf|00c2217d|9451 | NCSD | not_a_pdf |
| NCSD2023020618072302492024-2319-4843-af40-911812b52fc3.pdf|00c2217d|9451 | NCSD | not_a_pdf |
| NCSD2023020618072337d21540-59d1-432a-8cb6-7aa105e3204f.pdf|00c2217d|9451 | NCSD | not_a_pdf |
| NCSD2023020618072337eced3e-6488-400c-a82b-f785311a0eea.pdf|00c2217d|9451 | NCSD | not_a_pdf |
| NCSD202302061807233c5a5a61-d4cb-45fe-b574-f69cd9172344.pdf|00c2217d|9451 | NCSD | not_a_pdf |
| NCSD202302061807237591c886-db0d-4c9d-a4b8-7f08a3c8ff11.pdf|00c2217d|9451 | NCSD | not_a_pdf |
| NCSD2024020818385301d6067a-75e0-45ad-aeac-bbb2f5399c66.pdf|8a31866d|9252 | NCSD | not_a_pdf |
| NCSD2024020818385322ea0563-3c52-41bf-a7b8-9730141f6a4f.pdf|8a31866d|9252 | NCSD | not_a_pdf |
| NCSD2024020818385373ad33d1-81bd-46ae-b377-b05167c10e15.pdf|8a31866d|9252 | NCSD | not_a_pdf |
| NCSD20250724193521ee7a956f-e087-4ee5-bdb5-72f7c665623d.pdf|b974be7c|13808 | NCSD | not_a_pdf |
| NCSD202509020307438d0efaf1-f77d-453d-a9b6-d3102f9ac26d.pdf|7f030a5f|14290 | NCSD | not_a_pdf |
| NCSD202602270327482c4be2e7-b706-4b38-8a73-ce9e2b06b6ee.pdf|cd6346dc|72367 | NCSD | not_a_pdf |
| NCSD20260227033220ef5e1263-4dc1-4c55-a961-9bdd46205fc5.pdf|cd6346dc|72367 | NCSD | not_a_pdf |
