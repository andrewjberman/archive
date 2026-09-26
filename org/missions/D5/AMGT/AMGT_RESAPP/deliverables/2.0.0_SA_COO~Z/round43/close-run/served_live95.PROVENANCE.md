# FWD-30 on the served plane over the LIVE research library -- provenance of served_live95.tsv

| field | value |
|---|---|
| population | the LIVE research library (C-BACKFILL-DENOMINATOR-IS-THE-RESEARCH-FOLDER; Andrew's 2026-09-24 word) |
| folder read | `library.list_folders(library.library_root())`, root `...\OneDrive - Opal Capital\Shared - Documents\Asset Management\Research` |
| denominator | 95 folders |
| read_at | 2026-09-26T03:55:02Z (the log's first line) |
| deployed artifact | `opal-amgt-scoped-api` CodeSha256 `982nlz5TEI32UQZSqFqbtVwu7/qgVLPn89tMF6kmYvo=` (rr-3, LastModified 2026-09-25T23:22:39Z) |
| instrument | `round43/checks/sweep.py --served --live --require-cases` (fresh capture per name through lambda:Invoke; harness `exportCompare.harness.cjs` at portal DEV 53ccbc52, which carries rr-2's CASES grade) |
| result | served over 95 of 95 folders: OK 95, NOT_OK 0, CAPTURE_FAILED 0; cases over 95 of 95 compared names: page=285 rich=285 same=285 missing=0 extra=0 |

**The denominator moved as well as the numerator.** Round 42 read 89 of 94 on the live library at 18:42:56Z. Round 43's
rr-3 read 94 of 94 on the cut's pinned 94. This read covers 95, the 95th being AIA Group, which gained an identity at
23:48:58Z and a Model block afterwards (rows Z-S285, Z-S286).

Measured by `2.0.0_SA_COO~Z` after round 43's close, as input to `1.0.0_SA_CTO~Z`'s re-grade.
