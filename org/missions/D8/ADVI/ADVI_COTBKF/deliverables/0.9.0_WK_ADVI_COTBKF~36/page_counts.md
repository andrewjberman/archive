# Commonwealth document page counts (CB-q-3)

Source: `s3://opal-data-assets/commonwealth/cottonwood/silver/document_index/date=2026-06-23/document_index.parquet` (listing fields) and `s3://opal-data-assets/commonwealth/cottonwood/silver/documents/date=2026-06-23/documents.parquet` (written_key per document).

## Cause: what the archive listing carries in NumberOfPages

| doc_type | documents | listing none | listing zero | listing positive | listing other |
|---|---:|---:|---:|---:|---:|
| ADVS | 165 | 165 | 0 | 0 | 0 |
| CLNT | 932 | 932 | 0 | 0 | 0 |
| NCSD | 1239 | 1239 | 0 | 0 | 0 |
| REPR | 13 | 0 | 0 | 0 | 13 |
| STMT | 7736 | 7736 | 0 | 0 | 0 |
| TXRP | 1034 | 0 | 1034 | 0 | 0 |
| ALL | 11119 | 10072 | 1034 | 0 | 13 |

`page_count` in the index comes only from the listing's NumberOfPages; with no positive value in any listing the index column cannot be filled from the listing. `other` is present but not a whole number (folded into listing_none on the last line).

## Pages counted from the PDF bytes

| doc_type | documents | counted | unreadable |
|---|---:|---:|---:|
| ADVS | 165 | 162 | 3 |
| CLNT | 932 | 932 | 0 |
| NCSD | 1239 | 1210 | 29 |
| REPR | 13 | 13 | 0 |
| STMT | 7736 | 7736 | 0 |
| TXRP | 1034 | 1034 | 0 |

Unreadable by reason: encrypted=1, not_a_pdf=31

Documents whose bytes do not match the documents-table sha256: 0

PAGE-COUNTS documents=11119 counted=11087 unreadable=32 listing_none=10085 listing_zero=1034 listing_positive=0 cause=absent
