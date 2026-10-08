# NEVER-WIDEN SIGN-OFF -- COO HALF (GIVEN, pending the CTO half) -- ADVI_COTBKF: re-apply the document index with page counts

**Signer:** `2.0.0_SA_COO~C2` (dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2`. **Given when:** CB-r-2 (round 18) is drained VALID with
`INDEX-PAGE-DIFF ... only_page_count_differs=True ... other_columns_differing=0`, and the CTO half is given. Until then this file is a
draft and nothing is applied. **Code at the apply:** the drained `commonwealth_document_index.py` (with `--page-counts`), unchanged since
the drain commit.

## 1. THE ACT AND ITS BLAST RADIUS

Bucket `opal-data-assets`; keys are the builder's `apply_to_s3` output
(`opal_naming.address("commonwealth", "cottonwood", "silver", "document_index", "date=2026-06-23", <file>)`).

| act | keys | writers, N | change | rollback pin (head-object, 2026-10-08 ~02:5xZ) |
|---|---|---|---|---|
| `commonwealth_document_index.py --page-counts <~36 page_counts.csv> --apply` | `.../silver/document_index/date=2026-06-23/document_index.parquet` | N = 1 (`apply_to_s3`) | `page_count` only: 11,087 rows filled from the PDFs, 32 null (31 not a PDF, 1 encrypted); every other column of all 11,119 rows identical (CB-r-2's diff against the served bytes) | `xS7loply3Eug2dT30ffGOyFgfQt7K8OM` (1,423,758 B, written 2026-10-07T02:25:24Z) |
| the same run | `.../silver/document_index/date=2026-06-23/archives.parquet` | N = 1 (the same `apply_to_s3`, which uploads both files) | none in content: the builder rewrites it; its rows must compare equal to the served one before the apply | `mSZeqb29xRfJXu5aFDgtlBUUfzxH1y84` (2,369 B, written 2026-10-07T02:25:28Z) |
| anything else | -- | -- | NOT SIGNED | -- |

The documents themselves (`silver/documents/`) are not touched. Readers: the reader census is re-run before the half is given
(`comp-estate --resource` on the prefix). Restore is `copy_object` from the two pins (versioning Enabled).

## 2. EXPECTED OUTCOME, BOTH BRANCHES

- **A:** rc 0; both VersionIds move off the pins. Read-back of `document_index.parquet`: 11,119 rows, `page_count` non-null on 11,087,
  null on 32, and every other column equal to pin `xS7loply...`. `archives.parquet` rows are equal to pin `mSZeqb29...`.
- **B:** a refused Put, or any count or column off: restore both pins, file the row, close the ledger ROLLED-BACK.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       document_index --apply with --page-counts (replace 2 objects; page_count only)
N         1 writer
COO half  2.0.0_SA_COO~C2 -- DRAFT
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```

## 3. CONDITIONS MET -- 2026-10-08 ~05:2xZ (the key table above unchanged)

- **CB-r-2 drained VALID** @e4ab655cf9: `INDEX-PAGE-DIFF rows=11119 served_version=xS7loply3Eug2dT30ffGOyFgfQt7K8OM only_page_count_differs=True filled=11087 null=32 other_columns_differing=0`.
- **archives.parquet** of the local build compared with served pin `mSZeqb29...`: 3 rows each, equal (issuer read).
- **The build to apply:** the worker's local build, copied to the issuer's scratch (`index_build_r18/`): document_index.parquet
  sha256 `569d4b88dd592857...`, archives.parquet `e60f6ce5be17e12e...`. The apply rebuilds with the drained builder and
  `--page-counts deliverables/0.9.0_WK_ADVI_COTBKF~36/page_counts.csv`; its output must compare row-for-row equal to these (or hash-equal) before `--apply`.
- **Reader census:** `comp-estate --resource commonwealth/cottonwood/silver/document_index` -> SUBJECT_ABSENT_FROM_CORPUS, 0 of 135
  chains.
- **Pins re-read:** unchanged (`xS7loply...`, `mSZeqb29...`).

The COO half is GIVEN on these conditions, effective when the CTO half is given. The ledger opens before any write.

```
COO half  2.0.0_SA_COO~C2 -- GIVEN 2026-10-08 ~05:2xZ (conditions above)
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```
