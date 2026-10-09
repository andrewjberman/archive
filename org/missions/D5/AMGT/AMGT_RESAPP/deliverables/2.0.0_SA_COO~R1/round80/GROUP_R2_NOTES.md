# AMGT_RESAPP round 80 -- cell R2 drafting notes (the citation-heading parse)

Drafted 2026-10-09 by a read-only fork of `2.0.0_SA_COO~R1`. Source: CTO round-79 analysis R2 (`ledger/ROUND_ANALYSIS.round79.md`
@c249be336b); CVO L9 grade "For the analysis" item 2.

## Where the heading is built

- `lib/research/filings/passages.py:207-213` (`build_passage_map`): every excerpt line shorter than `_MIN_PASSAGE_CHARS` (60)
  becomes `pending_heading` and is written into the NEXT passage's `location` as `<item> / <heading> / paragraph N`. A table
  cell ("5.09%", "1", "(1)", "2025 2024 2023", "$1.19 ($20.38)", a lone U+200B) is under 60 characters, so it becomes a heading.
- The location is STORED at analysis time: `analyze.py:1403` builds the map into `filings/v1/<key>/<acc>.analysis.json`;
  `drafting_build.py:269` copies `passage["location"]` into `drafting/v1/<key>.json` `evidence_records[].source.location`.
- It is SERVED unchanged by `lib/research/api/scoped_amgt.py`: `_resolved_evidence` (:2850-2863), `_driver_point_passages`
  (:2866-2884), and the segment-row cite (:3804, reading the analysis `passage_map`). The print reads the same function
  (`lib/research/print/render_pack.py:594-605`). The page turns " / " into " > " (`portal/.../ThesisCards.tsx:244`).

## Census (read-only, 2026-10-09)

- `drafting/v1/`: 12 names, 1122 stored evidence records, 41 with a letterless heading; 272 served citations, 4 letterless
  (ASML NA P0064 "5.09%", P0065 "0.01%"; SAP GY P0139, P0143 a zero-width-space heading).
- `filings/v1/*.analysis.json`: 12 analyses, 3675 location fields, 74 letterless (BABA 19, NU 26, VLO 11, BA 5, ASML 4 ...).

## The fix shape (both ends, no re-run)

1. `passages.py`: `heading_has_words(line)` = any `str.isalpha()` character; `build_passage_map` skips a short line with no
   letter (it is neither a heading nor a passage, and it does not clear a pending real heading); `clean_location(location)`
   drops every middle segment with no letter. Future analyses store clean locations.
2. `scoped_amgt.py`: apply `passages.clean_location` to `location` at the three serve points. Stored objects are not
   rewritten; no model call, no store write.

Serving needs the `opal-amgt-scoped-api` redeploy (the round's deploy order, WORLD). The code cell itself is LOCAL.
`passages.py`/`analyze.py` are not on the census's site-Z producer list (@6a308cd424 rows 26-38 name `filings/battery.py`
hand-runs and the disabled `-FilingsAnalyzer` task only); the producer-side change takes effect at the next analysis run,
wherever it runs. OPEN for the issuer: whether `passages.py` counts as a FilingsAnalyzer producer path under CTO~DELL1
msg 1267 (the task is DISABLED, so no site-Z run moves on merge).

## Checks -- `checks/r80_r2.py`, dry-run at the base (box/dell1 @0e77b427cd)

- AC1 base: FAIL as expected (P1, P3, P4, P6, P7 FAIL; P2, P5 PASS; `R80 R2 AC1 SERVED: NO`, exit=1).
- AC2 base: FAIL as expected (S1 PASS 12 names; S2 PASS 41 stored; S3 FAIL 4 of 272 served; exit=1).
- AC3 base: PASS as expected (272 served, 0 changed, drift 0; `R80 R2 AC3 SERVED: YES`, exit=0).

AC2/AC3 read `s3://opal-data-harvest/drafting/v1/` (list + get) into a temp dir and serve through `AMGT_DRAFTING_ROOT`;
they write nothing. They do not cover the segment-row cite (:3804); the cell's tests must.
