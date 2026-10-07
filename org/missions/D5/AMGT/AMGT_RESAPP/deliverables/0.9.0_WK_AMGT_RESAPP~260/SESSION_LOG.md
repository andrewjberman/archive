# Session log -- 0.9.0_WK_AMGT_RESAPP~260 on AMGT_RESAPP.TO-AMGT-ay-4

- Baseline (before any edit), r75_served.py --cell c61 --where local: 36 bad segment headings of 95 names (BA: 10 headings incl. "ITEM 7..." x2, "BCA", "BGS total backlog of $29,720 million..."); table passages 3, without labels 3; R75 C61 SERVED: NO.
- Only 12 of the 95 covered names carry segment findings; only BA carries table passages (3).
- Segment names are read from stored text: abbreviation definitions in the filing analysis passages; names other findings of the same filing open on; "<Name> segment" in the sentence. Unnameable or multi-segment rows serve "Other" with segment_reason.
- Table labels: column header read from the stored filing text (filings/v1/<key>/<accession>.source.json excerpt) above the table; row labels from the passage's own lines. No SEC or vendor call.
- Commit 34e64fc16c: scoped_amgt.py (import, _segment_rows, _point_passage), segment_labels.py (new), tests/test_segment_labels.py (15 cases), rows AMGT_RESAPP-Z-W260-S1..S3.
- After: c61 C1 PASS (0 bad headings; BA = 3 names), C2 PASS (0 of 3 unlabelled); R75 C61 SERVED: YES. api suite 679 passed, 2 failed (test_scoped_amgt_mount, row S3).
