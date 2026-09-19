# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~41 on AMGT_RESAPP.TO-AMGT-rk-39

Worktree `/c/tmp/wk-amgt-14-41`, branch `wk-amgt-14-41`, cut from SITEZ HEAD `047aee5478`.

## What was built

`lib/research/filings/document.py` (new): `FAMILIES`, `pdf_to_text` (PyMuPDF block reflow with
hyphen repair and CJK no-space joins), `detect_family`, `detect_language`, `period_end`, `cut`
(bounded 10-K/20-F mode reusing fetch.py's own algorithm verbatim except the removed 20-F bare
`riskfactors` fallback; heading mode for ANNUAL-REPORT/YUHO where each key closes at the nearest
OTHER declared key's qualifying heading, excluding the promiscuous `officers`/"Directors" pattern
as a boundary source), and a CLI (`--pdf-url/--sha256/--security-key/--family/--out-dir
[--pdf-file] [--coverage]`) that downloads-or-caches, verifies the hash, reflows, detects family
and language, cuts, and writes a LOCAL `<key>.source.json`.

`lib/research/filings/fetch.py` (modified): `extract_sections` now delegates to `document.cut`;
`SECTION_PATTERNS` and the whole compacted-text cutter moved to document.py; the officer-section
write and the no-item UNRESOLVED-SOURCE reason both carry the cut's own per-key FAILED reason
(E10); `PARSER_VERSION` 1.0.0 -> 1.1.0. Every EDGAR-specific function (`http_get`, `latest_filing`,
`html_to_text`) is unchanged -- these were accidentally deleted in an over-wide first edit and
restored verbatim from the pre-cell file before any test ran.

`lib/research/filings/tests/test_document.py` (new): 9 tests on synthetic text (D9, E10 x2,
UNKNOWN x2, YUHO three-headings, language x2, a 10-K-family sanity check).

`lib/research/filings/__init__.py` (modified): one paragraph naming document.py.

## Key measurements against the two real documents (CSL, Keyence)

Both PDFs downloaded once (sha256 verified against the order's own recorded hashes, byte-identical),
cached under `.scratch/docs/_pdfcache/` for determinism-check re-runs. `detect_family` returned
ANNUAL-REPORT (CSL) and YUHO (Keyence) exactly as the order names; `period_end` returned
2026-06-30 and 2026-03-20 exactly as the order names; `detect_language` returned en and ja.

Coverage: reproducing the order's own cited D12 figures (9.3%/91.6% CSL, 1.8%/92.4% Keyence)
required scoping the raw-vs-reflow passage-coverage comparison to the "risk" item's own pages
alone -- risk+mdna combined, or the whole document, both read far off those figures (see
INVESTIGATION_v1.md row W41-S1). Once scoped to risk's own pages: CSL raw=8.94%/reflow=93.79%,
Keyence raw=2.08%/reflow=94.41%.

A second, independent defect was found and fixed in the coverage instrument itself:
`passages.build_passage_map`'s stored `text` field is ASCII-converted (`to_ascii`), which strips
CJK characters to almost nothing; computing "non-blank characters covered" from that field read
Keyence's genuinely well-reflowed text as ~6% covered. Reading each passage's `[start, end)` span
back into the ORIGINAL (pre-ASCII-conversion) text fixed this without touching passages.py (not
this cell's surface) -- see `document._coverage_share`.

CSL's own real primary risk-factors heading is "Material Risks" (verified against the reflowed
text at reflow offset 58707, and the TOC at offset 9717) -- a phrase not contained in any of the
order's four declared ANNUAL-REPORT risk phrases. The cutter instead resolves a different, real,
substantial heading also literally named "Risk management" inside CSL's Governance/ERMF section
(chars 8192, opens with a genuine ERMF description, not a story or cross-reference). See
INVESTIGATION_v1.md row W41-S2.

## Mutation control

Temporarily restored the removed bare `r"riskfactors"` 20-F fallback in document.py; the new D9
test (`test_a_line_opening_mid_sentence_mention_never_becomes_the_risk_section`, whose fixture
places "risk factors" at a genuine line-start with no Item-3/D or bare-D prefix, mirroring the
coincidental line-wrap shape D9 measured on CSL's own raw text) FAILED exactly as expected
(`'OK' != 'FAILED'`). Reverted immediately; the full 29-test suite was re-run and confirmed green
on the restored file.

## Gates run

`python -m py_compile`, `python .tools/ds-precommit-check.py`, `ruff check --target-version py39`
on all four changed/new `.py` files: all clean. ASCII check
(`len(b) - len(b.decode('utf-8')) == 0`) on all four files: 0 each.

## Surprise rows filed

`AMGT_RESAPP-Z-W41-S1` (coverage excerpt scope not order-legible) and `AMGT_RESAPP-Z-W41-S2`
(CSL's real "Material Risks" heading not in the declared phrase list) -- both OBSERVATION/INERT,
appended by textual splice inside `INVESTIGATION_v1.md`'s one fenced JSON array; the pre-existing
content was diffed (`git diff`) to confirm zero bytes of any existing row were altered.
